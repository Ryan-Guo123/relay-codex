# Relay for Codex

Relay for Codex is a Codex App plugin by Ryan-Guo123. It keeps project work moving without forcing the user to manage threads, session continuity, or "should I keep going?" decisions by hand.

It is inspired by Ralph-style agent workflows, but rebuilt for Codex App primitives: skills, hooks, automations, and repo-local state under `.relay/`.

## English

### What v1 does

- Enables Relay in the current repo and creates a durable `.relay/` workspace
- Tracks recent activity through a lightweight `PostToolUse` hook
- Maintains a four-state verdict for the project:
  - `continue`
  - `paused`
  - `needs_human`
  - `needs_review`
- Produces three automation packs:
  - `Continue Working`
  - `Daily Triage`
  - `Stuck Recovery`

### Repo Layout

```text
plugins/relay-codex/
  .codex-plugin/plugin.json
  hooks.json
  assets/
  scripts/relay_runtime.py
  skills/
tests/
```

### Quick Start

1. Install the plugin from this repo's marketplace entry.
2. In Codex App, use `Enable Relay in this repo`.
3. Review the generated `.relay/` files.
4. Ask Relay to inspect state or install automations.

### Local Validation

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

### Status Files

Relay stores project state in `.relay/`:

- `mission.md`
- `state.md`
- `queue.md`
- `guardrails.md`
- `automations.md`
- `events.jsonl`

These files are repo-local on purpose. Relay is meant to make Codex workflows inspectable and handoff-friendly.

## 中文

### v1 能做什么

- 在当前仓库启用 Relay，并创建可持续维护的 `.relay/` 工作区
- 通过轻量级 `PostToolUse` hook 追踪最近活动
- 为项目维护四种状态结论：
  - `continue`
  - `paused`
  - `needs_human`
  - `needs_review`
- 生成三套 automation pack：
  - `Continue Working`
  - `Daily Triage`
  - `Stuck Recovery`

### 仓库结构

```text
plugins/relay-codex/
  .codex-plugin/plugin.json
  hooks.json
  assets/
  scripts/relay_runtime.py
  skills/
tests/
```

### 快速开始

1. 通过本仓库的 marketplace entry 安装插件。
2. 在 Codex App 里使用 `Enable Relay in this repo`。
3. 查看生成的 `.relay/` 状态文件。
4. 继续让 Relay 检查状态或安装 automations。

### 本地验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

### 状态文件

Relay 会把项目状态写入 `.relay/`：

- `mission.md`
- `state.md`
- `queue.md`
- `guardrails.md`
- `automations.md`
- `events.jsonl`

这些文件故意保留在仓库本地。Relay 的目标是让 Codex 工作流可检查、可交接、可继续推进。
