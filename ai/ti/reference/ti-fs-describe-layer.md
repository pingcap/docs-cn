---
title: ti fs describe-layer
summary: 描述文件系统中的一个 layer。
---

# ti fs describe-layer

描述一个文件系统 layer。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs describe-layer
  --layer-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--layer-id <string>`：指定文件系统 layer 的 ID。\[必需]
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 描述一个 layer：

    ```bash
    # Inspect one layer's base root, state, durability, and metadata.
    ti fs describe-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)