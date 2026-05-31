# Stuck Recovery Walkthrough

This walkthrough validates Workflow B from [validation-plan.md](validation-plan.md):

```text
events -> needs_review verdict -> recovery queue -> human review point
```

It uses real Relay runtime output from a temporary copy of `tests/fixtures/in-progress-repo`. The point is not to simulate a dramatic failure. The point is to show that repeated test-only churn becomes a review handoff instead of another blind agent pass.

## Setup

Create a temporary target repo:

```bash
cp -R tests/fixtures/in-progress-repo /private/tmp/relay-stuck-walkthrough-20260531
python3 plugins/relay-codex/scripts/relay_runtime.py enable --root /private/tmp/relay-stuck-walkthrough-20260531 --json
```

Initial output:

```json
{
  "inspection": {
    "verdict": "continue",
    "reasons": [
      "Recent activity still supports continuing with the next queued task."
    ],
    "event_count": 0,
    "open_tasks": 4
  }
}
```

Relay starts in `continue` because the queue has work and no churn signal has been recorded.

## Trigger The Stuck Signal

Record the same failing test event three times:

```bash
CODEX_HOOK_PAYLOAD='{"tool_name":"Bash","tool_input":{"command":"npm test failed with error on checkout handoff assertion"}}' \
python3 plugins/relay-codex/scripts/relay_runtime.py hook-posttooluse --root /private/tmp/relay-stuck-walkthrough-20260531 --json
```

After the third event, Relay flips the verdict:

```json
{
  "updated": true,
  "event": {
    "kind": "bash",
    "summary": "npm test failed with error on checkout handoff assertion"
  },
  "verdict": "needs_review"
}
```

This is the key behavior: repeated failed test activity is no longer treated as "keep going." It becomes a maintainer review point.

## Generate Recovery Queue

Run recovery:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py recover --root /private/tmp/relay-stuck-walkthrough-20260531 --json
```

Relay writes `.relay/queue.md`:

```markdown
# Relay Queue

- Current verdict: `needs_review`

## Recovery Tasks

- [ ] Restate the last successful change before making more edits.
- [ ] Reduce the next step to one investigation or one implementation move.
- [ ] If credentials, product intent, or external systems are missing, stop and ask for that input directly.
- [ ] Do not keep running tests or formatting loops without a concrete hypothesis.

## Recovery Trigger

- Relay detected repeated test-only churn without enough evidence of forward progress.
```

## Generate Handoff

Run handoff:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py handoff --root /private/tmp/relay-stuck-walkthrough-20260531 --json
```

Relay writes `.relay/handoff.md`:

```markdown
# Relay Handoff

- Verdict: `needs_review`

## Current Signals

- Relay detected repeated test-only churn without enough evidence of forward progress.

## Recent Events

- 2026-05-31T02:12:43+00:00: `bash` - npm test failed with error on checkout handoff assertion
- 2026-05-31T02:12:52+00:00: `bash` - npm test failed with error on checkout handoff assertion
- 2026-05-31T02:12:59+00:00: `bash` - npm test failed with error on checkout handoff assertion
- 2026-05-31T02:13:08+00:00: `recovery_brief` - Relay generated a recovery queue because recent signals suggest the project needs review.

## Recommended Next Action

Switch to recovery: restate the last success, isolate one failing signal, and stop broad retries.

## Review Focus

Look for repeated failures, test-only churn, or repeated conclusions before approving more work.
```

## Why This Matters

This is the emotional value Relay can still own without duplicating Codex Goals:

- Codex Goals can keep the thread objective alive.
- Relay can package the repo evidence when work starts looping.
- The maintainer gets a review handoff instead of another vague "continue?" moment.

The walkthrough makes "stop and review" feel like progress because it produces a smaller recovery queue and a PR-ready handoff surface.

## Result

This satisfies issue #17's first-pass bar:

- the walkthrough uses real runtime output
- the path shows `continue -> needs_review -> recovery handoff`
- the recovery handoff identifies the smallest next review point
- the README links to this document
