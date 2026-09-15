---
title: 使用显式 SQL 角色查询 TiDB Cloud Starter
summary: 准备由 TiDB Cloud CLI 管理的 SQL 用户，并以显式权限意图执行只读、读写和管理员语句。
---

# 使用显式 SQL 角色查询 TiDB Cloud Starter

此工作流会先一次性准备三个 SQL 角色，然后为每条语句显式选择权限最小的角色。你可以将其用于交互式或自动化的 schema、数据和验证工作，而无需在每条命令中处理数据库密码。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

传统的数据库连接使用一组凭证，并在整个会话期间保留该凭证对应的权限。相比之下，`ti db create-db-sql-users` 会创建三个稳定身份，并将其凭证存储在本地。每次调用 `execute-sql-statement` 时，都会选择一个身份并执行一条语句，因此检查步骤无需保留写权限或管理员权限。

| 角色 | 用途 |
| --- | --- |
| `admin` | schema 变更和权限管理 |
| `read-write` | 应用数据修改 |
| `read-only` | 查询和验证 |

## 前提条件 {#prerequisites}

- 配置 `ti`。
- 选择一个处于活动状态的 TiDB Cloud Starter 实例 ID。

## 第 1 步：准备 SQL 用户 {#step-1-prepare-sql-users}

```bash
ti db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

该命令是幂等的，会创建或修复 `read_only`、`read_write` 和 `admin` 凭证。

## 第 2 步：使用 admin 进行 schema 变更 {#step-2-use-admin-for-schema-changes}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS role_demo"

ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --database role_demo \
  --sql "CREATE TABLE IF NOT EXISTS messages (id BIGINT PRIMARY KEY, body VARCHAR(255))"
```

## 第 3 步：使用 read-write 进行数据修改 {#step-3-use-read-write-for-data-changes}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database role_demo \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello') ON DUPLICATE KEY UPDATE body = VALUES(body)"
```

## 第 4 步：使用 read-only 进行验证 {#step-4-use-read-only-for-verification}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --sql "SELECT id, body FROM messages ORDER BY id" \
  --output text
```

预期结果应包含 ID `1` 和 body `hello`。

## 第 5 步：格式化连接环境 {#step-5-format-a-connection-environment}

将输出直接写入受保护的本地文件，而不是显示在终端中：

```bash
umask 077
ti db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --format env \
  --env-include-database-url > .env.tidb
```

不要提交 `.env.tidb`。

使用 `--format env` 时，该命令会写出独立的 `TIDB_` 连接变量，例如 `TIDB_HOST`、`TIDB_USER` 和 `TIDB_PASSWORD`。`--env-include-database-url` 选项还会额外添加一个 `DATABASE_URL` 值，供接受单个 MySQL 连接 URL 的应用使用。

## 清理 {#cleanup}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "DROP DATABASE role_demo"

rm -f .env.tidb
```

## 安全说明 {#security-notes}

- 对每条语句都使用权限最小的显式角色。
- `ti` 每次调用只接受一条 SQL 语句。
- HTTPS 是默认的 SQL 执行传输方式。若要改为打开直接的 TLS MySQL 连接，请指定 `--transport mysql`；CLI 不会自动切换传输方式。
- 连接字符串和环境输出中包含凭证。

## 后续操作 {#what-s-next}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)