---
title: Monitor a TiDB Cluster
summary: Learn how to monitor your TiDB cluster.
---

# Monitor a TiDB Cluster

This document describes how to monitor a TiDB cluster on TiDB Cloud.

## Cluster status and node status

You can see the current status of each running cluster on the cluster page.

### Cluster Status

| Cluster status | Description |
|:--|:--|
| **Normal** | Normal running (including data migration) |
| **Creating** | Creating the cluster |
| **Importing** | The cluster is importing data |
| **Scaling** | Scaling the TiDB, TiKV, or TiFlash nodes |
| **Upgrading** | Upgrading the TiDB version |
| **Unavailable** | The TiDB Cloud service is not available |
| **Unhealthy** | Part of nodes are unavailable, not enough replicas, and so on |
| **Recovering** | Backup recovery |

### TiDB node status

| TiDB node status | Description |
|:--|:--|
| **Normal** | Normal running |
| **Creating** | Creating the node |
| **Unavailable** | The TiDB node is not available |
| **Terminating** | The TiDB node is terminating |

### TiKV node status

| TiKV node status | Description |
|:--|:--|
| **Normal** | Normal running |
| **Creating** | Creating the node |
| **Unavailable** | The TiKV node is not available |
| **Terminating** | The TiKV node is terminating |
| **Leaving** | Migrating the current node data before termination |

## Monitoring metrics

In TiDB Cloud, you can view the commonly used metrics of a cluster from the following pages:

- Cluster overview page
- Cluster monitoring page

### Metrics on the cluster overview page

The cluster overview page provides general metrics of a cluster, including Total QPS, Latency, Connections, TiFlash Request QPS, TiFlash Request Duration, TiFlash Storage Size, TiKV Storage Size, TiDB CPU, TiKV CPU, TiKV IO Read, and TiKV IO Write.

To view metrics on the cluster overview page, take the following steps:

1. Navigate to the **Active Clusters** page.

2. Click the name of a cluster to go to its cluster overview page.

### Metrics on the cluster monitoring page

The cluster monitoring page provides a full set of standard metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

> **Note:**
>
> Currently, the cluster monitoring page is unavailable for [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier).

To view metrics on the cluster monitoring page, take the following steps:

1. Navigate to the **Diagnosis** tab of a cluster.

2. Click the **Monitoring** tab.

For more information, see [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md).

## Built-in alerting

TiDB Cloud has some built-in alerting conditions. You can configure TiDB Cloud to receive an email notification whenever a TiDB Cloud cluster in your project triggers a TiDB Cloud built-in alert condition.

For more information, see [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

## Third-party integrations

### Required access

To edit third-party integration settings, you must have the `Organization Owner` access to your organization or `Project Member` access to the target project.

### View or modify third-party integrations

1. On the TiDB Cloud console, choose a target project that you want to view or modify, and then click the **Project Settings** tab.
2. In the left pane, click **Integrations**. The available third-party integrations are displayed.

### Available integrations

| Third-party service  | Configuration details                                        |
| :------------------- | :----------------------------------------------------------- |
| **Datadog integration** | Configures TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). You can view these metrics in your Datadog dashboards. To get a detailed list of all metrics that Datadog tracks, refer to [Datadog Integration](/tidb-cloud/monitor-datadog-integration.md). |
| **Prometheus and Grafana integration** | Get a scrape_config file for Prometheus from TiDB Cloud and use the content from the file to configure Prometheus. You can view these metrics in your Grafana dashboards. To get a detailed list of all metrics that Prometheus tracks, refer to [Prometheus and Grafana Integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md). |
