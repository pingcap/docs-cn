---
title: Third-Party Monitoring Integrations
summary: Learn how to use third-party monitoring integrations.
---

# Third-Party Monitoring Integrations

You can integrate TiDB Cloud with third-party monitoring services to receive TiDB Cloud alerts and view the performance metrics of your TiDB cluster using the monitoring services.

> **Note:**
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), third-party monitoring integrations are not supported.

## Required access

To edit third-party integration settings, you must have the `Owner` access to your organization or `Member` access to the target project.

## View or modify third-party integrations

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. In the left navigation pane of the [**Clusters**](https://tidbcloud.com/console/clusters) page, do one of the following:

    - If you have multiple projects, switch to the target project, and then click **Admin** > **Integrations**.
    - If you only have one project, click **Admin** > **Integrations**.

The available third-party integrations are displayed.

## Available integrations

### Datadog integration

With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/) and view these metrics in your Datadog dashboards.

For the detailed integration steps and a list of metrics that Datadog tracks, refer to [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md).

### Prometheus and Grafana integration

With the Prometheus and Grafana integration, you can get a scrape_config file for Prometheus from TiDB Cloud and use the content from the file to configure Prometheus. You can view these metrics in your Grafana dashboards.

For the detailed integration steps and a list of metrics that Prometheus tracks, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).
