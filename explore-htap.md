---
title: HTAP 深入探索指南
summary: 本文介绍如何深入探索并使用 TiDB 的 HTAP 功能。 
---

# HTAP 深入探索指南

本指南介绍如何深入探索并使用 TiDB 在线事务与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 功能。

> **注意：**
>
> 如果你对 TiDB HTAP 功能还不太了解，希望快速试用体验，请参阅[快速上手 HTAP](/quick-start-with-htap.md)。

## HTAP 适用场景

TiDB HATP 可以满足企业海量数据的增产需求、降低运维的风险成本、与现有的大数据栈无缝缝合，从而实现数据资产价值的实时变现。

以下是三种 HTAP 典型适用场景：

- 混合负载场景

    当将 TiDB 应用于在线实时分析处理的混合负载场景时，开发人员只需要提供一个入口，TiDB 将自动根据业务类型选择不同的处理引擎。

- 实时流处理场景

    当将 TiDB 应用于实时流处理场景时，TiDB 能保证源源不断流入系统的数据实时可查，同时可兼顾高并发数据服务与 BI 查询。

- 数据中枢场景

    当将 TiDB 应用于数据中枢场景时，TiDB 作为数据中枢可以无缝连接数据业务层和数据仓库层，满足不同业务的需求。

如果想了解更多关于 TiDB HTAP 场景信息，请参阅 [PingCAP 官网中关于 HTAP 的博客](https://pingcap.com/blog-cn/#HTAP)。

## HTAP 架构

在 TiDB 中，面向在线事务处理的行存储引擎 [TiKV](/tikv-overview.md) 与面向实时分析场景的列存储引擎 [TiFlash](/tiflash/tiflash-overview.md) 同时存在，自动同步，保持强一致性。

更多架构信息，请参考 [TiDB HTAP 形态架构](/tiflash/tiflash-overview.md#整体架构)。

## HTAP 环境准备

在深入探索 TiDB HTAP 功能前，请依据你的数据场景部署 TiDB 以及对应的数据分析引擎。大数据场景 (100 T) 下，推荐使用 TiFlash MPP 作为 HTAP 的主要方案，TiSpark 作为补充方案。

- TiFlash

    - 如果已经部署 TiDB 集群但尚未部署 TiFlash 节点，请参阅[扩容 TiFlash 节点](/scale-tidb-using-tiup.md#扩容-tiflash-节点)中的步骤在现有 TiDB 集群中添加 TiFlash 节点。
    - 如果尚未部署 TiDB 集群，请使用 [TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)，并在包含最小拓扑的基础上，同时[增加 TiFlash 拓扑架构](/tiflash-deployment-topology.md)。
    - 在决定如何选择 TiFlash 节点数量时，请考虑以下几种业务场景：

        - 如果业务场景以 OLTP 为主，做轻量级的 Ad hoc OLAP 计算，通常部署 1 个或几个 TiFlash 节点就会产生明显的加速效果。
        - 当 OLTP 数据吞吐量对节点 I/O 无明显压力时，每个 TiFlash 节点将会使用较多资源用于计算，这样 TiFlash 集群可实现近似线性的扩展能力。TiFlash 节点数量应根据期待的性能和响应时间调整。
        - 当 OLTP 数据吞吐量较高时（例如写入或更新超过千万行/小时），由于网络和物理磁盘的写入能力有限，内部 TiKV 与 TiFlash 之间的 I/O 会成为主要瓶颈，也容易产生读写热点。此时 TiFlash 节点数与 OLAP 计算量有较复杂非线性关系，需要根据具体系统状态调整节点数量。

- TiSpark

    - 如果你的业务需要基于 Spark 进行分析，请部署 TiSpark（暂不支持 Spark 3.x）。具体步骤，请参阅 [TiSpark 用户指南](/tispark-overview.md)。

<!--    - 实时流处理
  - 如果你想将 TiDB 与 Flink 结合构建高效易用的实时数仓，请参与 Apache Flink x TiDB Meetup 系列讲座。-->

## HTAP 数据准备

TiFlash 部署完成后并不会自动同步数据，你需要指定需要同步到 TiFlash 的数据表。指定后，TiDB 将创建对应的 TiFlash 副本。

- 如果 TiDB 集群中还没有数据，请先迁移数据到 TiDB。详情请参阅[数据迁移](/migration-overview.md)。
- 如果 TiDB 集群中已经有从上游同步过来的数据，TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表，详情请参阅[使用 TiFlash](/tiflash/use-tiflash.md)。

## HTAP 数据处理

使用 TiDB 时，你只需输入 SQL 语句进行查询或者写入需求。对于创建了 TiFlash 副本的表，TiDB 会依靠前端优化器自由选择最优的执行方式。

> **注意：**
> 
> TiFlash 的 MPP 模式默认开启。当执行 SQL 语句时，TiDB 会通过优化器自动判断并选择是否以 MPP 模式执行。
>
> - 如需关闭 MPP 模式，请将系统变量 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 的值设置为 OFF。
> - 如需强制使用 TiFlash 的 MPP 模式执行查询，请将系统变量 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 和 [tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 的值设置为 ON。
> - 如需查看 TiDB 是否选择以 MPP 模式执行，你可以[通过 EXPLAIN 语句查看具体的查询执行计划](/explain-mpp.md#用-explain-查看-mpp-模式查询的执行计划)。如果 EXPLAIN 语句的结果中出现 ExchangeSender 和 ExchangeReceiver 算子，表明 MPP 已生效。

## HTAP 性能监控

在 TiDB 的使用过程中，可以选择以下方式监控 TiDB 集群运行情况并查看性能数据。

- [TiDB Dashboard](/dashboard/dashboard-intro.md)：查看集群整体运行概况，分析集群读写流量分布及趋势变化，详细了解耗时较长的 SQL 语句的执行信息。
- [监控系统 (Prometheus & Grafana)](/grafana-overview-dashboard.md)：查看 TiDB 集群各组件（包括 PD、TiDB、TiKV、TiFlash、TiCDC、Node_exporter）的相关监控参数。

如需查看 TiDB 和 TiFlash 集群报警规则和处理方法，请查阅 [TiDB 集群报警规则](/alert-rules.md)和 [TiFlash 报警规则](/tiflash/tiflash-alert-rules.md)。

## HTAP 故障诊断

在使用 TiDB 的过程中如果遇到问题，请参阅以下文档：

- [分析慢查询](/analyze-slow-queries.md)
- [定位消耗系统资源多的查询](/identify-expensive-queries.md)
- [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)
- [TiDB 集群故障诊断](/troubleshoot-tidb-cluster.md)
- [TiFlash 常见问题](/tiflash/troubleshoot-tiflash.md)

除此之外，你可以在 [Github Issues](https://github.com/pingcap/tiflash/issues) 新建一个 Issue 反馈问题，或者在 [AskTUG](https://asktug.com/) 提交你的问题。

## 探索更多

- 如果要查看 TiFlash 版本，以及 TiFlash 重要日志及系统表，请参阅 [TiFlash 集群运维](/tiflash/maintain-tiflash.md)。
- 如果需要移除某个 TiFlash 节点，请参阅[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。
