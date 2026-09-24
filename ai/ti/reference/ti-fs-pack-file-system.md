---
title: ti fs pack-file-system
summary: 打包本地文件系统叠加层状态。
---

# ti fs pack-file-system

将选定的[本地叠加层状态](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)打包到远程归档中。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs pack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--path <string>]
  [--remote-root <string>]
  [--version]
```

## 选项 {#options}

- `--archive-path <string>`：打包后归档的路径。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--local-root <string>`：包含叠加层目录的本地叠加层根路径。
- `--mount-path <string>`：本地挂载路径。
- `--mount-profile <string>`：选择一个[挂载预设](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)：`coding-agent`、`portable` 或 `none`。如果省略，则使用 `none`。
- `--path <string>`：用于打包的本地叠加层路径；可重复指定。
- `--remote-root <string>`：由本地叠加层表示的 TiDB Cloud 文件系统根路径。\[default: /]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 打包已挂载的工作区：

    ```bash
    # Persist the local overlay associated with an existing mount.
    ti fs pack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 打包显式指定的根路径：

    ```bash
    # Create a portable archive from selected local and remote roots.
    ti fs pack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)