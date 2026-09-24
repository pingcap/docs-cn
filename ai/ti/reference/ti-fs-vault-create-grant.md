---
title: ti fs-vault create-grant
summary: 创建委派 file system Vault grant。
---

# ti fs-vault create-grant

创建一个有时间限制的委派 grant，用于单个 agent 和作用域。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault create-grant
  --agent-id <string>
  --permission <string>
  --scope <string>
  --ttl <duration>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--label-hint <string>]
  [--token-only]
  [--version]
```

## 选项 {#options}

- `--agent-id <string>`：委派 grant 的 Agent ID。\[必需]
- `--permission <string>`：grant 权限：`read` 或 `write`。有关当前权限行为，请参见[grant 权限](#grant-permissions)。\[必需]
- `--scope <string>`：Secret 作用域，格式为 `<secret-name>`（表示所有字段）或 `<secret-name>/<field-name>`（表示单个字段）；可重复指定。也接受等效的规范 Vault 路径 `/n/vault/<secret-name>` 和 `/n/vault/<secret-name>/<field-name>`。\[必需]
- `--ttl <duration>`：grant 的生存时间，例如 `1h`。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 文件系统 本地存储的令牌。
- `--help`：显示帮助信息。
- `--label-hint <string>`：可选的 grant 标签提示。
- `--token-only`：仅输出委派 bearer token。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## grant 权限 {#grant-permissions}

| 权限 | 当前 `ti` 行为 |
| --- | --- |
| `read` | 允许在 grant 作用域内执行委派的 `list-secrets`、`read-secret`、`run-with-secret` 和 `mount-vault` 操作。 |
| `write` | 服务接受此权限，但它不包含读权限。当前 `ti` 命令界面未提供使用委派 token 写入 Secret 的操作。 |

## 示例 {#examples}

- 创建一个临时读 grant：

    ```bash
    # Limit an agent to one secret field for ten minutes.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m
    ```

- 仅返回委派 token：

    ```bash
    # Produce token-only output for injection into an isolated CI job.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id ci-agent --scope api-dev/TOKEN --permission read --ttl 5m --token-only
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)