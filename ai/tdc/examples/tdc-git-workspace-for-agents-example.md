---
title: 在 TiDB Cloud 文件系统中为 Agent 准备 Git Workspace
summary: 挂载文件系统、创建快速 Git workspace 与 linked worktree、正常使用 Git 并安全清理。
---

# 在 TiDB Cloud 文件系统中为 Agent 准备 Git Workspace

本示例为 agent 准备 repository 和隔离的 linked worktree。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

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

## 第 2 步：Clone 并 hydrate

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

验证：

```bash
git -C /path/to/workspace/tidb status
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
