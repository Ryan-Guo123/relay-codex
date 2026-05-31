# Outreach Log

Relay needs outside evidence, not more internal activity. This log tracks the outreach funnel that can produce that evidence.

Snapshot date: 2026-05-31.

## Funnel Metrics

| Metric | Current | Counts When |
| --- | ---: | --- |
| Targeted asks sent | 3 | A specific outside maintainer/reviewer receives a relevant ask. |
| Replies received | 0 | The target responds with any useful signal. |
| Reviewers accepted | 0 | The target agrees to review a Relay artifact or run the trial workflow. |
| External trial workflows run | 0 | A repository outside `Ryan-Guo123/relay-codex` runs the trial workflow on a real PR/task. |
| Feedback issues filed | 0 | An outside reviewer files or authorizes public feedback. |
| Positive outcomes | 0 | Feedback is `reused` or `edited_heavily`. |
| Negative outcomes | 0 | Feedback is `ignored`, `confusing`, or `not_needed` versus AI PR review tools. |
| Money signals | 0 | A maintainer asks for paid setup, sponsor link, or private workflow support after using Relay. |

Do not count stars, internal PRs, release activity, or owner comments as funnel movement.

## Outreach Queue

| Date | Target Segment | Public / Private | Artifact | Ask | Status | Reply | Outcome | AI Review Fit | Money Signal | Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | Maintainer reviewing AI-generated PRs | Private or public | [external-repo-trial.md](external-repo-trial.md) | Run one PR trial or review the generated bundle. | Not sent | Pending | Pending | Pending | No | Pick one specific maintainer; do not mass-post. |
| 2026-05-31 | GitHub Community coding-agent workflow thread | Public | [round1-reviewer-request.md](round1-reviewer-request.md), [external-repo-trial.md](external-repo-trial.md) | Ask whether the handoff adds value before/alongside AI review tools. | Sent | Pending | Pending | Pending | No | Wait 7 days, then mark `No response` or follow up once if a reviewer accepts. |
| 2026-05-31 | GitHub Community AI PR review tools thread | Public | [round1-reviewer-request.md](round1-reviewer-request.md), [external-repo-trial.md](external-repo-trial.md) | Ask whether CodeRabbit/Paragon-style AI review tools already make Relay's pre-review handoff unnecessary. | Sent | Pending | Pending | Pending | No | Wait 7 days, then mark `No response`; if anyone replies, record `not_needed` as useful negative evidence. |
| 2026-05-31 | GitHub Community bot review automation thread | Public | [round1-reviewer-request.md](round1-reviewer-request.md), [external-repo-trial.md](external-repo-trial.md) | Ask whether teams re-requesting bot reviews want review-readiness before the next AI review pass. | Sent | Pending | Pending | Pending | No | Wait 7 days; if all 3 asks receive no replies, stop this segment and revise the artifact or target audience. |
| TBD | Agent workflow builder | Private or public | [review-readiness.schema.json](review-readiness.schema.json) | Ask whether the schema is useful or already covered by their stack. | Not sent | Pending | Pending | Pending | No | Ask for schema critique, not adoption. |

## Status Values

Use these exact status values:

- `Not sent`
- `Sent`
- `Replied`
- `Accepted review`
- `Trial running`
- `Feedback filed`
- `No response`
- `Declined`
- `Unwelcome`

## Outcome Values

Use the public outcome labels:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`

Use `Pending` until the reviewer files or authorizes feedback.

## AI Review Fit Values

Use the feedback form values:

- `in_addition`
- `before_review`
- `instead`
- `not_needed`
- `unsure`

If the reviewer chooses `not_needed`, treat it as negative evidence even if they were polite.

## Ask Quality Rules

Every ask must:

- target someone plausibly close to PR review, AI-generated PRs, or agent workflow tooling
- include one concrete artifact or trial path
- ask for a decision, not praise
- disclose that Relay is the project being validated
- make negative feedback welcome
- avoid asking for stars, sponsors, or broad product advice

Do not send:

- mass comments
- generic repo links without a concrete artifact
- asks in communities where self-promotion is banned
- follow-ups that argue with negative feedback

## Follow-Up Timing

| Event | Follow-Up |
| --- | --- |
| No reply after 7 days | Mark `No response`; do not nudge more than once. |
| Reviewer accepts but does not file feedback after 7 days | Send one short reminder with the feedback form. |
| Reviewer says the ask is unwelcome | Mark `Unwelcome`; stop contacting that channel. |
| Reviewer files feedback | Update [validation-ledger.md](validation-ledger.md), remove `needs-ledger-update`, and update revenue gates if relevant. |

## Conversion Gates

Do not move to broader promotion until:

- targeted asks sent: at least 3
- feedback issues filed: at least 1
- external trial workflows run: at least 1

Do not test a paid setup ask until:

- positive outcomes: at least 1
- or a maintainer explicitly asks for setup/support after seeing a Relay artifact

If 3 targeted asks produce no reply, run [no-response-pivot.md](no-response-pivot.md), pause this target segment, and change the target segment or artifact instead of sending more asks.
