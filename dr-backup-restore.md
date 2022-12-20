---
title: 使用 TiDB 备份和恢复功能进行容灾
summary: 介绍在容灾场景下，如何使用 TiDB 备份与恢复功能？
---

# 使用 TiDB 备份和恢复功能进行容灾

基于 Raft 协议和合理的部署拓扑规划，TiDB 集群能够容忍单个机房、单个地理区域的故障，在故障发生的时候，TiDB 依然能对外提供服务。而 TiDB 备份恢复功能，支持将集群的数据备份到安全的灾备存储设施中，使得用户的数据能够免于更严重的自然灾害或者常见的人为误操作，是数据安全的最后一道防线。

TiDB 备份和恢复功能可以实现

- 低至 5 分钟的 Recovery Point Objective (RPO)。
- 不同的数据规模下，几十分钟到数小时不等的 Recovery Time Objective。

TiDB 准备了非常丰富的文档。你可以参考以下文档，了解在容灾场景下如何使用备份和恢复功能：

- [如何使用 TiDB 备份和恢复功能?](/br/br-use-overview.md)。
- [TiDB 备份恢复常见问题](/faq/backup-and-restore-faq.md).
- [TiDB 备份与恢复功能架构](/br/backup-and-restore-design.md)
