---
title: TiDB Log Backup and PITR Architecture
summary: Learn about the architecture of TiDB log backup and point-in-time recovery.
---

# TiDB Log Backup and PITR Architecture

This document introduces the architecture and process of TiDB log backup and point-in-time recovery (PITR) using a Backup & Restore (BR) tool as an example.

## Architecture

The log backup and PITR architecture is as follows:

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

## Process of log backup

The process of a cluster log backup is as follows:

![BR log backup process design](/media/br/br-log-backup-ts.png)

System components and key concepts involved in the log backup process:

* **local metadata**: indicates the metadata backed up by a single TiKV node, including local checkpoint ts, global checkpoint ts, and backup file information.
* **local checkpoint ts** (in local metadata): indicates that all logs generated before local checkpoint ts in this TiKV node have been backed up to the target storage.
* **global checkpoint ts**: indicates that all logs generated before global checkpoint ts in all TiKV nodes have been backed up to the target storage. TiDB Coordinator calculates this timestamp by collecting local checkpoint ts of all TiKV node and then reports it to PD.
* **TiDB Coordinator**: a TiDB node is elected as the coordinator, which is responsible for collecting and calculating the progress of the entire log backup task (global checkpoint ts). This component is stateless in design, and after its failure, a new Coordinator is elected from the surviving TiDB nodes.
* **TiKV log backup observer**: runs on each TiKV node in the TiDB cluster, which is responsible for backing up log data. If a TiKV node fails, backing up the data range on it will be taken by other TiKV nodes after region re-election, and these nodes will back up data of the failure range starting from global checkpoint ts.

The complete backup process is as follows:

1. BR receives the `br log start` command.

   * BR parses the checkpoint ts (the start time of log backup) and storage path of the backup task.
   * **Register log backup task**: BR registers a log backup task in PD.

2. TiKV monitors the creation and update of the log backup task.

   * **Fetch log backup task**: The log backup observer of each TiKV node fetches the log backup task from PD and then backs up the log data in the specified range.

3. The log backup observer backs up the KV change logs continuously.

   * **Read kv change data**: reads KV change data and then saves the change log to [backup files in custom format](#log-backup-files).
   * **Fetch global checkpoint ts**: fetches the global checkpoint ts from PD.
   * **Generate local metadata**: generates the local metadata of the backup task, including local checkpoint ts, global checkpoint ts, and backup file information.
   * **Upload log data & metadata**: uploads the backup files and local metadata to the target storage periodically.
   * **Configure GC**: requests PD to prevent data that have not been backed up (greater than local checkpoint ts) from being recycled by the [TiDB GC mechanism](/garbage-collection-overview.md).

4. The TiDB Coordinator monitors the progress of the log backup task.

   * **Watch backup progress**: gets the backup progress of each Region (Region checkpoint ts) by polling all TiKV nodes.
   * **Report global checkpoint ts**: calculates the progress of the entire log backup task (global checkpoint ts) based on the Region checkpoint ts and then reports the global checkpoint ts to PD.

5. PD persists the status of the log backup task, and you can view it using `br log status`.

## Process of PITR

The process of PITR is as follows:

![Point-in-time recovery process design](/media/br/pitr-ts.png)

The complete PITR process is as follows:

1. BR receives the `br restore point` command.

   * BR parses the full backup data address, log backup data address, and the point-in-time recovery time.
   * Queries the restore object (database or table) in the backup data and checks whether the table to be restored exists and meets the restore requirements.

2. BR restores the full backup data.

   * Restores full backup data. For more details about the process of snapshot backup data restore, refer to [Restore snapshot backup data](/br/br-snapshot-architecture.md#process-of-restore).

3. BR restores the log backup data.

   * **Read backup data**: reads the log backup data and calculates the log backup data that needs to be restored.
   * **Fetch Region info**: fetches all Regions distributions by accessing PD.
   * **Request TiKV to restore data**: creates a log restore request and sends it to the corresponding TiKV node. The log restore request contains the log backup data information to be restored.

4. TiKV accepts the restore request from BR and initiates a log restore worker.

   * The log restore worker gets the log backup data that needs to be restored.

5. TiKV restores the log backup data.

   * **Download KVs**: the log restore worker downloads the corresponding backup data from the backup storage to a local directory according to the log restore request.
   * **Rewrite KVs**: the log restore worker rewrites the KV data of the backup data according to the table ID of the restore cluster table, that is, replace the original table ID in the [Key-Value](/tidb-computing.md#mapping-table-data-to-key-value) with the new table ID. The restore worker also rewrites the index ID in the same way.
   * **Apply KVs**: the log restore worker writes the processed KV data to the store (RocksDB) through the raft interface.
   * **Report restore result**: the log restore worker returns the restore result to BR.

6. BR receives the restore result from each TiKV node.

   * If some data fails to be restored due to `RegionNotFound` or `EpochNotMatch`, for example, a TiKV node is down, BR will retry the restore.
   * If there is any data fails to be restored and cannot be retried, the restore task fails.
   * After all data is restored, the restore task succeeds.

## Log backup files

Log backup generates the following types of files:

- `{min_ts}-{uuid}.log` file: stores the KV change log data of the backup task. The `{min_ts}` is the minimum TSO timestamp of the KV change log data in the file, and the `{uuid}` is generated randomly when the file is created.
- `{checkpoint_ts}-{uuid}.meta` file: is generated every time each TiKV node uploads the log backup data and stores metadata of all log backup data files uploaded this time. The `{checkpoint_ts}` is the log backup checkpoint of the TiKV node, and the global checkpoint is the minimum checkpoint of all TiKV nodes. The `{uuid}` is generated randomly when the file is created.
- `{store_id}.ts` file: this file is updated with global checkpoint ts every time each TiKV node uploads the log backup data. The `{store_id}` is the store ID of the TiKV node.
- `v1_stream_truncate_safepoint.txt` file: stores the timestamp corresponding to the latest backup data in storage that deleted by `br log truncate`.

### Structure of backup files

```
.
├── v1
│   ├── backupmeta
│   │   ├── {min_restored_ts}-{uuid}.meta
│   │   ├── {checkpoint}-{uuid}.meta
│   ├── global_checkpoint
│   │   ├── {store_id}.ts
│   ├── {date}
│   │   ├── {hour}
│   │   │   ├── {store_id}
│   │   │   │   ├── {min_ts}-{uuid}.log
│   │   │   │   ├── {min_ts}-{uuid}.log
├── v1_stream_truncate_safepoint.txt
```

The following is an example:

```
.
├── v1
│   ├── backupmeta
│   │   ├── ...
│   │   ├── 435213818858112001-e2569bda-a75a-4411-88de-f469b49d6256.meta
│   │   ├── 435214043785779202-1780f291-3b8a-455e-a31d-8a1302c43ead.meta
│   │   ├── 435214443785779202-224f1408-fff5-445f-8e41-ca4fcfbd2a67.meta
│   ├── global_checkpoint
│   │   ├── 1.ts
│   │   ├── 2.ts
│   │   ├── 3.ts
│   ├── 20220811
│   │   ├── 03
│   │   │   ├── 1
│   │   │   │   ├── ...
│   │   │   │   ├── 435213866703257604-60fcbdb6-8f55-4098-b3e7-2ce604dafe54.log
│   │   │   │   ├── 435214023989657606-72ce65ff-1fa8-4705-9fd9-cb4a1e803a56.log
│   │   │   ├── 2
│   │   │   │   ├── ...
│   │   │   │   ├── 435214102632857605-11deba64-beff-4414-bc9c-7a161b6fb22c.log
│   │   │   │   ├── 435214417205657604-e6980303-cbaa-4629-a863-1e745d7b8aed.log
│   │   │   ├── 3
│   │   │   │   ├── ...
│   │   │   │   ├── 435214495848857605-7bf65e92-8c43-427e-b81e-f0050bd40be0.log
│   │   │   │   ├── 435214574492057604-80d3b15e-3d9f-4b0c-b133-87ed3f6b2697.log
├── v1_stream_truncate_safepoint.txt
```
