---
title: Check the TiDB Cluster Status Using SQL Statements
summary: This document introduces that TiDB offers some SQL statements and system tables to check the TiDB cluster status.
category: reference
---

# Check the TiDB Cluster Status Using SQL Statements

TiDB offers some SQL statements and system tables to check the TiDB cluster status.

The `INFORMATION_SCHEMA` system database offers system tables as follows to query the cluster status and diagnose common cluster issues:

- [`TABLES`](/v3.0/reference/system-databases/information-schema.md#tables-table)
- [`TIDB_INDEXES`](/v3.0/reference/system-databases/information-schema.md#tidb_indexes-table)
- [`ANALYZE_STATUS`](/v3.0/reference/system-databases/information-schema.md#analyze_status-table)
- [`TIDB_HOT_REGIONS`](/v3.0/reference/system-databases/information-schema.md#tidb_hot_regions-table)
- [`TIKV_STORE_STATUS`](/v3.0/reference/system-databases/information-schema.md#tikv_store_status-table)
- [`TIKV_REGION_STATUS`](/v3.0/reference/system-databases/information-schema.md#tikv_region_status-table)
- [`TIKV_REGION_PEERS`](/v3.0/reference/system-databases/information-schema.md#tikv_region_peers-table)

You can also use the following statements to obtain some useful information for troubleshooting and querying the TiDB cluster status.

- `ADMIN SHOW DDL`: obtains the ID of TiDB with the `DDL owner` role and `IP:PORT`.
- The feature of `SHOW ANALYZE STATUS` is the same with that of [the `ANALYZE_STATUS` table](/v3.0/reference/system-databases/information-schema.md#analyze_status-table).
- Specific `EXPLAIN` statements
    - `EXPLAIN ANALYZE`: obtains some detailed information for execution of a SQL statement.
    - `EXPLAIN FOR CONNECTION`: obtains the execution plan for the query executed last in a connection. Can be used along with `SHOW PROCESSLIST`.
    - For more information about `EXPLAIN`, see [Understand the Query Execution Plan](/v3.0/reference/performance/understanding-the-query-execution-plan.md).