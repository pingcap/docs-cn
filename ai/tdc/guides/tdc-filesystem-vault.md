---
title: 使用 TiDB Cloud 文件系统 Vault
summary: 保存文件系统 secret、委派有限访问、向进程注入 secret、审计访问并挂载只读 vault。
---

# 使用 TiDB Cloud 文件系统 Vault

`tdc fs-vault` 保存结构化 secret，并向 agent 委派有限、带过期时间的访问。Owner 操作使用文件系统 owner credential；委派读取使用 scope 限定到指定 secret 或 field 的 vault token。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

通过 profile 或无配置 FS 环境变量选择文件系统。不要输出、记录或提交 owner token 和 delegated token。

## 创建和替换 secret

使用可重复 field 创建 secret：

```bash
tdc fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt
```

`key=value` 使用 literal value，`key=@file` 读取文件，`key=-` 从 stdin 读取。

用目录中的文件替换全部 field：

```bash
tdc fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory ./secret-fields
```

## 读取、列出和删除

```bash
tdc fs-vault list-secrets
tdc fs-vault read-secret --secret-name db-prod
tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format raw
tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format env
```

删除 owner 可见的 secret：

```bash
tdc fs-vault delete-secret --secret-name db-prod
```

Raw 和 environment 输出包含 plaintext，只能发送给目标进程。

## 委派有限访问

创建短期 read grant 并获取 token：

```bash
export TDC_VAULT_TOKEN="$(tdc fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m \
  --token-only)"
```

Scope 可重复。`--label-hint` 可以添加非敏感 operator context。

使用 delegated token：

```bash
tdc fs-vault read-secret \
  --secret-name db-prod \
  --field DB_URL \
  --format raw
```

优先使用 `TDC_VAULT_TOKEN`，而不是 `--vault-token`，因为命令行值可能保留在进程列表或 shell history 中。

## 向进程注入 secret

```bash
tdc fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- env
```

子进程会将 secret field 作为环境变量接收。生产环境不要使用打印完整 environment 的命令；此处使用 `env` 仅用于展示接口。

## 审计和撤销

```bash
tdc fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20

tdc fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason rotated
```

撤销会阻止新的授权操作，但无法清除进程已经读取的 secret value。

## 挂载只读 vault

在支持 FUSE 的 macOS 或 Linux 上：

```bash
mkdir -p /path/to/vault
tdc fs-vault mount-vault \
  --mount-path /path/to/vault \
  --vault-token "$TDC_VAULT_TOKEN"
```

Mount 是只读的。`--foreground` 使其附着在终端，`--ready-timeout` 修改后台 readiness 等待时间。

Unmount：

```bash
tdc fs-vault unmount-vault --mount-path /path/to/vault
```

Unmount 还支持 `--timeout`、`--force` 和 `--ignore-absent`。Windows 不支持 vault mount，vault mount 需要 FUSE；直接 `read-secret` 和 `run-with-secret` 不需要 mount。

## 安全建议

- 为 agent 提供最小 field scope 和尽可能短的 TTL。
- 优先使用 `run-with-secret`，而不是将 plaintext 写入磁盘。
- 不要将委派 token 写入 tdc 配置或操作日志。
- Unmount 前停止正在使用 vault mount 的进程。
- 任务结束后撤销 grant。

## 后续步骤

- [向 Agent 委派 Vault Secret](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)
- [tdc 区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
