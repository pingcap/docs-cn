---
title: SLOW_QUERY
summary: 了解 information_schema 表 `SLOW_QUERY`。
---

# SLOW_QUERY

`SLOW_QUERY` 表中提供了当前节点的慢查询相关的信息，其内容通过解析当前节点的 TiDB 慢查询日志而来，列名和慢日志中的字段名是一一对应。关于如何使用该表调查和改善慢查询，请参考[慢查询日志文档](/identify-slow-queries.md)。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC slow_query;
```

```sql
+---------------------------+---------------------+------+------+---------+-------+
| Field                     | Type                | Null | Key  | Default | Extra |
+---------------------------+---------------------+------+------+---------+-------+
| Time                      | timestamp(6)        | YES  |      | NULL    |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |      | NULL    |       |
| User                      | varchar(64)         | YES  |      | NULL    |       |
| Host                      | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                   | bigint(20) unsigned | YES  |      | NULL    |       |
| Query_time                | double              | YES  |      | NULL    |       |
| Parse_time                | double              | YES  |      | NULL    |       |
| Compile_time              | double              | YES  |      | NULL    |       |
| Rewrite_time              | double              | YES  |      | NULL    |       |
| Preproc_subqueries        | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time   | double              | YES  |      | NULL    |       |
| Optimize_time             | double              | YES  |      | NULL    |       |
| Wait_TS                   | double              | YES  |      | NULL    |       |
| Prewrite_time             | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time | double              | YES  |      | NULL    |       |
| Commit_time               | double              | YES  |      | NULL    |       |
| Get_commit_ts_time        | double              | YES  |      | NULL    |       |
| Commit_backoff_time       | double              | YES  |      | NULL    |       |
| Backoff_types             | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time         | double              | YES  |      | NULL    |       |
| Local_latch_wait_time     | double              | YES  |      | NULL    |       |
| Write_keys                | bigint(22)          | YES  |      | NULL    |       |
| Write_size                | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region           | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                 | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                  | double              | YES  |      | NULL    |       |
| Process_time              | double              | YES  |      | NULL    |       |
| Wait_time                 | double              | YES  |      | NULL    |       |
| Backoff_time              | double              | YES  |      | NULL    |       |
| LockKeys_time             | double              | YES  |      | NULL    |       |
| Request_count             | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys              | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                        | varchar(64)         | YES  |      | NULL    |       |
| Index_names               | varchar(100)        | YES  |      | NULL    |       |
| Is_internal               | tinyint(1)          | YES  |      | NULL    |       |
| Digest                    | varchar(64)         | YES  |      | NULL    |       |
| Stats                     | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg              | double              | YES  |      | NULL    |       |
| Cop_proc_p90              | double              | YES  |      | NULL    |       |
| Cop_proc_max              | double              | YES  |      | NULL    |       |
| Cop_proc_addr             | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg              | double              | YES  |      | NULL    |       |
| Cop_wait_p90              | double              | YES  |      | NULL    |       |
| Cop_wait_max              | double              | YES  |      | NULL    |       |
| Cop_wait_addr             | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                   | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                  | bigint(20)          | YES  |      | NULL    |       |
| Succ                      | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache           | tinyint(1)          | YES  |      | NULL    |       |
| Plan                      | longblob            | YES  |      | NULL    |       |
| Plan_digest               | varchar(128)        | YES  |      | NULL    |       |
| Prev_stmt                 | longblob            | YES  |      | NULL    |       |
| Query                     | longblob            | YES  |      | NULL    |       |
+---------------------------+---------------------+------+------+---------+-------+
54 rows in set (0.00 sec)
```

## CLUSTER_SLOW_QUERY table

`CLUSTER_SLOW_QUERY` 表中提供了集群所有节点的慢查询相关的信息，其内容通过解析 TiDB 慢查询日志而来，该表使用上和 `SLOW_QUERY` 表一样。`CLUSTER_SLOW_QUERY` 表结构上比 `SLOW_QUERY` 多一列 `INSTANCE`，表示该行慢查询信息来自的 TiDB 节点地址。关于如何使用该表调查和改善慢查询，请参考[慢查询日志文档](/identify-slow-queries.md)。

{{< copyable "sql" >}}

```sql
desc cluster_slow_query;
```

```sql
+---------------------------+---------------------+------+------+---------+-------+
| Field                     | Type                | Null | Key  | Default | Extra |
+---------------------------+---------------------+------+------+---------+-------+
| INSTANCE                  | varchar(64)         | YES  |      | NULL    |       |
| Time                      | timestamp(6)        | YES  |      | NULL    |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |      | NULL    |       |
| User                      | varchar(64)         | YES  |      | NULL    |       |
| Host                      | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                   | bigint(20) unsigned | YES  |      | NULL    |       |
| Query_time                | double              | YES  |      | NULL    |       |
| Parse_time                | double              | YES  |      | NULL    |       |
| Compile_time              | double              | YES  |      | NULL    |       |
| Rewrite_time              | double              | YES  |      | NULL    |       |
| Preproc_subqueries        | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time   | double              | YES  |      | NULL    |       |
| Optimize_time             | double              | YES  |      | NULL    |       |
| Wait_TS                   | double              | YES  |      | NULL    |       |
| Prewrite_time             | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time | double              | YES  |      | NULL    |       |
| Commit_time               | double              | YES  |      | NULL    |       |
| Get_commit_ts_time        | double              | YES  |      | NULL    |       |
| Commit_backoff_time       | double              | YES  |      | NULL    |       |
| Backoff_types             | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time         | double              | YES  |      | NULL    |       |
| Local_latch_wait_time     | double              | YES  |      | NULL    |       |
| Write_keys                | bigint(22)          | YES  |      | NULL    |       |
| Write_size                | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region           | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                 | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                  | double              | YES  |      | NULL    |       |
| Process_time              | double              | YES  |      | NULL    |       |
| Wait_time                 | double              | YES  |      | NULL    |       |
| Backoff_time              | double              | YES  |      | NULL    |       |
| LockKeys_time             | double              | YES  |      | NULL    |       |
| Request_count             | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys              | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                        | varchar(64)         | YES  |      | NULL    |       |
| Index_names               | varchar(100)        | YES  |      | NULL    |       |
| Is_internal               | tinyint(1)          | YES  |      | NULL    |       |
| Digest                    | varchar(64)         | YES  |      | NULL    |       |
| Stats                     | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg              | double              | YES  |      | NULL    |       |
| Cop_proc_p90              | double              | YES  |      | NULL    |       |
| Cop_proc_max              | double              | YES  |      | NULL    |       |
| Cop_proc_addr             | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg              | double              | YES  |      | NULL    |       |
| Cop_wait_p90              | double              | YES  |      | NULL    |       |
| Cop_wait_max              | double              | YES  |      | NULL    |       |
| Cop_wait_addr             | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                   | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                  | bigint(20)          | YES  |      | NULL    |       |
| Succ                      | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache           | tinyint(1)          | YES  |      | NULL    |       |
| Plan                      | longblob            | YES  |      | NULL    |       |
| Plan_digest               | varchar(128)        | YES  |      | NULL    |       |
| Prev_stmt                 | longblob            | YES  |      | NULL    |       |
| Query                     | longblob            | YES  |      | NULL    |       |
+---------------------------+---------------------+------+------+---------+-------+
55 rows in set (0.00 sec)
```

查询集群系统表时，TiDB 也会将相关计算下推给其他节点执行，而不是把所有节点的数据都取回来，可以查看执行计划，如下：

{{< copyable "sql" >}}

```sql
desc SELECT count(*) FROM cluster_slow_query WHERE user = 'u1';
```

```sql
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                       | estRows  | task      | access object            | operator info                                        |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_20             | 1.00     | root      |                          | funcs:count(Column#53)->Column#51                    |
| └─TableReader_21         | 1.00     | root      |                          | data:StreamAgg_9                                     |
|   └─StreamAgg_9          | 1.00     | cop[tidb] |                          | funcs:count(1)->Column#53                            |
|     └─Selection_19       | 10.00    | cop[tidb] |                          | eq(information_schema.cluster_slow_query.user, "u1") |
|       └─TableFullScan_18 | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
```

上面执行计划表示，会将 `user = u1` 条件下推给其他的 (`cop`) TiDB 节点执行，也会把聚合算子（即图中的 `StreamAgg` 算子）下推。

目前由于没有对系统表收集统计信息，所以有时会导致某些聚合算子不能下推，导致执行较慢，用户可以通过手动指定聚合下推的 SQL HINT 来将聚合算子下推，示例如下：

{{< copyable "sql" >}}

```sql
SELECT /*+ AGG_TO_COP() */ count(*) FROM cluster_slow_query GROUP BY user;
```
