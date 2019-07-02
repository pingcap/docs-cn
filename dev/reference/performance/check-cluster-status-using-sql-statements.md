---
title: Check the TiDB Cluster Status Using SQL Statements
summary: This document introduces that TiDB offers some SQL statements and system tables to check the TiDB cluster status.
category: reference
---

# Check the TiDB Cluster Status Using SQL Statements

TiDB offers some SQL statements and system tables to check the TiDB cluster status.

The `INFORMATION_SCHEMA` system database offers system tables as follows to query the cluster status and diagnose common cluster issues:

- [`TABLES`](/reference/system-databases/information-schema.md#tables-table)
- [`TIDB_INDEXES`](/reference/system-databases/information-schema.md#tidb-indexes-table)
- [`ANALYZE_STATUS`](/reference/system-databases/information-schema.md#analyze-status-table)
- [`TIDB_HOT_REGIONS`](/reference/system-databases/information-schema.md#tidb-hot-regions-table)
- [`TIKV_STORE_STATUS`](/reference/system-databases/information-schema.md#tikv-store-status-table)
- [`TIKV_REGION_STATUS`](/reference/system-databases/information-schema.md#tikv-region-status-table)
- [`TIKV_REGION_PEERS`](/reference/system-databases/information-schema.md#tikv-region-peers-table)

You can also use the following statements to obtain some useful information for troubleshooting and querying the TiDB cluster status.

- `ADMIN SHOW DDL`: obtains the ID of TiDB with the `DDL owner` role and `IP:PORT`.
- The feature of `SHOW ANALYZE STATUS` is the same with that of [the `ANALYZE_STATUS` table](/reference/system-databases/information-schema.md#analyze-status-table).
- Specific `EXPLAIN` statements
    - `EXPLAIN ANALYZE`: obtains some detailed information for execution of a SQL statement.
    - `EXPLAIN FOR CONNECTION`: obtains the execution plan for the query executed last in a connection. Can be used along with `SHOW PROCESSLIST`.
    - For more information about `EXPLAIN`, see [Understand the Query Execution Plan](/reference/performance/understanding-the-query-execution-plan.md).
