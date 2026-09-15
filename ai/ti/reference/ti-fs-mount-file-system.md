---
title: ti fs mount-file-system
summary: 挂载一个 TiDB Cloud Filesystem。
---

# ti fs mount-file-system

通过 automatic、FUSE 或 WebDAV 模式挂载一个 Filesystem。该命令的别名是 `ti fs mount`。

该命令会在后台启动挂载过程，等待挂载就绪，然后输出结果。如果启动失败，错误信息中会包含用于诊断的日志路径。使用 `ti fs unmount-file-system` 结束挂载。

> **Important:**
>
> 层和检查点挂载需要 FUSE。在 macOS 上，automatic 选择通常会使用 WebDAV，因此请安装 macFUSE 并指定 `--driver fuse`。检查点挂载始终为只读。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs mount-file-system
  --mount-path <string>
  [--cache-dir <string>]
  [--checkpoint-id <string>]
  [--driver <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-ref <string>]
  [--local-root <string>]
  [--mount-profile <string>]
  [--no-auto-unpack]
  [--pack-path <string>]
  [--read-cache-max-file-mb <int64>]
  [--read-cache-size-mb <int64>]
  [--read-cache-ttl <duration>]
  [--read-only]
  [--ready-timeout <duration>]
  [--remote-path <string>]
  [--unpack-archive-path <string>]
  [--version]
  [--write-back-cache]
```

## 选项 {#options}

- `--mount-path <string>`：本地挂载路径。\[required]
- `--cache-dir <string>`：本地 FUSE 缓存目录。如果省略，则使用 `~/.ti/cache/mounts/<mount-hash>`。
- `--checkpoint-id <string>`：以只读方式挂载 `--layer-ref` 的此检查点。需要 FUSE。
- `--driver <string>`：挂载驱动：`auto`、`fuse` 或 `webdav`。\[default: auto]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，该命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，则该命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--layer-ref <string>`：通过可写层 ID、唯一名称或[标签引用](/ai/ti/reference/ti-filesystem.md#layer-references)进行挂载。需要 FUSE。
- `--local-root <string>`：本地叠加层根目录。如果省略，则使用 `~/.ti/local/fs/<mount-hash>`。
- `--mount-profile <string>`：选择一个[挂载预设](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)：`coding-agent`、`portable` 或 `none`。如果省略，则使用 `none`。
- `--no-auto-unpack`：在挂载前，跳过对 portable 挂载预设执行默认自动解包。
- `--pack-path <string>`：由自动或手动打包包含的本地叠加层路径。可重复指定。
- `--read-cache-max-file-mb <int64>`：允许进入 FUSE 读缓存的最大文件大小，单位为 MiB。0 表示使用默认值。\[default: 4]
- `--read-cache-size-mb <int64>`：FUSE 读缓存大小，单位为 MiB。0 表示使用默认值。\[default: 128]
- `--read-cache-ttl <duration>`：FUSE 读缓存生存时间。\[default: `30s`]
- `--read-only`：只读挂载模式。
- `--ready-timeout <duration>`：等待后台挂载就绪的时间。\[default: `30s`]
- `--remote-path <string>`：要挂载的 TiDB Cloud 文件系统根路径。\[default: /]
- `--unpack-archive-path <string>`：在挂载前恢复打包归档。
- `--version`：显示版本信息。
- `--write-back-cache`：先将 FUSE 写入持久化到本地，再在 flush 时将其写入文件系统。此行为默认启用；指定 `--write-back-cache=false` 可禁用。检查点挂载不支持此选项，因为检查点挂载始终为只读。\[default: true]

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 使用默认驱动挂载一个 Filesystem：

    ```bash
    # Let the CLI select the default driver for the current platform.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 创建一个只读 FUSE 挂载：

    ```bash
    # Expose the remote namespace through FUSE without permitting writes.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-only
    ```

- 在 macOS 上不使用 macFUSE 而使用 WebDAV：

    ```bash
    # Select WebDAV explicitly when a FUSE runtime is unavailable.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver webdav
    ```

- 调整 FUSE 读缓存：

    ```bash
    # Increase cache capacity for repeated reads of medium-sized files.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-cache-size-mb 256 --read-cache-max-file-mb 16
    ```

- 挂载一个可写子层：

    ```bash
    # Expose only the selected copy-on-write timeline at the local path.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/experiment --remote-path /workspace --driver fuse --layer-ref experiment
    ```

- 对比一个不可变的历史检查点：

    ```bash
    # A checkpoint mount is always read-only.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/checkpoint --remote-path /workspace --driver fuse --layer-ref experiment --checkpoint-id v5
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)