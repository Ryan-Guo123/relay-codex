# Contributing

Relay for Codex is intentionally small. Contributions should make the project sharper, not broader.

## Good contributions

- reproducible bug reports
- outside-maintainer feedback on generated `.relay/pr-comment.md` files
- stuck-repo fixtures that expose a real failure mode
- improvements to verdict quality
- better recovery heuristics
- better automation pack defaults
- clearer Codex App installation guidance

## Validating Relay as an outside reviewer

If you did not run the Codex session, your feedback is especially useful. Start with [docs/reviewers-wanted.md](docs/reviewers-wanted.md), use [docs/external-maintainer-validation.md](docs/external-maintainer-validation.md), and open a `Relay handoff feedback` issue with one of these outcomes:

- `reused`
- `edited_heavily`
- `ignored`
- `confusing`

## Before opening a pull request

1. Keep the scope narrow.
2. Prefer repo-local, inspectable behavior over hidden magic.
3. Avoid adding external runtime dependencies unless the gain is obvious.
4. Run the test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

To run the runtime tests directly:

```bash
python3 -m unittest tests.test_relay_runtime
```

## Project layout

- `plugins/relay-codex/`
  - plugin manifest, assets, hooks, runtime, and skills
- `tests/`
  - fixture-backed unit tests
- `docs/`
  - maintainer docs and launch notes

## Design principles

- App-native, not CLI-first
- state should live in the repository
- recovery beats blind persistence
- small surface area is a feature

## Pull request notes

- Update docs when behavior changes.
- Add or extend fixtures when a bug fix depends on a real scenario.
- Do not silently widen Relay into a general-purpose agent framework.
