---
title: ti fs-vault delete-grant
summary: 回收委派的文件系统 Vault grant。
---

# ti fs-vault delete-grant

回收一个委派的文件系统 Vault grant。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault delete-grant
  --grant-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--reason <string>]
  [--revoked-by <string>]
  [--version]
```

## 选项 {#options}

- `--grant-id <string>`：Vault grant ID。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--reason <string>`：（权限）回收原因，可选。
- `--revoked-by <string>`：用于（权限）回收审计条目的执行者标签。\[默认值：`ti`]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 回收一个 grant：

    ```bash
    # Invalidate the delegated token and record the revocation reason.
    ti fs-vault delete-grant --file-system-id <file-system-id> --grant-id "<grant-id>" --reason rotated
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)