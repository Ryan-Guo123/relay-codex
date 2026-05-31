# Security Policy

Relay for Codex is a local workflow layer for Codex App projects. It writes repo-local state, reads repo context, and produces maintainer-facing handoff guidance. It should not become a hidden background agent with broad access.

## Supported versions

Security fixes are accepted for the latest `0.1.x` release line and the current `main` branch.

Older tags are not supported unless the fix can be applied without changing the public artifact format or install flow.

## Reporting a vulnerability

If you find a security issue, do not post secrets, exploit details, private repository data, or personal information in a public issue.

Use one of these paths:

1. If GitHub private vulnerability reporting is available for this repository, use it.
2. If private reporting is not available, open a minimal public issue that says a security report is available and asks for a private contact path.

For ordinary hardening ideas that do not expose sensitive details, public issues are welcome.

Expected response:

- acknowledgement target: 7 days
- initial triage target: 14 days
- public advisory or release note: after a fix is available, when disclosure would not put users at extra risk

This is a small open-source project, so these are targets rather than service-level guarantees.

## In scope

Security reports are in scope when they involve:

- Relay reading files outside the intended repository root
- Relay writing outside `.relay/` without explicit maintainer action
- generated `.relay/` artifacts capturing secrets, private account data, or raw logs unexpectedly
- GitHub Actions trial workflows weakening checksum verification, token scope, or artifact boundaries
- runtime changes that allow network writes, publishing, pushing, or messaging without the normal Codex/GitHub approval flow
- release artifacts, install instructions, or plugin metadata that could cause maintainers to run untrusted code unexpectedly

## Out of scope

These are usually not security issues by themselves:

- generated handoff text that is incomplete, noisy, or strategically wrong
- a reviewer choosing to commit `.relay/` files from a private repository after seeing the warning
- normal GitHub token permissions granted by a repository owner to their own workflows
- attacks that require already having write access to the target repository
- social-engineering requests for stars, sponsorship, or maintainer attention

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

The copy-paste external trial workflow is also part of the trust boundary. It should stay pinned to a release artifact, verify the runtime checksum before execution, and upload only the generated Relay artifacts needed for review.

## Data handling boundaries

The runtime is intentionally stdlib-only and repo-local. It should:

- read only the target repository context needed to infer stack, commands, and Relay state
- write only `.relay/` files unless the maintainer explicitly asks for documentation or code changes
- keep event records lightweight and avoid storing raw secrets, tokens, private messages, or full logs
- prefer summaries and pointers over copying sensitive source material into `.relay/events.jsonl`
- treat generated automation prompts as reviewable suggestions, not silent authorization

Maintainers should review `.relay/` before committing it from private or sensitive projects.

If Relay is used on a regulated, confidential, or customer-data-bearing repository, prefer a disposable branch or external trial first and inspect the generated bundle before sharing it with anyone outside the repository.

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
