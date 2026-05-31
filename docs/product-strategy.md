# Product Strategy: Relay for Codex

Relay should become a Codex App-native GitHub handoff adapter for long-running Codex work. It should not become a general agent company, an agent framework, a memory engine, a local-first evidence ledger, or a dashboard clone.

## Research frame

This pass uses the Double Diamond model:

- Discover: understand the actual problem and adjacent products before assuming the answer.
- Define: choose the narrow problem Relay can own.
- Develop: explore product shapes that can beat the current alternatives.
- Deliver: test the smallest public artifact that proves the positioning.

The model matters because Relay sits near crowded territory: Codex now has native goal and continuation features, while Paperclip already covers broad multi-agent operations. Relay has to win a smaller, sharper job.

### Current Double Diamond status

Relay is currently in late Discover and early Define.

What is known:

- The market is real: agents now need durable work records, review gates, release handoff, and recovery paths.
- The crowded areas are also real: hosted agent runtimes, kanban boards, memory engines, broad skills packs, and autonomous-agent platforms are already occupied.
- Relay's strongest wedge is repo-local maintainer evidence: small artifacts that make PR review, release readiness, recovery notes, and remaining human judgment explicit.
- The sharpest public pain is review burden after agent work, not agent continuation itself: large generated PRs, shallow PR descriptions, hidden sensitive changes, and maintainers needing evidence before spending review attention.

What is not ready yet:

- Relay is not ready for a larger feature buildout.
- Relay is not ready for a new patch release just because more research landed.
- Relay is not ready to claim a finished product category until the demo proves the wedge in one real workflow.

The next gate is Define: turn the research into one primary use case, one demo path, and one public message. The current validation plan is tracked in [validation-plan.md](validation-plan.md), the stricter competitor map is tracked in [market-map.md](market-map.md), and community pain research is tracked in [community-research.md](community-research.md).

## Discover

### What Paperclip proves

Paperclip's public positioning is strong: it is a full control plane for managing agents at work, with a server, React UI, org charts, goal alignment, scheduled heartbeats, budgets, governance, ticketing, audit trails, plugins, secrets, and multi-company isolation.

The clearest lessons:

- A big metaphor travels. "Run a company made of agents" is easier to remember than a feature list.
- A real control plane needs governance, cost control, durable work records, and scheduling.
- A credible open-source agent product needs quickstart, docs, Discord/community links, roadmap, releases, telemetry policy, security policy, and visible demos.
- Paperclip explicitly says it is not a code review tool and not for single-agent use. That leaves room around maintainer workflows and repo-specific handoff.

### What Paperclip should not make us copy

Relay should not copy:

- server-first architecture
- org charts and agent employment metaphors
- budget/accounting systems
- multi-company data isolation
- secret storage
- a large dashboard before the repo workflow is proven
- "manage every agent" positioning

Those are already Paperclip's territory. Copying them would make Relay late, heavy, and harder to explain.

### What Codex native goals change

Codex-native goals reduce the value of a generic "keep working later" pitch. OpenAI positions `/goal` for long-running work with a durable objective, verifiable stopping condition, validation loop, and evidence-based completion. Relay should not sell continuation as the main product.

This overlap is stronger than the original strategy admitted. If Relay claims to decide whether Codex should continue, it is mostly duplicating the native Goal loop.

Instead, Relay should treat Codex continuation as upstream and add what a maintainer still needs after the run:

- a GitHub-ready PR comment or release note
- a small repo-local evidence bundle
- a review checklist tied to the files and commands touched
- explicit notes about what still needs human review

The boundary is simple:

- Codex Goal: thread-scoped completion contract.
- Relay: GitHub-facing handoff adapter after the Goal run.

### What AI workflow writing reinforces

Tom Tunguz's writing on harnessing AI reinforces the same product direction: the durable value is not only a smarter model, but the surrounding harness that turns model work into reliable workflows. Relay should be that harness for one specific slice of software work: Codex-driven repository maintenance.

That means Relay should invest in:

- evidence capture
- handoff surfaces
- review gates
- recovery paths
- release and PR workflows

It should avoid a vague "AI productivity" message and keep proving value through concrete maintainer flows.

### What Claude Managed Agents changes

Claude Managed Agents shows that platform vendors are also moving toward managed long-running agents: hosted or self-hosted sandboxes, persistent sessions, event streams, built-in tools, MCP, files, and resumable state. Anthropic's engineering write-up goes further: their durable primitives are session logs, replaceable harnesses, and decoupled sandboxes/tools. The design goal is stable interfaces around long-horizon agent work even as the harness changes.

That makes a generic "agent runtime" or "long-running session" pitch weaker for Relay. It also makes Relay's repo-local layer more important.

Relay should instead stay deliberately local and portable:

- do not compete with managed sandboxes, event streams, or provider-specific agent hosting
- keep the durable artifact inside the repository, not only inside a vendor session
- make `.relay/` a small, inspectable session summary that can survive provider, thread, or harness changes
- make release, PR, and review gates visible in files that GitHub, maintainers, and future agents can inspect
- treat Codex goals and managed-agent sessions as upstream execution layers that Relay can summarize, audit, and hand off

This also makes branding simpler: Relay should remain its own maintainer workflow layer, not appear to be a Codex, Claude, or Paperclip clone.

### What external coding-agent heuristics reinforce

Common coding-agent advice says the same thing in a more tactical way: direction before speed, plan before implementation, compare options before committing, split complex work into phases, and use human review at the high-leverage checkpoints.

Relay should not turn that into a generic multi-agent planning product. The useful translation is narrower:

- make phase boundaries visible in `.relay/queue.md`
- make review checkpoints visible in `.relay/handoff.md`
- make "stop and inspect" cheaper than another blind coding pass
- preserve enough evidence that a maintainer can compare plans or execution paths later

### What agent-skills proves

Addy Osmani's agent-skills project proves there is demand for production-grade agent workflows packaged as reusable skills. Its strongest pattern is not breadth alone; it is the discipline around lifecycle entry points, verification gates, progressive disclosure, and anti-rationalization language that prevents agents from skipping senior-engineering habits.

Relay should learn from that packaging without becoming a general skill library:

- keep Relay skills narrow and maintainer-workflow specific
- make every Relay skill end with evidence, not vibes
- use lifecycle verbs users already understand: inspect, recover, hand off, release
- keep supporting references lazy and small so Codex loads only what it needs
- avoid competing with broad engineering skill packs; Relay's value is stateful repo handoff

### What agentmemory proves

agentmemory proves that persistent memory for coding agents is a real demand, especially when it is cross-agent, automatic, searchable, benchmarked, and cheap to run. Its center of gravity is recall: remembering architecture decisions, bug fixes, preferences, and session history so agents do not rediscover the same context.

Relay should not compete with a full memory engine:

- do not build vector search, graph memory, or a memory server in the core product
- avoid claiming that Relay remembers everything
- store only the maintainer-facing state needed to continue, stop, recover, review, or release
- make `.relay/` readable by humans first and useful to memory systems second
- allow future integrations where agentmemory-like tools can index Relay artifacts, rather than replacing them

### What Warp proves

Warp shows that agentic development can be packaged as a visible open-source maintenance workflow, not only as an invisible assistant feature. The useful pattern is issue triage, readiness labels, specs, implementation, PR review, contributor coordination, and public activity around real repository work.

Relay should borrow the maintainer-workflow lesson:

- use GitHub Issues and PRs as the public surface, not a custom dashboard first
- make readiness explicit with labels or checklist states
- treat demo activity as real maintenance, not synthetic churn
- eventually show a compact "issue -> Relay verdict -> handoff -> PR/release" path

### What OpenAI Symphony changes

Symphony is the closest strategic neighbor from OpenAI itself. Its pitch is to turn project work into isolated autonomous implementation runs, connected to work boards, proof of work, CI, PR reviews, complexity analysis, walkthroughs, and safe landing. That is bigger than Codex Goals: it points toward teams managing work instead of supervising coding agents.

Relay should not compete with Symphony-style orchestration:

- do not spawn or schedule isolated implementation runs as the core product
- do not become a Linear-board or project-management orchestrator
- treat Symphony-like systems as upstream executors that can produce work
- make Relay the small downstream layer that records verdict, evidence, handoff, release readiness, and maintainer review state in the repository

If Symphony manages work at the board level, Relay should make each repo handoff trustworthy at the PR/release level.

### What Automaton warns against

Conway Automaton explores the opposite end of the market: continuously running, self-funding, self-modifying, self-replicating agents with wallets, identity, heartbeat loops, survival pressure, and world-write access. It is memorable because the story is extreme.

Relay should not borrow that autonomy story:

- no self-replication, wallet, survival, or autonomous business metaphor
- no unattended world-write loop as the default product promise
- keep human approval gates explicit for releases, external announcements, and high-risk actions
- make "stop and ask for review" a strength, not a weakness

The useful lesson is only the audit trail: if agents can act over long periods, every meaningful state transition needs a durable record.

### What vibe-kanban proves

vibe-kanban proves that a local board for coding agents is a real product category: plan with kanban issues, give each agent a branch/terminal/dev server workspace, review diffs inline, preview the app, create PRs, and merge. It also supports many coding agents, including Codex.

Relay should not build another agent board:

- GitHub Issues and PRs are enough for the first public surface
- avoid owning terminals, dev servers, previews, and inline review UI
- make Relay artifacts useful inside board tools rather than replacing them
- focus the demo on a tiny path: issue or task -> Codex run -> Relay verdict -> PR/release handoff

### What Matt Pocock's skills prove

Matt Pocock's skills project proves another angle on the same market: engineers want small, adaptable skills that preserve control instead of handing the whole process to a rigid framework. Its strongest ideas for Relay are shared project language, grilling/alignment before work, disciplined diagnosis, TDD loops, and compact handoff.

Relay should adopt the packaging style:

- keep skills small enough to inspect and modify
- teach the repo's vocabulary in `mission.md` and handoff files
- make diagnosis and recovery loops explicit
- avoid owning the entire development process; own the relay between runs and maintainers

### Discovery synthesis

| Category | Examples | What they own | Relay stance |
| --- | --- | --- | --- |
| Native continuation | Codex Goals | Thread-scoped objective, validation loop, completion criteria | Use as upstream signal; do not compete on "keep going later" |
| Managed runtimes | Claude Managed Agents, Symphony | Sandboxes, sessions, event logs, isolated implementation runs | Stay downstream and repo-local |
| Agent control planes | Paperclip, vibe-kanban, Warp/Oz workflows | Boards, agent workspaces, org/team workflows, PR UI | Integrate through GitHub artifacts; do not build a board first |
| Memory engines | agentmemory | Cross-agent recall, search, auto-capture, benchmarks | Store only maintainer state; allow indexing later |
| Skills packs | agent-skills, Matt Pocock skills | Reusable engineering process and expert workflows | Keep Relay skills narrow, inspectable, and evidence-driven |
| Autonomous agents | Automaton | Self-funding, self-modification, survival loops | Reject autonomy metaphor; keep human review gates |
| Review bottleneck | GitHub guidance, Reddit maintainer threads, MSR 2026 agent PR research | Human judgment, scope control, risky-file review, evidence before merge | Own the small review-readiness artifact, not the review bot |

The product boundary after discovery:

> Relay is not the system that runs the agent. Relay is the small repo-local record that lets a maintainer trust, review, resume, or release the work after the agent ran.

## Define

### Product thesis

Relay is a Codex App-native adapter that turns long-running Codex work into maintainer-readable GitHub artifacts.

It answers:

- What can be posted into the PR?
- What should the reviewer focus on?
- What verification happened or still needs to happen?
- What should go into release notes?
- What repo-local evidence should survive after the Codex thread ends?
- Is this agent PR ready for review, or should it be split, verified, or sent back before consuming maintainer attention?

### Confidence level

This is still a product bet, not a proven category.

Relay is likely useful if:

- a maintainer uses Codex often enough that work spans multiple threads, PRs, or release steps
- the repo needs a durable handoff that GitHub reviewers can inspect or paste into review surfaces
- the hard part is converting a Codex run into PR/release evidence, not deciding whether Codex should keep running

Relay is probably not useful if:

- the user only runs one-off coding prompts
- the project already has a full agent board and does not need repo-local handoff files
- a plain GitHub issue checklist is enough
- the maintainer does not care about preserving agent-run evidence in the repository
- Maestro, Kage, Recall, or another local-first continuity/evidence tool is already installed and trusted

The validation target is simple: a maintainer should see the README demo and immediately understand one GitHub workflow where Relay saves time or reduces review anxiety.

### Primary user

The first user is not "anyone using agents." It is a maintainer or solo builder who uses Codex heavily enough that work spans threads, branches, PRs, releases, or scheduled follow-ups.

They care about:

- not losing context
- knowing whether the agent is actually progressing
- avoiding repeated test churn
- giving future Codex runs a clean handoff
- making the public repository look real, maintained, and trustworthy

### Non-goals

Relay should not:

- replace Codex goals
- replace GitHub Issues or PRs
- become a full task manager
- orchestrate many unrelated agents
- store secrets or account data
- require a server for the core workflow
- make autonomous changes when the verdict is `needs_human` or `needs_review`

## Develop

### Product shape

The strongest near-term shape is a Codex App plugin plus repo-local protocol:

```text
.relay/
  mission.md          project goal and success definition
  state.md            current verdict and recent signal
  queue.md            next work or recovery checklist
  guardrails.md       when to stop, escalate, or recover
  handoff.md          PR/release handoff brief
  events.jsonl        lightweight event log
```

The public-facing product should feel like:

> "After Codex finishes a run, Relay gives you the PR or release handoff."

### Better-than-Paperclip wedge

Relay can beat a general control plane in one narrow place:

- no server required for the core loop
- works inside an existing GitHub repository
- produces files maintainers can inspect, diff, commit, and review
- focuses on PR/release handoff instead of agent-company management
- treats "stop and review" as a first-class success state

### Better-than-native-Codex wedge

Relay can beat native goals in one narrow place:

- goals live in the conversation; Relay artifacts live in the repo and GitHub workflow
- Codex can complete a goal; Relay packages the outcome for PR review and release handoff
- native goal state is useful to the current thread; Relay output is useful to reviewers and future maintainers

### Product experiments

1. PR Flight Recorder
   - Generate `.relay/handoff.md` from current state, queue, and events.
   - Include last successful change, likely stuck point, review checklist, and next command.
   - Use it as the concrete demo for issue #3.

2. PR Comment Adapter
   - Generate `.relay/pr-comment.md` from `.relay/handoff.md`.
   - Keep it paste-only unless a human explicitly approves posting to GitHub.
   - Use it to validate whether Relay is better than asking Codex to summarize the thread.

3. Release Handoff
   - Add a release checklist that maps state -> tests -> changelog -> tag -> GitHub release.
   - Keep human approval explicit.
   - Use it to close issue #4.

4. Stuck Recovery Demo
   - Record or script a fixture where repeated failure events flip the verdict to `needs_review`.
   - Show the queue rewrite.
   - Use it as the next production-quality walkthrough after the first runtime-generated GIF.

5. Public Proof Loop
   - Keep small PRs visible.
   - Close issues only when their done criteria are actually met.
   - Publish patch releases only after meaningful merged changes.

## Deliver

### Next product milestone

`v0.2.0` should not be "more automation." It should be:

> Relay can produce a GitHub-ready PR handoff from a Codex Goal/run.

Acceptance:

- `handoff.md` exists and is generated by the runtime.
- `pr-comment.md` exists and is generated by the runtime.
- `release-checklist.md` exists and is generated by the runtime.
- A stuck fixture demonstrates `continue -> needs_review -> recovery handoff`.
- README shows one real before/after flow.
- Release notes explain the difference from Codex native goals and Paperclip.

### Launch message

Use this short pitch:

> Relay for Codex turns long-running Codex work into GitHub-ready maintainer handoffs.

Avoid:

- "agent company"
- "orchestration platform"
- "task manager"
- "autonomous business"
- "replacement for Codex goals"

### Open questions

- Should `.relay/handoff.md` be committed by default or generated on demand?
- Should Relay create GitHub issue/PR comments, or only draft them for human approval?
- Should scheduled automations live in Codex App only, or should Relay also render copy-paste automation recipes?
- What is the minimum visual demo that makes a maintainer understand the value in 30 seconds?

## Sources

- Paperclip GitHub repository: https://github.com/paperclipai/paperclip
- Design Council Framework for Innovation and Double Diamond: https://www.designcouncil.org.uk/resources/framework-for-innovation/
- OpenAI Codex goal use case: https://developers.openai.com/codex/use-cases/follow-goals
- OpenAI Cookbook, Using Goals in Codex: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- Tom Tunguz, Harnessing AI: https://tomtunguz.com/harnessing-ai
- Anthropic Claude Managed Agents overview: https://platform.claude.com/docs/en/managed-agents/overview
- Anthropic Engineering, Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Addy Osmani, agent-skills: https://github.com/addyosmani/agent-skills
- rohitg00, agentmemory: https://github.com/rohitg00/agentmemory
- Warp: https://github.com/warpdotdev/warp
- OpenAI Symphony: https://github.com/openai/symphony
- Conway Research, Automaton: https://github.com/Conway-Research/automaton
- BloopAI, vibe-kanban: https://github.com/BloopAI/vibe-kanban
- Matt Pocock, skills: https://github.com/mattpocock/skills
