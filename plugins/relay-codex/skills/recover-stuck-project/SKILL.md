---
name: recover-stuck-project
description: Generate a recovery queue and stop Codex from brute-forcing progress when Relay sees churn or repeated failure.
---

# Recover Stuck Project

Use this skill when Relay says the repo needs review or the user says Codex is stuck.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py recover --json
```

2. Read the updated `.relay/queue.md` and `.relay/state.md`.
3. Produce a concise recovery brief:
   - what likely caused the stall
   - the smallest next investigation or implementation step
   - whether a human decision is now required

## Guardrails

- Recovery should shrink the next step, not widen it.
- If the real blocker is product intent, credentials, or external access, say so directly.
