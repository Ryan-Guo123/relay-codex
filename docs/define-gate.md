# Define Gate

Relay is not ready to move into broad buildout or promotion. It is at the Define gate of the Double Diamond: decide whether the narrow GitHub handoff wedge is worth developing further.

Snapshot date: 2026-05-31.

## Current Decision

Continue only as:

> A Codex App-native GitHub handoff adapter that turns a completed Codex Goal/run into maintainer-readable PR, review, and release artifacts.

Do not continue as:

- a Codex Goals replacement
- a general agent runtime
- an agent board
- a memory engine
- an AI PR review bot
- a broad local-first evidence protocol
- a hosted SaaS product

The original broad idea overlaps too much with native Codex Goals, managed-agent runtimes, Paperclip-style control planes, vibe-kanban-style boards, agentmemory-style recall, and AI PR review tools. The remaining wedge is useful only if real maintainers reuse the generated handoff artifact.

## Evidence State

Current external evidence:

| Signal | Current | Decision Meaning |
| --- | ---: | --- |
| GitHub stars | 1 | Existence only, not traction. |
| Forks | 0 | No distribution signal. |
| Targeted asks sent | 3 | Outreach started, not validation. |
| Replies received | 0 | No market response yet. |
| Outside reviewer outcomes | 0 | Product usefulness unproven. |
| External repo trials | 0 | Installation and workflow fit unproven. |
| Money signals | 0 | Revenue forecast stays $0. |

The three public targeted asks are useful because they test the riskiest question: whether Relay is `not_needed` because existing AI PR review tools already cover the job.

## Define Gate Question

Before building more features, answer:

> Does a maintainer who reviews AI-generated PRs want a pre-review handoff artifact before/alongside Copilot, CodeRabbit, Graphite, Qodo, PR-Agent, or another AI review tool?

The answer must come from outside this repository.

## Pass Conditions

Relay may move from Define into Develop only if at least one of these happens:

- 1 outside reviewer files or authorizes feedback on a Relay handoff.
- 1 outside repository runs the external trial workflow on a real PR or issue.
- 1 maintainer explicitly says the artifact is useful `before_review` or `in_addition` to an AI review tool.

Broader confidence still requires the larger gates in [evidence-and-business-case.md](evidence-and-business-case.md).

## Fail Conditions

Pause feature work and change the product shape if:

- 3 targeted asks get no reply after 7 days each.
- 1 reviewer says the artifact is `not_needed` because an existing AI PR review tool already covers it.
- 1 reviewer says the artifact is not better than asking Codex to summarize the thread.
- reviewers ask for a board, memory engine, dashboard, or autonomous runner instead of GitHub handoff artifacts.
- the next useful feature would require a server, billing, or hosted dashboard before external repo trials exist.

Negative evidence is not failure of the research process. It is the point of this gate.

## Next Three Actions

1. Wait for replies on the three public targeted asks already sent.
2. If any reviewer replies, record the outcome before changing the product.
3. If all three asks produce no reply after 7 days, run [no-response-pivot.md](no-response-pivot.md), stop outreach in that segment, and change the artifact or target segment before any new feature work.

Do not ask for stars, sponsorship, or paid setup during this gate.

## Product Shape If The Gate Passes

If the first outside signal is positive, keep the product small:

- runtime-generated `review-readiness`
- runtime-generated `pr-comment`
- runtime-generated `reviewer-pack`
- runtime-generated `release-checklist`
- copy-paste GitHub Actions trial
- public issue templates for blunt feedback

The next runtime work should improve the generated handoff artifact, not add a dashboard.

## Product Shape If The Gate Fails

If outside feedback says Relay is redundant, shrink to one of:

- a tiny GitHub Actions workflow plus schema
- a Codex skill pack that emits PR/release handoff templates
- a research/demo repository documenting the market map
- an archived experiment

Do not keep building a full product after the evidence says the wedge is too small.

## Revenue Rule

Expected revenue remains **$0** until one outside reviewer marks the artifact `reused` or `edited_heavily`, or one outside maintainer asks for setup/support after seeing a real Relay artifact.

The earliest paid hypothesis remains one-repo setup support at `$100-$250`, but it must not be offered before the evidence gate moves.
