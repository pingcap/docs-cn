---
title: Identify Expensive Queries
aliases: ['/docs/dev/identify-expensive-queries/','/docs/dev/how-to/maintain/identify-abnormal-queries/identify-expensive-queries/']
---

# Identify Expensive Queries

TiDB allows you to identify expensive queries during SQL execution, so you can diagnose and improve the performance of SQL execution. Specifically, TiDB prints the information about statements whose execution time exceeds [`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold) (60 seconds by default) or memory usage exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (1 GB by default) to the [tidb-server log file](/tidb-configuration-file.md#logfile) ("tidb.log" by default).

> **Note:**
>
> The expensive query log differs from the [slow query log](/identify-slow-queries.md) in this way: TiDB prints statement information to the expensive query log **as soon as** the statement exceeds the threshold of resource usage (execution time or memory usage); while TiDB prints statement information to the slow query log **after** the statement execution.

## Expensive query log example

```sql
[2020/02/05 15:32:25.096 +08:00] [WARN] [expensivequery.go:167] [expensive_query] [cost_time=60.008338935s] [wait_time=0s] [request_count=1] [total_keys=70] [process_keys=65] [num_cop_tasks=1] [process_avg_time=0s] [process_p90_time=0s] [process_max_time=0s] [process_max_addr=10.0.1.9:20160] [wait_avg_time=0.002s] [wait_p90_time=0.002s] [wait_max_time=0.002s] [wait_max_addr=10.0.1.9:20160] [stats=t:pseudo] [conn_id=60026] [user=root] [database=test] [table_ids="[122]"] [txn_start_ts=414420273735139329] [mem_max="1035 Bytes (1.0107421875 KB)"] [sql="insert into t select sleep(1) from t"]
```

## Fields description

Basic fields:

* `cost_time`: The execution time of a statement when the log is printed.
* `stats`: The version of statistics used by the tables or indexes involved in a statement. If the value is `pseudo`, it means that there are no available statistics. In this case, you need to analyze the tables or indexes.
* `table_ids`: The IDs of the tables involved in a statement.
* `txn_start_ts`: The start timestamp and the unique ID of a transaction. You can use this value to search for the transaction-related logs.
* `sql`: The sql statement.

Memory usage related fields:

* `mem_max`: Memory usage of a statement when the log is printed. This field has two kinds of units to measure memory usage: byte and other readable and adaptable units (such as MB and GB).

User related fields:

* `user`: The name of the user who executes the statement.
* `conn_id`: The connection ID (session ID). For example, you can use the keyword `con:60026` to search for the log whose session ID is `60026`.
* `database`: The database where the statement is executed.

TiKV Coprocessor task related fields:

* `wait_time`: The total waiting time of all Coprocessor requests of a statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests increases.
* `request_count`: The number of Coprocessor requests that a statement sends.
* `total_keys`: The number of keys that Coprocessor has scanned.
* `processed_keys`: The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that many old versions exist.
* `num_cop_tasks`: The number of Coprocessor requests that a statement sends.
* `process_avg_time`: The average execution time of Coprocessor tasks.
* `process_p90_time`: The P90 execution time of Coprocessor tasks.
* `process_max_time`: The maximum execution time of Coprocessor tasks.
* `process_max_addr`: The address of the Coprocessor task with the longest execution time.
* `wait_avg_time`: The average waiting time of Coprocessor tasks.
* `wait_p90_time`: The P90 waiting time of Coprocessor tasks.
* `wait_max_time`: The maximum waiting time of Coprocessor tasks.
* `wait_max_addr`: The address of the Coprocessor task with the longest waiting time.
