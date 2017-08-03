---
title: SQL 优化
category: faq-sql
---

# SQL 优化

## select count(1) 比较慢，有优化方法么？
count(1) 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考https://github.com/pingcap/docs-cn/blob/master/sql/tidb-specific.md#tidb_distsql_scan_concurrency。 但是也要看 cpu、io 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

1. 建议提升硬件，符合我们的标准https://github.com/pingcap/docs-cn/blob/master/op-guide/recommendation.md
2. 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间
3. 测试大数据量的 count
4. 调优 TiKV 配置： https://github.com/pingcap/docs-cn/blob/master/op-guide/tune-tikv.md

