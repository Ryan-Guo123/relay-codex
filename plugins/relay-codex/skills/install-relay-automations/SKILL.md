---
name: install-relay-automations
description: Recommend or install Relay automation packs so Codex can keep watching a project after the current thread goes quiet.
---

# Install Relay Automations

Use this skill when the user wants Relay to keep checking the project automatically.

## Workflow

1. Generate the pack definitions:

```bash
python3 ../../scripts/relay_runtime.py automations --json
```

2. Explain the three packs:
   - `Continue Working`
   - `Daily Triage`
   - `Stuck Recovery`
3. If the user explicitly wants installation, use Codex automations:
   - prefer a thread heartbeat automation for `Continue Working`
   - prefer a daily recurring automation for `Daily Triage`
   - prefer a review-oriented follow-up automation for `Stuck Recovery`
4. After installation, refresh `.relay/automations.md` in your summary if needed.

## Defaults

- `Continue Working`: recommend every 2 hours during active work periods
- `Daily Triage`: recommend every weekday morning
- `Stuck Recovery`: recommend only when the project enters `needs_review`

## Guardrails

- Do not silently install automations unless the user asked for it.
- Automations should inspect `.relay/` first and avoid blind continuation when the verdict is not `continue`.
