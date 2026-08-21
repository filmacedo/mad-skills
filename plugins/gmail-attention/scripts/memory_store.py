#!/usr/bin/env python3
"""Small, dependency-free local memory store for Gmail Attention.

The store keeps persona preferences, operational state, feedback, and shared-policy
candidates separate. It intentionally does not store Gmail message bodies.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


SCHEMA_VERSION = 1
MAX_RUNS = 100
MAX_DEDUPE = 500

PERSONA_FILE = "persona.json"
STATE_FILE = "state.json"
FEEDBACK_FILE = "feedback.jsonl"
CANDIDATES_FILE = "policy-candidates.jsonl"

SENSITIVE_KEYS = {
    "body",
    "message_body",
    "raw_message",
    "raw_mime",
    "html_body",
    "credentials",
    "access_token",
    "refresh_token",
    "raw_headers",
    "action_link",
    "href",
}

CLASSIFICATIONS = {
    "human_correspondence",
    "events",
    "content",
    "updates",
    "notifications",
    "transactions",
    "cold_outreach",
    "other",
}
ATTENTION_LEVELS = {"act_now", "act_later", "fyi", "routine_cleanup", "suspicious"}
PREFERENCE_ACTIONS = {
    "keep_inbox",
    "label",
    "archive",
    "label_and_archive",
    "unsubscribe",
    "report_spam",
    "block",
    "notify_only",
    "suppress_digest",
}
DIGEST_VISIBILITY = {"action", "fyi", "cleanup", "hidden"}
PREFERENCE_SOURCES = {"explicit_user_feedback", "audit_approval", "imported"}
PREFERENCE_STATUSES = {"active", "proposed", "disabled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _atomic_json_write(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_name, 0o600)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _touch_private(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    os.chmod(path, 0o600)


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _read_json_argument(raw: str) -> Dict[str, Any]:
    if raw.startswith("@"):
        return _read_json(Path(raw[1:]))
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("--json must contain a JSON object")
    return value


def _append_jsonl(path: Path, value: Dict[str, Any]) -> None:
    _reject_sensitive_keys(value)
    _touch_private(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, separators=(",", ":")))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _reject_sensitive_keys(value: Any) -> None:
    found = sorted({key for key in _walk_keys(value) if key.lower() in SENSITIVE_KEYS})
    if found:
        raise ValueError(f"sensitive fields are not allowed: {', '.join(found)}")


def init_store(root: Path, user_id: str = "") -> None:
    root.mkdir(parents=True, exist_ok=True)
    timestamp = now_iso()
    persona_path = root / PERSONA_FILE
    state_path = root / STATE_FILE

    if not persona_path.exists():
        _atomic_json_write(
            persona_path,
            {
                "schema_version": SCHEMA_VERSION,
                "user_id": user_id,
                "created_at": timestamp,
                "updated_at": timestamp,
                "mailboxes": [],
                "preferences": [],
                "output_preferences": {
                    "timezone": "UTC",
                    "voice": "concise",
                    "account_tags": True,
                    "maximum_focus_items": 3,
                },
            },
        )

    if not state_path.exists():
        _atomic_json_write(
            state_path,
            {
                "schema_version": SCHEMA_VERSION,
                "updated_at": timestamp,
                "mailboxes": {},
                "runs": [],
            },
        )

    _touch_private(root / FEEDBACK_FILE)
    _touch_private(root / CANDIDATES_FILE)


def _validate_timestamp(value: Any, field: str, issues: List[str]) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        issues.append(f"{field} must be a string or null")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        issues.append(f"{field} is not an ISO-8601 timestamp")


def _parsed_timestamp(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed


def _validate_string_list(value: Any, field: str, issues: List[str]) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        issues.append(f"{field} must be an array of strings")
    elif len(value) != len(set(value)):
        issues.append(f"{field} must not contain duplicates")


def _validate_mailbox(mailbox: Any, field: str, issues: List[str]) -> None:
    if not isinstance(mailbox, dict):
        issues.append(f"{field} must be an object")
        return
    required = ("address", "connection", "timezone", "allowed_labels", "allowed_actions")
    missing = [key for key in required if key not in mailbox]
    if missing:
        issues.append(f"{field} missing {', '.join(missing)}")
    for key in ("address", "connection", "timezone"):
        if key in mailbox and (not isinstance(mailbox[key], str) or not mailbox[key].strip()):
            issues.append(f"{field}.{key} must be a non-empty string")
    if "address" in mailbox and isinstance(mailbox["address"], str) and "@" not in mailbox["address"]:
        issues.append(f"{field}.address must be an email address")
    for key in ("allowed_labels", "allowed_actions"):
        if key in mailbox:
            _validate_string_list(mailbox[key], f"{field}.{key}", issues)


def _validate_preference(preference: Any, field: str, issues: List[str]) -> None:
    if not isinstance(preference, dict):
        issues.append(f"{field} must be an object")
        return
    required = (
        "id",
        "scope",
        "action",
        "digest_visibility",
        "source",
        "confidence",
        "status",
        "created_at",
        "updated_at",
        "reason",
    )
    missing = [key for key in required if key not in preference]
    if missing:
        issues.append(f"{field} missing {', '.join(missing)}")
    if "id" in preference and (not isinstance(preference["id"], str) or not preference["id"]):
        issues.append(f"{field}.id must be a non-empty string")
    if "scope" in preference and not isinstance(preference["scope"], dict):
        issues.append(f"{field}.scope must be an object")
    if "matcher" in preference and not isinstance(preference["matcher"], dict):
        issues.append(f"{field}.matcher must be an object")
    enum_fields = {
        "classification": CLASSIFICATIONS,
        "attention": ATTENTION_LEVELS,
        "action": PREFERENCE_ACTIONS,
        "digest_visibility": DIGEST_VISIBILITY,
        "source": PREFERENCE_SOURCES,
        "status": PREFERENCE_STATUSES,
    }
    for key, allowed in enum_fields.items():
        if key in preference and preference[key] not in allowed:
            issues.append(f"{field}.{key} has an unsupported value")
    confidence = preference.get("confidence")
    if confidence is not None and (not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1):
        issues.append(f"{field}.confidence must be between 0 and 1")
    if "standing_permission" in preference and not isinstance(preference["standing_permission"], bool):
        issues.append(f"{field}.standing_permission must be a boolean")
    if "reason" in preference and not isinstance(preference["reason"], str):
        issues.append(f"{field}.reason must be a string")
    if "example_message_ids" in preference:
        _validate_string_list(preference["example_message_ids"], f"{field}.example_message_ids", issues)
    for key in ("created_at", "updated_at", "expires_at"):
        if key in preference:
            _validate_timestamp(preference[key], f"{field}.{key}", issues)


def _validate_jsonl(path: Path, required: Iterable[str], issues: List[str]) -> None:
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append(f"{path.name}:{index} invalid JSON: {exc.msg}")
                continue
            if not isinstance(value, dict):
                issues.append(f"{path.name}:{index} must be a JSON object")
                continue
            missing = [key for key in required if key not in value]
            if missing:
                issues.append(f"{path.name}:{index} missing {', '.join(missing)}")
            try:
                _reject_sensitive_keys(value)
            except ValueError as exc:
                issues.append(f"{path.name}:{index} {exc}")


def validate_store(root: Path) -> List[str]:
    issues: List[str] = []
    required_files = [PERSONA_FILE, STATE_FILE, FEEDBACK_FILE, CANDIDATES_FILE]
    for name in required_files:
        if not (root / name).exists():
            issues.append(f"missing {name}")
    if issues:
        return issues

    try:
        persona = _read_json(root / PERSONA_FILE)
        _reject_sensitive_keys(persona)
        for field in ("schema_version", "user_id", "created_at", "updated_at", "mailboxes", "preferences", "output_preferences"):
            if field not in persona:
                issues.append(f"persona.json missing {field}")
        if persona.get("schema_version") != SCHEMA_VERSION:
            issues.append("persona.json has unsupported schema_version")
        if not isinstance(persona.get("mailboxes"), list):
            issues.append("persona.json mailboxes must be a list")
        else:
            addresses = []
            for index, mailbox in enumerate(persona["mailboxes"]):
                _validate_mailbox(mailbox, f"persona.mailboxes[{index}]", issues)
                if isinstance(mailbox, dict) and isinstance(mailbox.get("address"), str):
                    addresses.append(mailbox["address"].strip().lower())
            if len(addresses) != len(set(addresses)):
                issues.append("persona.json mailboxes must have unique addresses")
        if not isinstance(persona.get("preferences"), list):
            issues.append("persona.json preferences must be a list")
        else:
            preference_ids = []
            for index, preference in enumerate(persona["preferences"]):
                _validate_preference(preference, f"persona.preferences[{index}]", issues)
                if isinstance(preference, dict) and isinstance(preference.get("id"), str):
                    preference_ids.append(preference["id"])
            if len(preference_ids) != len(set(preference_ids)):
                issues.append("persona.json preferences must have unique ids")
        if not isinstance(persona.get("output_preferences"), dict):
            issues.append("persona.json output_preferences must be an object")
        _validate_timestamp(persona.get("created_at"), "persona.created_at", issues)
        _validate_timestamp(persona.get("updated_at"), "persona.updated_at", issues)
    except (ValueError, json.JSONDecodeError) as exc:
        issues.append(f"persona.json: {exc}")

    try:
        state = _read_json(root / STATE_FILE)
        _reject_sensitive_keys(state)
        for field in ("schema_version", "updated_at", "mailboxes", "runs"):
            if field not in state:
                issues.append(f"state.json missing {field}")
        if state.get("schema_version") != SCHEMA_VERSION:
            issues.append("state.json has unsupported schema_version")
        if not isinstance(state.get("mailboxes"), dict):
            issues.append("state.json mailboxes must be an object")
        if not isinstance(state.get("runs"), list):
            issues.append("state.json runs must be a list")
        _validate_timestamp(state.get("updated_at"), "state.updated_at", issues)
    except (ValueError, json.JSONDecodeError) as exc:
        issues.append(f"state.json: {exc}")

    _validate_jsonl(
        root / FEEDBACK_FILE,
        ("id", "recorded_at", "kind", "user_feedback", "interpretation"),
        issues,
    )
    _validate_jsonl(
        root / CANDIDATES_FILE,
        ("id", "recorded_at", "status", "proposed_rule", "rationale", "regression_case", "counterexamples"),
        issues,
    )
    return issues


def _require_fields(value: Dict[str, Any], fields: Iterable[str], name: str) -> None:
    missing = [field for field in fields if field not in value]
    if missing:
        raise ValueError(f"{name} missing required fields: {', '.join(missing)}")


def upsert_preference(root: Path, preference: Dict[str, Any]) -> None:
    init_store(root)
    _reject_sensitive_keys(preference)
    _require_fields(
        preference,
        ("id", "scope", "action", "digest_visibility", "source", "reason"),
        "preference",
    )
    timestamp = now_iso()
    preference = dict(preference)
    preference.setdefault("confidence", 1.0)
    preference.setdefault("status", "active")
    preference.setdefault("standing_permission", False)
    preference.setdefault("expires_at", None)
    preference.setdefault("example_message_ids", [])
    preference.setdefault("created_at", timestamp)
    preference["updated_at"] = timestamp

    preference_issues: List[str] = []
    _validate_preference(preference, "preference", preference_issues)
    if preference_issues:
        raise ValueError("; ".join(preference_issues))

    persona_path = root / PERSONA_FILE
    persona = _read_json(persona_path)
    preferences = persona.setdefault("preferences", [])
    existing_index = next((index for index, item in enumerate(preferences) if item.get("id") == preference["id"]), None)
    if existing_index is None:
        preferences.append(preference)
    else:
        preference["created_at"] = preferences[existing_index].get("created_at", preference["created_at"])
        preferences[existing_index] = preference
    persona["updated_at"] = timestamp
    _atomic_json_write(persona_path, persona)


def upsert_mailbox(root: Path, mailbox: Dict[str, Any]) -> None:
    init_store(root)
    _reject_sensitive_keys(mailbox)
    mailbox = dict(mailbox)
    if isinstance(mailbox.get("address"), str):
        mailbox["address"] = mailbox["address"].strip().lower()
    issues: List[str] = []
    _validate_mailbox(mailbox, "mailbox", issues)
    if issues:
        raise ValueError("; ".join(issues))

    persona_path = root / PERSONA_FILE
    persona = _read_json(persona_path)
    mailboxes = persona.setdefault("mailboxes", [])
    existing_index = next(
        (
            index
            for index, item in enumerate(mailboxes)
            if isinstance(item, dict)
            and str(item.get("address", "")).strip().lower() == mailbox["address"]
        ),
        None,
    )
    if existing_index is None:
        mailboxes.append(mailbox)
    else:
        mailboxes[existing_index] = mailbox
    persona["updated_at"] = now_iso()
    _atomic_json_write(persona_path, persona)


def set_output_preferences(root: Path, preferences: Dict[str, Any]) -> None:
    init_store(root)
    _reject_sensitive_keys(preferences)
    if not isinstance(preferences, dict):
        raise ValueError("output preferences must be an object")
    if "maximum_focus_items" in preferences:
        maximum = preferences["maximum_focus_items"]
        if not isinstance(maximum, int) or not 1 <= maximum <= 5:
            raise ValueError("maximum_focus_items must be an integer from 1 to 5")
    if "account_tags" in preferences and not isinstance(preferences["account_tags"], bool):
        raise ValueError("account_tags must be a boolean")

    persona_path = root / PERSONA_FILE
    persona = _read_json(persona_path)
    persona.setdefault("output_preferences", {}).update(preferences)
    persona["updated_at"] = now_iso()
    _atomic_json_write(persona_path, persona)


def append_feedback(root: Path, event: Dict[str, Any]) -> None:
    init_store(root)
    event = dict(event)
    event.setdefault("recorded_at", now_iso())
    event.setdefault("digest_run_id", None)
    event.setdefault("mailbox", None)
    event.setdefault("message_ids", [])
    event.setdefault("applied_preference_id", None)
    event.setdefault("reconciliation", None)
    _require_fields(event, ("id", "kind", "user_feedback", "interpretation"), "feedback")
    _append_jsonl(root / FEEDBACK_FILE, event)


def append_policy_candidate(root: Path, candidate: Dict[str, Any]) -> None:
    init_store(root)
    candidate = dict(candidate)
    candidate.setdefault("recorded_at", now_iso())
    candidate.setdefault("status", "pending")
    candidate.setdefault("counterexamples", [])
    candidate.setdefault("source_feedback_ids", [])
    _require_fields(
        candidate,
        ("id", "proposed_rule", "rationale", "regression_case"),
        "policy candidate",
    )
    if candidate["status"] != "pending":
        raise ValueError("new policy candidates must have status=pending")
    _append_jsonl(root / CANDIDATES_FILE, candidate)


def record_run(root: Path, run: Dict[str, Any]) -> None:
    init_store(root)
    _reject_sensitive_keys(run)
    _require_fields(run, ("id", "started_at", "completed_at", "mailboxes"), "run")
    if not isinstance(run["mailboxes"], dict):
        raise ValueError("run.mailboxes must be an object keyed by mailbox address")

    state_path = root / STATE_FILE
    state = _read_json(state_path)
    mailbox_state = state.setdefault("mailboxes", {})

    for address, result in run["mailboxes"].items():
        if not isinstance(result, dict):
            raise ValueError(f"run.mailboxes.{address} must be an object")
        status = result.get("status")
        if status not in {"complete", "incomplete"}:
            raise ValueError(f"run.mailboxes.{address}.status must be complete or incomplete")

        current = mailbox_state.setdefault(
            address,
            {
                "last_successful_cutoff": None,
                "recent_dedupe": [],
                "pending_reconciliation": [],
            },
        )
        if status == "complete":
            cutoff = result.get("cutoff")
            if not cutoff:
                raise ValueError(f"complete mailbox {address} requires cutoff")
            cutoff_time = _parsed_timestamp(cutoff, f"run.mailboxes.{address}.cutoff")
            existing_cutoff = current.get("last_successful_cutoff")
            if existing_cutoff and cutoff_time < _parsed_timestamp(
                existing_cutoff, f"state.mailboxes.{address}.last_successful_cutoff"
            ):
                raise ValueError(f"complete mailbox {address} cannot move its checkpoint backward")
            current["last_successful_cutoff"] = cutoff
            dedupe = list(current.get("recent_dedupe", []))
            dedupe.extend(str(item) for item in result.get("dedupe_keys", []))
            current["recent_dedupe"] = list(dict.fromkeys(dedupe))[-MAX_DEDUPE:]

    run_summary = dict(run)
    state.setdefault("runs", []).append(run_summary)
    state["runs"] = state["runs"][-MAX_RUNS:]
    state["updated_at"] = now_iso()
    _atomic_json_write(state_path, state)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize a memory root")
    init_parser.add_argument("--root", required=True, type=Path)
    init_parser.add_argument("--user-id", default="")

    validate_parser = subparsers.add_parser("validate", help="validate a memory root")
    validate_parser.add_argument("--root", required=True, type=Path)

    for command in (
        "upsert-mailbox",
        "set-output-preferences",
        "upsert-preference",
        "append-feedback",
        "append-policy-candidate",
        "record-run",
    ):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--root", required=True, type=Path)
        command_parser.add_argument("--json", required=True, help="JSON object or @path/to/file.json")

    context_parser = subparsers.add_parser("context", help="print persona and state JSON")
    context_parser.add_argument("--root", required=True, type=Path)
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        if args.command == "init":
            init_store(args.root, args.user_id)
        elif args.command == "validate":
            issues = validate_store(args.root)
            if issues:
                for issue in issues:
                    print(issue)
                return 1
            print("memory store valid")
        elif args.command == "upsert-preference":
            upsert_preference(args.root, _read_json_argument(args.json))
        elif args.command == "upsert-mailbox":
            upsert_mailbox(args.root, _read_json_argument(args.json))
        elif args.command == "set-output-preferences":
            set_output_preferences(args.root, _read_json_argument(args.json))
        elif args.command == "append-feedback":
            append_feedback(args.root, _read_json_argument(args.json))
        elif args.command == "append-policy-candidate":
            append_policy_candidate(args.root, _read_json_argument(args.json))
        elif args.command == "record-run":
            record_run(args.root, _read_json_argument(args.json))
        elif args.command == "context":
            print(
                json.dumps(
                    {
                        "persona": _read_json(args.root / PERSONA_FILE),
                        "state": _read_json(args.root / STATE_FILE),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
