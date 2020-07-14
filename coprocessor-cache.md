---
title: Coprocessor Cache
summary: Learn the features of Coprocessor Cache.
aliases: ['/docs/dev/coprocessor-cache/']
---

# Coprocessor Cache

Starting from v4.0, the TiDB instance supports caching the results of the calculation that is pushed down to TiKV (the Coprocessor Cache feature), which can accelerate the calculation process in some scenarios.

## Configuration

You can configure Coprocessor Cache via the `tikv-client.copr-cache` configuration items in the TiDB configuration file. For details about how to enable and configure Coprocessor Cache, see [TiDB Configuration File](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400).

## Feature description

+ When a SQL statement is executed on a single TiDB instance for the first time, the execution result is not cached.
+ Calculation results are cached in the memory of TiDB. If the TiDB instance is restarted, the cache becomes invalid.
+ The cache is not shared among TiDB instances.
+ Only push-down calculation result is cached. Even if cache is hit, TiDB still need to perform subsequent calculation.
+ The cache is in the unit of Region. Writing data to a Region causes the Region cache to be invalid. For this reason, the Coprocessor Cache feature mainly takes effect on the data that rarely changes.
+ When push-down calculation requests are the same, the cache is hit. Usually in the following scenarios, the push-down calculation requests are the same or partially the same:
    - The SQL statements are the same. For example, the same SQL statement is executed repeatedly.

        In this scenario, all the push-down calculation requests are consistent, and all requests can use the push-down calculation cache.

    - The SQL statements contain a changing condition, and the other parts are consistent. The changing condition is the primary key of the table or the partition.

        In this scenario, some of the push-down calculation requests are the same with some previous requests, and these calculation requests can use the cached (previous) push-down calculation result.

    - The SQL statements contain multiple changing conditions and the other parts are consistent. The changing conditions exactly match a compound index column.

        In this scenario, some of the push-down calculation requests are the same with some previous requests, and these calculation requests can use the cached (previous) push-down calculation result.

+ This feature is transparent to users. Enabling or disabling this feature does not affect the calculation result and only affects the SQL execution time.

## Check the cache effect

Currently (TiDB v4.0.0-rc.2), Coprocessor cache is still an experimental feature. Users cannot learn how many push-down requests hit the cache in a SQL statement, or understand the overall cache hits. The corresponding monitoring and checking method will be introduced in later TiDB versions.
