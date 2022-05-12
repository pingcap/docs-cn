---
title: 使用更大的 region size
---

# 使用更大的 region size

TiDB 自动将底层数据进行分片，每个分片压缩前的预期大小约为 96MiB。如果数据量太大，可能会造成分片数量过多，从而带来更多的资源开销。开启 region merge 或者 hibernate regions 都可以解决或缓解过多分片造成的开销问题。从 6.1.0 开始，TiDB 支持设置自定义的分片大小。

> **警告：**
>
> - 使用非默认的分片大小是 6.1.0 引入的实验特性，不建议在生产环境上自行配置。使用此特性的风险至少包括：
> 1. 更容易发生性能抖动；
> 2. 查询性能，尤其是大范围查询数据的性能会有回退；
> 3. 调度变慢。

## 调整 region size

分片的大小可以通过 `coprocessor.region-split-size` 进行设置。我们推荐的设置值包括 96MiB、128MiB、256MiB、512MiB、1GiB。随着大小越大，性能会越来越容易发生抖动。不推荐将大小设置超过 1GiB，强烈建议不超过 10GiB。

分片变大以后，为了增加查询并发，应当设置 `coprocessor.enable-region-bucket` 为 `true`。这个配置会让 TiDB 将每个 region 划分为更小的区间 (bucket)，并且以这个更小的区间作为并发查询单位。bucket 的大小通过 `coprocessor.region-bucket-size` 来控制，默认值为 `128MiB`.
