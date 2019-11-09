---
title: Follower Read
category: reference
aliases: ['/docs-cn/sql/follower-read/']
---

# Follower Read

TiDB 3.1 新增了 follower read 功能在不牺牲强一致性读的前提下使用 follower 副本来承载数据读取的任务。TiKV 的强一致性 follower read 需要使用 Raft 协议同 leader 进行一次交互获取当前最新已 commit 的 index，通过确保 follower 副本实际 apply 的 index 超过 read index 后再处理用户的数据读取请求，TiKV 的 follower read 可以维持线性一致性。虽然从 follower 副本读取数据时依旧需要同 leader 副本进行一次网络交互无法获得 latency 上的改善，但请求处理过程中资源消耗最大的数据读取部分得以在 follower 副本上执行，从而降低 leader 副本的负担并提升整体读吞吐能力。尤其在极端热点场景 leader 成为读取瓶颈的情况下，开启 TiDB 的 follower read 功能可以获得显著的吞吐能力收益。

## 使用方式

TiDB follower read 可以通过设定 SESSION 变量 tidb_replica_read 为 follower 的方式开启

{{< copyable "sql" >}}

```sql
set @@tidb_replica_read = 'follower';
```

作用域：SESSION

默认值：leader

这个变量用来设置当前会话期待的数据读取方式。设定为默认值 leader 或者空字符串时 TiDB 会维持原有行为方式将所有的读取操作都发送给 leader 副本处理。当设置为 follower 时，TiDB 会选择 follower 副本完成所有的数据读取操作。
