---
title: 列级权限管理
summary: TiDB 支持兼容 MySQL 的列级权限管理机制。你可以通过 `GRANT` 或 `REVOKE` 在指定表上对指定列授予或回收 `SELECT`、`INSERT`、`UPDATE`、`REFERENCES` 权限，实现更细粒度的访问控制。
---

# 列级权限管理

从 v8.5.6 版本开始，TiDB 支持兼容 MySQL 的列级权限管理机制。通过列级权限，你可以在指定表上对指定列授予或回收 `SELECT`、`INSERT`、`UPDATE`、`REFERENCES` 权限，从而实现更细粒度的数据访问控制。

> **注意：**
>
> 虽然 MySQL 语法允许 `REFERENCES(col_name)` 这种列级写法，但 `REFERENCES` 本身属于数据库/表级权限，用于外键相关的权限检查。因此，列级 `REFERENCES` 在 MySQL 中不会带来实际的列级权限效果。TiDB 的行为与 MySQL 保持一致。

## 语法

列级权限的授予和回收语法与表级权限类似，区别如下：

- 列名列表写在**权限类型**后面，而不是写在**表名**后面。
- 多个列名之间使用逗号（`,`）分隔。

```sql
GRANT priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    TO 'user'@'host';

REVOKE priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    FROM 'user'@'host';
```

其中：

* `priv_type` 支持 `SELECT`、`INSERT`、`UPDATE` 和 `REFERENCES`。
* `ON` 后必须指定具体表，例如 `test.tbl`。
* 同一条 `GRANT` 或 `REVOKE` 语句可以包含多个权限项，每个权限项都可以指定自己的列名列表。

例如，以下语句表示将 `col1`、`col2` 的 `SELECT` 权限和 `col3` 的 `UPDATE` 权限授予用户：

```sql
GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'user'@'host';
```

## 授予列级权限示例

以下示例将表 `test.tbl` 中 `col1` 和 `col2` 的 `SELECT` 权限授予用户 `newuser`，并将 `col3` 的 `UPDATE` 权限授予该用户：

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

DROP TABLE IF EXISTS tbl;
CREATE TABLE tbl (col1 INT, col2 INT, col3 INT);

DROP USER IF EXISTS 'newuser'@'%';
CREATE USER 'newuser'@'%';

GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

```
+---------------------------------------------------------------------+
| Grants for newuser@%                                                |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'                                 |
| GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
+---------------------------------------------------------------------+
```

除了使用 `SHOW GRANTS`，你还可以通过查询 `INFORMATION_SCHEMA.COLUMN_PRIVILEGES` 查看列级权限信息。

## 回收列级权限示例

以下示例从用户 `newuser` 收回列 `col2` 的 `SELECT` 权限：

```sql
REVOKE SELECT(col2) ON test.tbl FROM 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

```
+---------------------------------------------------------------+
| Grants for newuser@%                                          |
+---------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'                           |
| GRANT SELECT(col1), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
+---------------------------------------------------------------+
```

## 列级权限访问控制示例

在授予或回收列级权限后，TiDB 会对 SQL 中引用的列进行权限检查。例如：

* `SELECT` 语句：`SELECT` 列权限会影响 `SELECT` 列表以及 `WHERE`、`ORDER BY` 等子句中引用的列。
* `UPDATE` 语句：`SET` 子句中被更新的列需要 `UPDATE` 列权限。在表达式、条件中被读取的列通常还需要 `SELECT` 列权限。
* `INSERT` 语句：被写入的列需要 `INSERT` 列权限。`INSERT INTO t VALUES (...)` 等价于按表定义顺序向所有列写入值。

以下示例中，用户 `newuser` 仅能查询 `col1`，并更新 `col3`：

```sql
-- 以 newuser 登录执行
SELECT col1 FROM tbl;
SELECT * FROM tbl; -- 报错（缺少 col2、col3 的 SELECT 列权限）

UPDATE tbl SET col3 = 1;
UPDATE tbl SET col1 = 2; -- 报错（缺少 col1 的 UPDATE 列权限）

UPDATE tbl SET col3 = col1;
UPDATE tbl SET col3 = col3 + 1; -- 报错（缺少 col3 的 SELECT 列权限）
UPDATE tbl SET col3 = col1 WHERE col1 > 0;
```

## 与 MySQL 的兼容性差异

TiDB 的列级权限整体与 MySQL 兼容，但在以下场景存在差异：

| 场景                     | TiDB                        | MySQL                         |
| :----------------------- | :-------------------------- | :---------------------------- |
| 收回用户未被授予的列级权限             | `REVOKE` 可以成功执行                  | 在未使用 `IF EXISTS` 时，`REVOKE` 会报错               |
| 列裁剪与 `SELECT` 列权限检查的执行顺序 | 先检查 `SELECT` 列权限，再进行列裁剪。例如，执行 `SELECT a FROM (SELECT a, b FROM t) s` 需要同时拥有 `t.a` 和 `t.b` 的 `SELECT` 列权限。 | 先进行列裁剪，再检查 `SELECT` 列权限。例如，执行 `SELECT a FROM (SELECT a, b FROM t) s` 只需要 `t.a` 的 `SELECT` 列权限。 |

### 视图场景的列裁剪与权限检查

在对视图进行 `SELECT` 权限检查时，MySQL 和 TiDB 存在以下差异：

- MySQL 会先对视图内部查询做列裁剪，再检查内部表的列权限，因此在某些场景下检查相对宽松。
- TiDB 不会在权限检查之前做列裁剪，因此可能需要额外的列权限。

```sql
-- 以 root 登录准备环境
DROP USER IF EXISTS 'u'@'%';
CREATE USER 'u'@'%';

DROP TABLE IF EXISTS t;
CREATE TABLE t (a INT, b INT, c INT, d INT);

DROP VIEW IF EXISTS v;
CREATE SQL SECURITY INVOKER VIEW v AS SELECT a, b FROM t WHERE c = 0 ORDER BY d;

GRANT SELECT ON v TO 'u'@'%';

-- 以 u 登录
SELECT a FROM v;
-- MySQL：报错，缺少对 t.a、t.c、t.d 的访问权限
-- TiDB：报错，缺少对 t.a、t.b、t.c、t.d 的访问权限

-- 以 root 登录
GRANT SELECT(a, c, d) ON t TO 'u'@'%';

-- 以 u 登录
SELECT a FROM v;
-- MySQL：成功（会将内部查询裁剪为 `SELECT a FROM t WHERE c = 0 ORDER BY d`）
-- TiDB：报错，缺少对 t.b 的访问权限

SELECT * FROM v;
-- MySQL：报错，缺少对 t.b 的访问权限
-- TiDB：报错，缺少对 t.b 的访问权限

-- 以 root 登录
GRANT SELECT(b) ON t TO 'u'@'%';

-- 以 u 登录
SELECT * FROM v;
-- MySQL：成功
-- TiDB：成功
```

## 另请参阅

* [权限管理](/privilege-management.md)
* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
