# Relay Demo Storyboard

This is the target for the first short demo GIF or video. It should prove Relay's narrow wedge without making the product look like another agent runtime, kanban board, or memory engine.

Current demo asset:

```text
docs/assets/relay-demo.gif
```

Regenerate it with:

```bash
python3 tools/render_demo_gif.py
```

The renderer requires Pillow. It copies the `in-progress-repo` fixture, runs the real Relay runtime commands, and builds the GIF from generated `.relay` files.

## Demo Goal

Show that Relay turns a long-running Codex task into a maintainer-readable handoff.

The viewer should understand this in 30 seconds:

> Codex did work. Relay turns the run into a maintainer-readable PR or release handoff.

## Audience

The first viewer is a solo maintainer or small-team engineer who already uses Codex, Claude Code, Cursor, or another coding agent for real repository work.

They are not asking for another dashboard. They want to know:

- Did the agent actually make progress?
- What changed?
- What failed?
- Is it safe to keep going?
- What should I review before merge or release?

## 30-Second Script

1. Open a repository with Relay enabled.
2. Show `.relay/state.md` as supporting repo evidence.
3. Run a small Codex task that touches code or docs.
4. Run the Relay handoff command.
5. Show `.relay/handoff.md` with:
   - current verdict
   - recent progress
   - verification command
   - review checklist
   - next action
6. Run the release checklist command.
7. Show `.relay/release-checklist.md` with human approval gates.
8. End on the message:

```text
Relay turns long-running Codex work into GitHub-ready handoffs.
```

## Shot List

### Shot 1: Before

Show the repo and the `.relay/` files:

```text
.relay/
  mission.md
  state.md
  queue.md
  guardrails.md
```

Caption:

```text
Before Codex keeps going, Relay checks the repo state.
```

### Shot 2: Work Happens

Show a small diff or task result. Keep it concrete, not cinematic:

- one docs update
- one tiny code change
- one test command

Caption:

```text
Codex works in the repo, but the handoff stays inspectable.
```

### Shot 3: PR Handoff

Show:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py handoff
```

Then show `.relay/handoff.md`.

Caption:

```text
Relay turns the run into a maintainer-grade handoff.
```

### Shot 4: Release Gate

Show:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py release
```

Then show `.relay/release-checklist.md`.

Caption:

```text
Release steps stay gated by verification and human approval.
```

### Shot 5: Ending Frame

End with the concise product line:

```text
GitHub-ready handoffs for Codex-maintained projects.
```

## What Not To Show

- Do not show a generic prompt demo.
- Do not present Relay as a multi-agent dashboard.
- Do not claim Relay replaces Codex Goals.
- Do not show fake churn or synthetic activity as if it were maintenance.
- Do not show a release being published unless there is a real merged change.

## Acceptance Criteria For Issue #2

Issue #2 can close when the repository has a real GIF or video that:

- follows the 30-second path above
- shows actual Relay-generated files
- includes at least one real verification command
- makes the Codex Goals boundary clear
- is linked from the README near the demo usage docs

`docs/assets/relay-demo.gif` now satisfies these criteria for the first public demo. A future hand-recorded video can improve production quality, but it should not block the initial issue.

## Optional Longer Demo

After the short GIF exists, record a 2-minute walkthrough that compares:

- Codex Goal: thread-scoped objective and completion contract
- Relay: GitHub-ready PR handoff, release gates, and minimal repo evidence

This longer demo is useful for product education, but it should not block closing the first demo issue.
