---
title: TiDB Dashboard 实例性能分析页面
---

# TiDB Dashboard 实例性能分析页面

该功能允许用户对各个 TiDB、TiKV、PD 实例在不重启的情况下进行内部性能数据收集。收集到的性能数据可显示为火焰图或有向无环图，直观展现实例在性能收集的时间段内执行的各种内部操作及比例，快速了解该实例 CPU 资源消耗的主要内容。

## 访问

可以通过以下两种方法访问实例性能分析页面：

- 登录后，左侧导航条点击 **高级调试** → **实例性能分析**：

  ![访问](/media/dashboard/dashboard-profiling-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/instance_profiling>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 开始性能分析

在实例性能分析页面，选择至少一个想要分析的目标实例，点击**开始分析**（Start Profiling）按钮即可开始性能分析：

![界面](/media/dashboard/dashboard-profiling-start.png)

在开始性能分析前可以修改性能分析时长。性能分析所需时间取决于分析时长，默认为 30 秒。30 秒的性能分析大约需要 30 秒完成。

## 查看性能分析状态

开始性能分析后，可以看到实时性能分析状态和进度：

![界面](/media/dashboard/dashboard-profiling-view-progress.png)

性能分析会在后台运行，刷新或退出当前页面不会终止已经运行的性能分析任务。

## 下载性能分析结果

所有实例的性能分析都完成后，可点击右上角下载按钮（Download Profiling Result）打包下载所有性能分析结果：

![界面](/media/dashboard/dashboard-profiling-download.png)

也可以点击列表中的单个实例，直接查看其性能分析结果：

![界面](/media/dashboard/dashboard-profiling-view-single.png)

## 查看性能分析历史

在性能分析页面下方，列出了性能分析历史。点击任意一行，即可查看其状态详情：

![界面](/media/dashboard/dashboard-profiling-history.png)

关于状态详情页的操作，参见[查看性能分析状态](#查看性能分析状态)章节。
