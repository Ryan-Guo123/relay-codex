# Outreach Copy

Use these short drafts when asking for outside maintainer feedback. Keep the ask small and honest: Relay is not proven until people outside the build thread reuse or reject its handoff.

For the current Round 1 validation ask, use [round1-outreach-message.md](round1-outreach-message.md).

## One-Line Positioning

Relay for Codex turns long-running Codex work into GitHub-ready maintainer handoffs: what changed, what was verified, what still needs review, and what should happen next.

## Short Ask

```text
I am looking for maintainers who review AI-generated PRs.

Relay for Codex generates a `.relay/reviewer-pack.md` from a branch so someone who did not run the Codex thread can judge the handoff.

The test takes about 10 minutes: compare the Relay handoff with a normal Codex/manual summary and mark it as reused, edited heavily, ignored, or confusing.

Repo: https://github.com/Ryan-Guo123/relay-codex
60-second quick verdict: https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/reviewer-quick-verdict.md
Reviewer guide: https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/reviewers-wanted.md
```

## GitHub Issue Comment

```text
I am testing whether Relay handoffs are useful outside my own workflow.

If you review AI-generated PRs, could you try the 60-second quick verdict or the 10-minute reviewer path?

1. Quick path: compare the normal PR summary with the Relay handoff excerpt.
2. Full path: generate `.relay/reviewer-pack.md` and compare it with a normal Codex/manual summary.
3. Open a `Relay handoff feedback` issue with one outcome: `reused`, `edited_heavily`, `ignored`, or `confusing`.

Negative feedback is useful. If the artifact is too long, too generic, or not better than a normal summary, that should shape the product.
```

## Reddit / Forum Draft

```text
I am building a small Codex App-native tool called Relay for Codex.

The wedge is intentionally narrow: after a Codex run touches a repo, Relay generates GitHub-ready maintainer handoffs instead of trying to replace Codex Goals, kanban boards, or memory tools.

I am looking for maintainers who review AI-generated PRs. The validation question is simple:

Would you reuse the generated handoff, edit it heavily, ignore it, or find it confusing?

The reviewer path is here:
https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/reviewers-wanted.md

The 60-second no-install version is here:
https://github.com/Ryan-Guo123/relay-codex/blob/main/docs/reviewer-quick-verdict.md

Blunt negative feedback is welcome. If this is just another markdown artifact nobody wants, I would rather learn that early.
```

## Maintainer DM Draft

```text
Hey, quick ask. I am validating a small open-source Codex workflow tool.

It generates a reviewer pack from a branch so someone who did not run the AI coding thread can see what changed, what was verified, what needs review, and what the next action is.

Would you be open to spending 60 seconds on the no-install sample, or 10 minutes comparing one generated handoff against a normal Codex/manual PR summary?

The useful answers are blunt: reused, edited heavily, ignored, or confusing.
```

## What Not To Claim

- Do not claim Relay is a replacement for Codex Goals.
- Do not claim external validation is complete before an outside reviewer responds.
- Do not claim the artifact saves time unless a reviewer says so.
- Do not pitch Relay as an agent runtime, kanban board, or memory system.
- Do not ask for praise; ask for a decision.
