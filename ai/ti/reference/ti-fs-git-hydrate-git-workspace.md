---
title: ti fs-git hydrate-git-workspace
summary: 为 Filesystem Git 工作区补全干净的 Git 对象。
---

# ti fs-git hydrate-git-workspace

为现有的 `ti` Git 工作区补全干净的 Git 对象。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-git hydrate-git-workspace
  --target-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--timeout <duration>]
  [--version]
```

## 选项 {#options}

- `--target-path <string>`：挂载的 `ti fs` 工作区路径。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--timeout <duration>`：补全过程的最长持续时间。\[默认值：`30m0s`]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 完成 Git 工作区的补全：

    ```bash
    # Download missing clean Git objects for an existing blobless workspace.
    ti fs-git hydrate-git-workspace --file-system-id <file-system-id> --target-path /path/to/workspace/tidb --timeout 30m
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)