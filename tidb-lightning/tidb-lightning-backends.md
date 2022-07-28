---
title: TiDB Lightning Import Modes
summary: Learn how to choose different import modes of TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-tidb-backend/','/docs/dev/reference/tools/tidb-lightning/tidb-backend/','/tidb/dev/tidb-lightning-tidb-backend','/docs/dev/loader-overview/','/docs/dev/reference/tools/loader/','/docs/dev/load-misuse-handling/','/docs/dev/reference/tools/error-case-handling/load-misuse-handling/','/tidb/dev/load-misuse-handling','/tidb/dev/loader-overview/']
---

# TiDB Lightning Import Modes

TiDB Lightning supports two import modes in two [backends](/tidb-lightning/tidb-lightning-glossary.md#back-end). The backend determines how TiDB Lightning imports data into the target cluster.

- The **Local-backend**: TiDB Lightning first encodes data into key-value pairs, sorts and stores them in a local temporary directory, and *uploads* these key-value pairs to each TiKV node. Then, TiDB Lightning calls the TiKV ingest interface to write the data into RocksDB in TiKV. For initialized data import, consider the local-backend because it has a high import speed.

- The **TiDB-backend**: TiDB Lightning first encodes data into SQL statements, and then runs these statements to import data. If the target cluster is in a production environment, or if the target table already has data, consider the TiDB-backend.

| Backend | Local-backend | TiDB-backend |
|:---|:---|:---|
| Speed | Fast (~500 GB/hr) | Slow (~50 GB/hr) |
| Resource usage | High | Low |
| Network bandwidth usage | High | Low |
| ACID compliance during import | No | Yes |
| Target tables | Must be empty | Can be populated |
| TiDB versions supported | >= v4.0.0 | All |
| TiDB can provide services during import | No | Yes |

> **Note**:
>
> - Do not import data into an in-production TiDB cluster in the local-backend mode. This will cause severe impact on the online application.
> - By default, you cannot start multiple TiDB Lightning instances to import data into the same TiDB cluster. Instead, you need to use the [Parallel Import](/tidb-lightning/tidb-lightning-distributed-import.md) feature.
> - When you import data into the same target database using multiple TiDB Lightning instances, do not use more than one backend. For example, do not import data into a TiDB cluster using both the local-backend and the TiDB-backend.

## Local-backend

TiDB Lightning introduces the local-backend in TiDB v4.0.3. By using the local-backend, you can import data into TiDB clusters >= v4.0.0.

### Configuration and examples

```toml
[Lightning]
# Specifies the database to store the execution results. If you do not want to create this schema, set this value to an empty string.
# task-info-schema-name = 'lightning_task_info'

[tikv-importer]
backend = "local"
# When the backend is 'local', whether to detect and resolve conflicting records (unique key conflict).
# The following three resolution strategies are supported:
#  - none: does not detect duplicate records, which has the best performance in the three
#    strategies, but might lead to inconsistent data in the target TiDB.
#  - record: only records conflicting records to the `lightning_task_info.conflict_error_v1`
#    table on the target TiDB. Note that the required version of the target TiKV is not
#    earlier than v5.2.0; otherwise, it falls back to 'none'.
#  - remove: records all conflicting records, like the 'record' strategy. But it removes all
#    conflicting records from the target table to ensure a consistent state in the target TiDB.
# duplicate-resolution = 'none'

# The directory of local KV sorting in the local-backend mode. SSD is recommended, and the
# directory should be set on a different disk from `data-source-dir` to improve import
# performance.
# The sorted-kv-dir directory should have free space greater than the size of the largest
# table in the upstream. If the space is insufficient, the import will fail.
sorted-kv-dir = ""
# The concurrency that TiKV writes KV data in the local-backend mode. When the network
# transmission speed between TiDB Lightning and TiKV exceeds 10 Gigabit, you can increase
# this value accordingly.
# range-concurrency = 16
# The number of KV pairs sent in one request in the local-backend mode.
# send-kv-pairs = 32768

[tidb]
# The target cluster information. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# Required in the local-backend mode. Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Required in the local-backend mode. The address of any pd-server from the cluster.
pd-addr = "172.16.31.4:2379"
```

### Conflict resolution

The `duplicate-resolution` configuration offers three strategies to resollve the possible conflicting data.

- `none` (default): does not detect duplicate records, which has the best performance in the three strategies, but might lead to inconsistent data in the target TiDB.
- `record`: only records conflicting records to the `lightning_task_info.conflict_error_v1` table on the target TiDB. Note that the required version of the target TiKV is not earlier than v5.2.0; otherwise, it falls back to 'none'.
- `remove`: records all conflicting records, like the 'record' strategy. But it removes all conflicting records from the target table to ensure a consistent state in the target TiDB.

If you are not sure whether there is conflicting data in the data source, the `remove` strategy is recommended. The `none` and `record` strategies do not remove conflicting data from the target table, which means that the unique indexes generated by TiDB Lightning might be inconsistent with the data.

## TiDB-backend

### Configuration and examples

```toml
[tikv-importer]
# The backend mode. To use TiDB-backed, set it to "tidb".
backend = "tidb"

# Action to do when trying to insert a conflicting data.
# - replace: use new record to replace the existing record.
# - ignore: keep the existing record, and ignore the new record.
# - error: abort the import and report an error.
# on-duplicate = "replace"
```

### Conflict resolution

The TiDB-backend supports importing to an already-populated (non-empty) table. However, the new data might cause a unique key conflict with the old data. You can control how to resolve the conflict by using the `on-duplicate` configuration:

| Value | Default behavior on conflict | SQL statement |
|:---|:---|:---|
| `replace` | New records replace old ones | `REPLACE INTO ...` |
| `ignore` | Keep old records and ignore new ones | `INSERT IGNORE INTO ...` |
| `error` | Abort import | `INSERT INTO ...` |

## See also

- [Import Data in Parallel](/tidb-lightning/tidb-lightning-distributed-import.md)
