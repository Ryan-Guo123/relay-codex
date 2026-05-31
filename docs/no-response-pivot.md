# No-Response Pivot Checklist

Relay has sent three public targeted asks for Round 1 validation. Until the 7-day window closes, do not send more broad public asks in the same segment.

Snapshot date: 2026-05-31.

## Review Date

Run this checklist on **2026-06-07**.

Tracking issue: [#60 Run June 7 no-response pivot review](https://github.com/Ryan-Guo123/relay-codex/issues/60).

Issue label: `waiting-on-feedback`.

## Public Asks To Check

| Ask | Link | Segment | What To Check |
| --- | --- | --- | --- |
| GitHub Community coding-agent workflow thread | https://github.com/community/community/discussions/174930#discussioncomment-17120655 | Copilot/Codex-style agent PR workflows | Any reply that accepts, rejects, questions, or critiques the handoff artifact. |
| GitHub Community AI PR review tools thread | https://github.com/community/community/discussions/179633#discussioncomment-17120686 | CodeRabbit/Paragon-style PR review tool comparison | Any signal that Relay is useful `before_review`, `in_addition`, or `not_needed`. |
| GitHub Community bot review automation thread | https://github.com/community/community/discussions/186152#discussioncomment-17120741 | Re-requesting bot reviews in automated PR loops | Any signal that review-readiness is useful before the next AI review pass. |

## If Any Ask Receives A Reply

Do this before any new outreach:

1. Classify the reply:
   - `reused`
   - `edited_heavily`
   - `ignored`
   - `confusing`
2. Classify the AI review fit:
   - `before_review`
   - `in_addition`
   - `instead`
   - `not_needed`
   - `unsure`
3. Ask for permission to quote or summarize the reply publicly if the signal is not already clear enough.
4. Update [validation-ledger.md](validation-ledger.md).
5. Update [outreach-log.md](outreach-log.md).
6. Comment on [#39](https://github.com/Ryan-Guo123/relay-codex/issues/39) with the outcome and next product decision.

Do not argue with negative feedback. A `not_needed`, `ignored`, or `confusing` reply is useful evidence.

## If All Three Asks Receive No Reply

Do not send a fourth public ask in the same GitHub Community segment.

Instead:

1. Mark all three outreach rows as `No response` in [outreach-log.md](outreach-log.md).
2. Add a no-response row to [validation-ledger.md](validation-ledger.md).
3. Comment on [#39](https://github.com/Ryan-Guo123/relay-codex/issues/39) that Round 1 public-thread outreach produced no response.
4. Pause broad public-thread outreach.
5. Pick one pivot path below.

## Pivot Paths

### Pivot A: Artifact Simplification

Use if no one replies because the ask is too much work.

Tracking issue: [#62 Prepare 60-second reviewer sample if Round 1 gets no replies](https://github.com/Ryan-Guo123/relay-codex/issues/62), closed after [reviewer-quick-verdict.md](reviewer-quick-verdict.md) shipped.

Current status: ready as a lower-friction artifact, but not yet validated.

Use the 60-second sample instead of the full reviewer pack:

- [reviewer-quick-verdict.md](reviewer-quick-verdict.md)
- review path: `60-second quick verdict`
- required outcome: `reused`, `edited_heavily`, `ignored`, or `confusing`
- required AI review fit: `before_review`, `in_addition`, `not_needed`, or `unsure`

Then test only that smaller artifact before sending another full reviewer-pack ask.

### Pivot B: Target Segment Change

Use if GitHub Community public threads do not respond.

Switch from public threads to one of:

- maintainers with recent AI-generated PRs in their repo
- people who run AI PR review tools and have public config files
- agent workflow tool builders who can critique the JSON schema
- small teams using Copilot Coding Agent or Codex on GitHub PRs

Keep it to one careful ask. Do not mass-message.

### Pivot C: External Trial First

Use if reviewers need to see real output instead of docs.

Find one outside repository where the owner is willing to run the copy-paste workflow:

- [external-repo-trial.md](external-repo-trial.md)
- [examples/github-actions/relay-external-trial.yml](../examples/github-actions/relay-external-trial.yml)

This is stronger than another discussion comment because it creates a real artifact on a real PR.

### Pivot D: Shrink The Product

Use if replies or silence suggest the plugin is too heavy for the wedge.

Shrink Relay to:

- a GitHub Actions workflow
- a JSON schema
- a Codex skill pack
- a research/demo repository

Do not build a dashboard or hosted product before any external repo trial exists.

## Decision Rule

After the 2026-06-07 review:

| Evidence | Decision |
| --- | --- |
| Positive reply | Improve the artifact section the reviewer found useful. |
| Negative reply | Simplify, rename, or stop the contested surface. |
| No replies | Change target segment or artifact before another ask. |
| External trial accepted | Prioritize trial support over new docs. |
| Money/sponsor question | Record the signal, but do not sell before usage evidence. |

Expected revenue remains **$0** until an outside reviewer marks the artifact `reused` or `edited_heavily`, or an outside maintainer asks for setup/support after seeing a real Relay artifact.
