---
name: enable-relay
description: Enable Relay in the current repo by creating `.relay/` state, guardrails, queue, and automation guidance.
---

# Enable Relay

Use this skill when the user wants to turn the current repo into a Relay-managed Codex workflow.

## Workflow

1. Run the Relay runtime from this plugin:

```bash
python3 ../../scripts/relay_runtime.py enable --json
```

2. Read the generated `.relay/mission.md`, `.relay/state.md`, `.relay/queue.md`, and `.relay/guardrails.md`.
3. Summarize:
   - what Relay inferred about the repo
   - the current verdict
   - the next tasks Relay queued
4. Suggest either:
   - `inspect-relay-state` for a quick status read
   - `install-relay-automations` when the user wants recurring follow-up

## Guardrails

- Do not overwrite existing Relay files unless the user explicitly asks for a reset.
- If `.relay/` already exists, treat this as a refresh and preserve existing state.
