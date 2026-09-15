---
title: ti fs copy-file
summary: 复制文件到 TiDB Cloud Filesystem、从中复制文件，或在其中复制文件。
---

# ti fs copy-file

在本地路径、远程路径、stdin 和 stdout 之间复制文件。该命令的别名是 `ti fs cp`。

请准确指定以下来源和目标组合中的一种：

| 来源 | 目标 |
| --- | --- |
| `--from-local` | `--to-remote` |
| `--from-stdin` | `--to-remote` |
| `--from-remote` | `--to-local` |
| `--from-remote` | `--to-stdout` |
| `--from-remote` | `--to-remote` |

`--append` 仅支持将 `--from-local` 与 `--to-remote` 搭配使用。不支持标准输入或远程来源。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs copy-file
  [--append]
  [--create-parents]
  [--description <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--from-local <string>]
  [--from-remote <string>]
  [--from-stdin]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--overwrite]
  [--recursive]
  [--resume]
  [--tag <string>]
  [--to-local <string>]
  [--to-remote <string>]
  [--to-stdout]
  [--version]
```

## 选项 {#options}

- `--append`：将本地文件的内容追加到 TiDB Cloud 文件系统中的某个文件。
- `--create-parents`：从 TiDB Cloud 文件系统复制文件时，创建缺失的本地父目录。
- `--description <string>`：用于 `--to-remote` 操作的文件描述。
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--from-local <string>`：本地源路径。
- `--from-remote <string>`：TiDB Cloud 文件系统中的源路径。
- `--from-stdin`：从 stdin 读取并写入到 `--to-remote`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 存储的本地令牌。
- `--help`：显示帮助信息。
- `--layer-id <string>`：将复制的单个文件写入文件系统 layer，而不是基础文件系统。不能与 `--recursive` 组合使用。
- `--overwrite`：替换已存在的目标文件。
- `--recursive`：递归复制目录结构。不能与 `--layer-id` 组合使用；如需向 layer 目录写入数据填充内容，请改用可写的 FUSE 挂载。
- `--resume`：恢复一个正在进行的复制操作。
- `--tag <string>`：为 `--to-remote` 操作创建 `key=value` 标签；可重复指定。
- `--to-local <string>`：本地目标路径。
- `--to-remote <string>`：TiDB Cloud 文件系统中的目标路径。
- `--to-stdout`：将 `--from-remote` 写入 stdout。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 上传本地文件：

    ```bash
    # Copy a local report into the selected remote Filesystem.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./report.md --to-remote /reports/report.md
    ```

- 下载远程文件：

    ```bash
    # Create missing local parent directories while downloading the file.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports/report.md --to-local ./downloads/report.md --create-parents
    ```

- 复制远程目录：

    ```bash
    # Duplicate a complete directory tree without downloading it locally.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports --to-remote /archive/reports --recursive
    ```

- 恢复大型上传：

    ```bash
    # Continue an interrupted local-to-remote transfer instead of restarting it.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./large.bin --to-remote /artifacts/large.bin --resume
    ```

- 追加到远程日志：

    ```bash
    # Add local log data to the existing remote object efficiently.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./tail.log --to-remote /logs/app.log --append
    ```

- 将标准输入流式传输到 Filesystem：

    ```bash
    # Upload generated content without creating an intermediate local file.
    printf 'ready\n' | ti fs copy-file --file-system-id <file-system-id> --from-stdin --to-remote /status.txt --tag source=stdin --description "generated status"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)