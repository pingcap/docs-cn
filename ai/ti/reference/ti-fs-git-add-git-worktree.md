---
title: ti fs-git add-git-worktree
summary: 在已挂载的 TiDB Cloud Filesystem 中添加一个链接的 Git 工作树。
---

# ti fs-git add-git-worktree

从基础工作区添加一个链接的 Git 工作树。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-git add-git-worktree
  --base-path <string>
  --worktree-path <string>
  [--blobless]
  [--branch-name <string>]
  [--commit-ish <string>]
  [--detach]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--hydrate <string>]
  [--version]
```

## 选项 {#options}

- `--base-path <string>`：基础 Git 工作区的已挂载文件系统路径。\[必需]
- `--worktree-path <string>`：链接工作树的已挂载文件系统路径。\[必需]
- `--blobless`：验证基础工作区是否使用 blobless Git 存储。此选项不会将非 blobless 工作区转换为 blobless。
- `--branch-name <string>`：为链接工作树创建一个分支。
- `--commit-ish <string>`：链接工作树的可选 commit-ish。
- `--detach`：创建一个 detached 的链接工作树。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--hydrate <string>`：clean-data hydration 模式：`auto`、`background`、`sync` 或 `off`。使用 `auto` 时，链接到 blobless 基础工作区的工作树会在后台执行 hydration，而链接到非 blobless 基础工作区的工作树不会执行单独的 hydration 步骤。`background` 和 `sync` 要求基础工作区为 blobless；`off` 会跳过 hydration。\[默认值：auto]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 在新分支上创建一个工作树：

    ```bash
    # Give an agent an isolated branch while sharing the base Git object store.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-feature --branch-name feature-x
    ```

- 创建一个 detached 工作树：

    ```bash
    # Inspect a commit without creating or switching a branch.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-review --commit-ish origin/main --detach
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)