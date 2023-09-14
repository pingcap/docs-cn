---
title: Use Physical Import Mode
summary: Learn how to use the physical import mode in TiDB Lightning.
---

# Use Physical Import Mode

This document introduces how to use the [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) in TiDB Lightning, including writing the configuration file, tuning performance, and configuring disk quota.

There are limitations on the physical import mode. Before using the physical import mode, make sure to read [Limitations](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations).

## Configure and use the physical import mode

You can use the following configuration file to execute data import using the physical import mode:

```toml
[lightning]
# log
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# Checks the cluster minimum requirements before start.
check-requirements = true

[mydumper]
# The local data source directory or the URI of the external storage. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v6.6/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"

[conflict]
# Starting from v7.3.0, a new version of strategy is introduced to handle conflicting data. The default value is "".
# - "": TiDB Lightning does not detect or handle conflicting data. If the source file contains conflicting primary or unique key records, the subsequent step reports an error.
# - "error": when detecting conflicting primary or unique key records in the imported data, TiDB Lightning terminates the import and reports an error.
# - "replace": when encountering conflicting primary or unique key records, TiDB Lightning retains the new data and overwrites the old data.
# - "ignore": when encountering conflicting primary or unique key records, TiDB Lightning retains the old data and ignores the new data.
# The new version strategy cannot be used together with tikv-importer.duplicate-resolution (the old version of conflict detection).
strategy = ""
# threshold = 9223372036854775807
# max-record-rows = 100

[tikv-importer]
# Import mode. "local" means using the physical import mode.
backend = "local"

# The method to resolve the conflicting data.
duplicate-resolution = 'remove'

# The directory of local KV sorting.
sorted-kv-dir = "./some-dir"

# Limits the bandwidth in which TiDB Lightning writes data into each TiKV
# node in the physical import mode. 0 by default, which means no limit.
# store-write-bwlimit = "128MiB"

# Specifies whether Physical Import Mode adds indexes via SQL. The default value is `false`, which means that TiDB Lightning will encode both row data and index data into KV pairs and import them into TiKV together. This mechanism is consistent with that of the historical versions. If you set it to `true`, it means that TiDB Lightning adds indexes via SQL after importing the row data.
# The benefit of adding indexes via SQL is that you can separately import data and import indexes, and import data more quickly. After the data is imported, even if the indexes fail to be added, it does not affect the consistency of the imported data.
# add-index-by-sql = false

[tidb]
# The information of the target cluster. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# Required. Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Required. The address of any pd-server from the cluster.
pd-addr = "172.16.31.4:2379"
# tidb-lightning imports the TiDB library, and generates some logs.
# Set the log level of the TiDB library.
log-level = "error"

[post-restore]
# Specifies whether to perform `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after importing.
# The following options are available:
# - "required" (default): Perform admin checksum after importing. If checksum fails, TiDB Lightning will exit with failure.
# - "optional": Perform admin checksum. If checksum fails, TiDB Lightning will report a WARN log but ignore any error.
# - "off": Do not perform checksum after importing.
# Note that since v4.0.8, the default value has changed from "true" to "required".
#
# Note:
# 1. Checksum failure usually means import exception (data loss or data inconsistency), so it is recommended to always enable Checksum.
# 2. For backward compatibility, bool values "true" and "false" are also allowed for this field.
# "true" is equivalent to "required" and "false" is equivalent to "off".
checksum = "required"

# Specifies whether to perform `ANALYZE TABLE <table>` for each table after checksum is done.
# Options available for this field are the same as `checksum`. However, the default value for this field is "optional".
analyze = "optional"
```

For the complete configuration file, refer to [the configuration file and command line parameters](/tidb-lightning/tidb-lightning-configuration.md).

## Conflict detection

Conflicting data refers to two or more records with the same primary key or unique key column data. When the data source contains conflicting data and conflict detection feature is not turned on, the actual number of rows in the table is different from the total number of rows returned by the query using unique index.

There are two versions for conflict detection:

- The new version of conflict detection, controlled by the `conflict` configuration item.
- The old version of conflict detection, controlled by the `tikv-importer.duplicate-resolution` configuration item.

### The new version of conflict detection

The meaning of configuration values are as follows:

| Strategy | Default behavior of conflicting data | The corresponding SQL statement |
| :-- | :-- | :-- |
| `"replace"` | Replacing existing data with new data. | `REPLACE INTO ...` |
| `"ignore"` | Keeping existing data and ignoring new data. | `INSERT IGNORE INTO ...` |
| `"error"` | Pausing the import and reporting an error. | `INSERT INTO ...` |
| `""` | TiDB Lightning does not detect or handle conflicting data. If data with primary and unique key conflicts exists, the subsequent step reports an error. |  None   |

> **Note:**
>
> The conflict detection result in the physical import mode might differ from SQL-based import due to internal implementation and limitation of TiDB Lightning.

When the strategy is `"replace"` or `"ignore"`, conflicting data is treated as [conflict errors](/tidb-lightning/tidb-lightning-error-resolution.md#conflict-errors). If the [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) value is greater than `0`, TiDB Lightning tolerates the specified number of conflict errors. The default value is `9223372036854775807`, which means that almost all errors are tolerant. For more information, see [error resolution](/tidb-lightning/tidb-lightning-error-resolution.md).

The new version of conflict detection has the following limitations:

- Before importing, TiDB Lightning prechecks potential conflicting data by reading all data and encoding it. During the detection process, TiDB Lightning uses `tikv-importer.sorted-kv-dir` to store temporary files. After the detection is complete, TiDB Lightning retains the results for import phase. This introduces additional overhead for time consumption, disk space usage, and API requests to read the data.
- The new version of conflict detection only works in a single node, and does not apply to parallel imports and scenarios where the `disk-quota` parameter is enabled.
- The new version (`conflict`) and old version (`tikv-importer.duplicate-resolution`) conflict detection cannot be used at the same time. The new version of conflict detection is enabled when the configuration [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is set.

Compared with the old version of conflict detection, the new version takes less time when the imported data contains a large amount of conflicting data. It is recommended that you use the new version of conflict detection in non-parallel import tasks when the data contains conflicting data and there is sufficient local disk space.

### The old version of conflict detection

The old version of conflict detection is enabled when `tikv-importer.duplicate-resolution` is not an empty string. In v7.2.0 and earlier versions, TiDB Lightning only supports this conflict detection method.

In the old version of conflict detection, TiDB Lightning offers two strategies:

- `remove` (recommended): records and removes all conflicting records from the target table to ensure a consistent state in the target TiDB.
- `none`: does not detect duplicate records. `none` has the best performance in the two strategies, but might lead to inconsistent data in the target TiDB.

Before v5.3, TiDB Lightning does not support conflict detection. If there is conflicting data, the import process fails at the checksum step. When conflict detection is enabled, if there is conflicting data, TiDB Lightning skips the checksum step (because it always fails).

Suppose an `order_line` table has the following schema:

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int(11) NOT NULL,
  `ol_d_id` int(11) NOT NULL,
  `ol_w_id` int(11) NOT NULL,
  `ol_number` int(11) NOT NULL,
  `ol_i_id` int(11) NOT NULL,
  `ol_supply_w_id` int(11) DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int(11) DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

If Lightning detects conflicting data during the import, you can query the `lightning_task_info.conflict_error_v1` table as follows:

```sql
mysql> select table_name,index_name,key_data,row_data from conflict_error_v1 limit 10;
+---------------------+------------+----------+-----------------------------------------------------------------------------+
|  table_name         | index_name | key_data | row_data                                                                    |
+---------------------+------------+----------+-----------------------------------------------------------------------------+
| `tpcc`.`order_line` | PRIMARY    | 21829216 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 49931672 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 21829217 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 49931673 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 21829218 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 49931674 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 21829219 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 49931675 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 21829220 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
| `tpcc`.`order_line` | PRIMARY    | 49931676 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
+---------------------+------------+----------------------------------------------------------------------------------------+
10 rows in set (0.14 sec)
```

You can manually identify the records that need to be retained and insert these records into the table.

## Scope of pausing scheduling during import

Starting from v6.2.0, TiDB Lightning implements a mechanism to limit the impact of data import on online applications. With the new mechanism, TiDB Lightning does not pause the global scheduling, but only pauses scheduling for the Region that stores the target table data. This significantly reduces the impact of the import on online applications.

Starting from v7.1.0, you can control the scope of pausing scheduling by using the TiDB Lightning parameter [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md). The default value is `"table"`, which means that the scheduling is paused only for the Region that stores the target table data. When there is no business traffic in the cluster, it is recommended to set this parameter to `"global"` to avoid interference from other scheduling during the import.

<Note>

TiDB Lightning does not support importing data into a table that already contains data.

The TiDB cluster must be v6.1.0 or later versions. For earlier versions, TiDB Lightning keeps the old behavior, which pauses scheduling globally and severely impacts the online application during the import.

</Note>

By default, TiDB Lightning pauses the cluster scheduling for the minimum range possible. However, under the default configuration, the cluster performance still might be affected by fast import. To avoid this, you can configure the following options to control the import speed and other factors that might impact the cluster performance:

```toml
[tikv-importer]
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
store-write-bwlimit = "128MiB"

[tidb]
# Use smaller concurrency to reduce the impact of Checksum and Analyze on the transaction latency.
distsql-scan-concurrency = 3
```

## Performance tuning

**The most direct and effective ways to improve import performance of the physical import mode are as follows:**

- **Upgrade the hardware of the node where Lightning is deployed, especially the CPU and the storage device of `sorted-key-dir`.**
- **Use the [parallel import](/tidb-lightning/tidb-lightning-distributed-import.md) feature to achieve horizontal scaling.**

TiDB Lightning provides some concurrency-related configurations to affect import performance in the physical import mode. However, from long-term experience, it is recommended to keep the following four configuration items in the default value. Adjusting the four configuration items does not bring significant performance boost.

```
[lightning]
# The maximum concurrency of engine files.
# Each table is split into one "index engine" to store indices, and multiple
# "data engines" to store row data. These settings control the maximum
# concurrent number for each type of engines.
# The two settings controls the maximum concurrency of the two engine files.
index-concurrency = 2
table-concurrency = 6

# The concurrency of data. The default value is the number of logical CPUs.
region-concurrency =

# The maximum concurrency of I/O. When the concurrency is too high, the disk
# cache may be frequently refreshed, causing the cache miss and read speed
# to slow down. For different storage mediums, this parameter may need to be
# adjusted to achieve the best performance.
io-concurrency = 5
```

During the import, each table is split into one "index engine" to store indices, and multiple "data engines" to store row data.

`index-concurrency` controls the maximum concurrency of the index engine. When you adjust `index-concurrency`, make sure that `index-concurrency * the number of source files of each table > region-concurrency` to ensure that the CPU is fully utilized. The ratio is usually between 1.5 ~ 2. Do not set `index-concurrency` too high and not lower than 2 (default). Too high `index-concurrency` causes too many pipelines to be built, which causes the index-engine import stage to pile up.

The same goes for `table-concurrency`. Make sure that `table-concurrency * the number of source files of each table > region-concurrency` to ensure that the CPU is fully utilized. A recommended value is around `region-concurrency * 4 / the number of source files of each table` and not lower than 4.

If the table is large, Lightning will split the table into multiple batches of 100 GiB. The concurrency is controlled by `table-concurrency`.

`index-concurrency` and `table-concurrency` has little effect on the import speed. You can leave them in the default value.

`io-concurrency` controls the concurrency of file read. The default value is 5. At any given time, only 5 handles are performing read operations. Because the file read speed is usually not a bottleneck, you can leave this configuration in the default value.

After the file data is read, Lightning needs to do some post-processing, such as encoding and sorting the data locally. The concurrency of these operations is controlled by `region-concurrency`. The default value is the number of CPU cores. You can leave this configuration in the default value. It is recommended to deploy Lightning on a separate server from other components. If you must deploy Lightning together with other components, you need to lower the value of `region-concurrency` according to the load.

The [`num-threads`](/tikv-configuration-file.md#num-threads) configuration of TiKV can also affect the performance. For new clusters, it is recommended to set `num-threads` to the number of CPU cores.

## Configure disk quota <span class="version-mark">New in v6.2.0</span>

When you import data in the physical import mode, TiDB Lightning creates a large number of temporary files on the local disk to encode, sort, and split the original data. When the local disk space is insufficient, TiDB Lightning reports an error and exits because of write failure.

To avoid this situation, you can configure disk quota for TiDB Lightning. When the size of the temporary files exceeds the disk quota, TiDB Lightning pauses the process of reading the source data and writing temporary files. TiDB Lightning prioritizes writing the sorted key-value pairs to TiKV. After deleting the local temporary files, TiDB Lightning continues the import process.

To enable disk quota, add the following configuration to your configuration file:

```toml
[tikv-importer]
# MaxInt64 by default, which is 9223372036854775807 bytes.
disk-quota = "10GB"
backend = "local"

[cron]
# The interval of checking disk quota. 60 seconds by default.
check-disk-quota = "30s"
```

`disk-quota` limits the storage space used by TiDB Lightning. The default value is MaxInt64, which is 9223372036854775807 bytes. This value is much larger than the disk space you might need for the import, so leaving it as the default value is equivalent to not setting the disk quota.

`check-disk-quota` is the interval of checking disk quota. The default value is 60 seconds. When TiDB Lightning checks the disk quota, it acquires an exclusive lock for the relevant data, which blocks all the import threads. Therefore, if TiDB Lightning checks the disk quota before every write, it significantly slows down the write efficiency (as slow as a single-thread write). To achieve efficient write, disk quota is not checked before every write; instead, TiDB Lightning pauses all the import threads and checks the disk quota every `check-disk-quota` interval. That is, if the value of `check-disk-quota` is set to a large value, the disk space used by TiDB Lightning might exceed the disk quota you set, which leaves the disk quota ineffective. Therefore, it is recommended to set the value of `check-disk-quota` to a small value. The specific value of this item is determined by the environment in which TiDB Lightning is running. In different environments, TiDB Lightning writes temporary files at different speeds. Theoretically, the faster the speed, the smaller the value of `check-disk-quota` should be.
