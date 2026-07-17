# Repo Conventions

This file captures the repository-specific rules that agents should follow in `pingcap/docs-cn`.

## Repository scope

- `pingcap/docs-cn` stores the Chinese TiDB documentation source.
- `pingcap/docs` stores the English TiDB documentation source.
- This repository is the source for the Chinese TiDB documentation published on the PingCAP documentation website.
- Much of the Chinese content corresponds to an English source in `pingcap/docs`. When a change has an English counterpart, keep the two sides traceable instead of editing only one.

## Repository versions and branches

- The `master` branch tracks the latest development version (dev) of the Chinese TiDB documentation.
- Published documentation is maintained in the corresponding `release-<version>` branches.
- The PR template defines the canonical maintained version list: `master`, `v9.0`, `v8.5`, `v8.1`, `v7.5`, `v7.1`, `v6.5`, `v6.1`. Older `release-*` branches exist but are no longer routinely updated.
- By default, target `master` unless the change clearly belongs to a maintained release branch.
- Preserve branch intent. Do not treat release-branch behavior as the default development behavior, and do not move dev-only content into release branches.

## Choosing affected versions

Follow the repository's affected-version model when proposing or reviewing changes. The detailed Chinese guidance lives in `CONTRIBUTING.md` (版本选择指南).

- By default, affected versions should be `master` only for documentation enhancements, missing-content additions, wording fixes, refactors within a topic, and general corrections that are not tied to a specific released behavior.
- Choose the affected release branch or branches together with `master` when the change involves version-specific behavior, compatibility changes, changed default values, changed system variable behavior, display fixes, or broken-link fixes in published docs.
- If a change applies to multiple maintained versions, prefer the latest applicable branch and use cherry-pick labels instead of opening parallel PRs by default.
- If most of the change can be cherry-picked but some branches require different wording or follow-up edits, account for version-specific follow-up work and the relevant reminder labels.

## Cherry-pick and branch-follow-up conventions

- Use the repository's cherry-pick label workflow instead of inventing a custom multi-branch process.
- Cherry-pick labels follow the pattern `needs-cherry-pick-release-X.Y` (for example, `needs-cherry-pick-release-8.5`, `needs-cherry-pick-release-7.5`).
- If a change applies only to one documentation version, use that branch directly and do not add unnecessary cherry-pick labels.
- If a change applies to multiple documentation versions, prefer a single PR on the latest applicable branch and rely on cherry-pick labels for the remaining maintained versions.
- If branch-specific differences are expected, flag that clearly so reviewers know follow-up edits are required in the cherry-picked PRs.

## Repository layout and navigation

- Use the existing repository structure and nearby documents as the primary guide for where new content should live.
- New navigable documents usually require a matching update in the appropriate TOC file. This repository uses several TOC files:
    - `TOC.md`: the main TiDB Self-Managed documentation tree
    - `TOC-ai.md`: AI / vector search content (auto-translated, see below)
    - `TOC-api.md`: API docs
    - `TOC-best-practices.md`: best practices
    - `TOC-develop.md`: application development guides
    - `TOC-tidb-releases.md`: release notes
    - `TOC-pingkai.md`: PingKai-specific tree
- When a document is added, removed, moved, or renamed, check whether related TOC files, aliases, links, and cross-document references also need updates.
- Reuse existing document patterns in the same area before introducing a new structure.

## AI and TiDB Cloud content boundaries

- The `ai/` content and `TOC-ai.md` are AI-translated weekly from `pingcap/docs` (`release-8.5`) by `.github/workflows/sync-ai-docs-en-to-zh.yml`. Do not hand-edit the Chinese `ai/` content. To change it, edit the English source in `pingcap/docs` and let the sync workflow translate it.
- The `tidb-cloud/` content is largely derived from the English source as well. Be cautious before editing it directly; confirm whether the change should originate in `pingcap/docs`.
- Be careful with `CustomContent` tags such as `<CustomContent platform="tidb">` and `<CustomContent platform="tidb-cloud">`. Do not change, remove, or expand them casually, because they control platform-specific rendering behavior.

## Contribution model

- New documents should follow the templates in `resources/doc-templates/` when applicable.
- Keep PR descriptions compatible with `.github/pull_request_template.md`.
- Keep changes scoped to the requested task. Do not broaden a focused doc update into unrelated cleanup.
- Prefer existing repository workflows, labels, and conventions over ad hoc alternatives.
- When contributing diagrams, follow the existing diagram-style guidance rather than introducing a new visual style.

## File naming rules

- Use file names that briefly describe the document content, for example, `destroy-tidb-cluster.md`.
- Keep file names concise and general. Avoid overly specific wording that might require frequent renaming and cause unnecessary URL changes.
- File names use English even though the document content is Chinese.
- Except for special files such as `TOC.md`, `CONTRIBUTING.md`, and `README.md`, use lowercase letters only in file names.
- If a file name contains multiple English words, separate them with hyphens (`-`).
- Do not use underscores (`_`) in file names.
- Use lowercase file extensions only.
- Markdown files must use the `.md` extension.

## Content boundaries

- Preserve product behavior, version numbers, links, anchors, file intent, and branch intent unless the task explicitly requires changing them.
- Do not silently change technical meaning while improving wording.
- Avoid changing commands, code samples, UI strings, configuration names, API fields, JSON, EBNF content, or generated helper files unless the task directly requires it or they are factually wrong.
- When editing syntax-related content, be careful not to break EBNF or other structured source formats.
- Keep cross-repo translation traceability when work maps between `docs` and `docs-cn`.
- When a translation-related task maps content across repositories, preserve the source PR relationship, terminology intent, and affected-file mapping.

## Front matter and document metadata

- Preserve existing front matter structure unless the task requires a metadata change.
- When front matter is present, keep `title`, `summary`, `aliases`, and other metadata aligned with the document content.
- If a file is moved or renamed, check whether `aliases` should be updated to preserve inbound links. When deleting a document, add `aliases` at the top of the replacement so old links still resolve.
- Do not add or remove metadata fields casually. Follow existing patterns in nearby documents.

## Linking and cross-document consistency

- Preserve repository-relative absolute links such as `/foo/bar.md` when that is the repository convention.
- When editing a document that summarizes or references other docs, check whether those related docs also need updates.
- If a term, version statement, feature behavior, workflow, or compatibility note changes in one place, check nearby overview, task, reference, and release-note content for possible follow-up updates.
- When changing headings, verify whether anchors, intra-repo links, TOC entries, or external references might be affected.

## Validation habits

Use existing repository checks instead of inventing new ones.

- `./scripts/markdownlint <files>` for Markdown formatting (the 25 rules are explained in `resources/markdownlint-rules.md`)
- `./scripts/verify-links.sh` for link validation when links, anchors, moved files, or renamed files are involved
- `./scripts/verify-link-anchors.sh` for anchor validation
- `./scripts/check-keywords.py` when the task touches restricted or sensitive keywords
- `./scripts/verify-duplicated-file-name.sh` when adding or renaming files

If a full check is too expensive for the task, validate the files you changed and any directly affected TOC or link targets.

## Existing helpers

Look for established scripts and workflows before automating from scratch.

Use them as references for expected behavior, even when local credentials, permissions, or secrets prevent direct execution.

## Agent behavior in this repository

- Read the shared guidance in `.agents/shared/` before making non-trivial changes.
- Use a matching skill in `.agents/skills/` when the task is workflow-specific.
- Prefer minimal, targeted edits over broad rewrites.
- Reuse existing wording, terminology, and document structure when they are already correct.
- When unsure, check nearby docs, templates, and repository patterns before introducing a new approach.
