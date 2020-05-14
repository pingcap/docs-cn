---
title: CLUSTER_LOG
summary: Learn the `CLUSTER_LOG` cluster log table.
category: reference
---

# CLUSTER_LOG

You can query cluster logs on the `CLUSTER_LOG` cluster log table. By pushing down query conditions to each instance, the impact of the query on cluster performance is less than that of the `grep` command.

To get the logs of the TiDB cluster before v4.0, you need to log in to each instance to summarize logs. This cluster log table in 4.0 provides the global and time-ordered log search result, which makes it easier to track full-link events. For example, by searching logs according to the `region id`, you can query all logs in the life cycle of this Region. Similarly, by searching the full link log through the slow log's `txn id`, you can query the flow and the number of keys scanned by this transaction at each instance.

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_log;
```

```sql
+----------+------------------+------+------+---------+-------+
| Field    | Type             | Null | Key  | Default | Extra |
+----------+------------------+------+------+---------+-------+
| TIME     | varchar(32)      | YES  |      | NULL    |       |
| TYPE     | varchar(64)      | YES  |      | NULL    |       |
| INSTANCE | varchar(64)      | YES  |      | NULL    |       |
| LEVEL    | varchar(8)       | YES  |      | NULL    |       |
| MESSAGE  | var_string(1024) | YES  |      | NULL    |       |
+----------+------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

Field description:

* `TIME`: The time to print the log.
* `TYPE`: The instance type. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: The service address of the instance.
* `LEVEL`: The log level.
* `MESSAGE`: The log content.

> **Note:**
>
> + All fields of the cluster log table are pushed down to the corresponding instance for execution. So to reduce the overhead of using the cluster log table, specify as many conditions as possible. For example, the `select * from cluter_log where instance='tikv-1'` statement only executes the log search on the `tikv-1` instance.
>
> + The `message` field supports the `like` and `regexp` regular expressions, and the corresponding pattern is encoded as `regexp`. Specifying multiple `message` conditions is equivalent to the `pipeline` form of the `grep` command. For example, executing the `select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*'` statement is equivalent to executing `grep 'coprocessor' xxx.log | grep -E '.*slow.*'` on all cluster instances.

The following example shows how to query the execution process of a DDL statement using the `CLUSTER_LOG` table:

{{< copyable "sql" >}}

```sql
select * from information_schema.cluster_log where message like '%ddl%' and message like '%job%58%' and type='tidb' and time > '2020-03-27 15:39:00';
```

```sql
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TIME                    | TYPE | INSTANCE         | LEVEL | MESSAGE                                                                                                                                                                                                                                                                                                                                     |
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4008 | INFO  | [ddl_worker.go:253] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]                                                                       |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4008 | INFO  | [ddl.go:457] ["[ddl] start DDL job"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create table t3 (a int, b int,c int)"]                                                   |
| 2020/03/27 15:39:36.879 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:554] ["[ddl] run DDL job"] [worker="worker 1, tp general"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:0, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"]                                                             |
| 2020/03/27 15:39:36.936 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:739] ["[ddl] wait latest schema version changed"] [worker="worker 1, tp general"] [ver=35] ["take time"=52.165811ms] [job="ID:58, Type:create table, State:done, SchemaState:public, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] |
| 2020/03/27 15:39:36.938 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:359] ["[ddl] finish DDL job"] [worker="worker 1, tp general"] [job="ID:58, Type:create table, State:synced, SchemaState:public, SchemaID:1, TableID:57, RowCount:0, ArgLen:0, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"]                                                      |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:253] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]                                                                       |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4009 | INFO  | [ddl.go:457] ["[ddl] start DDL job"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create table t3 (a int, b int,c int)"]                                                   |
| 2020/03/27 15:39:37.141 | tidb | 172.16.5.40:4008 | INFO  | [ddl.go:489] ["[ddl] DDL job is finished"] [jobID=58]                                                                                                                                                                                                                                                                                       |
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

The above query results show the following process:

1. The request with a DDL JOB ID of `58` is sent to the `172.16.5.40: 4008` TiDB instance.
2. The `172.16.5.40: 4009` TiDB instance processes this DDL request, which indicates that the `172.16.5.40: 4009` instance is the DDL owner at that time.
3. The request with a DDL JOB ID of `58` has been processed.
