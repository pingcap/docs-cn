---
title: TiDB 简介
category: introduction
---

# TiDB 简介

TiDB 是 PingCAP 公司自主设计、研发的开源分布式数据库，是一款在线事务处理/在线分析处理（ HTAP: Hybrid Transactional/Analytical Processing）融合型分布式数据库产品，具备水平扩容或者缩容、高可用、实时 HTAP 、云原生的分布式数据库、兼容 MySQL5.7 协议和 MySQL 生态等重要特性。目标是为用户提供一站式 Online Transactional Processing、OLAP (Online Analytical Processing)、Hybrid Transactional/Analytical Processing 解决方案。TiDB 适合高可用、强一致要求较高，数据规模较大等各种场景。

五大核心特性，如下：

- 一键水平扩容或者缩容

    得益于 TiDB 存储计算分离的架构的设计，可按需对计算、存储分别进行在线扩容或者缩容，扩容或者缩容过程中对应用、运维人员透明。
  
 - 高可用

    数据采用多副本存储，数据副本通过 Mutil-Raft 协议同步事务日志，多数派写入成功事务才能提交，确保数据强一致性且少数副本发生故障时不影响数据的可用性。可按需配置副本地理位置、副本数量等策略满足不同容灾级别的要求。
    
- 实时 HTAP

    提供行存储引擎 TiKV、列存储引擎 TiFlash 两款存储引擎，TiFlash 通过 Mutil-Raft Lenrner 协议实时从 TiKV 复制数据，确保行存储引擎 TiKV 和列存储引擎 TiFlash 之间的数据强一致。TiKV、TiFlash 可按需部署在不同的机器，解决 HTAP 资源隔离的问题。  
    
- 云原生的分布式数据库

    专为云而设计的分布式数据库，通过[TiDB Operator](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/tidb-operator-overview/) 可在公有云、私有云、混合云中实现部署工具化、自动化。

- 兼容 MySQL5.7 协议和 MySQL 生态

    兼容 MySQL 5.7 协议、MySQL 常用的功能、MySQL 生态，应用无需或者修改少量代码即可从 MySQL 迁移到 TiDB。提供丰富的数据迁移工具帮助应用便捷完成数据迁移。
