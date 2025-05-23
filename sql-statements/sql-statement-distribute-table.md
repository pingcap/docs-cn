---
title: DISTRIBUTE TABLE
summary: 介绍 TiDB 数据库中 DISTRIBUTE TABLE 的使用概况。
---

# DISTRIBUTE TABLE

`DISTRIBUTE TABLE` 语句用于对指定表的 Region 进行重新打散和调度，以实现表级别的均衡分布。执行该语句可以防止个别 Region 集中在少数 TiFlash 或 TiKV 节点上，从而解决表中 Region 分布不均衡的问题。

## 语法图

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"

```

## 示例

通过 `DISTRIBUTE TABLE` 语句重新调度表中的 Region 时，你可以根据需求指定存储引擎（如 TiFlash 或 TiKV）以及不同的 Raft 角色（如 Leader、Learner、Voter）进行均衡打散操作。

对表 `t1` 在 TiKV 上的 Leader 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 RULE= `leader-scatter` ENGINE = tikv 
+---------+
| JOB_ID  |
100
+---------+
```

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE table t2  RULE = `learner-scatter` Engine=tiflash;
+---------+
| JOB_ID  | 
101
+---------+
```

对分区表 `t5` 的 `p1` 和 `p2` 分区在 TiKV 上的 peer 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t5 PARTITION (p1, p2) RULE= `peer-scatter` ENGINE =tikv;

+---------+
| JOB_ID  |
101
+---------+
```

对分区表 `t3` 的 `p1` 和 `p2` 分区在 TiKV 上的 Leader 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t3 (a INT);
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) ENGINE tikv role leader;
```

```
+---------+
| JOB_ID  |
102
+---------+
```

取消指定的调度任务
```sql
CANCEL DISTRIBUTION JOB 1;
```

## 注意事项

`DISTRIBUTE TABLE` 语句在重新调度表中的 Region 时，可能会受到 PD 热点调度器的影响。调度完成后，随着时间推移，表的 Region 分布可能再次失衡。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)