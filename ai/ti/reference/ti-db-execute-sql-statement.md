---
title: ti db execute-sql-statement
summary: 对 TiDB Cloud Starter 集群执行一条 SQL 语句。
---

# ti db execute-sql-statement

对 TiDB Cloud Starter 实例执行一条 SQL 语句。默认访问角色为 read-write；建议显式指定角色。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti db execute-sql-statement
  --db-cluster-id <string>
  --sql <string>
  [--admin]
  [--database <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--transport <string>]
  [--version]
```

## 选项 {#options}

- `--db-cluster-id <string>`: Starter DB cluster ID。\[必需]
- `--sql <string>`: 要执行的一条 SQL 语句。\[必需]
- `--admin`: 使用预置的 admin DB SQL 凭据。
- `--database <string>`: 数据库/默认 schema 名称。
- `--help`: 显示帮助信息。
- `--read-only`: 使用预置的 `read_only` DB SQL 凭据。
- `--read-write`: 使用预置的 `read_write` DB SQL 凭据。
- `--transport <string>`: SQL 执行传输方式：`https` 或 `mysql`。\[默认值: https]
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 使用默认 read-write 角色运行一条语句：

    ```bash
    # Use the default prepared role for normal application reads and writes.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --sql "INSERT INTO app.events(message) VALUES ('ready')"
    ```

- 运行只读查询：

    ```bash
    # Prevent the statement from using read-write or admin credentials.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1 AS ready" --output text
    ```

- 运行管理语句：

    ```bash
    # Use the admin role for schema creation or privilege management.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --admin --sql "CREATE DATABASE IF NOT EXISTS app"
    ```

- 使用 MySQL 回退传输方式：

    ```bash
    # Open a direct TLS MySQL connection when the workflow requires the MySQL protocol.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --transport mysql --sql "SELECT CURRENT_TIMESTAMP"
    ```

## 选择传输方式 {#choose-a-transport}

默认的 `https` 传输方式会将语句发送到 TiDB Cloud HTTPS SQL API。`mysql` 传输方式会直接通过 TLS MySQL 连接到该实例，执行一次语句后关闭连接。仅当你的网络环境或工作流明确要求使用 MySQL 协议时，才使用 `mysql`。

CLI 不会自动从 `https` 回退到 `mysql`，也不会通过另一种传输方式重试语句。这样可以防止在发生结果不明确的故障后，写语句被执行两次。

## 输出 {#output}

JSON 输出在适用时包含 `fields`、`rows`、`row_count`、`rows_affected`、`last_insert_id`，以及 `transport`、`access_mode` 和 `cluster_id`。`rows` 中的每一项都是一个以列名为键的对象。

使用 `--output text` 时，查询结果会以带列标题和行数统计的表格形式呈现。不返回行的语句会生成一条 `Query OK` 消息，其中包含受影响的行数，以及在可用时显示最后插入 ID。

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)