---
title: 管理 TiDB Cloud Filesystem 访问令牌
summary: 了解如何为 TiDB Cloud Filesystem 导入、生成、设置作用域、查看、禁用、轮转和回收访问令牌。
---

# 管理 TiDB Cloud Filesystem 访问令牌

你可以使用 Filesystem 访问令牌，为用户或自动化程序提供对 TiDB Cloud Filesystem 的访问能力，而无需共享 TiDB Cloud API 凭据。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 对于所有者令牌生成和基于 TiDB Cloud 身份验证的令牌管理，请配置 TiDB Cloud API 凭据并获取 Filesystem ID。
- 对于带作用域令牌生成或基于 bearer 身份验证的令牌管理，请获取一个 owner FS token。你可以通过 `--fs-token` 传入、设置 `TI_FS_TOKEN`，或使用为显式选定的 Filesystem 本地存储的令牌。

> **Note:**
>
> 为避免安全风险，请将令牌明文视为 Secret。令牌创建和轮转命令仅在令牌签发时返回一次明文。之后你将无法再次获取该明文。

## 导入现有令牌 {#import-an-existing-token}

运行 `import-file-system-token` 时，CLI 会验证令牌格式，提取其中嵌入的 Filesystem ID，通过发起远程 stat 请求验证连通性，并将令牌存储到本地凭据目录中：

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

## 生成令牌 {#generate-a-token}

使用 TiDB Cloud API 凭据生成另一个所有者令牌。默认情况下，CLI 不会将生成的令牌存储到本地，因此你必须安全地保存其一次性返回的明文响应：

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

如果希望 CLI 将生成的令牌存储到本地，请添加 `--store-locally`。如果此 Filesystem 已存储了其他令牌，请使用 `--replace`。

为了实现最小权限访问，可以基于所有者令牌生成一个受路径和操作限制的令牌：

```shell
ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --ttl 24h \
  --allow /workspace:read,list > ./scoped-token.json
```

## 查看并更改令牌状态 {#inspect-and-change-token-status}

列出不包含 Secret 的令牌元信息：

```shell
ti fs list-file-system-tokens --file-system-id "<file-system-id>"
```

使用 [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) 可临时停用令牌，使用 [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) 可恢复令牌。

## 轮转或回收令牌 {#rotate-or-revoke-a-token}

使用 [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) 轮转令牌。当你刷新本地存储的令牌时，CLI 会自动更新本地凭据文件。当你刷新通过 `--fs-token` 或 `TI_FS_TOKEN` 提供的令牌时，CLI 会在命令输出中返回新令牌，但不会将其存储到本地。

> **Note:**
>
> 刷新不是幂等操作。如果某个请求可能已经成功，但其响应丢失了，请不要使用旧令牌重试。应改为使用 TiDB Cloud 凭据生成一个新的所有者令牌。

使用 [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) 可永久回收令牌。如果被删除的令牌与本地存储的令牌匹配，CLI 会自动移除本地凭据。

> **Note:**
>
> 在轮转、禁用或删除某个被活动本地挂载使用的令牌之前，请先运行 [`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount)，然后运行 [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount)。CLI 会检查已知的活动挂载，如果该令牌仍在使用中，则会拒绝执行该操作。

## 接下来做什么 {#what-s-next}

- [在多台机器之间共享 TiDB Cloud Filesystem](/ai/ti/guides/ti-share-filesystem-across-machines-example.md)
- [在 Agent Sandbox 中使用 TiDB Cloud Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)