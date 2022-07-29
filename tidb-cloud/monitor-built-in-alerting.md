---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDB Cloud Built-in Alerting

The TiDB Cloud built-in alerting feature provides you with an easy way to be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

This document describes how to subscribe to alert notification emails from TiDB Cloud and also provides the TiDB Cloud built-in alert conditions for your reference.

## Limitation

You cannot customize the TiDB Cloud built-in alerting. If you would like to configure different trigger conditions, thresholds, or frequency, or have alerts automatically trigger actions in downstream services like [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/), consider using a third-party monitoring and alerting integration. Currently, TiDB Cloud supports the [Datadog integration](/tidb-cloud/monitor-datadog-integration.md) and the [Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## Subscribe to alert notification emails

If you are a member of a project and you want to get alert notification emails of clusters in your project, take the following steps:

1. Log into TiDB Cloud console.
2. On the TiDB Cloud console, choose a target project on which you want to receive alert notification emails, and then click the **Project Settings** tab.
3. In the left pane, click **Alerts**.
4. Enter your email address, and then click **Subscribe**.

To minimize the number of alert emails sent to subscribers, TiDB Cloud aggregates alerts into a single email that is sent every 3 hours.

## Unsubscribe from alert notification emails

If you no longer want to receive alert notification emails of clusters in your project, take the following steps:

1. Log into TiDB Cloud console.
2. On the TiDB Cloud console, choose the project on which you no longer want to receive alert notification emails.
3. In the left pane, click **Alerts**.
4. In the right pane, locate your email address and click **Delete**.

## TiDB Cloud built-in alert conditions

The following table provides the TiDB Cloud built-in alert conditions and the corresponding recommended actions.

> **Note:**
>
> Although these alert conditions do not necessarily mean there is a problem, they are often early warning indicators of emerging issues. Thus, taking the recommended action is advised.

| Condition | Recommended Action |
|:--- |:--- |
| Total TiDB node memory utilization across cluster exceeded 70% for 10 minutes | Total TiDB node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiDB nodes. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiKV node memory utilization across cluster exceeded 70% for 10 minutes | Total TiKV node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiKV nodes. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiFlash node memory utilization across cluster exceeded 70% for 10 minutes | Total TiFlash node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiFlash nodes. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
|`*` At least one TiDB node in the cluster has run out of memory | At least one TiDB node in cluster ABC in project XYZ ran out of memory while executing a SQL statement. Consider increasing the memory available to queries using the `tidb_mem_quota_query` session variable. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiDB node CPU utilization exceeded 80% for 10 minutes | Total TiDB node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiDB nodes. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiKV node CPU utilization exceeded 80% for 10 minutes | Total TiKV node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiKV nodes. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiFlash node CPU utilization exceeded 80% for 10 minutes | Total TiFlash node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. If you expect this to continue, it is recommended that you add additional TiFlash nodes. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
|`*`  TiKV storage utilization exceeds 80% | Total TiKV storage utilization of cluster ABC in project XYZ exceeds 80%. It is recommended that you add additional TiKV nodes to increase your storage capacity. To monitor storage utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
|`*`  TiFlash storage utilization exceeds 80% | Total TiFlash storage utilization of cluster ABC in project XYZ exceeds 80%. It is recommended that you add additional TiFlash nodes to increase your storage capacity. To monitor storage utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Cluster nodes are offline | Some or all nodes in cluster ABC in project XYZ  are offline. The TiDB Cloud Operations team is aware and working to resolve the issue. Refer to [TiDB Cloud Status](https://status.tidbcloud.com/) for the latest information. To monitor node status, see [Cluster status and node status](/tidb-cloud/monitor-tidb-cluster.md#cluster-status-and-node-status).  |

> **Note:**
>
> - [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier) only support a subset of alert conditions that are marked with `*` in the **Condition** column.
> - "cluster ABC" and "project XYZ" in the **Recommended Action** column are example names for reference.