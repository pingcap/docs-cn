---
title: TiDB Resource Unit
summary: TiDB 数据库中 Resource Unit (RU) 的概念
aliases: ['/docs-cn/dev/tidb-RU/','/docs-cn/dev/reference/tidb-RU/']
---
`RU` (Resource Unit) 是 TiDB 对 CPU、IO 等系统资源的统一抽象的单位, 目前包括 CPU、IOPS 和 IO 带宽三个指标。这三个指标的消耗会按照一定的比例统一到 `RU` 单位上。

一个 `RU` 代表一次 64 bytes 点查请求的资源消耗。