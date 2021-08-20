---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
aliases: ['/docs/dev/configure-memory-usage/','/docs/dev/how-to/configure/memory-control/']
---

# TiDB Memory Control

Currently, TiDB can track the memory quota of a single SQL query and take actions to prevent OOM (out of memory) or troubleshoot OOM when the memory usage exceeds a specific threshold value. In the TiDB configuration file, you can configure the options as below to control TiDB behaviors when the memory quota exceeds the threshold value:

```
# Valid options: ["log", "cancel"]
oom-action = "cancel"
```

- If the configuration item above uses "log", when the memory quota of a single SQL query exceeds the threshold value which is controlled by the `tidb_mem_quota_query` variable, TiDB prints an entry of log. Then the SQL query continues to be executed. If OOM occurs, you can find the corresponding SQL query in the log.
- If the configuration item above uses "cancel", when the memory quota of a single SQL query exceeds the threshold value, TiDB stops executing the SQL query immediately and returns an error to the client. The error information clearly shows the memory usage of each physical execution operator that consumes much memory in the SQL execution process.

## Configure the memory quota of a query

In the configuration file, you can set the default Memory Quota for each Query. The following example sets it to 32GB:

```
mem-quota-query = 34359738368
```

In addition, you can control the memory quota of a query using the following session variables. Generally, you only need to configure `tidb_mem_quota_query`. Other variables are used for advanced configuration which most users do not need to care about.

| Variable Name                    | Description                                       | Unit | Default Value |
| -------------------------------- | ------------------------------------------------- | ---- | ------------- |
| tidb_mem_quota_query             | Control the memory quota of a query               | Byte | 1 << 30 (1 GB)  |
| tidb_mem_quota_hashjoin          | Control the memory quota of "HashJoinExec"        | Byte | 32 << 30      |
| tidb_mem_quota_mergejoin         | Control the memory quota of "MergeJoinExec"       | Byte | 32 << 30      |
| tidb_mem_quota_sort              | Control the memory quota of "SortExec"            | Byte | 32 << 30      |
| tidb_mem_quota_topn              | Control the memory quota of "TopNExec"            | Byte | 32 << 30      |
| tidb_mem_quota_indexlookupreader | Control the memory quota of "IndexLookUpExecutor" | Byte | 32 << 30      |
| tidb_mem_quota_indexlookupjoin   | Control the memory quota of "IndexLookUpJoin"     | Byte | 32 << 30      |
| tidb_mem_quota_nestedloopapply   | Control the memory quota of "NestedLoopApplyExec" | Byte | 32 << 30      |

Some usage examples:

{{< copyable "sql" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8GB:
set @@tidb_mem_quota_query = 8 << 30;
```

{{< copyable "sql" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8MB:
set @@tidb_mem_quota_query = 8 << 20;
```

{{< copyable "sql" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8KB:
set @@tidb_mem_quota_query = 8 << 10;
```

## Configure the memory usage threshold of a tidb-server instance

In the TiDB configuration file, you can set the memory usage threshold of a tidb-server instance by configuring [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409).

The following example sets the total memory usage of a tidb-server instance to 32 GB:

{{< copyable "" >}}

```toml
[performance]
server-memory-quota = 34359738368
```

In this configuration, when the memory usage of a tidb-server instance reaches 32 GB, the instance starts to kill running SQL statements randomly until the memory usage drops below 32 GB. SQL operations that are forced to terminate return an `Out Of Global Memory Limit!` error message to the client.

> **Warning:**
>
> + `server-memory-quota` is still an experimental feature. It is **NOT** recommended that you use it in a production environment.
> + The default value of `server-memory-quota` is `0`, which means no memory limit.

## Trigger the alarm of excessive memory usage

In the default configuration, a tidb-server instance prints an alarm log and records associated status files when the machine memory usage reaches 80% of its total memory. You can set the memory usage ratio threshold by configuring `memory-usage-alarm-ratio`. For detailed alarm rules, refer to the description of [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).

Note that after the alarm is triggered once, it will be triggered again only if the memory usage rate has been below the threshold for more than ten seconds and reaches the threshold again. In addition, to avoid storing excessive status files generated by alarms, currently, TiDB only retains the status files generated during the recent five alarms.

The following example constructs a memory-intensive SQL statement that triggers the alarm:

1. Set `memory-usage-alarm-ratio` to `0.8`:

    {{< copyable "" >}}

    ```toml
    mem-quota-query = 34359738368  // Increases the memory limit of each query to construct SQL statements that take up larger memory.
    [performance]
    memory-usage-alarm-ratio = 0.8
    ```

2. Execute `CREATE TABLE t(a int);` and insert 1000 rows of data.

3. Execute `select * from t t1 join t t1 join t t3 order by t1.a`. This SQL statement outputs one billion records, which consumes a large amount of memory and therefore triggers the alarm.

4. Check the `tidb.log` file which records the total system memory, current system memory usage, memory usage of the tidb-server instance, and the directory of status files.

    ```
    [2020/11/30 15:25:17.252 +08:00] [WARN] [memory_usage_alarm.go:141] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=33682427904] ["system memory usage"=27142864896] ["tidb-server memory usage"=22417922896] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

    The fields of the example log file above are described as follows:

    * `is server-memory-quota set` indicates whether [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409) is set.
    * `system memory total` indicates the total memory of the current system.
    * `system memory usage` indicates the current system memory usage.
    * `tidb-server memory usage` indicates the memory usage of the tidb-server instance.
    * `memory-usage-alarm-ratio` indicates the value of [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).
    * `record path` indicates the directory of status files.

5. You can see a set of files in the directory of status files (In the above example, the directory is `/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record`), including `goroutinue`, `heap`, and `running_sql`. These three files are suffixed with the time when status files are logged. They respectively record goroutine stack information, the usage status of heap memory, and the running SQL information when the alarm is triggered. For the format of log content in `running_sql`, refer to [`expensive-queries`](/identify-expensive-queries.md).

## Other memory control behaviors of tidb-server

### Flow control

- TiDB supports dynamic memory control for the operator that reads data. By default, this operator uses the maximum number of threads that [`tidb_disql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL execution exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.

- This flow control behavior is controlled by the system variable [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action).
- When the flow control behavior is triggered, TiDB outputs a log containing the keywords `memory exceeds quota, destroy one token now`.

### Disk spill

TiDB supports disk spill for execution operators. When the memory usage of a SQL execution exceeds the memory quota, tidb-server can spill the intermediate data of execution operators to the disk to relieve memory pressure. Operators supporting disk spill include Sort, MergeJoin, HashJoin, and HashAgg.

- The disk spill behavior is jointly controlled by the [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query), [`oom-use-tmp-storage`](/tidb-configuration-file.md#oom-use-tmp-storage), [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path), and [`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota) parameters.
- When the disk spill is triggered, TiDB outputs a log containing the keywords `memory exceeds quota, spill to disk now` or `memory exceeds quota, set aggregate mode to spill-mode`.
- Disk spill for the Sort, MergeJoin, and HashJoin operator is introduced in v4.0.0; disk spill for the HashAgg operator is introduced in v5.2.0.
- When the SQL executions containing Sort, MergeJoin, or HashJoin cause OOM, TiDB triggers disk spill by default. When SQL executions containing HashAgg cause OOM, TiDB does not trigger disk spill by default. You can configure the system variable `tidb_executor_concurrency = 1` to trigger disk spill for HashAgg.

> **Note:**
>
> The disk spill for HashAgg does not support SQL executions containing the `DISTINCT` aggregate function. When a SQL execution containing a `DISTINCT` aggregate function uses too much memory, the disk spill does not apply.

The following example uses a memory-consuming SQL statement to demonstrate the disk spill feature for HashAgg:

1. Configure the memory quota of a SQL statement to 1GB (1 GB by default):

    {{< copyable "sql" >}}

    ```sql
    set tidb_mem_quota_query = 1 << 30;
    ```

2. Create a single table `CREATE TABLE t(a int);` and insert 256 rows of different data.

3. Execute the following SQL statement:

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    Because executing this SQL statement occupies too much memory, the following "Out of Memory Quota" error message is returned:

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4. Configure the system variable `tidb_executor_concurrency` to 1. With this configuration, when out of memory, HashAgg automatically tries to trigger disk spill.

    {{< copyable "sql" >}}

    ```sql
    set tidb_executor_concurrency = 1;
    ```

5. Execute the same SQL statement. You can find that this time, the statement is successfully executed and no error message is returned. From the following detailed execution plan, you can see that HashAgg has used 600 MB of hard disk space.

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    ```sql
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | id                              | estRows     | actRows  | task      | access object | execution info                                                                                                                                                      | operator info                                                   | memory    | disk     |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | HashAgg_11                      | 204.80      | 16777216 | root      |               | time:1m37.4s, loops:16385                                                                                                                                           | group by:test.t.a, test.t.a, test.t.a, funcs:count(1)->Column#7 | 1.13 GB   | 600.0 MB |
    | └─HashJoin_12                   | 16777216.00 | 16777216 | root      |               | time:21.5s, loops:16385, build_hash_table:{total:267.2µs, fetch:228.9µs, build:38.2µs}, probe:{concurrency:1, total:35s, max:35s, probe:35s, fetch:962.2µs}         | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |   ├─TableReader_21(Build)       | 256.00      | 256      | root      |               | time:87.2µs, loops:2, cop_task: {num: 1, max: 150µs, proc_keys: 0, rpc_num: 1, rpc_time: 145.1µs, copr_cache_hit_ratio: 0.00}                                       | data:TableFullScan_20                                           | 885 Bytes | N/A      |
    |   │ └─TableFullScan_20          | 256.00      | 256      | cop[tikv] | table:t3      | tikv_task:{time:23.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |   └─HashJoin_14(Probe)          | 65536.00    | 65536    | root      |               | time:728.1µs, loops:65, build_hash_table:{total:307.5µs, fetch:277.6µs, build:29.9µs}, probe:{concurrency:1, total:34.3s, max:34.3s, probe:34.3s, fetch:278µs}      | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |     ├─TableReader_19(Build)     | 256.00      | 256      | root      |               | time:126.2µs, loops:2, cop_task: {num: 1, max: 308.4µs, proc_keys: 0, rpc_num: 1, rpc_time: 295.3µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_18                                           | 885 Bytes | N/A      |
    |     │ └─TableFullScan_18        | 256.00      | 256      | cop[tikv] | table:t2      | tikv_task:{time:79.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |     └─TableReader_17(Probe)     | 256.00      | 256      | root      |               | time:211.1µs, loops:2, cop_task: {num: 1, max: 295.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 279.7µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_16                                           | 885 Bytes | N/A      |
    |       └─TableFullScan_16        | 256.00      | 256      | cop[tikv] | table:t1      | tikv_task:{time:71.4µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    9 rows in set (1 min 37.428 sec)
    ```