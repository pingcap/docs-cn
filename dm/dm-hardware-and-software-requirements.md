---
title: TiDB Data Migration 集群软硬件环境需求
summary: 了解部署 DM 集群的软件和硬件要求。
aliases: ['/docs-cn/tidb-data-migration/dev/hardware-and-software-requirements/']
---

# TiDB Data Migration 集群软硬件环境需求

TiDB Data Migration (DM) 支持主流的 Linux 操作系统，具体版本要求见下表：

| Linux 操作系统       | 版本         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 及以上   |
| CentOS                   | 7.3 及以上   |
| Oracle Enterprise Linux  | 7.3 及以上   |
| Ubuntu LTS               | 16.04 及以上 |

DM 可以在 Intel 架构服务器环境及主流虚拟化环境中部署和运行。

## 服务器建议配置

DM 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发，测试，及生产环境的服务器硬件配置（不包含操作系统本身的占用）有以下要求和建议：

### 开发及测试环境

| 组件 | CPU | 内存 | 本地存储 | 网络 | 实例数量（最低要求） |
| --- | --- | --- | --- | --- | --- |
| DM-master | 4 核+ | 8 GB+ | SAS，200 GB+ | 千兆网卡 | 1 |
| DM-worker | 8 核+ | 16 GB+ | SAS，200 GB+（大于迁移数据的大小） | 千兆网卡 | 上游 MySQL 实例的数量 |

> **注意：**
>
> - 在功能验证的测试环境中的 DM-master 和 DM-worker 可以部署在同一台服务器上。
> - 如进行性能相关的测试，避免采用低性能存储和网络硬件配置，防止对测试结果的正确性产生干扰。
> - 如果仅验证功能，可以单机部署一个 DM-master，DM-worker 部署的数量至少是上游 MySQL 实例的数量。为了保证高可用性，建议部署更多的 DM-worker。
> - DM-worker 在 `dump` 和 `load` 阶段需要存储全量数据，因此 DM-worker 的磁盘空间需要大于需要迁移数据的总量；如果迁移任务开启了 relay log，DM-worker 也需要一定的磁盘空间来存储上游的 binlog 数据。

### 生产环境

| 组件 | CPU | 内存 | 硬盘类型 | 网络 | 实例数量（最低要求） |
| --- | --- | --- | --- | --- | --- |
| DM-master | 4 核+ | 8 GB+ | SAS，200 GB+ | 千兆网卡 | 3 |
| DM-worker | 16 核+ | 32 GB+ | SSD，200 GB+（大于迁移数据的大小） | 万兆网卡 | 大于上游 MySQL 实例的数量 |
| 监控 | 8 核+ | 16 GB+ | SAS，200 GB+ | 千兆网卡 | 1 |

> **注意：**
>
> - 在生产环境中，不建议将 DM-master 和 DM-worker 部署和运行在同一个服务器上，以防 DM-worker 对磁盘的写入干扰 DM-master 高可用组件使用磁盘。
> - 在遇到性能问题时可参照[配置调优](/dm/dm-tune-configuration.md)尝试修改任务配置。调优效果不明显时，可以尝试升级服务器配置。

## 下游数据库所需空间

目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/manage-cluster-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

可以用下面 SQL 语句统计信息表的 `DATA_LENGTH` 字段估算数据量：

```sql
-- 统计所有 schema 大小
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- 统计最大的 5 个单表
SELECT
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```