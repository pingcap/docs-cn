---
title: TiDB 中的基本 SQL 操作
category: how-to
aliases: ['/docs-cn/try-tidb/']
---

# TiDB 中的基本 SQL 操作

成功部署 TiDB 集群之后，便可以在 TiDB 中执行 SQL 语句了。因为 TiDB 兼容 MySQL，你可以使用 MySQL 客户端连接 TiDB，并且[大多数情况下](/sql/mysql-compatibility.md)可以直接执行 MySQL 语句。

本文介绍 CRUD 操作等基本的 SQL 语句。完整的 SQL 语句列表，参见 [TiDB SQL 语法详解](https://pingcap.github.io/sqlgram/)。

## 创建、查看和删除数据库

使用 `CREATE DATABASE` 语句创建数据库。语法如下：

```sql
CREATE DATABASE db_name [options];
```

例如，要创建一个名为 `samp_db` 的数据库，可使用以下语句：

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

使用 `SHOW DATABASES` 语句查看数据库：

```sql
SHOW DATABASES;
```

使用 `DROP DATABASE` 语句删除数据库，例如：

```sql
DROP DATABASE samp_db;
```

## 创建、查看和删除表

使用 `CREATE TABLE` 语句创建表。语法如下：

```sql
CREATE TABLE table_name column_name data_type constraint;
```

例如：

```sql
CREATE TABLE person (
    number INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

如果表已存在，添加 `IF NOT EXISTS` 可防止发生错误：

```sql
CREATE TABLE IF NOT EXISTS person (
      number INT(11),
      name VARCHAR(255),
      birthday DATE
);
```

使用 `SHOW CREATE` 语句查看建表语句。例如：

```sql
SHOW CREATE table person;
```

使用 `SHOW FULL COLUMNS` 语句查看表的列。 例如：

```sql
SHOW FULL COLUMNS FROM person;
```

使用 `DROP TABLE` 语句删除表。例如：

```sql
DROP TABLE person;
```

或者

```sql
DROP TABLE IF EXISTS person;
```

使用 `SHOW TABLES` 语句查看数据库中的所有表。例如：

```sql
SHOW TABLES FROM samp_db;
```

## 创建、查看和删除索引

对于值不唯一的列，可使用 `CREATE INDEX` 或 `ALTER TABLE` 语句。例如：

```sql
CREATE INDEX person_num ON person (number);
```

或者

```sql
ALTER TABLE person ADD INDEX person_num (number);
```

对于值唯一的列，可以创建唯一索引。例如：

```sql
CREATE UNIQUE INDEX person_num ON person (number);
```

或者

```sql
ALTER TABLE person ADD UNIQUE person_num (number);
```

使用 `SHOW INDEX` 语句查看表内所有索引：

```sql
SHOW INDEX from person;
```

使用 `ALTER TABLE` 或 `DROP INDEX` 语句来删除索引。与 `CREATE INDEX` 语句类似，`DROP INDEX` 也可以嵌入 `ALTER TABLE` 语句。例如：

```sql
DROP INDEX person_num ON person;
ALTER TABLE person DROP INDEX person_num;
```

## 增删改查数据

使用 `INSERT` 语句向表内插入数据。例如：

```sql
INSERT INTO person VALUES("1","tom","20170912");
```

使用 `SELECT` 语句检索表内数据。例如：

```sql
SELECT * FROM person;
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-09-12 |
+--------+------+------------+
```

使用 `UPDATE` 语句修改表内数据。例如：

```sql
UPDATE person SET birthday='20171010' WHERE name='tom';

SELECT * FROM person;
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-10-10 |
+--------+------+------------+
```

使用 `DELETE` 语句删除表内数据：

```sql
DELETE FROM person WHERE number=1;
SELECT * FROM person;
Empty set (0.00 sec)
```

## 创建、授权和删除用户

使用 `CREATE USER` 语句创建一个用户 `tiuser`，密码为 `123456`：

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

授权用户 `tiuser` 可检索数据库 `samp_db` 内的表：

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

查询用户 `tiuser` 的权限：

```sql
SHOW GRANTS for tiuser@localhost;
```

删除用户 `tiuser`：

```sql
DROP USER 'tiuser'@'localhost';
```
