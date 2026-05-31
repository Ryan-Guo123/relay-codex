# Product Strategy: Relay for Codex

Relay should become the maintainer workflow layer for long-running Codex work. It should not become a general agent company, an agent framework, or a dashboard clone.

## Research frame

This pass uses the Double Diamond model:

- Discover: understand the actual problem and adjacent products before assuming the answer.
- Define: choose the narrow problem Relay can own.
- Develop: explore product shapes that can beat the current alternatives.
- Deliver: test the smallest public artifact that proves the positioning.

The model matters because Relay sits near crowded territory: Codex now has native goal and continuation features, while Paperclip already covers broad multi-agent operations. Relay has to win a smaller, sharper job.

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

Codex-native goals reduce the value of a generic "keep working later" pitch. Relay should not sell continuation as the main product.

Instead, Relay should treat Codex continuation as an input and add what a maintainer still needs:

- inspectable repo-local state
- a current verdict before more work happens
- stuck-recovery policy
- PR and release handoff
- audit-friendly evidence of what changed, what failed, and what needs review

## Define

### Product thesis

Relay is the repo-local flight recorder and handoff layer for Codex-maintained software projects.

It answers:

- What is Codex trying to do in this repo?
- What changed recently?
- Is the project safe to continue?
- Is Codex looping, blocked, or drifting?
- What should a human maintainer review before the next run?
- What is the smallest next action for PR or release handoff?

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

> "Before Codex keeps going, Relay tells you whether the repo is actually moving."

### Better-than-Paperclip wedge

Relay can beat a general control plane in one narrow place:

- no server required for the core loop
- works inside an existing GitHub repository
- produces files maintainers can inspect, diff, commit, and review
- focuses on PR/release handoff instead of agent-company management
- treats "stop and review" as a first-class success state

### Better-than-native-Codex wedge

Relay can beat native goals in one narrow place:

- goals live in the conversation; Relay state lives in the repo
- Codex can continue; Relay explains whether continuing is wise
- native goal state is useful to the current thread; Relay handoff is useful to future maintainers, future threads, and PR review

### Product experiments

1. PR Flight Recorder
   - Generate `.relay/handoff.md` from current state, queue, and events.
   - Include last successful change, likely stuck point, review checklist, and next command.
   - Use it as the concrete demo for issue #3.

2. Release Handoff
   - Add a release checklist that maps state -> tests -> changelog -> tag -> GitHub release.
   - Keep human approval explicit.
   - Use it to close issue #4.

3. Stuck Recovery Demo
   - Record or script a fixture where repeated failure events flip the verdict to `needs_review`.
   - Show the queue rewrite.
   - Use it to close issue #2 when a real GIF/video exists.

4. Public Proof Loop
   - Keep small PRs visible.
   - Close issues only when their done criteria are actually met.
   - Publish patch releases only after meaningful merged changes.

## Deliver

### Next product milestone

`v0.2.0` should not be "more automation." It should be:

> Relay can produce a maintainer-grade PR handoff from repo-local state.

Acceptance:

- `handoff.md` exists and is generated by the runtime.
- A stuck fixture demonstrates `continue -> needs_review -> recovery handoff`.
- README shows one real before/after flow.
- Release notes explain the difference from Codex native goals and Paperclip.

### Launch message

Use this short pitch:

> Relay for Codex is a repo-local flight recorder for long-running Codex work. It tells maintainers when Codex should continue, stop, recover, or hand off a PR.

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
