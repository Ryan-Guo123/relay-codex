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
| Open validation issues | 2 | Validation process exists, but outcomes are still pending. |
| Outside reviewer outcomes | 0 | Core product usefulness is unproven. |
| External repo trials | 0 | No proof that Relay works outside this repository. |
| Money signals | 0 | No evidence for sponsorship, setup support, or revenue. |

## Market Context

The broader market has attention, but that does not validate Relay.

| Project | Current Signal | Why Relay Should Not Copy It |
| --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 112,466 stars, 9,875 forks | Skills libraries win through broad reusable workflows; Relay should stay narrower. |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | 68,394 stars, 12,653 forks | Broad agent control planes are already memorable and crowded. |
| [warpdotdev/warp](https://github.com/warpdotdev/warp) | 60,658 stars, 4,843 forks | Agentic development environments own the interactive workspace. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 47,239 stars, 5,239 forks | Production-grade agent skills are a category, but Relay should not become a skills pack. |
| [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban) | 26,674 stars, 2,805 forks | Agent boards already own planning, branches, terminals, previews, and PR creation. |
| [openai/symphony](https://github.com/openai/symphony) | 24,857 stars, 2,475 forks | Project-to-autonomous-run orchestration is upstream from Relay's handoff layer. |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | 19,992 stars, 1,650 forks | Persistent memory is a different product with stronger dedicated players. |
| [Conway-Research/automaton](https://github.com/Conway-Research/automaton) | 4,569 stars, 979 forks | Extreme autonomy is memorable, but not Relay's safe maintainer workflow. |

Captured with GitHub CLI on 2026-05-31. Stars and forks are attention signals, not proof of willingness to use or pay for Relay.

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

1. Share the stable reviewer request: [round1-reviewer-request.md](round1-reviewer-request.md).
2. Share one concrete artifact: `.relay/validation-brief.md`, `.relay/review-readiness.md`, `.relay/pr-comment.md`, or a `relay-validation-bundle`.
3. If the reviewer wants to test a real repository, share the [external repo trial workflow](external-repo-trial.md).
4. Share a normal Codex/manual summary for comparison.
5. Ask whether they would use Relay in addition to, before, or instead of Copilot/CodeRabbit/Graphite/Qodo-style AI review.
6. Ask the reviewer to choose exactly one outcome: `reused`, `edited_heavily`, `ignored`, or `confusing`.
7. Ask for one product decision: keep, simplify, rename, remove, or retest.
8. Capture the response through the [Round 1 feedback form](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml) or the general handoff feedback form.
9. Apply exactly one `outcome:*` label and keep `needs-ledger-update` until [validation-ledger.md](validation-ledger.md) is updated.

## Success Metrics

Round 1 is a success only if:

- at least 1 outside reviewer files or authorizes a public feedback issue
- the issue compares Relay against a normal summary
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

If negative evidence appears, do not add features. Simplify the artifact, change the target segment, or stop the product direction.

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
