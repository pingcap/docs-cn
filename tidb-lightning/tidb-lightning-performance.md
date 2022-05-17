---
title: TiDB Lightning 性能优化
summary: 如何让 TiDB Lightning 运行的更快。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-performance/','/docs-cn/dev/reference/tools/tidb-lightning/performance/']
---

# TiDB Lightning 性能优化
本文主要介绍 TiDB Lightning 的性能基线以及如何调优。如果你对 TiDB Lightning 还不太了解，请先看[快速上手教程](https://docs.pingcap.com/zh/tidb/stable/get-started-with-tidb-lightning).

## Lightning 的导入模式选择
Lightning支持以下后端
- Local-backend
- TiDB-backend

链路越短，速度越快。所以，在数据量较大的情况下，建议选择 `Local-backend` 模式。
但如果 TiDB 存在边导入，边提供服务的需求，则只能选择 `TiDB-backend` 模式.此外，在`TiDB-backend` 中，目前是以数据量`1M`大小一个事务的方式写入。

更详细的说明，请看文档 [TiDB Lightning 后端](https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-backends)

## 硬件需求
不可否则，当前 Lightning 对硬件的需求是比较高的，因为里面有很多排序的动作。
因此，建议使用有较高存储和网络配置的服务器。
[相关配置](https://docs.pingcap.com/zh/tidb/stable/deploy-tidb-lightning#%E7%A1%AC%E4%BB%B6%E9%9C%80%E6%B1%82)

## Lightning 如何并行
![Lightning的并行](/media/lightning/lightning-concurrency.png)

1. 首先，我们很容易发现，不同表是可以并行导入的。参数 `index-concurrency` 就是用于控制可以几张表同时导入。
2. 如果表非常大，我们会按照100GB的大小，将表分割成多个批次来处理。总的并发数由 `table-concurrency` 控制。这是扫描文件的并发数。
3. 我们知道，Local-backend 导入模式是会将数据在本地进行编码排序。`region-concurrency`参数就是控制数据处理的并行度。默认配置为CPU核数。在 Tidb-backend 中，这个参数就是等同于写入并发数。

## 导入数据源格式的区别
lightning 支持多种数据格式导入，最常见的是 SQL 和 CSV。lightning 会尽量并行处理数据，通常情况是一个协程处理一个文件。但如果 CSV 文件符合严格格式，则 lightning 可以将单个 CSV 大文件，分割为多个文件块进行并行处理。[相关设置](https://docs.pingcap.com/zh/tidb/v5.3/migrate-from-csv-using-tidb-lightning#%E8%AE%BE%E7%BD%AE-strict-format-%E5%90%AF%E7%94%A8%E4%B8%A5%E6%A0%BC%E6%A0%BC%E5%BC%8F)  
而 SQL 文件无法进行快速分割，就无法通过分割文件提高并行度。因此，在导出数据时，尽量避免单个 SQL 文件过大，建议文件大小在256M左右。

## 总结
1. 如果是从0开始导入，不需要边导入边提供服务，请优先选择 `Local-backend` 模式。
2. Lightning 属于计算，存储，网络密集型的服务，所以，建议使用计算，网络，存储都比较高的服务器运行 Lightning，并避免混部.
3. 如果数据量非常大，dumpling时，不建议导出成一个 SQL 文件，这会影响导入速度。
