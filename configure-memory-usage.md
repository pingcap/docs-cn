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
