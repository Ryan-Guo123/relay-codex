# Validation Ledger

Relay should not treat documentation, releases, or internal PRs as proof of market demand. This ledger tracks the public validation work that can turn the product bet into evidence.

Snapshot date: 2026-05-31.

## Baseline

| Metric | Current | Evidence |
| --- | ---: | --- |
| GitHub stars | 1 | `gh repo view Ryan-Guo123/relay-codex` on 2026-05-31 |
| Forks | 0 | `gh repo view Ryan-Guo123/relay-codex` on 2026-05-31 |
| Open validation issues | 1 | [#24 Test Relay handoff with an outside maintainer](https://github.com/Ryan-Guo123/relay-codex/issues/24) |
| Outside reviewer outcomes | 0 | No `reused`, `edited_heavily`, `ignored`, or `confusing` feedback yet |
| External repo trials | 0 | No linked outside PR, issue, workflow artifact, or commit yet |
| Money signals | 0 | No sponsor, donation, paid setup request, or hosted-feature request yet |

## What Counts As Evidence

Strong evidence:

- An outside maintainer files a Relay handoff feedback issue.
- An outside repository runs `review-readiness` or `pr-comment` on a real PR.
- A reviewer says the artifact was `reused` or `edited_heavily`.
- A reviewer says the artifact was `ignored` or `confusing` and explains why.
- A maintainer asks for setup help, sponsorship, or hosted/private-team features after using Relay.

Weak evidence:

- Stars without known usage.
- Internal PRs in this repository.
- AI-generated praise.
- Synthetic demo reactions without a real review task.
- Traffic or impressions without a reviewer outcome.

## Round 1 Validation Plan

Goal:

> Get one outside maintainer or frequent PR reviewer to compare a Relay handoff with a normal Codex/manual summary and record a blunt outcome.

Timebox:

- 7 days from the first public ask.
- Stop early if one reviewer files useful feedback.

Minimum ask:

- 1 public issue comment, discussion reply, or maintainer DM using [outreach-copy.md](outreach-copy.md).
- 1 linked reviewer artifact: [reviewer-pack-example.md](reviewer-pack-example.md) or a real PR artifact.
- 1 follow-up asking for one of: `reused`, `edited_heavily`, `ignored`, `confusing`.

Do not ask for:

- stars
- sponsorship
- praise
- broad product feedback before the reviewer sees the artifact

## Candidate Reviewer Segments

| Segment | Why It Fits | First Ask |
| --- | --- | --- |
| Maintainers reviewing AI-generated PRs | They feel the review burden directly. | "Would this handoff help you decide whether to review, split, or reject an agent PR?" |
| Solo builders using Codex/Claude/Cursor | They often need future-self handoff and PR notes. | "Would you reuse this summary in your own PR or release note?" |
| Open-source maintainers with contribution queues | They care about reviewer time and trust signals. | "Does this reduce context reconstruction, or is it noise?" |
| People discussing AI PR review fatigue | They have already named the pain. | "Is a review-readiness gate useful, or would you prefer behavior/e2e proof?" |
| Agent workflow tool builders | They may integrate artifacts if the schema is useful. | "Would the JSON schema be enough to consume Relay output?" |

## Public Pain Threads To Reference

These links are evidence of the problem space, not proof that Relay solves it.

| Source | Pain Signal | Relay Hypothesis |
| --- | --- | --- |
| [GitHub Blog: Agent pull requests are everywhere](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/) | Agent PR review needs scope, CI, risk, and evidence checks. | `review-readiness` can pre-package the first review scan. |
| [Reddit: Is AI coding making pull requests harder to review?](https://www.reddit.com/r/github/comments/1rofktt/is_ai_coding_making_pull_requests_harder_to_review/) | Big AI PRs bury migrations, auth, billing, APIs, and config. | Relay should highlight sensitive paths and review routing before prose. |
| [Reddit: AI-generated PRs are faster to write but slower to review](https://www.reddit.com/r/ClaudeCode/comments/1roy3o0/aigenerated_prs_are_faster_to_write_but_slower_to/) | Reviewers worry about subtle behavior drift in clean-looking code. | Relay must expose verification gaps instead of claiming correctness. |
| [Reddit: First time reviewing PRs and finding it difficult](https://www.reddit.com/r/ExperiencedDevs/comments/1tbqunh/first_time_in_a_position_reviewing_pull_requests/) | Large likely-AI PRs overwhelm reviewers who lack a repeatable process. | Relay may be useful if the generated handoff reduces the first two minutes of confusion. |
| [arXiv 2601.04886](https://arxiv.org/abs/2601.04886) | AI PR descriptions can diverge from actual code changes. | Relay should compare repo state and changed files instead of trusting agent self-report. |

## Outreach Queue

| Date | Channel / Target | Artifact Shared | Status | Outcome | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-05-31 | GitHub issue #24 | `docs/reviewer-pack-example.md` and Review Readiness artifact path | Open | Pending | Keep open until an outside reviewer records one of the required outcomes. |
| TBD | Maintainer who reviews AI-generated PRs | `docs/reviewers-wanted.md` | Not contacted | Pending | Ask for a 10-minute comparison, not a star. |
| TBD | Community thread about AI PR review fatigue | `docs/reviewer-pack-example.md` | Not contacted | Pending | Reply only where self-promotion is allowed and the thread asks for tools/workflows. |
| TBD | Agent workflow tool builder | `docs/review-readiness.schema.json` | Not contacted | Pending | Ask whether the JSON payload is useful for integration. |
| TBD | External public repo trial | `review-readiness --base-ref origin/main --json` | Not started | Pending | Strongest evidence if the maintainer links a real PR artifact. |

## Decision Log

| Date | Decision | Evidence | Next Action |
| --- | --- | --- | --- |
| 2026-05-31 | Do not claim product-market confidence. | Relay has 1 star, 0 forks, no outside reviewer outcome, and no external repo trial. | Prioritize one outside reviewer before new feature expansion. |
| 2026-05-31 | Do not release docs-only validation work. | No runtime behavior changed. | Release only when runtime/user-facing plugin behavior changes. |

## Stop Rules

Pause feature work if:

- 3 outside reviewers mark the artifact `ignored` or `confusing`.
- 20 targeted asks produce no reviewer trial.
- Reviewers say they need behavior/e2e proof more than handoff prose.
- Reviewers only want a board, memory engine, or autonomous runtime.

Continue only if:

- At least one reviewer can identify changed files, verification, review focus, and next action without reading the Codex thread.
- The reviewer says the artifact is easier than reconstructing context manually.
- The next feature request improves that review moment, not generic agent management.
