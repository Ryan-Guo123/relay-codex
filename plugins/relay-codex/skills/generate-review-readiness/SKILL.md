---
name: generate-review-readiness
description: Generate `.relay/review-readiness.md`, a standalone review gate with changed-file scope, sensitive paths, and CODEOWNERS routing hints.
---

# Generate Review Readiness

Use this skill when the user wants to know whether a Codex-generated branch is ready to request review, who should review it, or whether the change should be split before deeper maintainer attention.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py review-readiness --json
```

2. Read `.relay/review-readiness.md`.
3. Report:
   - changed-file count
   - sensitive paths
   - CODEOWNERS routing hints
   - unowned changed paths
   - recommended review decision

## Guardrails

- Treat this as a routing gate, not merge approval.
- If the artifact flags a large review surface, recommend splitting or tightening the PR summary before requesting review.
- Redact sensitive paths, internal owner names, customer data, or private links before sharing publicly.
