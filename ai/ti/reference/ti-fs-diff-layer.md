---
title: ti fs diff-layer
summary: 显示文件系统 layer 中的更改。
---

# ti fs diff-layer

列出某个 layer 中的更改，并可选择限制到某个序列号为止。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs diff-layer
  --layer-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--max-seq <int64>]
  [--version]
```

## 选项 {#options}

- `--layer-id <string>`：layer 的 ID。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--max-seq <int64>`：要包含的最高 layer 序列；`0` 表示包含所有序列。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 显示所有 layer 更改：

    ```bash
    # Return the complete ordered change set for the selected layer.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

- 显示较早的 layer 视图：

    ```bash
    # Limit the diff to changes at or before a sequence number.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>" --max-seq 100
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)