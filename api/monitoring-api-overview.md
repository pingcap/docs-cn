---
title: TiDB Monitoring API Overview
summary: Learn the API of TiDB monitoring services.
---

# TiDB Monitoring API Overview

The TiDB monitoring framework uses two open-source projects: [Prometheus](https://prometheus.io) and [Grafana](https://grafana.com/grafana). TiDB uses Prometheus to store monitoring and performance metrics and Grafana to visualize these metrics. TiDB also provides the built-in [TiDB Dashboard](/dashboard/dashboard-intro.md) for monitoring and diagnosing TiDB clusters.

You can use the following interfaces to monitor TiDB cluster status:

- [Status interface](/tidb-monitoring-api.md#use-the-status-interface): monitor the [running status](/tidb-monitoring-api.md#running-status) of the current TiDB server and the [storage information](/tidb-monitoring-api.md#storage-information) of a table.
- [Metrics interface](/tidb-monitoring-api.md#use-the-metrics-interface): get detailed information about various operations in components and view these metrics using Grafana.

For more information about each API, including request parameters, response examples, and usage instructions, see [TiDB Monitoring API](/tidb-monitoring-api.md).
