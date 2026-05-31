# Evidence And Business Case

Relay should earn confidence with evidence, not with a neat story.

This document is the blunt version of the product case. It separates:

- evidence that the broader market is real
- evidence that Relay's specific wedge is still unproven
- thresholds that would justify more building
- thresholds that should make the project shrink, pivot, or stop

Snapshot date: 2026-05-31.

## Current Verdict

Relay is not yet proven to be a product that many people will use.

The evidence supports one narrower claim:

> Agent-driven software work is creating real review, handoff, and trust problems. A small GitHub-facing handoff adapter could be useful if real maintainers reuse its artifacts.

That is not the same as saying Relay will get many stars, sponsors, or revenue. Those outcomes require external validation that Relay does not have yet.

Relay should stay in Define / early Develop until outside maintainers prove that the handoff artifact is better than a normal Codex summary or GitHub checklist.

## Market Evidence

### Adjacent GitHub traction

The adjacent market has attention. The following public repository metrics were captured with GitHub CLI on 2026-05-31.

| Repository | Category | Stars | Forks | Issues count | Last pushed | Signal |
| --- | --- | ---: | ---: | ---: | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | agent skills | 112,424 | 9,870 | 48 | 2026-05-28 | Small reusable skills can travel extremely well. |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | agent control plane | 68,387 | 12,650 | 1,770 | 2026-05-30 | Broad "manage agents at work" positioning has major attention. |
| [warpdotdev/warp](https://github.com/warpdotdev/warp) | agentic dev environment | 60,646 | 4,841 | 3,576 | 2026-05-31 | Developers accept agentic workflow inside existing dev surfaces. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | agent skills | 47,232 | 5,239 | 43 | 2026-05-28 | Production-grade agent workflow packaging has obvious demand. |
| [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban) | agent board | 26,674 | 2,805 | 376 | 2026-04-24 | Local boards for coding agents are a real category. |
| [openai/symphony](https://github.com/openai/symphony) | agent work orchestration | 24,855 | 2,475 | 0 | 2026-05-29 | Platform-level task-to-run orchestration is becoming crowded. |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | agent memory | 19,972 | 1,646 | 91 | 2026-05-29 | Persistent memory for coding agents has substantial interest. |
| [Conway-Research/automaton](https://github.com/Conway-Research/automaton) | autonomous agent | 4,570 | 979 | 121 | 2026-05-30 | Memorable autonomy stories can attract attention, but this is not Relay's desired path. |
| [Ryan-Guo123/relay-codex](https://github.com/Ryan-Guo123/relay-codex) | Codex handoff adapter | 1 | 0 | 2 | 2026-05-31 | Relay itself has no external traction yet. |

`Issues count` is the `issues.totalCount` value returned by GitHub CLI; treat it as a rough activity signal, not as a normalized support or quality metric. Stars are attention, not revenue.

Interpretation:

- There is real demand around agent skills, memory, boards, and control planes.
- That demand does not prove Relay's exact shape.
- The strongest crowded categories are already owned by better-known projects.
- Relay should not try to win by being a smaller board, memory engine, or goal runner.

### Review pain evidence

Public review pain is the strongest support for Relay's current wedge.

- GitHub's 2026 guidance says agent pull requests are already common enough to need a different review posture, and it specifically recommends scanning file scope, CI changes, risky workflow changes, and evidence before deep review.
- The same GitHub article says GitHub Copilot code review had processed over 60 million reviews and that more than one in five GitHub code reviews involve an agent.
- A 2026 MSR paper on message-code inconsistency analyzed 23,247 agentic PRs and found that unreliable PR descriptions hurt acceptance rate and merge time.
- Another 2026 MSR paper analyzed 8,031 agentic PRs touching CI/CD configuration and showed that workflow files are a measurable agent-change surface.
- Reddit and community threads repeatedly complain that AI makes PRs faster to create but harder to review, especially when scope is broad, evidence is weak, or reviewers have to reconstruct context.

Interpretation:

- The review bottleneck is real.
- Maintainer judgment, context, and evidence are the scarce resources.
- Relay's review-readiness, PR comment, reviewer-pack, and release checklist artifacts point at the right pain.
- Relay still has to prove that its artifacts are better than asking Codex to summarize the thread.

### Direct AI PR review market

AI PR review is already a commercial and open-source category:

- GitHub Copilot code review is native to the GitHub PR reviewer flow and can leave review comments with suggested changes.
- CodeRabbit provides automated context-aware PR reviews, PR walkthrough comments, IDE/CLI review, planning, and Slack workflows.
- Graphite AI reviews focus on real bugs, full-codebase context, actionable suggestions, customization, and analytics.
- Qodo / Qodo Merge provides AI PR review agents, summaries, improvements, labeling, chat, and policy workflows.
- PR-Agent is a mature open-source PR review bot with 11,414 stars and 1,537 forks on 2026-05-31.
- Greptile and similar products have public pricing, which suggests the category can support commercial demand.

Interpretation:

- This is stronger evidence that PR review pain is worth solving.
- It is also stronger evidence that Relay must not become a generic AI PR reviewer.
- Relay must test whether maintainers want Codex-run provenance and readiness evidence in addition to, before, or instead of AI review bots.
- Paid AI review tools are not proof that Relay can earn money. Relay needs its own usage, sponsor, or support signal after a real handoff is used.

## Competitive Reality

Codex Goals already own thread-scoped continuation:

- objective
- stopping condition
- validation loop
- decision to continue or finish within the active Codex run

Claude Managed Agents and Symphony-style systems point toward larger managed execution layers:

- long-running sessions
- sandboxes
- event streams
- isolated implementation runs
- work-board integration

Paperclip, vibe-kanban, Warp, agentmemory, and skills libraries already own much of the broader workflow territory.

Copilot, CodeRabbit, Graphite, Qodo, PR-Agent, and Greptile already own much of the AI PR review territory.

Relay's possible wedge is therefore intentionally small:

> After an agent run touches a repo, Relay produces maintainer-readable GitHub artifacts that survive outside the chat thread.

If users want a board, memory engine, runtime, scheduler, or autonomous PR factory, Relay should point them elsewhere.

If users want inline bug finding, automated suggestions, or a required review bot, Relay should point them to AI PR review tools instead.

## Relay Evidence Today

Validated:

- Public repository exists.
- Public releases exist.
- Runtime can generate handoff, review-readiness, PR comment, reviewer-pack, and release checklist artifacts.
- GitHub Actions can generate and publish review-readiness artifacts on PRs.
- Documentation now clearly states that Relay is not Codex Goals, not Paperclip, not a board, and not a memory engine.

Not validated:

- No outside maintainer has recorded a `reused` or `edited_heavily` outcome.
- No external repository has installed and run Relay as part of its PR process.
- No evidence yet that Relay produces more stars than normal repo polish.
- No evidence yet that anyone would sponsor, donate, or pay for hosted Relay features.
- No evidence yet that the `.relay/` files stay useful after several real PRs instead of becoming stale documentation.

## Traction Gates

Do not claim "people want this" until at least one of these gates passes.

### Gate 1: Outside reviewer usefulness

Target:

- 3 outside maintainers or frequent PR reviewers read a Relay handoff.
- At least 2 mark the output as `reused` or `edited_heavily`.
- At least 1 reviewer says what they would remove or simplify.

Evidence artifact:

- GitHub issue comments on `Test Relay handoff with an outside maintainer`.

### Gate 2: External repo trial

Target:

- 1 public repository outside this project runs `review-readiness` or `pr-comment`.
- The maintainer posts or links the generated artifact in a real PR or issue.
- The result is not just a demo by the Relay author.

Evidence artifact:

- Linked PR, issue, workflow artifact, or repository commit.

### Gate 3: Star conversion from useful artifact

Target:

- 10 stars from accounts not controlled by the maintainer after public sharing.
- At least 2 stars can be traced to people who saw the demo, reviewer pack, or install flow.

Evidence artifact:

- GitHub stargazer snapshot plus linked outreach or discussion thread.

### Gate 4: Retention

Target:

- Relay is used on 3 separate PRs or releases in the same outside repo.
- At least one maintainer edits a generated artifact instead of ignoring it.

Evidence artifact:

- Three linked PRs/releases and one maintainer comment.

### Gate 5: Money signal

Target:

- 1 maintainer asks for a paid hosted feature, private workflow support, sponsorship link, or setup help.
- Or 1 sponsor/donation arrives after a real usage event, not after a generic announcement.

Evidence artifact:

- Sponsor, donation, support request, or public comment.

## Monetization Hypotheses

Relay should not build paid features now. The free core must prove pull first.

Possible later paths:

- GitHub Sponsors for maintainers who use the plugin and want ongoing maintenance.
- Paid setup/support for teams adopting Codex-heavy review workflows.
- Hosted dashboard only if multiple teams ask to aggregate review-readiness artifacts across repos.
- Private security/threat-model templates only if users repeatedly ask for regulated or sensitive review gates.

Do not build:

- SaaS dashboard before external repo trials.
- Billing before a repeated usage signal.
- Enterprise claims before a team asks for audit, permission, or reporting features.

## Stop Or Pivot Criteria

Pause or archive the product direction if any of these happen:

- 3 outside reviewers mark the handoff `ignored` or `confusing`.
- 20 targeted maintainer asks produce no trial, no feedback, and no stars.
- Reviewers say the output is not better than a normal Codex summary.
- Users mainly ask for agent memory, a kanban board, or a runtime instead of PR/release handoff evidence.
- Codex adds first-party repo-local PR/release artifacts that make Relay redundant.
- Maestro/Kage/Recall-style tools show stronger adoption for the same narrow handoff workflow.

Pivot options:

- Keep Relay as a research/demo repository.
- Turn Relay into a tiny schema and GitHub Actions workflow rather than a Codex App plugin.
- Contribute the useful handoff templates to a larger skills project.
- Archive the repo honestly if the wedge cannot be validated.

## Next Evidence Work

The next work should be validation, not feature expansion:

1. Get one outside reviewer to complete issue #24.
2. Run the GitHub Actions review-readiness workflow on every real Relay PR.
3. Share the reviewer-pack example with targeted maintainers who already review AI-generated PRs.
4. Track every response as `reused`, `edited_heavily`, `ignored`, or `confusing`.
5. Only release runtime changes when the validation evidence changes the product.

The public evidence queue lives in [validation-ledger.md](validation-ledger.md).

## Sources

- GitHub Blog, Agent pull requests are everywhere: https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- GitHub Copilot code review docs: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review
- CodeRabbit docs: https://docs.coderabbit.ai/
- CodeRabbit PR walkthroughs: https://docs.coderabbit.ai/pr-reviews/walkthroughs
- Graphite AI reviews: https://graphite.com/docs/ai-reviews
- Qodo Merge docs: https://docs.qodo.ai/v1/qodo-merge
- PR-Agent repository: https://github.com/The-PR-Agent/pr-agent
- Greptile pricing: https://www.greptile.com/pricing
- OpenAI Codex Goals: https://developers.openai.com/codex/use-cases/follow-goals
- OpenAI Cookbook, Using Goals in Codex: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- Claude Managed Agents overview: https://platform.claude.com/docs/en/managed-agents/overview
- Anthropic Engineering, Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Tomasz Tunguz, Software After AI: https://tomtunguz.com/harnessing-ai
- arXiv 2601.04886, Analyzing Message-Code Inconsistency in AI Coding Agent-Authored Pull Requests: https://arxiv.org/abs/2601.04886
- arXiv 2601.17413, When AI Agents Touch CI/CD Configurations: https://arxiv.org/abs/2601.17413
- Reddit, Is AI coding making pull requests harder to review?: https://www.reddit.com/r/github/comments/1rofktt/is_ai_coding_making_pull_requests_harder_to_review/
- Reddit, AI-generated PRs are faster to write but slower to review: https://www.reddit.com/r/ClaudeCode/comments/1roy3o0/aigenerated_prs_are_faster_to_write_but_slower_to/
