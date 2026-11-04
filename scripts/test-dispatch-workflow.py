"""Test credential and input handling in the docs dispatch workflow."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/dispatch.yml"


class DispatchWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text())
        cls.job = cls.workflow["jobs"]["trigger"]
        cls.step = cls.job["steps"][0]

    def test_workflow_has_no_github_token_permissions(self):
        self.assertEqual(self.workflow["permissions"], {})

    def test_event_data_and_secret_are_passed_through_env(self):
        self.assertEqual(
            self.step["env"]["DOCS_STAGING_TOKEN"], "${{ secrets.DOCS_STAGING }}"
        )
        self.assertEqual(self.step["env"]["SOURCE_BRANCH"], "${{ github.ref_name }}")
        self.assertEqual(
            self.step["env"]["SOURCE_REPOSITORY"], "${{ github.repository }}"
        )
        self.assertNotIn("${{", self.step["run"])

    def test_token_is_not_a_process_argument(self):
        script = self.step["run"]
        self.assertNotIn("--header \"Authorization:", script)
        self.assertNotIn("-H \"Authorization:", script)
        self.assertIn('--config "$CURL_CONFIG"', script)
        self.assertIn("0o600", script)
        self.assertIn("trap 'rm -f", script)

    def test_dispatch_uses_private_files_and_cleans_them_up(self):
        with tempfile.TemporaryDirectory(prefix="dispatch-workflow-test-") as directory:
            workdir = Path(directory)
            mock_curl = workdir / "curl"
            result_file = workdir / "result"
            mock_curl.write_text(
                """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import stat
import sys

assert "dummy-token" not in sys.argv
config_path = Path(sys.argv[sys.argv.index("--config") + 1])
payload_arg = sys.argv[sys.argv.index("--data-binary") + 1]
payload_path = Path(payload_arg[1:])
assert stat.S_IMODE(config_path.stat().st_mode) == 0o600
assert stat.S_IMODE(payload_path.stat().st_mode) == 0o600
assert config_path.read_text() == 'header = "Authorization: Bearer dummy-token"\\n'
assert json.loads(payload_path.read_text()) == {
    "ref": "main",
    "inputs": {"full": "false", "repo": "pingcap/docs-cn", "branch": "master"},
}
Path(os.environ["MOCK_RESULT"]).write_text(f"{config_path}\\n{payload_path}\\n")
"""
            )
            mock_curl.chmod(0o755)

            result = subprocess.run(
                [
                    "bash", "--noprofile", "--norc", "-eo", "pipefail", "-c",
                    self.step["run"],
                ],
                cwd=workdir,
                env={
                    **os.environ,
                    "DOCS_STAGING_TOKEN": "dummy-token",
                    "MOCK_RESULT": str(result_file),
                    "PATH": f"{workdir}:{os.environ['PATH']}",
                    "RUNNER_TEMP": str(workdir),
                    "SOURCE_BRANCH": "master",
                    "SOURCE_REPOSITORY": "pingcap/docs-cn",
                },
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for path in result_file.read_text().splitlines():
                self.assertFalse(Path(path).exists())


if __name__ == "__main__":
    unittest.main()
