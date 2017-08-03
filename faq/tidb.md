---
title: TiDB
category: faq-product
---

# TiDB

## TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数（`--lease=60`），其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。


## 在使用 TiDB 时，DDL 语句为什么这么慢？

TiDB 实现了 Google F1 的在线 Schema 变更算法（具体参见 [F1 论文](http://research.google.com/pubs/pub41376.html) 和[我们的一篇 Blog](https://github.com/ngaut/builddatabase/blob/master/f1/schema-change.md)）。 一般情况下，DDL 并不是一个频繁的操作，我们首先要保证的是数据的一致性以及线上业务不受影响。一个完整的 DDL 过程会有 2 到 5 个阶段（取决于语句类型），每个阶段至少会执行 2\*lease 时间，假设 lease 设为 1分钟，对于 Drop Table 语句（需要两个阶段），会执行 2\*2\*1 = 4 分钟。除此之外，DDL 的时间还取决其他的条件，比如做 Add Index 操作时，表中已有的数据量是影响 DDL 时间的主要因素。我们也了解过 Google 内部在 F1 上是如何做 DDL，一般是提交给 DBA，DBA 再通过专用的工具执行，执行的时间会很长。

## TiDB 是否支持其他存储引擎？

是的。除了 TiKV 之外，TiDB 还支持一些流行的单机存储引擎，比如 GolevelDB, RocksDB,  BoltDB 等。如果一个存储引擎是支持事务的 KV 引擎，并且能提供一个满足 TiDB 接口要求的 Client，即可接入 TiDB。

## TiDB 中 raft 的日志存储在哪里？
在 rocksdb 中。