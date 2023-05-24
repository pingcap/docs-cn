---
title: TiDB Dashboard Instance Profiling - Manual Profiling
summary: Learn how to collect performance data to analyze sophisticated problems.
aliases: ['/docs/dev/dashboard/dashboard-profiling/']
---

# TiDB Dashboard Instance Profiling - Manual Profiling

> **Note:**
>
> This feature is designed for database experts. For non-expert users, it is recommended to use this feature under the guidance of PingCAP technical supports.

Manual Profiling allows users to collect current performance data **on demand** for each TiDB, TiKV, PD and TiFlash instances with a single click. The collected performance data can be visualized as FlameGraph or DAG.

With these performance data, experts can analyze current resource consumption details like instance's CPU and memory, to help pinpoint sophisticated ongoing performance problems, such as high CPU overhead, high memory usage, and process stalls.

After initiates the profiling, TiDB Dashboard collects current performance data for a period of time (30 seconds by default). Therefore this feature can only be used to analyze ongoing problems that the cluster is facing now and has no significant effect on historical problems. If you want to collect and analyze performance data **at any time**, see [Continuous Profiling](/dashboard/continuous-profiling.md).

## Supported performance data

The following performance data are currently supported:

- CPU: The CPU overhead of each internal function on TiDB, TiKV, PD and TiFlash instances

  > The CPU overhead of TiKV and TiFlash instances is currently not supported in ARM architecture.

- Heap: The memory consumption of each internal function on TiDB and PD instances

- Mutex: The mutex contention states on TiDB and PD instances

- Goroutine: The running state and call stack of all goroutines on TiDB and PD instances

## Access the page

You can access the instance profiling page using either of the following methods:

* After logging in to TiDB Dashboard, click **Advanced Debugging** > **Profiling Instances** > **Manual Profiling** in the left navigation menu.

  ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

* Visit <http://127.0.0.1:2379/dashboard/#/instance_profiling> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Start Profiling

In the instance profiling page, choose at least one target instance and click **Start Profiling** to start the instance profiling.

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

You can modify the profiling duration before starting the profiling. This duration is determined by the time needed for the profiling, which is 30 seconds by default. The 30-second duration takes 30 seconds to complete.

Manual Profiling cannot be initiated on clusters that have [Continuous Profiling](/dashboard/continuous-profiling.md) enabled. To view the performance data at the current moment, click on the most recent profiling result in the [Continuous Profiling page](/dashboard/continuous-profiling.md#access-the-page).

## View profiling status

After a profiling is started, you can view the profiling status and progress in real time.

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

The profiling runs in the background. Refreshing or exiting the current page does not stop the profiling task that is running.

## Download performance data

After the profiling of all instances is completed, you can click **Download Profiling Result** in the upper right corner to download all performance data.

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

You can also click an individual instance in the table to view its profiling result. Alternatively, you can hover on ... to download raw data.

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## View profiling history

The on-demand profiling history is listed on the page. Click a row to view details.

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

For detailed operations on the profiling status page, see [View Profiling Status](#view-profiling-status).
