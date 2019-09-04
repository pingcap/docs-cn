---
title: Identify Slow Queries
summary: Use the slow query log to identify problematic SQL statements.
category: how-to
---

# Identify Slow Queries

The slow query log is a record of SQL statements that took a long time to perform.

A problematic SQL statement can increase the pressure on the entire cluster, resulting in a longer response time. To solve this problem, you can use the slow query log to identify the problematic statements and thus improve the performance.

> **Note:**
>
> This document describes the slow query log in TiDB 2.1.8 and later. For the slow query log in earlier versions see [Identifying Slow Queries (earlier)](/v2.1/how-to/maintain/identify-slow-queries-21.md).

## Obtain the log

In TiDB, the statements whose execution time exceeds [slow-threshold](/v2.1/reference/configuration/tidb-server/configuration-file.md#slow-threshold) are individually output to [slow-query-file](/v2.1/reference/configuration/tidb-server/configuration-file.md#slow-query-file) by default, the format of the slow log is compatible, and the slow log file can be directly analyzed with `pt-query-digest`. `slow-threshold` can be modified by the configuration file, which is set to 300ms by default. `slow-query-file` is set to `tidb-slow.log` by default.

## Usage example

```sql
# Time: 2019-04-25-15:06:54.247985 +0800
# Txn_start_ts: 407942204372287489
# User: root@127.0.0.1
# Conn_ID: 2
# Query_time: 2.6649544670000003
# Process_time: 0.066 Wait_time: 0.014 Request_count: 8 Total_keys: 20008 Process_keys: 20000
# DB: test
# Is_internal: false
# Digest: edb16a8f28d9c48790925fd1c868fdae3feb49bc58481dda7df228625a5ba6e1
# Stats: t_slim:407941901863354370,t_wide:407941920305971202
# Cop_proc_avg: 0.00825 Cop_proc_p90: 0.013 Cop_proc_max: 0.013 Cop_proc_addr: 127.0.0.1:22160
# Cop_wait_avg: 0.00175 Cop_wait_p90: 0.002 Cop_wait_max: 0.002 Cop_wait_addr: 127.0.0.1:22160
# Mem_max: 195802
select count(1) from t_slim, t_wide where t_slim.c0>t_wide.c0 and t_slim.c1>t_wide.c1 and t_wide.c0 > 5000;
```

## Fields description

* `Time`: The print time of log.
* `Txn_start_ts`: The start timestamp of the transaction (transaction ID). You can use this value to `grep` the transaction-related logs.
* `User`: The name of the user who executes this statement.
* `Conn_ID`: The Connection ID (session ID). For example, you can use the keyword `con:3` to `grep` the log whose session ID is 3.
* `DB`: The current database.
* `Index_ids`: The IDs of the indexes involved in the statement.
* `Is_internal`: Whether the SQL statement is TiDB internal. `true` indicates that the SQL statement is executed internally in TiDB, such as `analyze`, `load variables`, etc. `false` indicates that the SQL statement is executed by the user.
* `Digest`: The fingerprint of the SQL statement.
* `Memory_max`: The maximum memory space used during the execution period of this SQL statement (the unit is byte).
* `Query_time`: Indicates the execution time of this statement. Only the statement whose execution time exceeds slow-threshold outputs this log (the unit is second). The unit of all the following time fields is second.
* `Process_time`: The total processing time of this SQL statement in TiKV. Because the data is sent to TiKV concurrently, this value may exceed `Query_time`.
* `Wait_time`: The total waiting time of this statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests will increase.
* `Backoff_time`: The waiting time before retry when this statement encounters errors that require a retry. The common errors as such include: `lock occurs`, `Region split`, and `tikv server is busy`.
* `Request_count`: The number of Coprocessor requests that this statement sends.
* `Total_keys`: The number of keys that Coprocessor has scanned.
* `Process_keys`: The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that many old versions exist.
* `Cop_proc_avg`: The average execution time of cop-tasks.
* `Cop_proc_p90`: The P90 execution time of cop-tasks.
* `Cop_proc_max`: The maximum execution time of cop-tasks.
* `Cop_proc_addr`: The address of the cop-task with the longest execution time.
* `Cop_wait_avg`: The average waiting time of cop-tasks.
* `Cop_wait_p90`: The P90 waiting time of cop-tasks.
* `Cop_wait_max`: The maximum waiting time of cop-tasks.
* `Cop_wait_addr`: The address of the cop-task whose waiting time is the longest.
* `Query`: A SQL statement. `Query` is not printed in the slow log, but the corresponding field is called `Query` after the slow log is mapped to the memory table.

## Memory mapping in slow log

To locate slow queries using SQL queries, the contents of slow logs in TiDB are parsed and then mapped to the `INFORMATION_SCHEMA.SLOW_QUERY` table. The column names in the table and the field names recorded in slow logs are in a one-to-one correspondence relationship.

```sql
+------------+-------------------------------------------------------------+
| Table      | Create Table                                                |
+------------+-------------------------------------------------------------+
| SLOW_QUERY | CREATE TABLE `SLOW_QUERY` (                                 |
|            |   `Time` timestamp unsigned NULL DEFAULT NULL,              |
|            |   `Txn_start_ts` bigint(20) unsigned DEFAULT NULL,          |
|            |   `User` varchar(64) DEFAULT NULL,                          |
|            |   `Conn_ID` bigint(20) unsigned DEFAULT NULL,               |
|            |   `Query_time` double unsigned DEFAULT NULL,                |
|            |   `Process_time` double unsigned DEFAULT NULL,              |
|            |   `Wait_time` double unsigned DEFAULT NULL,                 |
|            |   `Backoff_time` double unsigned DEFAULT NULL,              |
|            |   `Request_count` bigint(20) unsigned DEFAULT NULL,         |
|            |   `Total_keys` bigint(20) unsigned DEFAULT NULL,            |
|            |   `Process_keys` bigint(20) unsigned DEFAULT NULL,          |
|            |   `DB` varchar(64) DEFAULT NULL,                            |
|            |   `Index_ids` varchar(100) DEFAULT NULL,                    |
|            |   `Is_internal` tinyint(1) unsigned DEFAULT NULL,           |
|            |   `Digest` varchar(64) DEFAULT NULL,                        |
|            |   `Stats` varchar(512) DEFAULT NULL,                        |
|            |   `Cop_proc_avg` double unsigned DEFAULT NULL,              |
|            |   `Cop_proc_p90` double unsigned DEFAULT NULL,              |
|            |   `Cop_proc_max` double unsigned DEFAULT NULL,              |
|            |   `Cop_proc_addr` varchar(64) DEFAULT NULL,                 |
|            |   `Cop_wait_avg` double unsigned DEFAULT NULL,              |
|            |   `Cop_wait_p90` double unsigned DEFAULT NULL,              |
|            |   `Cop_wait_max` double unsigned DEFAULT NULL,              |
|            |   `Cop_wait_addr` varchar(64) DEFAULT NULL,                 |
|            |   `Mem_max` bigint(20) unsigned DEFAULT NULL,               |
|            |   `Query` varchar(4096) DEFAULT NULL                        |
|            | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+------------+-------------------------------------------------------------+
```

By parsing slow logs in TiDB in real time, the contents in the `INFORMATION_SCHEMA.SLOW_QUERY` table are obtained. Every time you query this table, the contents in slow log file are read and then parsed.

## Query example of SLOW_QUERY

The following examples show how to identify a slow query by querying the SLOW_QUERY table.

### Top-N slow queries

Query the Top 2 slow queries of the users. `Is_internal=false` means excluding slow queries inside TiDB and only querying slow queries from users.

```sql
/* Query all the SQL statements executed by the user and sort them by execution run-time */
tidb > select `Query_time`, query from INFORMATION_SCHEMA.`SLOW_QUERY` where `Is_internal`=false order by `Query_time` desc limit 2;
+--------------+------------------------------------------------------------------+
| Query_time   | query                                                            |
+--------------+------------------------------------------------------------------+
| 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
|  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
+--------------+------------------------------------------------------------------+
2 rows in set
Time: 0.012s
```

### Query the Top-N slow query of the `test` user

```sql
/* Query the SQL statement executed by the `test` user, and sort these statements by execution time */
tidb > select `Query_time`, query,  user from INFORMATION_SCHEMA.`SLOW_QUERY` where `Is_internal`=false and user like "test%" order by `Query_time` desc limit 2;
+-------------+------------------------------------------------------------------+----------------+
| Query_time  | query                                                            | user           |
+-------------+------------------------------------------------------------------+----------------+
| 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test@127.0.0.1 |
+-------------+------------------------------------------------------------------+----------------+
1 row in set
Time: 0.014s
```

### Query slow queries with the same SQL fingerprints

If you want to query the slow query with the same SQL fingerprint query after querying the Top-N SQL statement, you can use the fingerprint as the filter condition.

```sql
tidb > select query_time, query,digest from INFORMATION_SCHEMA.`SLOW_QUERY` where `Is_internal`=false order by `Query_time` desc limit 1;
+-------------+-----------------------------+------------------------------------------------------------------+
| query_time  | query                       | digest                                                           |
+-------------+-----------------------------+------------------------------------------------------------------+
| 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
+-------------+-----------------------------+------------------------------------------------------------------+
1 row in set
Time: 0.007s
tidb > select query, query_time from INFORMATION_SCHEMA.`SLOW_QUERY` where digest="4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
+-----------------------------+-------------+
| query                       | query_time  |
+-----------------------------+-------------+
| select * from t1 where a=1; | 0.302558006 |
| select * from t1 where a=2; | 0.401313532 |
+-----------------------------+-------------+
2 rows in set
```

## Query the slow query with pseudo `stats`

```sql
tidb > select query, query_time, stats from INFORMATION_SCHEMA.`SLOW_QUERY` where is_internal=false and stats like('%pseudo%');
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

Currently, to query `INFORMATION_SCHEMA.SLOW_QUERY`, only the slow log file name of `slow-query-file` in the configuration file is parsed, and it is set to "tidb-slow.log" by default. But to parse other log files, you can set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow log file according to the set path.

```sql
/* Set the slow log file path to facilitate so that other slow log files will be easy to be parsed. The scope of the tidb_slow_query_file variable is session. */
tidb > set tidb_slow_query_file="/path-to-log/tidb-slow.log"
Query OK, 0 rows affected
Time: 0.001s
```

Currently, `INFORMATION_SCHEMA.SLOW_QUERY` only supports parsing a slow log file. If a slow log file exceeds a certain size and is logrotated into multiple files, querying `INFORMATION_SCHEMA.SLOW_QUERY` will only parse one file.

### Parse TiDB slow logs with `pt-query-digest`

TiDB slow logs can be analyzed by `pt-query-digest`. It is recommended to use `pt-query-digest` 3.0.13 or later. For example:

```shell
$pt-query-digest --version
pt-query-digest 3.0.13

$ pt-query-digest --report tidb-slow.log
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

Not all of the `SLOW_QUERY` statements are problematic. Only those whose `process_time` is very large will increase the pressure on the entire cluster.

The statements whose `wait_time` is very large and `process_time` is very small are usually not problematic. The large `wait_time` is because the statement is blocked by real problematic statements and it has to wait in the execution queue, which leads to a much longer response time.

### `admin show slow` command

In addition to the TiDB log file, you can identify slow queries by running the `admin show slow` command:

```sql
admin show slow recent N
admin show slow top [internal | all] N
```

`recent N` shows the recent N slow query records, for example:

```sql
admin show slow recent 10
```

`top N` shows the slowest N query records recently (within a few days).
If the `internal` option is provided, the returned results would be the inner SQL executed by the system;
If the `all` option is provided, the returned results would be the user's SQL combinated with inner SQL;
Otherwise, this command would only return the slow query records from the user's SQL.

```sql
admin show slow top 3
admin show slow top internal 3
admin show slow top all 5
```

Due to the memory footprint restriction, the stored slow query records count is limited. If the specified `N` is greater than the records count, the returned records count may be smaller than `N`.
