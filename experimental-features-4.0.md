---
title: TiDB 4.0 Experimental Features
summary: Learn the experimental features of TiDB v4.0.
---

# TiDB 4.0 Experimental Features

This document introduces the experimental features of TiDB v4.0. It is **NOT** recommended to use these features in the production environment.

## Scheduling

+ Cascading Placement Rules is an experimental feature of the Placement Driver (PD) introduced in v4.0. It is a replica rule system that guides PD to generate corresponding schedules for different types of data. By combining different scheduling rules, you can finely control the attributes of any continuous data range, such as the number of replicas, the storage location, the host type, whether to participate in Raft election, and whether to act as the Raft leader. See [Cascading Placement Rules](/configure-placement-rules.md) for details.
+ Elastic scheduling is an experimental feature based on Kubernetes, which enables TiDB to dynamically scale in and out nodes. This feature can effectively mitigate the high workload during peak hours of an application and saves unnecessary overhead.

## SQL feature

Support the expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details.

## Service-level features

+ TiDB instances support caching the calculation results that the operator has pushed down to TiKV in the unit of Region, which improves the efficiency of SQL executions in the following scenarios. See [Coprocessor Cache](/coprocessor-cache.md) for details.
    - The SQL statements are the same.
    - The SQL statements contain a changing condition (limited to the primary key of tables or partitions), and the other parts are consistent.
    - The SQL statements contain multiple changing conditions and the other parts are consistent. The changing conditions exactly match a compound index column.
+ Support persisting configuration parameters in PD and dynamically modifying configuration items to improve product usability.

## TiCDC

TiCDC is a tool for replicating the incremental data of TiDB. This tool is implemented by pulling TiKV change logs, which ensures high reliability and availability of data. You can subscribe to the change information of data, and the system automatically sends data to the downstream. Currently, the downstream database must be MySQL compatible (such as MySQL and TiDB) or Kafka. You can also extend the supported downstream systems based on the [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md). See [TiCDC](/ticdc/ticdc-overview.md) for details.
