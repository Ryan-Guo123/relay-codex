---
name: generate-pr-comment
description: Generate `.relay/pr-comment.md`, a GitHub-ready PR handoff comment with Relay state, handoff evidence, and review-readiness signals.
---

# Generate PR Comment

Use this skill when the user wants a PR-ready update, review handoff, maintainer note, or GitHub comment draft for a Relay-managed repository.

## Workflow

1. Run:

```bash
python3 ../../scripts/relay_runtime.py pr-comment --json
```

2. Read `.relay/pr-comment.md`.
3. Report:
   - current verdict
   - review posture
   - review-readiness signals, including sensitive paths, large-scope warnings, or CODEOWNERS routing hints
   - verification evidence or missing verification
   - risks / review focus
   - recommended next action

## Guardrails

- Do not post the comment to GitHub without explicit human approval.
- If the verdict is `needs_human` or `needs_review`, frame the comment as a review handoff, not approval to merge.
- Redact secrets, customer data, private context, or internal-only links before sharing the generated comment publicly.
