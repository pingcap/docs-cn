---
title: ti fs copy-file
summary: 复制文件到文件系统、从中复制文件，或在其中复制文件。
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

- `--append`：将本地文件的内容追加到文件系统中的某个文件。
- `--create-parents`：从文件系统复制文件时，创建缺失的本地父目录。
- `--description <string>`：用于 `--to-remote` 操作的文件描述。
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--from-local <string>`：本地源路径。请使用纯文件系统路径。形如 `file:///path` 的 URL scheme 会被拒绝。
- `--from-remote <string>`：文件系统中的源路径。
- `--from-stdin`：从 stdin 读取并写入到 `--to-remote`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统存储的本地令牌。
- `--help`：显示帮助信息。
- `--layer-id <string>`：将复制的单个文件写入文件系统 layer，而不是基础文件系统。不能与 `--recursive` 组合使用。
- `--overwrite`：替换已存在的目标。上传或下载会直接覆盖目标。在文件系统内复制时（`--from-remote` 与 `--to-remote`），文件系统不会替换已存在的路径，因此 `ti` 会先将源文件复制到名为 `<destination>.ti-tmp-<id>` 的临时同级路径，再将其重命名到目标位置。该重命名会一步替换目标，因此读方只会看到之前的文件或完整的新文件。此操作需要对源和目标具有读权限，并对目标所在目录具有读、写和删除权限。如果重命名失败且 `ti` 无法删除临时文件，错误信息会给出该路径。请使用相同的 `--file-system-id` 和具有删除权限的令牌，通过 `ti fs delete-file --path <temporary-path>` 删除它。使用 `--recursive` 时，`--overwrite` 不生效：复制不会经过暂存或重命名；如果目标路径已存在，命令会在复制任何文件之前停止。
- `--recursive`：递归复制目录结构。不能与 `--layer-id` 组合使用；如需向 layer 目录写入数据填充内容，请改用可写的 FUSE 挂载。
- `--resume`：恢复一个正在进行的复制操作。
- `--tag <string>`：为 `--to-remote` 操作创建 `key=value` 标签；可重复指定。
- `--to-local <string>`：本地目标路径。请使用纯文件系统路径。形如 `file:///path` 的 URL scheme 会被拒绝。
- `--to-remote <string>`：文件系统中的目标路径。
- `--to-stdout`：将 `--from-remote` 写入 stdout。
- `--version`：显示版本信息。

如果目标是已存在的目录，或路径以分隔符结尾，文件会被复制到 `<destination>/<source-file-name>`。不使用 `--overwrite` 时，命令在解析出的目标已存在时停止。有两个例外：使用 `--resume` 的下载（`--from-remote` 与 `--to-local`）会跳过此检查并替换已存在的本地文件，因此恢复前请保护好该文件；使用 `--layer-id` 时也会跳过此检查，命令直接写入 layer 并替换该路径上已存在的文件。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 上传本地文件：

    ```bash
    # Copy a local report into the selected remote file system.
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

- 替换已有的远程文件：

    ```bash
    # Replace the published report with the draft, without downloading either file.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports/draft.md --to-remote /reports/report.md --overwrite
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

- 将标准输入流式传输到文件系统：

    ```bash
    # Upload generated content without creating an intermediate local file.
    printf 'ready\n' | ti fs copy-file --file-system-id <file-system-id> --from-stdin --to-remote /status.txt --tag source=stdin --description "generated status"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)