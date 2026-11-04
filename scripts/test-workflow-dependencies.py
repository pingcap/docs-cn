"""Test dependency integrity controls in maintenance workflows."""

import os
from http.client import IncompleteRead
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parents[1]
# media.yml is covered by the separate media workflow hardening change.
WORKFLOW_NAMES = [
    "flush.yaml",
    "flush-version.yaml",
    "link.yaml",
    "link-fail-fast.yaml",
    "keywords.yaml",
]


class WorkflowDependencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflows = {
            name: yaml.safe_load((ROOT / ".github/workflows" / name).read_text())
            for name in WORKFLOW_NAMES
        }

    def test_actions_are_pinned_to_commits(self):
        for name, workflow in self.workflows.items():
            for job in workflow["jobs"].values():
                for step in job["steps"]:
                    if "uses" in step:
                        with self.subTest(workflow=name, action=step["uses"]):
                            reference = step["uses"].rsplit("@", 1)[-1]
                            self.assertRegex(reference, r"^[0-9a-f]{40}$")

    def test_flush_uses_reviewed_repository_list(self):
        workflow = self.workflows["flush.yaml"]
        job = workflow["jobs"]["flush-pdf"]
        steps = {step["name"]: step for step in job["steps"]}
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertIn("resources/cdnfresh.txt", steps["Print PDF list"]["run"])
        all_scripts = "\n".join(step.get("run", "") for step in job["steps"])
        self.assertNotIn("raw.githubusercontent.com", all_scripts)
        self.assertNotIn("TENCENTCLOUD_SECRET_ID", job.get("env", {}))
        self.assertIn("TENCENTCLOUD_SECRET_ID", steps["Refresh URLs"]["env"])

    def test_tccli_versions_are_pinned(self):
        for name in ["flush.yaml", "flush-version.yaml"]:
            job = self.workflows[name]["jobs"]["flush-pdf"]
            install = next(
                step for step in job["steps"]
                if step.get("name") == "Install Tencent Cloud CLI"
            )
            self.assertEqual(install["run"], "pip3 install tccli==3.1.194.1")

    def test_link_policy_stays_in_repository(self):
        workflow = self.workflows["link.yaml"]
        scripts = "\n".join(
            step.get("run", "") for step in workflow["jobs"]["linkChecker"]["steps"]
        )
        self.assertTrue((ROOT / ".lycheeignore").is_file())
        self.assertNotIn("raw.githubusercontent.com", scripts)
        self.assertNotIn("Download Exclude Path", scripts)

    def test_link_issue_write_permission_is_isolated(self):
        workflow = self.workflows["link.yaml"]
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertEqual(
            workflow["jobs"]["linkChecker"]["permissions"],
            {"contents": "read"},
        )
        self.assertEqual(
            workflow["jobs"]["createIssue"]["permissions"],
            {"actions": "read", "contents": "read", "issues": "write"},
        )

    def test_keywords_has_no_runtime_package_install(self):
        workflow = self.workflows["keywords.yaml"]
        scripts = "\n".join(
            step.get("run", "")
            for step in workflow["jobs"]["check-keywords"]["steps"]
        )
        self.assertNotIn("pip install", scripts)
        self.assertIn("git ls-remote", scripts)
        self.assertIn("${parser_sha}", scripts)
        self.assertIn(
            'git show "refs/remotes/origin/${branch}:keywords.md"', scripts
        )
        self.assertIn('${branch}.reason', scripts)
        self.assertIn('${branch}.parser-sha', scripts)
        self.assertIn('blob/${parser_sha}/pkg/parser/parser.y', scripts)
        self.assertNotIn('git checkout "$branch"', scripts)

    def run_keyword_download_with_response(self, response):
        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory(prefix="keyword-charset-test-") as directory:
            try:
                os.chdir(directory)
                with (
                    mock.patch(
                        "urllib.request.urlopen"
                    ) as mocked_urlopen,
                    mock.patch.object(
                        sys,
                        "argv",
                        [
                            "check-keywords.py",
                            "--download_from_url",
                            "--parser_url",
                            "https://example.invalid/parser.y",
                        ],
                    ),
                    self.assertRaises(SystemExit) as exit_context,
                ):
                    mocked_urlopen.return_value.__enter__.return_value = response
                    runpy.run_path(str(ROOT / "scripts/check-keywords.py"))
            finally:
                os.chdir(original_directory)

        return str(exit_context.exception)

    def test_keyword_download_handles_unknown_charset(self):
        response = mock.MagicMock()
        response.headers.get_content_charset.return_value = "unknown-charset"
        response.read.return_value = b"parser content"

        error = self.run_keyword_download_with_response(response)
        self.assertIn("Failed to download parser file", error)
        self.assertIn("unknown encoding", error)

    def test_keyword_download_handles_transport_errors(self):
        for transport_error in [
            IncompleteRead(b"partial", 20),
            ConnectionResetError("connection reset"),
        ]:
            with self.subTest(error=type(transport_error).__name__):
                response = mock.MagicMock()
                response.headers.get_content_charset.return_value = "utf-8"
                response.read.side_effect = transport_error

                error = self.run_keyword_download_with_response(response)
                self.assertIn("Failed to download parser file", error)

    def test_keyword_download_uses_standard_library(self):
        with tempfile.TemporaryDirectory(prefix="keyword-download-test-") as directory:
            workdir = Path(directory)
            parser_file = workdir / "parser.y"
            parser_file.write_text(
                'The following tokens belong to ReservedKeyword\n\tselect "SELECT"\n'
            )
            (workdir / "keywords.md").write_text("- SELECT (R)\n")
            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/check-keywords.py"),
                    "--download_from_url",
                    "--parser_url",
                    parser_file.as_uri(),
                ],
                cwd=workdir,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
