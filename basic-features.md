---
title: TiDB Features
summary: Learn about the basic features of TiDB.
aliases: ['/docs/dev/basic-features/']
---

# TiDB Features

This document lists the features supported in each TiDB version. Note that supports for experimental features might change before the final release.

## Data types, functions, and operators

| Data types, functions, and operators                                                                     | 5.3          | 5.2          | 5.1          | 5.0          | 4.0          |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Numeric types](/data-type-numeric.md)                                                                   | Y            | Y            | Y            | Y            | Y            |
| [Date and time types](/data-type-date-and-time.md)                                                       | Y            | Y            | Y            | Y            | Y            |
| [String types](/data-type-string.md)                                                                     | Y            | Y            | Y            | Y            | Y            |
| [JSON type](/data-type-json.md)                                                                          | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Control flow functions](/functions-and-operators/control-flow-functions.md)                             | Y            | Y            | Y            | Y            | Y            |
| [String functions](/functions-and-operators/string-functions.md)                                         | Y            | Y            | Y            | Y            | Y            |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md)           | Y            | Y            | Y            | Y            | Y            |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md)                           | Y            | Y            | Y            | Y            | Y            |
| [Bit functions and operators](/functions-and-operators/bit-functions-and-operators.md)                   | Y            | Y            | Y            | Y            | Y            |
| [Cast functions and operators](/functions-and-operators/cast-functions-and-operators.md)                 | Y            | Y            | Y            | Y            | Y            |
| [Encryption and compression functions](/functions-and-operators/encryption-and-compression-functions.md) | Y            | Y            | Y            | Y            | Y            |
| [Information functions](/functions-and-operators/information-functions.md)                               | Y            | Y            | Y            | Y            | Y            |
| [JSON functions](/functions-and-operators/json-functions.md)                                             | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Aggregation functions](/functions-and-operators/aggregate-group-by-functions.md)                        | Y            | Y            | Y            | Y            | Y            |
| [Window functions](/functions-and-operators/window-functions.md)                                         | Y            | Y            | Y            | Y            | Y            |
| [Miscellaneous functions](/functions-and-operators/miscellaneous-functions.md)                           | Y            | Y            | Y            | Y            | Y            |
| [Operators](/functions-and-operators/operators.md)                                                       | Y            | Y            | Y            | Y            | Y            |
| [Character sets and collations](/character-set-and-collation.md) [^1]                                    | Y            | Y            | Y            | Y            | Y            |

## Indexing and constraints

| Indexing and constraints                                                                                 | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Expression indexes](/sql-statements/sql-statement-create-index.md#expression-index)                     | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)                                               | Y            | Y            | Y            | Y            | Y            |
| [RocksDB engine](/storage-engine/rocksdb-overview.md)                                                    | Y            | Y            | Y            | Y            | Y            |
| [Titan plugin](/storage-engine/titan-overview.md)                                                        | Y            | Y            | Y            | Y            | Y            |
| [Invisible indexes](/sql-statements/sql-statement-add-index.md)                                          | Y            | Y            | Y            | Y            | N            |
| [Composite `PRIMARY KEY`](/constraints.md)                                                               | Y            | Y            | Y            | Y            | Y            |
| [Unique indexes](/constraints.md)                                                                        | Y            | Y            | Y            | Y            | Y            |
| [Clustered index on integer `PRIMARY KEY`](/constraints.md)                                              | Y            | Y            | Y            | Y            | Y            |
| [Clustered index on composite or non-integer key](/constraints.md)                                       | Y            | Y            | Y            | Y            | N            |

## SQL statements

| **SQL statements** [^2]                                                                                  | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| Basic `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REPLACE`                                                  | Y            | Y            | Y            | Y            | Y            |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                         | Y            | Y            | Y            | Y            | Y            |
| `LOAD DATA INFILE`                                                                                       | Y            | Y            | Y            | Y            | Y            |
| `SELECT INTO OUTFILE`                                                                                    | Y            | Y            | Y            | Y            | Y            |
| `INNER JOIN`, `LEFT\|RIGHT [OUTER] JOIN`                                                                 | Y                                                                 | Y            | Y            | Y            | Y            |
| `UNION`, `UNION ALL`                                                                                     | Y            | Y            | Y            | Y            | Y            |
| [`EXCEPT` and `INTERSECT` operators](/functions-and-operators/set-operators.md)                          | Y            | Y            | Y            | Y            | N            |
| `GROUP BY`, `ORDER BY`                                                                                   | Y            | Y            | Y            | Y            | Y            |
| [Window Functions](/functions-and-operators/window-functions.md)                                         | Y            | Y            | Y            | Y            | Y            |
| [Common Table Expressions (CTE)](/sql-statements/sql-statement-with.md)                                  | Y            | Y            | Y            | N            | N            |
| `START TRANSACTION`, `COMMIT`, `ROLLBACK`                                                                | Y            | Y            | Y            | Y            | Y            |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                                    | Y            | Y            | Y            | Y            | Y            |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                                    | Y            | Y            | Y            | Y            | Y            |
| [User-defined variables](/user-defined-variables.md)                                                     | Experimental | Experimental | Experimental | Experimental | Experimental |

## Advanced SQL features

| **Advanced SQL features**                                                                                | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Prepared statement cache](/sql-prepare-plan-cache.md)                                                   | Y            | Experimental | Experimental | Experimental | Experimental |
| [SQL plan management (SPM)](/sql-plan-management.md)                                                     | Y            | Y            | Y            | Y            | Y            |
| [Coprocessor cache](/coprocessor-cache.md)                                                               | Y            | Y            | Y            | Y            | Experimental |
| [Stale Read](/stale-read.md)                                                                             | Y            | Y            | Y            | N            | N            |
| [Follower reads](/follower-read.md)                                                                      | Y            | Y            | Y            | Y            | Y            |
| [Read historical data (tidb_snapshot)](/read-historical-data.md)                                         | Y            | Y            | Y            | Y            | Y            |
| [Optimizer hints](/optimizer-hints.md)                                                                   | Y            | Y            | Y            | Y            | Y            |
| [MPP Exection Engine](/explain-mpp.md)                                                                   | Y            | Y            | Y            | Y            | N            |
| [Index Merge Join](/explain-index-merge.md)                                                              | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Placement Rules in SQL](/placement-rules-in-sql.md)                                                     | Experimental | N            | N            | N            | N            |

## Data definition language (DDL)

| **Data definition language (DDL)**                                                                       | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| Basic `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`                                                    | Y            | Y            | Y            | Y            | Y            |
| [Generated columns](/generated-columns.md)                                                               | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Views](/views.md)                                                                                       | Y            | Y            | Y            | Y            | Y            |
| [Sequences](/sql-statements/sql-statement-create-sequence.md)                                            | Y            | Y            | Y            | Y            | Y            |
| [Auto increment](/auto-increment.md)                                                                     | Y            | Y            | Y            | Y            | Y            |
| [Auto random](/auto-random.md)                                                                           | Y            | Y            | Y            | Y            | Y            |
| [DDL algorithm assertions](/sql-statements/sql-statement-alter-table.md)                                 | Y            | Y            | Y            | Y            | Y            |
| Multi schema change: add column(s)                                                                       | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Change column type](/sql-statements/sql-statement-modify-column.md)                                     | Y            | Y            | Y            | N            | N            |
| [Temporary tables](/temporary-tables.md)                                                                 | Y            | N            | N            | N            | N            |

## Transactions

| **Transactions**                                                                                         | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Async commit](/system-variables.md#tidb_enable_async_commit-new-in-v50)                                 | Y            | Y            | Y            | Y            | N            |
| [1PC](/system-variables.md#tidb_enable_1pc-new-in-v50)                                                   | Y            | Y            | Y            | Y            | N            |
| [Large transactions (10GB)](/transaction-overview.md#transaction-size-limit)                             | Y            | Y            | Y            | Y            | Y            |
| [Pessimistic transactions](/pessimistic-transaction.md)                                                  | Y            | Y            | Y            | Y            | Y            |
| [Optimistic transactions](/optimistic-transaction.md)                                                    | Y            | Y            | Y            | Y            | Y            |
| [Repeatable-read isolation (snapshot isolation)](/transaction-isolation-levels.md)                       | Y            | Y            | Y            | Y            | Y            |
| [Read-committed isolation](/transaction-isolation-levels.md)                                             | Y            | Y            | Y            | Y            | Y            |

## Partitioning

| **Partitioning**                                                                                         | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Range partitioning](/partitioned-table.md)                                                              | Y            | Y            | Y            | Y            | Y            |
| [Hash partitioning](/partitioned-table.md)                                                               | Y            | Y            | Y            | Y            | Y            |
| [List partitioning](/partitioned-table.md)                                                               | Experimental | Experimental | Experimental | Experimental | N            |
| [List COLUMNS partitioning](/partitioned-table.md)                                                       | Experimental | Experimental | Experimental | Experimental | N            |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                                            | Experimental | Experimental | Experimental | Experimental | N            |
| [Dynamic Pruning](/partitioned-table.md#dynamic-pruning-mode)                                            | Experimental | Experimental | Experimental | N            | N            |

## Statistics

| **Statistics**                                                                                           | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [CMSketch](/statistics.md)                                                                               | Deprecated   | Deprecated   | Deprecated   | Deprecated   | Y            |
| [Histograms](/statistics.md)                                                                             | Y            | Y            | Y            | Y            | Y            |
| [Extended statistics (multiple columns)](/statistics.md)                                                 | Experimental | Experimental | Experimental | Experimental | N            |
| [Statistics Feedback](/statistics.md#automatic-update)                                                   | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Fast Analyze](/system-variables.md#tidb_enable_fast_analyze)                                            | Experimental | Experimental | Experimental | Experimental | Experimental |

## Security

| **Security**                                                                                             | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Transparent layer security (TLS)](/enable-tls-between-clients-and-servers.md)                           | Y            | Y            | Y            | Y            | Y            |
| [Encryption at rest (TDE)](/encryption-at-rest.md)                                                       | Y            | Y            | Y            | Y            | Y            |
| [Role-based authentication (RBAC)](/role-based-access-control.md)                                        | Y            | Y            | Y            | Y            | Y            |
| [Certificate-based authentication](/certificate-authentication.md)                                       | Y            | Y            | Y            | Y            | Y            |
| `caching_sha2_password` authentication                                                                   | Y            | Y            | N            | N            | N            |
| [MySQL compatible `GRANT` system](/privilege-management.md)                                              | Y            | Y            | Y            | Y            | Y            |
| [Dynamic Privileges](/privilege-management.md#dynamic-privileges)                                        | Y            | Y            | Y            | N            | N            |
| [Security Enhanced Mode](/system-variables.md#tidb_enable_enhanced_security)                             | Y            | Y            | Y            | N            | N            |
| [Redacted Log Files](/log-redaction.md)                                                                  | Y            | Y            | Y            | Y            | N            |

## Data import and export

| **Data import and export**                                                                               | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Fast Importer (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                             | Y            | Y            | Y            | Y            | Y            |
| mydumper logical dumper                                                                                  | Deprecated   | Deprecated   | Deprecated   | Deprecated   | Deprecated   |
| [Dumpling logical dumper](/dumpling-overview.md)                                                         | Y            | Y            | Y            | Y            | Y            |
| [Transactional `LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                  | Y            | Y            | Y            | Y            | N [^3]       |
| [Database migration toolkit (DM)](/migration-overview.md)                                                | Y            | Y            | Y            | Y            | Y            |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                                                      | Y    | Y    | Y    | Y    | Y    |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                                                    | Y            | Y            | Y            | Y            | Y            |

## Management, observability, and tools

| **Management, observability, and tools**                                                                  | **5.3**      | **5.2**      | **5.1**      | **5.0**      | **4.0**      |
|----------------------------------------------------------------------------------------------------------|:------------:|:------------:|:------------:|:------------:|:------------:|
| [TiDB Dashboard](/dashboard/dashboard-intro.md)                                                          | Y            | Y            | Y            | Y            | Y            |
| [SQL diagnostics](/information-schema/information-schema-sql-diagnostics.md)                             | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Information schema](/information-schema/information-schema.md)                                          | Y            | Y            | Y            | Y            | Y            |
| [Metrics schema](/metrics-schema.md)                                                                     | Y            | Y            | Y            | Y            | Y            |
| [Statements summary tables](/statement-summary-tables.md)                                                | Y            | Y            | Y            | Y            | Y            |
| [Slow query log](/identify-slow-queries.md)                                                              | Y            | Y            | Y            | Y            | Y            |
| [TiUP deployment](/tiup/tiup-overview.md)                                                                | Y            | Y            | Y            | Y            | Y            |
| Ansible deployment                                                                                       | N            | N            | N            | N            | Deprecated   |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/)                                      | Y            | Y            | Y            | Y            | Y            |
| [Built-in physical backup](/br/backup-and-restore-use-cases.md)                                          | Y            | Y            | Y            | Y            | Y            |
| Top SQL                                                                                                  | Y            | Y            | N            | N            | N            |
| [Global Kill](/sql-statements/sql-statement-kill.md)                                                     | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Lock View](/information-schema/information-schema-data-lock-waits.md)                                   | Y            | Y            | Experimental | Experimental | Experimental |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                            | Experimental | Experimental | Experimental | Experimental | Experimental |
| [`SET CONFIG`](/dynamic-config.md)                                                                       | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Continuous Profiling](/dashboard/continuous-profiling.md)                                               | Experimental | N            | N            | N            | N            |

[^1]: TiDB incorrectly treats latin1 as a subset of utf8. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.

[^2]: See [Statement Reference](/sql-statements/sql-statement-select.md) for a full list of SQL statements supported.

[^3]: For TiDB v4.0, the `LOAD DATA` transaction does not guarantee atomicity.
