---
title: ti db format-db-connection-string
summary: 为由 TiDB Cloud CLI 管理的 SQL 用户格式化连接字符串。
---

# ti db format-db-connection-string

将已存储的 SQL 凭据格式化为读写、只读或管理员访问所需的连接字符串。如果未指定角色选项，该命令将使用 `read_write`。该命令会在加载本地 SQL 凭据之前验证集群是否为 Starter。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db format-db-connection-string
  --db-cluster-id <string>
  [--admin]
  [--database <string>]
  [--env-database-url-name <string>]
  [--env-include-database-url]
  [--env-prefix <string>]
  [--format <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--version]
```

## 选项 {#options}

- `--db-cluster-id <string>`: Starter DB 集群 ID。\[required]
- `--admin`: 使用预设的管理员 DB SQL 凭据。
- `--database <string>`: 数据库/默认 schema 名称。
- `--env-database-url-name <string>`: 用于 `--format env` 的数据库 URL 变量名。\[default: DATABASE_URL]
- `--env-include-database-url`: 在使用 `--format env` 时包含数据库 URL 变量。
- `--env-prefix <string>`: 用于 `--format env` 的 dotenv 变量前缀。\[default: TIDB_]
- `--format <string>`: 连接字符串格式：`mysql-uri`、`jdbc`、`go-sql-driver`、`sqlalchemy` 或 `env`。\[default: mysql-uri]
- `--help`: 显示帮助信息。
- `--read-only`: 使用预设的 `read_only` DB SQL 凭据。
- `--read-write`: 使用预设的 `read_write` DB SQL 凭据。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 格式化读写 MySQL URI：

    ```bash
    # Use the default application role in tools that accept a MySQL URI.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format mysql-uri
    ```

- 格式化只读 dotenv 变量：

    ```bash
    # Emit environment assignments for a workload that must not modify data.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env --env-prefix TIDB_
    ```

- 格式化管理员 JDBC URL：

    ```bash
    # Generate a JDBC connection value with the prepared admin credentials.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --admin --format jdbc --database app
    ```

- 在 dotenv 输出中包含 DATABASE_URL：

    ```bash
    # Emit both component variables and a conventional DATABASE_URL value.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format env --env-include-database-url
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)