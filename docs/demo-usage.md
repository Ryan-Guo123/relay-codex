# Demo Usage Example

This example shows the narrow job Relay should do now that Codex has its own goal and continuation features: turn long-running Codex work into GitHub-ready maintainer handoff artifacts.

## Scenario

A maintainer opens a pull request that has been worked on for a while. Codex has already made several attempts, tests have been re-run multiple times, and the thread is starting to lose the original decision context.

Relay is useful when the question is no longer "can Codex keep going?" but:

- what is the current repo-local state?
- what can be posted into the PR?
- what should a maintainer review before merge or another agent pass?
- what evidence should survive after the thread ends?

## Step 1: enable Relay

From the target repository, run the Relay enable flow:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py enable --json
```

Relay creates:

```text
.relay/
  mission.md
  state.md
  queue.md
  guardrails.md
  automations.md
  events.jsonl
```

Expected result:

- `mission.md` captures the inferred project context
- `queue.md` names the smallest next tasks
- `guardrails.md` defines when to pause, escalate, or recover
- `state.md` records the current verdict

## Step 2: inspect before continuing

Before asking Codex to do another broad pass, inspect the repo-local state:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py inspect --json
```

If recent work is healthy, the verdict should stay:

```json
{
  "verdict": "continue",
  "reasons": []
}
```

If the project is drifting, Relay should make that visible:

```json
{
  "verdict": "needs_review",
  "reasons": [
    "Repeated failure-like events detected.",
    "Recent events look test-only; confirm whether product work is actually moving."
  ]
}
```

## Step 3: recover a stuck queue

When the verdict is `needs_review`, run recovery instead of asking Codex to blindly continue:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py recover --json
```

Relay rewrites `.relay/queue.md` into a small recovery checklist:

```text
## Recovery Tasks

- [ ] Restate the last successful change before making more edits.
- [ ] Reduce the next step to one investigation or one implementation move.
- [ ] If credentials, product intent, or external systems are missing, stop and ask for that input directly.
- [ ] Do not keep running tests or formatting loops without a concrete hypothesis.
```

This is the handoff point. A maintainer can inspect the queue and decide what to put in the PR note before asking for another agent pass.

## Step 4: generate the PR handoff

Generate a maintainer-ready handoff before continuing or posting a PR update:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py handoff --json
```

Relay writes:

```text
.relay/handoff.md
```

The handoff includes:

- current verdict
- last successful signal
- current blocker signals
- recent Relay events
- queue snapshot
- recommended next action
- review focus
- safe handoff rules

Expected excerpt when a repo is stuck:

```markdown
# Relay Handoff

- Verdict: `needs_review`

## Last Successful Signal

- No substantive Relay event recorded yet.

## Current Signals

- Relay saw repeated failure signals in recent events.

## Recommended Next Action

Switch to recovery: restate the last success, isolate one failing signal, and stop broad retries.
```

Expected excerpt when a repo is safe to continue:

```markdown
# Relay Handoff

- Verdict: `continue`

## Recommended Next Action

Pick one unchecked item from `.relay/queue.md` and continue with the smallest meaningful change.
```

## Example PR triage workflow

Use this flow on a real pull request:

1. Read the PR goal and latest failing or unresolved signal.
2. Run `inspect` and read `.relay/state.md`.
3. If the verdict is `continue`, pick exactly one item from `.relay/queue.md`.
4. If the verdict is `needs_review`, run `recover` and write a short PR comment or internal note with:
   - last successful change
   - likely stuck point
   - smallest next investigation
   - human decision needed, if any
5. Run `handoff` and use `.relay/handoff.md` as the maintainer review surface.
6. Do not install recurring automations until the queue has a clear owner and stop condition.

## What this demo proves

Relay is not trying to replace Codex goals. It adds a repo-local handoff surface around Codex work so maintainers can see:

- what the PR/release note should say
- what review focus should be preserved
- what state another person or agent can pick up later

## Release handoff

When the work is ready to ship, generate a release checklist instead of rebuilding release steps from memory:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py release --json
```

Relay writes:

```text
.relay/release-checklist.md
```

The checklist covers:

- release scope
- verification commands
- clean working tree check
- version and tag steps
- release notes
- human approval gates
- post-release checks

If the current verdict is `needs_human` or `needs_review`, the checklist tells the maintainer not to release until that state is reviewed.
