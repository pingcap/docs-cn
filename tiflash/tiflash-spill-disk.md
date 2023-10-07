---
title: TiFlash Spill to Disk
summary: Learn how TiFlash spills data to disk and how to customize the spill behavior.
---

# TiFlash Spill to Disk

This document introduces how TiFlash spills data to disk during computation.

Starting from v7.0.0, TiFlash supports spilling intermediate data to disk to relieve memory pressure. The following operators are supported:

* Hash Join operators with equi-join conditions
* Hash Aggregation operators with `GROUP BY` keys
* TopN operators, and Sort operators in Window functions

## Trigger the spilling

TiFlash provides two triggering mechanisms for spilling data to disk.

* Operator-level spilling: by specifing the data spilling threshold for each operator, you can control when TiFlash spills data of that operator to disk.
* Query-level spilling: by specifing the maximum memory usage of a query on a TiFlash node and the memory ratio for spilling, you can control when TiFlash spills data of supported operators in a query to disk as needed.

### Operator-level spilling

Starting from v7.0.0, TiFlash supports automatic spilling at the operator level. You can control the threshold of data spilling for each operator using the following system variables. When the memory usage of an operator exceeds the threshold, TiFlash triggers spilling for the operator.

* [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

#### Example

This example constructs a SQL statement that consumes a lot of memory to demonstrate the spilling of the Hash Aggregation operator.

1. Prepare the environment. Create a TiFlash cluster with 2 nodes and import the TPCH-100 data.
2. Execute the following statements. These statements do not limit the memory usage of the Hash Aggregation operator with `GROUP BY` keys.

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3. From the log of TiFlash, you can see that the query needs to consume 29.55 GiB of memory on a single TiFlash node:

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. Execute the following statement. This statement limits the memory usage of the Hash Aggregation operator with `GROUP BY` keys to 10737418240 (10 GiB).

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 10737418240;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5. From the log of TiFlash, you can see that by configuring `tidb_max_bytes_before_tiflash_external_group_by`, TiFlash triggers the spilling of intermediate results, significantly reducing the memory used by the query.

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]
    ```

### Query-level spilling

Starting from v7.4.0, TiFlash supports automatic spilling at the query level. You can control this feature using the following system variables:

* [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740): limits the maximum memory usage for a query on a TiFlash node.
* [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740): controls the memory ratio that triggers data spilling.

If both `tiflash_mem_quota_query_per_node` and `tiflash_query_spill_ratio` are set to values greater than 0, TiFlash automatically triggers spilling for supported operators in a query when the memory usage of a query exceeds `tiflash_mem_quota_query_per_node * tiflash_query_spill_ratio`.

#### Example

This example constructs a SQL statement that consumes a lot of memory to demonstrate the query-level spilling.

1. Prepare the environment. Create a TiFlash cluster with 2 nodes and import the TPCH-100 data.

2. Execute the following statements. These statements do not limit the memory usage of the query or the memory usage of the Hash Aggregation operator with `GROUP BY` keys.

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SET tiflash_mem_quota_query_per_node = 0;
    SET tiflash_query_spill_ratio = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3. From the log of TiFlash, you can see that the query consumes 29.55 GiB of memory on a single TiFlash node:

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. Execute the following statements. These statements limit the maximum memory usage of the query on a TiFlash node to 5 GiB.

    ```sql
    SET tiflash_mem_quota_query_per_node = 5368709120;
    SET tiflash_query_spill_ratio = 0.7;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5. From the log of TiFlash, you can see that by configuring query-level spilling, TiFlash triggers the spilling of intermediate results, significantly reducing the memory used by the query.

    ```
    [DEBUG] [MemoryTracker.cpp:101] ["Peak memory usage (for query): 3.94 GiB."] [source=MemoryTracker] [thread_id=1547]
    ```

## Notes

* When the Hash Aggregation operator does not have a `GROUP BY` key, it does not support spilling. Even if the Hash Aggregation operator contains a distinct aggregation function, it does not support spilling.
* Currently, the threshold for operator-level spilling is calculated for each operator separately. For a query containing two Hash Aggregation operators, if the query-level spilling is not configured and the threshold of the aggregation operator is set to 10 GiB, the two Hash Aggregation operators will only spill data when their respective memory usage exceeds 10 GiB.
* Currently, the Hash Aggregation operators and TopN/Sort operators use the merge aggregation and merge sort algorithm during the restore phase. Therefore, these two operators only trigger a single round of spill. If the memory demand is very high and the memory usage during the restore phase still exceeds the threshold, the spill will not be triggered again.
* Currently, the Hash Join operator uses the partition-based spill strategy. If the memory usage during the restore phase still exceeds the threshold, the spill will be triggered again. However, to control the scale of the spill, the number of rounds of spill is limited to three. If the memory usage during the restore phase still exceeds the threshold after the third round of spill, the spill will not be triggered again.
* When query-level spilling is configured (that is, both [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) and [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) are greater than 0), TiFlash ignores spilling thresholds of individual operators and automatically triggers spilling for relevant operators in a query based on the query-level spilling thresholds.
* Even when query-level spilling is configured, if none of the operators used in a query support spilling, the intermediate computation results of that query still cannot be spilled to disk. In this case, when the memory usage of that query exceeds the related threshold, TiFlash will return an error and terminate the query.
* Even when query-level spilling is configured and a query contains operators that support spilling, the query might still return an error due to exceeding memory thresholds in either of the following scenarios:
    - Other non-spilling operators in the query consume too much memory.
    - The spilling operators do not spill to disk timely.

  To address situations where spilling operators do not spill to disk in time, you can try reducing [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) to avoid memory threshold errors.
