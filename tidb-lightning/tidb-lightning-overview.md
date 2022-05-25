---
title: TiDB Lightning 简介
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-overview/','/docs-cn/dev/reference/tools/tidb-lightning/overview/','/docs-cn/tools/lightning/overview-architecture/','/docs-cn/dev/tidb-lightning/tidb-lightning-backends/']
---

# TiDB Lightning 简介

TiDB Lightning 是用于从静态文件导入 TB 级数据到 TiDB 集群的工具，常用于 TiDB 集群的初始化数据导入。

要快速了解 Lightning 的基本原理和使用方法，建议先观看下面的培训视频（时长 32 分钟）。注意本视频只为学习参考，具体操作步骤和最新功能，请以文档内容为准。

<video src="https://tidb-docs.s3.us-east-2.amazonaws.com/compressed+-+Lesson+19.mp4" width="600px" height="450px" controls="controls" poster="https://tidb-docs.s3.us-east-2.amazonaws.com/thumbnail+-+lesson+19.png"></video>

TiDB Lightning 支持以下文件类型：

- [Dumpling](/dumpling-overview.md) 生成的文件
- CSV 文件
- [Amazon Aurora 生成的 Apache Parquet 文件](/migrate-aurora-to-tidb.md)

TiDB Lightning 支持从以下位置读取：

- Local filesystem
- [Amazon S3](/br/backup-and-restore-storages.md#s3-的-url-参数)
- [Google GCS](/br/backup-and-restore-storages.md#gcs-的-url-参数)

## TiDB Lightning 整体架构

![TiDB Lightning 整体架构](/media/tidb-lightning-architecture.png)

TiDB Lightning 目前支持两种导入方式，通过`backend`配置区分。不同的模式决定 TiDB Lightning 如何将数据导入到目标 TiDB 集群。

- [SST Mode](/tidb-lightning/tidb-lightning-sst-mode.md)：TiDB Lightning 首先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对上传到各个 TiKV 节点，最后调用 TiKV Ingest 接口将数据插入到 TiKV 的 RocksDB 中。如果用于初始化导入，请优先考虑使用 SST 模式，其拥有较高的导入速度。

- [SQL Mode](/tidb-lightning/tidb-lightning-sql-mode.md)：TiDB Lightning 先将数据编码成 SQL，然后直接运行这些 SQL 语句进行数据导入。如果需要导入的集群为生产环境线上集群，或需要导入的目标表中已包含有数据，则应使用 SQL 模式。

| 导入模式 | SST Mode | SQL Mode |
|:---|:---|:---|
| 速度 | 快 (100 ~ 500 GB/小时) | 慢 (10 ~ 50 GB/小时) |
| 资源使用率 | 高 | 低 |
| 占用网络带宽 | 高 | 低 |
| 导入时是否满足 ACID | 否 | 是 |
| 目标表 | 必须为空 |  可以不为空 |
| 支持 TiDB 集群版本 | >= v4.0.0| 全部 |
| 导入期间是否允许 TiDB 对外提供服务 | 否 | 是 |

> **注意：**
>
> 以上性能数据用于对比两种模式的导入性能差异，实际导入速度受硬件配置、表结构、索引数量等多方面因素影响。