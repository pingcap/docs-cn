---
title: ti fs-journal append-journal-entries
summary: 向文件系统日志（Journal）追加条目。
---

# ti fs-journal append-journal-entries

向日志（Journal）追加一个 JSON 事件或一个 JSON 数组。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-journal append-journal-entries
  --journal-id <string>
  [--dry-run]
  [--entry-json <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--idempotency-key <string>]
  [--json-array]
  [--source <string>]
  [--subject <string>]
  [--version]
```

## 选项 {#options}

- `--journal-id <string>`：Journal ID。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--entry-json <string>`：单个 JSON 日志条目对象；可重复指定。支持的字段请参见[条目 JSON 格式](#entry-json-format)。
- `--entry-type <string>`：当输入对象省略 `type` 时使用的条目类型。如果输入对象中显式指定了 `type`，则其优先级更高。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，该命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，该命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--idempotency-key <string>`：用于对同一追加请求的重试进行去重的键。如果省略，每次调用都会获得一个新的键。
- `--json-array`：从 stdin 读取 JSON 数组，而不是 JSONL。
- `--source <string>`：条目来源。
- `--subject <string>`：条目主题；可重复指定。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 条目 JSON 格式 {#entry-json-format}

每个输入对象支持以下字段：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `type` | string | 事件类型。除非 `--entry-type` 提供了默认值，否则为必填。它必须以小写字母开头，并且可以包含小写字母、数字、下划线（`_`）、句点（`.`）或连字符（`-`）。 |
| `schema_version` | integer | 事件负载的 schema 版本。小于 `1` 的值会使用 `1`。 |
| `status` | string | 可选的用户自定义状态。CLI 会将其转换为小写。 |
| `occurred_at` | RFC3339 时间戳 | 事件发生的时间。如果省略，则由服务提供该时间。 |
| `actor` | object | 可选的 actor 对象，包含 `type` 和 `id` 两个字符串字段。 |
| `source` | string | 事件来源。支持的值为 `self_reported`、`gateway_observed`、`server_observed` 和 `imported`。\[default: `self_reported`] |
| `parent_entry_id` | string | 可选的父事件 ID。 |
| `correlation_id` | string | 可选的 ID，用于将相关事件分组。 |
| `subjects` | array of strings | 采用 `type:id` 形式的主题。通过 `--subject` 提供的值会被添加到该数组中。 |
| `summary` | JSON value | 可选的内联事件负载。 |

当前不支持 artifact 引用。请勿在条目中包含 `artifacts` 或 `artifact_refs`。

如果指定了 `--source`，它会替换每个输入对象中的 `source` 值。`--entry-type` 仅适用于省略了 `type` 的对象。

> **Important:**
>
> 为了使追加操作能够安全重试，请为该逻辑请求选择一个幂等键，并在每次重试时复用该键。如果省略 `--idempotency-key`，重试会获得一个新的键，并且可能会追加重复条目。

## 示例 {#examples}

- 追加一个 JSON 条目：

    ```bash
    # Record an event object and let the CLI or service apply default metadata.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-json '{"type":"task.started"}'
    ```

- 追加一个幂等的类型化条目：

    ```bash
    # Prevent retries from recording the same completion event twice.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-type task.completed --subject issue:42 --idempotency-key issue-42-complete
    ```

- 从标准输入追加一个 JSON 数组：

    ```bash
    # Batch multiple ordered events in a single append operation.
    printf '[{"type":"step.started"},{"type":"step.completed"}]' | ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --json-array
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)