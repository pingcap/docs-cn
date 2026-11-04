"""Test that local tooling installs only reviewed, locked dependencies."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallScriptTest(unittest.TestCase):
    def test_obsolete_bootstrap_scripts_are_removed(self):
        self.assertFalse((ROOT / "scripts/build.sh").exists())
        self.assertFalse((ROOT / "scripts/check_requirement.sh").exists())

    def test_markdownlint_is_an_exact_development_dependency(self):
        package = json.loads((ROOT / "package.json").read_text())
        self.assertEqual(package["devDependencies"]["markdownlint-cli"], "0.44.0")

    def test_markdownlint_is_locked_with_integrity(self):
        package = json.loads((ROOT / "package.json").read_text())
        lock = json.loads((ROOT / "package-lock.json").read_text())
        dependency = lock["packages"]["node_modules/markdownlint-cli"]
        self.assertEqual(dependency["version"], "0.44.0")
        self.assertTrue(dependency["integrity"].startswith("sha512-"))
        self.assertEqual(package["overrides"]["run-con"], "1.3.2")
        run_con = lock["packages"]["node_modules/markdownlint-cli/node_modules/run-con"]
        ini = lock["packages"]["node_modules/markdownlint-cli/node_modules/ini"]
        self.assertEqual(run_con["version"], "1.3.2")
        self.assertEqual(ini["version"], "4.1.3")
        self.assertIn(">=18.0.0", ini["engines"]["node"])

    def test_markdownlint_uses_clean_locked_install(self):
        script = (ROOT / "scripts/markdownlint").read_text()
        self.assertIn("npm ci --ignore-scripts --include=dev || exit 1", script)
        self.assertIn('packages["node_modules/markdownlint-cli"].version', script)
        self.assertIn('node "$program" --version', script)
        self.assertNotIn("npm install", script)
        self.assertNotIn("rm -f package-lock.json", script)

    def test_markdownlint_stops_when_locked_install_fails(self):
        with tempfile.TemporaryDirectory(prefix="markdownlint-install-test-") as directory:
            root = Path(directory)
            scripts = root / "scripts"
            mock_bin = root / "mock-bin"
            local_bin = root / "node_modules/.bin"
            scripts.mkdir()
            mock_bin.mkdir()
            local_bin.mkdir(parents=True)

            shutil.copy(ROOT / "scripts/markdownlint", scripts / "markdownlint")
            (root / "package-lock.json").write_text(
                json.dumps(
                    {
                        "packages": {
                            "node_modules/markdownlint-cli": {"version": "0.44.0"}
                        }
                    }
                )
            )
            old_linter = local_bin / "markdownlint"
            old_linter.write_text("#!/usr/bin/env bash\n")
            old_linter.chmod(0o755)

            mock_node = mock_bin / "node"
            mock_node.write_text(
                """#!/usr/bin/env bash
if [[ "$1" == "-p" ]]; then
  echo "0.44.0"
elif [[ "$2" == "--version" ]]; then
  echo "0.17.0"
else
  touch "$EXEC_MARKER"
fi
"""
            )
            mock_node.chmod(0o755)
            mock_npm = mock_bin / "npm"
            mock_npm.write_text("#!/usr/bin/env bash\nexit 23\n")
            mock_npm.chmod(0o755)

            marker = root / "old-linter-ran"
            result = subprocess.run(
                ["bash", str(scripts / "markdownlint")],
                env={
                    **os.environ,
                    "EXEC_MARKER": str(marker),
                    "PATH": f"{mock_bin}:{os.environ['PATH']}",
                },
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
