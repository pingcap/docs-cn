---
title: PLACEMENT_RULES
summary: 了解 information_schema 表 `PLACEMENT_RULES`。
---

# PLACEMENT_RULES

`PLACEMENT_RULES` 表展示所有已显式配置的 [Placement Rules in SQL](/placement-rules-in-sql.md) 信息，包括通过放置策略 (placement policy) 和通过直接放置 (directly placement) 进行配置的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC placement_rules;
```

```sql
+----------------------+--------------+------+------+---------+-------+
| Field                | Type         | Null | Key  | Default | Extra |
+----------------------+--------------+------+------+---------+-------+
| POLICY_ID            | bigint(64)   | NO   |      | NULL    |       |
| CATALOG_NAME         | varchar(512) | NO   |      | NULL    |       |
| POLICY_NAME          | varchar(5)   | YES  |      | NULL    |       |
| SCHEMA_NAME          | varchar(5)   | YES  |      | NULL    |       |
| TABLE_NAME           | varchar(5)   | YES  |      | NULL    |       |
| PARTITION_NAME       | varchar(5)   | YES  |      | NULL    |       |
| PRIMARY_REGION       | varchar(5)   | NO   |      | NULL    |       |
| REGIONS              | varchar(5)   | NO   |      | NULL    |       |
| CONSTRAINTS          | varchar(5)   | NO   |      | NULL    |       |
| LEADER_CONSTRAINTS   | varchar(5)   | NO   |      | NULL    |       |
| FOLLOWER_CONSTRAINTS | varchar(5)   | NO   |      | NULL    |       |
| LEARNER_CONSTRAINTS  | varchar(5)   | NO   |      | NULL    |       |
| SCHEDULE             | varchar(20)  | NO   |      | NULL    |       |
| FOLLOWERS            | bigint(64)   | NO   |      | NULL    |       |
| LEARNERS             | bigint(64)   | NO   |      | NULL    |       |
+----------------------+--------------+------+------+---------+-------+
15 rows in set (0.00 sec)
```

## 示例

`PLACEMENT_RULES` 表只展示显式配置的规则。如要查看 Placement Rules 放置规则的规范版本（包括附加到表格的放置策略），请改用 `SHOW PLACEMENT` 语句：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT) primary_region="us-east-1" regions="us-east-1";
CREATE PLACEMENT POLICY p1 primary_region="us-east-1" regions="us-east-1";
CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT; -- 包含 t3。
SELECT * FROM information_schema.placement_rules; -- 不包含 t3。
```

```sql
Query OK, 0 rows affected (0.09 sec)

Query OK, 0 rows affected (0.11 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.11 sec)

+---------------+------------------------------------------------+
| Target        | Placement                                      |
+---------------+------------------------------------------------+
| POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1" |
| TABLE test.t2 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1" |
| TABLE test.t3 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1" |
+---------------+------------------------------------------------+
3 rows in set (0.00 sec)

+-----------+--------------+-------------+-------------+------------+----------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
| POLICY_ID | CATALOG_NAME | POLICY_NAME | SCHEMA_NAME | TABLE_NAME | PARTITION_NAME | PRIMARY_REGION | REGIONS   | CONSTRAINTS | LEADER_CONSTRAINTS | FOLLOWER_CONSTRAINTS | LEARNER_CONSTRAINTS | SCHEDULE | FOLLOWERS | LEARNERS |
+-----------+--------------+-------------+-------------+------------+----------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
|         3 | def          | p1          | NULL        | NULL       | NULL           | us-east-1      | us-east-1 |             |                    |                      |                     |          |         0 |        0 |
|      NULL | def          | NULL        | test        | t2         | NULL           | us-east-1      | us-east-1 |             |                    |                      |                     |          |         0 |        0 |
+-----------+--------------+-------------+-------------+------------+----------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
2 rows in set (0.00 sec)
```
