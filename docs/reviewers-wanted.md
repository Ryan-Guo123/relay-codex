# Reviewers Wanted

Relay needs outside maintainer feedback.

The product is only useful if someone who did not run the Codex thread can still understand the generated handoff.

If you are sharing this request with another maintainer, use the drafts in [outreach-copy.md](outreach-copy.md).
If you want to review the format before installing anything, start with [reviewer-pack-example.md](reviewer-pack-example.md).

## Who This Is For

You are a good reviewer if you:

- maintain a GitHub repo
- review AI-generated PRs
- use Codex, Claude Code, Cursor, or another coding agent
- have ever had to reconstruct what an agent did from a long thread

## 10-Minute Review

1. Skim [round1-reviewer-request.md](round1-reviewer-request.md), [reviewer-pack-example.md](reviewer-pack-example.md), download the `relay-validation-bundle` artifact from a Relay PR, or pick a real PR or maintenance task.
2. Generate a Relay reviewer pack:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py reviewer-pack --json
```

Or generate the full validation ask:

```bash
python3 plugins/relay-codex/scripts/relay_runtime.py validation-brief --json
```

3. Open `.relay/reviewer-pack.md` or `.relay/validation-brief.md`.
4. Add or link a normal Codex/manual summary in the `Compare Against` section.
5. Compare the two without reading the full agent thread.
6. Open the [Round 1 feedback form](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml) or a `Relay handoff feedback` issue.

## What To Judge

Please be direct. Relay needs negative signal as much as positive signal.

Choose one outcome:

- `reused`: you would reuse most of the generated handoff.
- `edited_heavily`: the structure helped, but the content needed major edits.
- `ignored`: the generated handoff did not help.
- `confusing`: you could not tell what to do with it.

Score these from 1 to 5:

- changed files are clear
- verification is reviewable
- review focus points to the right risk
- next action is directly actionable
- GitHub fit is pasteable

## What Happens With Feedback

Relay should keep `pr-comment` only if outside reviewers say it saves review or summary reconstruction time.

If reviewers ignore it, find it confusing, or only reuse one section, Relay should simplify, rename, or remove the artifact instead of expanding the product.

That is the point of this validation: the product direction should be decided by real maintainer review, not internal enthusiasm.

Each feedback issue is triaged with one public outcome label and copied into [validation-ledger.md](validation-ledger.md). The triage rules live in [feedback-triage.md](feedback-triage.md).
