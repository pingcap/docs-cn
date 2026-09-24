---
title: ti fs search-file-content
summary: 在文件系统中搜索文件内容。
---

# ti fs search-file-content

搜索远程文件内容，也可以选择在某个层中搜索。该命令的别名是 `ti fs grep`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs search-file-content
  --pattern <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--path <string>]
  [--version]
```

## 选项 {#options}

- `--pattern <string>`：用于全文搜索的文本查询；在已配置的情况下，也可对提取出的文件内容和描述执行语义搜索。该值不是正则表达式或 glob。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--layer-id <string>`：在文件系统层内搜索。
- `--limit <int32>`：搜索结果的最大数量；`0` 表示使用服务默认值。
- `--path <string>`：要搜索的文件路径前缀。\[默认值：/]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 搜索基础文件系统中的内容：

    ```bash
    # Find matching text under a remote directory and limit the result count.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "TODO" --limit 50
    ```

- 搜索某个层中的内容：

    ```bash
    # Inspect uncommitted layer content separately from the base file system.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "deprecated" --layer-id "<layer-id>"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)