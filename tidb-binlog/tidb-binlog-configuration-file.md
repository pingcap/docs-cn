---
title: TiDB Binlog Configuration File
summary: Learn the configuration items of TiDB Binlog.
aliases: ['/docs/dev/tidb-binlog/tidb-binlog-configuration-file/','/docs/dev/reference/tidb-binlog/config/']
---

# TiDB Binlog Configuration File

This document introduces the configuration items of TiDB Binlog.

## Pump

This section introduces the configuration items of Pump. For the example of a complete Pump configuration file, see [Pump Configuration](https://github.com/pingcap/tidb-binlog/blob/master/cmd/pump/pump.toml).

### addr

* Specifies the listening address of HTTP API in the format of `host:port`.
* Default value: `127.0.0.1:8250`

### advertise-addr

* Specifies the externally accessible HTTP API address. This address is registered in PD in the format of `host:port`.
* Default value: `127.0.0.1:8250`

### socket

* The Unix socket address that HTTP API listens to.
* Default value: ""

### pd-urls

* Specifies the comma-separated list of PD URLs. If multiple addresses are specified, when the PD client fails to connect to one address, it automatically tries to connect to another address.
* Default value: `http://127.0.0.1:2379`

### data-dir

* Specifies the directory where binlogs and their indexes are stored locally.
* Default value: `data.pump`

### heartbeat-interval

* Specifies the heartbeat interval (in seconds) at which the latest status is reported to PD.
* Default value: `2`

### gen-binlog-interval

* Specifies the interval (in seconds) at which data is written into fake binlog.
* Default value: `3`

### gc

* Specifies the number of days (integer) that binlogs can be stored locally. Binlogs stored longer than the specified number of days are automatically deleted.
* Default value: `7`

### log-file

* Specifies the path where log files are stored. If the parameter is set to an empty value, log files are not stored.
* Default value: ""

### log-level

* Specifies the log level.
* Default value: `info`

### node-id

* Specifies the Pump node ID. With this ID, this Pump process can be identified in the cluster.
* Default value: `hostname:port number`. For example, `node-1:8250`.

### security

This section introduces configuration items related to security.

#### ssl-ca

* Specifies the file path of the trusted SSL certificate list or CA list. For example, `/path/to/ca.pem`.
* Default value: ""

#### ssl-cert

* Specifies the path of the X509 certificate file encoded in the Privacy Enhanced Mail (PEM) format. For example, `/path/to/pump.pem`.
* Default value: ""

#### ssl-key

* Specifies the path of the X509 key file encoded in the PEM format. For example, `/path/to/pump-key.pem`.
* Default value: ""

### storage

This section introduces configuration items related to storage.

#### sync-log

* Specifies whether to use `fsync` after each **batch** write to binlog to ensure data safety.
* Default value: `true`

#### kv_chan_cap

* Specifies the number of write requests that the buffer can store before Pump receives these requests.
* Default value: `1048576` (that is, 2 to the power of 20)

#### slow_write_threshold

* The threshold (in seconds). If it takes longer to write a single binlog file than this specified threshold, the write is considered slow write and `"take a long time to write binlog"` is output in the log.
* Default value: `1`

#### stop-write-at-available-space

* Binlog write requests is no longer accepted when the available storage space is below this specified value. You can use the format such as `900 MB`, `5 GB`, and `12 GiB` to specify the storage space. If there is more than one Pump node in the cluster, when a Pump node refuses a write request because of the insufficient space, TiDB will automatically write binlogs to other Pump nodes.
* Default value: `10 GiB`

#### kv

Currently the storage of Pump is implemented based on [GoLevelDB](https://github.com/syndtr/goleveldb). Under `storage` there is also a `kv` subgroup that is used to adjust the GoLevel configuration. The supported configuration items are shown as below:

* block-cache-capacity
* block-restart-interval
* block-size
* compaction-L0-trigger
* compaction-table-size
* compaction-total-size
* compaction-total-size-multiplier
* write-buffer
* write-L0-pause-trigger
* write-L0-slowdown-trigger

For the detailed description of the above items, see [GoLevelDB Document](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options).

## Drainer

This section introduces the configuration items of Drainer. For the example of a complete Drainer configuration file, see [Drainer Configuration](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml)

### addr

* Specifies the listening address of HTTP API in the format of `host:port`.
* Default value: `127.0.0.1:8249`

### advertise-addr

* Specifies the externally accessible HTTP API address. This address is registered in PD in the format of `host:port`.
* Default value: `127.0.0.1:8249`

### log-file

* Specifies the path where log files are stored. If the parameter is set to an empty value, log files are not stored.
* Default value: ""

### log-level

* Specifies the log level.
* Default value: `info`

### node-id

* Specifies the Drainer node ID. With this ID, this Drainer process can be identified in the cluster.
* Default value: `hostname:port number`. For example, `node-1:8249`.

### data-dir

* Specifies the directory used to store files that need to be saved during Drainer operation.
* Default value: `data.drainer`

### detect-interval

* Specifies the interval (in seconds) at which PD updates the Pump information.
* Default value: `5`

### pd-urls

* The comma-separated list of PD URLs. If multiple addresses are specified, the PD client will automatically attempt to connect to another address if an error occurs when connecting to one address.
* Default value: `http://127.0.0.1:2379`

### initial-commit-ts

* Specifies from which commit timestamp of the transaction the replication process starts. This configuration is applicable only to the Drainer node that is in the replication process for the first time. If a checkpoint already exists in the downstream, the replication will be performed according to the time recorded in the checkpoint.
* commit ts (commit timestamp) is a specific point in time for [transaction](/transaction-overview.md#transactions) commits in TiDB. It is a globally unique and increasing timestamp from PD as the unique ID of the current transaction. You can get the `initial-commit-ts` configuration in the following typical ways:
    - If BR is used, you can get `initial-commit-ts` from the backup TS recorded in the metadata backed up by BR (backupmeta).
    - If Dumpling is used, you can get `initial-commit-ts` from the Pos recorded in the metadata backed up by Dumpling (metadata),
    - If PD Control is used, `initial-commit-ts` is in the output of the `tso` command.
* Default value: `-1`. Drainer will get a new timestamp from PD as the starting time, which means that the replication process starts from the current time.

### synced-check-time

* You can access the `/status` path through the HTTP API to query the status of Drainer replication. `synced-check-time` specifies how many minutes from the last successful replication is considered as `synced`, that is, the replication is complete.
* Default value: `5`

### compressor

* Specifies the compression algorithm used for data transfer between Pump and Drainer. Currently only the `gzip` algorithm is supported.
* Default value: "", which means no compression.

### security

This section introduces configuration items related to security.

#### ssl-ca

* Specifies the file path of the trusted SSL certificate list or CA list. For example, `/path/to/ca.pem`.
* Default value: ""

#### ssl-cert

* Specifies the path of the X509 certificate file encoded in the PEM format. For example, `/path/to/drainer.pem`.
* Default value: ""

#### ssl-key

* Specifies the path of the X509 key file encoded in the PEM format. For example, `/path/to/pump-key.pem`.
* Default value: ""

### syncer

The `syncer` section includes configuration items related to the downstream.

#### db-type

Currently, the following downstream types are supported:

* `mysql`
* `tidb`
* `kafka`
* `file`

Default value: `mysql`

#### sql-mode

* Specifies the SQL mode when the downstream is the `mysql` or `tidb` type. If there is more than one mode, use commas to separate them.
* Default value: ""

#### ignore-txn-commit-ts

* Specifies the commit timestamp at which the binlog is ignored, such as `[416815754209656834, 421349811963822081]`.
* Default value: `[]`

#### ignore-schemas

* Specifies the database to be ignored during replication. If there is more than one database to be ignored, use commas to separate them. If all changes in a binlog file are filtered, the whole binlog file is ignored.
* Default value: `INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql`

#### ignore-table

Ignores the specified table changes during replication. You can specify multiple tables to be ignored in the `toml` file. For example:

{{< copyable "" >}}

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

If all changes in a binlog file are filtered, the whole binlog file is ignored.

Default value: `[]`

#### replicate-do-db

* Specifies the database to be replicated. For example, `[db1, db2]`.
* Default value: `[]`

#### replicate-do-table

Specifies the table to be replicated. For example:

{{< copyable "" >}}

```toml
[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "log"

[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "~^a.*"
```

Default value: `[]`

#### txn-batch

* When the downstream is the `mysql` or `tidb` type, DML operations are executed in different batches. This parameter specifies how many DML operations can be included in each transaction.
* Default value: `20`

#### worker-count

* When the downstream is the `mysql` or `tidb` type, DML operations are executed concurrently. This parameter specifies the concurrency numbers of DML operations.
* Default value: `16`

#### disable-dispatch

* Disables the concurrency and forcibly set `worker-count` to `1`.
* Default value: `false`

#### safe-mode

If the safe mode is enabled, Drainer modifies the replication updates in the following way:

* `Insert` is modified to `Replace Into`
* `Update` is modified to `Delete` plus `Replace Into`

Default value: `false`

### syncer.to

The `syncer.to` section introduces different types of downstream configuration items according to configuration types.

#### mysql/tidb

The following configuration items are related to connection to downstream databases:

* `host`: If this item is not set, TiDB Binlog tries to check the `MYSQL_HOST` environment variable which is `localhost` by default.
* `port`: If this item is not set, TiDB Binlog tries to check the `MYSQL_PORT` environment variable which is `3306` by default.
* `user`: If this item is not set, TiDB Binlog tries to check the `MYSQL_USER` environment variable which is `root` by default.
* `password`: If this item is not set, TiDB Binlog tries to check the `MYSQL_PSWD` environment variable which is `""` by default.

#### file

* `dir`: Specifies the directory where binlog files are stored. If this item is not set, `data-dir` is used.

#### kafka

When the downstream is Kafka, the valid configuration items are as follows:

* `zookeeper-addrs`
* `kafka-addrs`
* `kafka-version`
* `kafka-max-messages`
* `topic-name`

### syncer.to.checkpoint

This section introduces a configuration item related to `syncer.to.checkpoint`.

### type

* Specifies in what way the replication progress is saved.
* Available options: `mysql` and `tidb`.

* Default value: The same as the downstream type. For example, when the downstream is `file`, the progress is saved in the local file system; when the downstream is `mysql`, the progress is saved in the downstream database. If you explicitly specify using `mysql` or `tidb` to store the progress, make the following configuration:

    * `schema`: `tidb_binlog` by default.

        > **Note:**
        >
        > When deploying multiple Drainer nodes in the same TiDB cluster, you need to specify a different checkpoint schema for each node. Otherwise, the replication progress of two instances will overwrite each other.

    * `host`
    * `user`
    * `password`
    * `port`
