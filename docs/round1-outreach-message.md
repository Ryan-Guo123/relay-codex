# Round 1 Outreach Message

This is the outbound ask for Relay validation Round 1.

It should be used with [round1-reviewer-request.md](round1-reviewer-request.md). The goal is to collect one outside reviewer outcome, not stars, praise, or broad product advice.

## Public Ask

```text
I am looking for one maintainer or frequent PR reviewer who has reviewed AI-generated code.

Relay for Codex is a small open-source tool that turns Codex work into GitHub-ready maintainer handoffs. I am trying to validate whether the handoff is actually useful outside my own workflow.

The test should take about 10 minutes:

1. Open the Round 1 reviewer request:
   https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/round1-reviewer-request.md
2. Compare the Relay-generated handoff with the normal PR summary for the same real PR.
3. Record one outcome: reused, edited_heavily, ignored, or confusing.

Negative feedback is useful. If the Relay handoff is too long, too generic, missing proof, or not better than the normal summary, that is exactly what I need to know before building more.
```

## Short DM

```text
Quick ask: would you be open to spending 10 minutes reviewing a generated PR handoff?

I am validating Relay for Codex, an open-source tool that turns Codex work into GitHub-ready maintainer artifacts. I need one outside reviewer to compare the Relay handoff with a normal PR summary and mark it reused, edited_heavily, ignored, or confusing.

Round 1 reviewer request:
https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/round1-reviewer-request.md

Blunt negative feedback is welcome.
```

## Where To Post

Use this order:

1. GitHub issue #39 as the public repo-local ask.
2. A maintainer or reviewer who already reviews AI-generated PRs.
3. A community thread where AI PR review burden is already being discussed and self-promotion is allowed.
4. A builder of agent workflow tools who can judge whether the artifact or schema is useful.

Do not mass-post. One thoughtful ask is better than broad promotion.

## Evidence To Record

After sending the ask, record:

- URL of the public comment, discussion, issue, or PR.
- If private, the date and target segment without naming private people.
- Artifact shared: `round1-reviewer-request.md`.
- Outcome, once received: `reused`, `edited_heavily`, `ignored`, or `confusing`.
- Product decision: keep, simplify, rename, remove, or test again.

## Guardrails

- Do not ask for stars.
- Do not ask for sponsorship.
- Do not claim Relay saves time before a reviewer says it does.
- Do not count internal Relay PRs as external validation.
- Do not argue with negative feedback; convert it into a product decision.
