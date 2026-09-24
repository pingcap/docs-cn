---
title: 在 TiDB Cloud Filesystem 上为智能体准备 Git 工作区
summary: 快速让大型 Git 工作区可见，在后台补全干净对象，并让智能体在完整下载完成前开始工作。
---

# 在 TiDB Cloud Filesystem 上为智能体准备 Git 工作区

此工作流将大型仓库 clone 从启动智能体任务的关键路径中移除。当临时智能体需要在完整下载完成之前检查或修改大型仓库时，请使用此工作流。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 工作原理 {#how-it-works}

`ti fs-git clone-git-workspace --blobless --hydrate background` 会注册一个 Git 工作区，该工作区可以在替换后的智能体运行时之间共享，并且在所有干净 blob 完成下载之前就暴露其文件树。该命令会立即返回，因此智能体可以在 `ti` 于后台补全干净树和本地 Git 对象数据库的同时检查路径并开始工作。与普通 clone 不同，初始对象传输不会阻塞整个工作流。与仅使用原生 blobless partial clone 不同，后台补全可以减少智能体关键路径上重复的按需抓取。在补全完成前到达的读请求仍会回退到 Git 的惰性抓取，以保证正确性。普通 Git 仍然负责修改、提交、抓取和推送。

## 前提条件 {#prerequisites}

- 选择一个文件系统。
- 使用 Linux FUSE，或在 macOS 上安装 macFUSE 并显式指定 `--driver fuse`。Git 工作区依赖 FUSE 将远程 Git 树和工作区变更组合到挂载路径中；WebDAV 挂载不提供这种集成。
- 安装 Git 并配置仓库认证。

## 第 1 步：挂载工作区 {#step-1-mount-a-workspace}

```bash
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse \
  --mount-profile coding-agent
```

## 第 2 步：创建工作区并在后台补全 {#step-2-create-the-workspace-and-hydrate-in-the-background}

```bash
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate background
```

现在工作区树已可用，补全过程会在后台继续进行。让智能体使用普通命令开始工作：

```bash
find /path/to/workspace/tidb -maxdepth 2 -type f | head
git -C /path/to/workspace/tidb status
```

在执行确定性基准测试之前，或在对刷写挂载之前，你可以显式等待补全完成：

```bash
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

## 第 3 步：创建智能体工作树 {#step-3-create-an-agent-worktree}

```bash
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-agent-task \
  --branch-name agent-task
```

现在，智能体可以使用普通工具：

```bash
git -C /path/to/workspace/tidb-agent-task status
```

在移除工作树之前，请先提交或推送所需的更改。

## 清理 {#cleanup}

```bash
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

ti fs unmount-file-system --mount-path /path/to/workspace
```

仅当可以丢弃未提交更改时，才对工作树移除使用 `--force`。文件系统卸载会自动执行优雅的刷写；仅当你需要在不卸载的情况下将远程工作刷写出去时，才单独使用 `ti fs drain-file-system`。

## 安全与操作说明 {#security-and-operational-notes}

- 仓库凭据由 Git 管理，而不是 `ti`。
- `coding-agent` 挂载预设会将 Git 元信息、依赖关系目录、缓存、构建输出以及其他生成文件保留在本地机器上，以提升性能。
- 由 `coding-agent` 配置保留在本地的文件会随着临时机器消失。请提交或推送所需的 Git 更改，并使用带有显式 `--path` 值的 [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) 来保留其他无法重新构建的本地文件。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)