---
title: ti fs chmod-file
summary: 更改 TiDB Cloud Filesystem 中的文件权限。
---

# ti fs chmod-file

更改远程路径的 POSIX 模式元信息。该命令的别名是 `ti fs chmod`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs chmod-file
  --mode <string>
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--mode <string>`：权限模式，使用八进制值表示，例如 0644。\[required]
- `--path <string>`：文件或目录路径。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 更改远程权限元信息：

    ```bash
    # Restrict the selected file to owner read and write access.
    ti fs chmod-file --file-system-id <file-system-id> --path /reports/final.md --mode 0600
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)