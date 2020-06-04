---
title: TiDB Dashboard 流量可视化页面
category: how-to
aliases: ['/docs-cn/dev/how-to/monitor/key-visualizer/','/docs-cn/dev/key-visualizer-monitoring-tool/']
---

# TiDB Dashboard 流量可视化页面

流量可视化页面 (Key Visualizer) 可用于分析 TiDB 集群的使用模式和排查流量热点。该页面可视化地呈现了 TiDB 集群一段时间的流量情况。

## 访问页面

可以通过以下两种方法访问 Key Visualizer 流量可视化页面：

* 登录 TiDB Dashboard 后，点击左侧导航条的 **Key Visualizer**（流量可视化）：

![访问](/media/dashboard/dashboard-keyviz-access.png)

* 在浏览器中访问 `http://127.0.0.1:2379/dashboard/#/keyviz`（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 界面示例

流量可视化页面示例如下：

![Key Visualizer 示例图](/media/dashboard/dashboard-keyviz-overview.png)

从以上流量可视化界面可以观察到以下信息：

+ 一个大型热力图，显示整体访问流量随时间的变化情况。
+ 热力图某个坐标的详细信息。
+ 左侧为表、索引等标识信息。

## 基本概念

本节介绍流量可视化涉及的一些基本概念。

### Region

在 TiDB 集群中，数据以分布式的方式存储在所有的 TiKV 实例中。TiKV 在逻辑上是一个巨大且有序的 KV Map。整个 Key-Value 空间分成很多 Region，每一个 Region 是一系列连续的 Key。

> **注意：**
>
> 关于 Region 的详细介绍，请参考[三篇文章了解 TiDB 技术内幕 - 说存储](https://pingcap.com/blog-cn/tidb-internal-1/#region)

### 热点

在使用 TiDB 的过程中，热点是一个典型的现象，它表现为大量的流量都在读写一小块数据。由于连续的数据往往由同一个 TiKV 实例处理，因此热点对应的 TiKV 实例的性能就成为了整个业务的性能瓶颈。常见的热点场景有使用自增主键连续写入相邻数据导致的写入表数据热点、时间索引下写入相邻时间数据导致的写入表索引热点等。

> **注意：**
>
> 热点问题详情请参阅 [TiDB 热点问题详解](https://asktug.com/t/topic/358)。

### 热力图

热力图是流量可视化页面的核心，它显示了一个指标随时间的变化。热力图的横轴 X 是时间，纵轴 Y 则是按 Key 排序的连续 Region，横跨 TiDB 集群上所有数据库和数据表。颜色越暗 (cold) 表示该区域的 Region 在这个时间段上读写流量较低，颜色越亮 (hot) 表示读写流量越高，即越热。

### Region 压缩

一个 TiDB 集群中，Region 的数量可能多达数十万。在屏幕上是难以显示这么多 Region 信息的。因此，在一张热力图中，Region 会被压缩到约 1500 个连续范围，每个范围称为 Bucket。在一个热力图上，热的实例更需要关注，因此 Region 压缩总是倾向于将流量较小的大量 Region 压缩为一个 Bucket，而尽量让高流量的 Region 独立成 Bucket。

## 使用介绍

本节介绍如何使用流量可视化页面。

### 设置

首次使用流量可视化页面需要先通过**设置**页面手动开启此功能。参考页面指引，点击 **Open Settings**（打开设置）即可打开设置页面：

![功能未开启](/media/dashboard/dashboard-keyviz-not-enabled.png)

在功能已经开启时，可通过右上角的设置图标打开设置页面：

![设置按钮](/media/dashboard/dashboard-keyviz-settings-button.png)

设置页面如下图所示：

![设置页面](/media/dashboard/dashboard-keyviz-settings.png)

通过开关设定好是否开启收集，并点击 **Save**（保存）后生效。开启后，在界面上观察到工具栏已经可以使用：

![工具栏](/media/dashboard/dashboard-keyviz-toolbar.png)

功能开启后，后台会持续收集数据，稍等一段时间即可看到热力图。

### 观察某一段时间或者 Region 范围

打开流量可视化页面时，默认会显示最近六小时整个数据库内的热力图。其中，越靠近右侧（当前时间）时，每列 Bucket 对应的时间间隔会越小。如果你想观察某个特定时间段或者特定的 Region 范围，则可以通过放大来获得更多细节。具体操作描述如下：

* 在热力图中向上或向下滚动。
* 点击 **Select & Zoom**（框选）按钮，然后点击并拖动以选择要放大的区域。

![框选](/media/dashboard/dashboard-keyviz-select-zoom.gif)

* 点击 **Reset**（重置）按钮，将 Region 范围重置为整个数据库。
* 点击「时间选择框」（界面的 **6 hours** 处），重新选择观察时间段。

![时间选择](/media/dashboard/dashboard-keyviz-select-time.png)

> **注意：**
>
> 进行后三种操作，将引起热力图的重新绘制。你可能观察到热力图与放大前有较大差异。这是一个正常的现象，可能是由于在进行局部观察时，Region 压缩的粒度发生了变化，或者是局部范围内，“热”的基准发生了改变。

### 调整亮度

热力图使用颜色的明暗来表达一个 Bucket 的流量高低，颜色越暗 (cold) 表示该区域的 Region 在这个时间段上读写流量较低，颜色越亮 (hot) 表示读写流量越高，即越热。如果热力图中的颜色太亮或太暗，则可能很难观察到细节。此时，可以点击 **Brightness**（调整亮度）按钮，然后通过滑块来调节页面的亮度。

> **注意：**
>
> 在显示一个区域内的热力图时，会根据区域内的流量情况来界定冷热。当整个区域流量较为平均时，即使整体流量在数值上很低，你依然有可能观察到较大的亮色区域。请注意一定要结合数值一起分析。

### 选择指标

![指标选择](/media/dashboard/dashboard-keyviz-select-type.png)

你可以通过「指标选择框」（以上界面中 **Write (bytes)** 处）来查看你关心的指标：

* `Read (bytes)`：读取字节量
* `Write (bytes)`：读取字节量
* `Read (keys)`：读取次数
* `Write (keys)`：写入次数
* `All`：所有（读写流量的总和）

### 刷新与自动刷新

可以通过点击 **Refresh**（刷新）按钮来重新获得基于当前时间的热力图。当需要实时观察数据库的流量分布情况时，可以点击按钮右侧的向下箭头，选择一个固定的时间间隔让热力图按此间隔自动刷新。

> **注意：**
>
> 如果进行了时间范围或者 Region 范围的调整，自动刷新会被关闭。

### 查看详情

可以将鼠标悬停在你所关注的 Bucket 上，来查看这个区域的详细信息：

![Bucket 详细信息](/media/dashboard/dashboard-keyviz-tooltip.png)

如果需要复制某个信息，可以进行点击 Bucket。此时相关详细信息的页面会被暂时钉住。点击你关注的信息，即可将其复制到剪切板：

![复制 Bucket 详细信息](/media/dashboard/dashboard-keyviz-tooltip-copy.png)

## 常见热力图解读

本章节选取了 Key Visualizer 中常见的四种热力图进行解读。

### 均衡：期望结果

![均衡结果图](/media/dashboard/dashboard-keyviz-well-dist.png)

如上图所示，热力图颜色均匀或者深色和亮色混合良好，说明读取或写入在时间和 Region 空间范围上都分布得比较均衡，访问压力均匀地分摊在所有的机器上。这种负载是最适合分布式数据库的。

### X 轴明暗交替：需要关注高峰期的资源情况

![X 轴明暗交替](/media/dashboard/dashboard-keyviz-period.png)

如上图所示，热力图在 X 轴（时间）上表现出明暗交替，但 Y 轴 (Region) 则比较均匀，说明读取或写入负载具有周期性的变化。这种情况可能出现在周期性的定时任务场景，如大数据平台每天定时从 TiDB 中抽取数据。一般来说可以关注一下使用高峰时期资源是否充裕。

## Y 轴明暗交替：需要关注产生的热点聚集程度

![Y 轴明暗交替](/media/dashboard/dashboard-keyviz-continue.png)

如上图所示，热力图包含几个明亮的条纹，从 Y 轴来看条纹周围都是暗的，这表明明亮条纹区域的 Region 有很高的读写流量，可以从业务角度观察一下是否符合预期。例如，所有业务都关联用户表的情况下，用户表的整体流量就会很高，那么在热力图中表现为亮色区域就非常合理。

另外，明亮区域的高度（Y 轴方向的粗细）非常关键。由于 TiKV 自身拥有以 Region 为单位的热点平衡机制，因此涉及热点的 Region 越多其实越能有利于在所有 TiKV 实例上均衡流量。明亮条纹越粗、数量越多则意味着热点越分散、更多的 TiKV 能得到利用；明亮条纹越细、数量越少意味着热点越集中、热点 TiKV 越显著、越需要人工介入并关注。

### 明亮斜线：需要关注业务模式

![明亮斜线](/media/dashboard/dashboard-keyviz-sequential.png)

如上图所示，热力图显示了明亮的斜线，表明读写的 Region 是连续的。这种场景常常出现在带索引的数据导入或者扫描阶段。例如，向自增 ID 的表进行连续写入等等。图中明亮部分对应的 Region 是读写流量的热点，往往会成为整个集群的性能问题所在。这种时候，可能需要业务重新调整主键，尽可能打散以将压力分散在多个 Region 上，或者选择将业务任务安排在低峰期。

> **注意：**
>
> 这里只是列出了几种常见的热力图模式。流量可视化页面中实际展示的是整个集群上所有数据库、数据表的热力图，因此非常有可能在不同的区域观察到不同的热力图模式，也可能观察到多种热力图模式的混合结果。使用的时候应当视实际情况灵活判断。

## 解决热点问题

TiDB 内置了不少帮助缓解常见热点问题的功能，深入了解请参考 [TiDB 高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md)。
