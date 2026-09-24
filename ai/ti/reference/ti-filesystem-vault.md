---
title: TiDB Cloud Filesystem Vault CLI 命令参考
summary: 参考所有 `ti fs-vault` 命令，用于管理 Secret、委派访问、审计事件、向子进程注入 Secret 以及挂载。
---

# TiDB Cloud Filesystem Vault CLI 命令参考

使用 `ti fs-vault` 管理 TiDB Cloud Filesystem 中的 Secret 和委派访问。

大多数 Secret 管理命令通过 Secret 名称来标识 Secret，例如 `db-prod`。而 `replace-secret` 和 `run-with-secret` 则要求使用其规范 Vault 路径 `/n/vault/<secret-name>`。`/n/vault/` 是 Vault 命名空间的根路径，因此 `/n/vault/db-prod` 和 Secret 名称 `db-prod` 标识的是同一个 Secret。

## 命令 {#commands}

| 命令 | 描述 |
|---|---|
| [`create-secret`](/ai/ti/reference/ti-fs-vault-create-secret.md) | 创建一个 Secret。 |
| [`replace-secret`](/ai/ti/reference/ti-fs-vault-replace-secret.md) | 替换一个 Secret。 |
| [`read-secret`](/ai/ti/reference/ti-fs-vault-read-secret.md) | 读取一个 Secret。 |
| [`list-secrets`](/ai/ti/reference/ti-fs-vault-list-secrets.md) | 列出 Secret。 |
| [`delete-secret`](/ai/ti/reference/ti-fs-vault-delete-secret.md) | 删除一个 Secret。 |
| [`create-grant`](/ai/ti/reference/ti-fs-vault-create-grant.md) | 将对 Secret 的有限访问权限委派给其他主体。 |
| [`delete-grant`](/ai/ti/reference/ti-fs-vault-delete-grant.md) | 回收委派访问权限。 |
| [`list-audit-events`](/ai/ti/reference/ti-fs-vault-list-audit-events.md) | 列出 Vault 审计事件。 |
| [`run-with-secret`](/ai/ti/reference/ti-fs-vault-run-with-secret.md) | 将 Secret 注入到进程中。 |
| [`mount-vault`](/ai/ti/reference/ti-fs-vault-mount-vault.md) | 挂载只读 Vault 视图。 |
| [`unmount-vault`](/ai/ti/reference/ti-fs-vault-unmount-vault.md) | 卸载 Vault 视图。 |

## 另请参阅 {#see-also}

- [管理 TiDB Cloud Filesystem Vault Secret](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)
- [将 TiDB Cloud Filesystem Vault Secret 委派给 Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)