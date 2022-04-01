---
title: Use WebUI to Manage DM migration tasks
summary: Learn how to use WebUI to manage DM migration tasks.
---

# Use WebUI to Manage DM migration tasks

DM WebUI is a web-based GUI platform for managing TiDB Data Migration (DM) tasks. This platform provides a simple and intuitive way to manage a large number of migration tasks, which frees you from using the dmctl command-line tool.

This document introduces how to access DM WebUI, the prerequisites, the use cases of each page on the interface, and the attention points.

> **Warning:**
>
> - DM WebUI is currently an experimental feature. It is not recommended to use it in the production environment.
> - The lifecycle of `task` in DM WebUI has been changed, and it is not recommended to use DM WebUI and dmctl at the same time.

DM WebUI has the following pages:

- **Dashboard**: Displays the main monitoring information and status information of migration tasks in DM to help you quickly learn the overall running status of migration tasks and the key metrics on latency and performance.
- **Migration**
    - **Task**: Provides an entry to task creation, and displays the detailed information of each migration task. This page helps you monitor, create, delete, and configure migration tasks.
    - **Source**: Configures the information of upstream data source for a migration task. On this page, you can manage the upstream configuration in a data migration environment, including creating and deleting upstream configuration, monitoring the task status corresponding to the upstream configuration, and modifying upstream configuration.
    - **Replication Detail**: Displays the detailed status information of migration tasks. On this page, you can view the detailed configuration and status information based on a specified filter, including the configuration information and database names of the upstream and downstream, the relation of source tables and target tables.
- **Cluster**
    - **Members**: Displays the list of all master and worker nodes in the DM cluster, and the binding relationship between worker nodes and the source. On this page, you can view the configuration information of the current DM cluster and the status information of each worker. In addition, basic management is also provided on this page.

The interface is as follows:

![webui](/media/dm/dm-webui-preview-en.png)

## Access method

You can access DM WebUI from any master node of the DM cluster. The access port is `8261` by default and is the same as that of DM OpenAPI. Here is an example of an access address: `http://{master_ip}:{master_port}/dashboard/`.

## Prerequisites

To ensure that DM WebUI can display information properly, before using DM WebUI, make sure that the following operations or configuration have been completed:

+ Enable the DM OpenAPI configuration:

    - If your DM cluster has been deployed using binary, enable the `openapi` configuration item in the configuration of the master node:

        ```
        openapi = true
        ```

    - If your DM cluster has been deployed using TiUP, add the following configuration to the topology file:

        ```yaml
        server_configs:
          master:
            openapi: true
        ```

+ When deploying Grafana for the first time, make sure that the `monitoring_servers` and `grafana_servers` components have been correctly installed. You can expected to configure `grafana_servers` as follows:

    ```
    grafana_servers:
      - host: 10.0.1.14
        # port: 3000
        # deploy_dir: /tidb-deploy/grafana-3000
        config:       # Make sure that the TiUP version for tiup dm -v is later than v1.9.0.
          auth.anonymous.enabled: true
          security.allow_embedding: true
    ```

    If the IP and port of `grafana_servers` are not the default ones, you need to fill in the correct IP and port on the **Dashboard** page.

+ If your DM cluster is upgraded from an earlier version, you need to manually modify the Grafana configuration:

    1. Edit the `/{deploy-dir}/grafana-{port}/conf/grafana.ini` file as follows to modify two configuration items:

        ```ini
        [auth.anonymous]
        enabled = true

        [security]
        allow_embedding = true
        ```

    2. Run `tiup dm reload` to make the new configuration effective.

## Dashboard

To see the monitoring of migration tasks, visit the **Dashboard** page. **Dashboard** is an embedded Grafana Dashboard that contains `Standard` and `Professional` views, each of which displays monitoring information from a standard perspective, or from a relatively professional perspective.

## Migration

**Migration** includes **Source**, **Task**, and **Replication Detail** pages.

## Source

Before creating a migration task, you need to create the data source information of the upstream for the replication task. You can create the upstream configuration in the **Source** page. When creating sources, pay attention to the following items:

- If there is a auto failover between primary and secondary instance, enable GTID in the upstream MySQL and set GTID to `True` when creating the upstream configuration; otherwise, the migration task will be interrupted during the failover (except for AWS Aurora).
- If a MySQL instance needs to be temporarily offline, you can disable the instance. However, when the MySQL instance is being disabled, other MySQL instances running migration tasks should not execute DDL operations; otherwise, the disabled instance cannot properly migrate data after it is enabled.
- When multiple migration tasks use the same upstream, it might cause additional stress. Enabling relay log can reduce the impact on the upstream, so it is recommended to enable relay log.

### Task

You can view the migration task details on the **Task** page, and create migration tasks.

#### View migration task details

In the task list, click the task name to view the Details page from the right. The Details page displays more detailed task status information. On this page, you can view the status of each sub-task and the current configuration information of the migration task.

In DM, each sub-task of a migration task might be at different stages, namely full dump -> full import (load) -> incremental replication (sync). Therefore, the current stage of a task is displayed with the statistics of the sub-task statuses, which can help you better understand the running status of the task.

#### Create migration tasks

To create a migration task on this page, click the **Add** button on the top right corner. You can use one of the following methods to create a migration task:

- By following the WebUI instruction. Fill in the required information step by step on the WebUI. This method is suitable for beginners and for daily use.
- By using a configuration file. Paste or write a JSON-formatted configuration file to create a migration task. This method supports adjusting more parameters and is suitable for advanced users.

## Replication detail

You can view the status of the migration rules configured for a migration task on the **Replication Detail** page. This page supports querying by task, source, and database name.

The query result contains the corresponding information of the upstream table and the downstream table, so be careful using `.*` in case that too many query results slow down the page response.

## Cluster

### Members

The **Members** page displays all the master and worker nodes in the DM cluster, and the binding relationship between worker nodes and the source. 
