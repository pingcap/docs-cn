---
title: SHOW ANALYZE STATUS
summary: TiDB 数据库中 SHOW ANALYZE STATUS 的使用概况。
---

# SHOW ANALYZE STATUS

`SHOW ANALYZE STATUS` 语句提供 TiDB 正在执行的统计信息收集任务以及有限条历史任务记录。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## 示例

{{< copyable "sql" >}}

```sql
create table t(x int, index idx(x)) partition by hash(x) partition 4;
analyze table t;
show analyze status;
```

```sql
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | State    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          | p1             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p1             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
8 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE_STATUS 表](/information-schema/information-schema-analyze-status.md)