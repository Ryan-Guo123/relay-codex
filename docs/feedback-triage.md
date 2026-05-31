# Feedback Triage

Relay feedback is only useful when it turns into a recorded outcome.

Use this protocol for every outside reviewer issue opened through `Round 1 Relay feedback` or `Relay handoff feedback`.

## Outcome Labels

Apply exactly one outcome label to every external feedback issue:

| Label | Meaning | Product Signal |
| --- | --- | --- |
| `outcome:reused` | The reviewer would reuse most of the Relay artifact. | Positive evidence. Keep the artifact and look for repeat use. |
| `outcome:edited_heavily` | The structure helped, but the content needed major edits. | Mixed evidence. Simplify the artifact before expanding. |
| `outcome:ignored` | The reviewer would not use the artifact. | Negative evidence. Do not add adjacent features until the reason is understood. |
| `outcome:confusing` | The reviewer could not tell what to do with the artifact. | Negative evidence. Fix positioning and format before more outreach. |

Supporting labels:

| Label | Use |
| --- | --- |
| `round-1` | Feedback belongs to the first outside-review validation round. |
| `needs-ledger-update` | The issue has not yet been copied into [validation-ledger.md](validation-ledger.md). |

Every feedback issue should also record AI PR review fit:

| Value | Meaning |
| --- | --- |
| `in_addition` | Relay gives context or provenance the AI review tool does not. |
| `before_review` | Relay helps decide whether a PR is ready before any reviewer or review bot spends time. |
| `instead` | Relay is enough for this small handoff without another AI review layer. |
| `not_needed` | Existing AI PR review tools already solve this job. |
| `unsure` | The reviewer needs to test both on a real PR. |

## Triage Steps

1. Confirm the reviewer is outside the current Relay build thread.
2. Confirm the issue links or pastes the artifact being judged.
3. Confirm the issue compares Relay against a normal Codex, manual, or GitHub PR summary.
4. Confirm the issue records AI PR review fit.
5. Apply exactly one `outcome:*` label.
6. Keep `needs-ledger-update` until the issue is added to [validation-ledger.md](validation-ledger.md).
7. Update the ledger with the reviewer relationship, artifact, outcome, AI review fit, and product decision.
8. Remove `needs-ledger-update` after the ledger row is committed.
9. Close the feedback issue only after the ledger update is merged.

## Evidence Rules

Count as external validation:

- feedback from an outside maintainer, outside contributor, frequent PR reviewer, or teammate who did not run the Codex thread
- a linked external repository trial
- a public PR, issue, workflow artifact, or release handoff where Relay output was actually reviewed

Do not count as external validation:

- comments by the Relay maintainer
- internal Relay PRs without an outside reviewer
- stars without a known usage path
- praise that does not include `reused`, `edited_heavily`, `ignored`, or `confusing`

## Round 1 Close Rule

Keep [#39](https://github.com/Ryan-Guo123/relay-codex/issues/39) open until at least one outside reviewer issue has:

- one `outcome:*` label
- a linked artifact
- a comparison against a normal summary
- a row in [validation-ledger.md](validation-ledger.md)

If the first outside outcome is `ignored` or `confusing`, close Round 1 as negative evidence and shrink the next product step instead of broadening the feature set.
