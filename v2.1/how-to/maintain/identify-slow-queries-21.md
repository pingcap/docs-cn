---
title: Identify Slow Queries (earlier)
summary: Use the slow query log to identify problematic SQL statements.
category: user guide
---

# Identify Slow Queries (earlier)

The slow query log is a record of SQL statements that took a long time to perform.

A problematic SQL statement can increase the pressure on the entire cluster, resulting in a longer response time. To solve this problem, you can use the slow query log to identify the problematic statements and thus improve the performance.

> **Note:**
>
> This document describes the slow query log in versions up to TiDB 2.1.7. For the slow query log in later versions see [Identifying Slow Queries](/how-to/maintain/identify-slow-queries.md).

### Obtain the log

By `grep` the keyword `SLOW_QUERY` in the log file of TiDB, you can obtain the logs of statements whose execution time exceeds [slow-threshold](/reference/configuration/tidb-server/configuration-file.md#slow-threshold).

You can edit `slow-threshold` in the configuration file and its default value is 300ms. If you configure the [slow-query-file](/reference/configuration/tidb-server/configuration-file.md#slow-query-file), all the slow query logs will be written in this file. 

### Usage example

```
2018/08/20 19:52:08.632 adapter.go:363: [warning] [SLOW_QUERY] cost_time:18.647928814s
process_time:1m6.768s wait_time:12m11.212s backoff_time:600ms request_count:2058
total_keys:1869712 processed_keys:1869710 succ:true con:3 user:root@127.0.0.1
txn_start_ts:402329674704224261 database:test table_ids:[31],index_ids:[1],
sql:select count(c) from sbtest1 use index (k_1)
```

### Fields description

This section describes fields in the slow query log based on the usage example above.

#### `cost_time`

The execution time of this statement. Only the statements whose execution time exceeds [slow-threshold](/reference/configuration/tidb-server/configuration-file.md#slow-threshold) output this log.

#### `process_time`

The total processing time of this statement in TiKV. Because data is sent to TiKV concurrently for execution, this value might exceed `cost_time`.

#### `wait_time`

The total waiting time of this statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests will increase.

#### `backoff_time`

The waiting time before retry when this statement encounters errors that require a retry. The common errors as such include: lock occurs, Region split, the TiKV server is busy.

#### `request_count`

The number of Coprocessor requests that this statement sends.

#### `total_keys`

The number of keys that Coprocessor has scanned.

#### `processed_keys`

The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that the number of old versions are relatively large.

#### `succ`

Whether the execution of the request succeeds or not.

#### `con`

Connection ID (session ID). For example, you can use the keyword `con:3` to `grep` the log whose session ID is 3.

#### `user`

The name of the user who executes this statement.

#### `txn_start_ts`

The start timestamp of the transaction, that is, the ID of the transaction. You can use this value to `grep` the transaction-related logs.

#### `database`

The current database.

#### `table_ids`

The IDs of the tables involved in the statement.

#### `index_ids`

The IDs of the indexes involved in the statement.

#### `sql`

The SQL statement.

### Identify problematic SQL statements

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
