---
title: 使用 TiDB 探索 SQL
summary: 了解 TiDB 数据库的基本 SQL 语句。
---

# 使用 TiDB 探索 SQL

TiDB 与 MySQL 兼容，在大多数情况下您可以直接使用 MySQL 语句。有关不支持的功能，请参阅[与 MySQL 的兼容性](/mysql-compatibility.md#unsupported-features)。

<CustomContent platform="tidb">

要试验 SQL 并测试 TiDB 与 MySQL 查询的兼容性，您可以尝试使用 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=basic-sql-operations)。您也可以先部署一个 TiDB 集群，然后在其中运行 SQL 语句。

</CustomContent>

本页将指导您了解基本的 TiDB SQL 语句，如 DDL、DML 和 CRUD 操作。有关 TiDB 语句的完整列表，请参阅 [SQL 语句概览](/sql-statements/sql-statement-overview.md)。

## 分类

SQL 根据其功能分为以下 4 种类型：

- DDL（数据定义语言）：用于定义数据库对象，包括数据库、表、视图和索引。

- DML（数据操作语言）：用于操作应用程序相关的记录。

- DQL（数据查询语言）：用于在条件过滤后查询记录。

- DCL（数据控制语言）：用于定义访问权限和安全级别。

常见的 DDL 功能是创建、修改和删除对象（如表和索引）。相应的命令是 `CREATE`、`ALTER` 和 `DROP`。

## 显示、创建和删除数据库

TiDB 中的数据库可以被视为表和索引等对象的集合。

要显示数据库列表，使用 `SHOW DATABASES` 语句：

{{< copyable "sql" >}}

```sql
SHOW DATABASES;
```

要使用名为 `mysql` 的数据库，使用以下语句：

{{< copyable "sql" >}}

```sql
USE mysql;
```

要显示数据库中的所有表，使用 `SHOW TABLES` 语句：

{{< copyable "sql" >}}

```sql
SHOW TABLES FROM mysql;
```

要创建数据库，使用 `CREATE DATABASE` 语句：

{{< copyable "sql" >}}

```sql
CREATE DATABASE db_name [options];
```

要创建名为 `samp_db` 的数据库，使用以下语句：

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

添加 `IF NOT EXISTS` 可以防止在数据库已存在时出现错误。

要删除数据库，使用 `DROP DATABASE` 语句：

{{< copyable "sql" >}}

```sql
DROP DATABASE samp_db;
```

## 创建、显示和删除表

要创建表，使用 `CREATE TABLE` 语句：

{{< copyable "sql" >}}

```sql
CREATE TABLE table_name column_name data_type constraint;
```

例如，要创建一个名为 `person` 的表，其中包括编号、姓名和生日等字段，使用以下语句：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

要查看创建表的语句（DDL），使用 `SHOW CREATE` 语句：

{{< copyable "sql" >}}

```sql
SHOW CREATE table person;
```

要删除表，使用 `DROP TABLE` 语句：

{{< copyable "sql" >}}

```sql
DROP TABLE person;
```

## 创建、显示和删除索引

索引用于加快对索引列的查询。要为值不唯一的列创建索引，使用 `CREATE INDEX` 语句：

{{< copyable "sql" >}}

```sql
CREATE INDEX person_id ON person (id);
```

或使用 `ALTER TABLE` 语句：

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

要为值唯一的列创建唯一索引，使用 `CREATE UNIQUE INDEX` 语句：

{{< copyable "sql" >}}

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

或使用 `ALTER TABLE` 语句：

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

要显示表中的所有索引，使用 `SHOW INDEX` 语句：

{{< copyable "sql" >}}

```sql
SHOW INDEX FROM person;
```

要删除索引，使用 `DROP INDEX` 或 `ALTER TABLE` 语句。`DROP INDEX` 可以嵌套在 `ALTER TABLE` 中：

{{< copyable "sql" >}}

```sql
DROP INDEX person_id ON person;
```

{{< copyable "sql" >}}

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **注意：**
> 
> DDL 操作不是事务。执行 DDL 操作时不需要运行 `COMMIT` 语句。

## 插入、更新和删除数据

常见的 DML 功能是添加、修改和删除表记录。相应的命令是 `INSERT`、`UPDATE` 和 `DELETE`。

要向表中插入数据，使用 `INSERT` 语句：

{{< copyable "sql" >}}

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

要向表中插入包含某些字段数据的记录，使用 `INSERT` 语句：

{{< copyable "sql" >}}

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

要更新表中记录的某些字段，使用 `UPDATE` 语句：

{{< copyable "sql" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

要删除表中的数据，使用 `DELETE` 语句：

{{< copyable "sql" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **注意：**
> 
> 没有 `WHERE` 子句作为过滤器的 `UPDATE` 和 `DELETE` 语句会对整个表进行操作。

## 查询数据

DQL 用于从一个或多个表中检索所需的数据行。

要查看表中的数据，使用 `SELECT` 语句：

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

要查询特定列，在 `SELECT` 关键字后添加列名：

{{< copyable "sql" >}}

```sql
SELECT name FROM person;
```

```sql
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 子句过滤所有匹配条件的记录，然后返回结果：

{{< copyable "sql" >}}

```sql
SELECT * FROM person where id<5;
```

## 创建、授权和删除用户

DCL 通常用于创建或删除用户，以及管理用户权限。

要创建用户，使用 `CREATE USER` 语句。以下示例创建一个名为 `tiuser`，密码为 `123456` 的用户：

{{< copyable "sql" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

要授予 `tiuser` 检索 `samp_db` 数据库中表的权限：

{{< copyable "sql" >}}

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

要检查 `tiuser` 的权限：

{{< copyable "sql" >}}

```sql
SHOW GRANTS for tiuser@localhost;
```

要删除 `tiuser`：

{{< copyable "sql" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
