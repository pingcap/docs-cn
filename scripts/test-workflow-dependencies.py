"""Test dependency integrity controls in maintenance workflows."""

import os
from http.client import IncompleteRead
from pathlib import Path
import re
import runpy
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIRECTORY = ROOT / ".github/workflows"
WORKFLOW_NAMES = sorted(
    path.name
    for pattern in ("*.yml", "*.yaml")
    for path in WORKFLOW_DIRECTORY.glob(pattern)
)


class WorkflowDependencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflows = {
            name: yaml.safe_load((WORKFLOW_DIRECTORY / name).read_text())
            for name in WORKFLOW_NAMES
        }

    def test_actions_are_pinned_to_commits(self):
        for name, workflow in self.workflows.items():
            for job in workflow["jobs"].values():
                references = [job["uses"]] if "uses" in job else []
                references.extend(
                    step["uses"] for step in job.get("steps", []) if "uses" in step
                )
                for action in references:
                    if action.startswith("./"):
                        continue
                    with self.subTest(workflow=name, action=action):
                        self.assertIn("@", action)
                        reference = action.rsplit("@", 1)[-1]
                        self.assertRegex(reference, r"^[0-9a-f]{40}$")

    def test_sync_and_review_checkouts_do_not_persist_credentials(self):
        for name, job_name in (
            ("sync-ai-docs-en-to-zh.yml", "translate"),
            ("doc_review.yml", "review"),
        ):
            steps = self.workflows[name]["jobs"][job_name]["steps"]
            checkouts = [
                step for step in steps
                if step.get("uses", "").startswith("actions/checkout@")
            ]
            self.assertTrue(checkouts, name)
            for step in checkouts:
                with self.subTest(workflow=name, step=step.get("name")):
                    self.assertIs(step.get("with", {}).get("persist-credentials"), False)

    def test_scheduled_sync_reads_lock_from_workflow_commit(self):
        steps = self.workflows["sync-ai-docs-en-to-zh.yml"]["jobs"]["translate"]["steps"]
        lock_file = "scripts/ai-translator-requirements.lock"
        lock_checkout = next(
            step for step in steps if step.get("name") == "Checkout translation dependency lock"
        )
        checkout = lock_checkout["with"]
        self.assertTrue(lock_checkout["uses"].startswith("actions/checkout@"))
        self.assertNotIn("repository", checkout)
        self.assertEqual(checkout["ref"], "${{ github.sha }}")
        self.assertEqual(checkout["path"], "workflow-dependencies")
        self.assertEqual(checkout["sparse-checkout"], lock_file)
        self.assertIs(checkout["sparse-checkout-cone-mode"], False)

        lock_path = f"{checkout['path']}/{lock_file}"
        setup = next(step for step in steps if step.get("name") == "Setup Python")
        install = next(step for step in steps if step.get("name") == "Install dependencies")
        self.assertLess(steps.index(lock_checkout), steps.index(setup))
        self.assertLess(steps.index(setup), steps.index(install))
        self.assertEqual(setup["with"]["cache-dependency-path"], lock_path)
        install_args = shlex.split(install["run"].replace("\\\n", " "))
        self.assertEqual(install_args[install_args.index("-r") + 1], lock_path)

    def test_translation_dependencies_are_locked_and_hashed(self):
        lock_path = ROOT / "scripts/ai-translator-requirements.lock"
        lock_content = lock_path.read_text()
        requirement_lines = [
            line for line in lock_content.splitlines()
            if line and not line.startswith(("#", " "))
        ]
        hash_lines = [
            line.strip() for line in lock_content.splitlines()
            if line.startswith("    --hash=")
        ]
        self.assertTrue(requirement_lines)
        self.assertEqual(len(requirement_lines), len(hash_lines))
        self.assertTrue(
            all(
                "==" in line and line.endswith(" \\")
                for line in requirement_lines
            )
        )
        self.assertTrue(
            all(
                re.fullmatch(r"--hash=sha256:[0-9a-f]{64}", line)
                for line in hash_lines
            )
        )

        for name, job_name in (
            ("sync-ai-docs-en-to-zh.yml", "translate"),
            ("sync-doc-pr-en-to-zh.yml", "sync-docs"),
        ):
            install = next(
                step for step in self.workflows[name]["jobs"][job_name]["steps"]
                if step.get("name") == "Install dependencies"
            )["run"]
            self.assertIn("ai-translator-requirements.lock", install)
            self.assertIn("--require-hashes", install)
            self.assertIn("--only-binary=:all:", install)
            self.assertNotIn("pip install --upgrade pip", install)
            self.assertNotIn("ai-markdown-translator/scripts/requirements.txt", install)

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
