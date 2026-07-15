---
name: docs-pr-metadata-guard
description: Use when creating or editing pull requests in pingcap/docs-cn so the PR template sections, version checkboxes, related-link fields, HTML comments, and description structure stay intact. Trigger on tasks involving PR creation, PR body updates, version selection, cherry-pick label decisions, or translating a PR from pingcap/docs.
---

# Docs PR Metadata Guard

Use this skill for `pingcap/docs-cn` GitHub pull request metadata work. The goal is to preserve the repository-required PR description structure while editing only the mutable fields.

Before changing a PR body, read `.github/pull_request_template.md`.

## Workflow

1. PR titles follow `pingcap/community` commit-message style (for example, `Fix typos in tidb-monitoring-api.md`). Titles and section content can be in Chinese or English; keep product names, commands, and paths in English.
2. For a new PR, start from `.github/pull_request_template.md` instead of writing the body from scratch.
   - Copy the template into a local Markdown file and fill in the mutable fields.
   - Submit with `gh pr create --body-file <local-file>`. This is the reliable method. The `-T` / `--template` flag matches a template by **name** (the basename, for example `gh pr create -T pull_request_template.md`), not by path, so `-T .github/pull_request_template.md` will not match. Prefer `--body-file`.
   - Review the local file against the template before calling `gh`.
3. Fill in the required sections with concrete information.
   - **What is changed, added or deleted? (Required)**: describe what changed and why in clear, specific language. Do not leave this blank or fill it with a generic placeholder.
   - **Which TiDB version(s) do your changes apply to? (Required)**: check at least one version checkbox. Follow the `CONTRIBUTING.md` (版本选择指南):
     - Default to `master` only for general improvements, wording fixes, missing-content additions, and corrections not tied to a specific released behavior.
     - Check the affected release version(s) together with `master` when the change involves version-specific behavior, compatibility changes, changed defaults, or fixes in published docs.
   - **What is the related PR or file link(s)?**: fill in the source link under `This PR is translated from:` when the PR is a translation from `pingcap/docs`. Fill in other reference links such as product PRs, issues, or related doc PRs under `Other reference link(s):`.
   - **AI agent involvement**: when this section is present in the template, keep it intact. Check its checkbox only when the changes were primarily made by an AI agent on behalf of the PR author; otherwise leave it unchecked.
   - **Do your changes match any of the following descriptions?**: check all that apply. If the change needs different wording on another branch, check `Need modification after applied to another branch` and comment `/label requires-version-specific-changes` to trigger the bot. (Note: the PR template still prints the old command `/label version-specific-changes-required`, which the bot now rejects because the actual label is `requires-version-specific-changes`. Use the actual label name.)
4. Choose the correct base branch.
   - Default to `master` for most documentation PRs.
   - Use a specific `release-X.Y` branch when the change is scoped to a single published version and does not apply to `master`.
   - Do not open PRs for the Chinese .agents/` content: it is auto-translated weekly from `pingcap/docs`. Fix the English source instead.
5. For an existing PR, update only the mutable sections.
   - Safe targets: the description text under "What is changed, added or deleted?", the version checkboxes, the related-link fields, and the description checkboxes.
   - Do not rename headings, reorder sections, or rewrite the template wholesale.
6. Preserve hidden HTML comments exactly.
   - Keep `<!--Thanks for your contribution to TiDB documentation. Please answer the following questions.-->` unchanged.
   - Keep `<!--Tell us what you did and why.-->` unchanged.
   - Keep `<!-- Fill in "x" in [] to tick the checkbox below.-->` unchanged.
   - Keep `<!--Reference link(s) will help reviewers review your PR quickly.-->` unchanged.
   - Keep `<!-- If yes, please comment "/label version-specific-changes-required" below to trigger the bot to add the label.-->` unchanged.
   - Do not delete or rewrite any template comment that explains contributor behavior or bot behavior.
7. Preserve the "Tips for choosing the affected version(s)" guidance block.
   - The bold tips paragraph and the `CONTRIBUTING.md` (版本选择指南) link between the version heading and the checkboxes are part of the template structure. Do not delete, rewrite, or move them.
8. Handle the first-time contributors' checklist correctly.
   - If the contributor is not a first-time contributor, remove the entire "First-time contributors' checklist" section as the template comment instructs.
   - If the contributor is a first-time contributor, keep the section and check the CLA checkbox after signing the [Contributor License Agreement](https://cla.pingcap.net/pingcap/docs).
9. Prefer file-based edits for GitHub metadata.
   - Materialize the intended PR body into a local Markdown file.
   - Review that file against the PR template before calling `gh`.
10. After any PR body update, re-read the PR to verify the structure is intact.

## Version checkbox rules

The version checkboxes in the PR template follow a specific order from newest to oldest:

```
- [ ] master (the latest development version)
- [ ] v9.0 (TiDB 9.0 versions)
- [ ] v8.5 (TiDB 8.5 versions)
- [ ] v8.1 (TiDB 8.1 versions)
- [ ] v7.5 (TiDB 7.5 versions)
- [ ] v7.1 (TiDB 7.1 versions)
- [ ] v6.5 (TiDB 6.5 versions)
```

When filling them in:

- Do not add or remove version lines. The template defines the canonical list.
- Do not reorder the version lines.
- Check only the versions where the change should apply.
- If a version is not in the template list, do not invent a new checkbox line.

## Cherry-pick and label conventions

- When a change applies to multiple versions, prefer a single PR on the latest applicable branch and use cherry-pick labels for remaining maintained versions.
- Cherry-pick labels follow the pattern `needs-cherry-pick-release-X.Y` (for example, `needs-cherry-pick-release-8.5`, `needs-cherry-pick-release-7.5`).
- If branch-specific wording differences are expected, check `Need modification after applied to another branch` and comment `/label requires-version-specific-changes` so cherry-pick reviewers know follow-up edits are required. (`requires-version-specific-changes` is the real label name; the command printed in the PR template, `/label version-specific-changes-required`, is a historical error that the bot rejects.)
- The two other description checkboxes signal cherry-pick risk:
    - `Delete files` and `Change aliases` flag changes that need extra care during cherry-pick and link checking.
    - `Might cause conflicts after applied to another branch` warns reviewers that the automatic cherry-pick may not apply cleanly.
- Use the repository's cherry-pick label workflow. Do not invent a custom multi-branch process.
- Before applying a label, check which labels exist with `gh label list`. Apply a translation-source label when the PR is translated from `pingcap/docs`, and area/type labels that match the change.

## Quick checks

- The PR body contains the "What is changed, added or deleted? (Required)" heading with a non-empty description below it.
- At least one version checkbox is checked under "Which TiDB version(s) do your changes apply to? (Required)".
- The version checkbox section preserves the template's canonical version list (`master`, `v9.0`, `v8.5`, `v8.1`, `v7.5`, `v7.1`, `v6.5`) and order.
- The "Tips for choosing the affected version(s)" paragraph and the `CONTRIBUTING.md` link are present between the version heading and the checkboxes.
- The related-link fields (`This PR is translated from:` and `Other reference link(s):`) are present, even if left at their default values.
- The `AI agent involvement` section is present when defined by the template, and its checkbox accurately reflects whether an AI agent primarily made the changes on the PR author's behalf.
- The "Do your changes match any of the following descriptions?" section is present with its four checkboxes intact.
- The first-time contributors' checklist is either correctly filled in or removed entirely as instructed.
- The base branch matches the change scope: `master` by default, or a specific `release-X.Y` for version-scoped fixes.
