---
title: 下推计算结果缓存
category: reference
---

# 下推计算结果缓存

TiDB 从 4.0 起支持下推计算结果缓存功能（即 Coprocessor Cache）。开启该功能后，将在 TiDB 侧缓存下推给 TiKV 计算的结果，在部分场景下起到加速效果。

## 配置

Coprocessor Cache 功能在 GA 版本默认关闭，对用户透明，默认占用每个 TiDB 1GB 内存大小进行缓存。每个 TiDB 之间的缓存数据不共享。

修改以下 TiDB 配置可以对缓存细节进行调节：

```toml
[tikv-client.copr-cache]
# Whether to enable the copr cache. The copr cache saves the result from TiKV Coprocessor in the memory and
# reuses the result when corresponding data in TiKV is unchanged, on a region basis.
enabled = true

# The memory capacity in MB of the cache.
capacity-mb = 1000.0

# Requests that have result set size bigger than specified will not be cached.
admission-max-result-mb = 10.0
# Requests that have process time less than specified will not be cached.
admission-min-process-ms = 5
```

参数说明：

- `capacity-mb`: 缓存的总数据量大小，单位是 MB。当缓存空间满时，旧缓存条目将被逐出（LRU）。

- `admission-max-result-mb`：指定能被缓存的最大单个下推计算结果集。若单个下推计算在 Coprocessor 上返回的结果集大于该参数指定的大小，则结果集不会被缓存。

  调大该值可以缓存更多种类下推请求，但也将导致缓存空间更容易被占满。注意，每个下推计算结果集大小一般都会小于 Region 大小，因此将该值设置得远超过 Region 大小没有意义。

- `admission-min-process-ms`: 最小缓存的单个下推计算结果集计算时间，单位是 ms。若单个下推计算在 Coprocessor 上的计算时间小于该参数指定的时间，则结果集不会被缓存。

  处理得很快的请求没有必要进行缓存，仅对处理时间很长的请求进行缓存，减少缓存被逐出的概率，这是本配置参数的意义。

## 特性

1. 所有 SQL 在单个 TiDB 上的首次执行都不会被缓存。

2. 缓存仅存储在 TiDB 内存中，TiDB 重启后缓存会失效。

3. 不同 TiDB 之间不共享缓存。

4. 缓存的是下推计算结果，即使缓存命中，后续仍有 TiDB 计算。

5. 缓存以 Region 为单位，对 Region 的写入会导致涉及该 Region 的缓存失效。

   基于此原因，该功能主要会对很少变更的数据有效果。

6. 下推计算请求相同时，缓存会被命中。通常在以下场景下，下推计算的请求是相同或部分相同的：

   - SQL 语句完全一致，例如重复执行相同的 SQL 语句。

     该场景下所有下推计算的请求都是一致的，所有请求都能利用上下推计算缓存。

   - SQL 语句包含一个变化的条件，其他部分一致，变化的条件是表主键或分区主键。

     该场景下一部分下推计算的请求会与之前出现过的一致，部分请求能利用上下推计算结果缓存。

   - SQL 语句包含多个变化的条件，其他部分一致，变化的条件完全匹配一个复合索引列。

     该场景下一部分下推计算的请求会与之前出现过的一致，部分请求能利用上下推计算结果缓存。

## 检验缓存效果

目前 Coprocessor Cache 尚为实验性功能，用户无法判断一个 SQL 语句中有多少下推请求命中了缓存，也无法了解整体的缓存命中情况。后续版本中将引入相应的监控和检查方法。
