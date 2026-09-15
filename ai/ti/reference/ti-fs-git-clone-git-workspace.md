---
title: ti fs-git clone-git-workspace
summary: 将 Git 仓库克隆到已挂载的 TiDB Cloud Filesystem 中。
---

# ti fs-git clone-git-workspace

将仓库克隆到已挂载的 Filesystem 路径中。数据填充可以同步运行，也可以在后台运行。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-git clone-git-workspace
  --repo-url <string>
  --target-path <string>
  [--blobless]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--hydrate <string>]
  [--version]
```

## 选项 {#options}

- `--repo-url <string>`：Git 仓库 URL。\[必需]
- `--target-path <string>`：要克隆到的已挂载文件系统路径。\[必需]
- `--blobless`：创建无 blob 的部分本地 `.git`，并单独填充干净的 blob。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--hydrate <string>`：干净数据填充模式：`auto`、`background`、`sync` 或 `off`。使用 `auto` 时，无 blob 克隆会在后台进行填充，而非无 blob 克隆不会运行单独的填充步骤。`background` 和 `sync` 需要 `--blobless`；`off` 会跳过填充。\[默认值：auto]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 正常克隆一个仓库：

    ```bash
    # Create a complete Git checkout in the mounted Filesystem path.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb
    ```

- 立即启动一个无 blob 工作区：

    ```bash
    # Expose the repository tree while clean Git objects hydrate in the background.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate background
    ```

- 等待无 blob 填充完成：

    ```bash
    # Keep the clone command running until clean Git objects finish hydrating.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate sync
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)