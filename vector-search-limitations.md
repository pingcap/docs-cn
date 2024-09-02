---
title: 向量搜索限制
summary: 本文介绍 TiDB 的向量搜索限制。
---

# 向量搜索限制

本文档描述了 TiDB 向量搜索的已知限制。我们将继续努力，通过添加更多功能来提升您的使用体验。

- 最大支持16383维[向量](/vector-search-data-types.md)。

- 向量数据仅支持单精度浮点数 (Float32)。

- 创建[向量索引](/vector-search-index.md)时只支持余弦距离和L2距离。

## 反馈

我们非常重视您的反馈意见，并随时准备提供帮助：

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)