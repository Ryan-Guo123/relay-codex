# Community Research: Coding-Agent Continuity Pain

This document captures user pain from Reddit/community threads. It is separate from the market map because the goal is not only to list products, but to understand what users are actually complaining about.

## Summary

The pain is real, but Relay's original shape is too duplicated.

This is directional research, not a market-size estimate. Reddit posts can be deleted, edited, or biased toward builders promoting their own tools, so each conclusion below is treated as a pattern only when it appears across multiple threads, product pages, or repository claims.

Users repeatedly describe:

- fresh sessions starting blind
- context rot during long sessions
- agents re-trying rejected approaches
- stale handoff files
- project rules being too manual
- multiple agents racing over the same files
- agents claiming tests passed when external evidence says otherwise
- review burden moving to humans even when agents write the code

But many people are already building continuity, handoff, memory, and coordination tools. That means Relay should not try to own "handoff" in general.

The remaining possible wedge:

> Convert a Codex Goal/run into a GitHub-ready PR or release artifact.

That is narrower than repo memory, continuity runtime, task orchestration, or agent handoff protocol.

## Repeated Pain Points

### 0. Agent PRs increase review burden

Repeated pattern:

- agents make it easier to create more PRs than maintainers can review
- large generated diffs bury sensitive changes such as auth, billing, schema, and deployment config
- plausible-looking code passes superficial checks but still needs human judgment
- maintainers want evidence, scope control, and risk signals before investing review time

Community language:

> "AI coding tools are making it way easier to generate huge amounts of code quickly."

> "When a PR is big, reviewers naturally start skimming, and it gets easier for sensitive changes to slip through unnoticed."

> "The bigger issue is cohesion, not just size."

GitHub's own agent-PR review guidance makes the same point: agent pull requests are already saturating review bandwidth, reviewers need context before reading the diff, and agent-authored PR bodies should be edited before review is requested.

Research also points in the same direction. A 2026 MSR paper studying 33k agent-authored PRs found that unmerged agent PRs tend to be larger, touch more files, fail CI more often, and suffer from reviewer-engagement and misalignment issues.

Implication for Relay:

This is the strongest current wedge. Relay should not try to make more agent work happen. It should make agent work cheaper to review by producing a compact, evidence-backed PR handoff with changed files, verification, risk focus, and the next human decision.

### 1. New sessions start blind

Repeated pattern:

- users switch from Claude Code to Codex/Cursor or start a new session
- the agent does not know the branch, last prompt, decisions, failed attempts, or next task
- the user re-explains the same context over and over

Community language:

> "Every new AI coding session has the same problem: it starts dumb."

> "Even when you intentionally start fresh, you still have to re-explain everything from scratch."

Implication for Relay:

This pain is already being attacked by memory and continuity tools. Relay should not claim broad session continuity.

### 2. Handoff files are useful but easy to make stale

Repeated pattern:

- users ask the agent to write a handoff before clearing context
- common desired content: current goal, files touched, decisions, failed paths, next steps, uncertainty
- stale handoffs become another maintenance chore

Community language:

> "The zip/tar handoff idea is interesting for onboarding but feels like it would go stale fast on an active project."

> "I wouldn’t want an agent rewriting it after every close because that becomes noise fast."

Implication for Relay:

Relay handoff should be generated on demand for PR/release use, not maintained as a constantly mutating memory file.

### 3. Project rules are not enough

Repeated pattern:

- people ask why not just use project rules / CLAUDE.md / AGENTS.md
- users respond that rules capture only explicit durable conventions
- they miss emergent context: failed refactors, review feedback, weird service limits, ownership, rejected approaches

Community language:

> "Project rules help but they have two problems, you have to write and maintain them manually, and they only capture what you explicitly decide to document."

Implication for Relay:

Relay should not duplicate rule files. It should capture short-lived PR/release evidence that rules files are bad at representing.

### 4. Context rot happens before the user notices

Repeated pattern:

- long sessions drift across unrelated tasks
- old decisions stay technically in context but are no longer attended to
- users manually ask for a handoff and restart

Community language:

> "Context rot is the biggest unsolved problem in long coding sessions."

> "By the time I notice, Claude has often already produced a few bad outputs."

Implication for Relay:

Codex Goals may reduce this inside Codex. Relay should not try to be the context-rot detector unless it can prove a better external signal. GitHub handoff remains safer.

### 5. Multi-agent work creates coordination collisions

Repeated pattern:

- Codex and Claude diagnose the same bug
- multiple agents touch the same files
- two PRs solve one issue
- a later agent has to replay a previous agent's reasoning

Community language:

> "Every handoff replays the world."

> "Both agents diagnose the same bug, both edit the same file, you end up with two PRs for one fix."

Implication for Relay:

Coordination systems such as Colony, AICTX, ai-sync, and Maestro are closer to this pain than Relay. Relay should not build coordination claims, locks, or shared task ownership unless the product pivots fully.

### 6. Users want external proof, not agent self-report

Repeated pattern:

- agents say work is done when tests did not really pass
- users move tests outside the agent
- git checkpoints and external gates become the source of truth

Community language:

> "The agent reports a task as done when the tests didn't actually pass."

> "Repo state and test output stay the source of truth."

Implication for Relay:

This is a valid wedge for PR/release artifacts: Relay should cite commands, changed files, and gates, not summarize confidence.

## Existing Community Projects / Patterns

### Continue Later

Pattern:

- skills plus local CLI
- writes repo-root handoff files
- captures git state, prompts, tasks, gotchas, and run commands

Threat to Relay:

- Directly overlaps with generic handoff files.

Relay response:

- Do not compete on "resume next agent." Focus on GitHub PR/release artifacts.

### Swarm

Pattern:

- repo as shared memory and handoff state
- Orient -> Predict -> Act -> Compare -> Compress -> Hand off
- records Did / Expected / Actual / Next / Handoff

Threat to Relay:

- Overlaps with continuity loop and handoff protocol.

Relay response:

- Keep Relay narrower and less process-heavy.

### ai-sync

Pattern:

- `.ai-sync/` state files
- handoff, resume, diff, transfer
- adapters across tools
- conflict detection and audit trail

Threat to Relay:

- Directly overlaps with cross-agent handoff.

Relay response:

- Avoid cross-agent sync as a feature promise.

### Threadbase / PROJECT_STATE.md Pattern

Pattern:

- project memory in markdown inside the repo
- agent reads before work and updates after meaningful changes
- common desired schema: current goal, decisions, failed attempts, files touched, blocker, next step

Threat to Relay:

- A simple markdown state file may be good enough.

Relay response:

- Prove that generated PR/release handoff is better than a manual state file.

### Memtrace / Code Graph Memory

Pattern:

- always-fresh state after edits
- dependency/caller graph
- avoids stale context by tracking code changes incrementally

Threat to Relay:

- If users want accurate codebase state, Relay's markdown artifacts are too weak.

Relay response:

- Do not compete on code graph memory.

### Colony / AICTX / Coordination Substrates

Pattern:

- local-first coordination
- claims before edits
- compact handoffs/receipts
- active work state, risks, decisions, failures, contract compliance

Threat to Relay:

- These are closer to a full solution for multi-agent continuity.

Relay response:

- Relay should not claim multi-agent coordination.

## What This Means For Relay

### Original Relay

Original idea:

> repo-local state, verdicts, recovery, handoff, automations for long-running Codex work

Status:

Too duplicated.

Reasons:

- Codex Goals handles objective and continuation.
- Maestro handles local-first evidence, verdicts, and handoffs more seriously.
- Kage/Recall/codemem/agentmemory handle repo memory better.
- vibe-kanban/Optio/Symphony handle boards and agent work orchestration.
- Reddit/community projects already handle generic handoff files.

### Smaller Relay

Possible surviving idea:

> Codex App-native GitHub handoff adapter.

Concrete output:

- `pr-comment.md`
- `release-checklist.md`
- release note draft
- review checklist
- minimal evidence bundle tied to commands and changed files

User promise:

> "Do not make me reconstruct a PR/release explanation from a Codex thread."

This is narrower, less magical, and easier to kill if it fails.

## Updated Product Read

The public pain is not "I need another agent loop." That space is now strongly covered by native Goals, managed agents, Symphony-style implementation runs, Paperclip-style control planes, and vibe-kanban-style workspaces.

The public pain that still looks under-served is the maintainer review bottleneck after agent work:

- Was the PR scoped enough to review?
- Did the agent weaken CI, skip tests, or only make superficial progress?
- Which sensitive files changed?
- What should a human inspect before merge?
- Can the reviewer understand the work without reading the full agent thread?

That narrows Relay's positioning further:

> Relay is a review-readiness layer for Codex-generated repository work.

The current product bet should be validated in this order:

1. `reviewer-pack` example so reviewers can inspect the format without installing anything.
2. One real outside-review issue on a real PR/task.
3. Only then consider a runtime feature, such as risk-file detection or PR-size/scope warnings.

## Validation Questions

Relay should answer these before building more:

1. Is a generated PR comment better than asking Codex to summarize the thread?
2. Is the output better than a simple `CURRENT_STATE.md`?
3. Does a maintainer actually paste or reuse the artifact in GitHub?
4. Does it cite enough evidence to reduce review anxiety?
5. Does it avoid becoming another stale markdown file?

## Recommendation

Pause broad product expansion.

Do one narrow experiment:

```text
Codex Goal/run -> Relay handoff -> GitHub-ready PR comment
```

Compare it against:

- normal Codex summary
- manual `CURRENT_STATE.md`
- Maestro-style evidence/handoff
- Continue Later-style handoff file

If Relay is not clearly better for PR/release GitHub surfaces, archive or reposition the repo as a research/demo artifact.

## Sources

- Continue Later Reddit thread: https://www.reddit.com/r/ClaudeCode/comments/1t0m87n/i_made_a_skill_to_stop_losing_ai_coding_context/
- Swarm Reddit thread, title/metadata only if deleted: https://www.reddit.com/r/ClaudeAI/comments/1s3p08b/i_built_a_reponative_handoff_workflow_for_claude/
- ai-sync Reddit thread: https://www.reddit.com/r/ClaudeAI/comments/1rv4xm9/built_a_claude_code_plugin_for_seamless_handoff/
- Context loss between Claude Code / Cursor sessions: https://www.reddit.com/r/cursor/comments/1tg9acb/how_are_you_handling_context_loss_between_claude/
- Context loss between sessions thread: https://www.reddit.com/r/ClaudeAI/comments/1tg9bmz/context_loss_between_sessions_still_the_biggest/
- Memtrace Reddit thread: https://www.reddit.com/r/ClaudeAI/comments/1t3du61/your_claude_code_agent_is_always_working_from/
- Claude Code context limit handoff thread: https://www.reddit.com/r/ClaudeAI/comments/1sw0zs6/how_do_you_handle_the_context_limit_handoff_in/
- Colony Reddit thread: https://www.reddit.com/r/codex/comments/1t4xm2m/i_built_a_localfirst_coordination_layer_for/
- AICTX Reddit thread: https://www.reddit.com/r/buildinpublic/comments/1tbaeds/coding_agents_like_codex_or_claude_dont_just_need/
- Planning / git checkpoint / test gate thread: https://www.reddit.com/r/AI_Agents/comments/1tr652d/how_i_stopped_babysitting_claude_code_and_codex/
- Context-rot feature suggestion: https://www.reddit.com/r/ClaudeAI/comments/1t8batc/feature_suggestion_proactive_contextrot_detection/
- Agent PR review burden thread: https://www.reddit.com/r/github/comments/1rofktt/is_ai_coding_making_pull_requests_harder_to_review/
- Open source AI slop / maintainer burden thread: https://www.reddit.com/r/opensource/comments/1q3f89b/open_source_is_being_ddosed_by_ai_slop_and_github/
- GitHub agent PR review guidance: https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- MSR 2026 agent PR failure study: https://arxiv.org/abs/2601.15195
- CONTINUE.md: https://continue.md/
- Maestro: https://github.com/ReinaMacCredy/maestro
- AICTX: https://aictx.org/
- Kage: https://kage-core.com/
- codemem: https://codemem.sh/
