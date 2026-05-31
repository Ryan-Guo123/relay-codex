# Security Policy

Relay for Codex is a local workflow layer for Codex App projects. It writes repo-local state, reads repo context, and produces maintainer-facing handoff guidance. It should not become a hidden background agent with broad access.

## Supported versions

Security fixes are accepted for the latest `0.1.x` release line.

## Reporting a vulnerability

If you find a security issue, do not post secrets, exploit details, private repository data, or personal information in a public issue.

Use one of these paths:

1. If GitHub private vulnerability reporting is available for this repository, use it.
2. If private reporting is not available, open a minimal public issue that says a security report is available and asks for a private contact path.

For ordinary hardening ideas that do not expose sensitive details, public issues are welcome.

## Threat model

Relay touches these assets:

- `.relay/mission.md`, `.relay/state.md`, `.relay/queue.md`, `.relay/guardrails.md`, `.relay/automations.md`
- `.relay/events.jsonl`
- generated automation prompts and maintainer handoff notes
- summaries of recent Codex work, tool use, failures, and blockers

Relay assumes:

- the user already trusts the local repository enough to open it in Codex App
- the user has intentionally installed or enabled the Relay plugin
- repository files and generated Relay state may be committed unless the maintainer chooses otherwise
- hook payloads and automation summaries can accidentally include sensitive context if upstream tool summaries include it

Relay should not assume:

- access to browser sessions, email, calendars, secrets, API keys, or private accounts
- permission to publish, send messages, push code, or change cloud state without the user's normal Codex/GitHub approval flow
- that automation should continue when the project verdict is `paused`, `needs_human`, or `needs_review`

## Data handling boundaries

The runtime is intentionally stdlib-only and repo-local. It should:

- read only the target repository context needed to infer stack, commands, and Relay state
- write only `.relay/` files unless the maintainer explicitly asks for documentation or code changes
- keep event records lightweight and avoid storing raw secrets, tokens, private messages, or full logs
- prefer summaries and pointers over copying sensitive source material into `.relay/events.jsonl`
- treat generated automation prompts as reviewable suggestions, not silent authorization

Maintainers should review `.relay/` before committing it from private or sensitive projects.

## Security-sensitive changes

Changes need extra review when they:

- expand file system reads beyond the target repository
- add network access, package downloads, or external service calls
- make automations execute code without an explicit queue item and verdict check
- store raw tool outputs, logs, prompts, or browser/account data
- change hook behavior or event recording
- weaken the `needs_human` or `needs_review` stop conditions

## Maintainer checklist

Before shipping a release:

- run the test suite
- inspect new files that can be written under `.relay/`
- confirm no fixtures or docs contain real secrets
- confirm automation copy still tells Codex to stop on blocked or review-needed states
- keep release notes honest about what Relay can and cannot access
