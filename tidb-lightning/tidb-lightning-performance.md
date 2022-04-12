---
title: TiDB Lightning 性能优化
summary: 如何让 TiDB Lightning 运行的更快。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-performance/','/docs-cn/dev/reference/tools/tidb-lightning/performance/']
---

# TiDB Lightning 性能优化
本文主要介绍 TiDB Lightning 的性能基线以及如何调优。如果你对 TiDB Lightning 还不太了解，请先看[快速上手教程](https://docs.pingcap.com/zh/tidb/stable/get-started-with-tidb-lightning).

## 


## 总结
1. 如果数据量非常大，dumpling时，不建议导出成一个文件，这会影响导入速度。
