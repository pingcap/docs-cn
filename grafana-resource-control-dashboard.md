---
title: Key Monitoring Metrics of Resource Control
summary: Learn some key metrics displayed on the Grafana Resource Control dashboard.
---

# Key Monitoring Metrics of Resource Control

If you use TiUP to deploy the TiDB cluster, the monitoring system (Prometheus & Grafana) is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and Performance\_overview.

If your cluster has used the [Resource Control](/tidb-resource-control.md) feature, you can get an overview of the resource consumption status from the Resource Control dashboard. 

This document describes some key monitoring metrics displayed on the Resource Control dashboard.

## Metrics about Request Unit

- RU: the [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) consumption information of each resource group, calculated in real time. `total` is the sum of the Request Units consumed by all Resource Groups. The Request Unit consumption of each resource group should be equal to the sum of its read consumption (Read Request Unit) and write consumption (Write Request Unit).
- RU Per Query: the average number of Request Units consumed by each SQL statement per second. It is obtained by dividing the above RU metric by the number of SQL statements executed per second.
- RRU: the Read Request Unit consumption information of each resource group, calculated in real time. `total` is the sum of the Read Request Units consumed by all Resource Groups.
- RRU Per Query: the average number of Read Request Units consumed by each SQL statement per second. It is obtained by dividing the above RRU metric by the number of SQL statements executed per second.
- WRU: the Write Request Unit consumption information of each resource group, calculated in real time. `total` is the sum of the Write Request Units consumed by all Resource Groups.
- WRU Per Query: the average number of Write Request Units consumed by each SQL statement per second. It is obtained by dividing the above WRU metric by the number of SQL statements executed per second.

## Metrics about resources

- KV Request Count: the number of KV requests for each resource group, calculated per second. The requests are divided into read and write types. `total` is the sum of the KV requests for all Resource Groups.
- KV Request Count Per Query: the average number of read and write KV requests by each SQL statement per second. It is obtained by dividing the above KV Request Count metric by the number of SQL statements executed per second.
- Bytes Read: the amount of data read by each Resource Group, calculated per second. `total` is the sum of the data read by all Resource Groups.
- Bytes Read Per Query: the average amount of data read by each SQL statement per second. It is obtained by dividing the above Bytes Read metric by the number of SQL statements executed per second.
- Bytes Written: the amount of data written by each Resource Group, calculated in real time. `total` is the sum of the data written by all Resource Groups.
- Bytes Written Per Query: the average amount of data written by each SQL statement per second. It is obtained by dividing the above Bytes Written metric by the number of SQL statements executed per second.
- KV CPU Time: the KV layer CPU time consumed by each Resource Group, calculated in real time . `total` is the sum of the KV layer CPU time consumed by all Resource Groups.
- KV CPU Time Per Query: the average KV layer CPU time consumed by each SQL statement per second. It is obtained by dividing the above KV CPU Time metric by the number of SQL statements executed per second.
- SQL CPU Time: the SQL layer CPU time consumed by each Resource Group, calculated in real time. `total` is the sum of the SQL layer CPU time consumed by all Resource Groups.
- SQL CPU Time Per Query: the average SQL layer CPU time consumed by each SQL statement per second. It is obtained by dividing the above SQL CPU Time metric by the number of SQL statements executed per second.
