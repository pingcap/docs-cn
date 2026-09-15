---
title: ti fs list-files
summary: 列出 TiDB Cloud Filesystem 中的文件。
---

# ti fs list-files

列出远程路径下的条目。该命令的别名是 `ti fs ls`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs list-files
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--path <string>]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--path <string>`：文件系统目录路径。\[默认值：/]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出远程目录：

    ```bash
    # Return the entries under a specific Filesystem path.
    ti fs list-files --file-system-id <file-system-id> --path /reports
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)