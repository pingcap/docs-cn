---
title: TiDB Lightning 简介
summary: TiDB Lightning 是用于导入 TB 级数据到 TiDB 的工具。了解 TiDB Lightning 的基本原理和使用方法。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-overview/','/docs-cn/dev/reference/tools/tidb-lightning/overview/','/docs-cn/tools/lightning/overview-architecture/','/zh/tidb/dev/tidb-lightning-backends/','/docs-cn/dev/tidb-lightning/tidb-lightning-backends/','/docs-cn/dev/reference/tools/tidb-lightning/backend/','/zh/tidb/dev/tidb-lightning-tidb-backend','/docs-cn/dev/tidb-lightning/tidb-lightning-tidb-backend/','/docs-cn/dev/loader-overview/','/docs-cn/dev/reference/tools/loader/','/docs-cn/tools/loader/','/docs-cn/dev/load-misuse-handling/','/docs-cn/dev/reference/tools/error-case-handling/load-misuse-handling/','/zh/tidb/dev/loader-overview/']
---

# TiDB Lightning 简介

TiDB Lightning 是用于从静态文件导入 TB 级数据到 TiDB 集群的工具，常用于 TiDB 集群的初始化数据导入。

要快速了解 Lightning 的基本原理和使用方法，建议先观看下面的培训视频（时长 32 分钟）。注意本视频只为学习参考，具体操作步骤和最新功能，请以文档内容为准。

<video src="https://download.pingcap.com/docs-cn%2FLesson19_lightning.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson19.png"></video>

TiDB Lightning 支持以下文件类型：

- [Dumpling](/dumpling-overview.md) 生成的文件
- CSV 文件
- [Amazon Aurora 生成的 Apache Parquet 文件](/migrate-aurora-to-tidb.md)

TiDB Lightning 支持从以下位置读取：

- 本地
- [Amazon S3](/external-storage-uri.md#amazon-s3-uri-格式)
- [Google GCS](/external-storage-uri.md#gcs-uri-格式)

> **注意：**
>
> 与 TiDB Lightning 相比，[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 在部署、资源利用率、任务配置便捷性、调用集成便捷性、自动化分布式任务调度和管理、基于全局排序增强导入稳定性、高可用性和可扩展性等方面都有很大提升。建议您在合适的场景下，使用 `IMPORT INTO` 代替 TiDB Lightning。

## TiDB Lightning 整体架构

![TiDB Lightning 整体架构](/media/tidb-lightning-architecture.png)

TiDB Lightning 目前支持两种导入方式，通过 `backend` 配置区分。不同的模式决定 TiDB Lightning 如何将数据导入到目标 TiDB 集群。

- [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)：TiDB Lightning 首先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对上传到各个 TiKV 节点，最后调用 TiKV Ingest 接口将数据插入到 TiKV 的 RocksDB 中。如果用于初始化导入，请优先考虑使用物理导入模式，其拥有较高的导入速度。物理导入模式对应的后端模式为 `local`。

- [逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)：TiDB Lightning 先将数据编码成 SQL，然后直接运行这些 SQL 语句进行数据导入。如果需要导入的集群为生产环境线上集群，或需要导入的目标表中已包含有数据，则应使用逻辑导入模式。逻辑导入模式对应的后端模式为 `tidb`。

| 导入模式 | 物理导入模式 | 逻辑导入模式 |
|:---|:---|:---|
| 后端 | `local` | `tidb` |
| 速度 | 快 (100 ~ 500 GiB/小时) | 慢 (10 ~ 50 GiB/小时) |
| 资源使用率 | 高 | 低 |
| 占用网络带宽 | 高 | 低 |
| 导入时是否满足 ACID | 否 | 是 |
| 目标表 | 必须为空 |  可以不为空 |
| 支持 TiDB 集群版本 | >= v4.0.0| 全部 |
| 导入期间是否允许 TiDB 对外提供服务 | [受限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#使用限制) | 是 |

> **注意：**
>
> 以上性能数据用于对比两种模式的导入性能差异，实际导入速度受硬件配置、表结构、索引数量等多方面因素影响。
