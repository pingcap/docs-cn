---
title: 数据迁移最佳实践
summary: 了解使用 Data Migration (DM) 进行数据迁移的一些最佳实践。
---

# 数据迁移最佳实践

Data Migration (DM) 是由 PingCAP 开发维护的数据迁移同步工具，主要支持的源数据库类型为各类 MySQL 协议标准的关系型数据库，如 MySQL、Percona MySQL、MariaDB、AWS MYSQL RDS、AWS Aurora 等。DM 主要有以下几个使用场景：

- 单一实例全量和增量迁移
- 将分库分表的各个库表归并到一张总表的全量和增量迁移
- 在“业务数据中台、业务数据实时汇聚”等 DataHUB 场景中，作为数据同步中间件来使用

本文档介绍了如何优雅高效的使用 DM，以及如何规避使用 DM 时的常见误区。

## 性能边界定位

| 参数 | 限制 |
| -------- | :------: |
|  最大同步节点（Work Nodes ） |  1000  |
|  最大同步任务数量 |  600  |
|  最大同步 QPS   |  30k QPS/worker |
|  最大 Binlog 吞吐量  |  20 MB/s/worker |
|   SLA     |  >99.9% |
|   每个 Task 处理的表数量  | 无限制 |

- DM 支持同时管理 1000 个同步节点（Work Node），最大同步任务数量为 600 个。为了保证同步节点的高可用，应预留一部分 Work Node 节点作为备用节点，保证数据同步的高可用。预留已开启同步任务 Work Node 数量的 20% ~ 50%。
- 单机部署 Work Node 数量。在服务器配置较好情况下，要保证每个 Work Node 至少有 2 核 CPU 加 4G 内存的工作资源可以使用，并且应为主机预留  10% ~ 20% 的系统资源。
- 单个同步节点（Work Node ），理论最大同步 QPS 在 30K QPS/worker（不同 Schema 和 workload 会有所差异），处理上游 Binlog 的能力最高为 20MB/。
- 如果将 DM 作为需要长期使用的数据同步中间件，SLA 可以达到 3 个 9 以上。但需要注意 DM 组件的部署架构，参见[xxx](#xxx)。

## 数据迁移前的最佳实践

在所有数据迁移之前，整体方案的设计是至关重要的。尤其以迁移前的一系列方案设计，是整个方案实施好坏的重中之重。下面我们分别从业务侧要点及实施侧要点两个方面讲一下相关的实践经验和适用场景。

### 业务侧要点

为了让压力可以平均分配到多个节点上，在 Schema 设计上，分布式数据库与传统数据库差别很大，既要保证较低的业务迁移成本，又要保证迁移后应用逻辑的正确性。下面就从几个方面来看业务迁移前的最佳实践。

#### Schema 的设计

AUTO_INCREMENT 对业务的影响

TiDB 的 AUTO_INCREMENT 与 MySQL AUTO_INCREMENT 整体上看是相互兼容的。但因为 TiDB 作为分布式数据库，一般会有多个计算节点（client 端入口），应用数据写入时会将负载均分开，这就导致在有 AUTO_INCREMENT 列的表上，可能出现不连续的自增 ID。详细原理参考 [AUTO_INCREMENT](/auto-increment.md#实现原理)。

如果业务对自增 ID 有强依赖，可以考虑使用 [sequence 方案](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。

#### 是否要使用聚簇索引

## 数据迁移中的最佳实践

## 数据迁移后的最佳实践

## 数据长期同步的最佳实践