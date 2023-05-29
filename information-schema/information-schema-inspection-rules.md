---
title: INSPECTION_RULES
summary: 了解 information_schema 表 `INSPECTION_RULES`。
---

# INSPECTION_RULES

`INSPECTION_RULES` 表提供在检查结果中运行哪些诊断测试的信息，示例用法参见[`inspection-result` 表](/information-schema/information-schema-inspection-result.md)。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC inspection_rules;
```

```sql
+---------+--------------+------+------+---------+-------+
| Field   | Type         | Null | Key  | Default | Extra |
+---------+--------------+------+------+---------+-------+
| NAME    | varchar(64)  | YES  |      | NULL    |       |
| TYPE    | varchar(64)  | YES  |      | NULL    |       |
| COMMENT | varchar(256) | YES  |      | NULL    |       |
+---------+--------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM inspection_rules;
```

```sql
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| node-load       | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
| ddl             | summary    |         |
| gc              | summary    |         |
| pd              | summary    |         |
| query-summary   | summary    |         |
| raftstore       | summary    |         |
| read-link       | summary    |         |
| rocksdb         | summary    |         |
| stats           | summary    |         |
| wait-events     | summary    |         |
| write-link      | summary    |         |
+-----------------+------------+---------+
15 rows in set (0.00 sec)
```
