---
name: inspect-relay-state
description: Inspect `.relay/` and report the current Relay verdict, signals, and next-step posture.
---

# Inspect Relay State

Use this skill when the user wants a quick status read on a Relay-managed project.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py inspect --json
```

2. Read `.relay/state.md` and `.relay/queue.md` for human-friendly context.
3. Report:
   - current verdict
   - reasons behind it
   - the top queued next action
   - whether automations would help

## Guardrails

- Do not edit the queue unless the user asked for recovery or reprioritization.
