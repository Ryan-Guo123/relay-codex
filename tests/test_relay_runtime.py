from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "plugins" / "relay-codex" / "scripts" / "relay_runtime.py"
FIXTURES = ROOT / "tests" / "fixtures"


class RelayRuntimeTests(unittest.TestCase):
    def copy_fixture(self, name: str) -> Path:
        temp_root = Path(tempfile.mkdtemp(prefix="relay-runtime-"))
        fixture = FIXTURES / name
        workspace = temp_root / name
        workspace.mkdir(parents=True, exist_ok=True)
        shutil.copytree(fixture, workspace, dirs_exist_ok=True)
        self.addCleanup(lambda: shutil.rmtree(temp_root, ignore_errors=True))
        return workspace

    def run_runtime(self, workspace: Path, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(RUNTIME), *args, "--root", str(workspace), "--json"],
            input=input_text,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_enable_creates_relay_files(self) -> None:
        workspace = self.copy_fixture("empty-repo")
        result = self.run_runtime(workspace, "enable")
        payload = json.loads(result.stdout)
        relay_root = workspace / ".relay"
        for name in ("mission.md", "state.md", "queue.md", "guardrails.md", "automations.md", "events.jsonl"):
            self.assertTrue((relay_root / name).exists(), name)
        self.assertIn("mission.md", payload["created"])
        self.assertIn("empty-repo", (relay_root / "mission.md").read_text(encoding="utf-8"))

    def test_hook_records_event_and_keeps_continue_verdict(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        self.run_runtime(workspace, "enable")
        hook_payload = json.dumps(
            {
                "tool_name": "Write",
                "summary": "Updated the dashboard empty state copy and wired the CTA button.",
            }
        )
        hook_result = self.run_runtime(workspace, "hook-posttooluse", input_text=hook_payload)
        hook_json = json.loads(hook_result.stdout)
        self.assertTrue(hook_json["updated"])
        self.assertEqual(hook_json["verdict"], "continue")
        events = (workspace / ".relay" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(events), 1)

    def test_stuck_repo_is_flagged_for_review(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        inspect_result = self.run_runtime(workspace, "inspect")
        payload = json.loads(inspect_result.stdout)
        self.assertEqual(payload["verdict"], "needs_review")
        self.assertTrue(any("failure" in reason.lower() or "test-only" in reason.lower() for reason in payload["reasons"]))

    def test_recover_rewrites_queue(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        recover_result = self.run_runtime(workspace, "recover")
        payload = json.loads(recover_result.stdout)
        queue = (workspace / ".relay" / "queue.md").read_text(encoding="utf-8")
        self.assertEqual(payload["verdict"], "needs_review")
        self.assertIn("Recovery Tasks", queue)
        self.assertIn("Restate the last successful change", queue)

    def test_handoff_writes_maintainer_summary(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        handoff_result = self.run_runtime(workspace, "handoff")
        payload = json.loads(handoff_result.stdout)
        handoff_path = Path(payload["handoff"])
        handoff = handoff_path.read_text(encoding="utf-8")
        self.assertTrue(handoff_path.exists())
        self.assertEqual(payload["verdict"], "needs_review")
        self.assertIn("# Relay Handoff", handoff)
        self.assertIn("## Last Successful Signal", handoff)
        self.assertIn("pytest failed with error", handoff)
        self.assertIn("Do not continue automatically", handoff)

    def test_release_writes_checklist_with_approval_gates(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        release_result = self.run_runtime(workspace, "release")
        payload = json.loads(release_result.stdout)
        checklist_path = Path(payload["release_checklist"])
        checklist = checklist_path.read_text(encoding="utf-8")
        self.assertTrue(checklist_path.exists())
        self.assertIn("# Relay Release Checklist", checklist)
        self.assertIn("## 2. Verification", checklist)
        self.assertIn("Run `npm run test`", checklist)
        self.assertIn("## 5. Human Approval Gates", checklist)
        self.assertIn("Human confirms this release should be public", checklist)

    def test_automation_packs_are_rendered(self) -> None:
        workspace = self.copy_fixture("empty-repo")
        packs_result = self.run_runtime(workspace, "automations")
        payload = json.loads(packs_result.stdout)
        names = [pack["name"] for pack in payload["packs"]]
        self.assertEqual(names, ["Continue Working", "Daily Triage", "Stuck Recovery", "Release Readiness"])
        automations_doc = (workspace / ".relay" / "automations.md").read_text(encoding="utf-8")
        self.assertIn("Daily Triage", automations_doc)

    def test_generated_artifacts_keep_protocol_headings(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        self.run_runtime(workspace, "enable")
        self.run_runtime(workspace, "handoff")
        self.run_runtime(workspace, "release")

        relay_root = workspace / ".relay"
        expected = {
            "mission.md": ("# Relay Mission", "## Success Definition", "## Observed Context", "## Human Notes"),
            "state.md": ("# Relay State", "## Recent Progress", "## Current Signals"),
            "queue.md": ("# Relay Queue", "## Next Tasks", "## Why Relay Chose This"),
            "guardrails.md": ("# Relay Guardrails", "## Escalation Rules"),
            "automations.md": ("# Relay Automation Packs", "## Continue Working", "## Daily Triage", "## Stuck Recovery", "## Release Readiness"),
            "handoff.md": ("# Relay Handoff", "## Maintainer Summary", "## Recommended Next Action", "## Safe Handoff Rules"),
            "release-checklist.md": ("# Relay Release Checklist", "## Release Posture", "## 2. Verification", "## 5. Human Approval Gates"),
        }
        for filename, headings in expected.items():
            content = (relay_root / filename).read_text(encoding="utf-8")
            for heading in headings:
                self.assertIn(heading, content, f"{filename} missing {heading}")

        first_event = (relay_root / "events.jsonl").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("timestamp", json.loads(first_event))


if __name__ == "__main__":
    unittest.main()
