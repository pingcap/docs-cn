---
title: TiDB Request Unit
summary: TiDB 数据库中 Request Unit (RU) 的概念
---
RU (Request Unit) 是 TiDB 对 CPU、IO 等系统资源的统一抽象的单位, 目前包括 CPU、IOPS 和 IO 带宽三个指标。这三个指标的消耗会按照一定的比例统一到 `RU` 单位上。

在当前的实现中， 我们对用户请求对 TiKV 存储层 CPU 和 IO 资源的消耗，各种的比重因子如下表：

| 资源        | RU 权重 |
|:----------|:------|
| CPU       | 1 RU / 毫秒 |
| 读 IO      | 1 RU / MiB |
| 写 IO      | 5 RU / MiB |
| 一次读请求基本开销 | 1 RU  |
| 一次写请求基本开销 | 3 RU  |

基于上面那张表，如果某个资源组消耗了的 TiKV 时间是 c 毫秒，r1 次请求读取了 r2 MiB 数据，w1 次写请求，写入 w2 MiB 数据，则该资源组消耗的总 RU 的公式如下：
c + (r1 + r2) + (3 * w1 + 5 * w2)