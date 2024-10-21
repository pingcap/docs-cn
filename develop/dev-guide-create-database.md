---
title: 创建数据库
summary: 创建数据库的方法、规范及例子。
aliases: ['/zh/tidb/dev/create-database']
---

# 创建数据库

在这个章节当中，将开始介绍如何使用 SQL 来创建数据库，及创建数据库时应遵守的规则。将在这个章节中围绕 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 这个应用程序来对 TiDB 的创建数据库部分展开介绍。

> **注意：**
>
> 此处仅对 `CREATE DATABASE` 语句进行简单描述，详细参考文档（包含其他示例），可参阅 [CREATE DATABASE](/sql-statements/sql-statement-create-database.md) 文档。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)。

## 什么是数据库

在 TiDB 中[数据库](/develop/dev-guide-schema-design-overview.md#数据库-database)对象可以包含**表**、**视图**、**序列**等对象。

## 创建数据库过程

可使用 `CREATE DATABASE` 语句来创建数据库。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

此语句会创建一个名为 `bookshop` 的数据库（如果尚不存在）。请以 `root` 用户身份执行文件中的建库语句，运行以下命令：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

要查看集群中的数据库，可在命令行执行一条 `SHOW DATABASES` 语句：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

运行结果为：

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

## 数据库创建时应遵守的规则

- 遵循[数据库命名规范](/develop/dev-guide-object-naming-guidelines.md#数据库命名规范)，给你的数据库起一个有意义的名字。
- `test` 数据库是 TiDB 提供的一个默认数据库。如果没有必要，尽量不要在生产环境使用它。你可以自行使用 `CREATE DATABASE` 语句来创建数据库，并且在 SQL 会话中使用 `USE {databasename};` 语句来[更改当前数据库](/sql-statements/sql-statement-use.md)。
- 使用 root 用户创建数据库、角色、用户等，并只赋予必要的权限。
- 作为通用的规则，不推荐使用 Driver、ORM 进行数据库模式的定义与更改。相反，请使用 **MySQL 命令行客户端**或其他你喜欢的 **MySQL GUI 客户端**来进行操作。

## 更进一步

至此，你已经准备完毕 `bookshop` 数据库，可以将**表**添加到该数据库中。

你可继续阅读[创建表](/develop/dev-guide-create-table.md)文档获得相关指引。
