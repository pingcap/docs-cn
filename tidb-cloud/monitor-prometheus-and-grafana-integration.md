---
title: Integrate TiDB Cloud with Prometheus and Grafana (Beta)
summary: Learn how to monitor your TiDB cluster with the Prometheus and Grafana integration.
---

# Integrate TiDB Cloud with Prometheus and Grafana (Beta)

TiDB Cloud provides a [Prometheus](https://prometheus.io/) API endpoint (beta). If you have a Prometheus service, you can monitor key metrics of TiDB Cloud from the endpoint easily.

This document describes how to configure your Prometheus service to read key metrics from the TiDB Cloud endpoint and how to view the metrics using [Grafana](https://grafana.com/).

## Prerequisites

- To integrate TiDB Cloud with Prometheus, you must have a self-hosted or managed Prometheus service.

- To edit third-party integration settings of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Member` access to the target project in TiDB Cloud.

## Limitation

- You cannot use the Prometheus and Grafana integration in [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

- Prometheus and Grafana integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Steps

### Step 1. Get a scrape_config file for Prometheus

Before configuring your Prometheus service to read metrics of TiDB Cloud, you need to generate a scrape_config YAML file in TiDB Cloud first. The scrape_config file contains a unique bearer token that allows the Prometheus service to monitor any database clusters in the current project.

To get the scrape_config file for Prometheus, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Integrations** in the left navigation pane, and then click **Integration to Prometheus (BETA)**.
4. Click **Add File** to generate and show the scrape_config file for the current project.

5. Make a copy of the scrape_config file content for later use.

    > **Note:**
    >
    > For security reasons, TiDB Cloud only shows a newly generated scrape_config file once. Ensure that you copy the content before closing the file window. If you forget to do so, you need to delete the scrape_config file in TiDB Cloud and generate a new one. To delete a scrape_config file, select the file, click **...**, and then click **Delete**.

### Step 2. Integrate with Prometheus

1. In the monitoring directory specified by your Prometheus service, locate the Prometheus configuration file.

    For example, `/etc/prometheus/prometheus.yml`.

2. In the Prometheus configuration file, locate the `scrape_configs` section, and then copy the scrape_config file content obtained from TiDB Cloud to the section.

3. In your Prometheus service, check **Status** > **Targets** to confirm that the new scrape_config file has been read. If not, you might need to restart the Prometheus service.

### Step 3. Use Grafana GUI dashboards to visualize the metrics

After your Prometheus service is reading metrics from TiDB Cloud, you can use Grafana GUI dashboards to visualize the metrics as follows:

1. Download the Grafana dashboard JSON of TiDB Cloud [here](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json).
2. [Import this JSON to your own Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) to visualize the metrics.
3. (Optional) Customize the dashboard as needed by adding or removing panels, changing data sources, and modifying display options.

For more information about how to use Grafana, see [Grafana documentation](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/).

## Best practice of rotating scrape_config

To improve data security, it is a general best practice to periodically rotate scrape_config file bearer tokens.

1. Follow [Step 1](#step-1-get-a-scrape_config-file-for-prometheus) to create a new scrape_config file for Prometheus.
2. Add the content of the new file to your Prometheus configuration file.
3. Once you have confirmed that your Prometheus service is still able to read from TiDB Cloud, remove the content of the old scrape_config file from your Prometheus configuration file.
4. On the **Integration** page of your project, delete the corresponding old scrape_config file to block anyone else from using it to read from the TiDB Cloud Prometheus endpoint.

## Metrics available to Prometheus

Prometheus tracks the following metric data for your TiDB clusters.

| Metric name |  Metric type  | Labels | Description |
|:--- |:--- |:--- |:--- |
| tidbcloud_db_queries_total| count | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The total number of statements executed |
| tidbcloud_db_failed_queries_total | count | type: `planner:xxx\|executor:2345\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The total number of execution errors |
| tidbcloud_db_connections | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | Current number of connections in your TiDB server |
| tidbcloud_db_query_duration_seconds | histogram | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The duration histogram of statements |
| tidbcloud_changefeed_latency | gauge | changefeed_id | The data replication latency between the upstream and the downstream of a changefeed |
| tidbcloud_changefeed_replica_rows | gauge | changefeed_id | The number of replicated rows that a changefeed writes to the downstream per second |
| tidbcloud_node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | The disk usage bytes of TiKV/TiFlash nodes |
| tidbcloud_node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | The disk capacity bytes of TiKV/TiFlash nodes |
| tidbcloud_node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The CPU usage of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The CPU limit cores of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The used memory bytes of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The memory capacity bytes of TiDB/TiKV/TiFlash nodes |

## FAQ

- Why does the same metric have different values on Grafana and the TiDB Cloud console at the same time?

    The aggregation calculation logic is different between Grafana and TiDB Cloud, so the displayed aggregated values might differ. You can adjust the `mini step` configuration in Grafana to get more fine-grained metric values.
