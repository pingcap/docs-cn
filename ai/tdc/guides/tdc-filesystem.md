---
title: 使用 tdc 管理 TiDB Cloud 文件系统
summary: 管理文件系统资源、操作文件、使用 layer 和 pack，并通过内置 Drive9 companion 挂载文件系统。
---

# 使用 tdc 管理 TiDB Cloud 文件系统

使用 `tdc fs` 创建 TiDB Cloud 文件系统资源，并通过命令或本地挂载访问数据。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

- Provision 或删除文件系统前运行 `tdc configure`。
- 使用 release installer 安装 tdc，确保 `tdc-drive9` companion 位于 `tdc` 二进制旁。
- 将返回的 FS owner token 作为 secret 处理。

Data-plane 命令也可以通过 `TDC_FS_TOKEN`、`TDC_REGION_CODE` 和 `TDC_FS_FILE_SYSTEM_NAME` 使用已有文件系统，无需 TiDB Cloud API key。

## 管理文件系统资源

创建资源并将其设为 profile 默认值：

```bash
tdc fs create-file-system \
  --file-system-name workspace \
  --set-default \
  --wait
```

不指定 `--wait` 时，Drive9 接受异步创建请求后 tdc 立即返回。指定该 flag 后，tdc 最多等待 10 分钟，直到可以通过公开的 Drive9 data-plane CLI 读取根目录。等待失败不会删除资源或本地保存的凭证。

JSON 响应包含 `fs_token`。在不显示完整结果的情况下获取：

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name sandbox \
  --wait \
  --query fs_token \
  --output text)"
```

列出和查看本地已注册资源：

```bash
tdc fs list-file-systems
tdc fs describe-file-system --file-system-name workspace
```

设置或清除 profile 默认值：

```bash
tdc fs set-default-file-system --file-system-name workspace
tdc fs unset-default-file-system
```

检查所选资源和 companion：

```bash
tdc fs check-file-system --file-system-name workspace
```

删除资源前，先移除或保留需要的数据：

```bash
tdc fs delete-file-system \
  --file-system-name workspace \
  --confirm-file-system-name workspace
```

Create 和 delete 支持 `--dry-run`。删除需要 TiDB Cloud API key 和本地已注册资源；仅有 FS token 不能删除资源。Drive9 的删除是异步操作，请求成功被接受时返回 `status: "deleting"`，同时 tdc 会移除所选资源的本地 registry entry 和凭证。

## 在多个文件系统中选择

一个 profile 可以拥有多个资源。选择优先级为：

1. `--file-system-name`；
2. `TDC_FS_FILE_SYSTEM_NAME`；
3. profile 默认值；
4. 唯一的已注册资源。

选择存在歧义时，tdc 会失败，绝不会随机选择文件系统。

## 复制和读取数据

上传、下载和远端复制：

```bash
tdc fs copy-file --from-local ./README.md --to-remote /workspace/README.md
tdc fs copy-file --from-remote /workspace/README.md --to-local ./README.copy.md --create-parents
tdc fs copy-file --from-remote /workspace/README.md --to-remote /archive/README.md
```

使用 `--overwrite` 替换已有 target，使用 `--resume` 恢复受支持的中断上传或下载，使用 `--recursive` 复制目录：

```bash
tdc fs copy-file --from-local ./src --to-remote /workspace/src --recursive
tdc fs copy-file --from-local ./large.bin --to-remote /workspace/large.bin --resume
```

追加和 stream：

```bash
tdc fs copy-file --from-local ./tail.log --to-remote /logs/app.log --append
printf 'hello\n' | tdc fs copy-file --from-stdin --to-remote /workspace/stdin.txt
tdc fs copy-file --from-remote /workspace/stdin.txt --to-stdout
```

上传时添加 metadata：

```bash
tdc fs copy-file \
  --from-local ./report.md \
  --to-remote /workspace/report.md \
  --tag owner=agent \
  --tag stage=review \
  --description "agent review report"
```

读取完整文件或 byte range：

```bash
tdc fs read-file --path /workspace/report.md
tdc fs read-file --path /workspace/large.bin --offset 1024 --length 4096
```

## 查看和修改 namespace

```bash
tdc fs list-files --path /workspace
tdc fs describe-file --path /workspace/report.md
tdc fs create-directory --path /workspace/archive --mode 0755
tdc fs move-file --from-remote /workspace/report.md --to-remote /workspace/archive/report.md
tdc fs chmod-file --path /workspace/archive/report.md --mode 0600
tdc fs create-symlink --target archive/report.md --link-path /workspace/report.link
tdc fs create-hardlink --source-path /workspace/archive/report.md --link-path /workspace/report.hard
tdc fs delete-file --path /workspace/report.link
tdc fs delete-file --path /workspace/archive --recursive
```

修改 namespace 的命令支持 `--dry-run`。

搜索内容和 metadata：

```bash
tdc fs search-file-content --path /workspace --pattern "TODO" --limit 50
tdc fs find-files --path /workspace --file-name-pattern "*.md" --tag stage=review
```

`find-files` 还支持 resource type、时间、大小和结果数量筛选。两个 search 命令均接受 `--layer-id`。

## 使用 layer 和 checkpoint

Layer 在提交或丢弃之前记录 base root 上的变更：

```bash
tdc fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

使用返回的 layer ID：

```bash
tdc fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

tdc fs list-layers
tdc fs describe-layer --layer-id "<layer-id>"
tdc fs diff-layer --layer-id "<layer-id>"
tdc fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id before-review \
  --label "before review"
```

通过 rollback 或 commit 完成 layer：

```bash
tdc fs rollback-layer --layer-id "<layer-id>"
tdc fs commit-layer --layer-id "<layer-id>"
```

这两个命令表示同一任务的两种结果，实际 workflow 中不要依次执行两者。

## Pack 本地 overlay 状态

FUSE mount profile 可以将选定路径路由到本地 overlay storage。迁移到其他机器前，将这些路径 pack 到远端 archive：

```bash
tdc fs pack-file-system --mount-path /path/to/workspace
tdc fs unpack-file-system --mount-path /path/to/workspace
```

没有活跃 mount 时，提供 `--local-root`、`--remote-root` 和 `--mount-profile`。`--archive-path` 选择远端 archive，可重复的 `--path` 限制 pack 内容，`--no-replace` 让 unpack 进行 merge，而不是替换 manifest path。

## 挂载文件系统

创建本地 mount path，并在后台挂载：

```bash
mkdir -p /path/to/workspace
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace
```

默认 `--driver auto` 行为取决于平台。`--remote-path` 暴露子树，`--read-only` 禁止写入，`--foreground` 让 runtime 保持附着在终端。

### 平台行为

| 平台 | `--driver auto` | 可选或必要依赖 | 说明 |
| --- | --- | --- | --- |
| macOS | WebDAV | WebDAV 无需额外依赖 | 安装 macFUSE 并选择 `--driver fuse`，获得完整 FUSE 体验 |
| Linux | FUSE | FUSE3 和 `/dev/fuse` 访问权限；显式 WebDAV 需要 `davfs2` | FUSE 支持 drain 和 cache 控制 |
| Windows | WebDAV | Windows WebClient service | Mount path 必须是 `X:` 之类的 drive letter；不支持 FUSE 和 vault mount |

即使安装了 macFUSE，macOS 的自动选择也始终是 WebDAV。如需使用 FUSE，请从 [macFUSE 官网](https://macfuse.github.io/)安装受支持版本，完成 installer 要求的批准或重启，然后执行：

```bash
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace \
  --driver fuse
```

显式 FUSE 支持 cache 控制：

```bash
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace \
  --driver fuse \
  --cache-dir "$HOME/.tdc/cache/workspace" \
  --read-cache-size-mb 256 \
  --read-cache-max-file-mb 16 \
  --read-cache-ttl 30s
```

默认 mount profile 是 `coding-agent`，会将 dependency、cache、generated output 和 Git 内部状态等常见开发数据保留在本地 overlay。这些 local-only 文件不会在机器删除后保留，除非执行 pack 或保留本地 volume。需要自动 portable pack 行为时使用 `--mount-profile portable`；不需要 coding-agent overlay policy 时使用 `none`。

## Drain 和 unmount

清理前停止 writer 并关闭打开的文件。对于 FUSE：

```bash
tdc fs drain-file-system \
  --mount-path /path/to/workspace \
  --timeout 30s

tdc fs unmount-file-system \
  --mount-path /path/to/workspace
```

Drain 等待 dirty handle 和 pending write，不支持 WebDAV。`unmount-file-system` 还支持 `--timeout`、`--force`、`--ignore-absent`、`--pack-archive-path` 和 `--no-auto-pack`。

后台 mount 成功后，会在 `~/.tdc/mounts/` 写入非敏感 locator。同一个 `HOME` 下的 drain 和 unmount 可以使用该 locator，无需再次提供 `TDC_FS_TOKEN` 或 `TDC_REGION_CODE`。

> **警告：**
>
> 不要在仍有 pending write 时终止 sandbox 或虚拟机。已提交到远端的数据可以保留，但内存写入、位于已删除本地磁盘上的 write-back 数据，以及 coding-agent local-only 文件可能丢失。

## Unix 风格 alias

Alias 只修改命令名称。所有 flag 保持长名称，并与 canonical command 一致。

| Alias | Canonical command |
| --- | --- |
| `tdc fs cp` | `tdc fs copy-file` |
| `tdc fs cat` | `tdc fs read-file` |
| `tdc fs ls` | `tdc fs list-files` |
| `tdc fs stat` | `tdc fs describe-file` |
| `tdc fs mv` | `tdc fs move-file` |
| `tdc fs rm` | `tdc fs delete-file` |
| `tdc fs mkdir` | `tdc fs create-directory` |
| `tdc fs chmod` | `tdc fs chmod-file` |
| `tdc fs symlink` | `tdc fs create-symlink` |
| `tdc fs hardlink` | `tdc fs create-hardlink` |
| `tdc fs grep` | `tdc fs search-file-content` |
| `tdc fs find` | `tdc fs find-files` |
| `tdc fs mount` | `tdc fs mount-file-system` |
| `tdc fs drain` | `tdc fs drain-file-system` |
| `tdc fs umount` | `tdc fs unmount-file-system` |

## 命令汇总

| 范围 | 命令 |
| --- | --- |
| 资源 | `create-file-system`、`list-file-systems`、`describe-file-system`、`set-default-file-system`、`unset-default-file-system`、`check-file-system`、`delete-file-system` |
| 数据 | `copy-file`、`read-file`、`list-files`、`describe-file`、`move-file`、`delete-file`、`create-directory`、`chmod-file`、`create-symlink`、`create-hardlink`、`search-file-content`、`find-files` |
| Layer | `create-layer`、`list-layers`、`describe-layer`、`diff-layer`、`create-layer-checkpoint`、`rollback-layer`、`commit-layer` |
| 可移植性 | `pack-file-system`、`unpack-file-system` |
| Mount | `mount-file-system`、`drain-file-system`、`unmount-file-system` |

## 后续步骤

- [在 Agent Sandbox 中使用文件系统](/ai/tdc/examples/tdc-agent-sandbox-example.md)
- [在不同机器间共享文件系统](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)
- [在 TiDB Cloud 文件系统中使用 Git Workspace](/ai/tdc/guides/tdc-filesystem-git.md)
