# Relay for Codex Validation And Launch Playbook

This document is for maintainers. The goal is not "announce the repo." The goal is to find out whether strangers who review AI-generated PRs would reuse Relay's handoff artifacts.

## Positioning

Do not pitch Relay as:

- another prompt pack
- another agent framework
- another CLI loop
- a replacement for Codex Goals
- an agent board
- a repo memory engine

Pitch it as:

- a Codex App-native GitHub handoff adapter
- a way to turn a finished Codex run into review-readiness, PR comment, reviewer-pack, and release-checklist artifacts
- a small repo-local record that helps a maintainer see changed files, verification, review focus, and next action

## The best launch angle

Lead with a real review moment:

- Before: an agent PR lands with a vague summary and a diff that is expensive to scan.
- After: Relay shows changed-file scope, sensitive paths, CODEOWNERS routing, verification evidence, and a pasteable PR handoff.

That story is much stronger than "here is a plugin with several skills."

Do not claim that story is proven until the [validation ledger](validation-ledger.md) records outside reviewer outcomes.

## Assets to prepare before promotion

- a 20 to 40 second screen recording of `review-readiness` and `pr-comment`
- one clean screenshot of `.relay/` files in a real repo
- one real PR where Review Readiness ran in GitHub Actions
- one reviewer-pack example that can be judged without installing Relay
- one generated `.relay/validation-brief.md` for the real reviewer ask
- one external repo trial workflow that can run without installing the Codex App plugin
- one public validation issue asking for `reused`, `edited_heavily`, `ignored`, or `confusing`

## Best channels

- X / Twitter
  - short clip plus a single before/after thesis
- GitHub README
  - needs to explain the problem in the first screen
- Hacker News
  - only when you have a real demo and a crisp explanation
- Reddit
  - target communities discussing AI PR review fatigue, only where self-promotion is allowed
- short YouTube demo
  - useful once the setup story is cleaner
- GitHub issues/discussions
  - strongest when the ask is to review a concrete artifact, not to star the repo

## Star conversion checklist

- the repo description says what it does in one line
- the README hero explains the problem before the implementation
- the first screen shows a visual, not only text
- badges make the repo look maintained
- there is a credible test story
- there is a clear “why this is different” section
- there is a real demo, not only architecture
- there is a public evidence ledger showing what is and is not validated
- there is a public experiment protocol with success, failure, and stop rules
- the reviewer ask is small enough to complete in 10 minutes

## First 14 days

### Day 1 to 3

- keep README aligned with the handoff-adapter wedge
- make sure Actions and Review Readiness are green
- record the baseline stars, forks, open validation issues, and outside-review outcomes

### Day 4 to 7

- send one targeted outside-review ask
- ask for one outcome, not general praise
- log every response in [validation-ledger.md](validation-ledger.md)

### Day 8 to 14

- tighten install steps
- turn repeated feedback into README or runtime improvements
- ship one visible improvement only if it helps the review moment
- do not publish a patch release for docs-only validation work

## What usually gets ignored

- distribution matters as much as implementation
- examples matter more than architecture diagrams
- one strong use case beats five vague ones
- "GitHub-ready handoff after Codex work" is clearer than broad agent orchestration
- external validation is more valuable than more internal polish
