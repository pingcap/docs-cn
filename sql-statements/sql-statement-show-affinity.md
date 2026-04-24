---
title: SHOW AFFINITY
summary: 介绍 TiDB 数据库中 SHOW AFFINITY 的使用概况。
---

# SHOW AFFINITY <span class="version-mark">从 v8.5.5 和 v9.0.0 版本开始引入</span>

`SHOW AFFINITY` 语句用于查看配置了 `AFFINITY` 选项的表的[亲和性](/table-affinity.md)调度信息，以及 PD 当前记录的目标副本分布。

## 语法图

```ebnf+diagram
ShowAffinityStmt ::=
    "SHOW" "AFFINITY" ShowLikeOrWhereOpt
```

`SHOW AFFINITY` 支持使用 `LIKE` 或 `WHERE` 子句过滤表名。

## 示例

以下示例创建两个启用了亲和性调度的表，并查看其调度信息：

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
CREATE TABLE tp1 (a INT) AFFINITY = 'partition' PARTITION BY HASH(a) PARTITIONS 2;

SHOW AFFINITY;
```

输出结果示例如下：

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

- `Leader_store_id`、`Voter_store_ids`：PD 为该表或分区记录的目标 Leader 副本和 Voter 副本所在的 TiKV Store ID。如果亲和性分组尚未确定目标副本位置或 [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) 为 `0`，则显示为 `NULL`。
- `Status`：表示当前亲和性调度的状态。可能的取值如下：
    - `Pending`：PD 尚未对该表或分区进行亲和性调度（比如未确定 Leader 或 Voter 时）。
    - `Preparing`：PD 正在调度 Region 以满足亲和性要求。
    - `Stable`：所有 Region 已达到目标分布。
- `Region_count`：当前在该亲和性组中的 Region 数量。
- `Affinity_region_count`：当前已满足亲和性副本分布要求的 Region 数量。
    - 当 `Affinity_region_count` 小于 `Region_count` 时，表示仍有部分 Region 尚未完成基于亲和性的副本调度。
    - 当 `Affinity_region_count` 等于 `Region_count` 时，表示基于亲和性的 Region 副本迁移调度已完成，也就意味着所有 Region 的分布已经满足亲和性要求，但并不代表相关 Region 的合并操作已完成。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
