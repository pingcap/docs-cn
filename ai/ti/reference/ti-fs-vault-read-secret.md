---
title: ti fs-vault read-secret
summary: 从 file system Vault 读取 Secret。
---

# ti fs-vault read-secret

使用所有者凭证或委派凭证读取完整的 Secret 或其中一个字段。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault read-secret
  --secret-name <string>
  [--field <string>]
  [--file-system-id <string>]
  [--format <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## 选项 {#options}

- `--secret-name <string>`：Vault Secret 名称。\[必需]
- `--field <string>`：可选，要读取的字段名称。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--format <string>`：读取输出格式：`json`、`raw` 或 `env`。\[默认值：json]
- `--fs-token <string>`：设置文件系统所有者令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。对于委派认证，请改用 `--vault-token` 或 `TI_VAULT_TOKEN`。
- `--help`：显示帮助信息。
- `--vault-token <string>`：委派 `ti fs-vault` 令牌；建议优先使用 `TI_VAULT_TOKEN`。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 以原始文本形式读取一个 Secret 字段：

    ```bash
    # Write only the selected field value for direct consumption by a process.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field PASSWORD --format raw
    ```

- 将字段格式化为环境变量赋值：

    ```bash
    # Emit an exportable environment-variable representation of the field.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format env
    ```

- 使用 Vault 委派令牌读取：

    ```bash
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Access only the field allowed by the delegated token.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format raw
    unset TI_VAULT_TOKEN
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)