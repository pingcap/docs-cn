---
title: DISTRIBUTE TABLE
summary: 介绍 TiDB 数据库中 DISTRIBUTE TABLE 的使用概况。
---

# DISTRIBUTE TABLE 使用文档
`DISTRIBUTE TABLE` 语句用于对指定表的 Region 进行重新打散和调度，以实现表维度的均衡分布。执行该语句可以防止个别 Region 集中在少数 TiFlash 或 TiKV 节点上，从而解决表中 Region 分布不均衡的问题。

## 语法图

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE"  "TABLE" TableName PartitionNameList?  EngineOption? RoleOption?

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"

EngineOption ::=
    "ENGINE" Expression

RoleOption ::=
    "Role" Expression

```

## 示例
通过 `DISTRIBUTE TABLE` 语句重新调度表中的 Region 时，你可以根据需求指定存储引擎（如 TiFlash 或 TiKV）以及不同的 Raft 角色（如 learner、leader、voter） 进行打散均衡操作。

对表 `t1` 在 TiKV 上的 leader 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE table_name engine tikv role leader
```
+---------+
| JOB_ID  | 
100
+---------+

对表 `t2` 在 TiFlash 上的 learner 所在的 Region 重新进行均衡调度：
```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 ENGINE tiflash role learner;
```
+---------+
| JOB_ID  | 
101
+---------+

对分区表 `t5` 的 `p1` 和 `p2` 分区在 TiKV 上的 leader 所在的 Region 重新进行均衡调度：

```sql
CREATE TABLE t5 (a INT);
...
DISTRIBUTE TABLE t5 PARTITION (p1, p2) ENGINE tikv role leader;
```
+---------+
| JOB_ID  | 
102
+---------+


显示当前所有的调度任务：
```sql
SHOW DISTRIBUTION JOBS;
```

+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
| JOB_ID  |  DB_NAME   | TABLE_NAME | PARTITION_NAMES | ENGINE_TYPE | ROLE_TYPE | STATUS  | CREATE_USER | CREATE_TIME   |
+---------+------------+------------+-----------------+------------+-----------+--------+---------------+---------------+
|    1    |   db_1     |    t1      |                 | TIKV       | LEADER    | RUNNING  | ADMIN       | 20240712      |
|    2    |   db_1     |    t2      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240715      |
|    3    |   db_1     |    t3      |                 | TiKV       | VOTER     | STOPPED  | ADMIN       | 20240713      |
|    4    |   db_1     |    t4      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240713      |
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+


显示当前表 `t1` 的 region 分布情况:
```sql
SHOW TABLE DISTRIBUTION t1;
```

+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| DB_NAME | TABLE_NAME | PARTITION_NAME | STORE_ID | STORE_TYPE | REGION_LEADER_NUM | REGION_LEADER_BYTE | REGION_PEER_NUM | REGION_PEER_BYTE |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| db_1    |     t1     |                | 1        | TiKV       |               315 |        24057934521 |            1087 |      86938746542 |
| db_1    |     t1     |                | 2        | TiKV       |               324 |        28204839240 |            1104 |      91039476832 |
| db_1    |     t1     |                | 3        | TiKV       |               319 |        25986274812 |            1091 |      89405367423 |
| db_1    |     t1     |                | 4        | TiKV       |               503 |        41039587625 |            1101 |      90482317797 |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+


## 注意事项

`DISTRIBUTE TABLE` 语句在重新调度表中的 Region 时，可能会受到 PD 热点调度器的影响。调度完成后，随着时间推移，表的 Region 分布可能再次失衡。

## MySQL 兼容性
该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅
