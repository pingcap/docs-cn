---
title: Key Metrics
category: operations
---

# Key Metrics

If you use Ansible to deploy TiDB cluster, you can deploy the monitoring system at the same time. See [Overview of the Monitoring Framework](monitor-overview.md) for more information.

The Grafana dashboard is divided into four sub dashboards: node_export, PD, TiKV, and TiDB. There are a lot of metics there to help you diagnose. For routine operations, some of the key metrics are displayed on the Overview dashboard so that you can get the overview of the status of the components and the entire cluster. See the following section for their descriptions:

## Key metrics description

Service | Panel Name | Description | Normal Range
---- | ---------------- | ---------------------------------- | --------------
PD | Storage Capacity | the total storage capacity of the TiDB cluster |
PD | Current Storage Size | the occupied storage capacity of the TiDB cluster |
PD | Store Status  -- up store | the number of TiKV nodes that are up |
PD | Store Status  -- down store | the number of TiKV nodes that are down | `0`. If the number is bigger than `0`, it means some node(s) are not down.
PD | Store Status  -- offline store | the number of TiKV nodes that are manually offline|
PD | Store Status  -- Tombstone store | the number of TiKV nodes that are Tombstone|
PD | Current storage usage | the storage occupancy rate of the TiKV cluster | If it exceeds 80%, you need to consider adding more TiKV nodes.
PD | 99% completed cmds duration seconds | the 99th percentile duration to complete a pd-server request| less than 5ms
PD | average completed cmds duration seconds | the average duration to complete a pd-server request | less than 50ms
PD | leader balance ratio | the leader ratio difference of the nodes with the biggest leader ratio and the smallest leader ratio | It is less than 5% for a balanced situation. It becomes bigger when a node is restarting.
PD | region balance ratio | the region ratio difference of the nodes with the biggest region ratio and the smallest region ratio | It is less than 5% for a balanced situation. It becomes bigger when adding or removing a node.
TiDB | handle requests duration seconds | the response time to get TSO from PD| less than 100ms
TiDB | tidb server QPS | the QPS of the cluster | application specific
TiDB | connection count | the number of connections from application servers to the database | Application specific. If the number of connections hops, you need to find out the reasons. If it drops to 0, you can check if the network is broken; if it surges, you need to check the application.
TiDB | statement count | the number of different types of statement within a given time | application specific
TiDB | Query Duration 99th percentile | the 99th percentile query time |
TiKV | 99%  & 99.99% scheduler command duration | the 99th percentile and 99.99th percentile scheduler command duration| For 99%, it is less than 50ms; for 99.99%, it is less than 100ms.
TiKV | 95%  & 99.99% storage async_request duration | the 95th percentile and 99.99th percentile Raft command duration | For 95%, it is less than 50ms; for 99.99%, it is less than 100ms.
TiKV | server report failure message | There might be an issue with the network or the message might not come from this cluster. | If there are large amount of messages which contains `unreachable`, there might be an issue with the network. If the message contains `store not match`, the message does not come from this cluster.
TiKV  | Vote |the frequency of the Raft vote | Usually, the value only changes when there is a split. If the value of Vote remains high for a long time, the system might have a severe issue and some nodes are not working.
TiKV | 95% and 99% coprocessor request duration | the 95th percentile and the 99th percentile coprocessor request duration | Application specific. Usually, the value does not remain high.
TiKV | Pending task | the number of pending tasks | Except for PD worker, it is not normal if the value is too high.
TiKV | stall | RocksDB stall time | If the value is bigger than 0, it means that RocksDB is too busy, and you need to pay attention to IO and CPU usage.
TiKV | channel full | The channel is full and the threads are too busy. | If the value is bigger than 0, the threads are too busy.
TiKV |  95% send message duration seconds | the 95th percentile message sending time | less than 50ms
TiKV | leader/region | the number of leader/region per TiKV server| application specific