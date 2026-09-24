---
title: ti fs drain-file-system
summary: 刷写已挂载的 TiDB Cloud Filesystem。
---

# ti fs drain-file-system

在保持挂载在线的同时，将 FUSE 挂载中的待处理写入刷写到远端 文件系统。该命令的别名是 `ti fs drain`。对于 WebDAV 挂载，请先停止写入端并使用 `ti fs unmount-file-system`；对其运行 `drain-file-system` 会返回错误。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs drain-file-system
  --mount-path <string>
  [--dry-run]
  [--help]
  [--timeout <duration>]
  [--version]
```

## 选项 {#options}

- `--mount-path <string>`：本地 FUSE 挂载路径。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--help`：显示帮助信息。
- `--timeout <duration>`：等待脏句柄和待处理写入完成刷写的时间。\[default: `30s`]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 刷写待处理写入：

    ```bash
    # Flush queued FUSE writes while leaving the file system mounted.
    ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)