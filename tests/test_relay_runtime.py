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

    def test_automation_packs_are_rendered(self) -> None:
        workspace = self.copy_fixture("empty-repo")
        packs_result = self.run_runtime(workspace, "automations")
        payload = json.loads(packs_result.stdout)
        names = [pack["name"] for pack in payload["packs"]]
        self.assertEqual(names, ["Continue Working", "Daily Triage", "Stuck Recovery"])
        automations_doc = (workspace / ".relay" / "automations.md").read_text(encoding="utf-8")
        self.assertIn("Daily Triage", automations_doc)


if __name__ == "__main__":
    unittest.main()
