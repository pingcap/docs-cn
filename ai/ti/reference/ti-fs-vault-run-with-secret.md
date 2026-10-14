---
title: ti fs-vault run-with-secret
summary: 使用 file system Vault Secret 运行一个进程。
---

# ti fs-vault run-with-secret

运行一个命令，并将一个 Secret 注入到其环境变量中。`--` 之后的参数会传递给子命令。

每个 Secret 的字段名都会在子进程中成为同名的环境变量。字段名必须匹配 `[A-Z_][A-Z0-9_]*`，因此请将你打算注入的字段创建为大写名称。如果任意字段名（包括包含小写字母的名称）不匹配此模式，或者某个值包含不受支持的控制字符，则该命令会拒绝整个注入操作。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault run-with-secret
  --secret-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
  -- <command> [args...]
```

## 选项 {#options}

- `--secret-path <string>`: `/n/vault/<secret-name>` 形式的规范 Vault 路径。例如，创建为 `db-prod` 的 Secret 路径为 `/n/vault/db-prod`。\[required]
- `--file-system-id <string>`: 选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`: 设置文件系统所有者令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 文件系统 本地存储的令牌。对于委托认证，请改用 `--vault-token` 或 `TI_VAULT_TOKEN`。
- `--help`: 显示帮助信息。
- `--vault-token <string>`: 委托的 `ti fs-vault` 令牌；优先使用 `TI_VAULT_TOKEN`。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 使用 Secret 字段运行一个进程：

    ```bash
    # Verify that the child process receives DB_URL without printing its value.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL" && printf "DB_URL is set\n"'
    ```

- 使用注入字段运行一个应用程序：

    ```bash
    # Make all fields available only to the child process and its descendants.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- ./deploy.sh
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)