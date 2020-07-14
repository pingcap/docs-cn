---
title: Instance Profiling Page
summary: Learn the instance profiling page of TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-profiling/']
---

# Instance Profiling Page

The instance profiling page summarizes the internal performance data of each TiDB instance, TiKV instance, and PD instance. With this page, you can view the instance profiling without restarting these instances.

The summarized performance data can be displayed as a flame graph or a directed acyclic graph, which visually shows the internal operations and proportions performed on the instances during the performance summary period. With this graph, you can quickly learn the main CPU resource consumption of these instances.

## Access the page

You can access the instance profiling page using one of the following methods:

- After logging into TiDB Dashboard, click **Advanced Debugging** → **Profile Instances** on the left navigation bar.

  ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/instance_profiling> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Start Profiling

In the instance profiling page, choose at least one target instance and click **Start Profiling** to start the instance profiling.

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

You can modify the profiling duration before starting the profiling. This duration is determined by the time needed for the profiling, which is 30 seconds by default. The 30-second duration takes approximately 30 seconds to complete.

## View profiling status

After a profiling is started, you can view the profiling status and progress in real time.

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

The profiling runs in the background. Refreshing or exiting the current page does not stop the profiling task that is running.

## Download profiling result

After the profiling of all instances is completed, you can click **Download Profiling Result** in the upper right corner to download all profiling results.

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

You can also click a single instance on the list to directly view its profiling result.

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## View profiling history

The profiling history is listed on the instance profiling page. Click one row of the list and you can view the status detail.

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

For detailed operations on the profiling status page, see [View profiling status](#view-profiling-status).
