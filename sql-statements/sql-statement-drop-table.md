---
title: DROP TABLE
summary: TiDB 数据库中 DROP TABLE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-drop-table/','/docs-cn/dev/reference/sql/statements/drop-table/']
---

# DROP TABLE

`DROP TABLE` 语句用于从当前所选的数据库中删除表。如果表不存在则会报错，除非使用 `IF EXISTS` 修饰符。

## 语法图

```ebnf+diagram
DropTableStmt ::=
    'DROP' OptTemporary TableOrTables IfExists TableNameList RestrictOrCascadeOpt

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameList ::=
    TableName ( ',' TableName )*
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
DROP TABLE t1;
```

```
Query OK, 0 rows affected (0.22 sec)
```

{{< copyable "sql" >}}

```sql
DROP TABLE table_not_exists;
```

```
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'
```

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS table_not_exists;
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
CREATE VIEW v1 AS SELECT 1;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
DROP TABLE v1;
```

```
Query OK, 0 rows affected (0.23 sec)
```

## MySQL 兼容性

* 在尝试删除不存在的表时，使用 `IF EXISTS` 删除表不会返回警告。[Issue #7867](https://github.com/pingcap/tidb/issues/7867)
* 目前 `RESTRICT` 和 `CASCADE` 仅在语法上支持。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
