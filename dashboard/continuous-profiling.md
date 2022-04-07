---
title: TiDB Dashboard 实例性能分析 - 持续分析页面
summary: 了解如何持续地收集 TiDB、TiKV、PD 各个实例的性能数据，缩短平均故障恢复时间
---

# TiDB Dashboard 实例性能分析 - 持续分析页面

> **注意：**
>
> 该功能面向技术专家，建议在 PingCAP 专业技术人员的指导下使用该功能。
>
> 你必须使用 TiUP（v1.9.0 及以上版本）或 TiDB Operator（v1.3.0 及以上版本）部署或升级集群，才可以使用该功能。

持续性能分析功能可以**持续地**收集 TiDB、TiKV、PD 各个实例的性能数据。收集到的性能数据可显示为火焰图或有向无环图形式。

通过这些性能数据，技术专家可以分析实例的 CPU、内存等资源消耗细节，帮助解答诸如某一时刻 CPU 开销较高、内存占用较大、进程不明原因卡死等复杂问题。即使这类问题无法得到复现，技术专家也可以通过查看当时记录下的历史性能数据，还原问题现场，对当时的问题进行细致分析，从而有效缩短平均故障恢复时间。

## 与手工性能分析的区别

持续性能分析是[手工性能分析](/dashboard/dashboard-profiling.md)的强化功能，它们都能用于收集和分析各个实例不同维度的性能数据，主要区别如下：

- 手工性能分析仅在用户发起分析的时刻收集一小段时间（如 30 秒）的性能数据；持续性能分析开启后会持续收集性能数据；
- 手工性能分析只能用于分析集群当前的问题；持续性能分析既可以用于分析集群当前问题，可以分析集群历史问题；
- 手工性能分析允许仅收集特定实例的特定性能数据；持续性能分析会收集所有实例的所有性能数据；
- 由于持续性能分析存储了更多性能数据，因此会占用更大的磁盘空间；
- 由于目前频繁进行性能分析会对 TiFlash 产生稳定性影响，因此当前版本中持续性能分析功能不会收集 TiFlash 的性能数据。

## 支持的性能数据

除了 TiFlash CPU 开销情况由于稳定性原因没有收集以外，其他所有[手工性能分析](/dashboard/dashboard-profiling.md#支持的性能数据)中的性能数据都会在该功能中收集：

- CPU：TiDB、TiKV、PD 实例上各个内部函数的 CPU 开销情况

  > ARM 环境中暂不支持对 TiKV 的 CPU 开销情况进行分析。

- Heap：TiDB、PD 实例上各个内部函数的内存占用开销情况

- Mutex：TiDB、PD 实例上各个处于等待状态的 Mutex 情况

- Goroutine：TiDB、PD 实例上各个 Goroutine 的运行状态及调用栈情况

## 访问页面

你可以通过以下任一方式访问持续性能分析页面：

- 登录后，左侧导航条点击**高级调试** (Advanced Debugging) > **实例性能分析** (Profiling Instances) > **持续分析** (Continuous Profiling)：

  ![访问页面](/media/dashboard/dashboard-conprof-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/continuous_profiling>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 启用持续性能分析

持续性能分析默认处于关闭状态。该功能启用后，TiDB Dashboard 会在后台持续收集性能数据，用户无需保持网页处于打开状态。后台收集的性能数据可设置保留时长，超过保留时长的性能数据将会被自动清理。

你可以通过以下步骤启用该功能：

1. 访问持续性能分析页面。
2. 点击**打开设置** (Open Settings)。在右侧**设置** (Settings) 页面，将**启用特性** (Enable Feature) 下方的开关打开。设置**保留时间** (Retention Period) 不做修改使用默认值（3 天）。
3. 点击**保存** (Save)。

![启用功能](/media/dashboard/dashboard-conprof-start.png)

## 查看集群当前性能数据

在已经启用了持续性能分析的集群上，手工性能分析不再可用。若要查看当前时刻集群性能数据，请直接点击页面上最近一次的分析结果进行查看。

## 查看集群历史性能数据

你可以在列表中看到自启用该功能以来所有自动收集的性能数据：

![历史结果](/media/dashboard/dashboard-conprof-history.png)

## 下载性能数据

进入某次分析结果后，可点击右上角下载按钮 (Download Profiling Result) 打包下载所有性能数据：

![下载某次分析结果](/media/dashboard/dashboard-conprof-download.png)

也可以点击列表中的单个实例查看其性能数据，或者悬浮在 **...** 按钮上下载原始数据：

![查看单个实例分析结果](/media/dashboard/dashboard-conprof-single.png)

## 停用持续性能分析

你可以通过以下步骤在持续性能分析页面上停用该功能：

1. 访问持续性能分析页面。
2. 点击**设置** (Settings)，将**启用特性** (Enable Feature) 下方的开关关闭。
3. 在弹出的**停用持续分析** (Disable Continuous Profiling Feature) 对话框中，选择**停用** (Disable)。
4. 点击**保存** (Save)。
5. 点击弹窗的**确认**（Disable）。

![停用功能](/media/dashboard/dashboard-conprof-stop.png)
