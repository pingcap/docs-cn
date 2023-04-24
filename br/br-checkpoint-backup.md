---
title: Checkpoint Backup
summary: Learn about the checkpoint backup feature, including its application scenarios, implementation details, and usage.
aliases: ["/tidb/dev/br-checkpoint"]
---

# Checkpoint Backup

Snapshot backup might be interrupted due to recoverable errors, such as disk exhaustion and node crash. Before TiDB v6.5.0, data that is backed up before the interruption would be invalidated even after the error is addressed, and you need to start the backup from scratch. For large clusters, this incurs considerable extra cost.

In TiDB v6.5.0, Backup & Restore (BR) introduces the checkpoint backup feature to allow continuing an interrupted backup. This feature can retain most data of the interrupted backup.

## Application scenarios

If your TiDB cluster is large and cannot afford to back up again after a failure, you can use the checkpoint backup feature. The br command-line tool (hereinafter referred to as `br`) periodically records the shards that have been backed up. In this way, the next backup retry can use the backup progress close to the abnormal exit.

## Implementation details

During a snapshot backup, `br` encodes the tables into the corresponding key space, and generates backup RPC requests before sending them to TiKV nodes. After receiving the backup request, TiKV nodes back up the data within the requested range. Every time a TiKV node finishes backing up data of a Region, it returns the backup information of this range to `br`.

`br` records the information returned by TiKV nodes, which helps `br` get the key ranges that have been backed up. The checkpoint backup feature periodically uploads the new backup information to external storage so that the key ranges that have been backed up can be persisted.

When `br` retries the backup, it reads the key ranges that have been backed up from external storage, and compares them with the key ranges of the backup task. The differential data helps `br` to determine the key range that still needs to be backed up in checkpoint backup.

## Usage limitations

Checkpoint backup relies on the GC mechanism and cannot recover all data that has been backed up. The following sections provide the details.

### Backup retry must be prior to GC

During the backup, `br` periodically updates the `gc-safepoint` of the backup snapshot in PD to avoid data being garbage collected. When `br` exits, the `gc-safepoint` cannot be updated in time. As a result, before the next backup retry, the data might have been garbage collected.

To avoid this situation, `br` keeps the `gc-safepoint` for about one hour by default when `gcttl` is not specified. You can set the `gcttl` parameter to extend the retention period if needed .

The following example sets `gcttl` to 15 hours (54000 seconds) to extend the retention period of `gc-safepoint`:

```shell
br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" \
--gcttl 54000
```

> **Note:**
>
> The `gc-safepoint` created before backup is deleted after the snapshot backup is completed. You do not need to delete it manually.

### Some data needs to be backed up again

When `br` retries backup, some data that has been backed up might need to be backed up again, including the data being backed up and the data not recorded by the checkpoint.

- If the interruption is caused by an error, `br` will persist the meta information of the data backed up before exit. In this case, only the data being backed up needs to be backed up again in the next retry.

- If the `br` process is interrupted by the system, `br` cannot persist the meta information of the data backed up to the external storage. Since `br` persists the meta information every 30 seconds, data backed up in the last 30 seconds before interruption cannot be persisted and needs to be backed up again in the next retry.
