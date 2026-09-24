---
title: 在 Agent 沙箱中使用 TiDB Cloud Filesystem
summary: 在受信任的机器上预配文件系统，并让一个干净的 agent 沙箱在无需 TiDB Cloud API keys 和配置的情况下进行访问。
---

# 在 Agent 沙箱中使用 TiDB Cloud Filesystem

此工作流可为临时的编码 agent 提供一个持久、共享的工作区，而无需将用户完整的 TiDB Cloud CLI 配置复制到沙箱中。当沙箱的本地磁盘是一次性的，但 agent 需要使用来自先前会话或其他工作节点的产物、仓库状态或文件，并且不希望为每个沙箱都重新构建这些状态时，可以使用此工作流。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

> **Note:**
>
> 如需亲手实践此工作流，请打开 [TiDB Cloud Filesystem for Agent Sandbox Lab](https://labs.tidb.io/labs/demo_901)。此交互式 Lab Guide 将引导你在 agent 沙箱中使用持久化的文件系统。

## 工作原理 {#how-it-works}

受信任的机器只需预配一次文件系统。沙箱仅接收文件系统所有者令牌和 Region 代码，因此它可以使用普通文件操作，以及数据平面、挂载、Git、日志（Journal）和 Vault 工作流，而无需执行 `ti configure`、复制 `~/.ti/` 目录或使用 TiDB Cloud API keys。这也避免了通用对象存储 API 所需的、与应用相关的上传和下载逻辑。该令牌用于标识文件系统。当 agent 只需要部分选定的 Secret 时，请使用 Vault 委派令牌而不是所有者令牌。

## 前提条件 {#prerequisites}

- 在受信任的机器上安装并配置 TiDB Cloud CLI。
- 在沙箱中使用发布安装程序安装 TiDB Cloud CLI。
- 在受信任的机器上安装 `jq`。
- 使用安全的 Secret 管理器或加密的沙箱输入来传输令牌。

## 第 1 步：在受信任的机器上进行预配 {#step-1-provision-on-the-trusted-machine}

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

将令牌存储到 Secret 管理器中，记录 `FILE_SYSTEM_ID` 以便进行控制平面清理，并记录创建文件系统时使用的 Region 代码。在安全存储令牌后，删除 `filesystem.json`。

## 第 2 步：注入最小化的沙箱环境 {#step-2-inject-the-minimum-sandbox-environment}

使用以下内容配置沙箱的 Secret/环境变量机制：

```bash
TI_FS_TOKEN=<owner-token>
TI_REGION_CODE=<filesystem-region-code>
```

沙箱不需要 `TIDB_CLOUD_PUBLIC_KEY`、`TIDB_CLOUD_PRIVATE_KEY`、`ti configure`，也不需要从 `~/.ti/` 复制文件。

## 第 3 步：验证直接访问 {#step-3-verify-direct-access}

在沙箱中：

```bash
printf 'sandbox ready\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /sandbox/status.txt

ti fs read-file --path /sandbox/status.txt
```

预期输出：

```text
sandbox ready
```

## 第 4 步：可选地挂载文件系统 {#step-4-optionally-mount-the-file-system}

在使用 FUSE 的 Linux 上：

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --mount-path "$HOME/workspace" \
  --driver fuse

cat "$HOME/workspace/sandbox/status.txt"
```

在 macOS 上，省略 `--driver fuse` 以使用 WebDAV，这不需要安装 FUSE。当你需要 Git 工作区、layer 或在线刷写等 FUSE 特有能力时，请安装 macFUSE 并选择 FUSE。有关平台要求和挂载路径限制，请参见[挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)。

挂载后，你可以在相同的 FS 环境中使用 `ti fs-git`、`ti fs-journal` 和由所有者授予权限的 `ti fs-vault` 命令。当 agent 只需要部分选定的 Secret 字段时，请向其提供委派的 `TI_VAULT_TOKEN`，而不是所有者令牌。

## 清理 {#cleanup}

停止写入方并卸载。优雅的 FUSE 卸载会自动刷写并处理待完成的工作：

```bash
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

对于 FUSE 挂载，当你需要在保持挂载在线的同时验证远端持久性时，请单独使用 `ti fs drain-file-system --mount-path "$HOME/workspace"`。WebDAV 不支持 `drain-file-system`。更多信息，请参见[安全完成](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。然后回到受信任的机器上：

```bash
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## 安全与运维说明 {#security-and-operational-notes}

- 将 `TI_FS_TOKEN` 视为所有者凭证。
- 不要将其放入镜像、仓库、命令行参数或操作日志中。
- 删除沙箱不会删除远端文件系统。
- 优雅的卸载会刷写待处理的 FUSE 写入；不经卸载直接删除沙箱则不会。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)