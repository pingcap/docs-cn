---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
category: how-to
---

# TiDB Memory Control

Currently, TiDB can track the memory quota of a single SQL query and take actions to prevent OOM (out of memory) or troubleshoot OOM when the memory usage exceeds a specific threshold value. In the TiDB configuration file, you can configure the options as below to control TiDB behaviors when the memory quota exceeds the threshold value:

```
# Valid options: ["log", "cancel"]
oom-action = "log"
```

- If the configuration item above uses "log", when the memory quota of a single SQL query exceeds the threshold value which is controlled by the `tidb_mem_quota_query` variable, TiDB prints an entry of log. Then the SQL query continues to be executed. If OOM occurs, you can find the corresponding SQL query in the log.
- If the configuration item above uses "cancel", when the memory quota of a single SQL query exceeds the threshold value, TiDB stops executing the SQL query immediately and returns an error to the client. The error information clearly shows the memory usage of each physical execution operator that consumes much memory in the SQL execution process.

## Configure the memory quota of a query

In the configuration file, you can set the default Memory Quota for each Query. The following example sets it to 32GB:

```
mem-quota-query = 34359738368
```

In addition, you can control the memory quota of a query using the following session variables. Generally, you only need to configure `tidb_mem_quota_query`. Other variables are used for advanced configuration which most users do not need to care about.

| Variable Name | Description | Unit | Default Value |
|-----------------------------------|---------------------------------------------------|-------|-----------|
| tidb_mem_quota_query              | Control the memory quota of a query | Byte | 32 << 30 |
| tidb_mem_quota_hashjoin | Control the memory quota of "HashJoinExec" | Byte | 32 << 30 |
| tidb_mem_quota_mergejoin | Control the memory quota of "MergeJoinExec" | Byte | 32 << 30 |
| tidb_mem_quota_sort | Control the memory quota of "SortExec" | Byte | 32 << 30 |
| tidb_mem_quota_topn | Control the memory quota of "TopNExec" | Byte | 32 << 30 |
| tidb_mem_quota_indexlookupreader | Control the memory quota of "IndexLookUpExecutor" | Byte | 32 << 30 |
| tidb_mem_quota_indexlookupjoin | Control the memory quota of "IndexLookUpJoin" | Byte | 32 << 30 |
| tidb_mem_quota_nestedloopapply | Control the memory quota of "NestedLoopApplyExec" | Byte | 32 << 30 |

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
