---
title: 日志备份的已知问题
summary: 了解日志备份的已知问题。
---

# 日志备份的已知问题

本文列出了在使用日志备份功能时，可能会遇到的问题及相应的解决方法。

如果遇到未包含在此文档且无法解决的问题，可以在 [AskTUG](https://asktug.com/) 社区中搜索答案或提问。

## BR 进程在执行 PITR 恢复或执行 `br log truncate` 命令时出现 OOM 问题

Issue 链接：[#36648](https://github.com/pingcap/tidb/issues/36648)

执行 PITR 恢复时遇到 BR OOM 问题，从以下几点考虑：

- PITR 恢复出现 OOM，是由于待恢复的索引日志数据过多，以下是两个典型场景。
    - 恢复日志区间过大
        - 建议恢复的日志区间不超过 2 天，最长不超过一周。即在 PITR 备份过程中，最好每 2 天做一次快照备份操作。
    - 备份日志期间，存在长时间大量写入。
        - 长时间大量写入的场景一般出现在初始化集群全量导入数据的阶段。建议在导入完成后进行一次快照备份，使用该备份进行恢复。
- 删除日志时出现 OOM，是由于删除的日志区间过大。
    - 遇到此问题，解决方法是先减小删除的日志区间，可通过多次删除小区间日志来替代掉需要删除的大区间日志。
- br 进程所在的节点内存配置过低。
    - 建议升级节点内存配置到至少 16 GB，确保 PITR 恢复有足够的内存资源。

## 上游数据库使用 TiDB Lightning Physical 方式导入数据，导致无法使用日志备份功能

目前日志备份功能还没有完全适配 TiDB Lightning，导致 TiDB Lightning Physical 方式导入的数据无法备份到日志中。

在创建日志备份任务的上游集群中，请尽量避免使用 TiDB Lightning Physical 方式导入数据。可以选择使用 TiDB Lightning Logical 方式导入数据。若确实需要使用 Physical 导入方式，可在导入完成之后做一次快照备份操作，这样，PITR 就可以恢复到快照备份之后的时间点。

## 集群已经恢复了网络分区故障，日志备份任务进度 checkpoint 仍然不推进

Issue 链接：[#13126](https://github.com/tikv/tikv/issues/13126)

在集群出现网络分区故障后，备份任务难以继续备份日志，并且在超过一定的重试时间后，任务会被置为 `ERROR` 状态。此时备份任务已经停止，需要手动执行 `br log resume` 命令来恢复日志备份任务。

## 日志备份实际消耗的存储是集群监控显示的数据增量的 2~3 倍

Issue 链接：[#13306](https://github.com/tikv/tikv/issues/13306)

这是由于集群监控显示的是 RocksDB 压缩后的数据，而日志备份使用的是自定义的编码方式存储 KV 数据，因此造成压缩比率不一致，大约是 2~3 倍之间。日志备份没有使用 RocksDB 生成 SST 文件的方式存储数据，是因为日志备份期间生成的数据会遇到区间范围过大而实际区间内容较少的情况。这个情况下，通过 ingest SST 的方式恢复数据，并不能有效提升恢复性能。

## 执行 PITR 恢复时遇到 `execute over region id` 报错

Issue 链接：[#37207](https://github.com/pingcap/tidb/issues/37207)

该场景发生在全量数据导入时开启了日志备份，并使用 PITR 恢复全量导入时间段的日志。经过测试发现，当存在长时间（24 小时）大量热点写入，且平均单台 TiKV 节点写入 OPS > 50k/s（可以通过 Grafana 中 **TiKV-Details** -> **Backup Log** -> **Handle Event Rate** 确认该数值），那么有几率会遇到这个情况。

- 当前版本中建议在集群初始化后，进行一次有效快照备份，并且以此作为基础进行 PITR 恢复。

## 当存在大事务的时候，事务的提交时间会影响日志备份 checkpoint lag

Issue 链接：[#13304](https://github.com/tikv/tikv/issues/13304)

当场景中有大事务时，日志 checkpoint lag 在事务提交前都不会更新，因此会增加一段接近于大事务提交时长的时间。

## 索引加速功能与 PITR 功能不兼容

Issue 链接：[#38045](https://github.com/pingcap/tidb/issues/38045)

当前[索引加速功能](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)与 PITR 功能不兼容。在使用索引加速功能时，需要确保后台没有启动 PITR 备份任务，否则可能会出现非预期结果。非预期场景包括：

- 如果先启动 PITR 备份任务，再添加索引，此时即使索引加速功能打开，也不会使用加速索引功能，但不影响索引兼容性。
- 如果先启动添加索引加速任务，再创建 PITR 备份任务，此时 PITR 备份任务会报错，但不影响正在添加索引的任务。
- 如果同时启动 PITR 备份任务和添加索引加速任务，可能会由于两个任务无法察觉到对方而导致 PITR 不能成功备份增加的索引数据。

## 在 GCS 或 Azure Blob Storage 上第一次执行 `PITR Truncate` 命令时报错

Issue 链接：[#38229](https://github.com/pingcap/tidb/issues/38229)

在 GCS 或 Azure Blob Storage 上**第一次**执行 `PITR Truncate` 时会提示文件 `v1_stream_trancate_safepoint.txt` 不存在。有如下两种解决方法：

- 方法一：在 PITR 的备份根目录下，创建文件 `v1_stream_trancate_safepoint.txt`，然后写入 `0`。注意该文件不得包含其他字符。在第一次执行 `PITR Truncate` 命令时，添加该文件即可。
- 方法二：使用 v6.4.0 及以上版本的 BR。
