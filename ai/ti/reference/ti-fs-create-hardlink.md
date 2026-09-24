---
title: ti fs create-hardlink
summary: 在文件系统中创建硬链接。
---

# ti fs create-hardlink

为现有远程路径创建一个硬链接。该命令的别名是 `ti fs hardlink`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-hardlink
  --link-path <string>
  --source-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--link-path <string>`：在 TiDB Cloud 文件系统中创建的硬链接的文件路径。\[必需]
- `--source-path <string>`：TiDB Cloud 文件系统中现有文件的路径。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建硬链接：

    ```bash
    # Expose the same remote file content at a second path.
    ti fs create-hardlink --file-system-id <file-system-id> --source-path /reports/final.md --link-path /reports/final-copy.md
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)