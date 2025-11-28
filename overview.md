---
title: TiDB 简介
summary: TiDB 是平凯星辰公司自主设计、研发的开源分布式关系型数据库，支持在线事务处理与在线分析处理 (HTAP)。具有水平扩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 协议和 MySQL 生态等特性。适用于高可用、强一致性要求高、数据规模大等各种应用场景。具有一键水平扩缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 协议和 MySQL 生态等五大核心特性，以及金融行业、海量数据及高并发的 OLTP、实时 HTAP、数据汇聚、二次加工处理等四大核心应用场景。
---

# TiDB 简介

<!-- Localization note for TiDB:

- 英文：用 distributed SQL，同时开始强调 HTAP
- 中文：可以保留 NewSQL 字眼，同时强调一栈式实时 HTAP
- 日文：NewSQL 认可度高，用 NewSQL

-->

[TiDB](https://github.com/pingcap/tidb) 是[平凯星辰](https://pingkai.cn/about)公司自主设计、研发的开源分布式关系型数据库，是一款同时支持在线事务处理与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 的融合型分布式数据库产品，具备水平扩容或者缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 协议和 MySQL 生态等重要特性。目标是为用户提供一站式 OLTP (Online Transactional Processing)、OLAP (Online Analytical Processing)、HTAP 解决方案。TiDB 适合高可用、强一致要求较高、数据规模较大等各种应用场景。

## 五大核心特性

- 一键水平扩缩容

    得益于 TiDB 存储计算分离的架构的设计，可按需对计算、存储分别进行在线扩容或者缩容，扩容或者缩容过程中对应用运维人员透明。

- 金融级高可用

    数据采用多副本存储，数据副本通过 Multi-Raft 协议同步事务日志，多数派写入成功事务才能提交，确保数据强一致性且少数副本发生故障时不影响数据的可用性。可按需配置副本地理位置、副本数量等策略，满足不同容灾级别的要求。

- 实时 HTAP

    提供行存储引擎 [TiKV](/tikv-overview.md)、列存储引擎 [TiFlash](/tiflash/tiflash-overview.md) 两款存储引擎，TiFlash 通过 Multi-Raft Learner 协议实时从 TiKV 复制数据，确保行存储引擎 TiKV 和列存储引擎 TiFlash 之间的数据强一致。TiKV、TiFlash 可按需部署在不同的机器，解决 HTAP 资源隔离的问题。

- 云原生的分布式数据库

    专为云而设计的分布式数据库，通过 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/tidb-operator-overview) 可在公有云、私有云、混合云中实现部署工具化、自动化。

- 兼容 MySQL 协议和 MySQL 生态

    兼容 MySQL 协议、MySQL 常用的功能、MySQL 生态，应用无需或者修改少量代码即可从 MySQL 迁移到 TiDB。提供丰富的[数据迁移工具](/ecosystem-tool-user-guide.md)帮助应用便捷完成数据迁移。

## 四大核心应用场景

- 金融行业场景

    金融行业对数据一致性及高可靠、系统高可用、可扩展性、容灾要求较高。传统的解决方案的资源利用率低，维护成本高。TiDB 采用多副本 + Multi-Raft 协议的方式将数据调度到不同的机房、机架、机器，确保系统的 RTO <= 30s 及 RPO = 0。

- 海量数据及高并发的 OLTP 场景

    传统的单机数据库无法满足因数据爆炸性的增长对数据库的容量要求。TiDB 是一种性价比高的解决方案，采用计算、存储分离的架构，可对计算、存储分别进行扩缩容，计算最大支持 512 节点，每个节点最大支持 1000 并发，集群容量最大支持 PB 级别。

- 实时 HTAP 场景

    TiDB 适用于需要实时处理的大规模数据和高并发场景。TiDB 在 4.0 版本中引入列存储引擎 TiFlash，结合行存储引擎 TiKV 构建真正的 HTAP 数据库，在增加少量存储成本的情况下，可以在同一个系统中做联机交易处理、实时数据分析，极大地节省企业的成本。

- 数据汇聚、二次加工处理的场景

    TiDB 适用于将企业分散在各个系统的数据汇聚在同一个系统，并进行二次加工处理生成 T+0 或 T+1 的报表。与 Hadoop 相比，TiDB 要简单得多，业务通过 ETL 工具或者 TiDB 的同步工具将数据同步到 TiDB，在 TiDB 中可通过 SQL 直接生成报表。

## 另请参阅

- [TiDB 整体架构](/tidb-architecture.md)
- [TiDB 数据库的存储](/tidb-storage.md)
- [TiDB 数据库的计算](/tidb-computing.md)
- [TiDB 数据库的调度](/tidb-scheduling.md)
