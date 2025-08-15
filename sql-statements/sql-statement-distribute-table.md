---
title: DISTRIBUTE TABLE
summary: 介绍 TiDB 数据库中 DISTRIBUTE TABLE 的使用概况。
---

# DISTRIBUTE TABLE

<span class="version-mark">从 v9.0.0 开始引入</span>

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

`DISTRIBUTE TABLE` 语句用于对指定表的 Region 进行重新打散和调度，以实现表级别的均衡分布。执行该语句可以防止个别 Region 集中在少数 TiFlash 或 TiKV 节点上，从而解决表中 Region 分布不均衡的问题。

## 语法图

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier "TIMEOUT" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"
```

## 参数说明

通过 `DISTRIBUTE TABLE` 语句重新调度表中的 Region 时，你可以根据需求指定存储引擎（如 TiFlash 或 TiKV）以及不同的 Raft 角色（如 Leader、Learner、Voter）进行均衡。

- `RULE`：指定针对哪个 Raft 角色所在的 Region 进行均衡调度，可选值为 `"leader-scatter"`、`"peer-scatter"` 和 `"learner-scatter"`。
- `ENGINE`：指定存储引擎，可选值为 `"tikv"` 和 `"tiflash"`。
- `TIMEOUT`：指定打散操作的超时限制。如果 PD 未在该时间内进行打散，打散任务将会自动退出。当未指定该参数时，默认值为 `"30m"`。

## 示例

对表 `t1` 在 TiKV 上的 Leader 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 RULE = "leader-scatter" ENGINE = "tikv" TIMEOUT = "1h";
```

```
+--------+
| JOB_ID |
+--------+
|    100 |
+--------+
```

对表 `t2` 在 TiFlash 上的 Learner 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 RULE = "learner-scatter" ENGINE = "tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    101 |
+--------+
```

对分区表 `t3` 的 `p1` 和 `p2` 分区在 TiKV 上的 Peer 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t3 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) RULE = "peer-scatter" ENGINE = "tikv";
```

```
+--------+
| JOB_ID |
+--------+
|    102 |
+--------+
```

对分区表 `t4` 的 `p1` 和 `p2` 分区在 TiFlash 上的 Learner 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t4 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t4 PARTITION (p1, p2) RULE = "learner-scatter" ENGINE="tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    103 |
+--------+
```

## 注意事项

`DISTRIBUTE TABLE` 语句在重新调度表中的 Region 时，可能会受到 PD 热点调度器的影响。调度完成后，随着时间推移，表的 Region 分布可能再次失衡。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)