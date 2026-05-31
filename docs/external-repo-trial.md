# External Repo Trial

Use this when a maintainer wants to try Relay on a real pull request without installing the Codex App plugin or committing `.relay/` files.

The goal is not adoption yet. The goal is one outside reviewer outcome:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`

And one AI review fit answer:

- `in_addition`
- `before_review`
- `instead`
- `not_needed`
- `unsure`

## Fast Path

1. Copy [examples/github-actions/relay-external-trial.yml](../examples/github-actions/relay-external-trial.yml) into the target repository as:

   ```text
   .github/workflows/relay-external-trial.yml
   ```

2. Open or update a pull request in that repository.
3. Let the `Relay External Trial` workflow run.
4. Download the `relay-validation-bundle` artifact.
5. Compare `.relay/validation-brief.md` or `.relay/pr-comment.md` with the normal PR summary.
6. File feedback through the [Round 1 Relay feedback form](https://github.com/Ryan-Guo123/relay-codex/issues/new?template=round1-relay-feedback.yml).

## What The Workflow Does

The workflow:

- checks out the target repository
- downloads `relay_runtime.py` from the `v0.1.13` release tag
- runs `validation-brief --base-ref origin/<base-branch>`
- writes a review-readiness summary to the GitHub Actions job summary
- uploads a `relay-validation-bundle` artifact

It does not:

- post comments
- request reviews
- block merges
- send repository contents to a Relay server
- require a Relay API key
- require installing the Codex App plugin

## Why It Downloads From A Tag

The example pins the runtime to:

```text
https://raw.githubusercontent.com/Ryan-Guo123/relay-codex/v0.1.13/plugins/relay-codex/scripts/relay_runtime.py
```

Pinning to a tag is more reviewable than running from `main`. Maintainers should still inspect the workflow and runtime before enabling it on sensitive repositories.

## What To Ask The Reviewer

Ask one maintainer or frequent reviewer:

```text
Could you compare the Relay validation bundle with the normal PR summary?

Please answer two things:

1. Outcome: reused, edited_heavily, ignored, or confusing.
2. AI review fit: in_addition, before_review, instead, not_needed, or unsure compared with Copilot code review, CodeRabbit, Graphite, Qodo, PR-Agent, or another AI review tool you use.

Negative feedback is useful. If an existing review tool already solves this job, mark Relay not_needed.
```

## What Counts As Evidence

Count the trial only if:

- the target repository is not `Ryan-Guo123/relay-codex`
- the workflow ran on a real pull request or review task
- the reviewer saw the generated artifact
- the reviewer compared it with a normal PR summary
- the result is recorded in a public feedback issue or linked public comment

Do not count:

- copying the workflow without running it
- this repository running its own Review Readiness workflow
- a private compliment without one of the required outcomes
- a star without a linked trial

## Cleanup

If the target repository does not want to keep Relay:

1. Delete `.github/workflows/relay-external-trial.yml`.
2. Do not commit `.relay/` artifacts.
3. Keep only the linked feedback issue as the evidence record.

## Product Decision

If the first external repo trial returns:

| Result | Decision |
| --- | --- |
| `reused` or `edited_heavily` | Test one more external PR before building new features. |
| `ignored` or `confusing` | Simplify the generated artifact before more outreach. |
| `not_needed` versus AI review tools | Shrink Relay to a template/schema or stop the product direction. |
