---
title: 管理 TiDB Cloud Filesystem Vault Secrets
summary: 了解如何使用 TiDB Cloud Filesystem Vault 安全地存储、读取、委派、注入、审计、回收和挂载 Secret。
---

# 管理 TiDB Cloud Filesystem Vault Secrets

TiDB Cloud Filesystem Vault 支持你存储 Secret、向用户或代理委派细粒度且有时限的访问权限，并将凭证注入到进程中，而无需将明文写入磁盘。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择一个 Filesystem。
- 对于 owner 操作，通过 `--fs-token`、`TI_FS_TOKEN`，或为所选 Filesystem 本地存储的凭证提供 owner FS token。

> **Note:**
>
> 为避免安全风险，切勿打印、记录日志或提交 owner 或委派令牌。

## 创建并读取 Secret {#create-and-read-a-secret}

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt

ti fs-vault read-secret --secret-name db-prod
```

> **Note:**
>
> 所有 `read-secret` 输出格式（包括默认的 JSON 格式）都包含明文 Secret 值。请仅将输出定向到预期的目标进程。

## 委派受限访问权限 {#delegate-limited-access}

创建一个短期有效的读授权并获取其令牌：

```shell
export TI_VAULT_TOKEN="$(ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m \
  --token-only)"
```

相比命令行传递令牌，更推荐使用 `TI_VAULT_TOKEN`，因为命令行中的值可能会保留在进程列表或 shell 历史记录中。

## 向进程注入 Secret {#inject-a-secret-into-a-process}

CLI 可以将 Secret 字段作为环境变量注入到子进程中，而无需将明文写入磁盘。运行以下命令时，CLI 会读取 Secret，将每个字段设置为环境变量（例如 `DB_URL`、`PASSWORD`），从子进程中移除其自身的凭证环境变量，然后执行指定命令：

```shell
ti fs-vault run-with-secret --secret-path /n/vault/db-prod -- <command>
```

相比将明文写入磁盘，更推荐使用向子进程注入 Secret。

由 `run-with-secret` 注入的字段名必须匹配 `[A-Z_][A-Z0-9_]*`。如果任一字段名不匹配该模式，或任一字段值包含不受支持的控制字符，该命令会拒绝整个注入操作。创建计划用于注入的字段时，请使用环境变量风格的大写名称。

## 审计并回收访问权限 {#audit-and-revoke-access}

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason rotated
```

权限回收会阻止新的已授权操作，但无法抹除进程已经读取过的值。

## 挂载只读 Vault 视图 {#mount-a-read-only-vault-view}

在支持 FUSE 的 macOS 或 Linux 上，你可以挂载 Vault Secret 的只读 FUSE 视图。CLI 会创建挂载点，并将 Secret 字段作为文件提供在挂载路径下（例如 `/path/to/vault/db-prod/DB_URL`）：

挂载前，请将 `TI_VAULT_TOKEN` 设置为 Vault 委派令牌，例如在[委派受限访问权限](#delegate-limited-access)中创建的令牌。挂载命令要求提供 `TI_VAULT_TOKEN` 或 `--vault-token` 之一。

```shell
mkdir -p /path/to/vault
ti fs-vault mount-vault \
  --mount-path /path/to/vault
```

卸载前，请先停止所有使用该挂载点的进程：

```shell
ti fs-vault unmount-vault --mount-path /path/to/vault
```

Windows 不支持 Vault 挂载。直接读取 Secret 和向子进程注入 Secret 不需要挂载。

## 安全建议 {#security-recommendations}

- 授予最小字段作用域以及尽可能短的 TTL。
- 不要将委派令牌存储在 CLI 配置或操作日志中。
- 在任务完成后回收授权。

## 后续操作 {#what-s-next}

- [将 TiDB Cloud Filesystem Vault Secrets 委派给代理](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)