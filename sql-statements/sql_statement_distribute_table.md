---
title: distribute table 使用文档
aliases: ['/docs-cn/dev/sql-statements/sql-statement-distribute-table/','/docs-cn/dev/reference/sql/statements/distribute-table/']
summary: TiDB 中的 distribute table 功能可以解决表中 region 分布不均衡问题。通过重新调整 table 中的 region 的分布，可以让指定 table 下的 region 按照一定的策略进行均衡。重新分配可以指定不同的存储引擎，比如 TIFLASH 和 TIKV。同时也可以指定不同的 raft role，比如 learner，leader，voter。
---

# Distribute Table 使用文档

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

对表A 上的 tikv 上的 leader 重新进行均衡调度
```sql
CREATE TABLE t1 (a INT)；
...
DISTRIBUTE TABLE table_name engine tikv role leader
```
+---------+
| JOB_ID  | 
100
+---------+



显示当前所有的调度任务
```sql
SHOW DISTRIBUTION JOBS;
```

+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
| JOB_ID  |  DB_NAME   | TABLE_NAME | PARTITION_NAMES | ENGINE_TYPE | ROLE_TYPE | STATUS  | CREATE_USER | CREATE_TIME   |
+---------+------------+------------+-----------------+------------+-----------+--------+---------------+---------------+
|    1    |   db_1     |    t1      |                 | TIKV       | LEADER    | RUNNING  | ADMIN       |   20240712    |
|    2    |   db_1     |    t2      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240715      |
|    3    |   db_1     |    t3      |                 | TiKV       | VOTER     | STOPPED  | ADMIN       | 20240713      |
|    4    |   db_1     |    t4      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240713      |
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+


显示当前表 t1 的 region 分布情况
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

### Distribute Table Region


## 注意事项

Distribute Table 语句重新调度 table 下的 region 也会受到 PD 中热点调度器的影响。 同时该任务会在均衡后退出，退出后该表的分布可能会
被被破坏。

## MySQL 兼容性
该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅
