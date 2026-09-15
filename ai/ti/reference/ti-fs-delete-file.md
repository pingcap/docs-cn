---
title: ti fs delete-file
summary: 从 TiDB Cloud Filesystem 中删除文件。
---

# ti fs delete-file

删除远程文件或目录。该命令的别名是 `ti fs rm`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs delete-file
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--recursive]
  [--version]
```

## 选项 {#options}

- `--path <string>`：TiDB Cloud 文件系统中的文件或目录路径。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--recursive`：递归删除目录。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 删除远程文件：

    ```bash
    # Remove one object from the selected Filesystem.
    ti fs delete-file --file-system-id <file-system-id> --path /reports/obsolete.md
    ```

- 递归删除目录：

    ```bash
    # Remove a directory and all of its descendants in one request.
    ti fs delete-file --file-system-id <file-system-id> --path /scratch --recursive
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)