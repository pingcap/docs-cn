---
title: Load Base Split
summary: Learn the feature of Load Base Split.
aliases: ['/docs/dev/configure-load-base-split/']
---

# Load Base Split

Load Base Split is a new feature introduced in TiDB 4.0. It aims to solve the hotspot issue caused by unbalanced access between Regions, such as full table scans for small tables.

## Scenarios

In TiDB, it is easy to generate hotspots when the load is concentrated on certain nodes. PD tries to schedule the hot Regions so that they are distributed as evenly as possible across all nodes for better performance.

However, the minimum unit for PD scheduling is Region. If the number of hotspots in a cluster is smaller than the number of nodes, or if a few hotspots have far more load than other Regions, PD can only move the hotspot from one node to another, but not make the entire cluster share the load.

This scenario is especially common with workloads that are mostly read requests, such as full table scans and index lookups for small tables, or frequent access to some fields.

Previously, the solution to this problem was to manually execute a command to split one or more hotspot Regions, but this approach has two problems:

- Evenly splitting a Region is not always the best choice, because requests might be concentrated on a few keys. In such cases, hotspots might still be on one of the Regions after evenly splitting, and it might take multiple even splits to realize the goal.
- Human intervention is not timely or simple.

## Implementation principles

Load Base Split automatically splits the Region based on statistics. It identifies the Regions whose read load or CPU usage consistently exceeds the threshold for 10 seconds, and splits these Regions at a proper position. When choosing the split position, Load Base Split tries to balance the access load of both Regions after the split and avoid access across Regions.

The Region split by Load Base Split will not be merged quickly. On the one hand, PD's `MergeChecker` skips the hot Regions; on the other hand, PD also determines whether to merge two Regions according to `QPS` in the heartbeat information, to avoid the merging of two Regions with high `QPS`.

## Usage

The Load Base Split feature is currently controlled by the following parameters:

- [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold): The QPS threshold at which a Region is identified as a hotspot. The default value is `3000` per second when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is less than 4 GB; otherwise the default value is `7000`.
- [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50): (Introduced in v5.0) The traffic threshold at which a Region is identified as a hotspot. The unit is byte. The default value is 30 MiB per second when `region-split-size` is less than 4 GB; otherwise the default value is 100 MiB per second.
- [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620): (Introduced in v6.2.0) The CPU usage threshold (the percentage of CPU time of the read thread pool) at which a Region is identified as a hotspot. The default value is `0.25` when `region-split-size` is less than 4 GB; otherwise the default value is `0.75`.

If a Region meets one of the following conditions for 10 consecutive seconds, TiKV tries to split the Region:

- the sum of its read requests exceeds `split.qps-threshold`.
- its traffic exceeds `split.byte-threshold`.
- its CPU usage in the Unified Read Pool exceeds `split.region-cpu-overload-threshold-ratio`.

Load Base Split is enabled by default, but the parameter is set to a rather high value. If you want to disable this feature, set `split.qps-threshold` and `split.byte-threshold` high enough and set `split.region-cpu-overload-threshold-ratio` to `0` at the same time.

To modify the parameter, take either of the following two methods:

- Use a SQL statement:

    ```sql
    # Set the QPS threshold to 1500
    SET config tikv split.qps-threshold=1500;
    # Set the byte threshold to 15 MiB (15 * 1024 * 1024)
    SET config tikv split.byte-threshold=15728640;
    # Set the CPU usage threshold to 50%
    SET config tikv split.region-cpu-overload-threshold-ratio=0.5;
    ```

- Use TiKV:

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"1500"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.byte-threshold":"15728640"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.region-cpu-overload-threshold-ratio":"0.5"}'
    ```

Accordingly, you can view the configuration by either of the following two methods:

- Use a SQL statement:

    {{< copyable "sql" >}}

    ```sql
    show config where type='tikv' and name like '%split.qps-threshold%';
    ```

- Use TiKV:

    {{< copyable "shell-regular" >}}

    ```shell
    curl "http://ip:status_port/config"
    ```

> **Note:**
>
> Starting from v4.0.0-rc.2, you can modify and view the configuration using SQL statements.
