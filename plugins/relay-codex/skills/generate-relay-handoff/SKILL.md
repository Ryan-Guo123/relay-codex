---
name: generate-relay-handoff
description: Generate `.relay/handoff.md` so a maintainer or future Codex run can review the current verdict, recent signals, queue, and safest next action.
---

# Generate Relay Handoff

Use this skill when the user wants a PR handoff, release handoff, maintainer summary, or future-Codex pickup note for a Relay-managed repository.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py handoff --json
```

2. Read `.relay/handoff.md`.
3. Report:
   - current verdict
   - last successful signal
   - recommended next action
   - whether the handoff is safe to use in a PR or release note

## Guardrails

- If the verdict is `needs_human` or `needs_review`, do not continue implementation work until the handoff has been reviewed.
- Do not post the handoff externally without user approval.
- If the handoff contains sensitive project context, suggest keeping it local or redacting before committing.
