---
title: Identify Slow Queries
summary: Use the slow query log to identify problematic SQL statements.
aliases: ['/docs/dev/identify-slow-queries/','/docs/dev/how-to/maintain/identify-abnormal-queries/identify-slow-queries/','/docs/dev/how-to/maintain/identify-slow-queries']
---

# Identify Slow Queries

To help users identify slow queries, analyze and improve the performance of SQL execution, TiDB outputs the statements whose execution time exceeds [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) (The default value is 300 milliseconds) to [slow-query-file](/tidb-configuration-file.md#slow-query-file) (The default value is "tidb-slow.log").

TiDB enables the slow query log by default. You can enable or disable the feature by modifying the system variable [`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log).

## Usage example

```sql
# Time: 2019-08-14T09:26:59.487776265+08:00
# Txn_start_ts: 410450924122144769
# User@Host: root[root] @ localhost [127.0.0.1]
# Conn_ID: 3086
# Exec_retry_time: 5.1 Exec_retry_count: 3
# Query_time: 1.527627037
# Parse_time: 0.000054933
# Compile_time: 0.000129729
# Rewrite_time: 0.000000003 Preproc_subqueries: 2 Preproc_subqueries_time: 0.000000002
# Optimize_time: 0.00000001
# Wait_TS: 0.00001078
# Process_time: 0.07 Request_count: 1 Total_keys: 131073 Process_keys: 131072 Prewrite_time: 0.335415029 Commit_time: 0.032175429 Get_commit_ts_time: 0.000177098 Local_latch_wait_time: 0.106869448 Write_keys: 131072 Write_size: 3538944 Prewrite_region: 1
# DB: test
# Is_internal: false
# Digest: 50a2e32d2abbd6c1764b1b7f2058d428ef2712b029282b776beb9506a365c0f1
# Stats: t:pseudo
# Num_cop_tasks: 1
# Cop_proc_avg: 0.07 Cop_proc_p90: 0.07 Cop_proc_max: 0.07 Cop_proc_addr: 172.16.5.87:20171
# Cop_wait_avg: 0 Cop_wait_p90: 0 Cop_wait_max: 0 Cop_wait_addr: 172.16.5.87:20171
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
# Cop_backoff_rpcTiKV_total_times: 200 Cop_backoff_rpcTiKV_total_time: 0.2 Cop_backoff_rpcTiKV_max_time: 0.2 Cop_backoff_rpcTiKV_max_addr: 127.0.0.1 Cop_backoff_rpcTiKV_avg_time: 0.2 Cop_backoff_rpcTiKV_p90_time: 0.2
# Mem_max: 525211
# Disk_max: 65536
# Prepared: false
# Plan_from_cache: false
# Succ: true
# Plan: tidb_decode_plan('ZJAwCTMyXzcJMAkyMAlkYXRhOlRhYmxlU2Nhbl82CjEJMTBfNgkxAR0AdAEY1Dp0LCByYW5nZTpbLWluZiwraW5mXSwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCg==')
use test;
insert into t select * from t;
```

## Fields description

> **Note:**
>
> The unit of all the following time fields in the slow query log is **"second"**.

Slow query basics:

* `Time`: The print time of log.
* `Query_time`: The execution time of a statement.
* `Parse_time`: The parsing time for the statement.
* `Compile_time`: The duration of the query optimization.
* `Optimize_time`: The time consumed for optimizing the execution plan.
* `Wait_TS`: The waiting time of the statement to get transaction timestamps.
* `Query`: A SQL statement. `Query` is not printed in the slow log, but the corresponding field is called `Query` after the slow log is mapped to the memory table.
* `Digest`: The fingerprint of the SQL statement.
* `Txn_start_ts`: The start timestamp and the unique ID of a transaction. You can use this value to search for the transaction-related logs.
* `Is_internal`: Whether a SQL statement is TiDB internal. `true` indicates that a SQL statement is executed internally in TiDB and `false` indicates that a SQL statement is executed by the user.
* `Index_names`: The index names used by the statement.
* `Stats`: The health state of the involved tables. `pseudo` indicates that the state is unhealthy.
* `Succ`: Whether a statement is executed successfully.
* `Backoff_time`: The waiting time before retry when a statement encounters errors that require a retry. The common errors as such include: `lock occurs`, `Region split`, and `tikv server is busy`.
* `Plan`: The execution plan of a statement. Execute the `SELECT tidb_decode_plan('xxx...')` statement to parse the specific execution plan.
* `Binary_plan`: The execution plan of a binary-encoded statement. Execute the `SELECT tidb_decode_binary_plan('xxx...')` statement to parse the specific execution plan. The `Plan` and `Binary_plan` fields carry the same information. However, the format of execution plans parsed from the two fields are different.
* `Prepared`: Whether this statement is a `Prepare` or `Execute` request or not.
* `Plan_from_cache`: Whether this statement hits the execution plan cache.
* `Plan_from_binding`: Whether this statement uses the bound execution plans.
* `Has_more_results`: Whether this statement has more results to be fetched by users.
* `Rewrite_time`: The time consumed for rewriting the query of this statement.
* `Preproc_subqueries`: The number of subqueries (in the statement) that are executed in advance. For example, the `where id in (select if from t)` subquery might be executed in advance.
* `Preproc_subqueries_time`: The time consumed for executing the subquery of this statement in advance.
* `Exec_retry_count`: The retry times of this statement. This field is usually for pessimistic transactions in which the statement is retried when the lock is failed.
* `Exec_retry_time`: The execution retry duration of this statement. For example, if a statement has been executed three times in total (failed for the first two times), `Exec_retry_time` means the total duration of the first two executions. The duration of the last execution is `Query_time` minus `Exec_retry_time`.
* `KV_total`: The time spent on all the RPC requests on TiKV or TiFlash by this statement.
* `PD_total`: The time spent on all the RPC requests on PD by this statement.
* `Backoff_total`: The time spent on all the backoff during the execution of this statement.
* `Write_sql_response_total`: The time consumed for sending the results back to the client by this statement.
* `Result_rows`: The row count of the query results.
* `IsExplicitTxn`: Whether this statement is in an explicit transaction. If the value is `false`, the transaction is `autocommit=1` and the statement is automatically committed after execution.
* `Warnings`: The JSON-formatted warnings that are generated during the execution of this statement. These warnings are generally consistent with the output of the [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) statement, but might include extra warnings that provide more diagnostic information. These extra warnings are marked as `IsExtra: true`.

The following fields are related to transaction execution:

* `Prewrite_time`: The duration of the first phase (prewrite) of the two-phase transaction commit.
* `Commit_time`: The duration of the second phase (commit) of the two-phase transaction commit.
* `Get_commit_ts_time`: The time spent on getting `commit_ts` during the second phase (commit) of the two-phase transaction commit.
* `Local_latch_wait_time`: The time that TiDB spends on waiting for the lock before the second phase (commit) of the two-phase transaction commit.
* `Write_keys`: The count of keys that the transaction writes to the Write CF in TiKV.
* `Write_size`: The total size of the keys or values to be written when the transaction commits.
* `Prewrite_region`: The number of TiKV Regions involved in the first phase (prewrite) of the two-phase transaction commit. Each Region triggers a remote procedure call.

Memory usage fields:

* `Mem_max`: The maximum memory space used during the execution period of a SQL statement (the unit is byte).

Hard disk fields:

* `Disk_max`: The maximum disk space used during the execution period of a SQL statement (the unit is byte).

User fields:

* `User`: The name of the user who executes this statement.
* `Host`: The host name of this statement.
* `Conn_ID`: The Connection ID (session ID). For example, you can use the keyword `con:3` to search for the log whose session ID is `3`.
* `DB`: The current database.

TiKV Coprocessor Task fields:

* `Request_count`: The number of Coprocessor requests that a statement sends.
* `Total_keys`: The number of keys that Coprocessor has scanned.
* `Process_time`: The total processing time of a SQL statement in TiKV. Because data is sent to TiKV concurrently, this value might exceed `Query_time`.
* `Wait_time`: The total waiting time of a statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests increases.
* `Process_keys`: The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that many old versions exist.
* `Num_cop_tasks`: The number of Coprocessor tasks sent by this statement.
* `Cop_proc_avg`: The average execution time of cop-tasks, including some waiting time that cannot be counted, such as the mutex in RocksDB.
* `Cop_proc_p90`: The P90 execution time of cop-tasks.
* `Cop_proc_max`: The maximum execution time of cop-tasks.
* `Cop_proc_addr`: The address of the cop-task with the longest execution time.
* `Cop_wait_avg`: The average waiting time of cop-tasks, including the time of request queueing and getting snapshots.
* `Cop_wait_p90`: The P90 waiting time of cop-tasks.
* `Cop_wait_max`: The maximum waiting time of cop-tasks.
* `Cop_wait_addr`: The address of the cop-task whose waiting time is the longest.
* `Cop_backoff_{backoff-type}_total_times`: The total times of backoff caused by an error.
* `Cop_backoff_{backoff-type}_total_time`: The total time of backoff caused by an error.
* `Cop_backoff_{backoff-type}_max_time`: The longest time of backoff caused by an error.
* `Cop_backoff_{backoff-type}_max_addr`: The address of the cop-task that has the longest backoff time caused by an error.
* `Cop_backoff_{backoff-type}_avg_time`: The average time of backoff caused by an error.
* `Cop_backoff_{backoff-type}_p90_time`: The P90 percentile backoff time caused by an error.

## Related system variables

* [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold): Sets the threshold for the slow log. The SQL statement whose execution time exceeds this threshold is recorded in the slow log. The default value is 300 (ms).
* [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len): Sets the maximum length of the SQL statement recorded in the slow log. The default value is 4096 (byte).
* [tidb_redact_log](/system-variables.md#tidb_redact_log): Determines whether to desensitize user data using `?` in the SQL statement recorded in the slow log. The default value is `0`, which means to disable the feature.
* [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info): Determines whether to record the physical execution information of each operator in the execution plan. The default value is `1`. This feature impacts the performance by approximately 3%. After enabling this feature, you can view the `Plan` information as follows:

    ```sql
    > select tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMgk1BWM2zwAAMRnIADcVyAAxHcEQNQlOL0EBBPBbCjMJMTNfMTYJMQkzMTI4MS44NTc4MTk5MDUyMTcJdGFibGU6dCwgaW5kZXg6aWR4KGEpLCByYW5nZTpbLWluZiw1MDAwMCksIGtlZXAgb3JkZXI6ZmFsc2UJMjUBrgnQVnsA');
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMg |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |     id                    task    estRows               operator info                                                  actRows    execution info                                                                  memory       disk                              |
    |     StreamAgg_17          root    1                     funcs:count(Column#7)->Column#5                                1          time:10.931505ms, loops:2                                                       372 Bytes    N/A                               |
    |     └─IndexReader_18      root    1                     index:StreamAgg_9                                              1          time:10.927685ms, loops:2, rpc num: 1, rpc time:10.884355ms, proc keys:25007    206 Bytes    N/A                               |
    |       └─StreamAgg_9       cop     1                     funcs:count(1)->Column#7                                       1          time:11ms, loops:25                                                             N/A          N/A                               |
    |         └─IndexScan_16    cop     31281.857819905217    table:t, index:idx(a), range:[-inf,50000), keep order:false    25007      time:11ms, loops:25                                                             N/A          N/A                               |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    ```

If you are conducting a performance test, you can disable the feature of automatically collecting the execution information of operators:

{{< copyable "sql" >}}

```sql
set @@tidb_enable_collect_execution_info=0;
```

The returned result of the `Plan` field has roughly the same format with that of `EXPLAIN` or `EXPLAIN ANALYZE`. For more details of the execution plan, see [`EXPLAIN`](/sql-statements/sql-statement-explain.md) or [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md).

For more information, see [TiDB specific variables and syntax](/system-variables.md).

## Memory mapping in slow log

You can query the content of the slow query log by querying the `INFORMATION_SCHEMA.SLOW_QUERY` table. Each column name in the table corresponds to one field name in the slow log. For table structure, see the introduction to the `SLOW_QUERY` table in [Information Schema](/information-schema/information-schema-slow-query.md).

> **Note:**
>
> Every time you query the `SLOW_QUERY` table, TiDB reads and parses the current slow query log.

For TiDB 4.0, `SLOW_QUERY` supports querying the slow log of any period of time, including the rotated slow log file. You need to specify the `TIME` range to locate the slow log files that need to be parsed. If you don't specify the `TIME` range, TiDB only parses the current slow log file. For example:

* If you don't specify the time range, TiDB only parses the slow query data that TiDB is writing to the slow log file:

    {{< copyable "sql" >}}

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query;
    ```

    ```
    +----------+----------------------------+----------------------------+
    | count(*) | min(time)                  | max(time)                  |
    +----------+----------------------------+----------------------------+
    | 122492   | 2020-03-11 23:35:20.908574 | 2020-03-25 19:16:38.229035 |
    +----------+----------------------------+----------------------------+
    ```

* If you specify the time range, for example, from `2020-03-10 00:00:00` to `2020-03-11 00:00:00`, TiDB first locates the slow log files of the specified time range, and then parses the slow query information:

    {{< copyable "sql" >}}

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query
    where time > '2020-03-10 00:00:00'
      and time < '2020-03-11 00:00:00';
    ```

    ```
    +----------+----------------------------+----------------------------+
    | count(*) | min(time)                  | max(time)                  |
    +----------+----------------------------+----------------------------+
    | 2618049  | 2020-03-10 00:00:00.427138 | 2020-03-10 23:00:22.716728 |
    +----------+----------------------------+----------------------------+
    ```

> **Note:**
>
> If the slow log files of the specified time range are removed, or there is no slow query, the query returns NULL.

TiDB 4.0 adds the [`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table) system table to query the slow query information of all TiDB nodes. The table schema of the `CLUSTER_SLOW_QUERY` table differs from that of the `SLOW_QUERY` table in that an `INSTANCE` column is added to `CLUSTER_SLOW_QUERY`. The `INSTANCE` column represents the TiDB node address of the row information on the slow query. You can use `CLUSTER_SLOW_QUERY` the way you do with [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md).

When you query the `CLUSTER_SLOW_QUERY` table, TiDB pushes the computation and the judgment down to other nodes, instead of retrieving all slow query information from other nodes and executing the operations on one TiDB node.

## `SLOW_QUERY` / `CLUSTER_SLOW_QUERY` usage examples

### Top-N slow queries

Query the Top 2 slow queries of users. `Is_internal=false` means excluding slow queries inside TiDB and only querying slow queries of users.

{{< copyable "sql" >}}

```sql
select query_time, query
from information_schema.slow_query
where is_internal = false
order by query_time desc
limit 2;
```

Output example:

```
+--------------+------------------------------------------------------------------+
| query_time   | query                                                            |
+--------------+------------------------------------------------------------------+
| 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
|  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
+--------------+------------------------------------------------------------------+
```

### Query the Top-N slow queries of the `test` user

In the following example, the slow queries executed by the `test` user are queried, and the first two results are displayed in reverse order of execution time.

{{< copyable "sql" >}}

```sql
select query_time, query, user
from information_schema.slow_query
where is_internal = false
  and user = "test"
order by query_time desc
limit 2;
```

Output example:

```
+-------------+------------------------------------------------------------------+----------------+
| Query_time  | query                                                            | user           |
+-------------+------------------------------------------------------------------+----------------+
| 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test           |
+-------------+------------------------------------------------------------------+----------------+
```

### Query similar slow queries with the same SQL fingerprints

After querying the Top-N SQL statements, continue to query similar slow queries using the same fingerprints.

1. Acquire Top-N slow queries and the corresponding SQL fingerprints.

    {{< copyable "sql" >}}

    ```sql
    select query_time, query, digest
    from information_schema.slow_query
    where is_internal = false
    order by query_time desc
    limit 1;
    ```

    Output example:

    ```
    +-------------+-----------------------------+------------------------------------------------------------------+
    | query_time  | query                       | digest                                                           |
    +-------------+-----------------------------+------------------------------------------------------------------+
    | 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
    +-------------+-----------------------------+------------------------------------------------------------------+
    ```

2. Query similar slow queries with the fingerprints.

    {{< copyable "sql" >}}

    ```sql
    select query, query_time
    from information_schema.slow_query
    where digest = "4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
    ```

    Output example:

    ```
    +-----------------------------+-------------+
    | query                       | query_time  |
    +-----------------------------+-------------+
    | select * from t1 where a=1; | 0.302558006 |
    | select * from t1 where a=2; | 0.401313532 |
    +-----------------------------+-------------+
    ```

## Query slow queries with pseudo `stats`

{{< copyable "sql" >}}

```sql
select query, query_time, stats
from information_schema.slow_query
where is_internal = false
  and stats like '%pseudo%';
```

Output example:

```
+-----------------------------+-------------+---------------------------------+
| query                       | query_time  | stats                           |
+-----------------------------+-------------+---------------------------------+
| select * from t1 where a=1; | 0.302558006 | t1:pseudo                       |
| select * from t1 where a=2; | 0.401313532 | t1:pseudo                       |
| select * from t1 where a>2; | 0.602011247 | t1:pseudo                       |
| select * from t1 where a>3; | 0.50077719  | t1:pseudo                       |
| select * from t1 join t2;   | 0.931260518 | t1:407872303825682445,t2:pseudo |
+-----------------------------+-------------+---------------------------------+
```

### Query slow queries whose execution plan is changed

When the execution plan of SQL statements of the same category is changed, the execution slows down, because the statistics is outdated, or the statistics is not accurate enough to reflect the real data distribution. You can use the following SQL statement to query SQL statements with different execution plans.

{{< copyable "sql" >}}

```sql
select count(distinct plan_digest) as count,
       digest,
       min(query)
from cluster_slow_query
group by digest
having count > 1
limit 3\G
```

Output example:

```
***************************[ 1. row ]***************************
count      | 2
digest     | 17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94
min(query) | SELECT DISTINCT c FROM sbtest25 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (291638, 291737)];
***************************[ 2. row ]***************************
count      | 2
digest     | 9337865f3e2ee71c1c2e740e773b6dd85f23ad00f8fa1f11a795e62e15fc9b23
min(query) | SELECT DISTINCT c FROM sbtest22 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (215420, 215519)];
***************************[ 3. row ]***************************
count      | 2
digest     | db705c89ca2dfc1d39d10e0f30f285cbbadec7e24da4f15af461b148d8ffb020
min(query) | SELECT DISTINCT c FROM sbtest11 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (303359, 303458)];
```

Then you can query the different plans using the SQL fingerprint in the query result above:

{{< copyable "sql" >}}

```sql
select min(plan),
       plan_digest
from cluster_slow_query
where digest='17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94'
group by plan_digest\G
```

Output example:

```
*************************** 1. row ***************************
  min(plan):    Sort_6                  root    100.00131380758702      sbtest.sbtest25.c:asc
        └─HashAgg_10            root    100.00131380758702      group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
          └─TableReader_15      root    100.00131380758702      data:TableRangeScan_14
            └─TableScan_14      cop     100.00131380758702      table:sbtest25, range:[502791,502890], keep order:false
plan_digest: 6afbbd21f60ca6c6fdf3d3cd94f7c7a49dd93c00fcf8774646da492e50e204ee
*************************** 2. row ***************************
  min(plan):    Sort_6                  root    1                       sbtest.sbtest25.c:asc
        └─HashAgg_12            root    1                       group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
          └─TableReader_13      root    1                       data:HashAgg_8
            └─HashAgg_8         cop     1                       group by:sbtest.sbtest25.c,
              └─TableScan_11    cop     1.2440069558121831      table:sbtest25, range:[472745,472844], keep order:false
```

### Query the number of slow queries for each TiDB node in a cluster

{{< copyable "sql" >}}

```sql
select instance, count(*) from information_schema.cluster_slow_query where time >= "2020-03-06 00:00:00" and time < now() group by instance;
```

Output example:

```
+---------------+----------+
| instance      | count(*) |
+---------------+----------+
| 0.0.0.0:10081 | 124      |
| 0.0.0.0:10080 | 119771   |
+---------------+----------+
```

### Query slow logs occurring only in abnormal time period

If you find problems such as decreased QPS or increased latency for the time period from `2020-03-10 13:24:00` to `2020-03-10 13:27:00`, the reason might be that a large query crops up. Run the following SQL statement to query slow logs that occur only in abnormal time period. The time range from `2020-03-10 13:20:00` to `2020-03-10 13:23:00` refers to the normal time period.

{{< copyable "sql" >}}

```sql
SELECT * FROM
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ count(*),
         min(time),
         sum(query_time) AS sum_query_time,
         sum(Process_time) AS sum_process_time,
         sum(Wait_time) AS sum_wait_time,
         sum(Commit_time),
         sum(Request_count),
         sum(process_keys),
         sum(Write_keys),
         max(Cop_proc_max),
         min(query),min(prev_stmt),
         digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:24:00'
            AND time < '2020-03-10 13:27:00'
            AND Is_internal = false
    GROUP BY  digest) AS t1
WHERE t1.digest NOT IN
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:20:00'
            AND time < '2020-03-10 13:23:00'
    GROUP BY  digest)
ORDER BY  t1.sum_query_time DESC limit 10\G
```

Output example:

```
***************************[ 1. row ]***************************
count(*)           | 200
min(time)          | 2020-03-10 13:24:27.216186
sum_query_time     | 50.114126194
sum_process_time   | 268.351
sum_wait_time      | 8.476
sum(Commit_time)   | 1.044304306
sum(Request_count) | 6077
sum(process_keys)  | 202871950
sum(Write_keys)    | 319500
max(Cop_proc_max)  | 0.263
min(query)         | delete from test.tcs2 limit 5000;
min(prev_stmt)     |
digest             | 24bd6d8a9b238086c9b8c3d240ad4ef32f79ce94cf5a468c0b8fe1eb5f8d03df
```

### Parse other TiDB slow log files

TiDB uses the session variable `tidb_slow_query_file` to control the files to be read and parsed when querying `INFORMATION_SCHEMA.SLOW_QUERY`. You can query the content of other slow query log files by modifying the value of the session variable.

{{< copyable "sql" >}}

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

### Parse TiDB slow logs with `pt-query-digest`

Use `pt-query-digest` to parse TiDB slow logs.

> **Note:**
>
> It is recommended to use `pt-query-digest` 3.0.13 or later versions.

For example:

{{< copyable "shell-regular" >}}

```shell
pt-query-digest --report tidb-slow.log
```

Output example:

```
# 320ms user time, 20ms system time, 27.00M rss, 221.32M vsz
# Current date: Mon Mar 18 13:18:51 2019
# Hostname: localhost.localdomain
# Files: tidb-slow.log
# Overall: 1.02k total, 21 unique, 0 QPS, 0x concurrency _________________
# Time range: 2019-03-18-12:22:16 to 2019-03-18-13:08:52
# Attribute          total     min     max     avg     95%  stddev  median
# ============     ======= ======= ======= ======= ======= ======= =======
# Exec time           218s    10ms     13s   213ms    30ms      1s    19ms
# Query size       175.37k       9   2.01k  175.89  158.58  122.36  158.58
# Commit time         46ms     2ms     7ms     3ms     7ms     1ms     3ms
# Conn ID               71       1      16    8.88   15.25    4.06    9.83
# Process keys     581.87k       2 103.15k  596.43  400.73   3.91k  400.73
# Process time         31s     1ms     10s    32ms    19ms   334ms    16ms
# Request coun       1.97k       1      10    2.02    1.96    0.33    1.96
# Total keys       636.43k       2 103.16k  652.35  793.42   3.97k  400.73
# Txn start ts     374.38E       0  16.00E 375.48P   1.25P  89.05T   1.25P
# Wait time          943ms     1ms    19ms     1ms     2ms     1ms   972us
.
.
.
```

## Identify problematic SQL statements

Not all of the `SLOW_QUERY` statements are problematic. Only those whose `process_time` is very large increase the pressure on the entire cluster.

The statements whose `wait_time` is very large and `process_time` is very small are usually not problematic. This is because the statement is blocked by real problematic statements and it has to wait in the execution queue, which leads to a much longer response time.

### `ADMIN SHOW SLOW` command

In addition to the TiDB log file, you can identify slow queries by running the `ADMIN SHOW SLOW` command:

{{< copyable "sql" >}}

```sql
ADMIN SHOW SLOW recent N
ADMIN SHOW SLOW TOP [internal | all] N
```

`recent N` shows the recent N slow query records, for example:

{{< copyable "sql" >}}

```sql
ADMIN SHOW SLOW recent 10
```

`top N` shows the slowest N query records recently (within a few days). If the `internal` option is provided, the returned results would be the inner SQL executed by the system; If the `all` option is provided, the returned results would be the user's SQL combinated with inner SQL; Otherwise, this command would only return the slow query records from the user's SQL.

{{< copyable "sql" >}}

```sql
ADMIN SHOW SLOW top 3
ADMIN SHOW SLOW top internal 3
ADMIN SHOW SLOW top all 5
```

TiDB stores only a limited number of slow query records because of the limited memory. If the value of `N` in the query command is greater than the records count, the number of returned records is smaller than `N`.

The following table shows output details:

| Column name | Description |
|:------|:---- |
| start | The starting time of the SQL execution |
| duration | The duration of the SQL execution |
| details | The details of the SQL execution |
| succ | Whether the SQL statement is executed successfully. `1` means success and `0` means failure. |
| conn_id | The connection ID for the session |
| transaction_ts | The `commit ts` for a transaction commit |
| user | The user name for the execution of the statement |
| db | The database involved when the statement is executed |
| table_ids | The ID of the table involved when the SQL statement is executed |
| index_ids | The ID of the index involved when the SQL statement is executed |
| internal | This is a TiDB internal SQL statement |
| digest | The fingerprint of the SQL statement |
| sql | The SQL statement that is being executed or has been executed |
