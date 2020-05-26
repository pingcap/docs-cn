---
title: 日常巡检
summary: 介绍 TiDB 集群需要常关注的性能指标。
category: reference
---

# 日常巡检

TiDB 作为分布式数据库，对比单机数据库机制更加复杂。自带的 metrics 和监控项丰富。为了更便捷地运维 TiDB，本文介绍 TiDB 集群需要常关注的关键指标项。

## Dashboard 关键指标

从 4.0 版本开始，TiDB 提供了一个新的 Dashboard 运维管理工具，集成在 PD 组件上，默认地址为 <http://pd-ip:pd_port/dashboard>。

TiDB Dashboard 从用户角度出发，简化管理员对 TiDB 数据库的运维，可在一个界面查看整个分布式数据库集群的运行状况，包括数据热点、SQL 运行情况、集群信息、日志搜索、实时性能分析等。

## 集群状态

### 实例面板

![实例面板](/media/daily-inspection/instance-status-panel.png)

以上实例面板注意项说明如下：

+ **状态**查看是否正常，如果在线可忽略此项。
+ **启动时间**是关键指标。如果有发现启动时间有变动，那么需要排查组件重启的原因。
+ **版本**、**部署路径**、**Git 哈希值**需要关注，避免有部署路径和版本不一致或者错误的情况。

### 主机面板

![主机面板](/media/daily-inspection/host-panel.png)

通过主机面板可以查看 CPU、内存、磁盘使用率。当任何资源的平均使用率超过 60%，推荐安排扩容计划，达到 80%，推荐进行扩容。

### SQL 分析

![SQL 分析面板](/media/daily-inspection/sql-analysis-panel.png)

通过 SQL 分析面板可以分析对集群影响较大的慢 SQL，然后进行对应的 SQL 优化。

## 监控指标

## Region 信息

![Region 信息面板](/media/daily-inspection/region-panel.png)

以上面板说明如下：

+ `miss-peer-region-count` 是缺副本，不会一直大于 0。
+ `extra-peer-region-count` 是多副本，调度过程中会有产生。
+ `empty-region-count` 是空 Region，一般是 `TRUNCATE TABLE`/`DROP TABLE` 语句导致。如果数量较多，可以考虑开启跨表 Region merge。
+ `pending-peer-region-count` 是 Raft log 落后的 Region。由于调度产生少量的 pending peer 是正常的，但是如果持续很高，可能有问题。
+ `down-peer-region-count` 是 Raft leader 上报有不响应 peer 的 Region 数量。
+ `offline-peer-region-count` 是下线过程中的 Region 数量。

原则上来说，该监控面板偶尔有数据是符合预期的。但长期有数据，需要排查是否存在问题。

## 响应时间

### KV Request Duration

![TiKV 相应时间](/media/daily-inspection/kv-duration-panel.png)

TiKV 当前 .99（百分位）的响应时间。如果发现有明显高的节点，可以排查是否有热点，或者相关节点性能较差。

### PD TSO Wait Duration

![TiDB 从 PD 获取 TSO 的时间](/media/daily-inspection/pd-duration-panel.png)

TiDB 从 PD 获取 TSO 的时间。如果相关响应时间较高，一般常见原因如下：

+ TiDB 到 PD 的网络延迟较高，可以手动 Ping 一下网络延迟。
+ TiDB 压力较高，导致获取较慢。
+ PD 服务器压力较高，导致获取较慢。

## 硬件监控

### Overview 面板

![Overview 面板](/media/daily-inspection/overview-panel.png)

以上面板展示常见的负载、内存、网络、IO 监控。发现有瓶颈时，推荐扩容或者优化集群拓扑，优化 SQL、集群参数等。

## 异常监控

![异常监控面板](/media/daily-inspection/failed-query-panel.png)

以上面板展示每个 TiDB 实例上，执行 SQL 语句发生的错误，并按照错误类型进行统计，例如语法错误、主键冲突等。

## GC 状态

![GC 状态面板](/media/daily-inspection/garbage-collation-panel.png)

以上面板展示最后 GC（垃圾清理）的时间，观察 GC 是否正常。如果 GC 发生异常，可能会造成历史数据存留过多，影响访问效率。
