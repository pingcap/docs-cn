---
title: ti fs read-file
summary: 从文件系统读取文件。
---

# ti fs read-file

读取远程文件或字节范围，并将其输出到 stdout。该命令的别名是 `ti fs cat`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs read-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--length <int64>]
  [--offset <int64>]
  [--version]
```

## 选项 {#options}

- `--path <string>`：所选文件系统中的文件路径。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--length <int64>`：范围读取的字节长度。
- `--offset <int64>`：范围读取的从零开始的字节偏移。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 读取完整文件：

    ```bash
    # Write the remote file contents directly to standard output.
    ti fs read-file --file-system-id <file-system-id> --path /reports/report.md
    ```

- 读取字节范围：

    ```bash
    # Fetch only the requested range from a large remote object.
    ti fs read-file --file-system-id <file-system-id> --path /archives/large.bin --offset 1024 --length 4096
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)