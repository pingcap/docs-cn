"""Test actor guards on write-privileged workflows that consume secrets."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


DOC_REVIEW_CONDITION = """
contains(fromJson('["lilin90","qiancai","seominjea1942"]'), github.triggering_actor) &&
(
  github.event_name == 'workflow_dispatch' ||
  (
    github.event_name == 'issue_comment' &&
    contains(github.event.comment.body, '/bot-review') &&
    contains(fromJson('["lilin90","qiancai","seominjea1942"]'), github.event.comment.user.login)
  )
)
"""

AI_SYNC_CONDITION = """
github.repository == 'pingcap/docs-cn' &&
(
  (
    github.event_name == 'schedule' &&
    (
      github.run_attempt == 1 ||
      contains(fromJson('["lilin90","qiancai","seominjea1942"]'), github.triggering_actor)
    )
  ) ||
  (
    github.event_name == 'workflow_dispatch' &&
    contains(fromJson('["lilin90","qiancai","seominjea1942"]'), github.triggering_actor)
  )
)
"""

PR_SYNC_CONDITION = """
contains(fromJson('["lilin90","qiancai","seominjea1942"]'), github.triggering_actor)
"""


def load_workflow(workflow_name):
    """Load a workflow without evaluating any GitHub expressions."""
    workflow_path = ROOT / ".github/workflows" / workflow_name
    return yaml.safe_load(workflow_path.read_text())


def load_job(workflow_name, job_name):
    """Load a job definition from a workflow."""
    return load_workflow(workflow_name)["jobs"][job_name]


def normalize(condition):
    """Ignore YAML folding and indentation while preserving expression tokens."""
    return " ".join(condition.split())


class PrivilegedWorkflowActorTest(unittest.TestCase):
    def test_doc_review_guards_dispatch_comments_and_reruns(self):
        condition = load_job("doc_review.yml", "review")["if"]
        self.assertEqual(normalize(condition), normalize(DOC_REVIEW_CONDITION))

    def test_ai_sync_guards_manual_runs_and_scheduled_reruns(self):
        workflow = load_workflow("sync-ai-docs-en-to-zh.yml")
        translate = workflow["jobs"]["translate"]
        self.assertEqual(normalize(translate["if"]), normalize(AI_SYNC_CONDITION))
        self.assertNotIn("concurrency", workflow)
        self.assertEqual(
            translate["concurrency"],
            {"group": "sync-ai-docs-en-to-zh", "cancel-in-progress": True},
        )

    def test_pr_sync_guards_manual_runs_and_reruns(self):
        condition = load_job("sync-doc-pr-en-to-zh.yml", "sync-docs")["if"]
        self.assertEqual(normalize(condition), normalize(PR_SYNC_CONDITION))


if __name__ == "__main__":
    unittest.main()
