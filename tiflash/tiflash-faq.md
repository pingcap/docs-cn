---
title: TiFlash 常见问题
aliases: ['/docs-cn/v3.1/reference/tiflash/faq/']
---

# TiFlash 常见问题

本文介绍 TiFlash 使用过程中的常见问题及解决方案。

## TiFlash 是否可直接写入？

TiFlash 暂时无法直接接受写入，只能通过写入 TiKV 再同步到 TiFlash。

## 如果想在已经存在的集群增加 TiFlash，怎么去估算存储资源？

可以衡量哪些表可能需要加速，这些表的单副本大小大致就是 TiFlash 两副本所需的空间，再算上计划的余量就行。

## TiFlash 的数据如何做到高可用？

TiFlash 可以通过 TiKV 恢复数据。只要 TiKV 的对应 Region 是可用的，TiFlash 就可以从中恢复数据。

## TiFlash 推荐设置多少个副本？

如果需要 TiFlash 服务本身高可用（并非数据高可用），那么推荐将 TiFlash 设置成 2 副本；如果可以允许 TiFlash 丢失节点的情况下通过 TiKV 副本继续服务，那么也可以使用单副本。

## 什么时候使用 TiSpark 进行查询？什么时候使用 TiDB server 进行查询？

如果查询以单表聚合和过滤为主，那么 TiDB server 比 TiSpark 在列存上拥有更好的性能；如果查询以表连接为主，那么推荐使用 TiSpark。
