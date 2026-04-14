#!/usr/bin/env python3
"""Relay for Codex runtime.

This script powers the repo-local `.relay/` state used by the Relay plugin.
It intentionally stays stdlib-only so the plugin can run in clean workspaces.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RELAY_DIRNAME = ".relay"
QUESTION_PATTERNS = (
    "should i",
    "do you want",
    "would you like",
    "can you clarify",
    "need your input",
    "what should",
)
FAILURE_PATTERNS = ("error", "failed", "exception", "traceback")
TEST_PATTERNS = (
    "pytest",
    "npm test",
    "pnpm test",
    "yarn test",
    "bats",
    "cargo test",
    "go test",
)


@dataclass(frozen=True)
class AutomationPack:
    key: str
    name: str
    summary: str
    cadence: str
    destination: str
    prompt: str
    trigger: str


AUTOMATION_PACKS = (
    AutomationPack(
        key="continue-working",
        name="Continue Working",
        summary="Periodically inspect Relay state and create a fresh inbox item when the project should keep moving.",
        cadence="Every 2 hours during workdays",
        destination="thread",
        trigger="Use when the repo still has open queue items and no blocking verdict.",
        prompt=(
            "Inspect `.relay/state.md`, `.relay/queue.md`, and `.relay/guardrails.md`. "
            "If the project verdict is continue and the next task is clear, create a concise inbox item that tells Codex what to do next. "
            "If the verdict is paused, needs_human, or needs_review, do not continue execution blindly. Summarize why."
        ),
    ),
    AutomationPack(
        key="daily-triage",
        name="Daily Triage",
        summary="Summarize progress, unresolved work, and emerging risks once per day.",
        cadence="Every weekday morning",
        destination="thread",
        trigger="Use when a project needs regular visibility without manual inspection.",
        prompt=(
            "Summarize the last 24 hours of Relay state from `.relay/state.md`, `.relay/queue.md`, and `.relay/events.jsonl`. "
            "List recent progress, open tasks, blockers, and whether the verdict should stay continue, paused, needs_human, or needs_review."
        ),
    ),
    AutomationPack(
        key="stuck-recovery",
        name="Stuck Recovery",
        summary="Watch for stalled or repetitive work and generate a recovery brief instead of pushing Codex harder.",
        cadence="When the project enters needs_review",
        destination="thread",
        trigger="Use when hooks or inspections detect repeated failures, test-only churn, or unclear progress.",
        prompt=(
            "Inspect `.relay/state.md`, `.relay/queue.md`, and the latest entries in `.relay/events.jsonl`. "
            "If the verdict is needs_review or needs_human, produce a recovery brief with the likely cause, the smallest next investigation, and the point where a human should step in."
        ),
    ),
)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def relay_dir(root: Path) -> Path:
    return root / RELAY_DIRNAME


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            rows.append(json.loads(stripped))
        except json.JSONDecodeError:
            rows.append(
                {
                    "timestamp": iso_now(),
                    "kind": "invalid_event",
                    "summary": stripped[:200],
                }
            )
    return rows


def git_output(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def detect_repo_context(root: Path) -> dict[str, Any]:
    stack: list[str] = []
    commands: list[str] = []

    package_json = root / "package.json"
    if package_json.exists():
        stack.append("Node.js")
        try:
            payload = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        deps = {
            **payload.get("dependencies", {}),
            **payload.get("devDependencies", {}),
        }
        if "next" in deps:
            stack.append("Next.js")
        if "react" in deps:
            stack.append("React")
        if "typescript" in deps or (root / "tsconfig.json").exists():
            stack.append("TypeScript")
        scripts = payload.get("scripts", {})
        for key in ("dev", "build", "test", "lint"):
            if key in scripts:
                commands.append(f"npm run {key}")

    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        stack.append("Python")
        if (root / "tests").exists():
            commands.append("pytest")

    if (root / "Cargo.toml").exists():
        stack.append("Rust")
        commands.extend(["cargo build", "cargo test"])

    git_branch = git_output(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    visible_files = sorted(
        path.name
        for path in root.iterdir()
        if path.name not in {".git", RELAY_DIRNAME} and not path.name.startswith(".")
    )[:8]
    return {
        "project_name": root.name,
        "stack": dedupe_preserve_order(stack) or ["Unknown"],
        "commands": dedupe_preserve_order(commands),
        "git_repo": bool(git_branch) or (root / ".git").exists(),
        "git_branch": git_branch or "unknown",
        "visible_files": visible_files,
    }


def render_mission(context: dict[str, Any]) -> str:
    stack = ", ".join(context["stack"])
    visible = ", ".join(context["visible_files"]) or "No visible project files yet"
    commands = ", ".join(context["commands"]) or "No obvious dev/build/test commands detected yet"
    return f"""# Relay Mission

- Project: {context["project_name"]}
- Inferred stack: {stack}
- Git context: {"tracked repo" if context["git_repo"] else "not a git repo yet"} on branch `{context["git_branch"]}`

## Success Definition

- Keep Codex moving on the next meaningful change without losing state.
- Preserve a readable queue and escalation path for human review.
- Stop blindly continuing when progress turns repetitive or unclear.

## Observed Context

- Visible files: {visible}
- Suggested commands: {commands}

## Human Notes

- Add the real product goal here once the project direction is confirmed.
"""


def render_guardrails() -> str:
    return """# Relay Guardrails

Relay should stop trying to brute-force progress and mark the project for review when any of these patterns appear repeatedly:

- No substantive code or content change across multiple recent tool events
- Test-only or lint-only churn without advancing the queue
- Repeated failures or the same conclusion showing up again and again
- The agent keeps pushing decisions back to the user instead of narrowing the next move
- The queue is effectively done and the next action is handoff or review, not more execution

## Escalation Rules

- `continue`: next task is clear and recent events show forward motion
- `paused`: the queue is empty or the repo needs no immediate automation
- `needs_human`: Relay is blocked on missing product or operational input
- `needs_review`: Relay sees churn, repetition, or likely drift that should be inspected before continuing
"""


def render_automations() -> str:
    sections = ["# Relay Automation Packs", "", "Relay ships three packs in v1:"]
    for pack in AUTOMATION_PACKS:
        sections.extend(
            [
                "",
                f"## {pack.name}",
                f"- Purpose: {pack.summary}",
                f"- Recommended cadence: {pack.cadence}",
                f"- Trigger: {pack.trigger}",
            ]
        )
    return "\n".join(sections)


def render_queue(context: dict[str, Any], verdict: str, reasons: list[str]) -> str:
    queue_items = [
        "Confirm the real user-facing goal in `.relay/mission.md`.",
        "Choose the smallest next change that would materially move the project forward.",
        "Record blockers or review points instead of leaving them implicit.",
    ]
    if "Next.js" in context["stack"]:
        queue_items.append("Check app routes, data flow, and deployment assumptions before broad UI churn.")
    if "Python" in context["stack"]:
        queue_items.append("Confirm runtime entrypoints and test expectations before editing Python services.")
    reasons_block = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No elevated risks detected."
    checklist = "\n".join(f"- [ ] {item}" for item in queue_items)
    return f"""# Relay Queue

- Current verdict: `{verdict}`

## Next Tasks

{checklist}

## Why Relay Chose This

{reasons_block}
"""


def render_recovery_queue(verdict: str, reasons: list[str]) -> str:
    recovery_items = [
        "Restate the last successful change before making more edits.",
        "Reduce the next step to one investigation or one implementation move.",
        "If credentials, product intent, or external systems are missing, stop and ask for that input directly.",
        "Do not keep running tests or formatting loops without a concrete hypothesis.",
    ]
    queue = ["# Relay Queue", "", f"- Current verdict: `{verdict}`", "", "## Recovery Tasks", ""]
    queue.extend(f"- [ ] {item}" for item in recovery_items)
    queue.extend(["", "## Recovery Trigger", ""])
    queue.extend(f"- {reason}" for reason in reasons)
    return "\n".join(queue)


def summarize_recent_events(events: list[dict[str, Any]], limit: int = 5) -> str:
    if not events:
        return "- No Relay events recorded yet."
    lines = []
    for event in events[-limit:]:
        timestamp = event.get("timestamp", "unknown-time")
        kind = event.get("kind", "event")
        summary = event.get("summary", "No summary captured.")
        lines.append(f"- {timestamp}: `{kind}` — {summary}")
    return "\n".join(lines)


def infer_phase(context: dict[str, Any], events: list[dict[str, Any]]) -> str:
    if not events:
        return "setup"
    if any(event.get("kind") == "recovery_brief" for event in events[-3:]):
        return "recovery"
    if "Next.js" in context["stack"] or "React" in context["stack"]:
        return "delivery"
    return "active"


def render_state(context: dict[str, Any], events: list[dict[str, Any]], verdict: str, reasons: list[str]) -> str:
    recent = summarize_recent_events(events)
    reason_lines = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No active blocker signals."
    phase = infer_phase(context, events)
    return f"""# Relay State

- Verdict: `{verdict}`
- Phase: `{phase}`
- Last refreshed: {iso_now()}

## Recent Progress

{recent}

## Current Signals

{reason_lines}
"""


def normalize_summary(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    return normalized[:120]


def classify_event(event: dict[str, Any]) -> tuple[str, bool]:
    kind = event.get("kind", "note")
    summary = normalize_summary(event.get("summary", ""))
    if kind in {"write", "edit", "multi_edit"}:
        return "substantive", True
    if kind == "bash":
        if any(pattern in summary for pattern in TEST_PATTERNS):
            return "test_only", False
        if any(word in summary for word in ("build", "install", "migrate", "deploy")):
            return "substantive", True
        if any(pattern in summary for pattern in FAILURE_PATTERNS):
            return "failure", False
        return "command", False
    if any(pattern in summary for pattern in QUESTION_PATTERNS):
        return "question", False
    if any(pattern in summary for pattern in FAILURE_PATTERNS):
        return "failure", False
    return "note", False


def ensure_relay_workspace(root: Path) -> dict[str, str]:
    root.mkdir(parents=True, exist_ok=True)
    relay_root = relay_dir(root)
    relay_root.mkdir(parents=True, exist_ok=True)
    context = detect_repo_context(root)
    files_written: dict[str, str] = {}
    if not (relay_root / "mission.md").exists():
        files_written["mission.md"] = render_mission(context)
    if not (relay_root / "state.md").exists():
        files_written["state.md"] = render_state(context, [], verdict="continue", reasons=[])
    if not (relay_root / "queue.md").exists():
        files_written["queue.md"] = render_queue(context, verdict="continue", reasons=[])
    if not (relay_root / "guardrails.md").exists():
        files_written["guardrails.md"] = render_guardrails()
    if not (relay_root / "automations.md").exists():
        files_written["automations.md"] = render_automations()
    if not (relay_root / "events.jsonl").exists():
        files_written["events.jsonl"] = ""
    for name, content in files_written.items():
        target = relay_root / name
        if name.endswith(".jsonl"):
            target.touch()
        else:
            write_text(target, content)
    return files_written


def inspect_relay(root: Path) -> dict[str, Any]:
    ensure_relay_workspace(root)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    events = load_jsonl(relay_root / "events.jsonl")
    classifications = [classify_event(event) for event in events[-8:]]
    labels = [label for label, _substantive in classifications]
    substantive_flags = [substantive for _label, substantive in classifications]
    summaries = [normalize_summary(event.get("summary", "")) for event in events[-8:] if event.get("summary")]
    summary_counter = Counter(summary for summary in summaries if summary)
    repeated_summary = max(summary_counter.values(), default=0)
    open_tasks = read_text(relay_root / "queue.md").count("- [ ]")

    reasons: list[str] = []
    verdict = "continue"
    if labels.count("question") >= 2:
        verdict = "needs_human"
        reasons.append("Relay saw repeated requests for user input instead of narrowing the next move.")
    elif labels.count("failure") >= 2:
        verdict = "needs_review"
        reasons.append("Relay saw repeated failure signals in recent events.")
    elif labels.count("test_only") >= 3:
        verdict = "needs_review"
        reasons.append("Relay detected repeated test-only churn without enough evidence of forward progress.")
    elif repeated_summary >= 3:
        verdict = "needs_review"
        reasons.append("Relay saw the same conclusion repeated across multiple recent events.")
    elif len(substantive_flags) >= 5 and not any(substantive_flags[-5:]):
        verdict = "needs_review"
        reasons.append("Relay saw no substantive change across the last five tracked events.")
    elif open_tasks == 0:
        verdict = "paused"
        reasons.append("Relay found no unchecked queue items, so automatic continuation should pause.")
    else:
        reasons.append("Recent activity still supports continuing with the next queued task.")

    queue_renderer = render_recovery_queue if verdict == "needs_review" and any(
        event.get("kind") == "recovery_brief" for event in events[-3:]
    ) else render_queue
    write_text(relay_root / "state.md", render_state(context, events, verdict=verdict, reasons=reasons))
    write_text(relay_root / "queue.md", queue_renderer(context, verdict, reasons) if queue_renderer is render_queue else queue_renderer(verdict, reasons))
    return {
      "root": str(root),
      "relay_dir": str(relay_root),
      "project": context["project_name"],
      "verdict": verdict,
      "reasons": reasons,
      "event_count": len(events),
      "open_tasks": open_tasks,
      "stack": context["stack"]
    }


def recover_relay(root: Path) -> dict[str, Any]:
    inspection = inspect_relay(root)
    relay_root = relay_dir(root)
    write_text(relay_root / "queue.md", render_recovery_queue(inspection["verdict"], inspection["reasons"]))
    append_jsonl(
        relay_root / "events.jsonl",
        {
            "timestamp": iso_now(),
            "kind": "recovery_brief",
            "summary": "Relay generated a recovery queue because recent signals suggest the project needs review.",
        },
    )
    return inspect_relay(root)


def write_pack_summary(root: Path) -> None:
    relay_root = relay_dir(root)
    lines = ["# Relay Automation Packs", "", f"- Last refreshed: {iso_now()}", ""]
    for pack in AUTOMATION_PACKS:
        lines.extend(
            [
                f"## {pack.name}",
                f"- Purpose: {pack.summary}",
                f"- Recommended cadence: {pack.cadence}",
                f"- Trigger: {pack.trigger}",
                "",
            ]
        )
    write_text(relay_root / "automations.md", "\n".join(lines))


def render_pack_payload(root: Path) -> dict[str, Any]:
    return {
        "relay_dir": str(relay_dir(root)),
        "packs": [
            {
                "key": pack.key,
                "name": pack.name,
                "summary": pack.summary,
                "cadence": pack.cadence,
                "destination": pack.destination,
                "trigger": pack.trigger,
                "prompt": pack.prompt,
            }
            for pack in AUTOMATION_PACKS
        ],
    }


def parse_hook_payload() -> dict[str, Any]:
    payload = ""
    if not sys.stdin.isatty():
        payload = sys.stdin.read().strip()
    if not payload:
        payload = os.environ.get("CODEX_HOOK_PAYLOAD", "").strip()
    event: dict[str, Any] = {}
    if payload:
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            event["raw"] = payload
    tool_name = event.get("tool_name") or event.get("tool") or os.environ.get("CODEX_TOOL_NAME") or "unknown"
    tool_input = event.get("tool_input") or {}
    command = tool_input.get("command") or os.environ.get("CODEX_TOOL_COMMAND", "")
    raw_summary = json.dumps(event, ensure_ascii=True)[:240] if event else ""
    summary = command or event.get("summary") or raw_summary or "PostToolUse hook triggered."
    kind_map = {
        "Write": "write",
        "Edit": "edit",
        "MultiEdit": "multi_edit",
        "Bash": "bash",
    }
    return {
        "timestamp": iso_now(),
        "kind": kind_map.get(tool_name, tool_name.lower().replace(" ", "_")),
        "tool_name": tool_name,
        "summary": summary,
    }


def handle_hook(root: Path) -> dict[str, Any]:
    relay_root = relay_dir(root)
    if not relay_root.exists():
        return {"root": str(root), "updated": False, "reason": "relay_not_enabled"}
    event = parse_hook_payload()
    append_jsonl(relay_root / "events.jsonl", event)
    inspection = inspect_relay(root)
    return {"root": str(root), "updated": True, "event": event, "verdict": inspection["verdict"]}


def print_json(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def cmd_enable(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    files_written = ensure_relay_workspace(root)
    inspection = inspect_relay(root)
    payload = {"root": str(root), "created": sorted(files_written), "inspection": inspection}
    if args.json:
        print_json(payload)
    else:
        print(f"Relay enabled in {root}")
        for name in sorted(files_written):
            print(f"- created {RELAY_DIRNAME}/{name}")
        print(f"Verdict: {inspection['verdict']}")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    payload = inspect_relay(args.root.resolve())
    if args.json:
        print_json(payload)
    else:
        print(f"Relay verdict: {payload['verdict']}")
        for reason in payload["reasons"]:
            print(f"- {reason}")
    return 0


def cmd_recover(args: argparse.Namespace) -> int:
    payload = recover_relay(args.root.resolve())
    if args.json:
        print_json(payload)
    else:
        print(f"Relay recovery verdict: {payload['verdict']}")
        for reason in payload["reasons"]:
            print(f"- {reason}")
    return 0


def cmd_automations(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    ensure_relay_workspace(root)
    write_pack_summary(root)
    payload = render_pack_payload(root)
    if args.json:
        print_json(payload)
    else:
        for pack in payload["packs"]:
            print(f"{pack['name']}: {pack['summary']}")
    return 0


def cmd_hook(args: argparse.Namespace) -> int:
    payload = handle_hook(args.root.resolve())
    if args.json:
        print_json(payload)
    else:
        if payload.get("updated"):
            print(f"Relay updated after hook with verdict {payload['verdict']}")
        else:
            print("Relay hook skipped because .relay is not enabled in this repo.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Relay for Codex runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, handler in (
        ("enable", cmd_enable),
        ("inspect", cmd_inspect),
        ("recover", cmd_recover),
        ("automations", cmd_automations),
        ("hook-posttooluse", cmd_hook),
    ):
        command = subparsers.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--json", action="store_true")
        command.set_defaults(func=handler)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
