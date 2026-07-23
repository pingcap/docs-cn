---
title: 在 TiDB Cloud 文件系统中为 Agent 准备 Git Workspace
summary: 快速显示大型 Git workspace，在后台 hydrate clean object，并让 Agent 在完整下载结束前开始工作。
---

# 在 TiDB Cloud 文件系统中为 Agent 准备 Git Workspace

本示例将大型仓库 clone 从 Agent 启动任务的关键路径中移除。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## Agent 面临的问题

临时 Agent 通常需要等待 `git clone` 和 checkout 下载完整仓库，才能查看文件树并开始工作。对于大型 monorepo，每次替换沙箱都要重新承受这段启动延迟，即使 Agent 的第一个任务只需要仓库中的少量文件，它仍然只能等待。

## 普通 clone 和 partial clone 为什么不够

普通 clone 会一直阻塞到初始 object transfer 和 checkout 完成。原生 blobless partial clone 可以减少首次传输，但后续 Git 命令和文件读取仍可能在 Agent 的关键路径上触发大量按需 fetch。这两种方式本身也不提供可在不同 Agent runtime 之间恢复的共享文件系统 workspace。

## tdc 如何改变工作流

`tdc fs-git clone-git-workspace --blobless --hydrate background` 会注册 Git workspace，并在所有 clean blob 下载完成前先显示文件树。命令返回后，Agent 可以立即查看路径并开始工作，同时 tdc 在后台 hydrate clean tree 和本地 Git object database。Hydration 尚未完成时发生的读取会回退到 Git lazy fetch，以保证正确性。编辑、commit、fetch 和 push 仍然使用普通 Git。

## 前置条件

- 选择一个文件系统。
- 使用 Linux FUSE，或者在 macOS 安装 macFUSE 并显式使用 `--driver fuse`。
- 安装 Git 并配置 repository authentication。

## 第 1 步：挂载 workspace

```bash
mkdir -p /path/to/workspace
tdc fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

## 第 2 步：创建 workspace 并在后台 hydrate

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate background
```

此时 workspace 文件树已经可见，hydration 会继续在后台运行。Agent 可以立即执行普通命令：

```bash
find /path/to/workspace/tidb -maxdepth 2 -type f | head
git -C /path/to/workspace/tidb status
```

在运行确定性 benchmark 或 drain 挂载之前，可以显式等待 hydration 完成：

```bash
tdc fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

## 第 3 步：创建 agent worktree

```bash
tdc fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-agent-task \
  --branch-name agent-task
```

Agent 可以使用普通工具：

```bash
git -C /path/to/workspace/tidb-agent-task status
```

删除 worktree 前 commit 或 push 需要保留的变更。

## 清理

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

tdc fs drain-file-system --mount-path /path/to/workspace
tdc fs unmount-file-system --mount-path /path/to/workspace
```

只有可以丢弃未提交变更时，才为 worktree removal 使用 `--force`。

## 安全与 durability 说明

- Repository credentials 由 Git 管理，不属于 tdc。
- Coding-agent profile 为提高性能，将 `.git` 和 ignored generated file 保存在本地。
- 删除临时机器前，对无法重建的本地 overlay 状态执行保留或 pack。

## 后续步骤

- [在 TiDB Cloud 文件系统中使用 Git Workspace](/ai/tdc/guides/tdc-filesystem-git.md)
- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
