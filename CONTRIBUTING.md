# Contributing

Relay for Codex is intentionally small. Contributions should make the project sharper, not broader.

## Good contributions

- reproducible bug reports
- stuck-repo fixtures that expose a real failure mode
- improvements to verdict quality
- better recovery heuristics
- better automation pack defaults
- clearer Codex App installation guidance

## Before opening a pull request

1. Keep the scope narrow.
2. Prefer repo-local, inspectable behavior over hidden magic.
3. Avoid adding external runtime dependencies unless the gain is obvious.
4. Run the test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
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
