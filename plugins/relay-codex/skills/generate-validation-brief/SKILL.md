---
name: generate-validation-brief
description: Generate `.relay/validation-brief.md`, a shareable outside-review validation packet with the reviewer pack, outcome choices, and ledger update instructions.
---

# Generate Validation Brief

Use this skill when the user wants to collect outside maintainer feedback, validate Relay's product direction, or prepare a public/private reviewer ask.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py validation-brief --json
```

For a clean PR checkout, pass the fetched base ref:

```bash
python3 ../../scripts/relay_runtime.py validation-brief --base-ref origin/main --json
```

2. Read `.relay/validation-brief.md`.
3. Before sharing it:
   - add or link the normal Codex/manual summary in the embedded reviewer pack
   - redact secrets, private links, customer data, or internal owner names
   - keep the outcome choices intact: `reused`, `edited_heavily`, `ignored`, or `confusing`
   - ask for a decision, not praise

## Guardrails

- Do not treat the validation brief as validation by itself; only an outside reviewer outcome counts.
- Do not ask for stars, sponsorship, or money in the validation ask.
- Record the response in GitHub and update `docs/validation-ledger.md`.
