#!/usr/bin/env python3
"""Render the README demo GIF from real Relay runtime output."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as error:  # pragma: no cover - dependency guard for local docs tooling.
    raise SystemExit("Pillow is required to render the demo GIF. Install it with `python3 -m pip install pillow`.") from error


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "plugins" / "relay-codex" / "scripts" / "relay_runtime.py"
FIXTURE = ROOT / "tests" / "fixtures" / "in-progress-repo"
OUTPUT = ROOT / "docs" / "assets" / "relay-demo.gif"

WIDTH = 1280
HEIGHT = 720
MARGIN = 48
TITLE_COLOR = (247, 115, 22)
TEXT_COLOR = (226, 232, 240)
MUTED_COLOR = (148, 163, 184)
PANEL_COLOR = (15, 23, 42)
BG_COLOR = (2, 6, 23)
GREEN = (34, 197, 94)
YELLOW = (250, 204, 21)
BLUE = (56, 189, 248)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(40, bold=True)
FONT_SUBTITLE = font(24)
FONT_MONO = font(22)
FONT_SMALL = font(18)


def run_runtime(workspace: Path, command: str, input_payload: dict[str, str] | None = None) -> dict[str, object]:
    result = subprocess.run(
        ["python3", str(RUNTIME), command, "--root", str(workspace), "--json"],
        input=json.dumps(input_payload) if input_payload is not None else None,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compact_lines(text: str, keep: tuple[str, ...], limit: int = 11) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(token in stripped for token in keep):
            lines.append(stripped)
    return lines[:limit]


def wrap_text(text: str, chars: int = 84) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        if sum(len(part) for part in current) + len(current) + len(word) > chars:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def panel(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(xy, radius=8, fill=PANEL_COLOR, outline=(30, 41, 59), width=2)


def draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y: int,
    line_height: int = 31,
    color: tuple[int, int, int] = TEXT_COLOR,
) -> None:
    for line in lines:
        wrapped = wrap_text(line, chars=78) if len(line) > 78 else [line]
        for wrapped_line in wrapped[:2]:
            draw.text((x, y), wrapped_line, font=FONT_MONO, fill=color)
            y += line_height


def frame(title: str, subtitle: str, body_lines: list[str], accent: tuple[int, int, int] = BLUE) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 10), fill=accent)
    draw.text((MARGIN, 34), title, font=FONT_TITLE, fill=TITLE_COLOR)
    draw.text((MARGIN, 88), subtitle, font=FONT_SUBTITLE, fill=MUTED_COLOR)

    panel(draw, (MARGIN, 138, WIDTH - MARGIN, HEIGHT - 58))
    draw_lines(draw, body_lines, MARGIN + 32, 172)

    draw.text((MARGIN, HEIGHT - 36), "Relay for Codex: repo-local evidence for long-running agent work", font=FONT_SMALL, fill=MUTED_COLOR)
    return image


def build_frames(workspace: Path) -> list[Image.Image]:
    relay_root = workspace / ".relay"
    state = read(relay_root / "state.md")
    handoff = read(relay_root / "handoff.md")
    release = read(relay_root / "release-checklist.md")

    state_lines = compact_lines(
        state,
        ("Verdict", "Phase", "Recent activity", "Current Signals"),
    )
    handoff_lines = compact_lines(
        handoff,
        ("Current verdict", "Last Successful Signal", "Updated the dashboard", "Review Checklist", "npm run test", "Suggested Next Action"),
    )
    release_lines = compact_lines(
        release,
        ("Current verdict", "Release Posture", "npm run test", "git status --short", "Human confirms", "Release can proceed"),
    )

    return [
        frame(
            "1. Relay checks repo state",
            "Codex Goals track the thread. Relay writes the repo-local evidence.",
            [
                "$ python3 plugins/relay-codex/scripts/relay_runtime.py enable --json",
                "",
                ".relay/",
                "  mission.md",
                "  state.md",
                "  queue.md",
                "  guardrails.md",
                "  events.jsonl",
                "",
                *state_lines,
            ],
            BLUE,
        ),
        frame(
            "2. Codex does work",
            "The run is recorded as project evidence, not hidden in a chat transcript.",
            [
                "$ relay hook-posttooluse",
                "",
                "tool: Write",
                "summary: Updated the dashboard empty state copy and wired the CTA button.",
                "",
                "$ npm run test",
                "result: verification command is now part of the handoff trail",
            ],
            GREEN,
        ),
        frame(
            "3. Relay generates a PR handoff",
            "A future maintainer or agent can inspect what happened before continuing.",
            [
                "$ python3 plugins/relay-codex/scripts/relay_runtime.py handoff",
                "",
                ".relay/handoff.md",
                "",
                *handoff_lines,
            ],
            TITLE_COLOR,
        ),
        frame(
            "4. Release stays gated",
            "Relay helps ship carefully: tests, clean tree, release notes, approval.",
            [
                "$ python3 plugins/relay-codex/scripts/relay_runtime.py release",
                "",
                ".relay/release-checklist.md",
                "",
                *release_lines,
            ],
            YELLOW,
        ),
        frame(
            "Relay for Codex",
            "Not a runtime. Not a kanban board. A repo-local flight recorder.",
            [
                "Use Relay when long-running Codex work needs:",
                "",
                "- a current continue / recover / review / release verdict",
                "- a maintainer-readable PR handoff",
                "- release gates with human approval",
                "- evidence that survives thread, provider, or harness changes",
                "",
                "Before Codex keeps going, Relay tells you whether it should.",
            ],
            TITLE_COLOR,
        ),
    ]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="relay-demo-") as temp:
        workspace = Path(temp) / "demo-repo"
        shutil.copytree(FIXTURE, workspace)
        run_runtime(workspace, "enable")
        run_runtime(
            workspace,
            "hook-posttooluse",
            {"tool_name": "Write", "summary": "Updated the dashboard empty state copy and wired the CTA button."},
        )
        run_runtime(workspace, "handoff")
        run_runtime(workspace, "release")

        frames = build_frames(workspace)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=[2600, 2300, 3000, 3000, 3200],
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
