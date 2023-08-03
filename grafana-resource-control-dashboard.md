---
title: Key Monitoring Metrics of Resource Control
summary: Learn some key metrics displayed on the Grafana Resource Control dashboard.
---

# Key Monitoring Metrics of Resource Control

If you use TiUP to deploy the TiDB cluster, the monitoring system (Prometheus & Grafana) is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and Performance\_overview.

If your cluster has used the [Resource Control](/tidb-resource-control.md) feature, you can get an overview of the resource consumption status from the Resource Control dashboard.

TiDB uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket) for flow control. As described in the [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md#distributed-token-buckets), a TiDB node might have multiple Resource Groups, which are flow controlled by GAC (Global Admission Control) on the PD side. The Local Token Buckets in each TiDB node periodically (5 seconds by default) communicate with the GAC on the PD side to reconfigure the local tokens. In TiDB, the Local Token Buckets are implemented as Resource Controller Clients.

This document describes some key monitoring metrics displayed on the Resource Control dashboard.

## Metrics about Request Unit

- RU: the [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) consumption information of each resource group, calculated in real time. `total` is the sum of the Request Units consumed by all Resource Groups. The Request Unit consumption of each resource group should be equal to the sum of its read consumption (Read Request Unit) and write consumption (Write Request Unit).
- RU Per Query: the average number of Request Units consumed by each SQL statement per second. It is obtained by dividing the above RU metric by the number of SQL statements executed per second.
- RRU: the Read Request Unit consumption information of each resource group, calculated in real time. `total` is the sum of the Read Request Units consumed by all Resource Groups.
- RRU Per Query: the average number of Read Request Units consumed by each SQL statement per second. It is obtained by dividing the above RRU metric by the number of SQL statements executed per second.
- WRU: the Write Request Unit consumption information of each resource group, calculated in real time. `total` is the sum of the Write Request Units consumed by all Resource Groups.
- WRU Per Query: the average number of Write Request Units consumed by each SQL statement per second. It is obtained by dividing the above WRU metric by the number of SQL statements executed per second.
- Available RU: the available tokens in the RU token bucket of each resource group. When it is `0`, this resource group consumes tokens at the rate of `RU_PER_SEC` and can be considered to be in a rate-limited state.
- Query Max Duration: the maximum Query Duration in terms of resource groups.

## Metrics about resources

- KV Request Count: the number of KV requests for each resource group, calculated per second. The requests are divided into read and write types. `total` is the sum of the KV requests for all Resource Groups.
- KV Request Count Per Query: the average number of read and write KV requests by each SQL statement per second. It is obtained by dividing the above KV Request Count metric by the number of SQL statements executed per second.
- Bytes Read: the amount of data read by each Resource Group, calculated per second. `total` is the sum of the data read by all Resource Groups.
- Bytes Read Per Query: the average amount of data read by each SQL statement per second. It is obtained by dividing the above Bytes Read metric by the number of SQL statements executed per second.
- Bytes Written: the amount of data written by each Resource Group, calculated in real time. `total` is the sum of the data written by all Resource Groups.
- Bytes Written Per Query: the average amount of data written by each SQL statement per second. It is obtained by dividing the above Bytes Written metric by the number of SQL statements executed per second.
- KV CPU Time: the KV layer CPU time consumed by each Resource Group, calculated in real time. `total` is the sum of the KV layer CPU time consumed by all Resource Groups.
- SQL CPU Time: the SQL layer CPU time consumed by each Resource Group, calculated in real time. `total` is the sum of the SQL layer CPU time consumed by all Resource Groups.

## Metrics about Resource Controller Client

- Active Resource Groups: the number of resource groups for each Resource Controller Client, calculated in real time.
- Total KV Request Count: the number of KV requests for each Resource Controller Client, calculated in real time and by resource groups. `total` is the sum of the KV requests for all Resource Controller Clients.
- Failed KV Request Count: the number of failed KV requests for each Resource Controller Client, calculated in real time and by resource groups. `total` is the sum of the failed KV requests for all Resource Controller Clients.
- Successful KV Request Count: the number of successful KV requests for each Resource Controller Client, calculated in real time and by resource groups. `total` is the sum of the successful KV requests for all Resource Controller Clients.
- Successful KV Request Wait Duration (99/90): the waiting time (at different percentiles) for successful KV requests for each Resource Controller Client, calculated in real time and by resource groups.
- Token Request Handle Duration (999/99): the waiting time (at different percentiles) for token requests from the server side for each Resource Controller Client, calculated in real time and by resource groups.
- Token Request Count: the number of token requests from the server side for each Resource Controller Client, calculated in real time and by resource groups. `successful` and `failed` are the sums of the successful and failed token requests for all Resource Controller Clients.
