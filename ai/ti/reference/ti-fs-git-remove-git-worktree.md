---
title: ti fs-git remove-git-worktree
summary: 从已挂载的 TiDB Cloud Filesystem 中移除一个已链接的 Git 工作树。
---

# ti fs-git remove-git-worktree

移除一个已链接的 Git 工作树，同时保留其他工作树使用的共享 Git 数据。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-git remove-git-worktree
  --worktree-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--force]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--worktree-path <string>`：已链接工作树的已挂载 `ti fs` 路径。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--force`：即使已链接工作树存在本地更改，也强制移除。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 存储的本地令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 移除一个 Git 工作树：

    ```bash
    # Remove a clean linked worktree.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature
    ```

- 强制移除一个 Git 工作树：

    ```bash
    # Discard local changes only after deciding that they are no longer needed.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature --force
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)