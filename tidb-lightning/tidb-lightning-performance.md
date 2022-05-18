---
title: TiDB Lightning 性能优化
summary: 如何让 TiDB Lightning 运行的更快。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-performance/','/docs-cn/dev/reference/tools/tidb-lightning/performance/']
---

# TiDB Lightning 性能优化
本文主要介绍 TiDB Lightning 的性能基线以及如何调优。如果你对 TiDB Lightning 还不太了解，请先看[快速上手教程](https://docs.pingcap.com/zh/tidb/stable/get-started-with-tidb-lightning).

## Lightning 的导入模式选择
Lightning支持以下导入模式
- Local-backend
- TiDB-backend

链路越短，速度越快。所以，在数据量较大的情况下，建议选择 `Local-backend` 模式。
但如果 TiDB 存在边导入，边提供服务的需求，则只能选择 `TiDB-backend` 模式.此外，在`TiDB-backend` 中，目前是以数据量`1M`大小一个事务的方式写入。

更详细的说明，请看文档 [TiDB Lightning 后端](https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-backends)  

**注意**: Importer-backend已弃用，推荐使用 `Local-backend`。

## 硬件需求
不可否则，当前 Lightning 对硬件的需求是比较高的，因为里面有很多排序的动作。
因此，建议使用有较高存储和网络配置的服务器。同样，也请注意目标 `TiDB` 集群的硬件配置,特别是存储空间。
#### lightning 推荐硬件配置
CPU: ≥32C
内存: ≥20G
存储: SSD硬盘,侧重读
网卡: 带宽≥1GB/s

根据内部测试，使用推荐配置可达到300G/s的导入速度。更多部署相关的信息请看 [链接](https://docs.pingcap.com/zh/tidb/stable/deploy-tidb-lightning)


## Lightning 如何并行
![Lightning的并行](/media/lightning/lightning-concurrency.png)

1. 首先，我们能想到，不同表肯定能并行导入。参数 `index-concurrency` 就是用于控制可以几张表同时导入。导入时，每张表被切分成一个用于存储索引的"索引引擎"和若干存储行数据的"数据引擎",`index-concurrency`用于调整"索引引擎"的并发度，所以等同于表的并发度。
2. 如果表非常大，我们会按照100GB的大小，将表分割成多个批次来处理。文件扫描的并发度由 `table-concurrency` 控制。上述两个参数对导入速度影响不大，使用默认值即可。
3. 我们知道，Local-backend 导入模式是会将数据在本地进行编码排序。`region-concurrency`参数就是控制数据处理的并行度,在 Tidb-backend 中，这个参数就是等同于写入并发数。默认值为CPU核数不用管，如果和其它组件混跑，建议设置成 CPU 核数的 75%。

## 导入数据源格式的区别
lightning 支持多种数据格式导入，最常见的是 SQL 和 CSV。lightning 会尽量并行处理数据，由于文件必须顺序读取，所以处理并行度 `region-concurrency` 无法大于文件数，这导致大文件导入时会存在性能退化。  
但如果 CSV 文件符合严格格式，则 lightning 可以将单个 CSV 大文件，分割为多个文件块进行并行处理。[相关设置](https://docs.pingcap.com/zh/tidb/v5.3/migrate-from-csv-using-tidb-lightning#%E8%AE%BE%E7%BD%AE-strict-format-%E5%90%AF%E7%94%A8%E4%B8%A5%E6%A0%BC%E6%A0%BC%E5%BC%8F)  
而 SQL 文件无法进行快速分割，就无法通过分割文件提高并行度。因此，在导出数据时，尽量避免单个 SQL 文件过大，建议文件大小在256M左右。

## 总结
1. 如果是从0开始导入，不需要边导入边提供服务，请优先选择 `Local-backend` 模式。
2. 参数选择上，如果不存在组件混部，使用默认参数即可。
3. Lightning 属于计算，存储，网络密集型的服务，所以，建议使用计算，网络，存储都比较高的服务器运行 Lightning，并避免混部.
4. 如果数据量非常大，dumpling时，不建议导出成一个 SQL 文件，这会影响导入速度。
