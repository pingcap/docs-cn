---
title: 向量搜索限制
summary: 本文介绍 TiDB 的向量搜索限制。
---

# 向量搜索限制

本文档介绍 TiDB 向量搜索的已知限制。我们会持续新增更多功能来提升使用体验。

- 向量最大支持 16383 维。
- 向量数据中不支持 `NaN`、`Infinity` 和 `-Infinity` 浮点数。
- 目前，向量数据类型不能存储双精度浮点数。计划在未来的版本中支持这一功能。在此期间，如果为向量数据类型导入双精度浮点数，它们将被转换为单精度数。


## 反馈

我们非常重视您的反馈意见，并随时准备为您提供帮助：

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)