---
title: 高可用常见问题
summary: 介绍高可用相关的常见问题。
aliases: ['/docs-cn/stable/faq/high-availability-faq/','/docs-cn/v4.0/faq/high-availability-faq/']
---

# 高可用常见问题

本文档介绍高可用相关的常见问题。

## TiDB 数据是强一致的吗？

通过使用 [Raft 一致性算法](https://raft.github.io/)，数据在各 TiKV 节点间复制为多副本，以确保某个节点挂掉时数据的安全性。

在底层，TiKV 使用复制日志 + 状态机 (State Machine) 的模型来复制数据。对于写入请求，数据被写入 Leader，然后 Leader 以日志的形式将命令复制到它的 Follower 中。当集群中的大多数节点收到此日志时，日志会被提交，状态机会相应作出变更。

## 官方有没有三中心跨机房多活部署的推荐方案？

从 TiDB 架构来讲，支持真正意义上的跨中心异地多活，从操作层面讲，依赖数据中心之间的网络延迟和稳定性，一般建议延迟在 5ms 以下，目前我们已经有相似客户方案，具体请咨询官方 [info@pingcap.com](mailto:info@pingcap.com)。
