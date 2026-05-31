---
name: generate-reviewer-pack
description: Generate `.relay/reviewer-pack.md`, a reviewer-facing packet for outside maintainer validation of Relay PR handoffs.
---

# Generate Reviewer Pack

Use this skill when the user wants to ask an outside maintainer, teammate, contributor, or evaluator to review a Relay-generated PR handoff.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py reviewer-pack --json
```

2. Read `.relay/reviewer-pack.md`.
3. Before sharing it:
   - add or link the normal Codex/manual summary in the `Compare Against` section
   - redact secrets, private links, customer data, or internal context
   - keep the reviewer outcome options intact

## Guardrails

- Do not treat the reviewer pack as validation by itself; it is only a request packet.
- Do not send the packet externally without human approval.
- Record the response in GitHub using the `Relay handoff feedback` issue template.
