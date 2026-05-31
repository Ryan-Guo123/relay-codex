# PR Handoff Example

This example validates Workflow A from [validation-plan.md](validation-plan.md):

```text
issue/task -> Codex Goal/run -> relay handoff -> PR body/review checklist
```

The goal is not to prove that Relay is a complete product. The goal is narrower:

> Is a generated GitHub PR handoff more reusable than reconstructing the Codex thread manually?

## Fixture

The example uses a temporary copy of `tests/fixtures/stuck-repo`, which contains three repeated failing test events:

```json
{"timestamp":"2026-04-14T05:00:00+00:00","kind":"bash","summary":"pytest failed with error on the same login flow assertion"}
{"timestamp":"2026-04-14T05:05:00+00:00","kind":"bash","summary":"pytest failed with error on the same login flow assertion"}
{"timestamp":"2026-04-14T05:10:00+00:00","kind":"bash","summary":"pytest failed with error on the same login flow assertion"}
```

Run:

```bash
cp -R tests/fixtures/stuck-repo /tmp/relay-stuck-repo
python3 plugins/relay-codex/scripts/relay_runtime.py pr-comment --root /tmp/relay-stuck-repo --json
```

Relay writes:

```text
.relay/pr-comment.md
```

## Generated PR Comment

```markdown
## Relay PR Handoff

Relay converted the current Codex run state into a GitHub-ready review note. It does not post this comment automatically.

### Current State

- Project: `stuck-repo`
- Branch: `unknown`
- Verdict: `needs_review`
- Review posture: Needs maintainer review before another agent pass.

### What Changed

- No Git changes detected in the current workspace.

### Last Successful Signal

- No substantive Relay event recorded yet.

### Verification

- 2026-04-14T05:00:00+00:00: pytest failed with error on the same login flow assertion
- 2026-04-14T05:05:00+00:00: pytest failed with error on the same login flow assertion
- 2026-04-14T05:10:00+00:00: pytest failed with error on the same login flow assertion

### Risks / Review Focus

- Relay saw repeated failure signals in recent events.

### Recommended Next Action

Inspect the repeated failure or churn signal, then choose one narrow recovery step.
```

## Comparison

A normal Codex thread summary can explain the story, but it is not automatically shaped for GitHub review. The Relay PR comment is more useful when it:

- gives the reviewer a visible verdict
- separates changed files from generated Relay artifacts
- preserves verification evidence instead of confidence language
- names the risk or review focus
- states one next action
- reminds the maintainer that posting to GitHub still needs review/redaction

## Result

This passes the first version of issue #16's validation bar:

- a documented PR handoff example exists
- it uses real Relay runtime output from a fixture-backed run
- it links to the validation plan
- it makes the comparison against manual thread reconstruction explicit

This does not prove broad demand. It only proves that Relay now has a concrete GitHub-facing artifact to test on real PRs.
