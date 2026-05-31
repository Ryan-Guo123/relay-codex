# External Maintainer Validation

Relay has fixture-backed and real-branch validation. The next question is harder:

> Would someone who did not build Relay actually reuse a generated handoff?

Use this protocol when asking an outside maintainer, reviewer, or open-source collaborator to judge `.relay/pr-comment.md`.

## What To Test

Pick one real maintenance task:

- a small bug fix PR
- a docs or release handoff PR
- a failing test recovery pass
- a dependency or setup improvement

Do not use a synthetic demo as the main evidence. Synthetic demos are useful for onboarding, but they do not prove whether Relay reduces review work.

## How To Prepare

1. Run the normal Relay flow on the branch:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py handoff --json
python3 plugins/relay-codex/scripts/relay_runtime.py pr-comment --json
python3 plugins/relay-codex/scripts/relay_runtime.py reviewer-pack --json
```

2. Read `.relay/pr-comment.md`.
3. Read `.relay/reviewer-pack.md`.
4. Add or link the plain Codex summary or manual PR summary in the `Compare Against` section.
5. Remove secrets, customer data, private links, or internal context.
6. Ask one reviewer to compare both without reading the full Codex thread.

## Reviewer Prompt

Use this short ask:

```text
I am testing whether Relay's generated PR handoff is useful for maintainers.

Please compare this Relay handoff with a normal Codex/manual summary.

Could you tell what changed, what was verified, what still needs review, and what the next action should be?

Please be blunt: would you reuse this, edit it heavily, ignore it, or ask for a different format?
```

The generated `.relay/reviewer-pack.md` includes this prompt, the Relay handoff, the comparison placeholder, the scoring rubric, and the outcome choices.

## Scoring Rubric

Ask the reviewer to score each item from 1 to 5:

| Question | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Changed files | unclear | partly clear | obvious |
| Verification | missing | present but thin | evidence is reviewable |
| Review focus | vague | somewhat useful | points to the right risk |
| Next action | unclear | acceptable | directly actionable |
| GitHub fit | not pasteable | needs edits | easy to reuse |

## Required Outcome

Record one of these outcomes:

- `reused`: the reviewer reused most of the generated handoff.
- `edited_heavily`: the structure helped, but the content needed major edits.
- `ignored`: the generated handoff was not useful.
- `confusing`: the reviewer could not tell what to do with it.

## Decision Rules

Keep `pr-comment` if:

- at least one outside reviewer says it is easier than reconstructing the Codex thread
- the reviewer can identify changed files, verification, review focus, and next action in under two minutes

Simplify `pr-comment` if:

- reviewers reuse only one or two sections
- the output feels too long for GitHub
- the checklist reads as generic noise

Rename or remove `pr-comment` if:

- reviewers prefer a normal Codex summary
- reviewers cannot tell why Relay exists
- the artifact adds another stale markdown file without reducing review work

## Where To Record Feedback

Use the GitHub issue template:

```text
Relay handoff feedback
```

Each feedback issue should link:

- the PR or task being reviewed
- the generated `.relay/pr-comment.md` excerpt or redacted paste
- the comparison summary
- the reviewer outcome
- the product decision

This keeps Relay honest: external validation should decide the next feature, not internal enthusiasm.
