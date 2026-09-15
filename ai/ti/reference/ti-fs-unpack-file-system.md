---
title: ti fs unpack-file-system
summary: 恢复本地 Filesystem 叠加层状态。
---

# ti fs unpack-file-system

从远程归档中恢复[本地叠加层状态](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs unpack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--no-replace]
  [--remote-root <string>]
  [--version]
```

## 选项 {#options}

- `--archive-path <string>`：已打包归档的路径。
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--local-root <string>`：要恢复到的本地叠加层根目录。
- `--mount-path <string>`：本地挂载路径。
- `--mount-profile <string>`：选择一个[挂载预设](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)：`coding-agent`、`portable` 或 `none`。如果省略，则使用 `none`。
- `--no-replace`：合并归档条目，而不是替换它们。
- `--remote-root <string>`：当省略 `--archive-path` 时，在指定的根路径下查找已打包归档。\[默认值：/]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 解包到已挂载的工作区：

    ```bash
    # Restore the portable archive associated with an existing mount.
    ti fs unpack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 在不替换的情况下解包显式根路径：

    ```bash
    # Restore missing files while preserving existing destination entries.
    ti fs unpack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable --no-replace
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)