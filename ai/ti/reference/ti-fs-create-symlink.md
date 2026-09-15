---
title: ti fs create-symlink
summary: 在 TiDB Cloud Filesystem 中创建符号链接。
---

# ti fs create-symlink

创建一个符号链接。该命令的别名是 `ti fs symlink`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-symlink
  --link-path <string>
  --target <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--link-path <string>`：已创建符号链接的文件路径。\[required]
- `--target <string>`：被链接到的实际文件路径。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个符号链接：

    ```bash
    # Create a relative symbolic link inside the remote namespace.
    ti fs create-symlink --file-system-id <file-system-id> --target final.md --link-path /reports/latest.md
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)