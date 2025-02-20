---
title: SHOW TABLE DISTRIBUTION
summary: 介绍 TiDB 数据库中 SHOW TABLE DISTRIBUTION 的使用概况。
---

# SHOW TABLE DISTRIBUTION

`SHOW TABLE DISTRIBUTION` 语句用于显示指定表的 Region 分布情况。

## 语法图

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" "DISTRIBUTION" TableName

TableName ::=
    (SchemaName ".")? Identifier
```

## 示例

显示当前表 `t1` 的 Region 分布情况:

```sql
SHOW TABLE DISTRIBUTION t1;
```

```
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| DB_NAME | TABLE_NAME | PARTITION_NAME | STORE_ID | STORE_TYPE | REGION_LEADER_NUM | REGION_LEADER_BYTE | REGION_PEER_NUM | REGION_PEER_BYTE |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| db_1    |     t1     |                | 1        | TiKV       |               315 |        24057934521 |            1087 |      86938746542 |
| db_1    |     t1     |                | 2        | TiKV       |               324 |        28204839240 |            1104 |      91039476832 |
| db_1    |     t1     |                | 3        | TiKV       |               319 |        25986274812 |            1091 |      89405367423 |
| db_1    |     t1     |                | 4        | TiKV       |               503 |        41039587625 |            1101 |      90482317797 |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql_statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)