# Update Existing TiDB Documentation

Self-contained workflow for updating existing Chinese documentation pages in
`pingcap/docs-cn`. Follow these steps sequentially after SKILL.md has determined
that existing pages need updating.

## 1. Identify target docs

### From code patterns

This is the authoritative code-pattern → target-file mapping. It expands the triage table in `SKILL.md` with exact file paths. (File names are English; the content inside is Chinese.)

| Code pattern | Primary target |
| --- | --- |
| New/changed `SysVar` / `DefValue` | `system-variables.md` |
| New/changed config field / `toml` tag | `tidb-configuration-file.md` / `tikv-configuration-file.md` / `pd-configuration-file.md` / `tiflash/tiflash-configuration.md` |
| New/changed command-line flag | `command-line-flags-for-*-configuration.md` |
| Changed SQL grammar (parser `.y`) | `sql-statements/sql-statement-<name>.md` |
| New/changed function | `functions-and-operators/` |
| New INFORMATION_SCHEMA column | `information-schema/information-schema-<name>.md` |
| Changed metric or alert | `grafana-*.md` or component monitoring docs |
| Changed default/behavior | Feature doc + compatibility notes |
| New error code | Error reference docs |
| Changed API | API reference docs |

### Search strategies

```bash
# Find docs mentioning the feature/config/variable
rg -l "<name-or-keyword>" --type md

# Find where it appears in TOC
rg -n "<keyword>" TOC*.md

# Find docs that link to the target page
rg -l "/path-to-target.md" --type md
```

Also check component directories (`ticdc/`, `tiflash/`, `tiproxy/`, `dm/`,
`br/`) when the change touches a specific component.

Do not edit `ai/` content here; it is AI-translated weekly from `pingcap/docs`. Update the English source instead.

## 2. Assess related docs (impact radius)

A single code change often ripples into multiple pages.

### Direct impact (update in the same edit)

- The primary reference page (config file, system variables, flags)
- The feature/task page describing how to use the changed behavior
- The SQL statement page if syntax changed

### Indirect impact (assess case by case)

| Category | Examples |
| --- | --- |
| Overview pages | `sql-statements/sql-statement-overview.md`, `functions-and-operators/functions-and-operators-overview.md` |
| Feature lists | `basic-features.md` |
| Compatibility | `mysql-compatibility.md`, feature compat tables |
| Limitations | `tidb-limitations.md`, feature-specific limitations |
| FAQ | Feature FAQ pages |
| Best practices | Operational or schema best practices |
| Troubleshooting | If the change resolves or introduces known issues |
| Release notes | If user-facing in a specific version |

**Scope rule:**

- Direct-impact pages → update them.
- Indirect pages where the current text would become **incorrect** → update them.
- Indirect pages where the update is merely **nice to have** → flag in output
  notes, do not expand scope without user confirmation.

## 3. Read the existing page before editing

Before touching a file, understand:

| Aspect | What to look for |
| --- | --- |
| Structure | Heading hierarchy, section order, content flow |
| Voice | Terse vs. explanatory, imperative vs. descriptive |
| Pattern | How similar items on this page are documented |
| Terminology | Which terms are used — do not introduce synonyms |
| Scope | What the page covers and explicitly excludes |
| Sort order | Alphabetical, logical grouping, or chronological |

**Key principle:** the updated section must read as if written by the same author
as the rest of the page. New content should not stand out stylistically, and it
must follow the same Chinese/English spacing, punctuation, and terminology choices.

## 4. Plan the edit

For each target page, determine:

- **Where**: which section, which position within the section.
- **What**: add, change, or remove.
- **How much**: surrounding context to adjust for flow.

### Placement conventions

| Page type | Typical order |
| --- | --- |
| System variables | Alphabetical by name |
| Config parameters | Grouped by `[section]`, then by functionality |
| SQL statement page | Synopsis → Description → Examples → See also |
| Function reference | Syntax → Parameters → Return → Examples |
| Feature page | Intro → Usage → Limitations → Compatibility |

When adding a new item to a list, table, or parameter section:

- Insert in the correct sort position.
- Match the existing format exactly (fields, punctuation, backticks, spacing).
- Do not reorder existing items unless fixing a clear sorting error.

## 5. Write — match style and format

### Match the entry format

Study 2–3 neighboring entries on the same page and replicate their pattern.

**System variable entry example:**

```markdown
### variable_name

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`100`
- 取值范围：`[0, 10000]`
- 这个变量用于控制……
```

**Config parameter entry example:**

```markdown
### `parameter-name`

- 默认值：`value`
- 取值范围：`[min, max]`
- 说明该参数控制的行为。
```

New entries must follow the identical field order, punctuation, and detail level as the neighbors on the same page. Always copy the exact field labels already used on that page rather than inventing new ones.

### Match voice and depth

- If the page uses terse descriptions → keep new content terse.
- If the page writes full paragraphs → write comparably.
- If the page includes examples for each item → add an example.
- If the page omits examples → do not add one only for the new item unless
  critical for understanding.

### Version annotations

For version-specific changes, use the established format on the page:

- "从 vX.Y 起，……" or "本变量从 vX.Y 起引入。"
- For behavior changes, state both old and new behavior when helpful.
- Ensure version notes are accurate for the target branch.

### Additions vs. modifications vs. removals

**Adding** (new param, new section, new example):

- Follow the format of adjacent entries.
- Maintain heading level hierarchy.
- Add transitional context if needed for flow.

**Modifying** (changed default, updated behavior):

- Change only the specific facts that changed.
- Preserve sentence structure and style when possible.
- Add a version note if the change is version-specific.
- If breaking, add a warning.

**Removing** (deprecated feature, removed limitation):

- Remove cleanly; check for orphaned references on the same page.
- For deprecated features, add a deprecation note rather than deleting docs for
  still-functional features.
- Link to the replacement or migration path.

## 6. Verify cross-document consistency

After editing, check:

- [ ] Same fact appears in multiple docs → all updated?
- [ ] Changed a heading → anchors/links from other docs still valid?
- [ ] Feature gained capabilities → summary/overview pages still accurate?
- [ ] Behavior changed for MySQL compat → `mysql-compatibility.md` updated?
- [ ] Default changed → examples relying on old default still correct?
- [ ] Removed content → no orphaned cross-references remain?

## 7. Validate

```bash
./scripts/markdownlint <changed-files>
./scripts/verify-links.sh        # if headings/anchors/links changed
./scripts/verify-link-anchors.sh # if anchors changed
```

Also:

- [ ] Re-read the changed section with 2–3 surrounding sections — does it flow
      naturally?
- [ ] Facts match the source (code PR, issue, spec)?
- [ ] For procedural content, mentally trace the steps with the new info.
- [ ] No style discontinuity between new and existing content (spacing, punctuation, terminology).

## Common update patterns

### New system variable

1. Add entry in `system-variables.md` in alphabetical order, matching format.
2. Add to `system-variable-reference.md` if applicable.
3. Update the feature page to mention the variable.
4. If the variable controls a new feature, the feature doc is primary; the
   variable entry should link to it.

### New config parameter

1. Add entry in `*-configuration-file.md` under the correct `[section]`.
2. Match the exact format of neighbors.
3. If there is a corresponding CLI flag, update the flag doc too.

### Changed default value

1. Change the value in the parameter/variable description.
2. Add version note ("从 vX.Y 起，默认值变更为……").
3. Check if examples elsewhere assume the old default.
4. If breaking, add a compatibility/warning note.

### Removed limitation

1. Update the feature doc's limitations section.
2. Update `tidb-limitations.md` if listed there.
3. Remove or mark as unnecessary any workaround documentation.

### Deprecation

1. Add deprecation notice with version and expected removal timeline.
2. Update "recommended" guidance that points to the deprecated feature.
3. Link to the replacement.
4. Keep documentation for still-functional deprecated features.

## Common mistakes

- Updating one occurrence but missing the same fact in other docs.
- Breaking format/style consistency with surrounding entries.
- Expanding scope into unrelated improvements.
- Adding version notes inaccurate for the target branch.
- Leaving orphaned references when removing content.
- Introducing new terminology that conflicts with existing usage on the page or `resources/tidb-terms.md`.
- Rewriting surrounding text unnecessarily while making a targeted edit.
