---
title: ti fs create-directory
summary: 在 TiDB Cloud Filesystem 中创建目录。
---

# ti fs create-directory

创建远程目录。该命令的别名是 `ti fs mkdir`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-directory
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--mode <string>]
  [--version]
```

## 选项 {#options}

- `--path <string>`：要创建的目录的文件系统路径。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--mode <string>`：目录模式，使用八进制值表示，例如 0755。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建远程目录：

    ```bash
    # Create the directory with explicit POSIX permission metadata.
    ti fs create-directory --file-system-id <file-system-id> --path /reports/archive --mode 0755
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)