---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# Tune Region Performance

This document introduces how to tune Region performance by adjusting the Region size and how to use bucket to optimize concurrent queries when the Region size is large.

## Overview

TiKV automatically [shards bottom-layered data](/best-practices/tidb-best-practices.md#data-sharding). Data is split into multiple Regions based on the key ranges. When the size of a Region exceeds a threshold, TiKV splits it into two or more Regions.

In scenarios involving large datasets, if the Region size is relatively small, TiKV might have too many Regions, which causes more resource consumption and [performance regression](/best-practices/massive-regions-best-practices.md#performance-problem). Since v6.1.0, TiDB supports customizing Region size. The default size of a Region is 96 MiB. To reduce the number of Regions, you can adjust Regions to a larger size.

To reduce the performance overhead of many Regions, you can also enable [Hibernate Region](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances) or [`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval).

## Use `region-split-size` to adjust Region size

> **Note:**
>
> The recommended range for the Region size is [48MiB, 258MiB]. Commonly used sizes include 96 MiB, 128 MiB, and 256 MiB. It is NOT recommended to set the Region size beyond 1 GiB. Avoid setting the size to more than 10 GiB. An excessively large Region size might result in the following side effects:
>
> + Performance jitters
> + Decreased query performance, especially for queries that deal with a large range of data
> + Slower Region scheduling

To adjust the Region size, you can use the [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) configuration item. When TiFlash is used, the Region size should not exceed 256 MiB.

When the Dumpling tool is used, the Region size should not exceed 1 GiB. In this case, you need to reduce the concurrency after increasing the Region size; otherwise, TiDB might run out of memory.

## Use bucket to increase concurrency

> **Warning:**
>
> Currently, this is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments.

After Regions are set to a larger size, if you want to further improve the query concurrency, you can set [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610) to `true`. When you use this configuration, Regions are divided into buckets. Buckets are smaller ranges within a Region and are used as the unit of concurrent query to improve the scan concurrency. You can control the bucket size using [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610).