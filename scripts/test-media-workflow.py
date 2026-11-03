"""Check that the media workflow pins tools and keeps credentials out of argv."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/media.yml"


class MediaWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text())
        cls.upload_job = cls.workflow["jobs"]["upload"]
        cls.refresh_job = cls.workflow["jobs"]["cdn-refresh"]
        cls.install_step = next(
            step for step in cls.upload_job["steps"] if step.get("name") == "Install coscli"
        )
        cls.upload_step = next(
            step for step in cls.upload_job["steps"] if step.get("name") == "Upload to COS"
        )

    def test_workflow_has_read_only_repository_access(self):
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_actions_are_pinned_to_commits(self):
        for job in self.workflow["jobs"].values():
            for step in job["steps"]:
                if "uses" in step:
                    reference = step["uses"].rsplit("@", 1)[-1]
                    self.assertRegex(reference, r"^[0-9a-f]{40}$")

    def test_coscli_release_and_checksum_are_pinned(self):
        job_env = self.upload_job["env"]
        self.assertNotIn("COSCLI_PATH", job_env)
        self.assertEqual(job_env["COSCLI_VERSION"], "1.0.8")
        self.assertEqual(
            job_env["COSCLI_SHA256"],
            "7165f2ae16c5f7ac495864c963ca574a76e04ec72680d7bc8a8eee3234d8cf91",
        )
        install = self.install_step["run"]
        self.assertIn("releases/download/v${COSCLI_VERSION}", install)
        self.assertIn("curl --fail", install)
        self.assertIn("sha256sum --check", install)
        self.assertNotIn("cosbrowser.cloud.tencent.com/software/coscli", install)

    def test_runner_path_is_scoped_to_steps(self):
        expected = "${{ runner.temp }}/coscli"
        self.assertEqual(self.install_step["env"]["COSCLI_PATH"], expected)
        self.assertEqual(self.upload_step["env"]["COSCLI_PATH"], expected)

    def test_cos_credentials_are_scoped_to_upload_step(self):
        for name in ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]:
            expression = "${{ secrets." + name + " }}"
            self.assertEqual(self.upload_step["env"][name], expression)
            self.assertNotIn(name, self.install_step.get("env", {}))
            self.assertNotIn(expression, self.upload_step["run"])

    def test_cos_credentials_are_not_command_arguments(self):
        upload = self.upload_step["run"]
        self.assertNotIn("--secret-id", upload)
        self.assertNotIn("--secret-key", upload)
        self.assertIn('--config-path "$COSCLI_CONFIG"', upload)
        self.assertIn("0o600", upload)
        self.assertIn("trap 'rm -f", upload)

    def test_upload_uses_and_removes_private_config(self):
        with tempfile.TemporaryDirectory(prefix="media-workflow-test-") as directory:
            temp_dir = Path(directory)
            mock_coscli = temp_dir / "coscli"
            result_file = temp_dir / "result"
            mock_coscli.write_text(
                """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import stat
import sys

assert "--secret-id" not in sys.argv
assert "--secret-key" not in sys.argv
config_path = Path(sys.argv[sys.argv.index("--config-path") + 1])
config = json.loads(config_path.read_text())
assert config["cos"]["base"]["secretid"] == "dummy-id"
assert config["cos"]["base"]["secretkey"] == "dummy-key"
assert stat.S_IMODE(config_path.stat().st_mode) == 0o600
Path(os.environ["MOCK_RESULT"]).write_text(str(config_path))
"""
            )
            mock_coscli.chmod(0o755)

            result = subprocess.run(
                [
                    "bash", "--noprofile", "--norc", "-eo", "pipefail", "-c",
                    self.upload_step["run"],
                ],
                cwd=temp_dir,
                env={
                    **os.environ,
                    "COSCLI_PATH": str(mock_coscli),
                    "MOCK_RESULT": str(result_file),
                    "RUNNER_TEMP": str(temp_dir),
                    "TENCENTCLOUD_BUCKET_ID": "dummy-bucket",
                    "TENCENTCLOUD_SECRET_ID": "dummy-id",
                    "TENCENTCLOUD_SECRET_KEY": "dummy-key",
                },
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(Path(result_file.read_text()).exists())

    def test_tccli_version_is_pinned(self):
        install = next(
            step for step in self.refresh_job["steps"]
            if step.get("name") == "Install Tencent Cloud CLI"
        )
        self.assertEqual(install["run"], "pipx install tccli==3.1.194.1")


if __name__ == "__main__":
    unittest.main()
