---
title: Identify Slow Queries
summary: Use the slow query log to identify problematic SQL statements.
category: how-to
---

# Identify Slow Queries

To help users identify slow queries, analyze and improve the performance of SQL execution, TiDB outputs the statements whose execution time exceeds [slow-threshold](/dev/reference/configuration/tidb-server/configuration-file.md#slow-threshold) (The default value is 300 milliseconds) to [slow-query-file](/dev/reference/configuration/tidb-server/configuration-file.md#slow-query-file) (The default value is "tidb-slow.log").

## Usage example

```sql
# Time: 2019-08-14T09:26:59.487776265+08:00
# Txn_start_ts: 410450924122144769
# User: root@127.0.0.1
# Conn_ID: 3086
# Query_time: 1.527627037
# Process_time: 0.07 Request_count: 1 Total_keys: 131073 Process_keys: 131072 Prewrite_time: 0.335415029 Commit_time: 0.032175429 Get_commit_ts_time: 0.000177098 Local_latch_wait_time: 0.106869448 Write_keys: 131072 Write_size: 3538944 Prewrite_region: 1
# DB: test
# Is_internal: false
# Digest: 50a2e32d2abbd6c1764b1b7f2058d428ef2712b029282b776beb9506a365c0f1
# Stats: t:pseudo
# Num_cop_tasks: 1
# Cop_proc_avg: 0.07 Cop_proc_p90: 0.07 Cop_proc_max: 0.07 Cop_proc_addr: 172.16.5.87:20171
# Cop_wait_avg: 0 Cop_wait_p90: 0 Cop_wait_max: 0 Cop_wait_addr: 172.16.5.87:20171
# Mem_max: 525211
# Succ: false
insert into t select * from t;
```

## Fields description

> **Note:**
>
> The unit of all the following time fields in the slow query log is **"second"**.

Slow query basics:

* `Time`: The print time of log.
* `Query_time`: The execution time of a statement.
* `Query`: A SQL statement. `Query` is not printed in the slow log, but the corresponding field is called `Query` after the slow log is mapped to the memory table.
* `Digest`: The fingerprint of the SQL statement.
* `Txn_start_ts`: The start timestamp and the unique ID of a transaction. You can use this value to search for the transaction-related logs.
* `Is_internal`: Whether a SQL statement is TiDB internal. `true` indicates that a SQL statement is executed internally in TiDB and `false` indicates that a SQL statement is executed by the user.
* `Index_ids`: The IDs of the indexes involved in a statement.
* `Succ`: Whether a statement is executed successfully.
* `Backoff_time`: The waiting time before retry when a statement encounters errors that require a retry. The common errors as such include: `lock occurs`, `Region split`, and `tikv server is busy`.

Memory usage fields:

* `Memory_max`: The maximum memory space used during the execution period of a SQL statement (the unit is byte).

User fields:

* `User`: The name of the user who executes this statement.
* `Conn_ID`: The Connection ID (session ID). For example, you can use the keyword `con:3` to search for the log whose session ID is `3`.
* `DB`: The current database.

TiKV Coprocessor Task fields:

* `Request_count`: The number of Coprocessor requests that a statement sends.
* `Total_keys`: The number of keys that Coprocessor has scanned.
* `Process_time`: The total processing time of a SQL statement in TiKV. Because data is sent to TiKV concurrently, this value might exceed `Query_time`.
* `Wait_time`: The total waiting time of a statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests increases.
* `Process_keys`: The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that many old versions exist.
* `Cop_proc_avg`: The average execution time of cop-tasks.
* `Cop_proc_p90`: The P90 execution time of cop-tasks.
* `Cop_proc_max`: The maximum execution time of cop-tasks.
* `Cop_proc_addr`: The address of the cop-task with the longest execution time.
* `Cop_wait_avg`: The average waiting time of cop-tasks.
* `Cop_wait_p90`: The P90 waiting time of cop-tasks.
* `Cop_wait_max`: The maximum waiting time of cop-tasks.
* `Cop_wait_addr`: The address of the cop-task whose waiting time is the longest.

## Memory mapping in slow log

You can query the contents of the slow query log by querying the `INFORMATION_SCHEMA.SLOW_QUERY` table. Each column name in the table corresponds to one field name in the slow log. For table structure, see the introduction to the `SLOW_QUERY` table in [Information Schema](/dev/reference/system-databases/information-schema.md#information-schema).

> **Note:**
>
> Every time you query the `SLOW_QUERY` table, TiDB reads and parses the current slow query log.

## Query example of SLOW_QUERY

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

Usage example:

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

Usage example:

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

    Usage example:

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

    Usage example:

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

Usage example:

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

### Parse other TiDB slow log files

TiDB uses the session variable `tidb_slow_query_file` to control the files to be read and parsed when querying `INFORMATION_SCHEMA.SLOW_QUERY`. You can query the contents of other slow query log files by modifying the value of the session variable.

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

{{< copyable "shell" >}}

```shell
pt-query-digest --report tidb-slow.log
```

Usage example:

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

### `admin show slow` command

In addition to the TiDB log file, you can identify slow queries by running the `admin show slow` command:

{{< copyable "sql" >}}

```sql
admin show slow recent N
admin show slow top [internal | all] N
```

`recent N` shows the recent N slow query records, for example:

{{< copyable "sql" >}}

```sql
admin show slow recent 10
```

`top N` shows the slowest N query records recently (within a few days).
If the `internal` option is provided, the returned results would be the inner SQL executed by the system;
If the `all` option is provided, the returned results would be the user's SQL combinated with inner SQL;
Otherwise, this command would only return the slow query records from the user's SQL.

{{< copyable "sql" >}}

```sql
admin show slow top 3
admin show slow top internal 3
admin show slow top all 5
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
| transcation_ts | The `commit ts` for a transaction commit |
| user | The user name for the execution of the statement |
| db | The database involved when the statement is executed |
| table_ids | The ID of the table involved when the SQL statement is executed |
| index_ids | The ID of the index involved when the SQL statement is executed |
| internal | This is a TiDB internal SQL statement |
| digest | The fingerprint of the SQL statement |
| sql | The SQL statement that is being executed or has been executed |
