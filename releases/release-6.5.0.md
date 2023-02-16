---
title: TiDB 6.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.5.0.
---

# TiDB 6.5.0 Release Notes

Release date: December 29, 2022

TiDB version: 6.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.0#version-list)

TiDB 6.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 6.1.0, 6.5.0 not only includes new features, improvements, and bug fixes released in [6.2.0-DMR](/releases/release-6.2.0.md), [6.3.0-DMR](/releases/release-6.3.0.md), [6.4.0-DMR](/releases/release-6.4.0.md), but also introduces the following key features and improvements:

- The [index acceleration](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) feature becomes generally available (GA), which improves the performance of adding indexes by about 10 times compared with v6.1.0.
- The TiDB global memory control becomes GA, and you can control the memory consumption threshold via [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640).
- The high-performance and globally monotonic [`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) column attribute becomes GA, which is compatible with MySQL.
- [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) is now compatible with TiCDC and PITR and becomes GA.
- Enhance TiDB optimizer by making the more accurate [Cost Model version 2](/cost-model.md#cost-model-version-2) generally available and supporting expressions connected by `AND` for [INDEX MERGE](/explain-index-merge.md).
- Support pushing down the `JSON_EXTRACT()` function to TiFlash.
- Support [password management](/password-management.md) policies that meet password compliance auditing requirements.
- TiDB Lightning and Dumpling support [importing](/tidb-lightning/tidb-lightning-data-source.md) and [exporting](/dumpling-overview.md#improve-export-efficiency-through-concurrency) compressed SQL and CSV files.
- TiDB Data Migration (DM) [continuous data validation](/dm/dm-continuous-data-validation.md) becomes GA.
- TiDB Backup & Restore supports snapshot checkpoint backup, improves the recovery performance of [PITR](/br/br-pitr-guide.md#run-pitr) by 50%, and reduces the RPO in common scenarios to as short as 5 minutes.
- Improve the TiCDC throughput of [replicating data to Kafka](/replicate-data-to-kafka.md) from 4000 rows/s to 35000 rows/s, and reduce the replication latency to 2s.
- Provide row-level [Time to live (TTL)](/time-to-live.md) to manage data lifecycle (experimental).
- TiCDC supports [replicating changed logs to object storage](/ticdc/ticdc-sink-to-cloud-storage.md) such as Amazon S3, Azure Blob Storage, and NFS (experimental).

## New features

### SQL

* The performance of TiDB adding indexes is improved by about 10 times (GA) [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) @[tangenta](https://github.com/tangenta)

    TiDB v6.3.0 introduces the [Add index acceleration](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) as an experimental feature to improve the speed of backfilling when creating an index. In v6.5.0, this feature becomes GA and is enabled by default, and the performance on large tables is expected to be about 10 times faster than that in v6.1.0. The acceleration feature is suitable for scenarios where a single SQL statement adds an index serially. When multiple SQL statements add indexes in parallel, only one of the SQL statements will be accelerated.

* Provide lightweight metadata lock to improve the DML success rate during DDL change (GA) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

    TiDB v6.3.0 introduces [Metadata lock](/metadata-lock.md) as an experimental feature. To avoid the `Information schema is changed` error caused by DML statements, TiDB coordinates the priority of DMLs and DDLs during table metadata change, and makes the ongoing DDLs wait for the DMLs with old metadata to commit. In v6.5.0, this feature becomes GA and is enabled by default. It is suitable for various types of DDLs change scenarios. When you upgrade your existing cluster from versions earlier than v6.5.0 to v6.5.0 or later, TiDB automatically enables metadata lock. To disable this feature, you can set the system variable [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) to `OFF`.

    For more information, see [documentation](/metadata-lock.md).

* Support restoring a cluster to a specific point in time by using `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    Since v6.4.0, TiDB has introduced the [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) statement as an experimental feature. You can use this statement to restore a cluster to a specific point in time within the Garbage Collection (GC) life time. In v6.5.0, this feature is now compatible with TiCDC and PITR and becomes GA. This feature helps you to easily undo DML misoperations, restore the original cluster in minutes, and roll back data at different time points to determine the exact time when data changes.

    For more information, see [documentation](/sql-statements/sql-statement-flashback-to-timestamp.md).

* Fully support non-transactional DML statements including `INSERT`, `REPLACE`, `UPDATE`, and `DELETE` [#33485](https://github.com/pingcap/tidb/issues/33485) @[ekexium](https://github.com/ekexium)

    In the scenarios of large data processing, a single SQL statement with a large transaction might have a negative impact on the cluster stability and performance. A non-transactional DML statement is a DML statement split into multiple SQL statements for internal execution. The split statements compromise transaction atomicity and isolation but greatly improve the cluster stability. TiDB has supported non-transactional `DELETE` statements since v6.1.0, and non-transactional `INSERT`, `REPLACE`, and `UPDATE` statements since v6.5.0.

    For more information, see [Non-Transactional DML statements](/non-transactional-dml.md) and [`BATCH` syntax](/sql-statements/sql-statement-batch.md).

* Support time to live (TTL) (experimental) [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao)

    TTL provides row-level data lifetime management. In TiDB, a table with the TTL attribute automatically checks data lifetime and deletes expired data at the row level. TTL is designed to help you clean up unnecessary data periodically and in a timely manner without affecting the online read and write workloads.

    For more information, see [documentation](/time-to-live.md).

* Support saving TiFlash query results using the `INSERT INTO SELECT` statement (experimental) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    Starting from v6.5.0, TiDB supports pushing down the `SELECT` clause (analytical query) of the `INSERT INTO SELECT` statement to TiFlash. In this way, you can easily save the TiFlash query result to a TiDB table specified by `INSERT INTO` for further analysis, which takes effect as result caching (that is, result materialization). For example:

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    During the experimental phase, this feature is disabled by default. To enable it, you can set the [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) system variable to `ON`. There are no special restrictions on the result table specified by `INSERT INTO` for this feature, and you are free to add or not add a TiFlash replica to that result table. Typical usage scenarios of this feature include:

    - Run complex analytical queries using TiFlash
    - Reuse TiFlash query results or deal with highly concurrent online requests
    - Need a relatively small result set compared with the input data size, preferably smaller than 100 MiB.

  For more information, see [documentation](/tiflash/tiflash-results-materialization.md).

* Support binding history execution plans (experimental) [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)

    For a SQL statement, due to various factors during execution, the optimizer might occasionally choose a new execution plan instead of its previous optimal execution plan, and the SQL performance is impacted. In this case, if the optimal execution plan has not been cleared yet, it still exists in the SQL execution history.

    In v6.5.0, TiDB supports binding historical execution plans by extending the binding object in the [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) statement. When the execution plan of a SQL statement changes, you can bind the original execution plan by specifying `plan_digest` in the `CREATE [GLOBAL | SESSION] BINDING` statement to quickly recover SQL performance, as long as the original execution plan is still in the SQL execution history memory table (for example, `statements_summary`). This feature can simplify the process of handling execution plan change issues and improve your maintenance efficiency.

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan).

### Security

* Support the password complexity policy [#38928](https://github.com/pingcap/tidb/issues/38928) @[CbcWestwolf](https://github.com/CbcWestwolf)

    After this policy is enabled, when you set a password, TiDB checks the password length, whether uppercase and lowercase letters, numbers, and special characters in the password are sufficient, whether the password matches the dictionary, and whether the password matches the username. This ensures that you set a secure password.

    TiDB provides the SQL function [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength) to validate the password strength.

    For more information, see [documentation](/password-management.md#password-complexity-policy).

* Support the password expiration policy [#38936](https://github.com/pingcap/tidb/issues/38936) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB supports configuring the password expiration policy, including manual expiration, global-level automatic expiration, and account-level automatic expiration. After this policy is enabled, you must change your passwords periodically. This reduces the risk of password leakage due to long-term use and improves password security.

    For more information, see [documentation](/password-management.md#password-expiration-policy).

* Support the password reuse policy [#38937](https://github.com/pingcap/tidb/issues/38937) @[keeplearning20221](https://github.com/keeplearning20221)

    TiDB supports configuring the password reuse policy, including global-level password reuse policy and account-level password reuse policy. After this policy is enabled, you cannot use the passwords that you have used within a specified period or the most recent several passwords that you have used. This reduces the risk of password leakage due to repeated use of passwords and improves password security.

    For more information, see [documentation](/password-management.md#password-reuse-policy).

* Support failed-login tracking and temporary account locking policy [#38938](https://github.com/pingcap/tidb/issues/38938) @[lastincisor](https://github.com/lastincisor)

    After this policy is enabled, if you log in to TiDB with incorrect passwords multiple times consecutively, the account is temporarily locked. After the lock time ends, the account is automatically unlocked.

    For more information, see [documentation](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy).

### Observability

* TiDB Dashboard can be deployed on Kubernetes as an independent Pod [#1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @[SabaPing](https://github.com/SabaPing)

    TiDB v6.5.0 (and later) and TiDB Operator v1.4.0 (and later) support deploying TiDB Dashboard as an independent Pod on Kubernetes. Using TiDB Operator, you can access the IP address of this Pod to start TiDB Dashboard.

    Independently deploying TiDB Dashboard provides the following benefits:

    - The compute work of TiDB Dashboard does not pose pressure on PD nodes. This ensures more stable cluster operation.
    - The user can still access TiDB Dashboard for diagnosis even if the PD node is unavailable.
    - Accessing TiDB Dashboard on the internet does not involve the privileged interfaces of PD. Therefore, the security risk of the cluster is reduced.

  For more information, see [documentation](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently).

* Performance Overview dashboard adds TiFlash and CDC (Change Data Capture) panels [#39230](https://github.com/pingcap/tidb/issues/39230) @[dbsid](https://github.com/dbsid)

    Since v6.1.0, TiDB has introduced the Performance Overview dashboard in Grafana, which provides a system-level entry for overall performance diagnosis of TiDB, TiKV, and PD. In v6.5.0, the Performance Overview dashboard adds TiFlash and CDC panels. With these panels, starting from v6.5.0, you can use the Performance Overview dashboard to analyze the performance of all components in a TiDB cluster.

    The TiFlash and CDC panels reorganize the TiFlash and TiCDC monitoring information, which can help you greatly improve the efficiency of analyzing and troubleshooting TiFlash and TiCDC performance issues.

    - On the [TiFlash panels](/grafana-performance-overview-dashboard.md#tiflash), you can easily view the request types, latency analysis, and resource usage overview of your TiFlash cluster.
    - On the [CDC panels](/grafana-performance-overview-dashboard.md#cdc), you can easily view the health, replication latency, data flow, and downstream write latency of your TiCDC cluster.

  For more information, see [documentation](/performance-tuning-methods.md).

### Performance

* [INDEX MERGE](/glossary.md#index-merge) supports expressions connected by `AND` [#39333](https://github.com/pingcap/tidb/issues/39333) @[guo-shaoge](https://github.com/guo-shaoge) @[time-and-fate](https://github.com/time-and-fate) @[hailanwhu](https://github.com/hailanwhu)

    Before v6.5.0, TiDB only supported using index merge for the filter conditions connected by `OR`. Starting from v6.5.0, TiDB has supported using index merge for filter conditions connected by `AND` in the `WHERE` clause. In this way, the index merge of TiDB can now cover more general combinations of query filter conditions and is no longer limited to union (`OR`) relationship. The current v6.5.0 version only supports index merge under `OR` conditions as automatically selected by the optimizer. To enable index merge for `AND` conditions, you need to use the [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) hint.

    For more details about index merge, see [v5.4.0 Release Notes](/releases/release-5.4.0.md#performance) and [Explain Index Merge](/explain-index-merge.md).

* Support pushing down the following JSON functions to TiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @[yibin87](https://github.com/yibin87)

    * `->`
    * `->>`
    * `JSON_EXTRACT()`

  The JSON format provides a flexible way for application data modeling. Therefore, more and more applications are using the JSON format for data exchange and data storage. By pushing down JSON functions to TiFlash, you can improve the efficiency of analyzing data in the JSON type and use TiDB for more real-time analytics scenarios.

* Support pushing down the following string functions to TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `regexp_like`
    * `regexp_instr`
    * `regexp_substr`

* Support the global optimizer hint to interfere with the execution plan generation in [Views](/views.md) [#37887](https://github.com/pingcap/tidb/issues/37887) @[Reminiscent](https://github.com/Reminiscent)

    In some view access scenarios, you need to use optimizer hints to interfere with the execution plan of a query in the view to achieve the optimal performance. Starting from v6.5.0, TiDB supports adding global hints to query blocks in views, making the hints defined in the query effective in the view. This feature provides a way to inject hints into complex SQL statements that contain nested views, enhances the execution plan control, and stabilizes the performance of complex statements. To use global hints, you need to [name the query blocks](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint) and [specify hint references](/optimizer-hints.md#step-2-add-the-target-hints).

    For more information, see [documentation](/optimizer-hints.md#hints-that-take-effect-globally).

* Support pushing down sorting operations of [partitioned tables](/partitioned-table.md) to TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @[winoros](https://github.com/winoros)

    Although the [partitioned table](/partitioned-table.md) feature has been GA since v6.1.0, TiDB is continually improving its performance. In v6.5.0, TiDB supports pushing down sorting operations such as `ORDER BY` and `LIMIT` to TiKV for computation and filtering, which reduces network I/O overhead and improves SQL performance when you use partitioned tables.

* Optimizer introduces a more accurate Cost Model Version 2 (GA) [#35240](https://github.com/pingcap/tidb/issues/35240) @[qw4990](https://github.com/qw4990)

    TiDB v6.2.0 introduces the [Cost Model Version 2](/cost-model.md#cost-model-version-2) as an experimental feature. This model uses a more accurate cost estimation method to help the optimizer choose the optimal execution plan. Especially when TiFlash is deployed, Cost Model Version 2 automatically helps choose the appropriate storage engine and avoids much manual intervention. After real-scene testing for a period of time, this model becomes GA in v6.5.0. Starting from v6.5.0, newly created clusters use Cost Model Version 2 by default. For clusters upgrade to v6.5.0, because Cost Model Version 2 might cause changes to query plans, you can set the [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable to use the new cost model after sufficient performance testing.

    Cost Model Version 2 becomes a generally available feature that significantly improves the overall capability of the TiDB optimizer and helps TiDB evolve towards a more powerful HTAP database.

    For more information, see [documentation](/cost-model.md#cost-model-version-2).

* TiFlash optimizes the operations of getting the number of table rows [#37165](https://github.com/pingcap/tidb/issues/37165) @[elsa0520](https://github.com/elsa0520)

    In the scenarios of data analysis, It is a common operation to get the actual number of rows of a table through `COUNT(*)` without filter conditions. In v6.5.0, TiFlash optimizes the rewriting of `COUNT(*)` and automatically selects the not-null columns with the shortest column definition to count the number of rows, which can effectively reduce the number of I/O operations in TiFlash and improve the execution efficiency of getting row counts.

### Stability

* The global memory control feature is now GA [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    Since v6.4.0, TiDB has introduced global memory control as an experimental feature. In v6.5.0, it becomes GA and can track the main memory consumption. When the global memory consumption reaches the threshold defined by [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640), TiDB tries to limit the memory usage by GC or canceling SQL operations, to ensure stability.

    Note that the memory consumed by the transaction in a session (the maximum value was previously set by the configuration item [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)) is now tracked by the memory management module: when the memory consumption of a single session reaches the threshold defined by the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), the behavior defined by the system variable [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) will be triggered (the default is `CANCEL`, that is, canceling operations). To ensure forward compatibility, when [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) is configured as a non-default value, TiDB will still ensure that transactions can use the memory set by `txn-total-size-limit`.

    If you are using TiDB v6.5.0 or later, it is recommended to remove [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) and not to set a separate limit on the memory usage of transactions. Instead, use the system variables [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) and [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) to manage global memory, which can improve the efficiency of memory usage.

    For more information, see [documentation](/configure-memory-usage.md).

### Ease of use

* Refine the execution information of the TiFlash `TableFullScan` operator in the `EXPLAIN ANALYZE` output [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

    The `EXPLAIN ANALYZE` statement is used to print execution plans and runtime statistics. In v6.5.0, TiFlash has refined the execution information of the `TableFullScan` operator by adding the DMFile-related execution information. Now the TiFlash data scan status information is presented more intuitively, which helps you analyze TiFlash performance more easily.

    For more information, see [documentation](/sql-statements/sql-statement-explain-analyze.md).

* Support the output of execution plans in the JSON format [#39261](https://github.com/pingcap/tidb/issues/39261) @[fzzf678](https://github.com/fzzf678)

    In v6.5.0, TiDB extends the output format of execution plans. By specifying `FORMAT = "tidb_json"` in the `EXPLAIN` statement, you can output SQL execution plans in the JSON format. With this capability, SQL debugging tools and diagnostic tools can read execution plans more conveniently and accurately, thus improving the ease of use of SQL diagnosis and tuning.

    For more information, see [documentation](/sql-statements/sql-statement-explain.md).

### MySQL compatibility

* Support a high-performance and globally monotonic `AUTO_INCREMENT` column attribute (GA) [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    Since v6.4.0, TiDB has introduced the `AUTO_INCREMENT` MySQL compatibility mode as an experimental feature. This mode introduces a centralized auto-increment ID allocating service that ensures IDs monotonically increase on all TiDB instances. This feature makes it easier to sort query results by auto-increment IDs. In v6.5.0, this feature becomes GA. The insert TPS of a table using this feature is expected to exceed 20,000, and this feature supports elastic scaling to improve the write throughput of a single table and entire clusters. To use the MySQL compatibility mode, you need to set `AUTO_ID_CACHE` to `1` when creating a table. The following is an example:

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    For more information, see [documentation](/auto-increment.md#mysql-compatibility-mode).

### Data migration

* Support exporting and importing SQL and CSV files in gzip, snappy, and zstd compression formats [#38514](https://github.com/pingcap/tidb/issues/38514) @[lichunzhu](https://github.com/lichunzhu)

    Dumpling supports exporting data to compressed SQL and CSV files in these compression formats: gzip, snappy, and zstd. TiDB Lightning also supports importing compressed files in these formats.

    Previously, you had to provide large storage space for exporting or importing data to store CSV and SQL files, resulting in high storage costs. With the release of this feature, you can greatly reduce your storage costs by compressing the data files.

    For more information, see [documentation](/dumpling-overview.md#improve-export-efficiency-through-concurrency).

* Optimize binlog parsing capability [#924](https://github.com/pingcap/dm/issues/924) @[gmhdbjd](https://github.com/GMHDBJD)

    TiDB can filter out binlog events of the schemas and tables that are not in the migration task, thus improving the parsing efficiency and stability. This policy takes effect by default in v6.5.0. No additional configuration is required.

    Previously, even if only a few tables were migrated, the entire binlog file upstream had to be parsed. The binlog events of the tables in the binlog file that did not need to be migrated still had to be parsed, which was not efficient. Meanwhile, if these binlog events do not support parsing, the task will fail. By only parsing the binlog events of the tables in the migration task, the binlog parsing efficiency can be greatly improved and the task stability can be enhanced.

* Disk quota in TiDB Lightning is GA [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou)

    You can configure disk quota for TiDB Lightning. When there is not enough disk quota, TiDB Lightning stops reading source data and writing temporary files. Instead, it writes the sorted key-values to TiKV first, and then continues the import process after TiDB Lightning deletes the local temporary files.

    Previously, when TiDB Lightning imported data using physical mode, it would create a large number of temporary files on the local disk for encoding, sorting, and splitting the raw data. When your local disk ran out of space, TiDB Lightning would exit with an error due to failing to write to the file. With this feature, TiDB Lightning tasks can avoid overwriting the local disk.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620).

* Continuous data validation in DM is GA [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter)

    In the process of migrating incremental data from upstream to downstream databases, there is a small probability that data flow might cause errors or data loss. In scenarios where strong data consistency is required, such as credit and securities businesses, you can perform a full volume checksum on the data after migration to ensure data consistency. However, in some incremental replication scenarios, upstream and downstream writes are continuous and uninterrupted because the upstream and downstream data is constantly changing, making it difficult to perform consistency checks on all data.

    Previously, you needed to interrupt the business to validate the full data, which would affect your business. Now, with this feature, you can perform incremental data validation without interrupting the business.

    For more information, see [documentation](/dm/dm-continuous-data-validation.md).

### TiDB data share subscription

* TiCDC supports replicating changed logs to storage sinks (experimental) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu)

     TiCDC supports replicating changed logs to Amazon S3, Azure Blob Storage, NFS, and other S3-compatible storage services. Cloud storage is reasonably priced and easy to use. If you are not using Kafka, you can use storage sinks. TiCDC saves the changed logs to a file and then sends it to the storage system. From the storage system, the consumer program reads the newly generated changed log files periodically.

    The storage sink supports changed logs in the canal-json and CSV formats. For more information, see [documentation](/ticdc/ticdc-sink-to-cloud-storage.md).

* TiCDC supports bidirectional replication between two clusters [#38587](https://github.com/pingcap/tidb/issues/38587) @[xiongjiwei](https://github.com/xiongjiwei) @[asddongmen](https://github.com/asddongmen)

    TiCDC supports bidirectional replication between two TiDB clusters. If you need to build geo-distributed and multiple active data centers for your application, you can use this feature as a solution. By configuring the `bdr-mode = true` parameter for the TiCDC changefeeds from one TiDB cluster to another TiDB cluster, you can achieve bidirectional data replication between the two TiDB clusters.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC supports updating TLS online [#7908](https://github.com/pingcap/tiflow/issues/7908) @[CharlesCheung96](https://github.com/CharlesCheung96)

    To keep security of the database system, you need to set an expiration policy for the certificate used by the system. After the expiration period, the system needs a new certificate. TiCDC v6.5.0 supports online updates of TLS certificates. Without interrupting the replication tasks, TiCDC can automatically detect and update the certificate, without the need for manual intervention.

* TiCDC performance improves significantly [#7540](https://github.com/pingcap/tiflow/issues/7540) [#7478](https://github.com/pingcap/tiflow/issues/7478) [#7532](https://github.com/pingcap/tiflow/issues/7532) @[sdojjy](https://github.com/sdojjy) [@3AceShowHand](https://github.com/3AceShowHand)

    In a test scenario of the TiDB cluster, the performance of TiCDC has improved significantly. Specifically, the maximum row changes that a single TiCDC can process reaches 30K rows/s, and the replication latency is reduced to 10s. Even during TiKV and TiCDC rolling upgrade, the replication latency is less than 30s. In a disaster recovery (DR) scenario, by enabling TiCDC redo logs and Syncpoint, the TiCDC throughput of [replicating data to Kafka](/replicate-data-to-kafka.md) can be improved from 4000 rows/s to 35000 rows/s, and the replication latency can be maintained at 2s.

### Backup and restore

* TiDB Backup & Restore supports snapshot checkpoint backup [#38647](https://github.com/pingcap/tidb/issues/38647) @[Leavrth](https://github.com/Leavrth)

    TiDB snapshot backup supports resuming backup from a checkpoint. When Backup & Restore (BR) encounters a recoverable error, it retries backup. However, BR exits if the retry fails for several times. The checkpoint backup feature allows for longer recoverable failures to be retried, for example, a network failure of tens of minutes.

    Note that if you do not recover the system from a failure within one hour after BR exits, the snapshot data to be backed up might be recycled by the GC mechanism, causing the backup to fail. For more information, see [documentation](/br/br-checkpoint.md).

* PITR performance improved remarkably [@joccau](https://github.com/joccau)

    In the log restore stage, the restore speed of one TiKV can reach 9 MiB/s, which is 50% faster than before. The restore speed is scalable and the RTO in DR scenarios is reduced greatly. The RPO in DR scenarios can be as short as 5 minutes. In normal cluster operation and maintenance (OM), for example, a rolling upgrade is performed or only one TiKV is down, the RPO can be 5 minutes.

* TiKV-BR GA: Supports backing up and restoring RawKV [#67](https://github.com/tikv/migration/issues/67) @[pingyu](https://github.com/pingyu) @[haojinming](https://github.com/haojinming)

    TiKV-BR is a backup and restore tool used in TiKV clusters. TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. TiKV-BR supports data backup and restore for products that use RawKV. TiKV-BR can also upgrade the [`api-version`](/tikv-configuration-file.md#api-version-new-in-v610) from `API V1` to `API V2` for TiKV cluster.

    For more information, see [documentation](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/).

## Compatibility changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|`tidb_enable_amend_pessimistic_txn`| Deprecated | Starting from v6.5.0, this variable is deprecated, and TiDB uses the [Metadata Lock](/metadata-lock.md) feature by default to avoid the `Information schema is changed` error. |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the support of Outer Join for the [Join Reorder](/join-reorder.md) algorithm is enabled by default. |
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) | Modified | Changes the default value from `1` to `2` after further tests, meaning that Cost Model Version 2 is used for index selection and operator selection by default.  |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track)  |  Modified |   Changes the default value from `ON` to `OFF`. Because the GC-aware memory track is found inaccurate in tests and causes too large analyzed memory size tracked, the memory track is disabled. In addition, in Golang 1.19, the memory tracked by the GC-aware memory track does not have much impact on the overall memory.  |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the metadata lock feature is enabled by default. |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) | Modified | Takes effect starting from v6.5.0. It controls whether read operations in SQL statements containing `INSERT`, `DELETE`, and `UPDATE` can be pushed down to TiFlash. The default value is `OFF`. |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the acceleration of `ADD INDEX` and `CREATE INDEX` is enabled by default. |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) | Modified | For versions earlier than TiDB v6.5.0, this variable is used to set the threshold value of memory quota for a query. For TiDB v6.5.0 and later versions, to control the memory of DML statements more accurately, this variable is used to set the threshold value of memory quota for a session.  |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) | Modified | Starting from v6.5.0, to optimize load balancing across TiDB nodes, when this variable is set to`closest-adaptive` and the estimated result of a read request is greater than or equal to [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630), the number of TiDB nodes whose `closest-adaptive` configuration takes effect is limited in each availability zone, which is always the same as the number of TiDB nodes in the availability zone with the fewest TiDB nodes, and the other TiDB nodes automatically read from the leader replica. |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) | Modified | Changes the default value from `0` to `80%`. As the TiDB global memory control becomes GA, this default value change enables the memory control by default and sets the memory limit for a TiDB instance to 80% of the total memory by default. |
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650) | Newly added | Sets the global policy for automatic password expiration to require users to change passwords periodically. The default value `0` indicates that passwords never expire. |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650) | Newly added | Indicates whether TiDB disconnects the client connection when the password is expired. This variable is read-only. |
| [`password_history`](/system-variables.md#password_history-new-in-v650) | Newly added | This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on the number of password changes. The default value `0` means disabling the password reuse policy based on the number of password changes. |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650) | Newly added | This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on time elapsed. The default value `0` means disabling the password reuse policy based on time elapsed. |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650) | Newly added | This variable is used to set the concurrency of executing the automatic update of statistics. The default value is `1`.  |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650) | Newly added | When this variable is set to a value other than 0, data written in this session is considered to be written by TiCDC. This variable can only be modified by TiCDC. Do not manually modify this variable in any case. |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | Newly added | Sets the maximum concurrency for the intersection operations that index merge performs. It is effective only when TiDB accesses partitioned tables in the dynamic pruning mode. |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-new-in-v650) | Newly added | This variable is used to configure the different cluster IDs in a [bi-directional replication](/ticdc/ticdc-bidirectional-replication.md) cluster.|
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650) | Newly added | This variable is used to set the concurrency of scan operations performed when TiDB executes internal SQL statements (such as an automatic update of statistics). The default value is `1`. |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650) | Newly added | This variable is used to set the maximum number of rows that can be deleted in a single `DELETE` transaction in a TTL job. |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650) | Newly added | This variable is used to limit the maximum number of `DELETE` statements allowed per second in a single node in a TTL job. When this variable is set to `0`, no limit is applied. |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650) | Newly added | This variable is used to set the maximum concurrency of TTL jobs on each TiDB node. |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) | Newly added | This variable is used to control whether to enable TTL jobs. If it is set to `OFF`, all tables with TTL attributes automatically stop cleaning up expired data. |
| `tidb_ttl_job_run_interval` | Newly added | This variable is used to control the scheduling interval of the TTL job in the background. For example, if the current value is set to `1h0m0s`, each table with TTL attributes will clean up expired data once every hour. |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650) | Newly added | This variable is used to control the start time of the scheduling window of the TTL job in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650) | Newly added | This variable is used to control the end time of the scheduling window of the TTL job in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650) | Newly added | This variable is used to set the `LIMIT` value of each `SELECT` statement used to scan expired data in a TTL job. |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650) | Newly added | This variable is used to set the maximum concurrency of TTL scan jobs on each TiDB node. |
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password matches the username. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled. The default value is `ON`. |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password matches any word in the dictionary. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `2` (STRONG). The default value is `""`. |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) | Newly added | This variable controls whether to perform password complexity check. If this variable is set to `ON`, TiDB performs the password complexity check when you set a password. The default value is `OFF`. |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password length is sufficient. By default, the minimum password length is `8`. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled. |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient uppercase and lowercase letters. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient numbers. This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) | Newly added | This variable controls the policy for the password complexity check. The value can be `0`, `1`, or `2` (corresponds to LOW, MEDIUM, or STRONG). This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled. The default value is `1`. |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient special characters. This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409) | Deprecated | Starting from v6.5.0, this configuration item is deprecated. Instead, use the system variable [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) to manage memory globally. |
| TiDB | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | Newly added | Determines whether TiDB disconnects the client connection when the password is expired. The default value is `true`, which means the client connection is disconnected when the password is expired. |
| TiKV | `raw-min-ts-outlier-threshold` | Deleted | This configuration item was deprecated in v6.4.0 and deleted in v6.5.0. |
| TiKV | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)  | Modified | To reduce CDC latency, the default value is changed from `1s` to `200ms`. |
| TiKV | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-new-in-v650) | Newly added | Indicates the ratio of available memory to total system memory in PITR log recovery. |
| TiCDC | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Indicates the row terminator, which is used for separating two data change events. The value is empty by default, which means `\r\n` is used. |
| TiCDC | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Indicates the date separator type of the file directory. Value options are `none`, `year`, `month`, and `day`. `none` is the default value and means that the date is not separated. |
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Specifies whether to use partitions as the separation string. The default value is `false`, which means that partitions in a table are not stored in separate directories. |
| TiCDC | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Indicates the delimiter between fields. The value must be an ASCII character and defaults to `,`. |
| TiCDC | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | The quotation that surrounds the fields. The default value is `"`. When the value is empty, no quotation is used. |
| TiCDC | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Specifies the character displayed when the CSV column is null. The default value is `\N`.|
| TiCDC | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added| Specifies whether to include commit-ts in CSV rows. The default value is `false`. |

### Others

- Starting from v6.5.0, the `mysql.user` table adds two new columns: `Password_reuse_history` and `Password_reuse_time`.
- Starting from v6.5.0, the [index acceleration](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) feature is enabled by default. This feature is not fully compatible with [altering multiple columns or indexes in a single `ALTER TABLE` statement](/sql-statements/sql-statement-alter-table.md). When adding a unique index with the index acceleration, you need to avoid altering other columns or indexes in the same statement. This feature is incompatible with [PITR (Point-in-time recovery)](/br/br-pitr-guide.md) either. When using the index acceleration feature, you need to make sure that no PITR backup task is running in the background; otherwise, unexpected results might occur. For more information, see [documentation](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630).

## Deprecated feature

Starting from v6.5.0, the `AMEND TRANSACTION` mechanism introduced in v4.0.7 is deprecated and replaced by [Metadata Lock](/metadata-lock.md).

## Improvements

+ TiDB

    - For `BIT` and `CHAR` columns, make the result of `INFORMATION_SCHEMA.COLUMNS` consistent with MySQL [#25472](https://github.com/pingcap/tidb/issues/25472) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the TiDB probing mechanism for TiFlash nodes in the TiFlash MPP mode to mitigate the performance impact when nodes are abnormal [#39686](https://github.com/pingcap/tidb/issues/39686) @[hackersean](https://github.com/hackersean)

+ TiKV

    - Stop writing to Raft Engine when there is insufficient space to avoid exhausting disk space [#13642](https://github.com/tikv/tikv/issues/13642) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - Support pushing down the `json_valid` function to TiKV [#13571](https://github.com/tikv/tikv/issues/13571) @[lizhenhuan](https://github.com/lizhenhuan)
    - Support backing up multiple ranges of data in a single backup request [#13701](https://github.com/tikv/tikv/issues/13701) @[Leavrth](https://github.com/Leavrth)
    - Support backing up data to the Asia Pacific region (ap-southeast-3) of AWS by updating the rusoto library [#13751](https://github.com/tikv/tikv/issues/13751) @[3pointer](https://github.com/3pointer)
    - Reduce pessimistic transaction conflicts [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)
    - Improve recovery performance by caching external storage objects [#13798](https://github.com/tikv/tikv/issues/13798) @[YuJuncen](https://github.com/YuJuncen)
    - Run the CheckLeader in a dedicated thread to reduce TiCDC replication latency [#13774](https://github.com/tikv/tikv/issues/13774) @[overvenus](https://github.com/overvenus)
    - Support pull model for Checkpoints [#13824](https://github.com/tikv/tikv/issues/13824) @[YuJuncen](https://github.com/YuJuncen)
    - Avoid spinning issues on the sender side by updating crossbeam-channel [#13815](https://github.com/tikv/tikv/issues/13815) @[sticnarf](https://github.com/sticnarf)
    - Support batch Coprocessor tasks processing in TiKV [#13849](https://github.com/tikv/tikv/issues/13849) @[cfzjywxk](https://github.com/cfzjywxk)
    - Reduce waiting time on failure recovery by notifying TiKV to wake up Regions [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)
    - Reduce the requested size of memory usage by code optimization [#13827](https://github.com/tikv/tikv/issues/13827) @[BusyJay](https://github.com/BusyJay)
    - Introduce the Raft extension to improve code extensibility [#13827](https://github.com/tikv/tikv/issues/13827) @[BusyJay](https://github.com/BusyJay)
    - Support using tikv-ctl to query which Regions are included in a certain key range [#13760](https://github.com/tikv/tikv/issues/13760) [@HuSharp](https://github.com/HuSharp)
    - Improve read and write performance for rows that are not updated but locked continuously [#13694](https://github.com/tikv/tikv/issues/13694) [@sticnarf](https://github.com/sticnarf)

+ PD

    - Optimize the granularity of locks to reduce lock contention and improve the handling capability of heartbeats under high concurrency [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)
    - Optimize scheduler performance for large-scale clusters and accelerate the production of scheduling policies [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    - Improve the speed of loading Regions [#5606](https://github.com/tikv/pd/issues/5606) @[rleungx](https://github.com/rleungx)
    - Reduce unnecessary overhead by optimized handling of Region heartbeats [#5648](https://github.com/tikv/pd/issues/5648) @[rleungx](https://github.com/rleungx)
    - Add the feature of automatically garbage collecting tombstone stores [#5348](https://github.com/tikv/pd/issues/5348) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Improve write performance in scenarios where there is no batch processing on the SQL side [#6404](https://github.com/pingcap/tiflash/issues/6404) @[lidezhu](https://github.com/lidezhu)
    - Add more details for TableFullScan in the `explain analyze` output [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + TiDB Dashboard

        - Add three new fields to the slow query page: "Is Prepared?", "Is Plan from Cache?", "Is Plan from Binding?" [#1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @[shhdgit](https://github.com/shhdgit)

    + Backup & Restore (BR)

        - Optimize BR memory usage during the process of cleaning backup log data [#38869](https://github.com/pingcap/tidb/issues/38869) @[Leavrth](https://github.com/Leavrth)
        - Fix the restoration failure issue caused by PD leader switch during the restoration process [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - Improve TLS compatibility by using the OpenSSL protocol in log backup [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Improve the performance of Kafka protocol encoder [#7540](https://github.com/pingcap/tiflow/issues/7540) [#7532](https://github.com/pingcap/tiflow/issues/7532) [#7543](https://github.com/pingcap/tiflow/issues/7543) @[3AceShowHand](https://github.com/3AceShowHand) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - Improve the data replication performance for DM by not parsing the data of tables in the block list [#7622](https://github.com/pingcap/tiflow/pull/7622) @[GMHDBJD](https://github.com/GMHDBJD)
        - Improve the write efficiency of DM relay by using asynchronous write and batch write [#7580](https://github.com/pingcap/tiflow/pull/7580) @[GMHDBJD](https://github.com/GMHDBJD)
        - Optimize the error messages in DM precheck [#7621](https://github.com/pingcap/tiflow/issues/7621) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Improve the compatibility of `SHOW SLAVE HOSTS` for old MySQL versions [#5017](https://github.com/pingcap/tiflow/issues/5017) @[lyzx2001](https://github.com/lyzx2001)

## Bug fixes

+ TiDB

    - Fix the issue of memory chunk misuse for the chunk reuse feature that occurs in some cases [#38917](https://github.com/pingcap/tidb/issues/38917) @[keeplearning20221](https://github.com/keeplearning20221)
    - Fix the issue that the internal sessions of `tidb_constraint_check_in_place_pessimistic` might be affected by the global setting [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - Fix the issue that the `AUTO_INCREMENT` column cannot work with the `CHECK` constraint [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that using `INSERT IGNORE INTO` to insert data of the `STRING` type into an auto-increment column of the `SMALLINT` type will cause an error [#38483](https://github.com/pingcap/tidb/issues/38483) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the null pointer error occurs in the operation of renaming the partition column of a partitioned table [#38932](https://github.com/pingcap/tidb/issues/38932) @[mjonss](https://github.com/mjonss)
    - Fix the issue that modifying the partition column of a partitioned table causes DDL to hang [#38530](https://github.com/pingcap/tidb/issues/38530) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `ADMIN SHOW JOB` operation panics after upgrading from v4.0.16 to v6.4.0 [#38980](https://github.com/pingcap/tidb/issues/38980) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `tidb_decode_key` function fails to correctly parse the encoding of partitioned tables [#39304](https://github.com/pingcap/tidb/issues/39304) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that gRPC error logs are not redirected to the correct log file during log rotation [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - Fix the issue that TiDB generates an unexpected execution plan for the `BEGIN; SELECT... FOR UPDATE;` point query when TiKV is not configured as a read engine [#39344](https://github.com/pingcap/tidb/issues/39344) @[Yisaer](https://github.com/Yisaer)
    - Fix the issue that mistakenly pushing down `StreamAgg` to TiFlash causes wrong results [#39266](https://github.com/pingcap/tidb/issues/39266) @[fixdb](https://github.com/fixdb)

+ TiKV

    - Fix an error in Raft Engine ctl [#11119](https://github.com/tikv/tikv/issues/11119) @[tabokie](https://github.com/tabokie)
    - Fix the `Get raft db is not allowed` error when executing the `compact raft` command in tikv-ctl [#13515](https://github.com/tikv/tikv/issues/13515) @[guoxiangCN](https://github.com/guoxiangCN)
    - Fix the issue that log backup does not work when TLS is enabled [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the support issue of the Geometry field type [#13651](https://github.com/tikv/tikv/issues/13651) @[dveeden](https://github.com/dveeden)
    - Fix the issue that `_` in the `LIKE` operator cannot match non-ASCII characters when new collation is not enabled [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that tikv-ctl is terminated unexpectedly when executing the `reset-to-version` command [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)

+ PD

    - Fix the issue that the `balance-hot-region-scheduler` configuration is not persisted if not modified [#5701](https://github.com/tikv/pd/issues/5701) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that `rank-formula-version` does not retain the pre-upgrade configuration during the upgrade process [#5698](https://github.com/tikv/pd/issues/5698) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - Fix the issue that column files in the delta layer cannot be compacted after restarting TiFlash [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that TiFlash File Open OPS is too high [#6345](https://github.com/pingcap/tiflash/issues/6345) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that when BR deletes log backup data, it mistakenly deletes data that should not be deleted [#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that restore tasks fail when using old framework for collations in databases or tables [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)
        - Fix the issue that backup fails because Alibaba Cloud and Huawei Cloud are not fully compatible with Amazon S3 storage [#39545](https://github.com/pingcap/tidb/issues/39545) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that TiCDC gets stuck when the PD leader crashes [#7470](https://github.com/pingcap/tiflow/issues/7470) @[zeminzhou](https://github.com/zeminzhou)
        - Fix data loss occurred in the scenario of executing DDL statements first and then pausing and resuming the changefeed [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC mistakenly reports an error when there is a later version of TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - Fix the issue that the sink component gets stuck if the downstream network is unavailable [#7706](https://github.com/pingcap/tiflow/issues/7706) @[hicqu](https://github.com/hicqu)
        - Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix the issue that a `task-mode:all` task cannot be started when the upstream database enables the GTID mode but does not have any data [#7037](https://github.com/pingcap/tiflow/issues/7037) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that data is replicated for multiple times when a new DM worker is scheduled before the existing worker exits [#7658](https://github.com/pingcap/tiflow/issues/7658) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM precheck is not passed when the upstream database uses regular expressions to grant privileges [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the memory leakage issue when TiDB Lightning imports a huge source data file [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that TiDB Lightning cannot detect conflicts correctly when importing data in parallel [#39476](https://github.com/pingcap/tidb/issues/39476) @[dsdashun](https://github.com/dsdashun)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [e1ijah1](https://github.com/e1ijah1)
- [guoxiangCN](https://github.com/guoxiangCN) (First-time contributor)
- [jiayang-zheng](https://github.com/jiayang-zheng)
- [jiyfhust](https://github.com/jiyfhust)
- [mikechengwei](https://github.com/mikechengwei)
- [pingandb](https://github.com/pingandb)
- [sashashura](https://github.com/sashashura)
- [sourcelliu](https://github.com/sourcelliu)
- [wxbty](https://github.com/wxbty)
