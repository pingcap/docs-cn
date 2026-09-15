---
title: TiDB Cloud Filesystem Git CLI 命令参考
summary: 参考所有 `ti fs-git` 命令，用于克隆、hydrate 和管理链接的 Git 工作树。
---

# TiDB Cloud Filesystem Git CLI 命令参考

`ti fs-git` 可加速在已挂载的 TiDB Cloud Filesystem 路径上设置 Git 工作区。对于 status、edit、add、commit、fetch 和 push，仍然使用常规的 `git` 命令。

## 命令 {#commands}

| 命令 | 说明 |
|---|---|
| [`clone-git-workspace`](/ai/ti/reference/ti-fs-git-clone-git-workspace.md) | 将仓库克隆到已挂载的 Filesystem 路径中。 |
| [`hydrate-git-workspace`](/ai/ti/reference/ti-fs-git-hydrate-git-workspace.md) | 为现有的快速或 blobless 工作区具体化干净的 Git 数据。 |
| [`add-git-worktree`](/ai/ti/reference/ti-fs-git-add-git-worktree.md) | 从基础工作区创建一个链接的工作树。 |
| [`remove-git-worktree`](/ai/ti/reference/ti-fs-git-remove-git-worktree.md) | 删除一个链接的工作树。 |

## 另请参阅 {#see-also}

- [在 TiDB Cloud Filesystem 上管理 Git 工作区](/ai/ti/guides/manage-git-workspaces.md)
- [在 TiDB Cloud Filesystem 上为 Agents 准备 Git 工作区](/ai/ti/guides/ti-git-workspace-for-agents-example.md)