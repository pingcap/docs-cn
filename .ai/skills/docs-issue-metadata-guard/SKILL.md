---
name: docs-issue-metadata-guard
description: Use when creating or editing GitHub issues in pingcap/docs-cn so issue templates, required fields, scope boundaries, and labels stay consistent with repository workflow. Trigger on tasks involving issue creation, error reports, change requests, questions, label selection, or searching for existing issues before filing a new one.
---

# Docs Issue Metadata Guard

Use this skill for `pingcap/docs-cn` GitHub issue metadata work. The goal is to preserve issue-template structure, scope discipline, and searchable issue descriptions.

Before creating or editing an issue, read the matching file under `.github/ISSUE_TEMPLATE/`.

This repository has three issue templates and disables blank issues (`blank_issues_enabled: false` in `config.yml`). Every new issue must use one of the templates. The `config.yml` also routes usage questions to the AskTUG forum (`https://pingkai.cn/tidbcommunity/forum/`).

## Issue templates

| Template | File | `gh --template` name | Use when |
|---|---|---|---|
| Error Report | `error-report.md` | `🐛 Error Report` | Typos, grammatical errors, terminology misuse, ambiguity, broken formatting, incorrect code samples, wrong links |
| Change Request | `change-request.md` | `🚀 Change Request` | Suggesting new content, restructuring, adding missing information, improving existing documentation |
| Question | `question.md` | `🤔 Question` | Usage questions about documentation that are not answered in existing docs or discussions |

The templates are bilingual: English prompts with Chinese explanations inside HTML comments. Keep both. Contributors usually answer in Chinese, which is appropriate for this repository.

## Scope boundary

All three templates include the same scope reminder:

> This repository is ONLY used to solve problems related to DOCS-CN.

Enforce this boundary:

- Do not file product bug reports, feature requests, or technical support questions in this repository.
- Redirect product issues to the appropriate repository under `github.com/pingcap/`.
- Redirect technical support questions to the AskTUG community forum (`https://pingkai.cn/tidbcommunity/forum/`), as the templates instruct.
- If an issue mixes a doc problem with a product problem, separate them: file the doc part here and note where the product part should go.

## Workflow

1. Write issue titles and descriptions in Chinese (matching the repository audience). Keep product names, commands, and paths in English.
2. Search existing issues first before filing a new one.
   - Check open and closed issues for duplicates or related discussions.
   - If an existing issue covers the same problem, comment on it instead of creating a new one.
3. Choose the correct issue template based on the issue type.
   - Do not write the body from scratch. Start from the matching template.
   - The repository disables blank issues, but `gh issue create` does not enforce this — the agent must self-enforce template usage.
4. When using `gh issue create`:
   - Use `--template "🐛 Error Report"`, `--template "🚀 Change Request"`, or `--template "🤔 Question"` to select the template (the `-T` / `--template` flag for `gh issue create` takes a template **name** from the template front matter, not a file path).
   - Alternatively, copy the template body (everything below the YAML front matter `---` block) into a local file and use `--body-file <local-file>`. The YAML front matter (`name:` and `about:`) is GitHub metadata and does not appear in the issue body.
   - Always add `--label` flags explicitly — `gh issue create` does not auto-apply labels from templates.
5. Fill in all template fields with concrete information.

### Error report

Fill in both numbered prompts:

- **What is the document directory for the problem?** — provide the published doc URL or the repository file path. Do not leave this blank.
- **How would you like to improve it?** — describe the specific error and the expected correction. Include the current incorrect text and the proposed fix when possible.

### Change request

Fill in all three numbered prompts:

- **Describe what you find is inappropriate or missing in the existing docs.** — be specific about which document, section, or topic is affected.
- **Describe your suggestion or addition.** — explain what should be changed or added and why it helps users.
- **Provide some reference materials (documents, websites, etc) if you could.** — link to product PRs, release notes, related docs, or external references that support the request. Write "N/A" if no references are available; do not delete the prompt.

### Question

Before filing, complete the checklist the template lists:

- Search existing Stack Overflow questions and Google results.
- Search open and closed GitHub issues in `pingcap/docs-cn`.
- Read the relevant docs in `pingcap/docs` and `pingcap/docs-cn`.

Then describe the question clearly, including what you searched and why the existing documentation did not answer it.

## Editing existing issues

1. Fetch the current title, body, and labels first.
2. Patch only the intended sections and preserve untouched sections, metadata, and still-valid context.
3. Do not rewrite the issue body from scratch.
4. Preserve the template structure: keep the headings and numbered prompts intact.

## Preserving template structure

- Keep the bold scope reminder and the Chinese HTML comment block (the AskTUG forum link) unchanged.
- Keep the template heading (`## Error 报告`, `## Change Request`, or `## Question`) unchanged.
- Keep the numbered prompts, the bilingual instruction text, and the HTML comments in each template unchanged.
- Do not merge, reorder, or rename template sections.

## Labels

- Apply labels explicitly when creating or editing issues.
- For issues created with `gh issue create`, add labels via the `-l` / `--label` flag since the CLI does not auto-apply template labels.
- For existing issues, use `gh issue edit` to update labels.
- Pick labels that match the existing taxonomy in this repository:
    - **Type labels** describing the issue intent (for example, error/typo, enhancement, feature request, question, refactor).
    - **Area labels** identifying the documentation area (for example, a specific component or feature).
    - **Priority labels** when the issue affects published documentation accuracy or user-facing correctness.
    - **Workflow labels** such as `good first issue` or `help wanted` for community contribution signaling.
- Before inventing a label, check which labels the repository already uses with `gh label list`.
- If label permissions are missing, add a comment with `Suggested labels: ...` so maintainers can apply them.

## File-based editing

- Materialize the intended issue body in a local Markdown file.
- For new issues, review that file against the matching issue template before calling `gh`.
- For existing issues, diff the patched body against the current issue body before calling `gh`.

## Quick checks

- The issue uses one of the three available templates (Error Report, Change Request, or Question) — blank issues are not allowed.
- The issue stays within the docs-cn-only scope and does not mix in product bugs or feature requests.
- All template fields are filled in with concrete information, not generic placeholders.
- The template headings, numbered prompts, bilingual text, and HTML comments are preserved.
- Existing issue edits preserve untouched sections and metadata outside the intended patch.
- The issue carries appropriate labels, or a `Suggested labels: ...` comment is present when label permissions are missing.
