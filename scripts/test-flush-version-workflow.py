"""Test input handling in the privileged PDF flush workflow."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/flush-version.yaml"


class FlushVersionWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        workflow = yaml.safe_load(WORKFLOW.read_text())
        cls.workflow = workflow
        cls.job = workflow["jobs"]["flush-pdf"]
        cls.steps = {step["name"]: step for step in cls.job["steps"]}

    def run_script(self, script, env, directory):
        return subprocess.run(
            ["bash", "--noprofile", "--norc", "-euo", "pipefail", "-c", script],
            cwd=directory,
            env={**os.environ, **env},
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_workflow_has_no_token_permissions(self):
        self.assertEqual(self.workflow["permissions"], {})

    def test_version_is_passed_as_data(self):
        for step in self.job["steps"]:
            self.assertNotIn("${{ inputs.version }}", step.get("run", ""))
            self.assertNotIn("${{inputs.version}}", step.get("run", ""))

        for name in [
            "Validate version",
            "Print PDF to a file (tidb)",
            "Print PDF to a file (tidb operator)",
        ]:
            self.assertEqual(self.steps[name]["env"]["VERSION"], "${{ inputs.version }}")

    def test_version_validation(self):
        script = self.steps["Validate version"]["run"]
        cases = [
            ("tidb", "dev", True),
            ("tidb", "v6.5", True),
            ("tidb operator", "v1.6.4", True),
            ("tidb cloud", "", True),
            ("tidb", "", False),
            ("tidb", "6.5", False),
            ("tidb", "v6", False),
            ("tidb operator", "v1.6.4-rc.1", False),
        ]
        with tempfile.TemporaryDirectory(prefix="flush-version-test-") as directory:
            for document_type, version, succeeds in cases:
                with self.subTest(document_type=document_type, version=version):
                    result = self.run_script(
                        script,
                        {"DOCUMENT_TYPE": document_type, "VERSION": version},
                        directory,
                    )
                    self.assertEqual(result.returncode == 0, succeeds, result.stderr)

    def test_malicious_version_is_not_executed(self):
        validation = self.steps["Validate version"]["run"]
        print_steps = [
            self.steps["Print PDF to a file (tidb)"],
            self.steps["Print PDF to a file (tidb operator)"],
        ]
        payloads = [
            "v1.0$(touch${IFS}MARKER)",
            "v1.0`touch${IFS}MARKER`",
            'v1.0"; touch MARKER; #',
        ]

        for payload in payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory(
                prefix="flush-version-test-"
            ) as directory:
                marker = Path(directory) / "MARKER"
                result = self.run_script(
                    validation,
                    {"DOCUMENT_TYPE": "tidb", "VERSION": payload},
                    directory,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(marker.exists())

                for step in print_steps:
                    result = self.run_script(
                        step["run"],
                        {"CDN_BASE_URL": "https://example.com", "VERSION": payload},
                        directory,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(marker.exists())

    def test_cloud_credentials_are_step_scoped(self):
        self.assertNotIn("TENCENTCLOUD_SECRET_ID", self.job.get("env", {}))
        self.assertNotIn("TENCENTCLOUD_SECRET_KEY", self.job.get("env", {}))
        refresh_env = self.steps["Refresh URLs"]["env"]
        self.assertEqual(
            refresh_env["TENCENTCLOUD_SECRET_ID"],
            "${{ secrets.TENCENTCLOUD_SECRET_ID }}",
        )
        self.assertEqual(
            refresh_env["TENCENTCLOUD_SECRET_KEY"],
            "${{ secrets.TENCENTCLOUD_SECRET_KEY }}",
        )


if __name__ == "__main__":
    unittest.main()
