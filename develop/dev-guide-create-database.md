---
title: 创建数据库
summary: 了解创建数据库的步骤、规则和示例。
---

# 创建数据库

本文档介绍如何使用 SQL 和各种编程语言创建数据库，并列出了数据库创建的规则。在本文档中，以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序为例，指导您完成数据库创建的步骤。

## 开始之前

在创建数据库之前，请执行以下操作：

- [构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[架构设计概述](/develop/dev-guide-schema-design-overview.md)。

## 什么是数据库

TiDB 中的[数据库](/develop/dev-guide-schema-design-overview.md)对象包含**表**、**视图**、**序列**和其他对象。

## 创建数据库

要创建数据库，您可以使用 `CREATE DATABASE` 语句。

例如，要创建一个名为 `bookshop` 的数据库（如果它不存在），请使用以下语句：

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

有关 `CREATE DATABASE` 语句的更多信息和示例，请参见 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) 文档。

要以 `root` 用户身份执行库构建语句，请运行以下命令：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

## 查看数据库

要查看集群中的数据库，请使用 [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) 语句。

例如：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

以下是示例输出：

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

## 数据库创建规则

- 遵循[数据库命名约定](/develop/dev-guide-object-naming-guidelines.md)，为数据库命名时要有意义。
- TiDB 自带一个名为 `test` 的默认数据库。但是，如果不是必须，建议不要在生产环境中使用它。您可以使用 `CREATE DATABASE` 语句创建自己的数据库，并在 SQL 会话中使用 [`USE {databasename};`](/sql-statements/sql-statement-use.md) 语句更改当前数据库。
- 使用 `root` 用户创建数据库、角色和用户等对象。仅向角色和用户授予必要的权限。
- 作为最佳实践，建议使用 **MySQL 命令行客户端**或 **MySQL GUI 客户端**而不是驱动程序或 ORM 来执行数据库架构更改。

## 下一步

创建数据库后，您可以向其添加**表**。更多信息，请参见[创建表](/develop/dev-guide-create-table.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
