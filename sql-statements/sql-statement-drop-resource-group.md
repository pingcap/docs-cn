---
title: DROP RESOURCE GROUP
summary: TiDB 数据库中 DROP RESOURCE GROUP 的使用概况。
---

# DROP RESOURCE GROUP

`DROP RESOURCE GROUP` 语句用于在当前所选数据库中删除资源组。

## 语法图

```ebnf+diagram
DropResourceGroupStmt ::=
    "DROP" "RESOURCE" "GROUP" IfExists ResourceGroupName

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

> **注意：**
>
> - `DROP RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 设置为 `ON` 时才能执行。
> - `default` 资源组为系统保留的资源组，不支持删除。

## 示例

删除名为 `rg1` 的资源组：

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 500        | MEDIUM   | YES       | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.01 sec)
```

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 1 rows affected (0.09 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
Empty set (0.00 sec)
```

## MySQL 兼容性

MySQL 也支持 [DROP RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/drop-resource-group.html)，但 TiDB 不支持 `FORCE` 参数。

## 另请参阅

* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [RU](/tidb-resource-control.md#什么是-request-unit-ru)
