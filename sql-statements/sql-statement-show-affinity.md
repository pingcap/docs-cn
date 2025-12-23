---
title: SHOW AFFINITY
summary: 介绍 TiDB 数据库中 SHOW AFFINITY 的使用概况。
---

# SHOW AFFINITY <span class="version-mark">从 v8.5.5 开始引入</span>

`SHOW AFFINITY` 语句用于查看开启了 `AFFINITY` 选项的表或分区的亲和性调度信息，以及 PD 当前记录的目标副本分布。

## 语法图

```ebnf+diagram
ShowAffinityStmt ::=
    "SHOW" "AFFINITY" ShowLikeOrWhereOpt
```

`SHOW AFFINITY` 支持使用 `LIKE` 或 `WHERE` 过滤表名。

## 示例

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
CREATE TABLE tp1 (a INT) AFFINITY = 'partition' PARTITION BY HASH(a) PARTITIONS 2;

SHOW AFFINITY;
```

输出结果类似于：

```sql
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| Db_name | Table_name | Partition_name | Leader_store_id | Voter_store_ids  | Status   | Region_count | Affinity_region_count|
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| test    | t1         | NULL           | 1               | 1,2,3            | Stable   |            8 |                    8 |
| test    | tp1        | p0             | 4               | 4,5,6            | Preparing|            4 |                    2 |
| test    | tp1        | p1             | 4               | 4,5,6            | Preparing|            3 |                    2 |
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
```

各列含义如下：

- `LEADER_STORE_ID`、`VOTER_STORE_IDS`：PD 为该表或分区记录的目标 Leader 副本和 Voter 副本所在的 store ID。当亲和性尚未确定时显示为 `NULL`。
- `STATUS`：`Pending` 表示 PD 尚未进行亲和性调度，`Preparing` 表示正在调度 Region 以满足亲和性要求，`Stable` 表示所有 Region 已经达到目标分布。
- `REGION_COUNT`：当前在该亲和性组中的 Region 数量。
- `AFFINITY_REGION_COUNT`：已经满足亲和性副本分布的 Region 数量。若 region_count > Affinity_region_count 时，表示pd调度没有完成；若 region_count = Affinity_region_count 时，表示 pd 的基于亲和性的副本搬迁调度工作完成，也就意味着副本分布已经满足亲和性要求，但是不意味着 merge 操作已经完成。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
