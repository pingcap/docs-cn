---
title: ti fs unmount-file-system
summary: 卸载一个文件系统。
---

# ti fs unmount-file-system

优雅地刷新并卸载一个后台挂载。该命令的别名是 `ti fs umount`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs unmount-file-system
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--no-auto-pack]
  [--pack-archive-path <string>]
  [--timeout <duration>]
  [--version]
```

## 选项 {#options}

- `--mount-path <string>`：本地挂载路径。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--force`：如果优雅卸载超时，则终止挂载进程。这可能会导致未提交的内存状态或回写状态丢失。
- `--help`：显示帮助信息。
- `--ignore-absent`：当指定路径不存在文件系统挂载状态时，返回成功。
- `--no-auto-pack`：跳过挂载配置的默认自动打包操作。内置的 `portable` 挂载预设会通过选择 `/` 作为其打包路径来启用此操作。
- `--pack-archive-path <string>`：卸载后，将该挂载的本地叠加层打包到此远程归档路径。即使挂载预设没有默认打包路径，指定此选项也会请求执行打包。
- `--timeout <duration>`：等待挂载进程退出的时间。\[default: `30s`]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 卸载一个文件系统：

    ```bash
    # Gracefully flush pending writes and detach the file system mount.
    ti fs unmount-file-system --mount-path /path/to/workspace
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)