# Relay Validation Plan

Relay is in late Discover / early Define. The next milestone is not a bigger feature set. It is proof that the narrow repo-local handoff layer is useful enough for real maintainers.

## Core Hypothesis

Relay is useful when a maintainer uses Codex heavily enough that work spans threads, branches, pull requests, releases, or scheduled follow-ups.

The value is not "run agents better." The value is:

> Every long-running Codex run leaves behind a maintainer-readable handoff inside the repository.

That handoff should make it easier to decide whether the repo should continue, recover, review, or release.

## What Must Be Proven

### 1. The handoff is faster than reconstructing context

Question:

> Can a maintainer understand what happened in under two minutes without reading the full Codex thread?

Evidence:

- `.relay/state.md` shows a current verdict.
- `.relay/handoff.md` summarizes progress, risk, verification, and next action.
- A reviewer can explain the next action after reading only the README demo and generated Relay files.

Pass condition:

- Three real or fixture-backed runs produce handoffs that are understandable without thread context.

### 2. The verdict prevents bad continuation

Question:

> Does Relay stop Codex from blindly continuing when the repo is actually stuck or drifting?

Evidence:

- A stuck fixture flips to `needs_review`.
- The recovery queue names the smallest next investigation.
- The handoff says what a human should review before more autonomous work.

Pass condition:

- One demo shows `continue -> needs_review -> recovery handoff` using real runtime output.

### 3. The release gate makes shipping safer

Question:

> Does the release checklist reduce forgotten release steps?

Evidence:

- `.relay/release-checklist.md` includes verification commands, clean-tree check, release notes, tags, and human approval gates.
- The release flow distinguishes meaningful patch releases from activity-only releases.

Pass condition:

- One patch release uses the checklist without rebuilding release steps from memory.

### 4. The positioning is understandable

Question:

> Can a first-time visitor understand why Relay is not Codex Goals, Paperclip, vibe-kanban, agentmemory, or a skills pack?

Evidence:

- README explains the crowded market in plain language.
- The demo shows repo-local evidence rather than a dashboard or runtime.
- Product strategy names the non-goals.

Pass condition:

- A maintainer can restate Relay as "handoff evidence after agent work" instead of "another agent manager."

## Validation Workflows

### Workflow A: PR Handoff

Use when:

- Codex completes a small feature, fix, or docs task.

Path:

```text
issue/task -> Codex run -> relay handoff -> PR body/review checklist
```

Artifacts:

- `.relay/state.md`
- `.relay/events.jsonl`
- `.relay/handoff.md`
- PR description or comment drafted from the handoff

Measure:

- Could a reviewer identify what changed, what was tested, and what to review?

### Workflow B: Stuck Recovery

Use when:

- Tests fail repeatedly.
- Codex repeats inspection without progress.
- The next action becomes unclear.

Path:

```text
events -> needs_review verdict -> recovery queue -> human review point
```

Artifacts:

- stuck fixture or real repo event log
- `.relay/queue.md`
- `.relay/handoff.md`
- short GIF or narrated walkthrough

Measure:

- Did Relay make stopping feel like progress rather than failure?

### Workflow C: Release Handoff

Use when:

- A meaningful patch release is ready.

Path:

```text
merged PRs -> relay release checklist -> tag -> GitHub release -> post-release check
```

Artifacts:

- `.relay/release-checklist.md`
- GitHub release notes
- closed issue / merged PR links

Measure:

- Did the checklist catch version, test, notes, tag, and human approval steps?

## Develop Candidates

Only build these after the workflows above are clear.

### Candidate 1: PR Comment Draft

Generate a GitHub-ready PR comment from `.relay/handoff.md`.

Why:

- Keeps Relay inside the maintainer surface where review already happens.
- Avoids building a dashboard.

Definition of done:

- Command renders Markdown that can be pasted into a PR comment.
- Output includes verdict, summary, verification, risks, and next action.
- No network write happens without explicit human approval.

### Candidate 2: Stuck Recovery Demo

Create a higher-quality narrated walkthrough for the `needs_review` path.

Why:

- Current demo proves the handoff/release path.
- The strongest emotional value may be stopping blind continuation.

Definition of done:

- Demo uses real runtime output.
- It shows the verdict changing because of repeated failure or test-only churn.
- README links it below the first demo GIF.

### Candidate 3: Relay Artifact Schema

Document the minimal shape of `.relay/` files.

Why:

- Other agents, memory tools, or boards can index Relay artifacts later.
- The protocol becomes more credible without adding a server.

Definition of done:

- `docs/relay-protocol.md` defines required files and fields.
- Tests cover the generated file names and headings.
- Strategy remains human-readable first.

## Anti-Validation

Relay should shrink or pivot if:

- maintainers still prefer plain GitHub issue checklists
- the demo reads as another generic agent-productivity tool
- `.relay/` files feel like stale documentation instead of useful state
- users ask for a board, runtime, or memory system more than they ask for handoff evidence
- Codex native features expose repo-local evidence and release handoff directly

## Current Stage Gate

Relay can move from Define to Develop when:

- README explains the wedge clearly.
- A runtime-generated demo proves the handoff path.
- Open issues map to the three validation workflows above.
- The next feature PR improves one of those workflows, not the product surface area in general.
