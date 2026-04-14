---
name: continue-with-relay
description: Inspect Relay state before continuing work so Codex only keeps moving when the repo still has a clear next task.
---

# Continue With Relay

Use this skill when the user wants Codex to keep working in a Relay-managed repo.

## Workflow

1. Inspect Relay first:

```bash
python3 ../../scripts/relay_runtime.py inspect --json
```

2. Open `.relay/mission.md`, `.relay/state.md`, `.relay/queue.md`, and `.relay/guardrails.md`.
3. Apply the verdict:
   - `continue`: pick the next unchecked item in `.relay/queue.md` and execute it
   - `paused`: explain why Relay thinks the repo should pause
   - `needs_human`: stop and ask only for the missing decision
   - `needs_review`: do not continue blindly; route to recovery
4. After meaningful work, inspect Relay again so the final response reflects the latest state.

## Guardrails

- Never keep pushing when Relay says `needs_review`.
- Avoid test-only churn unless the queue explicitly calls for verification.
