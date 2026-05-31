# Revenue Experiment

Relay should not promise revenue before usage evidence exists. This document turns "when can this make money?" into falsifiable gates.

Snapshot date: 2026-05-31.

## Current Revenue Verdict

Current expected revenue: **$0**.

Evidence:

- GitHub stars: 1
- Forks: 0
- Targeted asks sent: 2
- Outside reviewer outcomes: 0
- External repo trials: 0
- Repeat usage: 0
- Sponsor/setup/paid-feature requests: 0

There is no defensible forecast for meaningful revenue until at least one outside maintainer uses or rejects the artifact on a real review task.

## Revenue Timeline

| Window | Required Evidence | Revenue Expectation | Decision |
| --- | --- | ---: | --- |
| 0-7 days | 1 outside reviewer outcome on a real Relay artifact | $0 | Do not ask for money. Ask for evidence. |
| 7-14 days | 1 outside repository runs the external trial workflow on a PR | $0 | Only ask whether setup help would be useful. |
| 14-30 days | 3 outside reviewer outcomes, with at least 2 `reused` or `edited_heavily` | $0-$500 | Add GitHub Sponsors and offer paid setup only if someone asks. |
| 30-60 days | 1 outside repo uses Relay on 2+ PRs or releases | $0-$1,000 | Test a setup/support offer. Do not build SaaS. |
| 60-90 days | 2 outside repos show repeat use, or 1 team asks for private workflow support | $500-$2,000 | Consider a paid support package. Still avoid hosted dashboard unless requested. |

These are not promises. They are permission gates. Missing the evidence keeps the revenue expectation at $0.

## First Paid Offer

Only offer this after an outside reviewer marks Relay `reused` or `edited_heavily`.

```text
Relay setup support

I can help wire the external trial workflow into one repo, tune the review-readiness artifact, and create a repeatable handoff flow for Codex-generated PRs.

Price: $100-$250 one-time setup for one repository.
```

Do not offer this in public outreach before evidence exists. If a maintainer asks first, record that as a money signal in [validation-ledger.md](validation-ledger.md).

## Sponsor Trigger

Add or promote GitHub Sponsors only after one of these happens:

- 1 outside maintainer files `reused` or `edited_heavily`
- 1 outside repository runs the trial workflow and links the artifact
- 1 maintainer asks how to support ongoing maintenance

Before that, a sponsor button is cosmetic and should not be counted as traction.

## What Counts As A Money Signal

Count:

- a public or private request for paid setup after seeing a Relay artifact
- a maintainer asking for a support package, sponsor link, or hosted workflow after a real trial
- a paid setup/support invoice
- a GitHub Sponsor or donation tied to a linked review/release handoff

Do not count:

- stars
- generic praise
- internal releases
- the maintainer adding their own sponsor link
- "this could be useful for teams" without a concrete request
- revenue from unrelated work

## Stop Rules

Keep expected revenue at $0 if:

- no outside reviewer outcome appears after 3 targeted asks
- no external repo trial happens within 14 days
- reviewers choose `not_needed` compared with AI PR review tools
- reviewers mark the artifact `ignored` or `confusing`

Pause monetization work if:

- users ask for an agent board, memory engine, or hosted AI review bot instead of Relay's handoff artifact
- support requests would require building a SaaS dashboard before repeat usage exists
- the paid setup ask distracts from getting the first external outcome

## Pricing Hypotheses

| Offer | Price | Build Only If |
| --- | ---: | --- |
| One-repo setup support | $100-$250 one time | 1 outside reviewer marks `reused` or `edited_heavily`. |
| Team workflow setup | $500-$1,000 one time | 1 team uses Relay on 2+ PRs or asks for private workflow support. |
| Hosted artifact dashboard | $10-$20 per repo/month | 2+ teams ask to aggregate artifacts across repos. |
| Security/release handoff templates | $250-$500 setup | A regulated/sensitive repo asks for threat-model or release gates. |

Relay should not build paid infrastructure for any row before its "Build Only If" condition is true.

## Next Action

The next revenue-related action is not selling. It is getting one outside reviewer outcome through [external-repo-trial.md](external-repo-trial.md) or [round1-reviewer-request.md](round1-reviewer-request.md).

Track every ask in [outreach-log.md](outreach-log.md) before treating the revenue gates as moved.
