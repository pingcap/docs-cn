---
title: 创建数据库
summary: 创建数据库的方法、最佳实践及例子。
---

# 创建数据库

此页面提供了一个创建数据库的最佳实践指南，并提供了一个基于 TiDB 的 [bookshop](/develop/bookshop-schema-design.md) 数据库的示例。

> **注意：**
>
> 有关该 `CREATE DATABASE` 语句的详细参考文档，包含其他示例，可参阅 [CREATE DATABASE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-database) 文档。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (DevTier) 构建 TiDB 集群](/develop/build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/schema-design-overview.md)。

## 创建数据库

[数据库](/develop/schema-design-overview.md#数据库-database)对象是 TiDB **表**、**视图**、**序列**等对象的集合。

若需创建数据库，请使用 `CREATE DATABASE` 语句，并遵循[数据库最佳实践](#数据库最佳实践)。

### 数据库最佳实践

这里是一些当你创建和使用数据库时可遵循的最佳实践：

- 尽量不要使用已存在的 `test` 数据库。而是应该使用 `CREATE DATABASE` 语句来创建数据库，并且在 SQL 会话中使用 `USE {databasename};` 语句来[更改当前数据库](https://docs.pingcap.com/zh/tidb/stable/sql-statement-use)。
- 使用 root 用户创建数据库、角色、用户等。并只赋予必要的权限。
- 作为通用的最佳实践，我们不推荐使用 Driver、ORM 进行数据库模式的定义与更改。相反，请使用 **MySQL 命令行客户端**或其他你喜欢的 **MySQL GUI 客户端**来进行操作。
- 遵循[数据库命名规范](/develop/object-naming-guidelines.md#数据库命名规范)。

### 示例

创建一个在文件末尾带有 `.sql` 文件拓展名的空文件。我们将使用该文件初始化数据库，该数据库将存储 `bookshop` 整个示例应用程序的所有数据。

例如：

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

至此，你已经准备完毕 `bookshop` 数据库，可以将**表**添加到该数据库中。

你可继续阅读[创建表](/develop/create-table.md)文档获得相关指引。
