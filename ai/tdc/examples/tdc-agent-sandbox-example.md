---
title: 在 Agent Sandbox 中使用 TiDB Cloud 文件系统
summary: 在可信机器上创建文件系统，并让全新的 Agent 沙箱在没有 TiDB Cloud API key 的情况下访问。
---

# 在 Agent Sandbox 中使用 TiDB Cloud 文件系统

本示例让临时 Coding Agent 获得持久工作区，而不需要将用户完整的 tdc 配置复制到沙箱中。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## Agent 面临的问题

Coding Agent 通常运行在全新、短生命周期的沙箱中。沙箱被替换后，本地磁盘随之消失，但 Agent 仍然需要之前生成的产物、仓库状态以及其他 worker 写入的文件。重复构建这些状态会浪费任务时间，而复制 `~/.tdc/` 或注入 TiDB Cloud API key，又会让沙箱获得并不需要的控制面权限。

## 本地存储和完整云凭证为什么不够

沙箱本地目录速度快，但既不持久也不能共享。通用对象存储 API 需要应用自行实现上传和下载逻辑，无法直接支持普通文件操作。给每个沙箱提供用户的完整云凭证虽然能够访问资源，却扩大了安全边界。

## tdc 如何改变工作流

可信机器只需创建一次文件系统。沙箱仅接收文件系统 owner token、region code 和文件系统名称，无需运行 `tdc configure`，即可使用 data plane、挂载、Git、Journal 和 Vault。Agent 只需要访问特定 secret 时，应使用委派的 Vault token，而不是 owner token。

## 前置条件

- 在可信机器上安装并配置 tdc。
- 在 sandbox 中安装 tdc。Release installer 包含 `tdc-drive9`。
- 使用 secret manager 或加密的 sandbox input 传递 token。

## 第 1 步：在可信机器上创建文件系统

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name agent-sandbox \
  --query fs_token \
  --output text)"
```

记录该 profile 使用的 canonical region code，例如 `aws-us-east-1`。不要输出 token。

## 第 2 步：注入最小 sandbox 环境

通过 sandbox secret/environment 机制配置：

```bash
TDC_FS_TOKEN=<owner-token>
TDC_REGION_CODE=aws-us-east-1
TDC_FS_FILE_SYSTEM_NAME=agent-sandbox
```

Sandbox 不需要 `TDC_PUBLIC_KEY`、`TDC_PRIVATE_KEY`、`tdc configure`，也不需要从 `~/.tdc/` 复制文件。

## 第 3 步：验证直接访问

在 sandbox 中：

```bash
printf 'sandbox ready\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /sandbox/status.txt

tdc fs read-file --path /sandbox/status.txt
```

预期输出：

```text
sandbox ready
```

## 第 4 步：可选挂载文件系统

在 Linux FUSE 环境中：

```bash
mkdir -p /workspace
tdc fs mount-file-system \
  --file-system-name agent-sandbox \
  --mount-path /workspace \
  --driver fuse

cat /workspace/sandbox/status.txt
```

在 macOS 上省略 `--driver fuse`，使用默认 WebDAV。只有安装 macFUSE 后才使用 FUSE。

挂载后，可以使用同一 FS 环境运行 `tdc fs-git`、`tdc fs-journal` 和 owner 授权的 `tdc fs-vault`。Agent 只需要指定 secret field 时，应提供 delegated `TDC_VAULT_TOKEN`，而不是 owner token。

## 清理

停止 writer。对于 FUSE：

```bash
tdc fs drain-file-system --mount-path /workspace
tdc fs unmount-file-system --mount-path /workspace
```

对于 WebDAV，关闭文件并只运行 unmount。回到可信机器：

```bash
tdc fs delete-file-system \
  --file-system-name agent-sandbox \
  --confirm-file-system-name agent-sandbox
```

## 安全说明

- 将 `TDC_FS_TOKEN` 视为 owner credential。
- 不要将其写入镜像、代码仓库、命令行参数或操作日志。
- 删除 sandbox 不会删除远端文件系统。
- 如果 pending write 必须持久化，请在删除 FUSE sandbox 前执行 drain。

## 后续步骤

- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
