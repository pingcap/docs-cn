---
title: TiDB 中的 CRUD SQL
summary: TiDB CRUD SQL 的简要介绍。
---

# TiDB 中的 CRUD SQL

本文简要介绍如何使用 TiDB 的 CRUD SQL。

## 开始之前

请确保你已连接到 TiDB 集群。如果没有，请参考[构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)来创建一个 TiDB Cloud Serverless 集群。

## 使用 TiDB 探索 SQL

> **注意：**
>
> 本文参考并简化了[使用 TiDB 探索 SQL](/basic-sql-operations.md)。更多详细信息，请参见[使用 TiDB 探索 SQL](/basic-sql-operations.md)。

TiDB 与 MySQL 兼容，在大多数情况下你可以直接使用 MySQL 语句。有关不支持的功能，请参见[与 MySQL 的兼容性](/mysql-compatibility.md#unsupported-features)。

要试验 SQL 并测试 TiDB 与 MySQL 查询的兼容性，你可以尝试使用 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=basic-sql-operations)。你也可以先部署一个 TiDB 集群，然后在其中运行 SQL 语句。

本页将指导你了解基本的 TiDB SQL 语句，如 DDL、DML 和 CRUD 操作。有关 TiDB 语句的完整列表，请参见 [SQL 语句概览](/sql-statements/sql-statement-overview.md)。

## 分类

SQL 根据其功能分为以下 4 种类型：

- **DDL（数据定义语言）**：用于定义数据库对象，包括数据库、表、视图和索引。

- **DML（数据操作语言）**：用于操作应用程序相关的记录。

- **DQL（数据查询语言）**：用于在条件过滤后查询记录。

- **DCL（数据控制语言）**：用于定义访问权限和安全级别。

以下主要介绍 DML 和 DQL。有关 DDL 和 DCL 的更多信息，请参见[使用 TiDB 探索 SQL](/basic-sql-operations.md)或 [SQL 语句概览](/sql-statements/sql-statement-overview.md)。

## 数据操作语言

常见的 DML 功能是添加、修改和删除表记录。对应的命令是 `INSERT`、`UPDATE` 和 `DELETE`。

要向表中插入数据，使用 `INSERT` 语句：

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

要向表中插入包含部分字段数据的记录，使用 `INSERT` 语句：

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

要更新表中某条记录的部分字段，使用 `UPDATE` 语句：

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

要删除表中的数据，使用 `DELETE` 语句：

```sql
DELETE FROM person WHERE id=2;
```

> **注意：**
>
> 没有 `WHERE` 子句作为过滤条件的 `UPDATE` 和 `DELETE` 语句会对整个表进行操作。

## 数据查询语言

DQL 用于从一个或多个表中检索所需的数据行。

要查看表中的数据，使用 `SELECT` 语句：

```sql
SELECT * FROM person;
```

要查询特定列，在 `SELECT` 关键字后添加列名：

```sql
SELECT name FROM person;
```

结果如下：

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 子句过滤所有匹配条件的记录，然后返回结果：

```sql
SELECT * FROM person WHERE id < 5;
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
