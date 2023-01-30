---
title: Data Migration 简介
summary: 了解 TiDB Data Migration
aliases: ['/zh/tidb/stable/quick-create-migration-task','/zh/tidb/stable/scenarios']
---

# Data Migration 简介

[TiDB Data Migration](https://github.com/pingcap/tiflow/tree/master/dm) (DM) 是一款便捷的数据迁移工具，支持从与 MySQL 协议兼容的数据库（MySQL、MariaDB、Aurora MySQL）到 TiDB 的全量数据迁移和增量数据同步。使用 DM 工具有利于简化数据迁移过程，降低数据迁移运维成本。

使用 DM 进行数据迁移的时候，需要执行以下操作：

- 部署 DM 集群
- 创建上游数据源（source）对象，保存数据源访问信息
- 创建（多个）数据迁移任务从数据源迁移数据到 TiDB

数据迁移任务包含全量数据迁移、增量数据复制两个阶段：

- 全量数据迁移：从数据源迁移对应表的表结构到 TiDB，然后读取存量数据写入到 TiDB 集群；
- 增量数据复制：全量数据迁移完成后，从数据源读取对应的表变更然后写入到 TiDB 集群。

要快速了解 DM 的原理架构、适用场景，建议先观看下面的培训视频（时长 22 分钟）。注意本视频只作为学习参考，具体操作步骤和最新功能，请以文档内容为准。

<video src="https://tidb-docs.s3.us-east-2.amazonaws.com/compressed+-+Lesson+20+part+1.mp4" width="600px" height="450px" controls="controls" poster="https://tidb-docs.s3.us-east-2.amazonaws.com/thumbnail+-+lesson+20+part+1.png"></video>

## 版本说明

本文档中的说明基于 DM 的最新稳定版本 v5.4。

在 v5.4 之前，DM 工具的文档独立于 TiDB 文档。要访问这些早期版本的 DM 文档，请点击以下链接：

- [DM v5.3 文档](https://docs.pingcap.com/zh/tidb-data-migration/v5.3)
- [DM v2.0 文档](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/)
- [DM v1.0 文档](https://docs.pingcap.com/zh/tidb-data-migration/v1.0/)（较旧的版本，不推荐使用）

> **注意：**
>
> - DM 的 GitHub 代码仓库已于 2021 年 10 月迁移至 [pingcap/tiflow](https://github.com/pingcap/tiflow/tree/master/dm)。如有任何关于 DM 的问题，请在 `pingcap/tiflow` 仓库提交，以获得后续反馈。
> - 在较早版本中（v1.0 和 v2.0），DM 采用独立于 TiDB 的版本号。从 DM v5.3 起，DM 采用与 TiDB 相同的版本号。DM v2.0 的下一个版本为 DM v5.3。DM v2.0 到 v5.3 无兼容性变更，升级过程与正常升级无差异。

## 基本功能

本节介绍 DM 工具的核心功能模块。

![DM Core Features](/media/dm/dm-core-features.png)

### Block & allow lists

[Block & Allow Lists](/dm/dm-key-features.md#block--allow-table-lists) 的过滤规则类似于 MySQL `replication-rules-db`/`replication-rules-table`，用于过滤或指定只迁移某些数据库或某些表的所有操作。

### Binlog event filter

[Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter) 用于过滤源数据库中特定表的特定类型操作，比如过滤掉表 `test`.`sbtest` 的 `INSERT` 操作或者过滤掉库 `test` 下所有表的 `TRUNCATE TABLE` 操作。

### Table routing

[Table Routing](/dm/dm-key-features.md#table-routing) 是将源数据库的表迁移到下游指定表的路由功能，比如将源数据表 `test`.`sbtest1` 的表结构和数据迁移到 TiDB 的表 `test`.`sbtest2`。它也是分库分表合并迁移所需的一个核心功能。

## 高级功能

### 分库分表合并迁移

DM 支持对源数据的分库分表进行合并迁移，但有一些使用限制，详细信息请参考[悲观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-pessimistic.md#使用限制)和[乐观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-optimistic.md#使用限制)。

### 对第三方 Online Schema Change 工具变更过程的同步优化

在 MySQL 生态中，gh-ost 与 pt-osc 等工具被广泛使用，DM 对其变更过程进行了特殊的优化，以避免对不必要的中间数据进行迁移。详细信息可参考 [online-ddl](/dm/dm-key-features.md#online-ddl-工具支持)。

### 使用 SQL 表达式过滤某些行变更

在增量同步阶段，DM 支持配置 SQL 表达式过滤掉特定的行变更，以实现对同步数据的更精细控制。详细信息可参考[使用 SQL 表达式过滤某些行变更](/dm/feature-expression-filter.md)。

## 使用限制

在使用 DM 工具之前，需了解以下限制：

+ 数据库版本要求

    - MySQL 版本 > 5.5
    - MariaDB 版本 >= 10.1.2

    > **注意：**
    >
    > 如果上游 MySQL/MariaDB servers 间构成主从复制结构，则需要 MySQL 版本高于 5.7.1 或者 MariaDB 版本等于或高于 10.1.3。

    > **警告：**
    >
    > 使用 DM 从 MySQL v8.0 迁移数据到 TiDB 目前为实验特性（从 DM v2.0 引入），不建议在生产环境下使用。

+ DDL 语法兼容性限制

    - 目前，TiDB 部分兼容 MySQL 支持的 DDL 语句。因为 DM 使用 TiDB parser 来解析处理 DDL 语句，所以目前仅支持 TiDB parser 支持的 DDL 语法。详见 [TiDB DDL 语法支持](/mysql-compatibility.md#ddl-的限制)。

    - DM 遇到不兼容的 DDL 语句时会报错。要解决此报错，需要使用 dmctl 手动处理，要么跳过该 DDL 语句，要么用指定的 DDL 语句来替换它。详见[如何处理不兼容的 DDL 语句](/dm/dm-faq.md#如何处理不兼容的-ddl-语句)。

+ 分库分表数据冲突合并

    - 如果业务分库分表之间存在数据冲突，可以参考[自增主键冲突处理](/dm/shard-merge-best-practices.md#自增主键冲突处理)来解决；否则不推荐使用 DM 进行迁移，如果进行迁移则有冲突的数据会相互覆盖造成数据丢失。
    - 分库分表 DDL 同步限制，参见[悲观模式下分库分表合并迁移使用限制](/dm/feature-shard-merge-pessimistic.md#使用限制)以及[乐观模式下分库分表合并迁移使用限制](/dm/feature-shard-merge-optimistic.md#使用限制)。

+ 数据源 MySQL 实例切换

    - 当 DM-worker 通过虚拟 IP（VIP）连接到 MySQL 且要切换 VIP 指向的 MySQL 实例时，DM 内部不同的 connection 可能会同时连接到切换前后不同的 MySQL 实例，造成 DM 拉取的 binlog 与从上游获取到的其他状态不一致，从而导致难以预期的异常行为甚至数据损坏。如需切换 VIP 指向的 MySQL 实例，请参考[虚拟 IP 环境下的上游主从切换](/dm/usage-scenario-master-slave-switch.md#虚拟-ip-环境下切换-dm-worker-与-mysql-实例的连接)对 DM 手动执行变更。

+ GBK 字符集兼容性限制

    - DM 在 v5.4.0 之前不支持将 `charset=GBK` 的表迁移到 TiDB。

## Contributing

欢迎参与 DM 开源项目并万分感谢您的贡献，可以查看 [CONTRIBUTING.md](https://github.com/pingcap/tiflow/blob/master/dm/CONTRIBUTING.md) 了解更多信息。

## 社区技术支持

您可以通过在线文档了解和使用 DM，如果您遇到无法解决的问题，可以选择以下途径之一联系我们。

- [GitHub](https://github.com/pingcap/tiflow/tree/master/dm)
- [AskTUG](https://asktug.com/tags/dm)

## License

DM 遵循 Apache 2.0 协议，在 [LICENSE](https://github.com/pingcap/tiflow/blob/master/LICENSE) 了解更多信息。

## 版本变更说明

在 v5.4 之前，DM 工具的文档独立于 TiDB 文档。要访问这些早期版本的 DM 文档，请点击以下链接：

- [DM v5.3 文档](https://docs.pingcap.com/zh/tidb-data-migration/v5.3)
- [DM v2.0 文档](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/)
- [DM v1.0 文档](https://docs.pingcap.com/zh/tidb-data-migration/v1.0/)

> **注意：**
>
> - DM 的 GitHub 代码仓库已于 2021 年 10 月迁移至 [pingcap/tiflow](https://github.com/pingcap/tiflow/tree/master/dm)。如有任何关于 DM 的问题，请在 `pingcap/tiflow` 仓库提交，以获得后续支持。
> - 在较早版本中（v1.0 和 v2.0），DM 采用独立于 TiDB 的版本号。从 DM v5.3 起，DM 采用与 TiDB 相同的版本号。DM v2.0 的下一个版本为 DM v5.3。DM v2.0 到 v5.3 无兼容性变更，升级过程与正常升级无差异。

要快速了解 DM 的原理架构、适用场景，建议先观看下面的培训视频。注意本视频只作为学习参考，具体操作步骤和最新功能，请以文档内容为准。

<video src="https://download.pingcap.com/docs-cn%2FLesson20_dm_part01.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson20.png"></video>

<video src="https://download.pingcap.com/docs-cn/Lesson20_dm_part02.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson20.png"></video>

<video src="https://download.pingcap.com/docs-cn/Lesson20_part03.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson20.png"></video>
