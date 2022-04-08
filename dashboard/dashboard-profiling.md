---
title: TiDB Dashboard 实例性能分析 - 手动分析页面
summary: 了解如何收集集群各个实例当前性能数据，从而分析复杂问题
aliases: ['/docs-cn/dev/dashboard/dashboard-profiling/']
---

# TiDB Dashboard 实例性能分析 - 手动分析页面

> **注意：**
>
> 该功能面向技术专家，建议在 PingCAP 专业技术人员的指导下使用该功能。

该页面允许用户**按需地**一键收集 TiDB、TiKV、PD、TiFlash 各个实例的当前性能数据。收集到的性能数据可显示为火焰图或有向无环图形式。

通过这些性能数据，技术专家可以分析实例当前的 CPU、内存等资源消耗细节，帮助解答诸如当前 CPU 开销较高、内存占用较大、进程不明原因卡死等复杂问题。

该功能在用户点击收集的时刻开始收集一小段时间（默认 30 秒）的性能数据，因而只能用于分析集群当前正在面临的问题，对于当前已经不再复现的问题没有显著效果。若你想要收集或分析过去任意时刻性能数据、不希望每次都人工介入按需分析，请参阅[持续性能分析](/dashboard/continuous-profiling.md)功能。

## 支持的性能数据

目前支持收集并分析以下性能数据：

- CPU：TiDB、TiKV、PD、TiFlash 实例上各个内部函数的 CPU 开销情况

  > ARM 环境中暂不支持对 TiKV 和 TiFlash 的 CPU 开销情况进行分析。

- Heap：TiDB、PD 实例上各个内部函数的内存占用开销情况

- Mutex：TiDB、PD 实例上各个处于等待状态的 Mutex 情况

- Goroutine：TiDB、PD 实例上各个 Goroutine 的运行状态及调用栈情况

## 访问页面

可以通过以下两种方法访问实例性能分析页面：

- 登录后，左侧导航条点击**高级调试** (Advanced Debugging) > **实例性能分析** (Profile Instances) > **手动分析** (Manually Profile)：

  ![访问页面](/media/dashboard/dashboard-profiling-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/instance_profiling>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 开始性能分析

在实例性能分析页面，选择至少一个目标实例和分析类型，确定性能分析时长（默认为 30 秒）。点击**开始分析** (Start Profiling) ：

![开始分析](/media/dashboard/dashboard-profiling-start.png)

在已经启用了[持续性能分析](/dashboard/continuous-profiling.md)的集群上，手工性能分析不再可用。若要在启用了持续性能分析功能的集群上获取当前时刻的集群性能数据，请直接点击持续性能分析页面上最近一次的分析结果进行查看。

## 查看性能分析状态

开始性能分析后，可以看到实时性能分析状态和进度：

![实时状态](/media/dashboard/dashboard-profiling-view-progress.png)

性能分析会在后台运行，刷新或退出当前页面不会终止已经运行的性能分析任务。

## 下载性能数据

所有实例的性能分析都完成后，可点击右上角下载按钮 (Download Profiling Result) 打包下载所有性能数据：

![下载分析结果](/media/dashboard/dashboard-profiling-download.png)

也可以点击列表中的单个实例查看其性能数据，或者悬浮到 **...** 按钮上下载原始数据：

![在线查看分析结果](/media/dashboard/dashboard-profiling-view-single.png)

## 查看历史性能数据

在性能分析页面下方，列出了你手工发起的性能分析历史。点击任意一行，即可查看其状态详情：

![历史列表](/media/dashboard/dashboard-profiling-history.png)

关于状态详情页的操作，参见[查看性能分析状态](#查看性能分析状态)章节。

若你想要收集或分析过去任意时刻性能数据、不希望每次都人工介入按需分析，请参阅[持续性能分析](/dashboard/continuous-profiling.md)功能。
