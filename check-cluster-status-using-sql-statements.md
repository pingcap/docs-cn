---
title: Check the TiDB Cluster Status Using SQL Statements
summary: This document introduces that TiDB offers some SQL statements and system tables to check the TiDB cluster status.
aliases: ['/docs/dev/check-cluster-status-using-sql-statements/','/docs/dev/reference/performance/check-cluster-status-using-sql-statements/']
---

# Check the TiDB Cluster Status Using SQL Statements

TiDB offers some SQL statements and system tables to check the TiDB cluster status.

The `INFORMATION_SCHEMA` system database offers system tables as follows to query the cluster status and diagnose common cluster issues:

- [`TABLES`](/information-schema/information-schema-tables.md)
- [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)
- [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)
- [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)
- [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)
- [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)
- [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)

You can also use the following statements to obtain some useful information for troubleshooting and querying the TiDB cluster status.

- `ADMIN SHOW DDL`: obtains the ID of TiDB with the `DDL owner` role and `IP:PORT`.
- The feature of `SHOW ANALYZE STATUS` is the same with that of [the `ANALYZE_STATUS` table](/information-schema/information-schema-analyze-status.md).
- Specific `EXPLAIN` statements
    - `EXPLAIN ANALYZE`: obtains some detailed information for execution of a SQL statement.
    - `EXPLAIN FOR CONNECTION`: obtains the execution plan for the query executed last in a connection. Can be used along with `SHOW PROCESSLIST`.
    - For more information about `EXPLAIN`, see [Understand the Query Execution Plan](/query-execution-plan.md).
