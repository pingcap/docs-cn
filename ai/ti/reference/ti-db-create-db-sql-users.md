---
title: ti db create-db-sql-users
summary: 为 TiDB Cloud Starter 实例创建由 TiDB Cloud CLI 管理的 SQL 用户。
---

# ti db create-db-sql-users

为 TiDB Cloud Starter 实例创建或修复三个由 `ti` 管理的 SQL 用户：只读、读写和管理员。它会将这些用户的凭据存储在本地，以便后续命令可以通过 `--read-only`、`--read-write` 或 `--admin` 选择相应的用户。

这些用户具有以下预定义的访问级别和内置 TiDB Cloud 角色：

| `ti` 访问模式 | TiDB Cloud 内置角色 | 预期用途 |
| --- | --- | --- |
| `read_only` | `role_readonly` | 查询并验证数据而不修改数据 |
| `read_write` | `role_readwrite` | 查询并修改应用数据 |
| `admin` | `role_admin` | 进行 schema 变更并管理权限 |

关于 TiDB Cloud 角色模型，请参见 [管理数据库用户和角色](https://docs.pingcap.com/tidbcloud/configure-sql-users)。

`ti` 会将生成的用户名和密码存储在 `~/.ti/db_users/<cluster-id>/credentials` 中，并为这三种访问模式分别使用独立的 TOML section。在支持 POSIX 权限的系统上，凭据文件仅其所有者可读写。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db create-db-sql-users
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--db-cluster-id <string>`：Starter DB 集群 ID。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建受管理的 SQL 用户：

    ```bash
    # Create or reconcile the read-only, read-write, and admin SQL users.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>"
    ```

- 预览 SQL 用户创建：

    ```bash
    # Show the three managed roles without changing SQL users or local credentials.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>" --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)