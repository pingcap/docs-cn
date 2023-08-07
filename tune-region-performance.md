---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# Tune Region Performance

This document introduces how to tune Region performance by adjusting the Region size and how to use bucket to optimize concurrent queries when the Region size is large.

## Overview

TiKV automatically [shards bottom-layered data](/best-practices/tidb-best-practices.md#data-sharding). Data is split into multiple Regions based on the key ranges. When the size of a Region exceeds a threshold, TiKV splits it into two or more Regions.

When processing a large amount of data, TiKV might split too many Regions, which causes more resource consumption and [performance regression](/best-practices/massive-regions-best-practices.md#performance-problem). For a certain amount of data, the larger the Region size, the fewer the Regions. Since v6.1.0, TiDB supports setting customizing Region size. The default size of a Region is 96 MiB. To reduce the number of Regions, you can adjust Regions to a larger size.

To reduce the performance overhead of many Regions, you can also enable [Hibernate Region](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances) or [`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval).

## Use `region-split-size` to adjust Region size

> **Warning:**
>
> Currently, customized Region size is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments. The risks are as follows:
>
> + Performance jitter might be caused.
> + The query performance, especially for queries that deal with a large range of data, might decrease.
> + The Region scheduling slows down.

To adjust the Region size, you can use the [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) configuration item. The recommended sizes are 96 MiB, 128 MiB, or 256 MiB. The larger the `region-split-size` value, the more jittery the performance will be. It is NOT recommended to set the Region size over 1 GiB. Avoid setting the size to more than 10 GiB. When TiFlash is used, the Region size should not exceed 256 MiB.

When the Dumpling tool is used, the Region size should not exceed 1 GiB. In this case, you need to reduce the concurrency after increasing the Region size; otherwise, TiDB might run out of memory.

## Use bucket to increase concurrency

> **Warning:**
>
> Currently, this is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments.

When Regions are set to a larger size, you need to set [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610) to `true` to increase the query concurrency. When you use this configuration, Regions are divided into buckets. Buckets are smaller ranges within a Region and are used as the unit of concurrent query to improve the scan concurrency. You can control the bucket size using [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610).