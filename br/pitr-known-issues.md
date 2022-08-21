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

- PITR 恢复出现 OOM，是由于待恢复的日志区间过大。
    - 一般建议恢复的日志区间不超过 2 天，最长不超过一周。即在 PITR 备份过过程中至少 2 天或一周至少做一次全量备份操作。
- 删除日志时出现 OOM，是由于删除的日志区间过大。
    - 遇到此问题，解决方法是先减小删除的日志区间，可通过多次删除小区间日志来替代掉需要删除的大区间日志。
- br 进程所在的节点内存配置过低。
    - 建议升级节点内存配置到至少 16 GB，确保 PITR 恢复有足够的内存资源。

## 上游数据库使用 TiDB Lightning Physical 方式导入数据，导致无法使用日志备份功能

目前日志备份功能还没有完全适配 TiDB Lightning，导致 TiDB Lightning Physical 方式导入的数据无法备份到日志中。

在创建日志备份任务的上游集群中，请尽量避免使用 TiDB Lightning Physical 方式导入数据。可以选择使用 TiDB Lightning Logical 方式导入数据。若确实需要使用 Physical 导入方式，可在导入完成之后做一次全量备份操作，这样，PITR 就可以恢复到全量备份之后的时间点。

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
