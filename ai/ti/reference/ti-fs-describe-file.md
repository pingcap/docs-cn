---
title: ti fs describe-file
summary: 描述 TiDB Cloud Filesystem 中的一个文件。
---

# ti fs describe-file

描述单个远程路径的元信息。该命令的别名是 `ti fs stat`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs describe-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--path <string>`：TiDB Cloud 文件系统中的文件或目录路径。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 描述远程文件：

    ```bash
    # Inspect file size, metadata, tags, and revision information.
    ti fs describe-file --file-system-id <file-system-id> --path /reports/report.md
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)