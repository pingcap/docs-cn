---
title: 将 TiDB Cloud Filesystem Vault Secret 委派给 Agent
summary: 存储一个 Secret，将其中一个字段授予 agent，将其注入到进程中，审计访问，并回收授权。
---

# 将 TiDB Cloud Filesystem Vault Secret 委派给 Agent

此工作流可让 agent 临时访问某个 Secret 的单个字段，而无需共享 Filesystem 所有者令牌或完整 Secret。当 agent 只需要为某个任务使用一个凭证，但不应在 prompt、`.env` 文件或 sandbox 镜像中保留该值时，请使用此方法。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

Filesystem 所有者只需存储一次 Secret，并创建一个作用域限定到所需字段的短期授权。agent 仅接收 Vault 委派令牌，并可将允许的值注入到子进程中。所有者可以查看审计事件，并在不轮换或暴露 Filesystem 所有者凭证的情况下回收该授权。

## 为什么使用这种方法 {#why-use-this-approach}

普通的环境变量和文件也可以传递 Secret，但它们无法提供带作用域和过期时间的委派机制，也无法提供访问审计轨迹。共享 Filesystem 所有者令牌还会授予比单个 Secret 字段所需更广泛的访问权限。单独的云 Secret 管理器也能提供类似控制，但它要求为每个 sandbox 额外配置身份、策略和集成路径。

## 前提条件 {#prerequisites}

- 选择一个具有 owner 访问权限的 Filesystem。
- 安装 `jq`。
- 将源 Secret 值存储在受保护的文件中。

## 步骤 1：创建 Secret {#step-1-create-a-secret}

```bash
ti fs-vault create-secret \
  --secret-name service-demo \
  --field ENDPOINT=https://service.example \
  --field API_TOKEN=@./api-token.txt
```

## 步骤 2：创建最小授权 {#step-2-create-a-narrow-grant}

```bash
umask 077
set -o noclobber
ti fs-vault create-grant \
  --agent-id example-agent \
  --scope service-demo/ENDPOINT \
  --permission read \
  --ttl 10m \
  --label-hint example > ./vault-grant.json
set +o noclobber

export TI_VAULT_TOKEN="$(jq -r '.token' ./vault-grant.json)"
export GRANT_ID="$(jq -r '.grant_id' ./vault-grant.json)"
```

受保护的文件会保存这两个一次性值，而不会打印令牌。请将该令牌存储在 Secret 管理器中，并保留 `GRANT_ID`，以便后续回收该授权。

## 步骤 3：使用委派字段 {#step-3-use-the-delegated-field}

```bash
ti fs-vault read-secret \
  --secret-name service-demo \
  --field ENDPOINT \
  --format raw
```

将允许的字段注入到命令中：

```bash
ti fs-vault run-with-secret \
  --secret-path /n/vault/service-demo \
  -- sh -c 'test -n "$ENDPOINT"'
```

`/n/vault/` 前缀用于标识接受完整 Secret 路径的命令中的 Vault 命名空间；`service-demo` 指的是在步骤 1 中创建的 Secret。`run-with-secret` 会读取允许的字段，将它们设置为子进程中的环境变量，然后执行 `--` 之后的命令。此测试会在 `ENDPOINT` 存在且不打印其值时成功退出。不要使用会打印所有环境变量值的命令。

## 步骤 4：审计并回收授权 {#step-4-audit-and-revoke}

```bash
ti fs-vault list-audit-events \
  --secret-name service-demo \
  --agent-id example-agent \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "$GRANT_ID" \
  --revoked-by operator \
  --reason task-complete
```

取消设置本地令牌：

```bash
unset TI_VAULT_TOKEN
```

## 清理 {#cleanup}

```bash
ti fs-vault delete-secret --secret-name service-demo
rm -f ./api-token.txt ./vault-grant.json
```

## 安全与运维说明 {#security-and-operational-notes}

- 将授权的作用域限制为最少的字段集合，并将 TTL 设为尽可能短但仍满足使用需求的时长。
- 已被回收的令牌无法再为新的读操作授予权限，但它无法抹除某个进程已经读取到的值。
- 避免使用 Secret 标记/参数，因为进程列表和 shell 历史记录可能会保留这些值。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)
- [TiDB Cloud CLI Regions、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md)