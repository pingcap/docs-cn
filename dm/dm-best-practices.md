---
title: DM 数据迁移最佳实践
summary: 了解使用 TiDB Data Migration (DM) 进行数据迁移的一些最佳实践。
---

# DM 数据迁移最佳实践

[TiDB Data Migration (DM)](https://github.com/pingcap/tiflow/tree/release-7.5/dm) 是由 PingCAP 开发维护的数据迁移同步工具，主要支持的源数据库类型为各类遵循 MySQL 协议标准的关系型数据库，如 MySQL、Percona MySQL、MariaDB、Amazon RDS for MySQL、Amazon Aurora 等。

DM 的使用场景主要有：

- 从兼容 MySQL 的单一实例中全量和增量迁移数据到 TiDB
- 将小数据量（小于 1 TB）分库分表 MySQL 合并迁移数据到 TiDB
- 在业务数据中台、业务数据实时汇聚等数据中枢场景中，作为数据同步中间件来使用

本文档介绍了如何优雅高效地使用 DM，以及如何规避使用 DM 的常见误区。

## 性能边界定位

DM 的性能参数如下表所示。

| 参数 | 限制 |
| -------- | :------: |
|  最大同步节点（Work Nodes ） |  1000  |
|  最大同步任务数量         |  600  |
|  最大同步 QPS            |  30k QPS/worker |
|  最大 Binlog 吞吐量      |  20 MB/s/worker |
|  每个 Task 处理的表数量   | 无限制 |

- DM 支持同时管理 1000 个同步节点（Work Node），最大同步任务数量为 600 个。为了保证同步节点的高可用，应预留一部分同步节点作为备用节点。建议预留的节点数量为已开启同步任务的同步节点数量的 20% ~ 50%。
- 单机部署 Work Node 数量。在服务器配置较好情况下，要保证每个 Work Node 至少有 2 核 CPU 加 4G 内存的可用工作资源，并且应为主机预留 10% ~ 20% 的系统资源。
- 单个同步节点（Work Node），理论最大同步 QPS 为 30K QPS/worker（不同 Schema 和 workload 会有所差异），处理上游 Binlog 的能力最高为 20 MB/s/worker。
- 如果将 DM 作为需要长期使用的数据同步中间件，需要注意 DM 组件的部署架构。请参见 [DM-master 与 DM-worker 部署实践](#dm-master-与-dm-worker-部署实践)。

## 数据迁移前

在所有数据迁移之前，整体方案的设计是至关重要的。下面我们分别从业务侧要点及实施侧要点两个方面讲一下相关的实践经验和适用场景。

### 业务侧要点

为了让压力可以平均分配到多个节点上，在 Schema 设计上，分布式数据库与传统数据库差别很大，既要保证较低的业务迁移成本，又要保证迁移后应用逻辑的正确性。下面就从几个方面来看业务迁移前的最佳实践。

#### Schema 的设计中 AUTO_INCREMENT 对业务的影响

TiDB 的 `AUTO_INCREMENT` 与 MySQL 的 `AUTO_INCREMENT` 整体上看是相互兼容的。但因为 TiDB 作为分布式数据库，一般会有多个计算节点（client 端入口），应用数据写入时会将负载均分开，这就导致在有 `AUTO_INCREMENT` 列的表上，可能出现不连续的自增 ID。详细原理参考 [`AUTO_INCREMENT`](/auto-increment.md#实现原理)。

如果业务对自增 ID 有强依赖，可以考虑使用 [SEQUENCE 函数](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。

#### 是否使用聚簇索引

TiDB 在建表时可以声明为主键创建聚簇索引或非聚簇索引。下面介绍各方案的优势和劣势。

- 聚簇索引

    [聚簇索引](/clustered-indexes.md#聚簇索引)使用主键作为数据存储的 handle ID（行 ID），在使用主键查询时可以减少一次回表的操作，有效提升查询效能。但如果表有大量数据写入且主键使用 [AUTO_INCREMENT](/auto-increment.md#实现原理)，非常容易造成数据存储的[写入热点问题](/best-practices/high-concurrency-best-practices.md#高并发批量插入场景)，导致集群整体效能不能充分利用，出现单存储节点的性能瓶颈问题。

- 非聚簇索引 + `shard row id bit`

    使用非聚簇索引，再配合表提示 `shard row id bit`，可以在继续使用 AUTO_INCREMENT 的情况下有效避免数据写入热点的产生。但是由于多了一次回表操作，此时使用主键查询数据，查询性能将有所影响。

- 聚簇索引 + 外部分布式发号器

    如果想使用聚簇索引，但还希望 ID 是单调递增的，那么可以考虑使用外部分布式发号器，如雪花算法 (Snowflake)、Leaf 等，来解决问题。由应用程序产生序列 ID，可以一定程度上保证 ID 的单调递增性，同时也保留了使用聚簇索引带来的收益。但相关应用程序需要进行改造。

- 聚簇索引 + AUTO_RANDOM

    此方案是目前分布式数据库既能避免出现写入热点问题，又能保留聚簇索引带来的查询收益的方案。整体改造也相对轻量，可以在业务切换使用 TiDB 作为写库时，修改 Schema 属性来达到目的。如果在后续查询时一定要利用 ID 列进行排序，可以使用 [AUTO_RANDOM](/auto-random.md) ID 列左移 6 位（符号位 1 位 + 分片位 5 位）来保证查询数据的顺序性。示例：

    ```sql
    CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM, b varchar(255));
    Select  a, a<<6 ,b from t order by a <<6 asc
    ```

下表汇总了不同使用场景的推荐方案和优劣势。

| 场景 | 推荐方案 | 优势 | 劣势 |
| :--- | :--- | :--- | :--- |
|  TiDB 未来作为主库使用，并会有大量数据写入。业务逻辑强依赖主键 ID 的连续性。  |  将表建立为非聚簇索引，并设置 SHARD_ROW_ID_BIT。使用 SEQUENCE 作为主键列。   |  可以有效避免数据写入热点，保证业务数据的连续性和单调递增。 | 数据写入的吞吐能力会下降（为保证数据写入连续性）；主键查询性能有所下降。 |
|   TiDB 未来作为主库使用，并会有大量数据写入。业务逻辑强依赖主键 ID 的递增特性。  |  将表建立为非聚簇索引，并设置 SHARD_ROW_ID_BIT；使用应用程序发号器来定义主键 ID。 |   可以有效避免数据写入热点；可以保证数据写入性能；可以有效保证业务数据是趋势性递增，但不能保证数据连续性。   |  对原有代码有一定的改造成本；外部发号器对时钟准确性有强依赖，引入新的故障风险点。 |
|  TiDB 未来作为主库使用，并会有大量数据写入。业务逻辑不依赖主键 ID 的连续性。   |  将表建立为聚簇索引表；主键列设置为 AUTO_RANDOM 属性。   |  可以有效避免数据写入热点；有非常有限的写入吞吐能力；主键查询性能优异；可以平滑将 AUTO_INCREMENT 属性切换为 AUTO_RANDOM 属性。    | 主键 ID 是完全随机的，业务数据排序建议使用插入时间列来完成。如果一定要使用主键 ID 排序，可以用 ID 左移 5 的方式查询，此方式查询的数据可以保证趋势递增的特性。  |
|  TiDB 未来作为只读的数据中台使用。  |  将表建立为非聚簇索引，并设置 SHARD_ROW_ID_BIT；使主键列维持与源数据库类型一致即可。  |  可以有效避免数据写入热点；改造成本低。   | 主键查询性能有所下降。  |

### 分库分表要点

#### 分与合

DM 支持[将上游分库分表的数据合并到下游 TiDB 中的同一个表](/migrate-small-mysql-shards-to-tidb.md)，这也是 TiDB 推荐的一种方式。

除了数据合并场景外，另一个典型场景为 **数据归档**场景。在此场景中，数据不断写入，随着时间流逝，大量的数据从热数据逐渐转变为温冷数据。在 TiDB 中，你可以通过 [Placement Rules](/configure-placement-rules.md) 放置规则来按照一定规则对数据设置不同的放置规则，而最小粒度即为[分区表 (Partition)](/partitioned-table.md)。

所以建议在遇到有大规模数据写入的场景，一开始就规划好未来是否需要归档或者有冷热数据分别存储在不同介质的需要。如果有，那么在迁移前请设置好分区表规则（目前 TiDB 还不支持 Table Rebuild 操作）。避免因为初期考虑不周，导致后期需要重新建表及重新导入数据。

#### 悲观 DDL 锁与乐观 DDL 锁

DM 默认会使用悲观 DDL 锁模式。在分库分表迁移与同步场景中，上游相关分表发生 Schema 变更后，会阻断后续的 DML 向下游 TiDB 写入。此时需要等待上游各分表的 Schema 都变更完毕并自动确认所有分表的结构一致后，从同步阻断记录点继续数据同步。

- 如果上游 Schema 变更时间较长，可能导致上游 Binlog 被清理，此问题可以通过开启 DM 的 Relay log 功能来避免。

- 如果不希望因为上游 Schema 变更阻塞数据写入，可以考虑使用乐观 DDL 锁模式。此时 DM 在发现上游分表 Schema 变更时也不会阻断数据同步，而是会持续同步数据。但如果同步期间 DM 发现上下游数据格式不兼容，将停止同步任务。此时需要人工介入处理。

下表汇总了乐观 DDL 锁和悲观 DDL 锁的优劣势。

| 场景 | 优势 | 劣势 |
| :--- | :--- | :--- |
| 悲观 DDL 锁（默认）   | 最大程度保证数据同步任务的可靠性    |  如果分表较多，将长时间阻断数据同步任务。并有可能因为上游的 Binlog 已被清理而导致同步中断。可以通过开启 DM-worker 的 Relay log 来避免问题。详情请参考 [Relay log 的使用](#relay-log-的使用) .|
| 乐观 DDL 锁   | 数据同步任务基本不会出现相关阻塞延迟    | 此模式下需要保证 Schema 变更的兼容性（增加列是否具有默认值）。如果考虑不周，可能出现未被发现的上下游数据不一致问题。更多限制，请参考[乐观模式下分库分表合并迁移](/dm/feature-shard-merge-optimistic.md#使用限制)。  |

### 其他限制与影响

#### 上下游的数据类型

这里主要需要考虑上下游的数据类型问题。TiDB 目前支持绝大部分 MySQL 的数据类型。但一些特殊类型尚不支持（如空间类型）。关于数据类型的兼容性，请参考[数据类型概述](/data-type-overview.md)。

#### 字符集与排序规则

自 TiDB v6.0.0 以后，默认使用新排序规则。如果需要 TiDB 支持 utf8_general_ci、utf8mb4_general_ci、utf8_unicode_ci、utf8mb4_unicode_ci、gbk_chinese_ci 和 gbk_bin 这几种排序规则，需要在集群创建时声明，将 `new_collations_enabled_on_first_bootstrap` 的值设为 `true`。更详细信息请参考[字符集和排序规则](/character-set-and-collation.md#新框架下的排序规则支持)。

TiDB 默认使用的字符集为 utf8mb4。建议同步上下游及应用统一使用 utf8mb4。如果上游有显式指定的字符集或者排序规则，需要确认 TiDB 是否支持。

从 v6.0.0 起，TiDB 支持 GBK 字符集。有关字符集的限制详见：

- [字符集和排序规则](/character-set-and-collation.md)
- [GBK 兼容情况](/character-set-gbk.md#与-mysql-的兼容性)

### 实施侧要点

#### DM-master 与 DM-worker 部署实践

DM 整体架构分为 DM-master 与 DM-worker。

- DM-master 主要负责同步任务的元数据管理，以及 DM-worker 的中心调度，是整个 DM 平台的核心。所以 DM-master 可以部署为集群模式，以保证 DM 同步平台的可用性。
- DM-worker 负责执行上下游同步任务，是无状态节点。最多可以部署 1000 个节点。在需要将 DM 作为数据同步平台的场景，可以预留一部分空闲的 DM-worker，以保证同步任务的高可用。

#### 同步任务规划

分库分表场景。在分库分表迁移场景，根据上游分库分表的种类进行同步任务的拆分，如 `usertable_1~50` 和 `Logtable_1~50` 是两类分表，那么就应该分别建 2 个 Task 任务进行同步。这样做的好处是可有效简化同步任务模板的复杂度，并有效控制数据同步中断的影响范围。

大规模数据迁移同步场景。可以参考以下思路进行 Task 任务拆分：

- 如果上游需要同步多个数据库，可以按照不同数据库拆分 Task。

- 根据上游写入压力拆分任务。即把上游 DML 操作频繁的表，拆分到单独的 Task 任务中，将其他没有频繁 DML 操作的表使用另一个 Task 任务进行同步。此方式可在一定程度上加速同步任务的推进能力。尤其是在上游有大量 Log 写入某张表，但业务关注的是其他表时，此方法可以有效解决此类问题。

请注意，拆分同步任务后只能保证数据同步的最终一致性，实时一致性因各种原因可能出现较大偏差。

下表给出了在不同的数据迁移与同步场景下部署 DM-master 与 DM-worker 的推荐方案。

| 场景 |  DM-master 部署 | DM-worker 部署 |
| :--- | :--- | :--- |
| 小规模数据 （1 TB 以下），一次性数据迁移场景  |  部署 1 个 DM-master 节点   | 根据上游数据源数量，部署 1 ~ N 个 DM-worker 节点。一般情况下 1 个 DM-worker 节点。   |
| 大规模数据 （1 TB 以上）及分库分表，一次性数据迁移场景  | 推荐部署 3 个 DM-master 节点，来保证在长时间数据迁移时 DM 集群的可用性   | 根据数据源数量或同步任务数量部署 DM-Worker 节点。推荐多部署 1~3 个空闲 DM-Worker 节点。   |
|  长期数据同步迁移场景  | 务必部署 3 个 DM-master 节点。如在云上部署，尽量将 DM-master 部署在不同的可用区（AZ）    |   根据数据源数量或同步任务数量部署 DM-worker 节点。务必部署实际需要 DM-worker 节点数量的 1.5 ~ 2 倍的 DM-worker 节点数量。 |

#### 上游数据源选择与设置

DM 支持存量数据迁移，但在做全量迁移时会对整库进行全量数据备份。DM 采用的备份方式为并行逻辑备份，备份 MySQL 期间会加上全局只读锁 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)。此时会短暂地阻塞上游数据库的 DML 和 DDL 操作。所以强烈建议使用上游的备库来进行全量备份，并同时在数据源开启 GTID 的功能 (`enable-gtid: true`)。这样既可避免存量迁移时对上游业务的影响，也可以在增量同步期间再切换到上游主库节点降低数据同步的延迟。切换上游 MySQL 数据源的方法，请参考[切换 DM-worker 与上游 MySQL 实例的连接](/dm/usage-scenario-master-slave-switch.md#切换-dm-worker-与上游-mysql-实例的连接)。

下面是一些特殊场景下的注意事项：

- 只能在上游主库进行全量备份

    在该场景中，可以在同步任务配置中设置一致性参数为 none，`mydumpers.global.extra-args: "--consistency none"` 避免给主库加全局只读锁，但有可能破坏全量备份的数据一致性，导致最终上下游数据不一致。

- 利用备份快照解决存量迁移（只适用 AWS 上 MySQL RDS 和 Aurora RDS 的迁移）

    如果要迁移的数据库正好为 AWS MySQL RDS 或者 Aurora RDS，可以利用 RDS Snapshot 备份将 Amazon S3 中的备份数据直接迁移到 TiDB，以此保证存量数据迁移的一致性。整个操作流程以及后续增量同步方法，请参考[从 Amazon Aurora 迁移数据到 TiDB](/migrate-aurora-to-tidb.md#从-amazon-aurora-迁移数据到-tidb)。

### 配置细节详解

#### 大小写

TiDB 默认情况下对 Schema name 大小写不敏感，即 `lower_case_table_names:2`。但上游 MySQL 大多为 Linux 系统，默认对大小写敏感。此时需要注意，在 DM 数据同步任务设置时将 `case-sensitive` 设置为 `true`，保证可以正确同步上游的 Schema。

特殊情况下，比如上游一个数据库中，既有大写表如 `Table`，又有小写表如 `table`，那么 Schema 创建时将报错:

`ERROR 1050 (42S01): Table '{tablename}' already exists`

#### 过滤规则

在配置数据源时即可配置过滤规则。配置方法请参考[数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)。

配置过滤规则的好处有：

- 可以减少下游处理 Binglog Event 的数量，提升同步效能
- 可以减少不必要的 Relay log 的落盘，节约磁盘空间

> **注意：**
>
> 在分库分表场景中，如果你在数据源配置了过滤规则，请确保数据源与同步任务中设置的过滤规则相匹配。如果不匹配，将会导致同步任务长期接收不到增量数据。

#### Relay Log 的使用

MySQL 的主从复制在 Secondary 端会保存一份 Relay log，以此保证异步复制的可靠性与效能。DM 也支持在 DM-worker 侧保存一份 Relay log，并可设置存储位置、过期清理时间等信息。此功能适用于以下场景：

- 在进行全量 + 增量数据迁移时，因为全量迁移数据量较大，整个过程耗费时间超过了上游 Binlog 归档的时间，导致增量同步任务不能正常启动，如果开启 Relay Log 在全量同步启动同时，DM-worker 即会开始接收 Relay log，避免增量任务启动失败。
- 在使用 DM 进行长期数据同步的场景中，有时因为各种原因导致同步任务长时间阻塞，此时开启了 Relay log 功能，可以有效应对同步任务阻塞而导致的上游 Binglog 被回收问题。

在使用 Relay Log 功能时也会有一定的限制。DM 支持高可用，当某个 DM-worker 出现故障，会尝试将空闲的 DM-worker 实例提升为工作实例，如果此时上游 Binlog 没有包含必要的同步日志，将可能出现同步中断情况。此时需要人工干预，尽快将 Relay log 复制到新的 DM-worker 节点上来，并修改相应的 Relay meta 文件。具体方法请参考[故障处理](/dm/dm-error-handling.md#relay-处理单元报错-event-from--in--diff-from-passed-in-event--或迁移任务中断并包含-get-binlog-error-error-1236-hy000binlog-checksum-mismatch-data-may-be-corrupted-等-binlog-获取或解析失败错误)。

#### 上游使用在线变更工具 PT-osc/GH-ost

在日常运维 MySQL 时，想要在线变更表结构，一般会使用 PT-osc/GH-ost 这类工具，以此保证 DDL 变更对线上业务的影响最小。但整个过程会被如实地记录到 MySQL Binlog 中，如果全部同步到下游 TiDB，将产生大量的写放大，既不高效也不经济。DM 在设置 Task 任务时候可以设置支持三方数据同步工具 PT-osc 或 GH-ost，配置后将不再同步大量冗余数据，并且能保证数据同步的一致性。具体设置方式请参考[迁移使用 GH-ost/PT-osc 的源数据库](/dm/feature-online-ddl.md)。

## 数据迁移中

在这个环节基本上遇到的问题都是 Troubleshooting 类的问题，在这里给大家列举一些场景的问题及处理方式。

### 上游与下游 Schema 不一致

常见报错信息：

- `messages: Column count doesn't match value count: 3 (columns) vs 2 (values)`
- `Schema/Column doesn't match`

此类问题主要原因是下游 TiDB 中增加或修改了索引，或者下游比上游更多列。当出现此类的同步报错信息时，请检查是否是上下游 Schema 不一致导致的同步中断。

要解决此类问题，只需将 DM 中缓存的 Schema 信息更新成与下游 TiDB Schema 一致即可。具体方法参考[管理迁移表的表结构](/dm/dm-manage-schema.md)。

如果是下游比上游多列的场景，请参考[下游存在更多列的迁移场景](/migrate-with-more-columns-downstream.md)。

### 处理因为 DDL 中断的数据同步任务

DM 支持跳过或者替换导致同步任务中断的 DDL 语句。并且针对是否为分库分表合并场景有对应不同的操作，具体请参考[处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md#使用示例)。

## 数据迁移后的数据校验

在完成数据迁移后，建议对新旧数据进行数据一致性校验。TiDB 提供了相应的同步工具 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 来帮助你完成数据校验工作。

通过管理 DM 中的同步任务，sync-diff-inspector 可以自动管理需要进行数据一致性检查的 Table 列表，相较之前的手动配置更加的高效。具体参考[基于 DM 同步场景下的数据校验](/sync-diff-inspector/dm-diff.md)。

自 DM v6.2.0 版本开始，DM 支持在增量同步的同时进行数据校验。具体参考 [DM 增量数据校验](/dm/dm-continuous-data-validation.md)。

## 数据长期同步

如果将 DM 作为持续的数据同步平台，建议一定要做好必要的元信息备份。一方面是保证同步集群故障重建的能力，另一方面可以实现同步任务的版本控制。具体实现方式参考[导出和导入集群的数据源和任务配置](/dm/dm-export-import-config.md)。
