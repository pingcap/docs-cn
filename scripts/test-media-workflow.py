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
        cls.stage_step = next(
            step
            for step in cls.upload_job["steps"]
            if step.get("name") == "Stage publishable media"
        )
        cls.upload_step = next(
            step for step in cls.upload_job["steps"] if step.get("name") == "Upload to COS"
        )
        cls.purge_step = next(
            step
            for step in cls.refresh_job["steps"]
            if step.get("name") == "Purge production CDN cache"
        )

    def test_workflow_has_read_only_repository_access(self):
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_credentialed_runs_use_an_explicit_branch_allowlist(self):
        trigger = self.workflow.get("on", self.workflow.get(True))
        branches = trigger["push"]["branches"]
        self.assertIn("master", branches)
        self.assertNotIn("release-*", branches)
        self.assertNotIn("release-8.5-temp", branches)
        self.assertFalse(any("*" in branch for branch in branches))

    def test_only_publishable_media_is_staged(self):
        stage = self.stage_step["run"]
        for extension in ["gif", "jpeg", "jpg", "png", "svg"]:
            self.assertIn(f"*.{extension}", stage)
        self.assertIn('cp "$media_file" "$destination"', stage)
        self.assertNotIn("TENCENTCLOUD_SECRET", self.stage_step.get("env", {}))
        self.assertIn('sync "$MEDIA_UPLOAD_DIR/"', self.upload_step["run"])
        self.assertNotIn("sync media/", self.upload_step["run"])

    def test_staging_excludes_unsupported_files(self):
        with tempfile.TemporaryDirectory(prefix="media-stage-test-") as directory:
            workdir = Path(directory)
            source = workdir / "media" / "nested"
            destination = workdir / "staged"
            source.mkdir(parents=True)
            (source / "image.PNG").write_bytes(b"image")
            (source / "backup.png.bak").write_bytes(b"backup")

            result = subprocess.run(
                [
                    "bash", "--noprofile", "--norc", "-eo", "pipefail", "-c",
                    self.stage_step["run"],
                ],
                cwd=workdir,
                env={**os.environ, "MEDIA_UPLOAD_DIR": str(destination)},
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "nested" / "image.PNG").is_file())
            self.assertFalse((destination / "nested" / "backup.png.bak").exists())

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
                    "MEDIA_UPLOAD_DIR": str(temp_dir / "media-upload"),
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

    def test_cdn_credentials_are_scoped_to_purge_step(self):
        self.assertNotIn("env", self.refresh_job)
        for name in ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]:
            expression = "${{ secrets." + name + " }}"
            self.assertEqual(self.purge_step["env"][name], expression)
            for step in self.refresh_job["steps"]:
                if step is not self.purge_step:
                    self.assertNotIn(name, step.get("env", {}))


if __name__ == "__main__":
    unittest.main()
