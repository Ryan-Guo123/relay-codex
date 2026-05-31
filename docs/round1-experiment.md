# Round 1 Validation Experiment

Relay is not validated by repository polish, internal PRs, or the existence of adjacent high-star agent projects. Round 1 exists to test one narrow claim:

> A maintainer who did not run the Codex thread can use a Relay artifact to decide what changed, what was verified, what still needs review, and whether the PR should be reviewed, split, or sent back.

## Stage

Double Diamond status:

| Stage | Status | Evidence |
| --- | --- | --- |
| Discover | Active | External research shows agent PR review burden is real, and adjacent agent workflow projects have strong attention. |
| Define | Active | Relay has narrowed away from Codex continuation, memory, boards, and managed-agent runtime. |
| Develop | Limited | Build only improvements that make the maintainer handoff easier to judge. |
| Deliver | Not ready | Do not launch broadly until at least one outside reviewer outcome exists. |

## Current Baseline

Snapshot date: 2026-05-31.

| Metric | Current | Meaning |
| --- | ---: | --- |
| Relay stars | 1 | No traction signal yet. |
| Relay forks | 0 | No adoption signal yet. |
| Open validation issues | 3 | Validation process exists, but outcomes are still pending. |
| Outside reviewer outcomes | 0 | Core product usefulness is unproven. |
| External repo trials | 0 | No proof that Relay works outside this repository. |
| Money signals | 0 | No evidence for sponsorship, setup support, or revenue. |

## Market Context

The broader market has attention, but that does not validate Relay. The adjacent traction snapshot lives in [evidence-and-business-case.md](evidence-and-business-case.md) so this experiment does not need a stale duplicate star table.

Use that market context only to avoid obvious duplication:

- skills libraries show reusable workflows can spread, but Relay should not become a broad skills pack
- Paperclip, vibe-kanban, Warp, and Symphony-style projects own agent control, boards, workspaces, and orchestration
- agentmemory, Kage, Recall, and codemem-style tools own memory and continuity
- Copilot code review, CodeRabbit, Graphite, Qodo, PR-Agent, and Greptile own inline AI PR review

Round 1 is not testing whether these adjacent categories are popular. It is testing whether a reviewer still wants a small pre-review handoff after a Codex run.

## Non-Duplicated Wedge

Codex Goals already owns the continuation loop:

- durable objective
- verifiable stopping condition
- validation loop
- evidence-based continue-or-complete decision inside the thread

Claude Managed Agents and Symphony-style systems own managed execution:

- long-running sessions
- cloud or isolated environments
- event streams
- tools and files
- autonomous implementation runs

Relay's only testable wedge is downstream:

```text
Codex Goal/run -> repo evidence -> maintainer-readable GitHub handoff
```

If reviewers say a normal Codex summary is just as good, Relay should shrink or stop.

## Target Reviewer

Ask only reviewers who can judge the review moment:

- maintainers who review GitHub PRs
- engineers who review AI-generated PRs
- contributors who have had to reconstruct agent work from a long thread
- agent workflow builders who can judge whether the artifact/schema is reusable

Do not ask random developers for stars. Do not ask communities where the request would be spam.

## Experiment Procedure

For each target:

1. If attention is cold, start with [reviewer-quick-verdict.md](reviewer-quick-verdict.md).
2. If the reviewer has more time, share the stable reviewer request: [round1-reviewer-request.md](round1-reviewer-request.md).
3. Share one concrete artifact: `.relay/validation-brief.md`, `.relay/review-readiness.md`, `.relay/pr-comment.md`, a `relay-validation-bundle`, or the quick verdict excerpt.
4. If the reviewer wants to test a real repository, share the [external repo trial workflow](external-repo-trial.md).
5. Share a normal Codex/manual summary for comparison.
6. Ask whether they would use Relay in addition to, before, or instead of Copilot/CodeRabbit/Graphite/Qodo-style AI review.
7. Ask the reviewer to choose exactly one outcome: `reused`, `edited_heavily`, `ignored`, or `confusing`.
8. Ask for one product decision: keep, simplify, rename, remove, or retest.
9. Capture the response through the [Round 1 feedback form](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml) or the general handoff feedback form.
10. Record the review path: `60-second quick verdict`, `Round 1 reviewer request`, `Reviewer pack example`, `External repo trial`, `Real PR handoff`, or `Other`.
11. Apply exactly one `outcome:*` label and keep `needs-ledger-update` until [validation-ledger.md](validation-ledger.md) is updated.

## Success Metrics

Round 1 is a success only if:

- at least 1 outside reviewer files or authorizes a public feedback issue
- the issue compares Relay against a normal summary
- the issue records the review path
- the issue has exactly one `outcome:*` label
- the reviewer can identify changed files, verification, review focus, and next action without reading the full Codex thread

Round 1 is a strong success if:

- 2 of 3 outside reviewers mark `reused` or `edited_heavily`
- 1 reviewer says which section they would paste into GitHub
- 1 reviewer names something to remove or shorten

## Failure Metrics

Round 1 is negative evidence if:

- the first outside reviewer marks `ignored` or `confusing`
- 3 targeted asks receive no response after 7 days
- a maintainer says the ask itself is noisy or unwelcome
- reviewers prefer a normal Codex summary
- reviewers say an existing AI PR review tool already solves the job
- reviewers ask for a board, memory engine, or autonomous runtime instead of a handoff artifact

If negative evidence appears, do not add features. Simplify the artifact, change the target segment, or stop the product direction. If all three targeted asks receive no response, run the [no-response pivot checklist](no-response-pivot.md) before sending another ask.

## What Not To Count

Do not count:

- README edits
- internal PRs
- internal issue comments
- GitHub stars without a known path from the reviewer artifact
- AI-generated compliments
- demo views without feedback
- private praise that cannot be recorded as one of the four outcomes

## Next Decision

After the first outside outcome:

| Outcome | Product Decision |
| --- | --- |
| `reused` | Keep the handoff path; test on a larger PR or an external repo. |
| `edited_heavily` | Simplify the artifact; keep only the sections the reviewer touched. |
| `ignored` | Stop feature work; learn whether the target, artifact, or problem is wrong. |
| `confusing` | Fix naming and first-screen explanation before more outreach. |

## Sources

- GitHub Blog, agent pull request review guidance: https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- OpenAI Codex Goals: https://developers.openai.com/codex/use-cases/follow-goals
- OpenAI Cookbook, Using Goals in Codex: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- Claude Managed Agents overview: https://platform.claude.com/docs/en/managed-agents/overview
- Anthropic Engineering, Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Reddit, AI coding and PR review burden: https://www.reddit.com/r/github/comments/1rofktt/is_ai_coding_making_pull_requests_harder_to_review/
- Reddit, whether AI-generated code changes review: https://www.reddit.com/r/ExperiencedDevs/comments/1t1zfsz/does_ai_generated_code_change_the_review_process/
