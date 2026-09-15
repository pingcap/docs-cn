---
title: ti fs find-files
summary: 在 TiDB Cloud Filesystem 中查找文件。
---

# ti fs find-files

按名称、类型、标签、大小或修改时间查找远程路径。该命令的别名是 `ti fs find`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs find-files
  [--file-name-pattern <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--max-size-bytes <int64>]
  [--min-size-bytes <int64>]
  [--newer <string>]
  [--older <string>]
  [--path <string>]
  [--resource-type <string>]
  [--tag <string>]
  [--version]
```

## 选项 {#options}

- `--file-name-pattern <string>`：文件名模式过滤器，例如 `*.md`。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--layer-id <string>`：在特定文件系统 layer 中搜索文件和目录。
- `--limit <int32>`：结果的最大数量；0 表示使用服务默认值。
- `--max-size-bytes <int64>`：文件大小上限（字节）。
- `--min-size-bytes <int64>`：文件大小下限（字节）。
- `--newer <string>`：返回比指定日期更新的文件，日期格式为 `YYYY-MM-DD`。
- `--older <string>`：返回比指定日期更早的文件，日期格式为 `YYYY-MM-DD`。
- `--path <string>`：文件路径前缀。\[default: /]
- `--resource-type <string>`：资源类型过滤器：`file` 或 `directory`。
- `--tag <string>`：通过 `key=value` 精确匹配标签，或者仅指定 `key` 以匹配该标签键的任意值。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 按名称查找文件：

    ```bash
    # Locate Markdown files recursively under the selected remote path.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --file-name-pattern "*.md"
    ```

- 按元信息查找文件：

    ```bash
    # Select tagged files that also meet a minimum size threshold.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --tag stage=review --min-size-bytes 1024
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)