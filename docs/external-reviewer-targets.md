# External Reviewer Targets

This document turns the Round 1 validation plan into a small, careful reviewer target list.

The goal is not promotion volume. The goal is one useful outside reviewer outcome:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`

Do not mass-post. Do not ask for stars. Do not ask for sponsorship. Ask for one review decision.

## Current Validation Assets

- Stable reviewer packet: [round1-reviewer-request.md](round1-reviewer-request.md)
- Public ask copy: [round1-outreach-message.md](round1-outreach-message.md)
- Feedback form: [Round 1 Relay feedback](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml)
- Tracking issue: [#39 Run validation round 1 with an outside reviewer](https://github.com/Ryan-Guo123/relay-codex/issues/39)

## Targeting Rule

Only ask someone if at least one of these is true:

- They maintain or review a GitHub project.
- They have publicly discussed AI-generated PR review burden.
- They build or use coding-agent workflow tools.
- They can judge whether the review-readiness artifact is useful in a real PR workflow.

Do not ask:

- random stargazers
- people who have not discussed review or maintainer workflows
- communities where self-promotion is banned
- maintainers currently dealing with high-stress incidents or harassment

## Round 1 Target Queue

| Priority | Target segment | Evidence source | Why it fits | Action | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | GitHub issue #39 public audience | [#39](https://github.com/Ryan-Guo123/relay-codex/issues/39) | Repo-local, low-risk, transparent validation ask. | Public ask already posted; wait for organic response while doing one targeted ask. | Posted |
| 2 | Maintainers discussing AI PR review burden | [Reddit r/github thread](https://www.reddit.com/r/github/comments/1rofktt/is_ai_coding_making_pull_requests_harder_to_review/) | Thread discusses large AI PRs, sensitive changes, cohesion, and reviewer load. | Reply only if tool/resource sharing is welcome; otherwise use as research only. | Research only |
| 3 | Engineers discussing hard PR review process | [Reddit r/ExperiencedDevs thread](https://www.reddit.com/r/ExperiencedDevs/comments/1tbqunh/first_time_in_a_position_reviewing_pull_requests/) | Reviewers mention huge likely-AI PRs and the need for structured review. | Do not pitch unless the thread allows tools; use the pain language to sharpen the ask. | Research only |
| 4 | Communities discussing AI-generated PR overload | [ITK discourse thread](https://discourse.itk.org/t/ai-generated-pull-requests-overwhelming-hard-to-review-carefully/7728) | Maintainers discuss being overwhelmed by large AI-generated PRs. | Do not post unless invited; use as evidence that review burden is real. | Research only |
| 5 | GitHub Community users improving coding-agent PR workflows | [GitHub Community discussion #174930](https://github.com/orgs/community/discussions/174930) | Discussion is about making Copilot/Coding Agent work more reviewable. | Consider a short resource reply if it is relevant and not spammy. | Candidate |
| 6 | Agent workflow builders | GitHub topics: [ai-code-review](https://github.com/topics/ai-code-review), [code-review-automation](https://github.com/topics/code-review-automation) | Builders can judge whether Relay's schema/artifacts are useful for integration. | Ask for artifact/schema critique, not adoption. | Candidate |
| 7 | Maintainers worried about AI PR slop | [GitHub Blog review guide](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/) | GitHub's guidance says agent PRs need scope, evidence, risky-file checks, and edited PR bodies. | Use as framing source in the ask; do not treat it as validation. | Framing |

## First Direct Ask

Use this only for a maintainer or reviewer who is plausibly close to the problem:

```text
Quick ask: would you be open to spending 10 minutes reviewing a generated PR handoff?

I am validating Relay for Codex, an open-source tool that turns Codex work into GitHub-ready maintainer artifacts. I need one outside reviewer to compare the Relay handoff with a normal PR summary and mark it reused, edited_heavily, ignored, or confusing.

Round 1 reviewer request:
https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/round1-reviewer-request.md

Feedback form:
https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml

Blunt negative feedback is welcome.
```

## Posting Rules

- Prefer one direct, relevant ask over broad posting.
- If posting in a public thread, disclose that Relay is your project.
- Use the stable reviewer request, not a vague repo link.
- Ask for `reused`, `edited_heavily`, `ignored`, or `confusing`.
- Do not argue with negative feedback.
- If a moderator or maintainer says the ask is unwelcome, stop and record that as a distribution constraint.

## Evidence To Record

For each ask, update [validation-ledger.md](validation-ledger.md) with:

- date
- channel or target segment
- artifact shared
- whether the ask was public or private
- outcome, if any
- product decision

If the ask is private, record the segment without naming the person.

## Stop Condition For Round 1 Outreach

Stop this round if:

- one outside reviewer files usable feedback
- three targeted asks receive no response after seven days
- one maintainer says the request itself is noisy or unwelcome

Then decide whether to simplify the artifact, change the target segment, or stop the product direction.
