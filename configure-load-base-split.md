---
title: Load Base Split
summary: 如何配置 Load Base Split。
category: how-to
---

# Load Base Split 

Load Base Split 是 TiKV 在 4.0 版本引入的特性，旨在解决 Region 访问分布不均匀造成的热点问题。适用场景有小表的全表扫描或明星字段的访问。

## 背景

对于 TiDB 来说，当流量集中在某些 Store 的时候很容易形成热点， PD 会尝试通过调度 Hot Region，尽可能让这些 Hot Region 均匀分布在各个节点上，以求获得更好的性能。

但是 PD 的调度的最小粒度是 Region，如果集群的热点数目少于节点数目，或者说存在某几个热点流量远高于其他 Region，这样的情况下，对 PD 的热点调度来说，能做到的也只是让热点从一个节点转移到另一个节点，而无法让整个集群承担负载。

这种场景在读请求居多的 workload 中尤为常见。比如对小表的全表扫描和索引查找，或者是对一些明星字段的频繁访问。

在此之前解决此类问题的办法是手动输入命令去拆分这一个或这几个 Region，但是这样有两个问题：

1. 均匀拆分 Region 并不一定是最好的选择，请求可能集中在某几个 Key 上，即使均匀拆分后可能仍然落在其中一个 Region 上，可能需要经过多次均匀拆分才能达到目标。

2. 需要人工介入，不够及时和易用。

## 原理

Load Base Split 会基于统计信息来自动地解决这个问题，通过统计去识别出那些读流量在10s 内持续超过阈值的 Region，并在合适的位置将其拆分。在选择拆分的位置时，我们会尽可能平衡拆分后两个 Region 的访问量，并尽量避免跨 Region 的访问。

Load Base Split 后的 Region 是否会被迅速 Merge，答案是否定的，一方面，PD 的 `MergeChecker` 会跳过 hot Region ，另一方面我们也会针对心跳信息中的 `QPS`去进行判断，避免 Merge 两个 `QPS` 很高的 Region。

## 使用

目前的 Load Base Split 的控制参数，主要是前文提到的阈值，也即 `split.qps-threshold`。当下的策略相对保守，默认值是 3000。也就是说，如果连续 10s 内，某个 Region 每秒的各类读请求之和超过 3000 ，那么就对对此 Region 进行拆分。如果想要关闭这个功能，可以将这个阈值调到足够高即可。

目前有两种办法修改配置：

1. 通过 SQL 修改，`set config tikv split.qps-threshold=3000`

2. 通过 TiKV 修改，`curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"3000"}'`

同理，目前也有两种办法查看配置：

1. 通过 SQL 查看，`show config where type='tikv' and name like '%split.qps-threshold%'`
2. 通过 TiKV 查看，`curl "http://ip:status_port/config"`

*注：使用 SQL 修改和查看配置的最低版本 4.0.0-rc2*
