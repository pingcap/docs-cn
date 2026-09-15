---
title: ti fs-vault list-secrets
summary: 列出 Filesystem Vault 凭证可见的 Secret。
---

# ti fs-vault list-secrets

列出当前激活的所有者凭证或委派凭证可见的 Secret。

该命令会返回完整的可见列表，不会对结果进行分页。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-vault list-secrets
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置所有者 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。对于委派认证，请改用 `--vault-token` 或 `TI_VAULT_TOKEN`。
- `--help`：显示帮助信息。
- `--vault-token <string>`：委派 `ti fs-vault` 令牌；建议优先使用 `TI_VAULT_TOKEN`。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出所有者可见的 Secret：

    ```bash
    # Return secret metadata without exposing field values.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    ```

- 列出委派令牌可见的 Secret：

    ```bash
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Restrict results to the token's granted scope.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    unset TI_VAULT_TOKEN
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)