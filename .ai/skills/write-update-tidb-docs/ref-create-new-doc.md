# Create New TiDB Documentation

Self-contained workflow for creating a new Chinese documentation page in `pingcap/docs-cn`. Follow these steps sequentially if the [write-update-tidb-docs](/.ai/skills/write-update-tidb-docs/SKILL.md) skill has determined that a new page is needed.

## Confirm the decision to create

This is a final sanity re-check of the create-vs-update decision already made in Step 4 (the authoritative decision point) of the [write-update-tidb-docs](/.ai/skills/write-update-tidb-docs/SKILL.md) skill — not a second, independent decision. If any criterion below fails, switch to `ref-update-existing-doc.md`.

A new page is justified when all of these are true:

- The content does not fit cleanly as a section of an existing page.
- There is enough substance for ≥3 meaningful sections.
- The content has standalone discoverability value (users might search for it directly).

Typical triggers: new feature with its own scenarios/config/limitations, new SQL statement, new `INFORMATION_SCHEMA` table, new integration/tool, new troubleshooting workflow.

Do **not** create a new page if:

- The content can be a section in an existing page without making it too long.
- The content would be too thin (fewer than ~3 sections).
- Similar content already exists and could be expanded instead.

Also confirm this content should be authored in Chinese directly. If it has an English counterpart in `pingcap/docs`, coordinate per the SKILL.md "English-first vs. Chinese-original content" guidance, and never hand-author `ai/` pages here.

## 1. Choose doc type and template

| Doc type | User question it answers | Template to read |
| --- | --- | --- |
| New feature | "What is this? Why use it? How?" | `resources/doc-templates/template-new-feature.md` |
| Task | "How do I do X step by step?" | `resources/doc-templates/template-task.md` |
| Concept | "What is X and how does it work?" | `resources/doc-templates/template-concept.md` |
| Reference | "What are the params/syntax/options?" | `resources/doc-templates/template-reference.md` |
| Troubleshooting | "Something is wrong, how to fix?" | `resources/doc-templates/template-troubleshooting.md` |

Read the selected template before drafting. Use it as a structural skeleton; skip sections that do not apply.

For features combining concept + usage + reference (common in TiDB), use the **new feature** template. Split into multiple pages only when content naturally exceeds ~1500 words per concern.

## 2. Choose file path and name

Look at where similar docs live:

```bash
# Find peers in the TOC
rg -n "<component>|<feature-keyword>" TOC*.md

# Check existing directory structure
ls <component-dir>/
```

**Naming rules** (file names are English even though the content is Chinese):

- Lowercase, hyphen-separated: `feature-name.md`
- Concise and stable: avoid version numbers or overly specific wording
- Follow existing patterns in the same area

**Placement rules:**

| Feature scope | Path |
| --- | --- |
| Component-specific (TiCDC, TiFlash, TiProxy, DM, BR) | `<component>/feature-name.md` |
| SQL statement | `sql-statements/sql-statement-<name>.md` |
| INFORMATION_SCHEMA table | `information-schema/information-schema-<name>.md` |
| Function/operator | `functions-and-operators/<category>.md` |
| Cross-component or general | Root: `feature-name.md` |

## 3. Determine TOC placement

Every navigable page needs a TOC entry.

### Which TOC file?

| Content area | TOC file |
| --- | --- |
| TiDB Self-Managed (most common) | `TOC.md` |
| App development guides | `TOC-develop.md` |
| Best practices | `TOC-best-practices.md` |
| API docs | `TOC-api.md` |
| TiDB release notes | `TOC-tidb-releases.md` |
| PingKai content | `TOC-pingkai.md` |
| AI / vector search | `TOC-ai.md` (auto-translated from `pingcap/docs`; do not add entries here manually) |

### Where in the TOC?

1. Find the relevant section: `rg -n "<keyword>" TOC.md`
2. Look at neighbors (TOC groups by component), then by complexity (overview → getting started → usage → reference → troubleshooting).
3. Place the entry adjacent to similar items at the correct nesting level.

**Format** (2-space indent per level in TOC files):

```markdown
- Category Name
  - [Page Title](/path/to/file.md)
  - [New Page Title](/path/to/new-file.md)
    - [Sub Page](/path/to/sub.md)
```

**TOC title**: concise (3 to 7 words), match the doc H1 when feasible.

## 4. Write front matter

```yaml
---
title: <same as H1>
summary: <concise, verb-led sentence describing what the reader will learn or do>
---
```

- `title` must match the H1 exactly.
- `summary` must not start with `>`, `*`, `#`, `-`, or `[`. If it must, wrap the summary in quotation marks.
- `summary` tells readers what they will learn or accomplish. Keep it one concise sentence and follow the length and phrasing of `summary` fields in nearby docs.
- Add `aliases` only if replacing an older page URL.

## 5. Draft the document

### Writing principles

- Start with what users care about, not the internal background.
- Put conditions before instructions.
- Define jargon on first use.
- Include realistic, runnable examples.
- End with related resources or next steps.
- Apply Chinese writing conventions from `.ai/shared/writing-style.md`: Chinese/English spacing, full-width punctuation in prose, and terminology from `resources/tidb-terms.md`.

### Structure by doc type

**New feature:**

```
# Feature Name
  Intro: what it does, why it matters, when to use it.

## 使用场景

## 前提条件（如有）

## 使用方式
### 方法一：<name>（推荐）
### 方法二：<name>

## 参数说明（如适用）

## 使用限制

## 兼容性

## 常见问题（如有）

## 另请参阅
```

**Task:**

```
# Task Title
  Intro: what this helps you accomplish.

## 前提条件

## 第 1 步：<verb phrase>

## 第 2 步：<verb phrase>

## 第 3 步：<verb phrase>

## 下一步
```

**Concept:**

```
# Concept Title
  Intro: what this concept is and why it matters.

## 工作原理

## 主要特性

## 使用限制（如适用）

## 下一步
```

**Reference:**

```
# Reference Title
  Intro: what this reference covers.

## Category 1
### Item / parameter

## Category 2
### Item / parameter
```

**Troubleshooting:**

```
# Troubleshoot <Problem>
  Intro: what problems this covers.

## 常见原因
### 原因一
  现象 → 解决方案
### 原因二

## 其他原因
### 原因三
```

### Co-authoring mode (for substantial docs)

When the doc is expected to exceed ~800 words or has unclear scope:

1. Propose 3 to 5 core sections. Get confirmation.
2. Start with the highest-value or most-uncertain section.
3. Draft section by section. Ask questions only when facts cannot be derived from available sources.
4. After drafting, run a reader test: predict 5 to 10 questions a real user would ask. Verify the doc answers them.
5. Ask: can anything be removed without losing value?

## 6. Handle associated updates

| Check | Action when needed |
| --- | --- |
| TOC entry | Always required |
| Overview page | Add brief mention or link (e.g., `sql-statements/sql-statement-overview.md`) |
| Related docs | Add "另请参阅" links where users benefit |
| Release notes | Flag for follow-up |
| System variable page | Cross-link if the feature has variables |
| Compatibility page | Update if MySQL compat is affected |

## 7. Validate

```bash
./scripts/markdownlint <new-file> <changed-toc-file>
./scripts/verify-links.sh  # if links were added
```

Also check:

- [ ] Front matter: title matches H1; summary is a concise verb-led sentence and does not start with a special character
- [ ] TOC: correct file, correct level, correct indentation
- [ ] Heading levels: no skipped levels, exactly one H1
- [ ] File name: lowercase, hyphen-separated, `.md` extension
- [ ] Chinese conventions: Chinese/English spacing, full-width punctuation, terminology from `resources/tidb-terms.md`
- [ ] A user finding this via search can complete their task without hidden context

## Common mistakes

- Page too thin — should have been a section in an existing page.
- TOC entry in wrong file or wrong nesting level.
- Intro describes what the doc will do instead of starting with useful info.
- Missing overview/reference page updates that help users discover the new page.
- Forgetting `aliases` when replacing an older page.
- Writing content that duplicates an existing page without adding new user value.
- Hand-authoring an `ai/` page that should come from the English source.
