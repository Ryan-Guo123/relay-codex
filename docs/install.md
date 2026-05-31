# Install Relay for Codex

Relay is currently distributed from this repository as a local Codex App plugin bundle. The install path should leave you with a visible plugin, a generated `.relay/` folder in a target repo, and handoff artifacts you can reuse in PR or release workflows.

## Fast path

1. Clone this repository.

   ```bash
   git clone https://github.com/Ryan-Guo123/relay-codex.git
   cd relay-codex
   ```

2. Confirm the local plugin marketplace entry exists.

   ```bash
   test -f .agents/plugins/marketplace.json
   test -f plugins/relay-codex/.codex-plugin/plugin.json
   ```

3. Open this repository in Codex App.

4. Install `Relay for Codex` from the local plugin marketplace entry.

5. Open the repository you want Relay to manage.

6. Run:

   ```text
   Enable Relay in this repo
   ```

7. Inspect the generated state.

   ```text
   Check whether Codex is stuck and what to do next
   ```

## Expected result

After enabling Relay in a target repository, you should see:

```text
.relay/
  mission.md
  state.md
  queue.md
  guardrails.md
  automations.md
  events.jsonl
```

`state.md` should contain a verdict:

- `continue`: the next action is clear
- `paused`: there is no immediate work to continue
- `needs_human`: missing input blocks safe progress
- `needs_review`: Relay sees churn, repetition, or drift

`queue.md` should contain the next concrete tasks or recovery tasks. `events.jsonl` may be empty until Codex tools run in the repo.

## Smoke test without installing

You can verify the runtime directly from this repository:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py enable --root /path/to/target-repo --json
python3 plugins/relay-codex/scripts/relay_runtime.py inspect --root /path/to/target-repo --json
python3 plugins/relay-codex/scripts/relay_runtime.py review-readiness --root /path/to/target-repo --json
python3 plugins/relay-codex/scripts/relay_runtime.py pr-comment --root /path/to/target-repo --json
python3 plugins/relay-codex/scripts/relay_runtime.py reviewer-pack --root /path/to/target-repo --json
```

For a clean PR checkout or GitHub Actions job, compare committed changes against a base ref:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py review-readiness --root /path/to/target-repo --base-ref origin/main --json
python3 plugins/relay-codex/scripts/relay_runtime.py pr-comment --root /path/to/target-repo --base-ref origin/main --json
```

This repository also ships a `Review Readiness` GitHub Actions workflow. On pull requests it generates `.relay/review-readiness.md` and `relay-review-readiness.json`, then uploads both as the `relay-review-readiness` artifact.

Use a disposable test repository if you do not want `.relay/` files in a real project yet.

## Common problems

### The plugin does not appear in Codex App

Check that this repository is open as the active workspace and that `.agents/plugins/marketplace.json` still points at `./plugins/relay-codex`.

### `Enable Relay in this repo` creates no `.relay/` folder

Make sure you are running the skill in the target repository, not in a read-only directory or a browser-only context. Relay writes `.relay/` into the current workspace root.

### The verdict says `needs_human`

Open `.relay/mission.md` and add the real product goal or missing decision. Relay is designed to stop when continuing would require guessing.

### The verdict says `needs_review`

Run the recovery flow before doing more work:

```text
Recover this stuck project with Relay
```

Then read `.relay/queue.md` and pick one recovery task.

### You do not want `.relay/` committed

Relay state is repo-local so it can be inspected and handed off. In private or sensitive repositories, review `.relay/` before committing it, or add `.relay/` to that repository's `.gitignore`.

## Where to go next

- [Demo usage example](demo-usage.md)
- [Relay artifact protocol](relay-protocol.md)
- [Security policy and threat model](../SECURITY.md)
- [Launch playbook](launch-playbook.md)
