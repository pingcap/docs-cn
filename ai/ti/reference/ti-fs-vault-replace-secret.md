---
title: ti fs-vault replace-secret
summary: 替换 file system Vault Secret 中的所有字段。
---

# ti fs-vault replace-secret

使用本地目录中的文件替换一个 Secret 中的所有字段。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault replace-secret
  --from-directory <string>
  --secret-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--from-directory <string>`：其中文件将成为 Secret 字段的目录。\[required]
- `--secret-path <string>`：规范的 Vault 路径，格式为 `/n/vault/<secret-name>`。例如，以 `db-prod` 创建的 Secret 路径为 `/n/vault/db-prod`。\[required]
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 从目录替换 Secret：

    ```bash
    # Replace all fields with files loaded from the selected directory.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields
    ```

- 预览 Secret 替换：

    ```bash
    # Validate the replacement source without changing the stored secret.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)