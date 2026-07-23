---
title: 使用显式 SQL 角色查询 TiDB Cloud Starter
summary: 准备 tdc 管理的 SQL 用户，并以明确权限意图运行只读、读写和管理员 statement。
---

# 使用显式 SQL 角色查询 TiDB Cloud Starter

本示例让 Agent 完成 schema、数据写入和结果验证，同时为每条 SQL 明确指定所需权限。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## Agent 面临的问题

能够读取数据的 Agent，有时还需要执行 migration 或更新数据。让整个任务共用一个管理员连接最为方便，但 Agent 在检查数据时一旦生成错误 SQL，也会拥有修改或删除数据的权限。只提供只读连接又无法完成合理的写入和 schema 变更。

## 单一原生数据库连接为什么不够

TiDB 本身支持 SQL 权限，但传统客户端 session 只使用当前连接凭证对应的权限。用户需要自行创建、保存和切换多组凭证，Agent 也可能在任务阶段变化后继续使用权限过高的连接。

## tdc 如何改变工作流

`tdc db create-db-sql-users` 创建稳定的 read-only、read-write 和 admin 身份，并在本地保存对应凭证。每次执行 `execute-sql-statement` 时都显式选择一个角色，并且一次只执行一条 SQL。Agent 可以使用 admin 修改 schema、使用 read-write 修改数据，再使用 read-only 验证结果，全程无需直接处理密码。

## 前置条件

- 配置 tdc。
- 选择一个 active Starter cluster ID。

## 第 1 步：准备用户

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

该命令可重入，会创建或修复 `read_only`、`read_write` 和 `admin` 凭证。

## 第 2 步：使用 admin 修改 schema

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS role_demo"

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --database role_demo \
  --sql "CREATE TABLE IF NOT EXISTS messages (id BIGINT PRIMARY KEY, body VARCHAR(255))"
```

## 第 3 步：使用 read-write 修改数据

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database role_demo \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello') ON DUPLICATE KEY UPDATE body = VALUES(body)"
```

## 第 4 步：使用 read-only 验证

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --sql "SELECT id, body FROM messages ORDER BY id" \
  --output text
```

预期结果包含 ID `1` 和 body `hello`。

## 第 5 步：格式化连接环境

将输出直接写入受保护的本地文件，而不是显示：

```bash
umask 077
tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --format env \
  --env-include-database-url > .env.tidb
```

不要提交 `.env.tidb`。

## 清理

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "DROP DATABASE role_demo"

rm -f .env.tidb
```

## 安全说明

- 每条 statement 使用权限最低的显式角色。
- 每次 tdc 调用只接受一条 SQL statement。
- 默认 transport 为 HTTPS；`--transport mysql` 是显式回退。
- 连接字符串和环境变量输出包含凭证。

## 后续步骤

- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
