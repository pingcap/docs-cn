---
title: TiDB Dashboard FAQ
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-faq/']
---

# TiDB Dashboard FAQ

This document summarizes the frequently asked questions (FAQs) and answers about TiDB Dashboard.

## Access-related FAQ

### When the firewall or reverse proxy is configured, I am redirected to an internal address other than TiDB Dashboard

When multiple Placement Driver (PD) instances are deployed in a cluster, only one of the PD instances actually runs the TiDB Dashboard service. If you access other PD instances instead of this one, your browser redirects you to another address. If the firewall or reverse proxy is not properly configured for accessing TiDB Dashboard, when you visit the Dashboard, you might be redirected to an internal address that is protected by the firewall or reverse proxy.

- See [TiDB Dashboard Multi-PD Instance Deployment](/dashboard/dashboard-ops-deploy.md) to learn the working principle of TiDB Dashboard with multiple PD instances.
- See [Use TiDB Dashboard through a Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md) to learn how to correctly configure a reverse proxy.
- See [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md) to learn how to correctly configure the firewall.

### When TiDB Dashboard is deployed with dual network interface cards (NICs), TiDB Dashboard cannot be accessed using another NIC

For security reasons, TiDB Dashboard on PD only monitors the IP addresses specified during deployment (that is, it only listens on one NIC), not on `0.0.0.0`. Therefore, when multiple NICs are installed on the host, you cannot access TiDB Dashboard using another NIC.

If you have deployed TiDB using the `tiup cluster` or `tiup playground` command, currently this problem cannot be solved. It is recommended that you use a reverse proxy to safely expose TiDB Dashboard to another NIC. For details, see [Use TiDB Dashboard behind a Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md).

## UI-related FAQ

### A `prometheus_not_found` error is shown in **QPS** and **Latency** sections on the Overview page

The **QPS** and **Latency** sections on the **Overview** page require a cluster with Prometheus deployed. Otherwise, the error is shown. You can solve this problem by deploying a Prometheus instance in the cluster.

If you still encounter this problem when the Prometheus instance has been deployed, the possible reason is that your deployment tool is out of date (TiUP, TiDB Operator, or TiDB Ansible), and your tool does not automatically report metrics addresses, which makes TiDB Dashboard unable to query metrics. You can upgrade you deployment tool to the latest version and try again.

If your deployment tool is TiUP, take the following steps to solve this problem. For other deployment tools, refer to the corresponding documents of those tools.

1. Upgrade TiUP and TiUP Cluster:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2. After the upgrade, when a new cluster is deployed with Prometheus instances, the metrics can be displayed normally.

3. After the upgrade, for an existing cluster, you can restart this cluster to report the metrics addresses. Replace `CLUSTER_NAME` with the actual cluster name:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

   Even if the cluster has been started, still execute this command. This command does not affect the normal application in the cluster, but refreshes and reports the metrics addresses, so that the monitoring metrics can be displayed normally in TiDB Dashboard.

### An `invalid connection` error is shown in **Top SQL Statements** and **Recent Slow Queries** on the Overview page

The possible reason is that you have enabled the `prepared-plan-cache` feature of TiDB. As an experimental feature, when enabled, `prepared-plan-cache` might not function properly in specific TiDB versions, which could cause this problem in TiDB Dashboard (and other applications). You can disable `prepared-plan-cache` by updating [TiDB Configuration file](/tidb-configuration-file.md#prepared-plan-cache) to solve this problem.
