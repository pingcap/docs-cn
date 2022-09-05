---
title: 日志备份故障处理
summary: 了解日志备份常见故障以及解决方法。
---

# 日志备份故障处理

本文列出了在使用日志备份功能时，可能会遇到的故障及相应的解决方法。

如果遇到未包含在此文档且无法解决的问题，可以在 [AskTUG](https://asktug.com/) 社区中搜索答案或提问。

## 在使用 `br restore point` 命令恢复下游集群后，无法从 TiFlash 引擎中查询到数据，该如何处理？

在 v6.2.0 版本中，使用 PITR 功能恢复下游集群数据时，并不支持恢复下游的 TiFlash 副本。恢复数据之后，需要执行如下命令手动设置 schema 或 table 的 TiFlash 副本：

``` shell
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

## 日志备份任务的 `status` 变为 `ERROR`，该如何处理？

在运行日志备份过程中，遇到错误后经过重试也无法恢复的故障场景，任务会被设置为 `ERROR` 状态，如：

``` shell
br log status --pd x.x.x.x:2379

● Total 1 Tasks.
> #1 <
                    name: task1
                  status: ○ ERROR
                   start: 2022-07-25 13:49:02.868 +0000
                     end: 2090-11-18 14:07:45.624 +0000
                 storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
             speed(est.): 0.00 ops/s
      checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=11h31m29s
          error[store=1]: KV:LogBackup:RaftReq
error-happen-at[store=1]: 2022-07-25 14:54:44.467 +0000; gap=11h23m35s
  error-message[store=1]: retry time exceeds: and error failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }
```

此时，你需要根据错误提示来确认故障的原因并恢复故障。确认故障恢复之后，可执行下面的命令来恢复备份任务：

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

备份任务恢复后，再次查询 `br log status`，任务状态变为正常，备份任务继续执行。

```shell
● Total 1 Tasks.
> #1 <
              name: task1
            status: ● NORMAL
             start: 2022-07-25 13:49:02.868 +0000
               end: 2090-11-18 14:07:45.624 +0000
           storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
       speed(est.): 15509.75 ops/s
checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=6m28s
```

> **注意：**
>
> 由于此功能会备份集群的多版本数据，当任务发生错误且状态变更为 `ERROR` 时，同时会将当前任务的备份进度点的数据设为一个 `safe point`，`safe point` 的数据将保证 24 小时不被 GC 掉。所以，当任务恢复之后，会从上一个备份点继续备份日志。如果任务失败时间超过 24 小时，前一次备份进度点的数据就已经 GC，此时恢复任务操作会提示失败。这种场景下，只能执行 `br log stop` 命令先停止本次任务，然后重新开启新的备份任务。

## 执行 `br log resume` 命令恢复处于暂停状态的任务时报 `ErrBackupGCSafepointExceeded` 错误，该如何处理？

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

暂停日志备份任务后，备份程序为了防止生成变更日志的 MVCC 数据被 GC，暂停任务程序会自动将当前备份点 checkpoint 设置为 service safepoint，允许保留最近 24 小时内的 MVCC 数据。当超过 24 小时后，备份点 checkpoint 的 MVCC 数据已经被 GC，此时程序会拒绝恢复备份任务。

此场景的处理办法是：先执行 `br log stop` 命令来删除当前的任务，然后执行 `br log start` 重新创建新的日志备份任务，同时做一个全量备份，便于后续做 PITR 恢复操作。

## 日志备份过程中执行分区交换 (Exchange Partition) DDL，在 PITR 恢复时会报错，该如何处理？

在执行 PITR 恢复日志过程中，出现如下报错：

```shell
restore of ddl `exchange-table-partition` is not supported
```

因为当前 v6.2.0 版本的日志备份功能尚且不兼容分区交换 (Exchange Partition) DDL，在使用日志备份功能时，应尽量避免执行分区交换 DDL。如果已经执行此 DDL，需要立即做一次全量备份操作，PITR 即可恢复本次全量备份点之后的日志数据。
