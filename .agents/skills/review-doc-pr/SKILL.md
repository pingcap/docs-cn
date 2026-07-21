---
name: review-doc-pr
description: Review a Chinese TiDB documentation pull request or Markdown diff for factual accuracy, user usefulness, structure, completeness, version fit, links, and repo-style issues in pingcap/docs-cn.
---

# Review Doc PR

Use this skill when the task is to review a documentation PR, a Markdown diff, or changed documentation content in `pingcap/docs-cn`.

## Default behavior

- By default, present review findings in the conversation. Do not post comments, reviews, or committable suggestions to the GitHub PR unless the user explicitly asks you to publish them.
- When the user does ask you to post to the PR, format safe line-level fixes as GitHub-ready committable suggestions so the author can apply them directly.
- This repository also runs an automated AI review via `.github/workflows/doc_review.yml` (triggered by a `/bot-review` comment, driven by `doc-review-prompt.txt`). When mirroring the repo's review behavior, align with that prompt.

## Load this context first

Read only the files that matter for the current review:

- `.agents/shared/repo-conventions.md`
- `.agents/shared/writing-style.md`
- `.agents/shared/translation-rules.md` and `.agents/shared/translation-terms.md` when the PR is a translation from `pingcap/docs`
- `doc-review-prompt.txt` when you need to mirror the repo's AI review behavior
- `resources/tidb-terms.md` when terminology is uncertain
- `resources/doc-templates/<relevant-template>.md` if the doc type matters

Also inspect the PR description, linked issues, the English source PR (for translations), nearby docs, and other relevant context when needed to understand what changed, why it changed, who it affects, and which versions or branches are in scope.

## Review mindset

Review from the user's perspective, not only the author's.

Treat this skill as having two equally important responsibilities:

1. Act as a TiDB expert and check for technical, accuracy, logic, consistency, and user-impact issues.
2. Act as a senior Chinese technical writer: check whether the content is clear, concise, and easy to understand, and review it against `.agents/shared/writing-style.md`, including Chinese terminology (`resources/tidb-terms.md`), Chinese/English spacing, and full-width punctuation.

Do not treat writing-style review as optional after the technical review. Both are part of the default review scope. When the content does not meet the bar for technical writing quality, improve it so the content becomes more logical, clear, concise, and easy to understand, while preserving technical meaning and scope.

Ask:

- Can a TiDB user understand what this is, why it matters, when to use it, and how to use it?
- Does the document help the user complete a task or make a decision?
- If there are multiple methods, does it help the user choose among them?
- Does the content explain user-facing behavior instead of focusing too much on internal implementation?

Do not stop at wording fixes. Review for user impact, missing context, hidden confusion, and maintenance risk.

## Review priorities

Check issues in this order:

1. factual correctness
2. logic problems, contradictions, or missing user context
3. completeness of the user-facing explanation
4. version or branch mismatch
5. missing related updates in other docs
6. broken links, anchors, aliases, TOC, or path assumptions
7. Markdown and style problems, including Chinese grammar, terminology, spacing, punctuation, and other wording issues

## Review rules

- Formatting rule (applies when the user has asked you to post to the PR): for any line-level issue that can be fixed safely without changing technical meaning or broadening scope, prefer a GitHub-ready committable suggestion over a plain review comment.
- This suggestion-first rule applies to both categories of review findings:
    - TiDB expert findings such as technical accuracy, logic, terminology, consistency, version fit, and user-impact issues
    - senior technical writer findings such as clarity, structure, wording, grammar, punctuation, Chinese/English spacing, heading style, and writing-style-guide issues
- When the problem is weak Chinese technical writing and the fix is safe, provide the improved Chinese directly as a GitHub-ready committable suggestion instead of only describing the issue.
- Use a plain review comment only when the fact is unclear, the issue spans multiple lines or paragraphs in a way that is not safe to suggest inline, or the correct fix depends on product confirmation or broader structural decisions.
- Do not give praise-only comments.
- Keep comments actionable and tied to the changed lines, behavior, or user impact.
- Prefer explaining why the issue matters to the user, not just what wording looks odd.
- Preserve the author's intent when suggesting revised wording.
- Whenever practical, provide ready-to-commit doc suggestions so the author can apply them directly.
- If a direct wording fix is not appropriate because the issue is factual, structural, or unclear, explain the issue clearly and ask a concrete clarification question when needed.
- Do not rewrite code samples, commands, UI strings, API fields, configuration names, JSON, or outputs unless they are factually wrong, inconsistent, or part of the requested task.
- Before raising a question, first use nearby docs, PR context, linked issues, the English source, or other trustworthy references to understand the change.
- If uncertainty remains, raise a concrete clarification question instead of guessing.

## Special-case review scope

When the PR is a translation from `pingcap/docs` (for example, created by `.github/workflows/sync-doc-pr-en-to-zh.yml` or an automated translation bot), prioritize:

- Chinese grammar, spelling, and full-width punctuation
- Chinese/English spacing
- terminology consistency against `resources/tidb-terms.md`
- faithfulness to the English source (no added or dropped facts, prerequisites, or version claims)

Still flag factual, terminology, or user-facing accuracy issues when they are visible from the changed content.

## Review by change type

### For new documents

Check whether:

- the document is placed in a reasonable location in the doc structure
- the title is clear and searchable
- the file name follows repo naming rules
- the document includes an appropriate `summary`
- the structure matches the document type and user task
- related TOC files also need updates

### For deleted documents

Check whether:

- the deletion leaves navigation or conceptual gaps
- the parent document should mention the removal or deprecation
- a replacement feature or alternative document should be linked
- `aliases` are added at the top of the replacement to preserve old inbound links

### For updated documents

Check whether:

- other related documents also need updates
- summary pages, overview docs, or aggregate docs also need updates
- the updated content still matches the current document scope and title
- the change should also affect release notes or other versioned docs

### For renamed documents

Check whether:

- TOC files are updated
- links and references are updated
- `aliases` are added when needed to preserve existing URLs

## Version and branch checks

Pay special attention to version-sensitive changes.

- Confirm whether the change applies only to dev docs (`master`) or to multiple released versions.
- For compatibility changes, bug fixes, behavior changes, or system variable changes, check whether all applicable branches should be updated.
- For system variable additions, removals, or behavior changes, verify the version where the change starts.
- If a change mentions product versions and requires cherry-picks with branch-specific wording, flag the need for branch-specific follow-up.
- Check whether the change should also update the relevant release notes.

## User usefulness checks

Check whether the document tells the user:

- what this feature or behavior is
- why they might need it
- when to perform the action
- what prerequisites or conditions apply
- what happens after the step
- what risks, limits, or tradeoffs matter
- how to choose among multiple available methods

Also check whether:

- the document focuses on how users use the product, not just how the product works internally
- recommendations explain the reason behind them
- commands, outputs, placeholders, or special markers are understandable to the reader
- abstract wording should be made more concrete

## Information design checks

Check whether:

- information types are separated clearly, such as concept, procedure, reference, warning, limitation, input, and output
- similar items are grouped together
- important information is distinguished from ordinary information
- warnings, limitations, and ordinary notes are not mixed together
- a list, table, or image would communicate the content better
- when multiple methods exist, the recommended one appears first or is clearly identified

## Order and flow checks

Check whether:

- prerequisites appear before the steps they affect
- conditions are placed before instructions, not after
- the content follows the actual operation order
- expected results or follow-up behavior are clear
- the user gets the most useful information at the point where they need it
- a less recommended method appears first without explanation

## Logic, consistency, and completeness checks

Check whether:

- the title matches the content
- the content is internally consistent
- examples, commands, outputs, and explanations agree with each other
- the same concept is named consistently within the document
- similar scopes or categories are described consistently
- information conflicts with other docs that cover the same area
- linked or referenced information is actually linked when needed
- prerequisite steps, follow-up behavior, default values, configuration location, or modification method are missing when users would likely need them

## Minimalism and maintainability checks

Check whether:

- the document repeats information unnecessarily
- introductory text duplicates later procedural content without adding value
- sentences contain removable redundancy
- warnings, step overviews, or critical reminders are repeated for a valid reason
- version-sensitive statements are likely to go stale
- duplicated facts will be hard to maintain across files
- file additions, deletions, moves, or renames also require TOC, alias, link, or cross-doc updates

## Suggested review workflow

1. Inspect the PR title, description, affected files, and target branch.
2. Determine the change type: new doc, deleted doc, renamed doc, doc fix, doc optimization, feature doc, compatibility change, behavior update, or translation from `pingcap/docs`.
3. Read the changed sections plus the nearby context needed to judge correctness and user impact.
4. Check linked issues, feature specs, release notes, the English source PR, or related docs when background is needed.
5. Compare the document shape against the nearest repo template when structure matters.
6. Run lightweight checks when useful:
   - `gh pr view <pr>`
   - `gh pr diff <pr>`
   - `./scripts/markdownlint <files>`
   - `./scripts/verify-links.sh` or `./scripts/verify-link-anchors.sh` when links, moved files, renamed files, TOC files, or anchors changed
7. Report only concrete findings.

## Output expectations

- Lead with findings, ordered by severity.
- Include file and line references when available.
- Explain the user impact or maintenance impact of each finding when possible.
- Distinguish confirmed issues from clarification questions.
- For safe line-level fixes, prefer GitHub-ready committable suggestions by default.
- Apply this default to both technical/correctness findings and writing-style findings.
- Fall back to plain review comments only for fact-sensitive, cross-paragraph, or structurally ambiguous issues that are not safe to express as inline suggestions.
- In addition to general review comments, provide ready-to-commit doc suggestions whenever practical, especially for wording, grammar, structure, clarity, and small completeness fixes.
- If no findings remain, say so explicitly and mention any residual review gap, such as checks not run or product facts not independently verified.
