# Skill system

This repository is the canonical home for Filipe's portable personal plugins, standalone capabilities, and their maintenance process. Project-specific workflows remain in the repositories they operate.

```text
plugin
└── several related skills serving one mission

standalone capability
└── one independent skill
```

Skills are available for automatic selection unless their `agents/openai.yaml` sets `allow_implicit_invocation: false`. Use that explicit-only policy for intentional workflows that should begin only when Filipe asks for them, while keeping reusable disciplines available to project workflows.

## Update loop

1. Use the skill on real work.
2. Preserve compact evidence of specific friction, missing context, or repeated useful behavior.
3. Check for an existing GitHub issue in the canonical repository. With the user's approval, create or update one labeled `skill-improvement`; never include private source material.
4. Propose the smallest change and get the relevant owner's approval before changing shared or sensitive skills.
5. Edit and validate the canonical source through a reviewed pull request.
6. Merge, reinstall or update, and test discovery in a new Codex task.
7. Close the issue with the merged change and update the catalog when ownership, status, location, or replacement changes.

Skills may suggest improvements and offer to record a candidate, but never create an issue or rewrite themselves without approval. Personal preferences and private feedback stay in user-owned memory; only de-identified, reusable lessons belong in a shared issue.

See `catalog.json` for the machine-readable inventory.
