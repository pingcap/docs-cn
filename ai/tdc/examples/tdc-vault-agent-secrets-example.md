---
title: 向 Agent 委派文件系统 Vault Secret
summary: 保存 secret、将一个 field 委派给 agent、注入进程、审计访问并撤销 grant。
---

# 向 Agent 委派文件系统 Vault Secret

本示例在不共享文件系统 owner token 或完整 secret 的情况下，向 Agent 临时开放一个 secret field。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## Agent 面临的问题

Agent 可能只需要一个 API endpoint 或 token 来完成短期任务。把完整 secret 放进 prompt、`.env` 文件或沙箱镜像，会让 secret 暴露给超出所需范围和生命周期的环境。共享文件系统 owner token 同样会授予远多于一个 secret field 的权限。

## 普通环境变量和文件为什么不够

环境变量和文件可以传递 secret，但不能形成限定 scope、自动过期的委派，也不提供访问审计。独立的云 secret manager 可以提供这些控制，但每个沙箱都需要额外配置一套身份、策略和集成路径。

## tdc 如何改变工作流

文件系统 owner 只需保存一次 secret，并创建一个仅覆盖所需 field 的短期 grant。Agent 只接收委派的 Vault token，并将允许访问的值注入子进程。Owner 可以检查 audit event 并撤销 grant，而无需轮换或暴露文件系统 owner credential。

## 前置条件

- 以 owner access 选择一个文件系统。
- 将源 secret value 保存在受保护文件中。

## 第 1 步：创建 secret

```bash
tdc fs-vault create-secret \
  --secret-name service-demo \
  --field ENDPOINT=https://service.example \
  --field API_TOKEN=@./api-token.txt
```

## 第 2 步：创建最小 grant

```bash
export TDC_VAULT_TOKEN="$(tdc fs-vault create-grant \
  --agent-id example-agent \
  --scope service-demo/ENDPOINT \
  --permission read \
  --ttl 10m \
  --label-hint example \
  --token-only)"
```

实际 workflow 应从结构化 create result 记录返回的 grant ID。Token 被捕获而不会显示。

## 第 3 步：使用 delegated field

```bash
tdc fs-vault read-secret \
  --secret-name service-demo \
  --field ENDPOINT \
  --format raw
```

将允许的 field 注入命令：

```bash
tdc fs-vault run-with-secret \
  --secret-path /n/vault/service-demo \
  -- sh -c 'test -n "$ENDPOINT"'
```

允许的 field 存在时进程成功退出。不要使用会打印全部 environment value 的命令。

## 第 4 步：审计和撤销

```bash
tdc fs-vault list-audit-events \
  --secret-name service-demo \
  --agent-id example-agent \
  --limit 20

tdc fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason task-complete
```

清除本地 token：

```bash
unset TDC_VAULT_TOKEN
```

## 清理

```bash
tdc fs-vault delete-secret --secret-name service-demo
rm -f ./api-token.txt
```

## 安全说明

- 将 grant 限制到最小 field 集合和最短实用 TTL。
- 撤销的 token 无法授权新的读取，但不能清除进程已经读取的 value。
- 避免使用 secret flag，因为进程列表和 shell history 可能保留它们。

## 后续步骤

- [使用 TiDB Cloud 文件系统 Vault](/ai/tdc/guides/tdc-filesystem-vault.md)
- [tdc 区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
