---
title: ti exec
summary: 在不将 Filesystem 挂载到本地的情况下，对 TiDB Cloud Filesystem 运行远程命令，保留工作区文件，选择执行选项，并安全地处理失败情况。
---

# ti exec

`ti exec` 可在不将 Filesystem 挂载到本地的情况下，对 TiDB Cloud Filesystem 运行命令。输出会流式传输到你的终端；远程退出状态会被保留。

> **Note:**
>
> Runtime 仅在 AWS Oregon (`us-west-2`) 和 AWS N. Virginia (`us-east-1`) 中可用。请使用 `aws-us-west-2` 或 `aws-us-east-1` 作为 CLI Region 代码。你需要在这些 Region 之一中拥有启用了 Runtime 的 Filesystem。CLI 对 `ti exec` 的支持不会在服务端启用 Runtime。

> **Warning:**
>
> 预览版 `ti exec` 功能的验证尚未完成。超时或取消请求可能会返回未知结果（`255`），且无法确认命令是否已经停止。在决定是否再次运行该命令之前，请先验证结果。

## Prerequisites {#prerequisites}

- 安装 TiDB Cloud CLI **v0.2.11 或更高版本**，并确保 `ti-drive9` companion 为最新版本。更早版本的 `ti` 不包含 `ti exec`。运行 `ti --version` 以检查已安装的版本。
- 在受支持的 Region 中[创建 Filesystem](/ai/ti/reference/ti-fs-create-file-system.md)，并保留其 ID 和所有者 Token。
- 为该 ID 使用本地存储的 Token，或在环境中设置 `TI_FS_TOKEN`。建议优先使用环境变量而不是 `--fs-token`，以避免在参数中暴露它。Vault 委派 Token 不能运行命令。路径作用域的 Token 不能挂载 sandbox。
- `ti exec --help` 仅检查本地命令是否存在。它不会验证 companion 或远程 Runtime。两者都必须支持 exec。

### Upgrade an existing installation {#upgrade-an-existing-installation}

升级前，请停止写入程序，并卸载所有 Filesystem 或 Vault 挂载。在 macOS 或 Linux 上，如果 `ti` 是以用户拥有的方式安装的，请更新到最新版本并验证版本：

```bash
ti update
ti --version
ti exec --help
```

当 `ti update` 安装了不同版本的 `ti` 时，也会替换 `ti-drive9` companion。如果 `ti` 已经是所请求的版本，更新程序不会刷新 companion。要在 macOS 或 Linux 上刷新过期的 companion，请重新运行 shell 安装程序；使用 `--install-dir` 可保留自定义安装目录。

在 Windows 上，请重新运行 PowerShell 安装程序；不支持原地自更新。安装步骤请参见[安装 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli)。

## Syntax and execution {#syntax-and-execution}

```text
ti exec [options] [--] command [arg...]
ti exec [options] 'shell command line'
```

将 `ti` 选项放在远程命令之前。其后的参数（包括 `--help`）都属于远程命令。单个 shell 命令行会由 `/bin/sh -c` 解释；多个参数则会被直接传递。

服务端会选择执行后端。轻量级 shell 执行器支持的命令可以在不启动 sandbox 的情况下运行。其他命令会在执行开始前使用 sandbox。仅凭 shell 语法本身并不能决定后端。命令一旦启动，失败后绝不会在另一个后端上重试。

Filesystem 可在 `/workspace` 访问。`/workspace` 之外的文件都是临时的。`--fresh` 会启动一个新的 sandbox，同时保留 Filesystem 数据。`-w` 用于选择工作目录；它不会将访问限制在该目录内。

## Example: process and read back a file {#example-process-and-read-back-a-file}

本示例要求本地有兼容 POSIX 的 shell，远程有 Python 3。

```bash
export TI_REGION_CODE=aws-us-east-1
export TI_FS_FILE_SYSTEM_ID='<file-system-id>'
workdir="runtime-demo-$(date +%s)"
ti fs create-directory --path "/$workdir"

# Inspect the directory without permitting writes.
ti exec --read-only -w "$workdir" ls

# Process data remotely and save the result in the Filesystem.
ti exec -w "$workdir" python3 -c \
  'from pathlib import Path; Path("result.txt").write_text("total=42\n")'

# Start a new sandbox and read the saved result.
ti exec --fresh -w "$workdir" cat result.txt
```

预期输出：

```text
total=42
```

请独立验证，然后删除示例目录：

```bash
ti fs read-file --path "/$workdir/result.txt"
ti fs delete-file --path "/$workdir" --recursive
```

## Options {#options}

| 选项 | 说明 |
| --- | --- |
| `--file-system-id ID` | 选择一个 Filesystem。也可以设置 `TI_FS_FILE_SYSTEM_ID`，或提供一个包含该 ID 的 Token。 |
| `--fs-token TOKEN` | 提供一个 Token。建议优先使用 `TI_FS_TOKEN`。否则，将使用所选 Filesystem 的本地存储 Token。 |
| `-w`, `--workspace PATH` | 选择远程工作目录。默认为匹配的本地 FUSE 目录，或 Filesystem 根目录。 |
| `-C`, `--cwd DIR` | 选择该工作目录中的一个子目录。 |
| `-e`, `--env KEY[=VALUE]` | 设置远程变量；仅提供 key 时会复制其本地值。可重复使用。 |
| `-t`, `--timeout DURATION` | 设置截止时间，例如 `30s` 或 `10m`。服务端可能会施加更短的限制。 |
| `--fresh` | 启动新的 sandbox，而不是复用现有 sandbox。 |
| `--layer REF` | 使用 layer ID、名称或 tag 引用。 |
| `--read-only` | 在执行期间阻止对 Filesystem 的写入。 |
| `-v`, `--verbose` | 在标准错误中显示执行细节。 |

在匹配的、由 `ti` 创建的 FUSE 挂载中，如果省略 `-w`，会上传待处理的本地写入并跟随当前目录。显式指定 `-w` 时，不会先上传本地更改。对于 WebDAV 挂载，请显式传入 `-w`。

## Failures and limitations {#failures-and-limitations}

已完成的命令会返回其精确的退出状态。使用最新的 `ti-drive9` companion 时，请结合错误消息来解释以下状态：

| 退出状态 | 含义 |
| --- | --- |
| `124` | 命令超时并已被停止。 |
| `125` | 执行器失败。输出或写入可能不完整。 |
| `126` | 命令不可执行。 |
| `127` | 未找到命令。 |
| `130` | 执行前取消、已确认取消，或在第二次按下 Ctrl-C 后分离。仅凭此状态并不能证明远程命令已停止。 |
| `255` | 结果未知。这种情况也可能发生在超时或取消请求之后。 |

命令本身也可能返回这些数字，因此仅凭退出状态无法识别原因。

- 不支持远程 stdin 和交互式终端。不支持 `--output`、`--query` 和 `--dry-run`。
- 按一次 Ctrl-C 以请求取消，并等待确认。再次按下会分离；命令可能仍在运行。
- 如果结果未知，请先检查 Filesystem，再决定是否重新运行命令。连接中断或缺少执行记录并不能证明执行已经停止。`ti exec` 绝不会自动重试。