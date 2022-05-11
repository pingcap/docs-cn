---
title: 创建数据库
summary: 创建数据库的方法、最佳实践及例子。
---

# 创建数据库

在这个章节当中，我们将开始介绍如何使用 SQL 以及多种编程语言来创建数据库，及创建数据库的最佳实践指南。

> **注意：**
>
> 此处我们仅对 `CREATE DATABASE` 语句进行简单描述，详细参考文档（包含其他示例），可参阅 [CREATE DATABASE](/sql-statements/sql-statement-create-database.md) 文档。

## 在开始之前

下面我们将围绕 [Bookshop](/develop/bookshop-schema-design.md) 这个应用程序来对 TiDB 的创建数据库部分展开介绍。

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (DevTier) 构建 TiDB 集群](/develop/build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/schema-design-overview.md)。

## 创建数据库过程

在 TiDB 中[数据库](/develop/schema-design-overview.md#数据库-database)对象可以包含**表**、**视图**、**序列**等对象。

可使用 `CREATE DATABASE` 语句来创建数据库。此处将创建一个在文件末尾带有 `.sql` 文件拓展名的空文件。我们将使用该文件初始化数据库，该数据库将存储 `bookshop` 整个示例应用程序的所有数据。

{{< copyable "shell-regular" >}}

```shell
touch dbinit.sql
```

随后，在文本编辑器中打开 `dbinit.sql`，然后在文件顶部添加 `CREATE DATABASE` 语句：

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

此语句会创建一个名为 `bookshop` 的数据库（如果尚不存在）。

`dbinit.sql` 要以 `root` 用户身份执行文件中的建库语句，请运行以下命令：

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < dbinit.sql
```

要查看集群中的数据库，可在命令行执行一条 `SHOW DATABASES` 语句：

{{< copyable "shell-regular" >}}

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

### 数据库创建时应遵守的规则

这里是一些当你创建和使用数据库时可遵循的规则：

- 遵循[数据库命名规范](/develop/object-naming-guidelines.md#数据库命名规范)，给你的数据库起一个有意义的名字。
- `test` 数据库是 TiDB 提供的一个默认数据库。如果没有必要，尽量不要在生产环境使用它。你可以自行使用 `CREATE DATABASE` 语句来创建数据库，并且在 SQL 会话中使用 `USE {databasename};` 语句来[更改当前数据库](/sql-statements/sql-statement-use.md)。
- 使用 root 用户创建数据库、角色、用户等。并只赋予必要的权限。
- 作为通用的规则，我们不推荐使用 Driver、ORM 进行数据库模式的定义与更改。相反，请使用 **MySQL 命令行客户端**或其他你喜欢的 **MySQL GUI 客户端**来进行操作。

## 更进一步

至此，你已经准备完毕 `bookshop` 数据库，可以将**表**添加到该数据库中。

你可继续阅读[创建表](/develop/create-table.md)文档获得相关指引。
