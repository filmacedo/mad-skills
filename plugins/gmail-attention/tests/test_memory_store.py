import importlib.util
import json
import multiprocessing
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "memory_store.py"
SPEC = importlib.util.spec_from_file_location("gmail_attention_memory", SCRIPT)
memory = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(memory)


def record_run_after_delayed_state_read(root, run, state_read):
    original_read_json = memory._read_json

    def delayed_read_json(path):
        value = original_read_json(path)
        if path.name == memory.STATE_FILE:
            state_read.set()
            time.sleep(0.5)
        return value

    memory._read_json = delayed_read_json
    memory.record_run(Path(root), run)


def record_run_in_process(root, run):
    memory.record_run(Path(root), run)


class MemoryStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / ".gmail-attention"
        memory.init_store(self.root, "person-1")

    def tearDown(self):
        self.temp_dir.cleanup()

    def read_json(self, name):
        return json.loads((self.root / name).read_text(encoding="utf-8"))

    def test_init_and_validate(self):
        persona = self.read_json("persona.json")
        self.assertEqual(persona["user_id"], "person-1")
        self.assertEqual(memory.validate_store(self.root), [])

    def test_upsert_preference_preserves_identity_and_created_at(self):
        preference = {
            "id": "archive-retired-org",
            "scope": {"mailbox": "person@example.com"},
            "matcher": {"authenticated_org": "Example Org"},
            "classification": "notifications",
            "attention": "routine_cleanup",
            "action": "label_and_archive",
            "digest_visibility": "cleanup",
            "source": "explicit_user_feedback",
            "reason": "User is no longer an active member",
        }
        memory.upsert_preference(self.root, preference)
        first = self.read_json("persona.json")["preferences"][0]

        preference["reason"] = "Updated reason"
        memory.upsert_preference(self.root, preference)
        second = self.read_json("persona.json")["preferences"][0]

        self.assertEqual(second["reason"], "Updated reason")
        self.assertEqual(second["created_at"], first["created_at"])
        self.assertEqual(len(self.read_json("persona.json")["preferences"]), 1)

    def test_partial_preference_update_preserves_optional_fields(self):
        memory.upsert_preference(
            self.root,
            {
                "id": "archive-retired-org",
                "scope": {"mailbox": "person@example.com"},
                "matcher": {"authenticated_org": "Example Org"},
                "classification": "notifications",
                "attention": "routine_cleanup",
                "action": "label_and_archive",
                "digest_visibility": "cleanup",
                "source": "explicit_user_feedback",
                "reason": "User is no longer an active member",
                "standing_permission": True,
                "expires_at": "2027-08-21T07:00:00Z",
                "example_message_ids": ["message-1"],
            },
        )

        memory.upsert_preference(
            self.root,
            {
                "id": "archive-retired-org",
                "scope": {"mailbox": "person@example.com"},
                "action": "archive",
                "digest_visibility": "hidden",
                "source": "explicit_user_feedback",
                "reason": "Updated without repeating optional fields",
            },
        )

        preference = self.read_json("persona.json")["preferences"][0]
        self.assertEqual(preference["matcher"], {"authenticated_org": "Example Org"})
        self.assertEqual(preference["classification"], "notifications")
        self.assertEqual(preference["attention"], "routine_cleanup")
        self.assertTrue(preference["standing_permission"])
        self.assertEqual(preference["expires_at"], "2027-08-21T07:00:00Z")
        self.assertEqual(preference["example_message_ids"], ["message-1"])
        self.assertEqual(preference["action"], "archive")
        self.assertEqual(preference["digest_visibility"], "hidden")

    def test_mailbox_and_output_preferences_are_configurable(self):
        memory.upsert_mailbox(
            self.root,
            {
                "address": " Person@Example.com ",
                "connection": "gmail_primary",
                "timezone": "Europe/Lisbon",
                "account_tag": "work",
                "allowed_labels": [
                    "Updates",
                    "Notifications",
                    "Newsletters/Weekly Digest",
                    "Events/Discovery",
                ],
                "allowed_actions": ["label", "archive"],
                "label_map": {
                    "content": "Newsletters/Weekly Digest",
                    "events": "Events/Discovery",
                },
            },
        )
        memory.set_output_preferences(
            self.root,
            {"timezone": "Europe/Lisbon", "voice": "assistant", "maximum_focus_items": 2},
        )

        persona = self.read_json("persona.json")
        self.assertEqual(persona["mailboxes"][0]["address"], "person@example.com")
        self.assertEqual(persona["output_preferences"]["maximum_focus_items"], 2)
        self.assertEqual(memory.validate_store(self.root), [])

    def test_invalid_preference_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported value"):
            memory.upsert_preference(
                self.root,
                {
                    "id": "bad-action",
                    "scope": {},
                    "action": "delete_everything",
                    "digest_visibility": "cleanup",
                    "source": "explicit_user_feedback",
                    "reason": "Invalid test",
                },
            )

    def test_feedback_and_policy_candidates_are_separate(self):
        memory.append_feedback(
            self.root,
            {
                "id": "feedback-1",
                "kind": "explicit_persistent_preference",
                "user_feedback": "Archive messages from an organization I left.",
                "interpretation": {"scope": "organization"},
            },
        )
        memory.append_policy_candidate(
            self.root,
            {
                "id": "candidate-1",
                "proposed_rule": "Treat a brief human acknowledgement as human correspondence.",
                "rationale": "Authorship is independent from reply need.",
                "regression_case": {"input": "Cool!", "expected": "human_correspondence"},
            },
        )

        self.assertEqual(len((self.root / "feedback.jsonl").read_text().splitlines()), 1)
        candidate = json.loads((self.root / "policy-candidates.jsonl").read_text().strip())
        self.assertEqual(candidate["status"], "pending")
        self.assertEqual(self.read_json("persona.json")["preferences"], [])

    def test_partial_run_advances_only_successful_mailbox(self):
        memory.record_run(
            self.root,
            {
                "id": "run-1",
                "pipeline": "daily",
                "started_at": "2026-08-21T07:00:00Z",
                "completed_at": "2026-08-21T07:05:00Z",
                "mailboxes": {
                    "one@example.com": {
                        "status": "complete",
                        "cutoff": "2026-08-21T07:00:00Z",
                        "dedupe_keys": ["one@example.com|m1|2026-08-21T06:00:00Z"],
                    },
                    "two@example.com": {
                        "status": "incomplete",
                        "failure": "pagination failed",
                    },
                },
            },
        )
        state = self.read_json("state.json")
        self.assertEqual(
            state["pipelines"]["daily"]["mailboxes"]["one@example.com"]["last_successful_cutoff"],
            "2026-08-21T07:00:00Z",
        )
        self.assertIsNone(
            state["pipelines"]["daily"]["mailboxes"]["two@example.com"]["last_successful_cutoff"]
        )

    def test_pipelines_advance_independently(self):
        for pipeline, cutoff in (
            ("daily", "2026-08-21T07:00:00Z"),
            ("weekly_content", "2026-08-17T09:00:00Z"),
        ):
            memory.record_run(
                self.root,
                {
                    "id": f"run-{pipeline}",
                    "pipeline": pipeline,
                    "started_at": cutoff,
                    "completed_at": cutoff,
                    "mailboxes": {
                        "one@example.com": {
                            "status": "complete",
                            "cutoff": cutoff,
                        }
                    },
                },
            )

        state = self.read_json("state.json")
        self.assertEqual(
            state["pipelines"]["daily"]["mailboxes"]["one@example.com"]["last_successful_cutoff"],
            "2026-08-21T07:00:00Z",
        )
        self.assertEqual(
            state["pipelines"]["weekly_content"]["mailboxes"]["one@example.com"]["last_successful_cutoff"],
            "2026-08-17T09:00:00Z",
        )

    def test_concurrent_pipeline_updates_do_not_overwrite_each_other(self):
        context = multiprocessing.get_context("spawn")
        state_read = context.Event()
        daily_run = {
            "id": "run-daily",
            "pipeline": "daily",
            "started_at": "2026-08-21T07:00:00Z",
            "completed_at": "2026-08-21T07:05:00Z",
            "mailboxes": {
                "one@example.com": {
                    "status": "complete",
                    "cutoff": "2026-08-21T07:00:00Z",
                }
            },
        }
        weekly_run = {
            "id": "run-weekly-content",
            "pipeline": "weekly_content",
            "started_at": "2026-08-21T08:00:00Z",
            "completed_at": "2026-08-21T08:05:00Z",
            "mailboxes": {
                "one@example.com": {
                    "status": "complete",
                    "cutoff": "2026-08-21T08:00:00Z",
                }
            },
        }

        delayed_process = context.Process(
            target=record_run_after_delayed_state_read,
            args=(str(self.root), daily_run, state_read),
        )
        delayed_process.start()
        self.assertTrue(state_read.wait(timeout=5), "delayed process did not read state")
        concurrent_process = context.Process(
            target=record_run_in_process,
            args=(str(self.root), weekly_run),
        )
        concurrent_process.start()
        delayed_process.join(timeout=10)
        concurrent_process.join(timeout=10)

        self.assertEqual(delayed_process.exitcode, 0)
        self.assertEqual(concurrent_process.exitcode, 0)
        state = self.read_json("state.json")
        self.assertIn("daily", state["pipelines"])
        self.assertIn("weekly_content", state["pipelines"])

    def test_non_array_dedupe_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "must be an array of strings"):
            memory.record_run(
                self.root,
                {
                    "id": "run-bad-dedupe",
                    "pipeline": "daily",
                    "started_at": "2026-08-21T07:00:00Z",
                    "completed_at": "2026-08-21T07:05:00Z",
                    "mailboxes": {
                        "one@example.com": {
                            "status": "complete",
                            "cutoff": "2026-08-21T07:00:00Z",
                            "dedupe_keys": "one@example.com|m1|2026-08-21T06:00:00Z",
                        }
                    },
                },
            )
        self.assertNotIn("daily", self.read_json("state.json")["pipelines"])

    def test_checkpoint_cannot_move_backward(self):
        first_run = {
            "id": "run-newer",
            "pipeline": "daily",
            "started_at": "2026-08-21T07:00:00Z",
            "completed_at": "2026-08-21T07:05:00Z",
            "mailboxes": {
                "one@example.com": {
                    "status": "complete",
                    "cutoff": "2026-08-21T07:00:00Z",
                }
            },
        }
        memory.record_run(self.root, first_run)
        older_run = {
            "id": "run-older",
            "pipeline": "daily",
            "started_at": "2026-08-20T07:00:00Z",
            "completed_at": "2026-08-20T07:05:00Z",
            "mailboxes": {
                "one@example.com": {
                    "status": "complete",
                    "cutoff": "2026-08-20T07:00:00Z",
                }
            },
        }
        with self.assertRaisesRegex(ValueError, "checkpoint backward"):
            memory.record_run(self.root, older_run)

    def test_sensitive_payload_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "sensitive fields"):
            memory.append_feedback(
                self.root,
                {
                    "id": "feedback-sensitive",
                    "kind": "exact_message_correction",
                    "user_feedback": "Wrong category",
                    "interpretation": {"message_body": "private content"},
                },
            )


if __name__ == "__main__":
    unittest.main()
