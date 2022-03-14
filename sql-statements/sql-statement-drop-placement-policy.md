---
title: DROP PLACEMENT POLICY
summary: TiDB 数据库中 ALTER PLACEMENT POLICY 的使用概况。
---

# DROP PLACEMENT POLICY

`DROP PLACEMENT POLICY` 用于删除已创建的放置策略。

## 语法图

```ebnf+diagram
DropPolicyStmt ::=
    "DROP" "PLACEMENT" "POLICY" IfExists PolicyName

PolicyName ::=
    Identifier
```

## 示例

删除放置策略时，确保该策略未被任何表或分区引用，否则会删除失败。

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
CREATE TABLE t1 (a INT PRIMARY KEY) PLACEMENT POLICY=p1;
DROP PLACEMENT POLICY p1;  -- 该语句执行失败，因为放置策略 p1 被引用。

-- 查看引用放置策略的表和分区。
SELECT table_schema, table_name FROM information_schema.tables WHERE tidb_placement_policy_name='p1';
SELECT table_schema, table_name FROM information_schema.partitions WHERE tidb_placement_policy_name='p1';

ALTER TABLE t1 PLACEMENT POLICY=default;  -- 移除表 t1 上的默认放置策略。
DROP PLACEMENT POLICY p1;  -- 执行成功。
```

```sql
Query OK, 0 rows affected (0.10 sec)

Query OK, 0 rows affected (0.11 sec)

ERROR 8241 (HY000): Placement policy 'p1' is still in use

+--------------+------------+
| table_schema | table_name |
+--------------+------------+
| test         | t1         |
+--------------+------------+
1 row in set (0.00 sec)

Empty set (0.01 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.21 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [ALTER PLACEMENT POLICY](/sql-statements/sql-statement-alter-placement-policy.md)
