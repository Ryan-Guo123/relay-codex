# Reviewer Pack Example

This is a sample `.relay/reviewer-pack.md` generated from a temporary copy of `tests/fixtures/stuck-repo`.

It exists so outside reviewers can judge the shape of Relay's handoff without installing the plugin first. This is still not proof that Relay is useful; proof requires an outside maintainer to compare it with a normal Codex/manual summary and file feedback.

## Command

```bash
cp -R tests/fixtures/stuck-repo /private/tmp/relay-reviewer-pack-example
python3 plugins/relay-codex/scripts/relay_runtime.py reviewer-pack --root /private/tmp/relay-reviewer-pack-example --json
```

Runtime result:

```json
{
  "project": "relay-reviewer-pack-example",
  "verdict": "needs_review",
  "event_count": 3,
  "stack": ["Node.js"],
  "review_readiness": {
    "changed_file_count": 0,
    "large_change": false,
    "sensitive_paths": []
  }
}
```

## Generated Reviewer Pack

````markdown
# Relay Reviewer Pack

- Project: `relay-reviewer-pack-example`
- Branch: `unknown`
- Verdict: `needs_review`

## Reviewer Ask

I am testing whether Relay's generated PR handoff is useful for maintainers.

Please compare the Relay handoff below with a normal Codex/manual summary for the same PR or task.

Could you tell what changed, what was verified, what still needs review, and what the next action should be?

Could you also tell whether the changed-file scope and sensitive-path scan are enough to decide who should review this PR?

Please be blunt: would you reuse this, edit it heavily, ignore it, or ask for a different format?

## Relay Handoff To Review

```markdown
## Relay PR Handoff

Relay converted the current Codex run state into a GitHub-ready review note. It does not post this comment automatically.

### Current State

- Project: `relay-reviewer-pack-example`
- Branch: `unknown`
- Verdict: `needs_review`
- Review posture: Needs maintainer review before another agent pass.

### What Changed

- No Git changes detected in the current workspace.

### Review Readiness

- Scope: No non-Relay Git changes detected.
- Review signal: Use this artifact as a handoff sample, not as proof that code changed.

### Last Successful Signal

- No substantive Relay event recorded yet.

### Verification

- 2026-04-14T05:00:00+00:00: pytest failed with error on the same login flow assertion
- 2026-04-14T05:05:00+00:00: pytest failed with error on the same login flow assertion
- 2026-04-14T05:10:00+00:00: pytest failed with error on the same login flow assertion

### Risks / Review Focus

- Relay detected repeated test-only churn without enough evidence of forward progress.

### Recent Relay Events

- 2026-04-14T05:00:00+00:00: `bash` - pytest failed with error on the same login flow assertion
- 2026-04-14T05:05:00+00:00: `bash` - pytest failed with error on the same login flow assertion
- 2026-04-14T05:10:00+00:00: `bash` - pytest failed with error on the same login flow assertion

### Recommended Next Action

Inspect the repeated failure or churn signal, then choose one narrow recovery step.

### Maintainer Checklist

- [ ] Confirm the changed files match the PR intent.
- [ ] Check any sensitive paths or large-scope warning before requesting review.
- [ ] Confirm verification evidence is present or run the suggested command.
- [ ] Resolve any `needs_human` or `needs_review` signal before merge.
- [ ] Paste or adapt this note into the PR only after removing sensitive context.
```

## Compare Against

Paste or link the normal Codex/manual summary here before sending this pack to a reviewer.

## Scoring Rubric

| Question | Score | Notes |
| --- | --- | --- |
| Changed files are clear |  |  |
| Verification is reviewable |  |  |
| Review focus points to the right risk |  |  |
| Review readiness signals are useful |  |  |
| Next action is directly actionable |  |  |
| GitHub fit is pasteable |  |  |

## Required Outcome

Choose one:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`
````

## What To Judge

When reviewing this example, ignore whether the fixture itself is useful. Judge the handoff shape:

- Can you identify the current verdict?
- Can you see the verification evidence?
- Does the review focus point to the right risk?
- Is the next action specific enough?
- Would this be easier to reuse than reconstructing the Codex thread manually?

If the answer is no, file `ignored` or `confusing` feedback. That signal is valuable.
