---
title: Changefeed Overview
summary: Learn basic concepts, state definitions, and state transfer of changefeeds.
---

# Changefeed Overview

A changefeed is a replication task in TiCDC, which replicates the data change logs of specified tables in a TiDB cluster to the designated downstream. You can run and manage multiple changefeeds in a TiCDC cluster.

## Changefeed state transfer

The state of a replication task represents the running status of the replication task. During the running of TiCDC, replication tasks might fail with errors, be manually paused, resumed, or reach the specified `TargetTs`. These behaviors can lead to the change of the replication task state. This section describes the states of TiCDC replication tasks and the transfer relationships between states.

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

The states in the preceding state transfer diagram are described as follows:

- `Normal`: The replication task runs normally and the checkpoint-ts proceeds normally.
- `Stopped`: The replication task is stopped, because the user manually pauses the changefeed. The changefeed in this state blocks GC operations.
- `Error`: The replication task returns an error. The replication cannot continue due to some recoverable errors. The changefeed in this state keeps trying to resume until the state transfers to `Normal`. The changefeed in this state blocks GC operations.
- `Finished`: The replication task is finished and has reached the preset `TargetTs`. The changefeed in this state does not block GC operations.
- `Failed`: The replication task fails. Due to some unrecoverable errors, the replication task cannot resume and cannot be recovered. The changefeed in this state does not block GC operations.

The numbers in the preceding state transfer diagram are described as follows.

- ① Run the `changefeed pause` command.
- ② Run the `changefeed resume` command to resume the replication task.
- ③ Recoverable errors occur during the `changefeed` operation, and the operation is resumed automatically.
- ④ Run the `changefeed resume` command to resume the replication task.
- ⑤ Unrecoverable errors occur during the `changefeed` operation.
- ⑥ `changefeed` has reached the preset `TargetTs`, and the replication is automatically stopped.
- ⑦ `changefeed` suspended longer than the duration specified by `gc-ttl`, and cannot be resumed.
- ⑧ `changefeed` experienced an unrecoverable error when trying to execute automatic recovery.

## Operate changefeeds

You can manage a TiCDC cluster and its replication tasks using the command-line tool `cdc cli`. For details, see [Manage TiCDC changefeeds](/ticdc/ticdc-manage-changefeed.md).

You can also use the HTTP interface (the TiCDC OpenAPI feature) to manage a TiCDC cluster and its replication tasks. For details, see [TiCDC OpenAPI](/ticdc/ticdc-open-api.md).

If your TiCDC is deployed using TiUP, you can start `cdc cli` by running the `tiup ctl:v<CLUSTER_VERSION> cdc` command. Replace `v<CLUSTER_VERSION>` with the TiCDC cluster version, such as `v6.5.0`. You can also run `cdc cli` directly.
