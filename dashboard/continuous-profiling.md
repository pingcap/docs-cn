---
title: TiDB Dashboard Continuous Profiling
summary: Learn how to enable Continuous Profiling and observe system conditions by using this feature.
---

# TiDB Dashboard Instance Profiling - Continuous Profiling

> **Warning:**
>
> Continuous Profiling is currently an experimental feature and is not recommended for use in production environments.
>

Introduced in TiDB 5.3.0, Continuous Profiling is a way to observe resource overhead at the system call level. With the support of Continuous Profiling, TiDB provides performance insight as clear as directly looking into the database source code, and helps R&D and operation and maintenance personnel to locate the root cause of performance problems using a flame graph.

With less than 0.5% performance loss, this feature takes continuous snapshots (similar to CT scan) of the database internal operations, turning the database from a "black box" into a "white box" that is more observable. This feature runs automatically after being enabled by one click and keeps storage results generated within the retention period. Storage results beyond the retention period are recycled to release the storage space.

## Restrictions

Before enabling the Continuous Profiling feature, pay attention to the following restrictions:

- Under the x86 architecture, this feature supports TiDB, TiKV, and PD, but does not support TiFlash. This feature is not fully compatible with the ARM architecture and cannot be enabled under this architecture.

- Currently, this feature is only available for clusters deployed or upgraded using TiUP, and is unavailable for clusters deployed or upgraded by using TiDB Operator or binary packages.

## Profiling content

With Continuous Profiling, you can collect continuous performance data of TiDB, TiKV, and PD instances, and have the nodes monitored day and night without restarting any of them. The data collected can be displayed on a flame graph or a directed acyclic graph. The graph visually shows what internal operations are performed on the instances during the performance summary period and the corresponding proportions. With this graph, you can quickly learn the CPU resource consumption of these instances.

Currently, Continuous Profiling can display the following performance data:

- TiDB/PD: CPU profile, Heap, Mutex, Goroutine (debug=2)
- TiKV: CPU profile

## Enable Continuous Profiling

To enable Continuous Profiling, you need to first check the version information and then configure related settings on the control machine and TiDB Dashboard.

### Check versions

Before enabling this feature, check the version of the TiUP cluster and ensure that it is 1.7.0 or above. If it is earlier than 1.7.0, upgrade it first.

1. Check the TiUP version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster --version
    ```

    The command output shows the TiUP version, as shown below:

    ```shell
    tiup version 1.7.0 tiup
    Go Version: go1.17.2
    Git Ref: v1.7.0
    ```

    - If `tiup version` is earlier than 1.7.0, upgrade the TiUP cluster by referring to the next step.
    - If `tiup version` is 1.7.0 or above, you can directly reload Prometheus.

2. Upgrade TiUP and TiUP cluster to the latest version.

    - Upgrade TiUP:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup update --self
        ```

    - Upgrade the TiUP cluster:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup update cluster
        ```

After TiUP and the TiUP cluster are upgraded to the latest version, version check is completed.

### Configure the control machine and TiDB Dashboard

1. On the control machine, add the `ng_port` configuration item by using TiUP.

    1. Open the configuration file of the cluster in the editing mode:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster edit-config ${cluster-name}
        ```

    2. Set parameters: add `ng_port:${port}` under [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers).

        ```shell
        monitoring_servers:
        - host: 172.16.6.6
          ng_port: ${port}
        ```

    3. Reload Prometheus:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster reload ${cluster-name} --role prometheus
        ```

    After reloading Prometheus, you have finished operations on the control machine.

2. Enable the Continuous Profiling feature.

    1. On TiDB Dashboard, click **Advanced Debugging** > **Profile Instances** > **Continuous Profile**.

    2. In the displayed window, switch on the button under **Enable Feature** on the right. Modify the value of **Retention Duration** as required or retain the default value.

    3. Click **Save** to enable this feature.

    ![Enable the feature](/media/dashboard/dashboard-conprof-start.png)

## Access the page

You can access the instance profiling page using either of the following methods:

- After logging into TiDB Dashboard, click **Advanced Debugging** > **Profile Instances** > **Continuous Profile** on the left navigation bar.

    ![Access](/media/dashboard/dashboard-conprof-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/continuous_profiling> via your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## View profiling history

After starting continuous profiling, you can view the profiling result on the instance profiling page.

![Profiling history](/media/dashboard/dashboard-conprof-history.png)

Performance profiling runs in the background. Refreshing or exiting the current page will not terminate a running performance profiling task.

## Download profiling result

On the profiling result page, you can click **Download Profiling Result** in the upper-right corner to download all profiling results.

![Download profiling result](/media/dashboard/dashboard-conprof-download.png)

You can also click an individual instance to view its profiling result:

![View the profiling result of an instance](/media/dashboard/dashboard-conprof-single.png)

## Disable Continuous Profiling

1. On TiDB Dashboard, click **Advanced Debugging** > **Profile Instances** > **Continuous Profile** on the left navigation bar. Click **Settings**.

2. In the popped-up window, switch off the button under **Enable Feature**.

3. In the dialog box of **Disable Continuous Profiling Feature**, click **Disable**.

4. Click **Save**.

    ![Disable the feature](/media/dashboard/dashboard-conprof-stop.png)