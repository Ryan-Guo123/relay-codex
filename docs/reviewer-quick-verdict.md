# Reviewer Quick Verdict

Use this page when you have 60 seconds and do not want to install Relay.

The goal is one blunt first impression:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`

This quick verdict is not enough to prove Relay works. It is only a low-friction screen before asking for a full feedback issue or external repo trial.

## Scenario

PR #42 fixed a validation-bundle bug in Relay itself:

- the generated validation brief told reviewers to inspect `.relay/review-readiness.md`
- the uploaded `relay-validation-bundle` did not include that file
- reviewers would have needed to download a second artifact

## Normal PR Summary

```markdown
## Summary
- include .relay/review-readiness.md directly in relay-validation-bundle
- update the workflow summary and docs so the bundle matches the validation brief artifact list

## Validation
- git diff --check
- python3 -m unittest discover -s tests -p test_*.py

## Release
No release: workflow/docs artifact fix only.
```

## Relay Handoff Excerpt

```markdown
### Current State

- Project: `relay-codex`
- Branch: `HEAD`
- Verdict: `continue`
- Review posture: Ready for maintainer review or one focused follow-up task.

### What Changed

- `.github/workflows/review-readiness.yml`
- `docs/external-maintainer-validation.md`
- `docs/install.md`

### Review Readiness

- Scope: 3 non-Relay changed file(s) against `origin/main`, focused review surface.
- Sensitive paths detected:
  - `.github/workflows/review-readiness.yml` (CI / automation)
- Review signal: Ask a maintainer familiar with the sensitive area to inspect before merge.
- Review routing: No CODEOWNERS file detected.

### Verification

- No verification command or event captured yet.

### Recommended Next Action

Review the changed files and pick one remaining queue item if more work is needed.
```

## 60-Second Questions

Answer without reading the full PR or Codex thread.

| Question | Yes / No |
| --- | --- |
| Can you tell which files changed? |  |
| Can you tell which file needs special review? |  |
| Can you tell what verification evidence is missing? |  |
| Would this help before or beside an AI PR review bot? |  |
| Would you paste or edit any part of it into GitHub? |  |

## Required Quick Outcome

Choose one:

- `reused`: I would reuse most of this structure.
- `edited_heavily`: The shape helps, but the content needs major edits.
- `ignored`: The normal PR summary is enough.
- `confusing`: I cannot tell what to do with this.

Then choose one AI review fit:

- `before_review`
- `in_addition`
- `not_needed`
- `unsure`

If the quick outcome is `ignored`, `confusing`, or `not_needed`, that is useful negative evidence. Open the [Round 1 feedback form](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml) if you are willing to leave a public record.

## What This Tests

This page tests only one question:

> Is Relay's handoff easier to evaluate than reconstructing the agent run from a normal PR summary?

It does not test installation, runtime behavior, external repo fit, or willingness to pay. Those still require [external-repo-trial.md](external-repo-trial.md) and a recorded reviewer outcome.
