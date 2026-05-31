#!/usr/bin/env python3
"""Run Relay artifact generation against a fixture without dirtying the repo."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_COMMANDS = (
    "review-readiness",
    "handoff",
    "pr-comment",
    "reviewer-pack",
    "validation-brief",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Relay validation bundle from a copied fixture.",
    )
    parser.add_argument(
        "--fixture",
        default="tests/fixtures/stuck-repo",
        help="Fixture repo to copy before running artifact generation.",
    )
    parser.add_argument(
        "--runtime",
        default="plugins/relay-codex/scripts/relay_runtime.py",
        help="Relay runtime script path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    fixture = (repo_root / args.fixture).resolve()
    runtime = (repo_root / args.runtime).resolve()

    if not fixture.is_dir():
        print(f"Fixture not found: {fixture}", file=sys.stderr)
        return 2
    if not runtime.is_file():
        print(f"Runtime not found: {runtime}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="relay-fixture-") as temp_dir:
        workspace = Path(temp_dir) / fixture.name
        shutil.copytree(fixture, workspace)
        print(f"Copied fixture to {workspace}", flush=True)

        for command in DEFAULT_COMMANDS:
            print(f"Generating {command}", flush=True)
            subprocess.run(
                [
                    sys.executable,
                    str(runtime),
                    command,
                    "--root",
                    str(workspace),
                    "--json",
                ],
                cwd=repo_root,
                check=True,
            )

    print("Fixture bundle smoke test passed without modifying the source fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
