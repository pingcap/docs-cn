---
title: 在 TiDB Cloud 文件系统中使用 Git Workspace
summary: 在已挂载的 TiDB Cloud 文件系统中 clone、hydrate 并管理 linked Git worktree。
---

# 在 TiDB Cloud 文件系统中使用 Git Workspace

`tdc fs-git` 用于加速已挂载 TiDB Cloud 文件系统路径中的 Git workspace 初始化。它增强而不是替代 Git；status、edit、add、commit、fetch 和 push 仍使用普通 `git` 命令。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

- 通过 FUSE 挂载文件系统。Git workspace 加速依赖已挂载的文件系统 runtime。
- 安装 `git`，并独立配置 repository credentials。
- 确保 FS owner token 或所选 profile 能访问文件系统。

## Clone workspace

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

对于大型 repository，创建 blobless workspace 并同步 hydrate：

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

`--hydrate` 接受 `auto`、`background`、`sync` 或 `off`。

## Hydrate 已有 workspace

```bash
tdc fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Hydrate 为 fast 或 blobless workspace materialize clean Git object，不会丢弃 working-tree change。

## 添加 linked worktree

```bash
tdc fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

使用 `--detach` 创建 detached worktree，使用 `--commit-ish` 选择起始 revision；base workspace 使用 blobless mode 时，配合 `--blobless` 和 `--hydrate`。

正常使用 Git：

```bash
git -C /path/to/workspace/tidb-feature status
git -C /path/to/workspace/tidb-feature add .
git -C /path/to/workspace/tidb-feature commit -m "Implement feature x"
```

## 删除 worktree

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

默认拒绝删除 dirty worktree。只有确定可以丢弃本地变更时才使用 `--force`：

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature \
  --force
```

## Lifecycle 建议

终止临时机器前：

1. Commit 或以其他方式保留必要的 working-tree change。
2. 删除不再需要的 linked worktree。
3. Drain 文件系统 mount。
4. Unmount。

默认 coding-agent mount profile 将 `.git` 和可重建的 generated file 保存在本地 overlay。必须跨机器保留时，请保存或 pack 本地状态。

## 后续步骤

- [为 Agent 准备 Git Workspace](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md)
- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
