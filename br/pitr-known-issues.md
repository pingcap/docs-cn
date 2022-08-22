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

## 使用自建的 Minio 系统作为日志备份的存储，执行 `br restore point` 或者 `br log truncate` 出现 `RequestCanceled` 错误

Issue 链接：[#36515](https://github.com/pingcap/tidb/issues/36515)

```shell
[error="RequestCanceled: request context canceled\ncaused by: context canceled"]
```

出现此错误的原因是，当前日志备份会产生大量小文件，自建的 Minio 存储系统的支持能力不能满足当前日志备份功能的需求。

如需解决该问题，需要将 Minio 系统升级到更大规模的分布式集群，或者直接使用 Amazon S3 存储系统作为日志备份的存储。

## 集群负载过高，Region 过多，存储达到性能瓶颈（比如使用自建的 Minio 系统作为日志备份的存储）等情况下，备份进度 checkpoint 延迟可能超过 10 分钟

Issue 链接：[#13030](https://github.com/tikv/tikv/issues/13030)

因为日志备份会产生大量小文件，而自建的 Minio 系统在规模上难以支撑日志备份对于大量小文件的写入需求，导致备份进度缓慢。

如需解决该问题，需将 Minio 系统升级到更大规模，或者直接使用 Amazon S3 存储系统作为日志备份的存储。

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
