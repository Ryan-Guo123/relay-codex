---
name: generate-release-checklist
description: Generate `.relay/release-checklist.md` with verification, versioning, GitHub release, and human approval gates for a Relay-managed repo.
---

# Generate Release Checklist

Use this skill when the user wants to prepare a release, tag a version, publish a GitHub release, or hand off release readiness.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py release --json
```

2. Read `.relay/release-checklist.md`.
3. Report:
   - current verdict
   - release posture
   - verification commands
   - human approval gates
   - whether the release should proceed, pause, or be reviewed first

## Guardrails

- Do not create tags, push tags, publish GitHub releases, or post public announcements unless the user explicitly asks for that release action.
- If the verdict is `needs_human` or `needs_review`, treat the checklist as a review artifact, not permission to release.
- Keep patch releases tied to meaningful merged changes.
