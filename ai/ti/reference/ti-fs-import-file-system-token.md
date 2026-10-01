---
title: ti fs import-file-system-token
summary: 将现有的文件系统令牌导入到所选的本地配置（Profile）中。
---

# ti fs import-file-system-token

验证现有的文件系统令牌，并将其存储到所选的本地配置（Profile）中。文件系统 ID 会从令牌中派生；你可以使用可选的 `--file-system-id` 来验证该令牌是否属于预期的文件系统。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs import-file-system-token
  [--dry-run]
  [--file-system-id <string>]
  [--from-file <string>]
  [--fs-token <string>]
  [--help]
  [--replace]
  [--version]
```

## 选项 {#options}

- `--dry-run`：验证令牌和目标位置，但不写入本地凭证。
- `--file-system-id <string>`：断言该令牌属于此文件系统 ID。
- `--from-file <string>`：从仅所有者可读的文件中读取令牌，或使用 `-` 表示标准输入。
- `--fs-token <string>`：直接提供令牌。建议优先使用 `TI_FS_TOKEN` 或 `--from-file`，以避免通过进程参数暴露令牌。
- `--help`：显示帮助信息。
- `--replace`：验证后，替换同一文件系统在本地存储的其他令牌。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 从受保护的文件中导入令牌：

    ```bash
    # Validate the token remotely and store it under its embedded file system ID.
    chmod 600 ./fs-token
    ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
    ```

- 从标准输入导入令牌：

    ```bash
    # Avoid placing the token in shell history or a process argument.
    cat ./fs-token | ti fs import-file-system-token --from-file - --region aws-us-east-1
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)