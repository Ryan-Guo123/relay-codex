# AI PR Review Competitors

Relay's remaining wedge sits next to a crowded AI PR review market. This document checks whether Relay is duplicating existing review bots.

Snapshot date: 2026-05-31.

## Short Answer

AI PR review is already an active, commercial category. Relay should not position itself as:

- an AI code reviewer
- a bug finder
- an inline suggestion bot
- a merge blocker
- a replacement for Copilot, CodeRabbit, Graphite, Qodo, Greptile, or PR-Agent

Relay's possible role is narrower:

> Before or beside an AI review bot, Relay packages the provenance of a Codex run: changed-file scope, verification evidence, risk focus, and the next human decision.

If outside reviewers say an AI review bot's PR summary already solves that job, Relay should shrink to a template/schema or stop.

## Direct Competitor Map

| Tool | What It Owns | Evidence | Relay Boundary |
| --- | --- | --- | --- |
| GitHub Copilot code review | Native GitHub PR review comments, suggested changes, automatic reviews, repository instructions. | GitHub docs say Copilot can be requested as a PR reviewer and leaves review comments with suggested changes where possible. | Relay should not review code inline or pretend to be a required approval. |
| CodeRabbit | Pull-request reviews, walkthrough comments, inline comments, IDE/CLI reviews, planning, Slack agent workflows. | CodeRabbit docs describe automated context-aware reviews and a PR walkthrough comment posted on every reviewed PR. | Relay should not compete on comprehensive review automation. |
| Graphite AI reviews | Bug-focused AI review, codebase context, actionable suggestions, customization, analytics. | Graphite docs emphasize real bugs, full-codebase context, actionable suggestions, feedback learning, and review analytics. | Relay should not claim bug-finding accuracy or review-quality analytics. |
| Qodo / Qodo Merge | AI review agents for pull requests, summaries, suggestions, labeling, chat, policy/compliance workflows. | Qodo docs describe automatic PR review, summaries, improvements, labeling, and organization policy support. | Relay should not become team compliance or enterprise PR governance. |
| PR-Agent | Open-source PR reviewer with review, description, improvement, labeling, and chat-like PR commands. | The-PR-Agent/pr-agent has 11,414 stars and 1,537 forks on 2026-05-31. | Relay should not copy open-source PR command bots. |
| Greptile | Commercial AI code review with repository context and pricing around PR review volume. | Greptile has a public pricing page and AI code review product positioning. | Relay should not enter paid AI review before proving handoff pull. |

## What These Tools Already Solve

These tools already make strong claims around:

- reading pull request diffs
- finding bugs
- producing inline comments
- suggesting code changes
- summarizing PRs
- labeling or categorizing PRs
- adapting to team rules
- running automatically in GitHub
- charging teams for review automation

That means the existence of paid AI review tools is evidence that the market spends money on review pain, but it is not evidence that Relay will earn money. Relay has to prove it solves a different job.

## Gaps Relay Can Test

Relay can still be useful if reviewers want something AI review bots usually do not emphasize:

| Gap | Relay Test |
| --- | --- |
| Codex-run provenance | Can the reviewer see what the agent was asked to do and what state it left behind? |
| Verification gaps | Does the handoff clearly say what was run, what was not run, and what still needs human review? |
| Review routing before bug-finding | Does `review-readiness` help decide whether the PR is ready, too broad, sensitive, or needs a specific reviewer? |
| Release handoff | Does the artifact help decide whether a tag/release should happen, not just whether code has bugs? |
| Future-agent handoff | Can another Codex thread resume with less context reconstruction? |
| Lightweight local artifact | Does a readable `.relay/` file help when the repo does not want another SaaS reviewer? |

## Round 1 Reviewer Question

Round 1 should include this explicit comparison:

> Would you use Relay in addition to, before, or instead of Copilot/CodeRabbit/Graphite/Qodo-style AI review?

Allowed answers:

- `in_addition`: Relay gives context/provenance the review bot does not.
- `before_review`: Relay helps decide whether a PR is ready for any reviewer.
- `instead`: Relay is enough for this small PR or release handoff.
- `not_needed`: an existing PR review tool already solves the job.

If the common answer is `not_needed`, stop expanding Relay.

## Pricing And Money Signal

Commercial AI review products have public pricing pages, which suggests willingness to pay in the category. Relay cannot use that as its own money signal.

Relay's first valid money signal would be one of:

- a maintainer asks for paid setup/support after using a Relay artifact
- a maintainer asks for a hosted aggregator only after multiple real artifacts exist
- a sponsor/donation happens after a real review or release handoff, not after a generic announcement

Until then, Relay should stay free, small, and evidence-gated.

## Sources

- GitHub Copilot code review docs: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review
- CodeRabbit docs: https://docs.coderabbit.ai/
- CodeRabbit PR walkthroughs: https://docs.coderabbit.ai/pr-reviews/walkthroughs
- Graphite AI reviews: https://graphite.com/docs/ai-reviews
- Qodo Merge docs: https://docs.qodo.ai/v1/qodo-merge
- PR-Agent repository: https://github.com/The-PR-Agent/pr-agent
- Greptile pricing: https://www.greptile.com/pricing
