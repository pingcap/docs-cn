"""Test that local tooling installs only reviewed, locked dependencies."""

import json
from pathlib import Path
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
        lock = json.loads((ROOT / "package-lock.json").read_text())
        dependency = lock["packages"]["node_modules/markdownlint-cli"]
        self.assertEqual(dependency["version"], "0.44.0")
        self.assertTrue(dependency["integrity"].startswith("sha512-"))

    def test_markdownlint_uses_clean_locked_install(self):
        script = (ROOT / "scripts/markdownlint").read_text()
        self.assertIn("npm ci --ignore-scripts", script)
        self.assertNotIn("npm install", script)
        self.assertNotIn("rm -f package-lock.json", script)


if __name__ == "__main__":
    unittest.main()
