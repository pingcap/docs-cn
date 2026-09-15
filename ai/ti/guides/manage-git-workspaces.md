---
title: 在 TiDB Cloud Filesystem 上管理 Git 工作区
summary: 了解如何在已挂载的 TiDB Cloud Filesystem 上克隆、hydrate、创建链接工作树以及删除 Git 工作区。
---

# 在 TiDB Cloud Filesystem 上管理 Git 工作区

使用 `ti fs-git` 可以加速已挂载 TiDB Cloud Filesystem 上的 Git 工作区设置，同时在日常工作中继续使用常规 Git 命令。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 通过 FUSE [挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择已挂载的 Filesystem。请提供具有 Git 工作区权限的 FS token。
- 单独安装 Git 并配置仓库凭证。

## 克隆工作区 {#clone-a-workspace}

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

对于大型仓库，可添加 `--blobless --hydrate background`，以便立即使目录树可用。CLI 会在 clone 命令返回后启动一个后台进程，下载干净的文件内容和 Git 对象。如果你的工作流要求在命令返回前完成 hydrate，请使用 `--hydrate sync`。

## hydrate 现有工作区 {#hydrate-an-existing-workspace}

如果某个工作区是通过 `--blobless` 克隆的，你可以通过运行 `hydrate-git-workspace` 显式获取缺失的 Git 对象：

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

hydrate 会从远程仓库获取缺失的 blob 数据，同时不会丢弃你在工作树中的修改。

## 添加并使用链接工作树 {#add-and-use-a-linked-worktree}

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

创建完成后，即可在该链接工作树中使用常规 Git 命令。

## 删除工作树 {#remove-a-worktree}

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

CLI 会检查是否存在未提交的更改；如果工作树不是干净状态，则会拒绝删除。只有在你确认可以丢弃该工作树中的本地更改后，才使用 `--force`。

> **注意：**
>
> 在终止临时机器之前，请保留所需更改，删除不再使用的工作树，并优雅地卸载 Filesystem。

## 后续操作 {#what-s-next}

- [为 TiDB Cloud Filesystem 上的 Agents 准备 Git 工作区](/ai/ti/guides/ti-git-workspace-for-agents-example.md)
- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)