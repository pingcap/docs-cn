# AI Collaboration Guide

This directory stores repo-local guidance for AI agents working in `pingcap/docs-cn`, the source repository for the Chinese TiDB documentation.

## Structure

- `.ai/shared/`: reusable repo policy, Chinese writing guidance, and EN -> ZH translation guidance
- `.ai/skills/`: workflow-specific instructions for recurring tasks in this repo

## Shared guidance

Read only the files that apply to the task:

- `.ai/shared/repo-conventions.md`: repository scope, branch and version rules, file naming, TOC expectations, AI/TiDB Cloud content boundaries, cross-repo (docs <-> docs-cn) traceability, and validation habits
- `.ai/shared/writing-style.md`: document structure, Chinese-language wording and punctuation, formatting, headings, front matter, and repo-compatible writing style for Chinese docs
- `.ai/shared/translation-rules.md`: EN (`pingcap/docs`) -> ZH (`pingcap/docs-cn`) translation constraints, traceability, structure preservation, and workflow expectations
- `.ai/shared/translation-terms.md`: quick terminology reference for frequent translation terms

Use `resources/tidb-terms.md` (the TiDB 中英术语表) when terminology is uncertain or not covered by the quick reference.

## Current skills

- `.ai/skills/write-update-tidb-docs/`: write new Chinese TiDB documentation or update existing documentation based on code PRs, issues, design docs, product specs, or feature descriptions; includes separate reference files for creating new docs (`ref-create-new-doc.md`) and updating existing docs (`ref-update-existing-doc.md`)
- `.ai/skills/review-doc-pr/`: review documentation PRs and Markdown diffs for factual accuracy, user usefulness, completeness, version fit, related-doc impact, links, and Chinese writing style
- `.ai/skills/docs-pr-metadata-guard/`: guard PR template structure when creating or editing pull requests, such as version checkboxes, required sections, HTML comments, related-link fields, and cherry-pick conventions
- `.ai/skills/docs-issue-metadata-guard/`: guard issue template structure when creating or editing issues, such as template selection, required fields, scope boundaries, and label hygiene

## Repo automation worth knowing

This repository already automates several workflows. Prefer these over ad hoc processes:

- `.github/workflows/sync-doc-pr-en-to-zh.yml`: syncs translated changes from an English source PR in `pingcap/docs` into an **existing** Chinese target PR in `pingcap/docs-cn` (it requires both `source_pr_url` and `target_pr_url`; it does not create the target PR). Manual dispatch only, restricted to authorized accounts.
- `.github/workflows/sync-ai-docs-en-to-zh.yml`: weekly AI translation of `ai/` content and `TOC-ai.md` from `pingcap/docs` (`release-8.5`) into this repo. Do not hand-edit the Chinese `ai/` content; fix the English source in `pingcap/docs` instead.
- `.github/workflows/doc_review.yml`: AI doc review triggered by a `/bot-review` comment, driven by `doc-review-prompt.txt`.

## How to use it

Use progressive loading so the task stays grounded but efficient:

1. Start with the relevant shared guidance.
2. Load a skill only when the task matches that workflow.
3. Validate the files you changed with the repo's existing checks (`./scripts/markdownlint`, `./scripts/verify-links.sh`) when practical.

Keep the task grounded in the existing repository rules, templates, scripts, and workflows.
