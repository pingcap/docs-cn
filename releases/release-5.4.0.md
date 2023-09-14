---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 Release Notes

Release date: February 15, 2022

TiDB version: 5.4.0

In v5.4, the key new features or improvements are as follows:

- Support the GBK character set
- Support using Index Merge to access data, which merges the filtering results of indexes on multiple columns
- Support reading stale data using a session variable
- Support persisting the configuration for collecting statistics
- Support using Raft Engine as the log storage engine of TiKV (experimental)
- Optimize the impact of backup on the cluster
- Support using Azure Blob storage as the backup storage
- Continuously improve the stability and performance of TiFlash and the MPP engine
- Add a switch in TiDB Lightning to determine whether to allow importing to an existing table with data
- Optimize the Continuous Profiling feature (experimental)
- TiSpark supports user identification and authentication

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v5.4.0, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/releases/release-notes.md) of the corresponding version.

### System variables

<table>
<thead>
  <tr>
    <th>Variable name</th>
    <th>Change type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_column_tracking-new-in-v540"><code>tidb_enable_column_tracking</code></a></td>
    <td>Newly added</td>
    <td>Controls whether to allow TiDB to collect <code>PREDICATE COLUMNS</code>. The default value is <code>OFF.</code></td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_paging-new-in-v540"><code>tidb_enable_paging</code></a></td>
    <td>Newly added</td>
    <td>Controls whether to use the method of paging to send coprocessor requests in <code>IndexLookUp</code> operator. The default value is <code>OFF</code>.<br/>For read queries that use <code>IndexLookup</code> and <code>Limit</code> and that <code>Limit</code> cannot be pushed down to <code>IndexScan</code>, there might be high latency for the read queries and high CPU usage for TiKV's <code>unified read pool</code>. In such cases, because the <code>Limit</code> operator only requires a small set of data, if you set <code>tidb_enable_paging</code> to <code>ON</code>, TiDB processes less data, which reduces query latency and resource consumption.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_top_sql-new-in-v540"><code>tidb_enable_top_sql</code></a></td>
    <td>Newly added</td>
    <td>Controls whether to enable the Top SQL feature. The default value is <code>OFF</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_persist_analyze_options-new-in-v540"><code>tidb_persist_analyze_options</code></a></td>
    <td>Newly added</td>
    <td>Controls whether to enable the <a href="https://docs.pingcap.com/tidb/dev/statistics#persist-analyze-configurations">ANALYZE configuration persistence</a> feature. The default value is <code>ON</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_read_staleness-new-in-v540"><code>tidb_read_staleness</code></a></td>
    <td>Newly added</td>
    <td>Controls the range of historical data that can be read in the current session. The default value is <code>0</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_regard_null_as_point-new-in-v540"><code>tidb_regard_null_as_point</code></a></td>
    <td>Newly added</td>
    <td>Controls whether the optimizer can use a query condition including null equivalence as a prefix condition for index access.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_sync_wait-new-in-v540"><code>tidb_stats_load_sync_wait</code></a></td>
    <td>Newly added</td>
    <td>Controls whether to enable the synchronously loading statistics feature. The default value <code>0</code> means that the feature is disabled and that the statistics is asynchronously loaded. When the feature is enabled, this variable controls the maximum time that SQL optimization can wait for synchronously loading statistics before timeout.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_pseudo_timeout-new-in-v540"><code>tidb_stats_load_pseudo_timeout</code></a></td>
    <td>Newly added</td>
    <td>Controls when synchronously loading statistics reaches timeout, whether SQL fails (<code>OFF</code>) or falls back to using pseudo statistics (<code>ON</code>). The default value is <code>OFF</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_backoff_lock_fast"><code>tidb_backoff_lock_fast</code></a></td>
    <td>Modified</td>
    <td>The default value is changed from <code>100</code> to <code>10</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_index_merge-new-in-v40"><code>tidb_enable_index_merge</code></a></td>
    <td>Modified</td>
    <td>The default value is changed from <code>OFF</code> to <code>ON</code>.<ul><li>If you upgrade a TiDB cluster from versions earlier than v4.0.0 to v5.4.0 or later, this variable is <code>OFF</code> by default.</li><li>If you upgrade a TiDB cluster from v4.0.0 or later to v5.4.0 or later, this variable remains the same as before the upgrade.</li><li>For the newly created TiDB clusters of v5.4.0 and later, this variable is <code>ON</code> by default.</li></ul></td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_store_limit-new-in-v304-and-v40"><code>tidb_store_limit</code></a></td>
    <td>Modified</td>
    <td>Before v5.4.0, this variable can be configured at instance level and globally. Starting from v5.4.0, this variable only supports global configuration.</td>
  </tr>
</tbody>
</table>

### Configuration file parameters

|  Configuration file    |  Configuration |  Change type  | Description    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) | Newly added |  Controls the maximum number of columns that the TiDB synchronously loading statistics feature can process concurrently. The default value is `5`.  |
| TiDB | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)   | Newly added |  Controls the maximum number of column requests that the TiDB synchronously loading statistics feature can cache. The default value is`1000`.  |
| TiKV | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540) | Newly added | The size of the `snap-generator` thread pool. The default value is `2`. |
| TiKV | `log.file.max-size`, `log.file.max-days`, `log.file.max-backups` | Newly added  | For details, see [TiKV Configuration File - `log.file`](/tikv-configuration-file.md#logfile-new-in-v540). |
| TiKV | `raft-engine` | Newly added | Includes `enable`, `dir`, `batch-compression-threshold`, `bytes-per-sync`, `target-file-size`, `purge-threshold`, `recovery-mode`, `recovery-read-block-size`, `recovery-read-block-size`, and `recovery-threads`. For details, see [TiKV Configuration File - `raft-engine`](/tikv-configuration-file.md#raft-engine).|
| TiKV | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) | Newly added | In v5.3.0, the default value is `false`. Since v5.4.0, the default value is changed to `true`. This parameter controls whether to limit the resources used by backup tasks to reduce the impact on the cluster when the cluster resource utilization is high. In the default configuration, the speed of backup tasks might slow down. |
| TiKV | `log-level`, `log-format`, `log-file`, `log-rotation-size` | Modified | The names of TiKV log parameters are replaced with the names that are consistent with TiDB log parameters, which are `log.level`, `log.format`, `log.file.filename`, and `log.enable-timestamp`. If you only set the old parameters, and their values are set to non-default values, the old parameters remain compatible with the new parameters. If both old and new parameters are set, the new parameters take effect. For details, see [TiKV Configuration File - log](/tikv-configuration-file.md#log-new-in-v540). |
| TiKV  |  `log-rotation-timespan`  | Deleted |  The timespan between log rotations. After this timespan passes, a log file is rotated, which means a timestamp is appended to the file name of the current log file, and a new log file is created. |
| TiKV | `allow-remove-leader` | Deleted  | Determines whether to allow deleting the main switch. |
| TiKV | `raft-msg-flush-interval` | Deleted | Determines the interval at which Raft messages are sent in batches. The Raft messages are sent in batches at every interval specified by this configuration item. |
| PD | [`log.level`](/pd-configuration-file.md#level) | Modified | The default value is changed from "INFO" to "info", guaranteed to be case-insensitive. |
| TiFlash | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added  |  Determines whether to enable or disable the elastic thread pool function. Enabling this configuration item can significantly improve TiFlash CPU utilization in high concurrency scenarios. The default value is `false`. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | Specifies the version of DTFile. The default value is `2`, under which hashes are embedded in the data file. You can also set the value to `3`. When it is `3`, the data file contains metadata and token data checksum, and supports multiple hash algorithms. |
| TiFlash | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | The default value is changed to `10`. |
| TiFlash | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | The default value is changed to `8234`. |
| TiFlash | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Newly added | The allowable number of threads in the pool that flushes Raft data to storage. The default value is `4`. |
| TiFlash | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Newly added | The allowable number of threads that process Raft, which is the size of the Raftstore thread pool. The default value is `4`. |
| TiDB Data Migration (DM)  | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | The mode to sync the default collation in `CREATE` SQL statements. The value options are "loose" (by default) and "strict".  |
| TiCDC | `max-message-bytes` | Modified| Change the default value of `max-message-bytes` in Kafka sink to `104857601` (10MB)  |
| TiCDC | `partition-num`     | Modified | Change the default value of `partition-num` in Kafka Sink from `4` to `3`. It makes TiCDC send messages to Kafaka partitions more evenly. |
| TiDB Lightning | `meta-schema-name` | Modified | Specifies the schema name for the metadata in the target TiDB. From v5.4.0, this schema is created only if you have enabled [parallel import](/tidb-lightning/tidb-lightning-distributed-import.md) (the corresponding parameter is `tikv-importer.incremental-import = true`). |
| TiDB Lightning | `task-info-schema-name` |  Newly added  | Specifies the name of the database where duplicated data is stored when TiDB Lightning detects conflicts. By default, the value is "lightning_task_info". Specify this parameter only if you have enabled the "duplicate-resolution" feature. |
| TiDB Lightning | `incremental-import` | Newly added | Determines whether to allow importing data to tables where data already exists. The default value is `false`. |

### Others

- An interface is added between TiDB and PD. When you use the `information_schema.TIDB_HOT_REGIONS_HISTORY` system table, TiDB needs to use PD in the corresponding version.
- TiDB Server, PD Server, and TiKV Server start using a unified naming method for the log-related parameters to manage log names, output formats, and the rules for rotation and expiration. For details, see [TiKV configuration file - log](/tikv-configuration-file.md#log-new-in-v540).
- Since v5.4.0, if you create a SQL binding for an execution plan that has been cached via Plan Cache, the binding invalidates the plan already cached for the corresponding query. The new binding does not affect execution plans cached before v5.4.0.
- In v5.3 and earlier versions, [TiDB Data Migration (DM)](https://docs.pingcap.com/tidb-data-migration/v5.3/) documentation is independent of TiDB documentation. Since v5.4, DM documentation is integrated into TiDB documentation with the same version. You can directly read [DM documentation](/dm/dm-overview.md) without accessing the DM documentation site.
- Remove the experimental feature of Point-in-time recovery (PITR) along with cdclog. Since v5.4.0, cdclog-based PITR and cdclog are no longer supported.
- Make the behavior of setting system variables to the "DEFAULT" more MySQL-compatible [#29680](https://github.com/pingcap/tidb/pull/29680)
- Set the system variable `lc_time_names` to read-only [#30084](https://github.com/pingcap/tidb/pull/30084)
- Set the scope of `tidb_store_limit` from INSTANCE or GLOBAL to GLOBAL [#30756](https://github.com/pingcap/tidb/pull/30756)
- Forbid converting the integer type column to the time type column when the column contains zero [#25728](https://github.com/pingcap/tidb/pull/25728)
- Fix the issue that no error is reported for the `Inf` or `NAN` value when inserting floating-point values [#30148](https://github.com/pingcap/tidb/pull/30148)
- Fix the issue that the `REPLACE` statement incorrectly changes other rows when the auto ID is out of range [#30301](https://github.com/pingcap/tidb/pull/30301)

## New features

### SQL

- **TiDB supports the GBK character set since v5.4.0**

    Before v5.4.0, TiDB supports `ascii`, `binary`, `latin1`, `utf8`, and `utf8mb4` character sets.

    To better support Chinese users, TiDB supports the GBK character set since v5.4.0. After enabling the [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) option in the TiDB configuration file when initializing a TiDB cluster for the first time, the TiDB GBK character set supports both `gbk_bin` and `gbk_chinese_ci` collations.

    When using the GBK character set, you need to pay attention to the compatibility restrictions. For details, see [Character Set and Collation - GBK](/character-set-gbk.md).

### Security

- **TiSpark supports user authentication and authorization**

    Since TiSpark 2.5.0, TiSpark supports both database user authentication and read/write authorization at a database or table level. After enabling this feature, you can prevent the business from running unauthorized batch tasks such as draws to obtain data, which improves the stability and data security of online clusters.

    This feature is disabled by default. When it is enabled, if a user operating through TiSpark does not have the needed permissions, the user gets an exception from TiSpark.

    [User document](/tispark-overview.md#security)

- **TiUP supports generating an initial password for the root user**

    An `--init` parameter is introduced to the command for starting a cluster. With this parameter, in a TiDB cluster deployed using TiUP, TiUP generates an initial strong password for the database root user. This avoids security risks in using a root user with an empty password and ensures the security of databases.

    [User document](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### Performance

- **Continue improving the stability and performance of the columnar storage engine TiFlash and the computing engine MPP**

    - Support pusing down more functions to the MPP engine:

        - String functions: `LPAD()`, `RPAD()`, `STRCMP()`
        - Date functions: `ADDDATE(string, real)`, `DATE_ADD(string, real)`, `DATE_SUB(string, real)`, `SUBDATE(string, real)`, `QUARTER()`

    - Introduce the elastic thread pool feature to improve resource utilization (experimental)
    - Improve the efficiency of converting data from row-based storage format to column-based storage format when replicating data from TiKV, which brings 50% improvement in the overall performance of data replication
    - Improve TiFlash performance and stability by tuning the default values of some configuration items. In an HTAP hybrid load, the performance of simple queries on a single table improves up to 20%.

    User documents: [Supported push-down calculations](/tiflash/tiflash-supported-pushdown-calculations.md), [Configure the tiflash.toml file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

- **Read historical data within a specified time range through a session variable**

    TiDB is a multi-replica distributed database based on the Raft consensus algorithm. In face of high-concurrency and high-throughput application scenarios, TiDB can scale out its read performance through follower replicas, separating read and write requests.

    For different application scenarios, TiDB provides two modes of follower read: strongly consistent read and weakly consistent history read. The strongly consistent read mode is suitable for application scenarios that require real-time data. However, in this mode, because of the data replication latency between leaders and followers and the reduced throughput, the read request might have high latency, especially for geo-distributed deployments.

    For the application scenarios that have less strict requirements on real-time data, the history read mode is recommended. This mode can reduce latency and improve throughput. TiDB currently supports reading historical data by the following methods: Use SQL statements to read data from a time point in the past, or start a read-only transaction based on a time point in the past. Both methods support reading the historical data of a specific point in time or within a specified time range. For details, refer to [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md).

    Since v5.4.0, TiDB improves the usability of the history read mode by supporting reading historical data within a specified time range through a session variable. This mode serves low-latency, high-throughput read requests in quasi-real-time scenarios. You can set the variable as follows:

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    By this setting, TiDB can select the nearest leader or follower node and read the latest historical data within 5 seconds.

    [User document](/tidb-read-staleness.md)

- **GA for Index Merge**

    Index Merge is introduced in TiDB v4.0 as an experimental feature for SQL optimization. This method greatly accelerates condition filtering when a query requires scanning of multiple columns of data. Take the following query as an example. In the `WHERE` statement, if the filtering conditions connected by `OR` have their respective indexes on columns _key1_ and _key2_, the Index Merge feature filters the respective indexes at the same time, merges the query results, and returns the merged result.

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    Before TiDB v4.0, a query on a table supports using only one index for filtering at one time. If you want to query multiple columns of data, you can enable Index Merge to get the exact query result in a short time by using the indexes in individual columns. Index Merge avoids unnecessary full table scans and does not require establishing a large number of composite indexes.

    In v5.4.0, Index Merge becomes GA. However, you still need to pay attention to the following restrictions:

    - Index Merge supports only disjunctive normal form (X<sub>1</sub> ⋁ X<sub>2</sub> ⋁ …X<sub>n</sub>). That is, this feature only works when filtering conditions in a `WHERE` clause are connected by `OR`.

    - For newly deployed TiDB clusters of v5.4.0 or later, this feature is enabled by default. For v5.4.0 or later TiDB clusters upgraded from earlier versions, this feature inherits the setting before the upgrade and you can change the setting as required (for TiDB clusters earlier than v4.0, this feature does not exist and is disabled by default).

    [User document](/explain-index-merge.md)

- **Support Raft Engine (experimental)**

    Support using [Raft Engine](https://github.com/tikv/raft-engine) as the log storage engine in TiKV. Compared with RocksDB, Raft Engine can reduce TiKV I/O write traffic by up to 40% and CPU usage by 10%, while improving foreground throughput by about 5% and reducing tail latency by 20% under certain loads. In addition, Raft Engine improves the efficiency of log recycling and fixes the issue of log accumulation in extreme conditions.

    Raft Engine is still an experimental feature and is disabled by default. Note that the data format of Raft Engine in v5.4.0 is not compatible with previous versions. Before upgrading the cluster, you need to make sure that Raft Engine on all TiKV nodes is disabled. It is recommended to use Raft Engine only in v5.4.0 or a later version.

    [User document](/tikv-configuration-file.md#raft-engine)

- **Support collecting statistics on `PREDICATE COLUMNS` (experimental)**

    In most cases, when executing SQL statements, the optimizer only uses statistics of some columns (such as columns in the `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` statements). These used columns are called `PREDICATE COLUMNS`.

    Since v5.4.0, you can set the value of the [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540) system variable to `ON` to enable TiDB to collect `PREDICATE COLUMNS`.

    After the setting, TiDB writes the `PREDICATE COLUMNS` information to the `mysql.column_stats_usage` system table every 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease). When the query pattern of your business is stable, you can use the `ANALYZE TABLE TableName PREDICATE COLUMNS` syntax to collect statistics on the `PREDICATE COLUMNS` columns only, which can greatly reduce the overhead of collecting statistics.

    [User document](/statistics.md#collect-statistics-on-some-columns)

- **Support synchronously loading statistics (experimental)**

    Since v5.4.0, TiDB introduces the synchronously loading statistics feature. This feature is disabled by default. After enabling the feature, TiDB can synchronously load large-sized statistics (such as histograms, TopN, and Count-Min Sketch statistics) into memory when you execute SQL statements, which improves the completeness of statistics for SQL optimization.

    [User document](/statistics.md#load-statistics)

### Stability

- **Support persisting ANALYZE configurations**

    Statistics are one type of the basic information that the optimizer refers to when generating execution plans. The accuracy of the statistics directly affects whether the generated execution plans are reasonable. To ensure the accuracy of the statistics, sometimes it is necessary to set different collection configurations for different tables, partitions, and indexes.

    Since v5.4.0, TiDB supports persisting some `ANALYZE` configurations. With this feature, the existing configurations can be easily reused for future statistics collection.

    The `ANALYZE` configuration persistence feature is enabled by default (the system variable `tidb_analyze_version` is `2` and [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540) is `ON` by default). You can use this feature to record the persistence configurations specified in the `ANALYZE` statement when executing the statement manually. Once recorded, the next time TiDB automatically updates statistics or you manually collect statistics without specifying these configurations, TiDB will collect statistics according to the recorded configurations.

    [User document](/statistics.md#persist-analyze-configurations)

### High availability and disaster recovery

- **Reduce the impact of backup tasks on the cluster**

    Backup & Restore (BR) introduces the auto-tune feature (enabled by default). This feature can reduce the impact of backup tasks on the cluster by monitoring the cluster resource usage and adjusting the number of threads used by the backup tasks. In some cases, if you increase the cluster hardware resource for backup and enable the auto-tune feature, it can limit the impact of backup tasks on the cluster to 10% or less.

   [User document](/br/br-auto-tune.md)

- **Support Azure Blob Storage as a target storage for backup**

   Backup & Restore (BR) supports Azure Blob Storage as a remote backup storage. If you deploy TiDB in Azure Cloud, now you can back up the cluster data to the Azure Blob Storage service.

    [User document](/br/backup-and-restore-storages.md)

### Data migration

- **TiDB Lightning introduces a new feature to determine whether to allow importing data to tables with data**

    TiDB Lightning introduces a configuration item`incremental-import`. It determines whether to allow importing data to tables with data. The default value is `false`. When using the parallel import mode, you must set the configuration to `true`.

    [User document](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

- **TiDB Lightning introduces the schema name that stores the meta information for parallel import**

    TiDB Lightning introduces the `meta-schema-name` configuration item. In parallel import mode, this parameter specifies the schema name that stores the meta information for each TiDB Lightning instance in the target cluster. By default, the value is "lightning_metadata". The value set for this parameter must be the same for each TiDB Lightning instance that participates in the same parallel import; otherwise, the correctness of the imported data cannot be ensured.

  [User document](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

- **TiDB Lightning introduces duplicate resolution**

    In Local-backend mode, TiDB Lightning outputs duplicated data before the data import is completed, and then removes that duplicated data from the database. You can resolve the duplicated data after the import is completed and select suitable data to insert according to application rules. It is recommended to clean upstream data sources based on duplicated data to avoid data inconsistency caused by duplicated data encountered in the subsequent incremental data migration phase.

    [User document](/tidb-lightning/tidb-lightning-error-resolution.md)

- **Optimize the usage of relay log in TiDB Data Migration (DM)**

    - Recover the `enable-relay` switch in the `source` configuration.

    - Support dynamically enabling and disabling relay log using the `start-relay` and `stop-relay` commands.

    - Bind the status of relay log to `source`. `source` keeps its original status of being enabled or disabled after it is migrated to any DM-worker.

    - Move the storage path of relay log to the DM-worker configuration file.

    [User document](/dm/relay-log.md)

- **Optimize the processing of [collation](/character-set-and-collation.md) in DM**

    Add the `collation_compatible` configuration item. The value options are `loose` (default) and `strict`:

    - If your application does not have strict requirements on collation, and the collation of query results can be different between the upstream and downstream, you can use the default `loose` mode to avoid reporting errors.
    - If your application has strict requirements on collation, and the collation must be consistent between the upstream and downstream, you can use the `strict` mode. However, if the downstream does not support the upstream's default collation, the data replication might report errors.

   [User document](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

- **Optimize `transfer source` in DM to support running replication tasks smoothly**

    When the DM-worker nodes have an unbalanced load, the `transfer source` command can be used to manually transfer the configuration of a `source` to another load. After the optimization, the `transfer source` command simplifies the manual operation. You can smoothly transfer the source instead of pausing all related tasks, because DM completes other operations internally.

- **DM OpenAPI becomes generally available (GA)**

    DM supports daily management via API, including adding data sources and managing tasks. In v5.4.0, DM OpenAPI becomes GA.

    [User document](/dm/dm-open-api.md)

### Diagnostic efficiency

- **Top SQL (experimental feature)**

    A new experimental feature, Top SQL (disabled by default), is introduced to help you easily find source-consuming queries.

    [User document](/dashboard/top-sql.md)

### TiDB data share subscription

- **Optimize the impact of TiCDC on clusters**

    Significantly reduces the impact on the performance of TiDB clusters when you use TiCDC. In the test environment, the performance impact of TiCDC on TiDB can be reduced to less than 5%.

### Deployment and maintenance

- **Enhance Continuous Profiling (experimental)**

    - More components supported: Besides TiDB, PD, and TiKV, TiDB v5.4.0 also supports CPU profiling of TiFlash.
    - More forms of profiling display: Supports showing CPU profiling and Goroutine results on flame charts.

    - More deployment environments supported: Continuous Profiling can also be used for clusters deployed using TiDB Operator.

   Continuous Profiling is disabled by default and can be enabled on TiDB Dashboard.

    Continuous Profiling is applicable to clusters deployed or upgraded using TiUP of v1.9.0 or later or TiDB Operator of v1.3.0 or later.

    [User document](/dashboard/continuous-profiling.md)

## Improvements

+ TiDB

    - Support the `ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE` syntax to clear the cached query plan [#30370](https://github.com/pingcap/tidb/pull/30370)

+ TiKV

    - Coprocessor supports paging API to process requests in a stream-like way [#11448](https://github.com/tikv/tikv/issues/11448)
    - Support `read-through-lock` so that read operations do not need to wait for secondary locks to be resolved [#11402](https://github.com/tikv/tikv/issues/11402)
    - Add a disk protection mechanism to avoid panic caused by disk space drainage [#10537](https://github.com/tikv/tikv/issues/10537)
    - Support archiving and rotating logs [#11651](https://github.com/tikv/tikv/issues/11651)
    - Reduce the system call by the Raft client and increase CPU efficiency [#11309](https://github.com/tikv/tikv/issues/11309)
    - Coprocessor supports pushing down substring to TiKV [#11495](https://github.com/tikv/tikv/issues/11495)
    - Improve the scan performance by skip reading locks in the Read Committed isolation level [#11485](https://github.com/tikv/tikv/issues/11485)
    - Reduce the default thread pool size used by backup operations and limit the use of thread pool when the stress is high [#11000](https://github.com/tikv/tikv/issues/11000)
    - Support dynamically adjusting the sizes of the Apply thread pool and the Store thread pool [#11159](https://github.com/tikv/tikv/issues/11159)
    - Support configuring the size of the `snap-generator` thread pool [#11247](https://github.com/tikv/tikv/issues/11247)
    - Optimize the issue of global lock race that occurs when there are many files with frequent reads and writes [#250](https://github.com/tikv/rocksdb/pull/250)

+ PD

    - Record the historic hotspot information by default [#25281](https://github.com/pingcap/tidb/issues/25281)
    - Add signature for the HTTP component to identify the request source [#4490](https://github.com/tikv/pd/issues/4490)
    - Update TiDB Dashboard to v2021.12.31 [#4257](https://github.com/tikv/pd/issues/4257)

+ TiFlash

    - Optimize the communication of local operators
    - Increase the non-temporary thread count of gRPC to avoid the frequent creation or destruction of threads

+ Tools

    + Backup & Restore (BR)

        - Add a validity check for the key when BR performs encrypted backup [#29794](https://github.com/pingcap/tidb/issues/29794)

    + TiCDC

        - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Reduce the replication latency when replicating many tables [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

    + TiDB Data Migration (DM)

        - Lower the usage rate of CPU when the relay is enabled [#2214](https://github.com/pingcap/dm/issues/2214)

    + TiDB Lightning

        - Use optimistic transactions by default to write data to improve performance in TiDB-backend mode [#30953](https://github.com/pingcap/tidb/pull/30953)

    + Dumpling

        - Improve compatibility when Dumpling checks the database version [#29500](https://github.com/pingcap/tidb/pull/29500)
        - Add the default collation when dumping `CREATE DATABASE` and `CREATE TABLE` [#3420](https://github.com/pingcap/tiflow/issues/3420)

## Bug fixes

+ TiDB

    - Fix the issue of the `tidb_analyze_version` value change that occurs when upgrading the cluster from v4.x to v5.x [#25422](https://github.com/pingcap/tidb/issues/25422)
    - Fix the issue of the wrong result that occurs when using different collations in a subquery [#30748](https://github.com/pingcap/tidb/issues/30748)
    - Fix the issue that the result of `concat(ifnull(time(3))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that the query execution plan of IndexMerge is wrong when an expression cannot be pushed down to TiKV [#30200](https://github.com/pingcap/tidb/issues/30200)
    - Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Fix the issue that the IndexMerge query result is wrong when there is a subquery [#30913](https://github.com/pingcap/tidb/issues/30913)
    - Fix the panic issue that occurs when the FetchSize is set too large in the client [#30896](https://github.com/pingcap/tidb/issues/30896)
    - Fix the issue that LEFT JOIN might be mistakenly converted to INNER JOIN [#20510](https://github.com/pingcap/tidb/issues/20510)
    - Fix the issue that panic might occur when the `CASE-WHEN` expression and collation are used together [#30245](https://github.com/pingcap/tidb/issues/30245)
    - Fix the issue of wrong query result that occurs when the `IN` value contains a binary constant [#31261](https://github.com/pingcap/tidb/issues/31261)
    - Fix the issue of wrong query result that occurs when CTE has a subquery [#31255](https://github.com/pingcap/tidb/issues/31255)
    - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)

+ TiKV

    - Fix the issue that the MVCC deletion records are not cleared by GC [#11217](https://github.com/tikv/tikv/issues/11217)
    - Fix the issue that retrying prewrite requests in the pessimistic transaction mode might cause the risk of data inconsistency in rare cases [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix the issue that GC scan causes memory overflow [#11410](https://github.com/tikv/tikv/issues/11410)
    - Fix the issue that RocksDB flush or compaction causes panic when the disk capacity is full [#11224](https://github.com/tikv/tikv/issues/11224)

+ PD

    - Fix the issue that Region statistics are not affected by `flow-round-by-digit` [#4295](https://github.com/tikv/pd/issues/4295)
    - Fix the issue that the scheduling operator cannot fail fast because the target store is down [#3353](https://github.com/tikv/pd/issues/3353)
    - Fix the issue that Regions on offline stores cannot be merged [#4119](https://github.com/tikv/pd/issues/4119)
    - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix the issue that TiFlash might panic when an MPP query is stopped
    - Fix the issue that queries with the `where <string>` clause return wrong results
    - Fix the potential issue of data inconsistency that might occur when setting the column type of an integer primary key to a larger range
    - Fix the issue that when an input time is earlier than 1970-01-01 00:00:01 UTC, the behavior of `unix_timestamp` is inconsistent with that of TiDB or MySQL
    - Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is restarted
    - Fix the issue that the `CastStringAsDecimal` behavior is inconsistent in TiFlash and in TiDB/TiKV
    - Fix the issue that the `DB::Exception: Encode type of coprocessor response is not CHBlock` error is returned in the query result
    - Fix the issue that the `castStringAsReal` behavior is inconsistent in TiFlash and in TiDB/TiKV
    - Fix the issue that the returned result of the `date_add_string_xxx` function in TiFlash is inconsistent with that in MySQL

+ Tools

    + Backup & Restore (BR)

        - Fix the potential issue that Region distribution might be uneven after a restore operation is finished [#30425](https://github.com/pingcap/tidb/issues/30425)
        - Fix the issue that `'/'` cannot be specified in endpoint when `minio` is used as the backup storage [#30104](https://github.com/pingcap/tidb/issues/30104)
        - Fix the issue that system tables cannot be restored because concurrently backing up system tables makes the table name fail to update [#29710](https://github.com/pingcap/tidb/issues/29710)

    + TiCDC

        - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the issue that the `cached region` monitoring metric is negative [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the compatibility issue of `sql mode` [#3810](https://github.com/pingcap/tiflow/issues/3810)
        - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the issue of panic and data inconsistency that occurs when outputting the default column value [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Fix the issue that no log is output when the disk is fully written [#3362](https://github.com/pingcap/tiflow/issues/3362)
        - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Fix the OOM issue in the container environment [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)

    + TiDB Data Migration (DM)

        - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)
        - Fix the issue that the table checkpoint is not updated in time after a DDL statement is skipped [#4184](https://github.com/pingcap/tiflow/issues/4184)
        - Fix a compatibility issue of the TiDB version with the Parser version [#4298](https://github.com/pingcap/tiflow/issues/4298)
        - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)

    + TiDB Lightning

        - Fix the issue of wrong import result that occurs when TiDB Lightning does not have the privilege to access the `mysql.tidb` table [#31088](https://github.com/pingcap/tidb/issues/31088)
        - Fix the issue that some checks are skipped when TiDB Lightning is restarted [#30772](https://github.com/pingcap/tidb/issues/30772)
        - Fix the issue that TiDB Lightning fails to report the error when the S3 path does not exist [#30674](https://github.com/pingcap/tidb/pull/30674)

    + TiDB Binlog

        - Fix the issue that Drainer fails because it is incompatible with the `CREATE PLACEMENT POLICY` statement [#1118](https://github.com/pingcap/tidb-binlog/issues/1118)
