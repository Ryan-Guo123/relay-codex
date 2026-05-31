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

    def test_pr_comment_writes_github_ready_handoff(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        comment_result = self.run_runtime(workspace, "pr-comment")
        payload = json.loads(comment_result.stdout)
        comment_path = Path(payload["pr_comment"])
        comment = comment_path.read_text(encoding="utf-8")
        self.assertTrue(comment_path.exists())
        self.assertEqual(payload["verdict"], "needs_review")
        self.assertIn("## Relay PR Handoff", comment)
        self.assertIn("### Verification", comment)
        self.assertIn("pytest failed with error", comment)
        self.assertIn("### Risks / Review Focus", comment)
        self.assertIn("Needs maintainer review before another agent pass", comment)
        self.assertIn("does not post this comment automatically", comment)

    def test_pr_comment_omits_relay_artifacts_from_changed_files(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
        (workspace / ".github").mkdir()
        (workspace / ".github" / "CODEOWNERS").write_text(
            "/src/auth/* @security-team\n.github/workflows/* @platform-team\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "package.json", ".github/CODEOWNERS"], cwd=workspace, capture_output=True, text=True, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.email=relay@example.com",
                "-c",
                "user.name=Relay Test",
                "commit",
                "-m",
                "Seed fixture",
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        package_json = workspace / "package.json"
        package_json.write_text(package_json.read_text(encoding="utf-8").replace("in-progress-repo", "relay-pr-test"), encoding="utf-8")
        (workspace / "src").mkdir()
        (workspace / "src" / "app.ts").write_text("export const status = 'ready';\n", encoding="utf-8")
        (workspace / "src" / "auth").mkdir()
        (workspace / "src" / "auth" / "session.ts").write_text("export const token = 'redacted';\n", encoding="utf-8")
        (workspace / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
        (workspace / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
        result = self.run_runtime(workspace, "pr-comment")
        payload = json.loads(result.stdout)

        comment = (workspace / ".relay" / "pr-comment.md").read_text(encoding="utf-8")
        self.assertIn("`package.json`", comment)
        self.assertIn("`src/app.ts`", comment)
        self.assertIn("### Review Readiness", comment)
        self.assertIn("4 non-Relay changed file(s)", comment)
        self.assertIn("`src/auth/session.ts` (Auth / permissions)", comment)
        self.assertIn("`.github/workflows/ci.yml` (CI / automation)", comment)
        self.assertIn("Review routing from `.github/CODEOWNERS`", comment)
        self.assertIn("@security-team: `src/auth/session.ts`", comment)
        self.assertIn("@platform-team: `.github/workflows/ci.yml`", comment)
        self.assertEqual(payload["review_readiness"]["changed_file_count"], 4)
        self.assertEqual(len(payload["review_readiness"]["sensitive_paths"]), 2)
        routing = payload["review_readiness"]["review_routing"]
        self.assertEqual(routing["codeowners_path"], ".github/CODEOWNERS")
        self.assertEqual(
            {entry["owner"] for entry in routing["suggested_reviewers"]},
            {"@platform-team", "@security-team"},
        )
        self.assertNotIn("`ackage.json`", comment)
        self.assertNotIn("`.relay/handoff.md`", comment)
        self.assertNotIn("`.relay/state.md`", comment)

    def test_review_readiness_writes_standalone_gate(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
        (workspace / ".github").mkdir()
        (workspace / ".github" / "CODEOWNERS").write_text(
            "/src/auth/* @security-team\n*.json @tooling-team\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "package.json", ".github/CODEOWNERS"], cwd=workspace, capture_output=True, text=True, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.email=relay@example.com",
                "-c",
                "user.name=Relay Test",
                "commit",
                "-m",
                "Seed fixture",
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        (workspace / "src" / "auth").mkdir(parents=True)
        (workspace / "src" / "auth" / "session.ts").write_text("export const status = 'review';\n", encoding="utf-8")

        result = self.run_runtime(workspace, "review-readiness")
        payload = json.loads(result.stdout)
        artifact = Path(payload["review_readiness_artifact"])
        content = artifact.read_text(encoding="utf-8")

        self.assertTrue(artifact.exists())
        self.assertIn("# Relay Review Readiness", content)
        self.assertIn("## Review Gate", content)
        self.assertIn("## Suggested Reviewers", content)
        self.assertIn("@security-team: `src/auth/session.ts`", content)
        self.assertEqual(payload["review_readiness"]["changed_file_count"], 1)
        self.assertEqual(payload["review_readiness"]["review_routing"]["codeowners_path"], ".github/CODEOWNERS")
        self.assertEqual(payload["review_readiness"]["decision"]["risk_level"], "high")
        self.assertEqual(payload["review_readiness"]["decision"]["decision"], "owner_review_required")

    def test_review_readiness_can_diff_against_base_ref(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        subprocess.run(["git", "init"], cwd=workspace, capture_output=True, text=True, check=True)
        (workspace / ".github").mkdir()
        (workspace / ".github" / "CODEOWNERS").write_text(
            "/src/auth/* @security-team\npackage.json @tooling-team\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "package.json", ".github/CODEOWNERS"], cwd=workspace, capture_output=True, text=True, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.email=relay@example.com",
                "-c",
                "user.name=Relay Test",
                "commit",
                "-m",
                "Seed main",
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(["git", "branch", "main"], cwd=workspace, capture_output=True, text=True, check=True)
        subprocess.run(["git", "switch", "-c", "feature"], cwd=workspace, capture_output=True, text=True, check=True)
        (workspace / "src" / "auth").mkdir(parents=True)
        (workspace / "src" / "auth" / "session.ts").write_text("export const status = 'base-ref';\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/auth/session.ts"], cwd=workspace, capture_output=True, text=True, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.email=relay@example.com",
                "-c",
                "user.name=Relay Test",
                "commit",
                "-m",
                "Add auth session",
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )

        result = self.run_runtime(workspace, "review-readiness", "--base-ref", "main")
        payload = json.loads(result.stdout)
        content = Path(payload["review_readiness_artifact"]).read_text(encoding="utf-8")

        self.assertIn("1 non-Relay changed file(s) against `main`", content)
        self.assertIn("@security-team: `src/auth/session.ts`", content)
        self.assertEqual(payload["review_readiness"]["base_ref"], "main")
        self.assertEqual(payload["review_readiness"]["change_source"], "base_ref_diff")
        self.assertEqual(payload["review_readiness"]["changed_file_count"], 1)
        self.assertEqual(payload["review_readiness"]["decision"]["risk_level"], "high")
        self.assertEqual(payload["review_readiness"]["decision"]["decision"], "owner_review_required")

    def test_reviewer_pack_wraps_pr_comment_and_rubric(self) -> None:
        workspace = self.copy_fixture("stuck-repo")
        pack_result = self.run_runtime(workspace, "reviewer-pack")
        payload = json.loads(pack_result.stdout)
        pack_path = Path(payload["reviewer_pack"])
        pack = pack_path.read_text(encoding="utf-8")
        self.assertTrue(pack_path.exists())
        self.assertEqual(payload["verdict"], "needs_review")
        self.assertIn("# Relay Reviewer Pack", pack)
        self.assertIn("## Reviewer Ask", pack)
        self.assertIn("## Relay Handoff To Review", pack)
        self.assertIn("## Scoring Rubric", pack)
        self.assertIn("Relay handoff feedback", pack)
        self.assertIn("Needs maintainer review before another agent pass", pack)

    def test_changed_files_ignore_parent_repo_when_root_is_nested_fixture(self) -> None:
        workspace = self.copy_fixture("in-progress-repo")
        parent_repo = workspace.parent
        subprocess.run(["git", "init"], cwd=parent_repo, capture_output=True, text=True, check=True)
        (parent_repo / "outside.md").write_text("outside change\n", encoding="utf-8")

        self.run_runtime(workspace, "pr-comment")

        comment = (workspace / ".relay" / "pr-comment.md").read_text(encoding="utf-8")
        self.assertIn("No Git changes detected in the current workspace", comment)
        self.assertNotIn("outside.md", comment)
        self.assertNotIn("../", comment)

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
        self.run_runtime(workspace, "review-readiness")
        self.run_runtime(workspace, "pr-comment")
        self.run_runtime(workspace, "reviewer-pack")
        self.run_runtime(workspace, "release")

        relay_root = workspace / ".relay"
        expected = {
            "mission.md": ("# Relay Mission", "## Success Definition", "## Observed Context", "## Human Notes"),
            "state.md": ("# Relay State", "## Recent Progress", "## Current Signals"),
            "queue.md": ("# Relay Queue", "## Next Tasks", "## Why Relay Chose This"),
            "guardrails.md": ("# Relay Guardrails", "## Escalation Rules"),
            "automations.md": ("# Relay Automation Packs", "## Continue Working", "## Daily Triage", "## Stuck Recovery", "## Release Readiness"),
            "handoff.md": ("# Relay Handoff", "## Maintainer Summary", "## Recommended Next Action", "## Safe Handoff Rules"),
            "review-readiness.md": ("# Relay Review Readiness", "## Review Gate", "## Suggested Reviewers", "## Recommended Review Decision"),
            "pr-comment.md": ("## Relay PR Handoff", "### Current State", "### Review Readiness", "### Verification", "### Recommended Next Action", "### Maintainer Checklist"),
            "reviewer-pack.md": ("# Relay Reviewer Pack", "## Reviewer Ask", "## Scoring Rubric", "## Required Outcome"),
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
