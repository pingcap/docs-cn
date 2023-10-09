---
title: TiCDC FAQs
summary: Learn the FAQs you might encounter when you use TiCDC.
---

# TiCDC FAQs

This document introduces the common questions that you might encounter when using TiCDC.

> **Note:**
>
> In this document, the server address specified in `cdc cli` commands is `--server=http://127.0.0.1:8300`. When you use the command, replace the address with your actual PD address.

## How do I choose `start-ts` when creating a task in TiCDC?

The `start-ts` of a replication task corresponds to a Timestamp Oracle (TSO) in the upstream TiDB cluster. TiCDC requests data from this TSO in a replication task. Therefore, the `start-ts` of the replication task must meet the following requirements:

- The value of `start-ts` is larger than the `tikv_gc_safe_point` value of the current TiDB cluster. Otherwise, an error occurs when you create a task.
- Before starting a task, ensure that the downstream has all data before `start-ts`. For scenarios such as replicating data to message queues, if the data consistency between upstream and downstream is not required, you can relax this requirement according to your application need.

If you do not specify `start-ts`, or specify `start-ts` as `0`, when a replication task is started, TiCDC gets a current TSO and starts the task from this TSO.

## Why can't some tables be replicated when I create a task in TiCDC?

When you execute `cdc cli changefeed create` to create a replication task, TiCDC checks whether the upstream tables meet the [replication requirements](/ticdc/ticdc-overview.md#best-practices). If some tables do not meet the requirements, `some tables are not eligible to replicate` is returned with a list of ineligible tables. You can choose `Y` or `y` to continue creating the task, and all updates on these tables are automatically ignored during the replication. If you choose an input other than `Y` or `y`, the replication task is not created.

## How do I view the state of TiCDC replication tasks?

To view the status of TiCDC replication tasks, use `cdc cli`. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --server=http://127.0.0.1:8300
```

The expected output is as follows:

```json
[{
    "id": "4e24dde6-53c1-40b6-badf-63620e4940dc",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

* `checkpoint`: TiCDC has replicated all data before this timestamp to downstream.
* `state`: The state of this replication task:
    * `normal`: The task runs normally.
    * `stopped`: The task is stopped manually or encounters an error.
    * `removed`: The task is removed.

> **Note:**
>
> This feature is introduced in TiCDC 4.0.3.

## What is `gc-ttl` in TiCDC?

Since v4.0.0-rc.1, PD supports external services in setting the service-level GC safepoint. Any service can register and update its GC safepoint. PD ensures that the key-value data later than this GC safepoint is not cleaned by GC.

When the replication task is unavailable or interrupted, this feature ensures that the data to be consumed by TiCDC is retained in TiKV without being cleaned by GC.

When starting the TiCDC server, you can specify the Time To Live (TTL) duration of GC safepoint by configuring `gc-ttl`. You can also [use TiUP to modify](/ticdc/deploy-ticdc.md#modify-ticdc-cluster-configurations-using-tiup) `gc-ttl`. The default value is 24 hours. In TiCDC, this value means:

- The maximum time the GC safepoint is retained at the PD after the TiCDC service is stopped.
- The maximum time a replication task can be suspended after the task is interrupted or manually stopped. If the time for a suspended replication task is longer than the value set by `gc-ttl`, the replication task enters the `failed` status, cannot be resumed, and cannot continue to affect the progress of the GC safepoint.

The second behavior above is introduced in TiCDC v4.0.13 and later versions. The purpose is to prevent a replication task in TiCDC from suspending for too long, causing the GC safepoint of the upstream TiKV cluster not to continue for a long time and retaining too many outdated data versions, thus affecting the performance of the upstream cluster.

> **Note:**
>
> In some scenarios, for example, when you use TiCDC for incremental replication after full replication with Dumpling/BR, the default 24 hours of `gc-ttl` may not be sufficient. You need to specify an appropriate value for `gc-ttl` when you start the TiCDC server.

## What is the complete behavior of TiCDC garbage collection (GC) safepoint?

If a replication task starts after the TiCDC service starts, the TiCDC owner updates the PD service GC safepoint with the smallest value of `checkpoint-ts` among all replication tasks. The service GC safepoint ensures that TiCDC does not delete data generated at that time and after that time. If the replication task is interrupted, or manually stopped, the `checkpoint-ts` of this task does not change. Meanwhile, PD's corresponding service GC safepoint is not updated either.

If the replication task is suspended longer than the time specified by `gc-ttl`, the replication task enters the `failed` status and cannot be resumed. The PD corresponding service GC safepoint will continue.

The Time-To-Live (TTL) that TiCDC sets for a service GC safepoint is 24 hours, which means that the GC mechanism does not delete any data if the TiCDC service can be recovered within 24 hours after it is interrupted.

## How to understand the relationship between the TiCDC time zone and the time zones of the upstream/downstream databases?

||Upstream time zone| TiCDC time zone|Downstream time zone|
| :-: | :-: | :-: | :-: |
| Configuration method | See [Time Zone Support](/configure-time-zone.md) | Configured using the `--tz` parameter when you start the TiCDC server |  Configured using the `time-zone` parameter in `sink-uri` |
| Description | The time zone of the upstream TiDB, which affects DML operations of the timestamp type and DDL operations related to timestamp type columns.| TiCDC assumes that the upstream TiDB's time zone is the same as the TiCDC time zone configuration, and performs related operations on the timestamp column.| The downstream MySQL processes the timestamp in the DML and DDL operations according to the downstream time zone setting.|

 > **Note:**
 >
 > Be careful when you set the time zone of the TiCDC server, because this time zone is used for converting the time type. Keep the upstream time zone, TiCDC time zone, and the downstream time zone consistent. The TiCDC server chooses its time zone in the following priority:
 >
 > - TiCDC first uses the time zone specified using `--tz`.
 > - When `--tz` is not available, TiCDC tries to read the time zone set using the `TZ` environment variable.
 > - When the `TZ` environment variable is not available, TiCDC uses the default time zone of the machine.

## What is the default behavior of TiCDC if I create a replication task without specifying the configuration file in `--config`?

If you use the `cdc cli changefeed create` command without specifying the `-config` parameter, TiCDC creates the replication task in the following default behaviors:

- Replicates all tables except system tables
- Only replicates tables that contain [valid indexes](/ticdc/ticdc-overview.md#best-practices)

## Does TiCDC support outputting data changes in the Canal format?

Yes. To enable Canal output, specify the protocol as `canal` in the `--sink-uri` parameter. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **Note:**
>
> * This feature is introduced in TiCDC 4.0.2.
> * TiCDC currently supports outputting data changes in the Canal format only to MQ sinks such as Kafka.

For more information, refer to [TiCDC changefeed configurations](/ticdc/ticdc-changefeed-config.md).

## Why does the latency from TiCDC to Kafka become higher and higher?

* Check [how do I view the state of TiCDC replication tasks](#how-do-i-view-the-state-of-ticdc-replication-tasks).
* Adjust the following parameters of Kafka:

    * Increase the `message.max.bytes` value in `server.properties` to `1073741824` (1 GB).
    * Increase the `replica.fetch.max.bytes` value in `server.properties` to `1073741824` (1 GB).
    * Increase the `fetch.message.max.bytes` value in `consumer.properties` to make it larger than the `message.max.bytes` value.

## When TiCDC replicates data to Kafka, can I control the maximum size of a single message in TiDB?

When `protocol` is set to `avro` or `canal-json`, messages are sent per row change. A single Kafka message contains only one row change and is generally no larger than Kafka's limit. Therefore, there is no need to limit the size of a single message. If the size of a single Kafka message does exceed Kakfa's limit, refer to [Why does the latency from TiCDC to Kafka become higher and higher?](/ticdc/ticdc-faq.md#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher).

When `protocol` is set to `open-protocol`, messages are sent in batches. Therefore, one Kafka message might be excessively large. To avoid this situation, you can configure the `max-message-bytes` parameter to control the maximum size of data sent to the Kafka broker each time (optional, `10MB` by default). You can also configure the `max-batch-size` parameter (optional, `16` by default) to specify the maximum number of change records in each Kafka message.

## If I modify a row multiple times in a transaction, will TiCDC output multiple row change events?

No. When you modify the same row in one transaction multiple times, TiDB only sends the latest modification to TiKV. Therefore, TiCDC can only obtain the result of the latest modification.

## When TiCDC replicates data to Kafka, does a message contain multiple types of data changes?

Yes. A single message might contain multiple `update`s or `delete`s, and `update` and `delete` might co-exist.

## When TiCDC replicates data to Kafka, how do I view the timestamp, table name, and schema name in the output of TiCDC Open Protocol?

The information is included in the key of Kafka messages. For example:

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

For more information, refer to [TiCDC Open Protocol event format](/ticdc/ticdc-open-protocol.md#event-format).

## When TiCDC replicates data to Kafka, how do I know the timestamp of the data changes in a message?

You can get the unix timestamp by moving `ts` in the key of the Kafka message by 18 bits to the right.

## How does TiCDC Open Protocol represent `null`?

In TiCDC Open Protocol, the type code `6` represents `null`.

| Type | Code | Output Example | Note |
|:--|:--|:--|:--|
| Null | 6 | `{"t":6,"v":null}` | |

For more information, refer to [TiCDC Open Protocol column type code](/ticdc/ticdc-open-protocol.md#column-type-code).

## How can I tell if a Row Changed Event of TiCDC Open Protocol is an `INSERT` event or an `UPDATE` event?

* `UPDATE` event contains both `"p"` and `"u"` fields
* `INSERT` event only contains the `"u"` field
* `DELETE` event only contains the `"d"` field

For more information, refer to [Open protocol Row Changed Event format](/ticdc/ticdc-open-protocol.md#row-changed-event).

## How much PD storage does TiCDC use?

TiCDC uses etcd in PD to store and regularly update the metadata. Because the time interval between the MVCC of etcd and PD's default compaction is one hour, the amount of PD storage that TiCDC uses is proportional to the amount of metadata versions generated within this hour. However, in v4.0.5, v4.0.6, and v4.0.7, TiCDC has a problem of frequent writing, so if there are 1000 tables created or scheduled in an hour, it then takes up all the etcd storage and returns the `etcdserver: mvcc: database space exceeded` error. You need to clean up the etcd storage after getting this error. See [etcd maintenance space-quota](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota) for details. It is recommended to upgrade your cluster to v4.0.9 or later versions.

## Does TiCDC support replicating large transactions? Is there any risk?

TiCDC provides partial support for large transactions (more than 5 GB in size). Depending on different scenarios, the following risks might exist:

- The latency of primary-secondary replication might greatly increase.
- When TiCDC's internal processing capacity is insufficient, the replication task error `ErrBufferReachLimit` might occur.
- When TiCDC's internal processing capacity is insufficient or the throughput capacity of TiCDC's downstream is insufficient, out of memory (OOM) might occur.

Since v6.2, TiCDC supports splitting a single-table transaction into multiple transactions. This can greatly reduce the latency and memory consumption of replicating large transactions. Therefore, if your application does not have a high requirement on transaction atomicity, it is recommended to enable the splitting of large transactions to avoid possible replication latency and OOM. To enable the splitting, set the value of the sink uri parameter [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) to `none`.

If you still encounter an error above, it is recommended to use BR to restore the incremental data of large transactions. The detailed operations are as follows:

1. Record the `checkpoint-ts` of the changefeed that is terminated due to large transactions, use this TSO as the `--lastbackupts` of the BR incremental backup, and execute [incremental data backup](/br/br-incremental-guide.md#back-up-incremental-data).
2. After backing up the incremental data, you can find a log record similar to `["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]` in the BR log output. Record the `BackupTS` in this log.
3. [Restore the incremental data](/br/br-incremental-guide.md#restore-incremental-data).
4. Create a new changefeed and start the replication task from `BackupTS`.
5. Delete the old changefeed.

## Does TiCDC replicate data changes caused by lossy DDL operations to the downstream?

Lossy DDL refers to DDL that might cause data changes when executed in TiDB. Some common lossy DDL operations include:

- Modifying the type of a column, for example, INT -> VARCHAR
- Modifying the length of a column, for example, VARCHAR(20) -> VARCHAR(10)
- Modifying the precision of a column, for example, DECIMAL(10, 3) -> DECIMAL(10, 2)
- Modifying the UNSIGNED or SIGNED attribute of a column, for example, INT UNSIGNED -> INT SIGNED

Before TiDB v7.1.0, TiCDC replicates DML events with identical old and new data to the downstream. When the downstream is MySQL, these DML events do not cause any data changes until the downstream receives and executes the DDL statement. However, when the downstream is Kafka or a cloud storage service, TiCDC writes a row of redundant data to the downstream.

Starting from TiDB v7.1.0, TiCDC eliminates these redundant DML events and no longer replicates them to downstream.

## The default value of the time type field is inconsistent when replicating a DDL statement to the downstream MySQL 5.7. What can I do?

Suppose that the `create table test (id int primary key, ts timestamp)` statement is executed in the upstream TiDB. When TiCDC replicates this statement to the downstream MySQL 5.7, MySQL uses the default configuration. The table schema after the replication is as follows. The default value of the `timestamp` field becomes `CURRENT_TIMESTAMP`:

{{< copyable "sql" >}}

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int(11) NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

From the result, you can see that the table schema before and after the replication is inconsistent. This is because the default value of `explicit_defaults_for_timestamp` in TiDB is different from that in MySQL. See [MySQL Compatibility](/mysql-compatibility.md#default-differences) for details.

Since v5.0.1 or v4.0.13, for each replication to MySQL, TiCDC automatically sets `explicit_defaults_for_timestamp = ON` to ensure that the time type is consistent between the upstream and downstream. For versions earlier than v5.0.1 or v4.0.13, pay attention to the compatibility issue caused by the inconsistent `explicit_defaults_for_timestamp` value when using TiCDC to replicate the time type data.

## Why do `INSERT`/`UPDATE` statements from the upstream become `REPLACE INTO` after being replicated to the downstream if I set `safe-mode` to `true` when I create a TiCDC replication task?

TiCDC guarantees that all data is replicated at least once. When there is duplicate data in the downstream, write conflicts occur. To avoid this problem, TiCDC converts `INSERT` and `UPDATE` statements into `REPLACE INTO` statements. This behavior is controlled by the `safe-mode` parameter.

In versions earlier than v6.1.3, `safe-mode` defaults to `true`, which means all `INSERT` and `UPDATE` statements are converted into `REPLACE INTO` statements. In v6.1.3 and later versions, TiCDC can automatically determine whether the downstream has duplicate data, and the default value of `safe-mode` changes to `false`. If no duplicate data is detected, TiCDC replicates `INSERT` and `UPDATE` statements without conversion.

## When the sink of the replication downstream is TiDB or MySQL, what permissions do users of the downstream database need?

When the sink is TiDB or MySQL, the users of the downstream database need the following permissions:

- `Select`
- `Index`
- `Insert`
- `Update`
- `Delete`
- `Create`
- `Drop`
- `Alter`
- `Create View`

If you need to replicate `recover table` to the downstream TiDB, you should have the `Super` permission.

## Why does TiCDC use disks? When does TiCDC write to disks? Does TiCDC use memory buffer to improve replication performance?

When upstream write traffic is at peak hours, the downstream may fail to consume all data in a timely manner, resulting in data pile-up. TiCDC uses disks to process the data that is piled up. TiCDC needs to write data to disks during normal operation. However, this is not usually the bottleneck for replication throughput and replication latency, given that writing to disks only results in latency within a hundred milliseconds. TiCDC also uses memory to accelerate reading data from disks to improve replication performance.

## Why does replication using TiCDC stall or even stop after data restore using TiDB Lightning and BR from upstream?

Currently, TiCDC is not yet fully compatible with TiDB Lightning and BR. Therefore, please avoid using TiDB Lightning and BR on tables that are replicated by TiCDC.

## After a changefeed resumes from pause, its replication latency gets higher and higher and returns to normal only after a few minutes. Why?

When a changefeed is resumed, TiCDC needs to scan the historical versions of data in TiKV to catch up with the incremental data logs generated during the pause. The replication process proceeds only after the scan is completed. The scan process might take several to tens of minutes.

## How should I deploy TiCDC to replicate data between two TiDB cluster located in different regions?

For TiCDC versions earlier than v6.5.2, it is recommended that you deploy TiCDC in the downstream TiDB cluster. If the network latency between the upstream and downstream is high, for example, more than 100 ms, the latency produced when TiCDC executes SQL statements to the downstream might increase dramatically due to the MySQL transmission protocol issues. This results in a decrease in system throughput. However, deploying TiCDC in the downstream can greatly ease this problem. After optimization, starting from TiCDC v6.5.2, it is recommended that you deploy TiCDC in the upstream TiDB cluster.

## What is the order of executing DML and DDL statements?

The execution order is: DML -> DDL -> DML. To ensure that the table schema is correct when DML events are executed downstream during data replication, it is necessary to coordinate the execution order of DDL and DML statements. Currently, TiCDC adopts a simple approach: it replicates all DML statements before the DDL ts to downstream first, and then replicates DDL statements.

## How should I check whether the upstream and downstream data is consistent?

If the downstream is a TiDB cluster or MySQL instance, it is recommended that you compare the data using [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md).

## Replication of a single table can only be run on a single TiCDC node. Will it be possible to use multiple TiCDC nodes to replicate data of multiple tables?

This feature is currently not supported, which might be supported in a future release. By then, TiCDC might replicate data change logs by TiKV Region, which means scalable processing capability.

## Does TiCDC replication get stuck if the upstream has long-running uncommitted transactions?

TiDB has a transaction timeout mechanism. When a transaction runs for a period longer than [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl), TiDB forcibly rolls it back. TiCDC waits for the transaction to be committed before proceeding with the replication, which causes replication delay.

## Why can't I use the `cdc cli` command to operate a TiCDC cluster deployed by TiDB Operator?

This is because the default port number of the TiCDC cluster deployed by TiDB Operator is `8301`, while the default port number of the `cdc cli` command to connect to the TiCDC server is `8300`. When using the `cdc cli` command to operate the TiCDC cluster deployed by TiDB Operator, you need to explicitly specify the `--server` parameter, as follows:

```shell
./cdc cli changefeed list --server "127.0.0.1:8301"
[
  {
    "id": "4k-table",
    "namespace": "default",
    "summary": {
      "state": "stopped",
      "tso": 441832628003799353,
      "checkpoint": "2023-05-30 22:41:57.910",
      "error": null
    }
  },
  {
    "id": "big-table",
    "namespace": "default",
    "summary": {
      "state": "normal",
      "tso": 441872834546892882,
      "checkpoint": "2023-06-01 17:18:13.700",
      "error": null
    }
  }
]
```
