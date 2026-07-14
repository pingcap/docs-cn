# Translation Rules

Use this file for EN -> ZH translation work that maps changes in `pingcap/docs` (English) into `pingcap/docs-cn` (Chinese).

## Scope

- This guidance is for translating English docs work in `pingcap/docs` into Chinese docs work in `pingcap/docs-cn`.
- Keep the translation faithful to the source change unless the target repo or branch requires a documented difference.
- Prefer the repository automation when it applies:
    - `.github/workflows/sync-doc-pr-en-to-zh.yml` does not open a new PR. It takes an English `source_pr_url` and an **existing** Chinese `target_pr_url`, then syncs the translated changes into that target PR. It is `workflow_dispatch`-only and restricted to authorized accounts. So create or identify the target Chinese PR first, then run the workflow to populate it.
    - `.github/workflows/sync-ai-docs-en-to-zh.yml` translates `ai/` content and `TOC-ai.md` weekly.
  Adapt these workflows instead of building a new translation process from scratch.

## Preserve structure

Keep the following stable unless translation requires a language-only adjustment:

- heading hierarchy
- lists and numbering
- tables and column order
- code fences and info strings
- links, anchors, and repo paths
- commands, flags, API names, config keys, and version numbers
- product names and branch names

Do not invent new product behavior, prerequisites, warnings, or version claims.

## Chinese-language quality

After translating, the Chinese text must read as native documentation, not literal word-for-word conversion. Apply `.ai/shared/writing-style.md`:

- Add a space between Chinese and adjacent English words, numbers, or inline code.
- Use full-width Chinese punctuation in prose and half-width punctuation inside code.
- Keep product names, commands, flags, paths, and config keys in English.

## Terminology

- Use `resources/tidb-terms.md` (the TiDB 中英术语表) as the source of truth for terminology.
- Use `.ai/shared/translation-terms.md` as a quick reference for high-frequency terms.
- If a term is missing or ambiguous, keep the source term until you can verify the preferred translation.

## PR traceability

When preparing a translation PR:

- reference the source English PR or file links in the PR body under `This PR is translated from:` (the docs-cn PR template provides this field)
- preserve the intended affected versions as much as the target repo allows, following the version checkboxes in `.github/pull_request_template.md`
- keep the PR body compatible with `.github/pull_request_template.md`
- make the relationship to the source PR explicit, and apply the relevant translation label when available

## Workflow expectations

- Identify the source files in `pingcap/docs` and the target files in `pingcap/docs-cn` before translating.
- Check whether the target branch should be `master` or a release branch, matching the source PR's affected versions.
- If a helper script or sync workflow is available, prefer adapting it over rewriting the workflow from scratch.
- If local automation depends on unavailable tokens or secrets, still prepare the branch, file list, PR body, and follow-up instructions so a human can finish the workflow quickly.
- Do not hand-translate `ai/` content; it is synced automatically from the English source.
