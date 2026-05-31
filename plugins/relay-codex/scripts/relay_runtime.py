#!/usr/bin/env python3
"""Relay for Codex runtime.

This script powers the repo-local `.relay/` state used by the Relay plugin.
It intentionally stays stdlib-only so the plugin can run in clean workspaces.
"""

from __future__ import annotations

import argparse
import fnmatch
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
CODEOWNERS_LOCATIONS = (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS")
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
REVIEW_SENSITIVE_PATHS = (
    ("CI / automation", re.compile(r"(^|/)(\.github/workflows|\.gitlab-ci\.yml|circle\.yml|azure-pipelines\.yml|Jenkinsfile)")),
    ("Secrets / environment", re.compile(r"(^|/)(\.env|\.npmrc|\.pypirc|secrets?|credentials?)", re.IGNORECASE)),
    ("Auth / permissions", re.compile(r"(^|/)(auth|oauth|permission|policy|rbac|session|token|jwt)(/|\.|-|_)", re.IGNORECASE)),
    ("Security", re.compile(r"(^|/)(security|crypto|csrf|cors|csp|sanitize|encrypt|decrypt)(/|\.|-|_)", re.IGNORECASE)),
    ("Deploy / infrastructure", re.compile(r"(^|/)(Dockerfile|docker-compose|vercel\.json|wrangler\.toml|terraform|infra|deploy|k8s|helm)(/|\.|-|_)?", re.IGNORECASE)),
    ("Database / migrations", re.compile(r"(^|/)(migrations?|schema|prisma|supabase)(/|\.|-|_)", re.IGNORECASE)),
    ("Dependency manifest", re.compile(r"(^|/)(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|requirements\.txt|poetry\.lock|Cargo\.lock|Gemfile\.lock)$")),
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
    AutomationPack(
        key="release-readiness",
        name="Release Readiness",
        summary="Generate a release checklist before tagging or publishing a GitHub release.",
        cadence="Before every public release",
        destination="thread",
        trigger="Use when a maintainer is preparing a tag, GitHub release, launch note, or release handoff.",
        prompt=(
            "Inspect `.relay/state.md`, `.relay/queue.md`, `.relay/handoff.md`, and `.relay/release-checklist.md` if present. "
            "Generate or refresh the release checklist. Do not tag, push tags, publish a GitHub release, or announce externally unless the user explicitly approves that release action. "
            "If the verdict is needs_human or needs_review, explain what must be reviewed before release."
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
    return result.stdout.rstrip("\n")


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


def summarize_last_success(events: list[dict[str, Any]]) -> str:
    for event in reversed(events):
        _label, substantive = classify_event(event)
        if substantive:
            timestamp = event.get("timestamp", "unknown-time")
            summary = event.get("summary", "No summary captured.")
            return f"{timestamp}: {summary}"
    return "No substantive Relay event recorded yet."


def summarize_verification(events: list[dict[str, Any]], commands: list[str]) -> str:
    verification_events: list[str] = []
    for event in events[-8:]:
        label, _substantive = classify_event(event)
        summary = event.get("summary", "No summary captured.")
        timestamp = event.get("timestamp", "unknown-time")
        normalized = normalize_summary(summary)
        if label == "test_only" or any(word in normalized for word in ("test", "lint", "build", "typecheck")):
            verification_events.append(f"- {timestamp}: {summary}")

    if verification_events:
        return "\n".join(verification_events)

    suggested = [
        command
        for command in commands
        if any(word in command for word in ("test", "lint", "build", "check"))
    ]
    if suggested:
        return "\n".join(f"- Not recorded yet. Suggested: run `{command}`." for command in suggested)
    return "- No verification command or event captured yet."


def collect_changed_files(root: Path, base_ref: str | None = None) -> list[str]:
    git_top_level = git_output(root, ["rev-parse", "--show-toplevel"])
    if git_top_level and Path(git_top_level).resolve() != root.resolve() and not (root / ".git").exists():
        return []

    if base_ref:
        diff = git_output(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_ref}...HEAD"])
        if not diff:
            diff = git_output(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_ref}..HEAD"])
        files = [
            line.strip()
            for line in diff.splitlines()
            if line.strip() and line.strip() != RELAY_DIRNAME and not line.strip().startswith(f"{RELAY_DIRNAME}/")
        ]
        return dedupe_preserve_order(files)

    status = git_output(root, ["status", "--short", "--untracked-files=all"])
    if not status:
        return []

    files: list[str] = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path == RELAY_DIRNAME or path.startswith(f"{RELAY_DIRNAME}/"):
            continue
        files.append(path)

    return dedupe_preserve_order(files)


def summarize_changed_files(root: Path, base_ref: str | None = None) -> str:
    files = collect_changed_files(root, base_ref=base_ref)
    if not files:
        if base_ref:
            return f"- No Git changes detected against `{base_ref}`."
        return "- No Git changes detected in the current workspace."

    display = files[:12]
    lines = [f"- `{path}`" for path in display]
    if len(files) > len(display):
        lines.append(f"- ...and {len(files) - len(display)} more file(s).")
    return "\n".join(lines)


def detect_sensitive_review_paths(files: list[str]) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    for path in files:
        normalized = path.strip()
        for label, pattern in REVIEW_SENSITIVE_PATHS:
            if pattern.search(normalized):
                matches.append((label, normalized))
                break
    return matches


def load_codeowners(root: Path) -> tuple[str, list[tuple[str, list[str]]]]:
    for relative_path in CODEOWNERS_LOCATIONS:
        source = root / relative_path
        if not source.exists():
            continue
        rules: list[tuple[str, list[str]]] = []
        for line in source.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split()
            if len(parts) < 2:
                continue
            pattern = parts[0]
            owners = [part for part in parts[1:] if part.startswith("@")]
            if owners:
                rules.append((pattern, owners))
        return relative_path, rules
    return "", []


def codeowner_pattern_matches(pattern: str, path: str) -> bool:
    normalized = pattern.strip()
    if not normalized:
        return False
    normalized = normalized.lstrip("/")
    if normalized.endswith("/"):
        prefix = normalized.rstrip("/")
        return path == prefix or path.startswith(f"{prefix}/")
    if "/" not in normalized:
        return fnmatch.fnmatch(Path(path).name, normalized)
    return fnmatch.fnmatch(path, normalized) or fnmatch.fnmatch(f"/{path}", pattern)


def match_codeowners(path: str, rules: list[tuple[str, list[str]]]) -> list[str]:
    matched: list[str] = []
    for pattern, owners in rules:
        if codeowner_pattern_matches(pattern, path):
            matched = owners
    return matched


def summarize_review_routing(root: Path, files: list[str]) -> tuple[list[str], dict[str, Any]]:
    source, rules = load_codeowners(root)
    metadata: dict[str, Any] = {
        "codeowners_path": source or None,
        "suggested_reviewers": [],
        "unowned_paths": [],
    }

    if not files:
        return [], metadata
    if not source:
        return ["- Review routing: No CODEOWNERS file detected."], metadata
    if not rules:
        return [f"- Review routing: `{source}` exists but has no supported owner rules."], metadata

    owner_paths: dict[str, list[str]] = {}
    unowned_paths: list[str] = []
    for path in files:
        owners = match_codeowners(path, rules)
        if not owners:
            unowned_paths.append(path)
            continue
        for owner in owners:
            owner_paths.setdefault(owner, []).append(path)

    metadata["suggested_reviewers"] = [
        {"owner": owner, "paths": paths}
        for owner, paths in sorted(owner_paths.items())
    ]
    metadata["unowned_paths"] = unowned_paths

    if not owner_paths:
        return [f"- Review routing: `{source}` found, but no CODEOWNERS rule matched the changed files."], metadata

    lines = [f"- Review routing from `{source}`:"]
    for owner, paths in sorted(owner_paths.items())[:8]:
        sample = ", ".join(f"`{path}`" for path in paths[:3])
        suffix = f" and {len(paths) - 3} more" if len(paths) > 3 else ""
        lines.append(f"  - {owner}: {sample}{suffix}")
    if unowned_paths:
        lines.append(f"  - Unowned changed paths: {len(unowned_paths)}")
    return lines, metadata


def decide_review_readiness(metadata: dict[str, Any]) -> dict[str, str]:
    suggested_reviewers = metadata["review_routing"]["suggested_reviewers"]
    unowned_paths = metadata["review_routing"]["unowned_paths"]
    if metadata["large_change"]:
        return {
            "risk_level": "high",
            "decision": "split_or_summarize",
            "recommended_action": "Ask for a split or a tighter maintainer summary before deep review.",
        }
    if metadata["sensitive_paths"]:
        return {
            "risk_level": "high",
            "decision": "owner_review_required",
            "recommended_action": "Route to an owner for the sensitive area before merge.",
        }
    if unowned_paths:
        return {
            "risk_level": "medium",
            "decision": "review_unowned_paths",
            "recommended_action": "Check unowned changed paths and decide who should review them.",
        }
    if suggested_reviewers:
        return {
            "risk_level": "medium",
            "decision": "request_codeowners_review",
            "recommended_action": "Request review from the suggested CODEOWNERS owner(s).",
        }
    if metadata["changed_file_count"] == 0:
        return {
            "risk_level": "none",
            "decision": "no_changed_files",
            "recommended_action": "Treat this as a handoff sample; no code-review gate is available without changed files.",
        }
    return {
        "risk_level": "low",
        "decision": "normal_review",
        "recommended_action": "Scope looks small enough for normal maintainer review.",
    }


def summarize_review_readiness(root: Path, base_ref: str | None = None) -> tuple[str, dict[str, Any]]:
    files = collect_changed_files(root, base_ref=base_ref)
    sensitive_paths = detect_sensitive_review_paths(files)
    file_count = len(files)
    large_change = file_count > 12
    routing_lines, routing_metadata = summarize_review_routing(root, files)

    if not files:
        scope_note = f"No non-Relay Git changes detected against `{base_ref}`." if base_ref else "No non-Relay Git changes detected."
        lines = [
            f"- Scope: {scope_note}",
            "- Review signal: Use this artifact as a handoff sample, not as proof that code changed.",
        ]
    else:
        scope = "large review surface" if large_change else "focused review surface"
        source = f" against `{base_ref}`" if base_ref else ""
        lines = [f"- Scope: {file_count} non-Relay changed file(s){source}, {scope}."]
        if sensitive_paths:
            lines.append("- Sensitive paths detected:")
            for label, path in sensitive_paths[:8]:
                lines.append(f"  - `{path}` ({label})")
            if len(sensitive_paths) > 8:
                lines.append(f"  - ...and {len(sensitive_paths) - 8} more sensitive path(s).")
        else:
            lines.append("- Sensitive paths detected: none from Relay's default path scan.")
        if large_change:
            lines.append("- Review signal: Consider splitting the PR or asking for a tighter summary before deep review.")
        elif sensitive_paths:
            lines.append("- Review signal: Ask a maintainer familiar with the sensitive area to inspect before merge.")
        else:
            lines.append("- Review signal: Changed-file scope looks small enough for normal maintainer review.")
        lines.extend(routing_lines)

    metadata: dict[str, Any] = {
        "changed_file_count": file_count,
        "base_ref": base_ref,
        "change_source": "base_ref_diff" if base_ref else "git_status",
        "large_change": large_change,
        "sensitive_paths": [{"label": label, "path": path} for label, path in sensitive_paths],
        "review_routing": routing_metadata,
    }
    metadata["decision"] = decide_review_readiness(metadata)
    return "\n".join(lines), metadata


def render_review_readiness(context: dict[str, Any], inspection: dict[str, Any], summary: str) -> str:
    metadata = inspection["review_readiness"]
    verdict = inspection["verdict"]
    reasons = inspection["reasons"]
    reason_lines = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No active blocker signals."
    routing = metadata["review_routing"]
    suggested_reviewers = routing["suggested_reviewers"]

    if suggested_reviewers:
        reviewer_lines = "\n".join(
            f"- {entry['owner']}: {', '.join(f'`{path}`' for path in entry['paths'][:5])}"
            for entry in suggested_reviewers[:8]
        )
    elif routing["codeowners_path"]:
        reviewer_lines = "- No CODEOWNERS owner matched the changed files."
    else:
        reviewer_lines = "- No CODEOWNERS file detected."

    decision = metadata["decision"]["recommended_action"]

    return f"""# Relay Review Readiness

- Project: `{context["project_name"]}`
- Branch: `{context["git_branch"]}`
- Verdict: `{verdict}`
- Generated: {iso_now()}

## Review Gate

{summary}

## Suggested Reviewers

{reviewer_lines}

## Current Relay Signals

{reason_lines}

## Recommended Review Decision

{decision}

## Safe Use

- This is a routing and review-prep artifact, not merge approval.
- Use Codex Goals for execution; use Relay review readiness to decide who should inspect the PR and whether the scope is reviewable.
- Redact sensitive paths or internal owner names before sharing publicly.
"""


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


def render_handoff(context: dict[str, Any], events: list[dict[str, Any]], inspection: dict[str, Any]) -> str:
    reasons = inspection["reasons"]
    reason_lines = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No active blocker signals."
    recent = summarize_recent_events(events, limit=6)
    last_success = summarize_last_success(events)
    queue = read_text(relay_dir(Path(inspection["root"])) / "queue.md").strip() or "No queue captured."
    verdict = inspection["verdict"]

    if verdict == "continue":
        next_action = "Pick one unchecked item from `.relay/queue.md` and continue with the smallest meaningful change."
        review_focus = "Confirm the queued task still maps to the PR or release goal before making more edits."
    elif verdict == "paused":
        next_action = "Do not schedule more agent work until a new maintainer goal or queue item exists."
        review_focus = "Check whether the project is actually complete or just missing a next task."
    elif verdict == "needs_human":
        next_action = "Ask for the missing product, credential, approval, or scope decision before continuing."
        review_focus = "Resolve the human decision point explicitly; do not let Codex guess."
    else:
        next_action = "Switch to recovery: restate the last success, isolate one failing signal, and stop broad retries."
        review_focus = "Look for repeated failures, test-only churn, or repeated conclusions before approving more work."

    return f"""# Relay Handoff

- Project: {context["project_name"]}
- Stack: {", ".join(context["stack"])}
- Git branch: `{context["git_branch"]}`
- Verdict: `{verdict}`
- Generated: {iso_now()}

## Maintainer Summary

Relay generated this handoff so a human maintainer or future Codex run can decide whether to continue, pause, recover, or ask for input before more work happens.

## Last Successful Signal

- {last_success}

## Current Signals

{reason_lines}

## Recent Events

{recent}

## Queue Snapshot

```markdown
{queue}
```

## Recommended Next Action

{next_action}

## Review Focus

{review_focus}

## Safe Handoff Rules

- Use Codex goals for the thread objective and completion contract; use Relay handoff for repo-local evidence, review gates, and future pickup.
- Do not continue automatically when the verdict is `needs_human` or `needs_review`.
- Keep the next action to one investigation or one implementation move.
- If this handoff is used in a PR, include the verdict, last successful signal, and recommended next action in the PR note.
"""


def write_handoff(root: Path) -> dict[str, Any]:
    inspection = inspect_relay(root)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    events = load_jsonl(relay_root / "events.jsonl")
    write_text(relay_root / "handoff.md", render_handoff(context, events, inspection))
    return {**inspection, "handoff": str(relay_root / "handoff.md")}


def render_pr_comment(context: dict[str, Any], events: list[dict[str, Any]], inspection: dict[str, Any], base_ref: str | None = None) -> str:
    reasons = inspection["reasons"]
    reason_lines = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No active blocker signals."
    recent = summarize_recent_events(events, limit=4)
    last_success = summarize_last_success(events)
    verification = summarize_verification(events, context["commands"])
    changed_files = summarize_changed_files(Path(inspection["root"]), base_ref=base_ref)
    review_readiness, _readiness_metadata = summarize_review_readiness(Path(inspection["root"]), base_ref=base_ref)
    verdict = inspection["verdict"]

    if verdict == "continue":
        posture = "Ready for maintainer review or one focused follow-up task."
        next_action = "Review the changed files and pick one remaining queue item if more work is needed."
    elif verdict == "paused":
        posture = "No automatic follow-up should be scheduled until the queue is intentionally reopened."
        next_action = "Confirm whether the PR is complete or needs a new explicit task."
    elif verdict == "needs_human":
        posture = "Blocked on a human decision before more implementation work."
        next_action = "Resolve the missing product, credential, approval, or scope input."
    else:
        posture = "Needs maintainer review before another agent pass."
        next_action = "Inspect the repeated failure or churn signal, then choose one narrow recovery step."

    return f"""## Relay PR Handoff

Relay converted the current Codex run state into a GitHub-ready review note. It does not post this comment automatically.

### Current State

- Project: `{context["project_name"]}`
- Branch: `{context["git_branch"]}`
- Verdict: `{verdict}`
- Review posture: {posture}
- Generated: {iso_now()}

### What Changed

{changed_files}

### Review Readiness

{review_readiness}

### Last Successful Signal

- {last_success}

### Verification

{verification}

### Risks / Review Focus

{reason_lines}

### Recent Relay Events

{recent}

### Recommended Next Action

{next_action}

### Maintainer Checklist

- [ ] Confirm the changed files match the PR intent.
- [ ] Check any sensitive paths or large-scope warning before requesting review.
- [ ] Confirm verification evidence is present or run the suggested command.
- [ ] Resolve any `needs_human` or `needs_review` signal before merge.
- [ ] Paste or adapt this note into the PR only after removing sensitive context.
"""


def write_pr_comment(root: Path, base_ref: str | None = None) -> dict[str, Any]:
    handoff_payload = write_handoff(root)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    events = load_jsonl(relay_root / "events.jsonl")
    target = relay_root / "pr-comment.md"
    _review_readiness, readiness_metadata = summarize_review_readiness(root, base_ref=base_ref)
    write_text(target, render_pr_comment(context, events, handoff_payload, base_ref=base_ref))
    return {**handoff_payload, "pr_comment": str(target), "review_readiness": readiness_metadata}


def write_review_readiness(root: Path, base_ref: str | None = None) -> dict[str, Any]:
    inspection = inspect_relay(root)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    target = relay_root / "review-readiness.md"
    summary, readiness_metadata = summarize_review_readiness(root, base_ref=base_ref)
    payload = {**inspection, "review_readiness": readiness_metadata}
    write_text(target, render_review_readiness(context, payload, summary))
    return {**payload, "review_readiness_artifact": str(target)}


def render_reviewer_pack(context: dict[str, Any], pr_comment: str, inspection: dict[str, Any]) -> str:
    return f"""# Relay Reviewer Pack

- Project: `{context["project_name"]}`
- Branch: `{context["git_branch"]}`
- Verdict: `{inspection["verdict"]}`
- Generated: {iso_now()}

## Reviewer Ask

I am testing whether Relay's generated PR handoff is useful for maintainers.

Please compare the Relay handoff below with a normal Codex/manual summary for the same PR or task.

Could you tell what changed, what was verified, what still needs review, and what the next action should be?

Could you also tell whether the changed-file scope and sensitive-path scan are enough to decide who should review this PR?

Please be blunt: would you reuse this, edit it heavily, ignore it, or ask for a different format?

Also compare Relay with AI PR review tools such as Copilot code review, CodeRabbit, Graphite, Qodo, or PR-Agent:

- `in_addition`: Relay gives context or provenance the review bot does not.
- `before_review`: Relay helps decide whether a PR is ready for any reviewer.
- `instead`: Relay is enough for this small PR or release handoff.
- `not_needed`: an existing AI PR review tool already solves this job.
- `unsure`: you would need to test both on a real PR first.

## Relay Handoff To Review

```markdown
{pr_comment.strip()}
```

## Compare Against

Paste or link the normal Codex/manual summary here before sending this pack to a reviewer.

```markdown
TODO: Add the non-Relay summary for comparison.
```

## Scoring Rubric

Score each item from 1 to 5.

| Question | Score | Notes |
| --- | --- | --- |
| Changed files are clear |  |  |
| Verification is reviewable |  |  |
| Review focus points to the right risk |  |  |
| Review readiness signals are useful |  |  |
| Next action is directly actionable |  |  |
| GitHub fit is pasteable |  |  |
| Fit with AI PR review tools is clear |  |  |

## Required Outcome

Choose one:

- `reused`: the reviewer reused most of the generated handoff.
- `edited_heavily`: the structure helped, but the content needed major edits.
- `ignored`: the generated handoff was not useful.
- `confusing`: the reviewer could not tell what to do with it.

## Record The Feedback

Open a GitHub issue with the `Relay handoff feedback` template and include:

- the PR or task being reviewed
- the redacted Relay handoff excerpt
- the comparison summary
- the outcome
- whether Relay is `in_addition`, `before_review`, `instead`, `not_needed`, or `unsure` compared with AI PR review tools
- the product decision: keep, simplify, rename, remove, or test again

Do not treat this pack as proof of value until someone outside the current build thread responds.
"""


def write_reviewer_pack(root: Path, base_ref: str | None = None) -> dict[str, Any]:
    pr_payload = write_pr_comment(root, base_ref=base_ref)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    pr_comment = read_text(relay_root / "pr-comment.md")
    target = relay_root / "reviewer-pack.md"
    write_text(target, render_reviewer_pack(context, pr_comment, pr_payload))
    return {**pr_payload, "reviewer_pack": str(target)}


def render_validation_brief(context: dict[str, Any], reviewer_pack: str, payload: dict[str, Any]) -> str:
    readiness = payload.get("review_readiness", {})
    decision = readiness.get("decision", {})
    changed_count = readiness.get("changed_file_count", 0)
    base_ref = readiness.get("base_ref")
    base_line = f"- Base ref: `{base_ref}`" if base_ref else "- Base ref: current worktree status"
    action = decision.get("recommended_action", "Ask an outside reviewer to compare the Relay handoff with a normal summary.")
    return f"""# Relay Validation Brief

- Project: `{context["project_name"]}`
- Branch: `{context["git_branch"]}`
- Verdict: `{payload["verdict"]}`
- Generated: {iso_now()}
{base_line}

## Validation Goal

Get one outside maintainer or frequent PR reviewer to compare Relay's generated handoff with a normal Codex/manual summary and record one blunt outcome.

This brief is not proof of product value. It is the packet to send when collecting proof.

## Artifacts To Share

- `.relay/review-readiness.md`
- `.relay/pr-comment.md`
- `.relay/reviewer-pack.md`

## Current Review Gate

- Changed files: {changed_count}
- Risk level: `{decision.get("risk_level", "unknown")}`
- Decision: `{decision.get("decision", "unknown")}`
- Recommended action: {action}

## Short Ask

```text
I am validating Relay for Codex, a small tool that turns Codex work into GitHub-ready maintainer handoffs.

Could you spend about 10 minutes comparing this Relay handoff with a normal Codex/manual summary?

Please record one outcome: reused, edited_heavily, ignored, or confusing.

Also record whether Relay is useful in addition to, before, or instead of AI PR review tools such as Copilot code review, CodeRabbit, Graphite, Qodo, or PR-Agent. If an existing review bot already solves this job, mark Relay `not_needed`.

The useful question is not whether the repo looks polished. It is whether this handoff helps you decide what changed, what was verified, what still needs review, and what should happen next.
```

## Reviewer Pack

````markdown
{reviewer_pack.strip()}
````

## Feedback To Record

- Link to the PR or task being reviewed.
- Link or paste the redacted Relay handoff.
- Link or paste the normal Codex/manual summary used for comparison.
- Record one outcome: `reused`, `edited_heavily`, `ignored`, or `confusing`.
- Record AI review fit: `in_addition`, `before_review`, `instead`, `not_needed`, or `unsure`.
- Record whether the reviewer identified changed files, verification, review focus, and next action without reading the full Codex thread.
- Update `docs/validation-ledger.md` with the result.

## Guardrails

- Do not ask for stars, sponsorship, or praise in the validation ask.
- Do not count this brief, an internal PR, or a synthetic demo as validation.
- Redact secrets, customer data, private links, and internal owner names before sharing.
- If the reviewer marks this `ignored` or `confusing`, treat that as useful product signal.
- If the reviewer marks Relay `not_needed` compared with an AI PR review tool, shrink to a template/schema or stop instead of adding features.
"""


def write_validation_brief(root: Path, base_ref: str | None = None) -> dict[str, Any]:
    pack_payload = write_reviewer_pack(root, base_ref=base_ref)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    reviewer_pack = read_text(relay_root / "reviewer-pack.md")
    target = relay_root / "validation-brief.md"
    write_text(target, render_validation_brief(context, reviewer_pack, pack_payload))
    return {**pack_payload, "validation_brief": str(target)}


def render_release_checklist(context: dict[str, Any], inspection: dict[str, Any]) -> str:
    commands = context["commands"]
    test_commands = [command for command in commands if "test" in command]
    if not test_commands and (Path(inspection["root"]) / "tests").exists():
        test_commands = ["python3 -m unittest discover -s tests -p 'test_*.py'"]
    test_lines = "\n".join(f"- [ ] Run `{command}` and record the result." for command in test_commands)
    if not test_lines:
        test_lines = "- [ ] Identify the smallest project-specific smoke test and record why it is sufficient."

    if inspection["verdict"] in {"needs_human", "needs_review"}:
        release_posture = "Do not release until the verdict is reviewed and the blocker is resolved or explicitly accepted."
    elif inspection["verdict"] == "paused":
        release_posture = "Release is possible only if the queue is intentionally complete and the changelog is clear."
    else:
        release_posture = "Release can proceed after tests, changelog, and human approval are complete."

    return f"""# Relay Release Checklist

- Project: {context["project_name"]}
- Current verdict: `{inspection["verdict"]}`
- Generated: {iso_now()}

## Release Posture

{release_posture}

## 1. Scope

- [ ] Name the release type: patch, minor, major, docs-only, or internal.
- [ ] List the merged PRs or commits included in this release.
- [ ] Confirm no unrelated work is bundled into the release.

## 2. Verification

{test_lines}
- [ ] Run `git status --short` and confirm the release branch is clean.
- [ ] Confirm generated `.relay/` files do not contain secrets or private context.

## 3. Version And Tag

- [ ] Update the package or plugin version if behavior changed.
- [ ] Choose the exact tag, for example `v0.1.3`.
- [ ] Create an annotated tag only after verification passes.
- [ ] Push the tag to GitHub.

## 4. Release Notes

- [ ] Summarize what changed in user-facing language.
- [ ] Explain why the change matters.
- [ ] Link merged PRs and closed issues.
- [ ] State any known limitations or follow-up work.

## 5. Human Approval Gates

- [ ] Human confirms this release should be public.
- [ ] Human confirms the release notes are accurate.
- [ ] Human confirms any external announcements, demos, or posts before they are published.

## 6. After Release

- [ ] Check that the GitHub release page renders correctly.
- [ ] Check that linked issues closed as expected.
- [ ] Add a follow-up issue only for real remaining work.
- [ ] Do not publish another patch release unless there is a meaningful merged change.
"""


def write_release_checklist(root: Path) -> dict[str, Any]:
    inspection = inspect_relay(root)
    context = detect_repo_context(root)
    relay_root = relay_dir(root)
    target = relay_root / "release-checklist.md"
    write_text(target, render_release_checklist(context, inspection))
    return {**inspection, "release_checklist": str(target)}


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


def cmd_handoff(args: argparse.Namespace) -> int:
    payload = write_handoff(args.root.resolve())
    if args.json:
        print_json(payload)
    else:
        print(f"Relay handoff written to {payload['handoff']}")
        print(f"Verdict: {payload['verdict']}")
    return 0


def cmd_pr_comment(args: argparse.Namespace) -> int:
    payload = write_pr_comment(args.root.resolve(), base_ref=args.base_ref)
    if args.json:
        print_json(payload)
    else:
        print(f"Relay PR comment written to {payload['pr_comment']}")
        print(f"Verdict: {payload['verdict']}")
    return 0


def cmd_review_readiness(args: argparse.Namespace) -> int:
    payload = write_review_readiness(args.root.resolve(), base_ref=args.base_ref)
    if args.json:
        print_json(payload)
    else:
        print(f"Relay review readiness written to {payload['review_readiness_artifact']}")
        print(f"Changed files: {payload['review_readiness']['changed_file_count']}")
    return 0


def cmd_reviewer_pack(args: argparse.Namespace) -> int:
    payload = write_reviewer_pack(args.root.resolve(), base_ref=args.base_ref)
    if args.json:
        print_json(payload)
    else:
        print(f"Relay reviewer pack written to {payload['reviewer_pack']}")
        print(f"Verdict: {payload['verdict']}")
    return 0


def cmd_validation_brief(args: argparse.Namespace) -> int:
    payload = write_validation_brief(args.root.resolve(), base_ref=args.base_ref)
    if args.json:
        print_json(payload)
    else:
        print(f"Relay validation brief written to {payload['validation_brief']}")
        print(f"Verdict: {payload['verdict']}")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    payload = write_release_checklist(args.root.resolve())
    if args.json:
        print_json(payload)
    else:
        print(f"Relay release checklist written to {payload['release_checklist']}")
        print(f"Verdict: {payload['verdict']}")
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
        ("handoff", cmd_handoff),
        ("review-readiness", cmd_review_readiness),
        ("pr-comment", cmd_pr_comment),
        ("reviewer-pack", cmd_reviewer_pack),
        ("validation-brief", cmd_validation_brief),
        ("release", cmd_release),
        ("automations", cmd_automations),
        ("hook-posttooluse", cmd_hook),
    ):
        command = subparsers.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--base-ref", default=None)
        command.add_argument("--json", action="store_true")
        command.set_defaults(func=handler)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
