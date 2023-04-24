---
title: Checkpoint Restore
summary: Learn about the checkpoint restore feature, including its application scenarios, implementation details, and usage.
---

# Checkpoint Restore

Snapshot restore or log restore might be interrupted due to recoverable errors, such as disk exhaustion and node crash. Before TiDB v7.1.0, the recovery progress before the interruption would be invalidated even after the error is addressed, and you need to start the restore from scratch. For large clusters, this incurs considerable extra cost.

Starting from TiDB v7.1.0, Backup & Restore (BR) introduces the checkpoint restore feature, which enables you to continue an interrupted restore. This feature can retain most recovery progress of the interrupted restore.

## Application scenarios

If your TiDB cluster is large and cannot afford to restore again after a failure, you can use the checkpoint restore feature. The br command-line tool (hereinafter referred to as `br`) periodically records the shards that have been restored. In this way, the next restore retry can use a recovery progress point close to the abnormal exit.

## Implementation details

The implementation of checkpoint restore is divided into two parts: snapshot restore and log restore.

### Snapshot restore

The implementation of snapshot restore is similar to [snapshot backup](/br/br-checkpoint-backup.md#implementation-details). `br` restores all SST files within a key range (Region) in batches. After completing a restore, `br` records this range and the table ID of the restored cluster table. The checkpoint restore feature periodically uploads the new restore information to external storage so that the key ranges that have been restored can be persisted.

When `br` retries a restore, it reads the key ranges that have been restored from external storage, and matches them with the corresponding table ID. During the restore, `br` skips any key ranges that overlap with those recorded in the checkpoint restore, and that have the same table ID.

If you delete tables before `br` retries the restore, the table ID of the newly created table during the retry will be different from the previously recorded table ID in the checkpoint restore. In this case, `br` bypasses the previous checkpoint restore information and restores the table again. This means that the same table with a new ID disregards the old ID's checkpoint restore information and records the new checkpoint restore information corresponding to the new ID.

Due to the use of the MVCC (Multi-Version Concurrency Control) mechanism, data with specified timestamps can be written unordered and repeatedly.

When restoring database or table DDLs using snapshot restore, the `ifExists` parameter is added. For existing databases or tables that are already considered created, `br` automatically skips the restore.

### Log restore

Log restore is the process of restoring data metadata backed up by TiKV nodes (meta-kv) in the order of timestamps. The checkpoint restore first establishes a one-to-one ID mapping relationship between the backup cluster and the restored cluster based on the meta-kv data. This ensures that the ID of meta-kv remains consistent across different restore retries, enabling meta-kv to be restored again.

Unlike snapshot backup files, the range of log backup files might overlap. Thus, the key range cannot be used directly as recovery progress metadata. Additionally, there might be a large number of log backup files. However, each log backup file has a fixed position in the log backup metadata. This means that a unique position in the log backup metadata can be assigned to each log backup file as recovery progress metadata.

The log backup metadata contains an array of file metadata. Each file metadata in the array represents a file composed of multiple log backup files. The file metadata records the offset and size of a log backup file in the concatenated file. Therefore, `br` can use the triple `(log backup metadata name, file metadata array offset, log backup file array offset)` to uniquely identify a log backup file.

## Usage limitations

Checkpoint restore relies on the GC mechanism and cannot record all data that has been restored. The following sections provide the details.

### GC will be paused

During a log restore, the order of the restored data is unordered, which means that the deletion record of a key might be restored before its write record. If GC is triggered at this time, all data of the key will be deleted and then GC cannot process subsequent write records of the key. To avoid this situation, `br` pauses GC during log restore. If `br` exits halfway, GC remains paused.

After the log restore is completed, GC is restarted automatically without manual startup. However, if you decide not to continue the restore, you can manually enable GC as follows:

The principle of `br` pausing GC is to execute `SET config tikv gc.ratio-threshold = -1.0` to set `gc.ratio-threshold` to a negative number, thus pausing GC. You can manually enable GC by modifying the value of [`gc.ratio-threshold`](/tikv-configuration-file.md#ratio-threshold). For example, to reset to its default value, you can execute `SET config tikv gc.ratio-threshold = 1.1`.

### Some data needs to be restored again

When `br` retries a restore, some data that has been restored might need to be restored again, including the data being restored and the data not recorded by the checkpoint.

- If the interruption is caused by an error, `br` persists the meta information of the data restored before exit. In this case, only the data being restored needs to be restored again in the next retry.

- If the `br` process is interrupted by the system, `br` cannot persist the meta information of the data restored to the external storage. Since `br` persists the meta information every 30 seconds, data restored in the last 30 seconds before interruption cannot be persisted and needs to be restored again in the next retry.

### Avoid modifying cluster data during the restore

After a restore failure, avoid writing, deleting, or creating tables in the cluster. This is because the backup data might contain DDL operations for renaming tables. If you modify the cluster data, the checkpoint restore cannot decide whether the deleted or existing table are resulted from external operations, which affects the accuracy of the next restore retry.
