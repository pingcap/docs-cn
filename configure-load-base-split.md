---
title: Load Base Split
summary: 介绍 Load Base Split 功能。
aliases: ['/docs-cn/dev/configure-load-base-split/']
---

# Load Base Split 

Load Base Split 是 TiKV 在 4.0 版本引入的特性，旨在解决 Region 访问分布不均匀造成的热点问题，比如小表的全表扫描。

## 场景描述

在 TiDB 中，当流量集中在某些节点时很容易形成热点。PD 会尝试通过调度 Hot Region，尽可能让这些 Hot Region 均匀分布在各个节点上，以求获得更好的性能。

但是 PD 的调度的最小粒度是 Region。如果集群的热点数目少于节点数目，或者说存在某几个热点流量远高于其他 Region，对 PD 的热点调度来说，能做到的也只是让热点从一个节点转移到另一个节点，而无法让整个集群承担负载。

这种场景在读请求居多的 workload 中尤为常见。例如对小表的全表扫描和索引查找，或者是对一些字段的频繁访问。

在此之前解决此类问题的办法是手动输入命令去拆分一个或几个热点 Region，但是这样的操作存在以下两个问题：

- 均匀拆分 Region 并不一定是最好的选择，请求可能集中在某几个 Key 上，即使均匀拆分后热点可能仍然集中在其中一个 Region 上，可能需要经过多次均匀拆分才能达到目标。
- 人工介入不够及时和易用。

## 实现原理

Load Base Split 会基于统计信息自动拆分 Region。通过统计去识别出那些读流量在 10s 内持续超过阈值的 Region，并在合适的位置将这些 Region 拆分。在选择拆分的位置时，会尽可能平衡拆分后两个 Region 的访问量，并尽量避免跨 Region 的访问。

在选择 key 的时候，会考虑两点，既要让 split key 两侧的查询尽可能均衡，也要尽可能少地产生 split 后跨 Region 的请求。这些 key 的候选者来自于最近 10s 中采样的请求。

Load Base Split 后的 Region 不会短时间内被 Merge，因为 PD 的 `MergeChecker` 会跳过 hot Region。

## 使用方法

目前的 Load Base Split 的控制参数为 `split.qps-threshold`（QPS 阈值）和 `split.byte-threshold`（流量阈值）。如果连续 10s 内，某个 Region 每秒的各类读请求之和都超过 QPS 阈值或流量阈值，那么就对此 Region 进行拆分。

目前默认开启 Load Base Split，但配置相对保守，`split.qps-threshold` 默认为 `3000`，`split.byte-threshold` 默认为 30MB/s，满足任何一个条件即会进行 split。如果想要关闭这个功能，将这两个阈值全部都调到足够高即可。

对于选择 key 的阈值，则由`split.split-balance-score`和`split.split-contained-score`控制，前者确保 Region 切分后左右访问尽量均匀，数值越小越均匀，但也可能导致无法切分；后者避免 split 产生过多跨 Region 的请求，数值越小，切分后跨 Region 的访问越少。`split.split-balance-score` 默认值是 0.25，`split.split-contained-score` 默认值是 0.5。

如果期待有 Load Base split，但是却没有，一般有两种原因，一种是 Region 的 QPS 和 byte 均低于阈值，这个时候可以根据当前集群中流量较大的 region 向下进行调整；另一种是没有合适的 key 进行切分，这时候监控会有 load_fit 和 no_fit_key 同时出现，可以根据具体的原因进行调整，但需要注意的是，可能会导致切分后流量不均匀或者产生跨 Region 的请求过多而降低性能。

以`split.qps-threshold`为例，目前有两种办法修改配置：

- 通过 SQL 语句修改，例如：

  {{< copyable "sql" >}}

  ```sql
  set config tikv split.qps-threshold=3000
  ```
- 通过 TiKV 修改，例如：

  {{< copyable "shell-regular" >}}

  ```shell
  curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"3000"}'
  ```

同理，目前也有两种办法查看配置：

- 通过 SQL 查看，例如：

  {{< copyable "sql" >}}

  ```sql
  show config where type='tikv' and name like '%split.qps-threshold%'
  ```
- 通过 TiKV 查看，例如：

  {{< copyable "shell-regular" >}}

  ```shell
  curl "http://ip:status_port/config"
  ```

## 监控信息

与 Load Base Split 相关的监控有两个面板，在 TiKV Detail 中 Raft Admin 下的 "Load base split event" 和 "TopN QPS exceeds threshold"。

前者的内容通常来说有三类：

1. load_fit，也即 region 的 QPS 或者 Byte 流量符合切分的需求
2. no_fit_key，也即没有合适的 key 去 split。
3. prepare_to_split，也即准备去 split。

后者则可以看到每个 store 中 QPS 超过阈值的 Region，默认显示 Top1，最多能显示 Top10。值得一提的是，如果想查看更详细的信息，可以通过 pd-ctl 使用 `pd-ctl hot read` 去查询。

> **注意：**
>
> 从 v4.0.0-rc.2 起可以使用 SQL 语句来修改和查看配置。
>

