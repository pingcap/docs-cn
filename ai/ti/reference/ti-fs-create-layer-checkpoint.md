---
title: ti fs create-layer-checkpoint
summary: 在文件系统的层中创建一个检查点。
---

# ti fs create-layer-checkpoint

在单个层中创建一个检查点。如果省略 `--checkpoint-id`，则由服务自动生成一个。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-layer-checkpoint
  --layer-id <string>
  [--checkpoint-id <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--label <string>]
  [--version]
```

## 选项 {#options}

- `--layer-id <string>`：用于标识该层的 layer ID。\[必需]
- `--checkpoint-id <string>`：检查点 ID。通常由服务自动生成。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--label <string>`：检查点标签。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个命名检查点：

    ```bash
    # Record the current layer state under a stable checkpoint ID.
    ti fs create-layer-checkpoint --file-system-id <file-system-id> --layer-id "<layer-id>" --checkpoint-id before-review
    ```

- 创建一个自动分配标识的检查点：

    ```bash
    # Let the service assign the checkpoint ID while retaining a human label.
    ti fs create-layer-checkpoint --file-system-id <file-system-id> --layer-id "<layer-id>" --label "before review"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)