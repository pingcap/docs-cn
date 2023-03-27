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

TiDB provides the following system variables to control the threshold of spilling for each operator. When the memory usage of an operator exceeds the threshold, TiFlash triggers the spilling for the operator.

* [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

## Example

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

## Notes

* When the Hash Aggregation operator does not have a `GROUP BY` key, it does not support spilling. Even if the Hash Aggregation operator contains a distinct aggregation function, it does not support spilling.
* Currently, the threshold is calculated for each operator. If a query contains two Hash Aggregation operators, and the threshold is set to 10 GiB, then the two Hash Aggregation operators will only spill data when their respective memory usage exceeds 10 GiB.
* Currently, the Hash Aggregation operators and TopN/Sort operators use the merge aggregation and merge sort algorithm during the restore phase. Therefore, these two operators only trigger a single round of spill. If the memory demand is very high and the memory usage during the restore phase still exceeds the threshold, the spill will not be triggered again.
* Currently, the Hash Join operator uses the partition-based spill strategy. If the memory usage during the restore phase still exceeds the threshold, the spill will be triggered again. However, to control the scale of the spill, the number of rounds of spill is limited to three. If the memory usage during the restore phase still exceeds the threshold after the third round of spill, the spill will not be triggered again.
