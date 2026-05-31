# Relay Market Map

This document is the stricter version of the product research. The question is not "can Relay be described differently?" The question is:

> Is this already being solved well enough that Relay should stop, shrink, or pivot?

## Short Answer

Yes, much of the original Relay idea is already covered.

The crowded areas are:

- Codex-native goal continuation
- managed long-running agent sessions
- agent work boards and PR orchestration
- local-first repo memory
- local-first handoff/evidence ledgers
- reusable agent skills

Relay should not continue as a generic "decide whether Codex should continue" tool. That overlaps too much with Codex Goals and newer harnesses.

The only potentially useful remaining wedge is smaller:

> A Codex App-native adapter that turns a finished goal/run into GitHub-ready maintainer artifacts: PR comment, release note, review checklist, and minimal `.relay/` evidence bundle.

Even that wedge is not proven. Maestro already covers a larger and more serious version of the local-first evidence/handoff space.

## Competitor Categories

### 1. Native Goal / Continuation

Examples:

- OpenAI Codex Goals

What they own:

- Thread-scoped objective
- completion criteria
- validation loop
- decision to continue or stop within the active Codex run

Implication:

Relay should stop positioning itself as the system that decides whether Codex should continue. That is native territory.

Relay can only add value after a run by packaging evidence for people and repository surfaces that were not inside the thread.

### 2. Managed Agent Runtime / Work Orchestration

Examples:

- Claude Managed Agents
- OpenAI Symphony
- Optio

What they own:

- long-running sessions
- sandboxes or workspaces
- event streams and logs
- issue/ticket intake
- CI and review feedback loops
- autonomous task-to-PR pipelines

Important observation:

Optio explicitly goes from ticket to merged PR and watches CI/review feedback. Symphony explicitly moves from supervising coding agents to managing work. These systems attack the whole workflow, not just the handoff.

Implication:

Relay should not build a task runner, board, dashboard, scheduler, CI feedback loop, or autonomous merge pipeline.

### 3. Agent Boards / PR UI

Examples:

- Paperclip
- vibe-kanban
- Warp/Oz-style agent workflows

What they own:

- agent workspaces
- kanban/task planning
- branch and terminal management
- diff review
- previews
- PR creation and merge surfaces

Important observation:

vibe-kanban already says the highest leverage is planning and reviewing coding agents. It gives each agent a branch, terminal, dev server, diff review UI, previews, PR creation, and merge path.

Implication:

Relay should not build a board. If Relay survives, it must be useful as a tiny artifact producer inside existing GitHub and Codex surfaces.

### 4. Local-First Repo Memory

Examples:

- codemem
- Kage
- Recall
- agentmemory
- aictx-style local continuity tools

What they own:

- repo-specific memory
- decisions, gotchas, corrections, dead ends
- searchable recall
- session trails
- local viewer or dashboard
- MCP/lifecycle hook injection
- local-first storage

Important observation:

Kage already stores reviewable repo-local packets in `.agent_memory/`. Recall learns from corrections and review feedback, keeps quality gates, and injects trusted instructions into agents. codemem explicitly targets decisions, dead ends, session trails, and handing context between humans and coding agents.

Implication:

Relay should not claim "repo memory" as a differentiator. That market is already active and better scoped by memory-specific products.

### 5. Local-First Handoff / Evidence Ledger

Examples:

- Maestro
- agent-handoff-protocol-style projects
- session-handoff skills

What they own:

- on-disk state model
- specs, tasks, contracts, evidence, verdicts
- lifecycle handoff envelopes
- verification gates
- local-first trust substrate
- multi-session handoff across Codex, Claude Code, and other agents

Important observation:

Maestro is the most direct overlap. It describes itself as a local-first agent harness for the spec-to-ship loop with on-disk state for specs, tasks, evidence, contracts, handoffs, and principles. It has verdicts, handoff envelopes, evidence rows, MCP tools, risk classes, verification protocols, and a mission-control surface.

Implication:

The original Relay idea is not strong enough against Maestro. Relay cannot win as "the local-first evidence and handoff layer" in general.

Relay must either:

- become much narrower and Codex App-native, or
- stop and redirect effort toward using/extending an existing project.

### 6. Reusable Agent Skills

Examples:

- Addy Osmani's agent-skills
- Matt Pocock's skills
- spec-handoff/session-handoff skills

What they own:

- packaged process
- verification gates
- handoff templates
- expert workflow language
- small composable skills

Implication:

Relay should not become a broad skills library. At most, it can ship a few Codex-specific skills that call a very small artifact generator.

## Strongest Direct Overlaps

| Product | Overlap With Relay | Why It Matters |
| --- | --- | --- |
| Codex Goals | continue/stop decision, completion criteria, validation loop | Makes Relay's original verdict pitch redundant |
| Maestro | local-first state, evidence, verdicts, handoff envelopes, verification | Directly challenges Relay's repo-local evidence idea |
| Kage | repo-local reviewable memory packets for agents | Undercuts "repo memory" positioning |
| Recall | lifecycle hooks, trusted repo instructions, local dashboard, session feed | Covers memory + injection better than Relay should |
| Optio | ticket-to-merged-PR automation, CI/review feedback loop | Owns broader workflow orchestration |
| vibe-kanban | board, branch/workspace, diff review, PR creation | Owns the visual planning/review layer |
| Paperclip | broad agent management/control plane | Owns the memorable "manage agents at work" category |

## Product Decision

Relay should not be pitched as:

- "Codex continuation"
- "repo memory"
- "agent state"
- "handoff protocol"
- "agent control plane"
- "agent board"
- "trust substrate"

Those are already occupied or too close to stronger projects.

The possible pivot is:

> Relay is a Codex App-native GitHub handoff adapter.

It takes the state that Codex Goals, Codex threads, or Relay's lightweight files already have, and produces maintainer artifacts:

- PR comment draft
- PR review checklist
- release note draft
- release checklist
- concise evidence bundle

This is less ambitious, but it is less duplicated.

## What Relay Should Do Next

### Keep

- Codex App plugin packaging
- `.relay/handoff.md` as a generated artifact
- `.relay/release-checklist.md`
- README demo showing GitHub-facing handoff
- validation plan

### De-emphasize

- Relay's own continue/recover verdict as a primary product claim
- "memory" language
- automation packs that imply Relay decides to continue work
- broad "flight recorder" claims

### Add

- `pr-comment` command that turns a handoff into a GitHub-ready PR comment
- explicit "Codex Goal is upstream" section in README
- examples showing Relay after a Codex Goal run, not instead of one
- comparison table saying when to use Maestro/Kage/Recall/vibe-kanban instead

### Consider Removing Later

- `continue-with-relay` as a top-level skill
- automation pack language that creates follow-up work based on Relay's own verdict
- any claims that Relay is a general local-first handoff/evidence layer

## Kill Criteria

Relay should be paused or archived if the next validation shows:

- users want Maestro/Kage/Recall features more than GitHub handoff artifacts
- Codex exposes repo-local PR/release handoff directly
- the PR comment/release note output is not better than asking Codex to summarize the thread
- the product cannot be explained without saying "it is like Goals, but..."

## Current Recommendation

Do one more narrow validation, not a feature buildout:

1. Build `pr-comment` as a Codex App-native handoff adapter.
2. Test whether the generated PR comment is better than a normal Codex thread summary.
3. If it is not clearly better, stop expanding Relay and turn the repo into a research artifact or plugin experiment.

## Sources

- OpenAI Codex goal use case: https://developers.openai.com/codex/use-cases/follow-goals
- OpenAI Cookbook, Using Goals in Codex: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- OpenAI Symphony: https://github.com/openai/symphony
- Anthropic Claude Managed Agents overview: https://platform.claude.com/docs/en/managed-agents/overview
- Anthropic Engineering, Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Optio: https://optio.host/
- Paperclip: https://github.com/paperclipai/paperclip
- vibe-kanban: https://github.com/BloopAI/vibe-kanban
- Maestro: https://github.com/ReinaMacCredy/maestro
- codemem: https://codemem.sh/
- Kage: https://kage-core.com/
- Recall: https://recallmemory.dev/
- rohitg00, agentmemory: https://github.com/rohitg00/agentmemory
- Addy Osmani, agent-skills: https://github.com/addyosmani/agent-skills
- Matt Pocock, skills: https://github.com/mattpocock/skills
