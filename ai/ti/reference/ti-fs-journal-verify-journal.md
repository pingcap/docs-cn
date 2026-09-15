---
title: ti fs-journal verify-journal
summary: 验证一个 Filesystem 日志（Journal）的哈希链。
---

# ti fs-journal verify-journal

验证单个日志（Journal）哈希链的完整性。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-journal verify-journal
  --journal-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--journal-id <string>`：Journal ID。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 验证一个 Journal：

    ```bash
    # Validate the journal's ordered hash chain and integrity metadata.
    ti fs-journal verify-journal --file-system-id <file-system-id> --journal-id jrn-demo
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)