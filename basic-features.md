---
title: TiDB Features
summary: Learn about the feature overview of TiDB.
aliases: ['/docs/dev/basic-features/','/tidb/dev/experimental-features-4.0/']
---

# TiDB Features

This document lists the features supported in each TiDB version.

> **Note:**
>
> - Y: the feature is generally available (GA) and can be used in production environments.
> - N: the feature is not supported.
> - Experimental: the feature is not GA yet and you need to be aware of the usage limitations. Experimental features are subject to change or removal without prior notice. The syntax and implementation might be modified before the general availability. If you encounter any problems, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Data types, functions, and operators

| Data types, functions, and operators                         | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |     5.3      |     5.2      |     5.1      |     5.0      |     4.0      |
| ------------------------------------------------------------  | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [Numeric types](/data-type-numeric.md)                      | Y  | Y  | Y  | Y | Y | Y |  Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Date and time types](/data-type-date-and-time.md)           | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [String types](/data-type-string.md)                         | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [JSON type](/data-type-json.md)                              | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Control flow functions](/functions-and-operators/control-flow-functions.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [String functions](/functions-and-operators/string-functions.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | Y | Y | Y | Y | Y | Y   | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md) | Y | Y | Y | Y | Y | Y    | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Bit functions and operators](/functions-and-operators/bit-functions-and-operators.md) | Y | Y | Y | Y | Y | Y    | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Cast functions and operators](/functions-and-operators/cast-functions-and-operators.md) | Y | Y | Y | Y | Y | Y    | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Encryption and compression functions](/functions-and-operators/encryption-and-compression-functions.md) | Y | Y | Y | Y | Y | Y    | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Information functions](/functions-and-operators/information-functions.md) | Y | Y | Y | Y | Y | Y    | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [JSON functions](/functions-and-operators/json-functions.md)  | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Aggregation functions](/functions-and-operators/aggregate-group-by-functions.md)  | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Window functions](/functions-and-operators/window-functions.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Miscellaneous functions](/functions-and-operators/miscellaneous-functions.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Operators](/functions-and-operators/operators.md)          | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Character sets and collations](/character-set-and-collation.md) [^1]  | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [User-level lock](/functions-and-operators/locking-functions.md) | Y | Y | Y | Y | Y | N | N | N | N | N | N | N |

## Indexing and constraints

| Indexing and constraints                                    | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [Expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) [^2] | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)   | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Use FastScan to accelerate queries in OLAP scenarios](/develop/dev-guide-use-fastscan.md) | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N | N | N | N |
| [RocksDB engine](/storage-engine/rocksdb-overview.md)        | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Titan plugin](/storage-engine/titan-overview.md)            | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge-experimental)   |  Experimental   |  Experimental   |  Experimental   |  Experimental    |  Experimental    |  Experimental    |    Experimental     |    Experimental     |    Experimental     |    Experimental     |    Experimental     |    Experimental     |
| [Use buckets to improve scan concurrency](/tune-region-performance.md#use-bucket-to-increase-concurrency) | Experimental | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N | N | N |
| [Invisible indexes](/sql-statements/sql-statement-add-index.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| [Composite `PRIMARY KEY`](/constraints.md)                   | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Unique indexes](/constraints.md)                            | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Clustered index on integer `PRIMARY KEY`](/constraints.md)  | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Clustered index on composite or non-integer key](/constraints.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |

## SQL statements

| SQL statements [^3]                                      | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| -------------------------------------------------------- | :--: | :--: | :--: | :--: | :--:| :--: | :--: | :--: | :--: | :----------: | :------: | :------:|
| Basic `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REPLACE`     | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `INSERT ON DUPLICATE KEY UPDATE`                             | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `LOAD DATA INFILE`                                           | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `SELECT INTO OUTFILE`                                        | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `INNER JOIN`, <code>LEFT\|RIGHT [OUTER] JOIN</code>          | Y | Y| Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `UNION`, `UNION ALL`                                         | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXCEPT` and `INTERSECT` operators](/functions-and-operators/set-operators.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| `GROUP BY`, `ORDER BY`                                       | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Window Functions](/functions-and-operators/window-functions.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Common Table Expressions (CTE)](/sql-statements/sql-statement-with.md)| Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| `START TRANSACTION`, `COMMIT`, `ROLLBACK`                    | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)        | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [User-defined variables](/user-defined-variables.md)        | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) | Y | Y | Y | Y | Y | N | N | N | N | N | N | N |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) | Y | N | N | N | N | N | N | N | N | N | N | N |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) | Y | Y | Y | Y | Experimental | N | N | N | N | N | N | N |
| [Table Lock](/tidb-configuration-file.md#enable-table-lock-new-in-v400) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [TiFlash Query Result Materialization](/tiflash/tiflash-results-materialization.md) | Experimental | N | N | N | N | N | N | N | N | N | N | N |

## Advanced SQL features

| Advanced SQL features                                    | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0   |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [Prepared statement cache](/sql-prepared-plan-cache.md)       | Y | Y | Y | Y | Y | Y | Y            |      Y       | Experimental | Experimental | Experimental | Experimental |
| [SQL plan management (SPM)](/sql-plan-management.md)         | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Create bindings according to historical execution plans](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) | Experimental | N | N | N | N | N | N | N | N | N | N | N |
| [Coprocessor cache](/coprocessor-cache.md)                   | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       | Experimental |
| [Stale Read](/stale-read.md)                                 | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| [Follower reads](/follower-read.md)                          | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Read historical data (tidb_snapshot)](/read-historical-data.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Optimizer hints](/optimizer-hints.md)                       | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [MPP Execution Engine](/explain-mpp.md)                      | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| [Index Merge](/explain-index-merge.md)                  | Y | Y | Y | Y | Y | Y | Y            | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Placement Rules in SQL](/placement-rules-in-sql.md)        | Y  | Y  | Y  | Y | Y | Y | Experimental | Experimental |      N       |      N       |      N       |      N       |
| [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |

## Data definition language (DDL)

| Data definition language (DDL)                           | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| Basic `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`        | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Generated columns](/generated-columns.md)                  | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Views](/views.md)                                          | Y  | Y  | Y  | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Sequences](/sql-statements/sql-statement-create-sequence.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Auto increment](/auto-increment.md)                         | Y | Y [^4] | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Auto random](/auto-random.md)                               | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [TTL (Time to Live)](/time-to-live.md) | Experimental | N | N | N | N | N | N | N | N | N | N | N |
| [DDL algorithm assertions](/sql-statements/sql-statement-alter-table.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| Multi-schema change: add columns                           | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Change column type](/sql-statements/sql-statement-modify-column.md) | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| [Temporary tables](/temporary-tables.md)                    | Y | Y | Y | Y | Y | Y   | Y            |      Y       |      N       |      N       |      N       |      N       |
| Concurrent DDL statements | Y | Y | Y | Y | N | N | N | N | N | N | N | N |
| [Acceleration of `ADD INDEX` and `CREATE INDEX`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) | Y | Experimental | Experimental | N | N | N | N | N | N | N | N | N |
| [Metadata lock](/metadata-lock.md) | Y | Experimental | Experimental | N | N | N | N | N | N | N | N | N |
| [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) | Y | Experimental | N | N | N | N | N | N | N | N | N | N |

## Transactions

| Transactions                                             | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4  | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :-----| ---- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [Async commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |
| [1PC](/system-variables.md#tidb_enable_1pc-new-in-v50)       | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |
| [Large transactions (10GB)](/transaction-overview.md#transaction-size-limit) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Pessimistic transactions](/pessimistic-transaction.md)      | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Optimistic transactions](/optimistic-transaction.md)        | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Repeatable-read isolation (snapshot isolation)](/transaction-isolation-levels.md) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Read-committed isolation](/transaction-isolation-levels.md) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |

## Partitioning

| Partitioning                                             | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0| 5.4          |   5.3    |   5.2    |   5.1    |   5.0    | 4.0 |
| ------------------------------------------------------------| :--:  | :--:  | :--:  | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :-----: |
| [Range partitioning](/partitioned-table.md)                  | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [Hash partitioning](/partitioned-table.md)                   | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [List partitioning](/partitioned-table.md)                   | Y | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [List COLUMNS partitioning](/partitioned-table.md)           | Y | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [Dynamic pruning](/partitioned-table.md#dynamic-pruning-mode) | Y | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental |      N       |    N    |
| [Range COLUMNS partitioning](/partitioned-table.md#range-columns-partitioning) | Y | Y | Y | N | N | N | N | N |N | N | N |      N       |    N    |
| [Range INTERVAL partitioning](/partitioned-table.md#range-interval-partitioning) | Experimental | Experimental | Experimental | N | N | N | N | N |N | N | N |      N       |    N    |

## Statistics

| Statistics                                              | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1   |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [CMSketch](/statistics.md)                                  | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Y | Y | Y |      Y       |
| [Histograms](/statistics.md)                                 | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Extended statistics](/extended-statistics.md)     | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental |      N       |
| Statistics feedback       | N | N | N | N | Deprecated | Deprecated | Deprecated   | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Automatically update statistics](/statistics.md#automatic-update) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [Fast Analyze](/system-variables.md#tidb_enable_fast_analyze) | Experimental | Experimental | Experimental | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Dynamic pruning](/partitioned-table.md#dynamic-pruning-mode) | Y | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | N | N |
| [Collect statistics for `PREDICATE COLUMNS`](/statistics.md#collect-statistics-on-some-columns) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N |
| [Control the memory quota for collecting statistics](/statistics.md#the-memory-quota-for-collecting-statistics) | Experimental | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N | N | N |
| [Randomly sample about 10000 rows of data to quickly build statistics](/system-variables.md#tidb_enable_fast_analyze) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Lock statistics](/statistics.md#lock-statistics) | Experimental | N | N | N | N | N | N | N | N | N | N | N |

## Security

| Security                                               | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4  | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ---- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [Transparent layer security (TLS)](/enable-tls-between-clients-and-servers.md) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Encryption at rest (TDE)](/encryption-at-rest.md)          | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Role-based authentication (RBAC)](/role-based-access-control.md) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Certificate-based authentication](/certificate-authentication.md) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [`caching_sha2_password` authentication](/system-variables.md#default_authentication_plugin)        | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    N    |    N    |    N    |
| [`tidb_sm3_password` authentication](/system-variables.md#default_authentication_plugin)             | Y | Y | Y | N | N | N | N | N | N |    N    |    N    |    N    |
| [`tidb_auth_token` authentication](/system-variables.md#default_authentication_plugin)             | Y | Y | N | N | N | N | N | N | N |    N    |    N    |    N    |
| [Password management](/password-management.md) | Y | N | N | N | N | N | N | N | N | N | N | N |
| [MySQL compatible `GRANT` system](/privilege-management.md)  | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Dynamic Privileges](/privilege-management.md#dynamic-privileges) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    N    |    N    |
| [Security Enhanced Mode](/system-variables.md#tidb_enable_enhanced_security) | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    N    |    N    |
| [Redacted Log Files](/log-redaction.md)                      | Y | Y | Y | Y | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |

## Data import and export

| Data import and export                                                | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4  | 5.3      | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------| :--: | :--: | :--: | :--: | :--: | :--: |:------------:|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Fast Importer (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                             | Y | Y | Y | Y | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |
| mydumper logical dumper                                                                                 | Deprecated  | Deprecated  | Deprecated  | Deprecated | Deprecated | Deprecated | Deprecated | Deprecated   | Deprecated   | Deprecated   | Deprecated   | Deprecated   |
| [Dumpling logical dumper](/dumpling-overview.md)                                                         | Y | Y | Y | Y | Y | Y | Y           | Y            | Y            | Y            | Y            | Y            |
| [Transactional `LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                 | Y | Y | Y | Y | Y | Y  | Y           | Y            | Y            | Y            | Y            | N [^5]       |
| [Database migration toolkit (DM)](/migration-overview.md)                                               | Y | Y | Y | Y | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                                                     | Y | Y | Y | Y | Y | Y  | Y   | Y    | Y    | Y    | Y    | Y    |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                                                   | Y | Y | Y | Y | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |
| [Stream data to Amazon S3, Azure Blob Storage, and NFS through TiCDC](/ticdc/ticdc-sink-to-cloud-storage.md) | Experimental | N | N | N | N | N | N | N | N | N | N | N |
| [TiCDC supports bidirectional replication between two TiDB clusters](/ticdc/ticdc-bidirectional-replication.md) | Y | N | N | N | N | N | N | N | N | N | N | N |

## Management, observability, and tools

| Management, observability, and tools                     | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | :--: | :--: | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [TiDB Dashboard UI](/dashboard/dashboard-intro.md)              | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [TiDB Dashboard Continuous Profiling](/dashboard/continuous-profiling.md)   | Y | Y | Y | Y | Y | Y | Experimental | Experimental |      N       |      N       |      N       |      N       |
| [TiDB Dashboard Top SQL](/dashboard/top-sql.md)                             | Y | Y | Y | Y | Y | Y | Experimental |      N       |      N       |      N       |      N       |      N       |
| [TiDB Dashboard SQL Diagnostics](/information-schema/information-schema-sql-diagnostics.md) | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [TiDB Dashboard Cluster Diagnostics](/dashboard/dashboard-diagnostics-access.md) | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [TiKV-FastTune dashboard](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Information schema](/information-schema/information-schema.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Metrics schema](/metrics-schema.md)                       | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Statements summary tables](/statement-summary-tables.md)    | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Slow query log](/identify-slow-queries.md)                 | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [TiUP deployment](/tiup/tiup-overview.md)                   | Y | Y | Y | Y | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Built-in physical backup](/br/backup-and-restore-use-cases.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Global Kill](/sql-statements/sql-statement-kill.md)       | Y | Y | Y | Y | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Lock View](/information-schema/information-schema-data-lock-waits.md) | Y | Y | Y | Y | Y | Y | Y            |      Y       |      Y       | Experimental | Experimental | Experimental |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| [`SET CONFIG`](/dynamic-config.md)                           | Y | Y | Y | Y | Y | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [DM WebUI](/dm/dm-webui-guide.md) | Experimental| Experimental| Experimental | Experimental| Experimental | Experimental | N | N | N | N | N | N |
| [Foreground Quota Limiter](/tikv-configuration-file.md#foreground-quota-limiter)  | Y | Y | Y | Y| Experimental | Experimental | N | N | N | N | N | N |
| [Background Quota Limiter](/tikv-configuration-file.md#background-quota-limiter) | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N | N | N | N |
| [EBS volume snapshot backup and restore](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)                        |    Y    |    Y    |    N     |    N     |    N    |    N     |    N     |    N     |    N     |    N     |    N     |  N        |
| [PITR](/br/backup-and-restore-overview.md)   |    Y    |    Y    |    Y     |    Y     |    N    |    N     |    N     |    N     |    N     |    N     |    N     |  N        |
| [Global memory control](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)   |    Y    |    Experimental    |    N     |    N     |    N    |    N     |    N     |    N     |    N     |    N     |    N     |  N        |
| [Cross-cluster RawKV replication](/tikv-configuration-file.md#api-version-new-in-v610) | Experimental | Experimental | Experimental | Experimental | N | N | N | N | N | N | N | N |
| [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | N |

[^1]: TiDB incorrectly treats latin1 as a subset of utf8. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.

[^2]: Starting from v6.5.0, the expression indexes created on the functions listed by the [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520) system variable have been tested and can be used in production environments, and more functions will be supported in the future releases. For functions not listed by this variable, the corresponding expression indexes are not recommended for use in production environments. See [expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) for details.

[^3]: See [Statement Reference](/sql-statements/sql-statement-select.md) for a full list of SQL statements supported.

[^4]: Starting from v6.4.0, TiDB supports [high-performance and globally monotonic `AUTO_INCREMENT` columns](/auto-increment.md#mysql-compatibility-mode)

[^5]: For TiDB v4.0, the `LOAD DATA` transaction does not guarantee atomicity.
