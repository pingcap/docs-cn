---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# Tune Region Performance

This document introduces how to tune Region performance by adjusting the Region size and how to use bucket to optimize concurrent queries when the Region size is large. In addition, this document introduces how to enhance the ability of PD to provide Region information to TiDB nodes by enabling the Active PD Follower feature.

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

## Use the Active PD Follower feature to enhance the scalability of PD's Region information query service

> **Warning:**
>
> The Active PD Follower feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

To ensure high availability, the PD leader synchronizes Region information with its followers in real time. PD followers maintain and store Region information in memory, enabling them to process Region information requests. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also directly handle Region requests, thereby reducing the CPU pressure on the PD leader.

PD ensures that the Region information in TiDB is always up-to-date by maintaining the status of Region synchronization streams and using the fallback mechanism of TiKV client-go. 

- When the network between the PD leader and a follower is unstable or a follower is unavailable, the Region synchronization stream is disconnected, and the PD follower rejects Region information requests. In this case, TiDB automatically retries the request to the PD leader and temporarily marks the follower as unavailable. 
- When the network is stable, because there might be a delay in the synchronization between the leader and the follower, some Region information obtained from the follower might be outdated. In this case, if the KV request corresponding to the Region fails, TiDB automatically re-requests the latest Region information from the PD leader and sends the KV request to TiKV again.
