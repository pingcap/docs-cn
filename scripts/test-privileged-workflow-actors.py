"""Test actor guards on write-privileged workflows that consume secrets."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_MAINTAINERS = ("lilin90", "qiancai", "seominjea1942")
FORMER_MAINTAINERS = ("hfxsd", "likidu", "Oreoxmt")


def load_job(workflow_name, job_name):
    workflow_path = ROOT / ".github/workflows" / workflow_name
    workflow = yaml.safe_load(workflow_path.read_text())
    return workflow["jobs"][job_name]


class PrivilegedWorkflowActorTest(unittest.TestCase):
    def assert_current_maintainer_guard(self, condition):
        self.assertIn("github.triggering_actor", condition)
        self.assertNotIn("github.actor", condition)
        for login in ACTIVE_MAINTAINERS:
            self.assertIn(login, condition)
        for login in FORMER_MAINTAINERS:
            self.assertNotIn(login, condition)

    def test_doc_review_guards_dispatch_comments_and_reruns(self):
        condition = load_job("doc_review.yml", "review")["if"]
        self.assert_current_maintainer_guard(condition)
        self.assertIn("github.event_name == 'workflow_dispatch'", condition)
        self.assertIn("github.event_name == 'issue_comment'", condition)
        self.assertIn("github.event.comment.user.login", condition)

    def test_ai_sync_guards_manual_runs_and_scheduled_reruns(self):
        condition = load_job("sync-ai-docs-en-to-zh.yml", "translate")["if"]
        self.assert_current_maintainer_guard(condition)
        self.assertIn("github.repository == 'pingcap/docs-cn'", condition)
        self.assertIn("github.event_name == 'workflow_dispatch'", condition)
        self.assertIn("github.event_name == 'schedule'", condition)
        self.assertIn("github.run_attempt == 1", condition)

    def test_pr_sync_guards_manual_runs_and_reruns(self):
        condition = load_job("sync-doc-pr-en-to-zh.yml", "sync-docs")["if"]
        self.assert_current_maintainer_guard(condition)


if __name__ == "__main__":
    unittest.main()
