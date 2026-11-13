"""Test actor guards on write-privileged workflows that consume secrets."""

import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_workflow(workflow_name):
    """Load a workflow without evaluating any GitHub expressions."""
    workflow_path = ROOT / ".github/workflows" / workflow_name
    return yaml.safe_load(workflow_path.read_text())


def load_job(workflow_name, job_name):
    """Load a job definition from a workflow."""
    return load_workflow(workflow_name)["jobs"][job_name]


class PrivilegedWorkflowActorTest(unittest.TestCase):
    def test_gate_checks_current_permission_and_rerun_initiator(self):
        gate = load_job("authorize-privileged-workflow.yml", "authorize")["steps"][0]
        mock_api = """
gh() {
    case "$2" in
        */attempts/2)
            printf '{"triggering_actor":{"login":"rerunner","id":%s}}' "$RERUN_ID"
            ;;
        */collaborators/renamed/permission)
            printf '{"user":{"id":%s},"permission":"%s"}' "$API_ID" "$ROLE"
            ;;
        */collaborators/rerunner/permission)
            printf '{"user":{"id":%s},"permission":"%s"}' "$RERUN_ID" "$RERUN_ROLE"
            ;;
        *) return 1 ;;
    esac
}
"""
        cases = (
            ("authorized renamed commenter", {}, True),
            ("public commenter", {"ACTOR_ID": "42", "COMMENT_AUTHOR_ID": "42"}, False),
            ("read-only allowlisted account", {
                "ACTOR_ID": "47792576", "COMMENT_AUTHOR_ID": "47792576",
                "API_ID": "47792576", "ROLE": "read",
            }, False),
            ("reassigned login", {"API_ID": "42"}, False),
            ("different comment author", {"COMMENT_AUTHOR_ID": "42"}, False),
            ("non-master dispatch", {
                "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/test",
            }, False),
            ("first scheduled run", {"GITHUB_EVENT_NAME": "schedule", "ACTOR_ID": "42"}, True),
            ("authorized rerun", {"GITHUB_RUN_ATTEMPT": "2"}, True),
            ("unauthorized rerun", {"GITHUB_RUN_ATTEMPT": "2", "RERUN_ROLE": "read"}, False),
            ("original actor loses access", {"GITHUB_RUN_ATTEMPT": "2", "ROLE": "read"}, False),
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            for name, overrides, allowed in cases:
                with self.subTest(case=name):
                    output.write_text("")
                    env = {
                        **os.environ,
                        "GITHUB_REPOSITORY": "pingcap/docs-cn",
                        "GITHUB_REF": "refs/heads/master",
                        "GITHUB_EVENT_NAME": "issue_comment",
                        "GITHUB_ACTOR": "renamed",
                        "GITHUB_RUN_ID": "123",
                        "GITHUB_RUN_ATTEMPT": "1",
                        "GITHUB_OUTPUT": str(output),
                        "ACTOR_ID": "30922556",
                        "COMMENT_AUTHOR_ID": "30922556",
                        "API_ID": "30922556",
                        "ROLE": "admin",
                        "RERUN_ID": "79440533",
                        "RERUN_ROLE": "write",
                        **overrides,
                    }
                    result = subprocess.run(
                        ["bash", "-c", mock_api + gate["run"]],
                        env=env,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode == 0, allowed, result.stderr)
                    expected = f"attempt={env['GITHUB_RUN_ATTEMPT']}\n" if allowed else ""
                    self.assertEqual(output.read_text(), expected)

    def test_privileged_jobs_require_the_shared_authorization_workflow(self):
        for filename, job_name in (
            ("doc_review.yml", "review"),
            ("sync-ai-docs-en-to-zh.yml", "translate"),
            ("sync-doc-pr-en-to-zh.yml", "sync-docs"),
            ("flush.yaml", "flush-pdf"),
            ("flush-version.yaml", "flush-pdf"),
        ):
            with self.subTest(workflow=filename):
                workflow = load_workflow(filename)
                gate = workflow["jobs"]["authorize"]
                self.assertEqual(
                    gate["uses"],
                    "./.github/workflows/authorize-privileged-workflow.yml",
                )
                self.assertEqual(gate["permissions"], {"actions": "read"})
                self.assertNotIn("secrets", gate)
                self.assertEqual(workflow["jobs"][job_name]["needs"], "authorize")
                self.assertEqual(
                    workflow["jobs"][job_name]["if"],
                    "needs.authorize.outputs.attempt == github.run_attempt",
                )

    def test_ai_sync_keeps_concurrency_scoped_to_translation(self):
        workflow = load_workflow("sync-ai-docs-en-to-zh.yml")
        self.assertNotIn("concurrency", workflow)
        self.assertEqual(
            workflow["jobs"]["translate"]["concurrency"],
            {"group": "sync-ai-docs-en-to-zh", "cancel-in-progress": True},
        )

    def test_ci_uses_read_only_repository_permissions(self):
        permissions = load_workflow("ci.yaml")["permissions"]
        self.assertEqual(permissions, {"contents": "read"})


if __name__ == "__main__":
    unittest.main()
