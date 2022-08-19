---
title: TiDB Monitoring FAQs
summary: Learn about the FAQs related to TiDB Monitoring.
---

# TiDB Monitoring FAQs

This document summarizes the FAQs related to TiDB monitoring.

- For details of Prometheus monitoring framework, see [Overview of the Monitoring Framework](/tidb-monitoring-framework.md).
- For details of key metrics of monitoring, see [Key Metrics](/grafana-overview-dashboard.md).

## Is there a better way of monitoring the key metrics?

The monitoring system of TiDB consists of Prometheus and Grafana. From the dashboard in Grafana, you can monitor various running metrics of TiDB which include the monitoring metrics of system resources, of client connection and SQL operation, of internal communication and Region scheduling. With these metrics, the database administrator can better understand the system running status, running bottlenecks and so on. In the practice of monitoring these metrics, we list the key metrics of each TiDB component. Generally you only need to pay attention to these common metrics. For details, see [official documentation](/grafana-overview-dashboard.md).

## The Prometheus monitoring data is deleted every 15 days by default. Could I set it to two months or delete the monitoring data manually?

Yes. Find the startup script on the machine where Prometheus is started, edit the startup parameter and restart Prometheus.

```config
--storage.tsdb.retention="60d"
```

## Region Health monitor

In TiDB 2.0, Region health is monitored in the PD metric monitoring page, in which the `Region Health` monitoring item shows the statistics of all the Region replica status. `miss` means shortage of replicas and `extra` means the extra replica exists. In addition, `Region Health` also shows the isolation level by `label`. `level-1` means the Region replicas are isolated physically in the first `label` level. All the Regions are in `level-0` when `location label` is not configured.

## What is the meaning of `selectsimplefull` in Statement Count monitor?

It means full table scan but the table might be a small system table.

## What is the difference between `QPS` and `Statement OPS` in the monitor?

The `QPS` statistics is about all the SQL statements, including `use database`, `load data`, `begin`, `commit`, `set`, `show`, `insert` and `select`.

The `Statement OPS` statistics is only about applications related SQL statements, including `select`, `update` and `insert`, therefore the `Statement OPS` statistics matches the applications better.
