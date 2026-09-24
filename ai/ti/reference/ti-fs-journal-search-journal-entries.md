---
title: ti fs-journal search-journal-entries
summary: 搜索文件系统日志（Journal）及其条目。
---

# ti fs-journal search-journal-entries

搜索日志（Journal），并可选择返回匹配的条目。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-journal search-journal-entries
  [--actor <string>]
  [--cursor <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--include-entries]
  [--journal-kind <string>]
  [--label <string>]
  [--limit <int32>]
  [--since <string>]
  [--status <string>]
  [--subject <string>]
  [--until <string>]
  [--version]
```

## 选项 {#options}

- `--actor <string>`：Actor，格式为 `type:id`。
- `--cursor <string>`：上一页返回的游标。继续查询时，请重复使用原始请求中的筛选条件。
- `--entry-type <string>`：条目类型筛选器。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--include-entries`：在匹配结果中包含完整的条目负载。
- `--journal-kind <string>`：日志（Journal）类型筛选器。
- `--label <string>`：标签筛选器，格式为 `key=value`；可重复指定。
- `--limit <int32>`：要读取的最大匹配数。\[默认值：100]
- `--since <string>`：时间下界，可以是相对时长（例如 `24h`）或 RFC3339 时间戳。
- `--status <string>`：条目状态筛选器。
- `--subject <string>`：主题筛选器；可重复指定。
- `--until <string>`：时间上界，必须为 RFC3339 时间戳。不接受相对时长。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 按条目类型搜索：

    ```bash
    # Find journals containing task-start events and include their payloads.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --entry-type task.started --include-entries
    ```

- 按标签和时间搜索：

    ```bash
    # Limit deployment journal matches to one environment and time window.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --label env=dev --since 2026-07-01T00:00:00Z --limit 100
    ```

- 按 actor 和 subject 搜索：

    ```bash
    # Find events produced by one agent for a specific task subject.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --actor agent:ti --subject issue-42 --include-entries
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)