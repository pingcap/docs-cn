---
title: ti fs-journal read-journal-entries
summary: 从文件系统日志（Journal）中读取条目。
---

# ti fs-journal read-journal-entries

按顺序从单个 journal 中读取条目。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-journal read-journal-entries
  --journal-id <string>
  [--after-seq <int64>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--version]
```

## 选项 {#options}

- `--journal-id <string>`：Journal ID。\[必需]
- `--after-seq <int64>`：读取此序列号之后的条目。如果省略或设置为 `0`，则从最早的条目开始读取。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，此命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，则此命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--limit <int32>`：最多读取的条目数。\[默认值：100]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 读取 journal 条目：

    ```bash
    # Return the first page of ordered entries for a journal.
    ti fs-journal read-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo
    ```

- 从某个序列号之后继续读取：

    ```bash
    # Read the next page after the last sequence processed by a consumer.
    ti fs-journal read-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --after-seq 100 --limit 50
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)