# Relay Validation Plan

Relay is in late Discover / early Define. The next milestone is not a bigger feature set. It is proof that a narrow Codex App-native GitHub handoff adapter is useful enough for real maintainers.

## Core Hypothesis

Relay is useful when a maintainer uses Codex heavily enough that work spans threads, branches, pull requests, releases, or scheduled follow-ups.

The value is not "run agents better" or "decide whether Codex should continue." Codex Goals already own that loop. The value is:

> Every long-running Codex Goal/run can become a GitHub-ready maintainer handoff.

That handoff should make it easier to review, comment on, resume, or release the work without reconstructing the full thread.

## What Must Be Proven

### 1. The handoff is faster than reconstructing context

Question:

> Can a maintainer understand what happened in under two minutes without reading the full Codex thread?

Evidence:

- `.relay/state.md` shows a current verdict.
- `.relay/handoff.md` summarizes progress, risk, verification, and next action.
- `.relay/pr-comment.md` turns the handoff into a GitHub-ready review note.
- `.relay/reviewer-pack.md` turns the PR handoff into an outside-review request with a rubric.
- A reviewer can explain the next action after reading only the README demo and generated Relay files.

Pass condition:

- Three real or fixture-backed runs produce handoffs that are understandable without thread context.

### 2. The handoff prevents bad review or blind follow-up

Question:

> Does Relay make it obvious when a PR needs human review instead of another generic agent pass?

Evidence:

- A stuck fixture or run flips to `needs_review`.
- The recovery queue names the smallest next investigation.
- The handoff says what a human should review before another agent pass.

Pass condition:

- One demo shows `needs_review -> recovery handoff -> PR comment draft` using real runtime output.

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

### 5. Outside reviewers actually reuse the handoff

Question:

> Does someone outside the current Codex/build thread reuse the generated PR handoff?

Evidence:

- An outside maintainer, contributor, teammate, or evaluator compares `.relay/pr-comment.md` with a normal Codex/manual summary.
- The reviewer records whether the output was reused, edited heavily, ignored, or confusing.
- `.relay/reviewer-pack.md` packages the handoff, reviewer prompt, comparison placeholder, scoring rubric, and outcome choices.
- The feedback is captured through the `Relay handoff feedback` issue template.

Pass condition:

- At least one outside reviewer can identify changed files, verification, review focus, and next action without reading the full Codex thread.
- The reviewer says the Relay handoff saved review or summary reconstruction time.

## Validation Workflows

### Workflow A: PR Handoff

Use when:

- Codex completes a small feature, fix, or docs task.

Path:

```text
issue/task -> Codex Goal/run -> relay handoff -> PR body/review checklist
```

Artifacts:

- `.relay/state.md`
- `.relay/events.jsonl`
- `.relay/handoff.md`
- `.relay/pr-comment.md`
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

- Did Relay make human review feel like progress rather than failure?

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

### Workflow D: External Reviewer Feedback

Use when:

- A real PR or repo task has a generated `.relay/pr-comment.md`.
- Someone outside the active build thread can review it.

Path:

```text
real PR/task -> relay pr-comment -> outside reviewer comparison -> feedback issue -> product decision
```

Artifacts:

- `.relay/pr-comment.md`
- `.relay/reviewer-pack.md`
- normal Codex/manual summary for comparison
- `Relay handoff feedback` issue
- follow-up decision: keep, simplify, rename, or remove

Measure:

- Did the outside reviewer reuse the artifact or find it clearer than reconstructing the Codex thread?

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
- outside reviewers mark the handoff as ignored or confusing after real PR trials
- users ask for a board, runtime, or memory system more than they ask for handoff evidence
- Codex native features expose repo-local evidence and release handoff directly
- Maestro/Kage/Recall-style tools prove the same handoff use case with stronger adoption

## Current Stage Gate

Relay can move from Define to Develop when:

- README explains the wedge clearly.
- A runtime-generated demo proves the handoff path.
- Open issues map to the three validation workflows above.
- The next feature PR improves GitHub handoff output, not the product surface area in general.
