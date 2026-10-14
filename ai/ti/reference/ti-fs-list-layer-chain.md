---
title: ti fs list-layer-chain
summary: 列出文件系统 layer 的祖先链。
---

# ti fs list-layer-chain

列出从根 layer 到所选子 layer 的父子 layer 链，并包含每个 layer 的序列边界。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs list-layer-chain
  --layer-ref <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--layer-ref <string>`：Layer ID、唯一名称，或[标签引用](/ai/ti/reference/ti-filesystem.md#layer-references)。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 查看子时间线：

    ```bash
    # Render the root-to-tip ancestry as stable text columns.
    ti fs list-layer-chain --file-system-id <file-system-id> --layer-ref experiment-a --output text
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [`ti fs fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md)