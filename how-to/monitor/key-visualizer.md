---
title: Key Visualizer 热点可视化
category: how-to
---

# Key Visualizer 热点可视化

## 什么是 Key Visualizer？

Key Visualizer 是一款用于分析 TiDB 使用模式和排查流量热点的工具。它会将 TiDB 数据库集群一段时间的指标生成可视化报告，可用于快速直观地观察集群整体热点及流量分布情况。

## 如何访问 Key Visualizer？

Key Visualizer 功能作为 TiDB Dashboard 组件的功能之一，直接集成在 PD 节点上，无需单独部署。可通过以下方式在浏览器中访问某个 PD 实例上的 Dashboard：

{{< copyable "" >}}

```
http://PDAddress:PDPort/dashboard
```

> **注意：**
>
> 默认情况下 `PDPort` 是 `2379`。若部署时修改过 PD 相应参数，则需要填写对应的端口。

### 4.0.0-beta.1 版本中的注意事项

* 存在一些显示问题和浏览器兼容问题，如文本溢出边框等。
* 首次打开时，界面的文本显示可能存在问题，您可能会见到诸如 `keyvis.toolbar.brightness` 这样的文本。此时您只需点击页面的右上角，重新选择语言即可，如图所示：
    
    ![choose language](/media/dashboard/language.png)
    
* 默认情况下，所有的 PD 节点上都能访问 Dashbord，但目前只有 PD Leader 节点能正常显示热力图。如果当前 PD 有多个节点，您可以按照以下方式获取当前 PD Leader 节点的信息：
    * 访问任意 PD 节点的如下 API 地址：`http://PDAddress:PDPort/pd/api/v1/leader`
    * 使用返回数据中 client_urls 字段中的地址访问 PD Leader 节点的 Dashboard

## Key Visualizer 总览

下图为一个 Key Visualizer 页面示例，可以观察到以下信息：

* 一个大型热力图，显示访问流量随时间的变化情况。
* 下方和右侧为沿热力图的每个轴的平均值。
* 左侧为表、索引等信息。

![overview key-visualizer](/media/dashboard/keyvisualizer/overview.png)

## 如何使用 Key Visualizer？

此部分介绍如何使用 Key Visualizer。

### 概念介绍

**Region**

TiDB 作为一个分布式数据库，其数据是分散在不同的节点上的。对于一张表的数据，我们会在逻辑上切分成若干个连续的区间，将这些区间内的数据分给不同的机器存储，不管是写入还是读取，只需要知道目标数据属于哪个区间，就可以直接到那个机器上进行访问。然后加上对每一个区间的数据在物理上做多副本冗余实现高可用。如下图所示，Region 在 TiDB 的内部就是一个个连续的数据区间。

![view region](/media/dashboard/keyvisualizer/region.png)

> **注意：**
>
> 关于 Region 的详细介绍，请参考[《三篇文章了解 TiDB 技术内幕 - 说存储》](https://pingcap.com/blog-cn/tidb-internal-1/#region)

**热点**

一个典型的热点，是大量的流量都在读写一小块数据，在 TiDB 架构中，每一行数据会对应一个 TiKV 节点进行处理，而不是所有节点都能用于处理这一行数据。因而，如果大多数业务流量都在频繁访问某一行数据，那么大多数业务流量最终都会由某一个 TiKV 节点来处理，最终这个 TiKV 机器的性能就成为了整个业务的性能上限，无法通过增加更多机器来提高处理能力。由于 TiDB 实际上是以 Region（即一批相邻数据）为单位划分处理，因此除了上述场景以外还有更多会产生热点的场景，如使用自增主键连续写入相邻数据导致的写入表数据热点、时间索引下写入相邻时间数据导致的写入表索引热点等。

> **注意：** 
>
> 热点问题详情请参阅[《TiDB 热点问题详解》](https://asktug.com/t/tidb/358)。

**热力图**

热力图是 Key Visualizer 的核心，它显示了一个指标随时间的变化。热力图的横轴 X 是时间，纵轴 Y 则表示集群里面的 Region，横跨 TiDB 集群上所有数据库和数据表。颜色越暗（cold）表示该区域的 Region 在这个时间段上读写流量较低，颜色越亮（hot）表示读写流量越高，即越热。

**Region 压缩**

一个 TiDB 集群中，Region 的数量可能多达数十万。我们难以把这么多的 Region 信息显示在屏幕上。因此，在一张热力图中，我们会将 Region 压缩到约 1500 个连续范围，每个范围我们称为「Bucket」。由于在一个热力图上，我们更关心那些热的节点，因此 Region 压缩总是倾向于将 流量较小的大量 Region 压缩为一个 Bucket，而尽量让高流量的 Region 独立成 Bucket。

### 使用说明

![view toolbar](/media/dashboard/keyvisualizer/toolbar.png)

**观察某一段时间或者 Region 范围**

打开 Key Visualizer 时，默认会显示最近 6 小时整个数据库内的热力图。其中，越靠近右侧（当前时间）时，每个 Bucket 对应的时间间隔会越小。如果您想观察某个特定时间段或者特定的 Region 范围，则可以通过放大来获得更多细节。

* 在热力图中向上或向下滚动。
* 点击 **Select & Zoom** 按钮，然后点击并拖动以选择要放大的区域。
* 点击 **Reset** 按钮，将 Region 范围重置为整个数据库。
* 点击 **时间选择框**，重新选择观察时间段。

> **注意：**
>
> 使用后几种方法，将引起热力图的重新绘制，您可能观察到热力图与放大前有较大差异。这是一个正常的现象。它可能是由于在进行局部观察时，Region 压缩的粒度发生了变化，或者是局部范围内，“热”的基准发生了改变。

**调整亮度**

热力图使用颜色的明暗来表达一个 Bucket 的流量高低，颜色越暗（cold）表示该区域的 Region 在这个时间段上读写流量较低，颜色越亮（hot）表示读写流量越高，即越热。如果热力图中的颜色太亮或太暗，则可能很难观察到细节。此时，我们可以点击 **Brightness** 按钮，然后通过滑块来调节页面的亮度。

> 注意：Key Visualizer 在显示一个区域内的热力图时，会根据区域内的流量情况来界定冷热。当整个区域流量较为平均时，即使整体流量在数值上很低，您依然有可能观察到较大的亮色区域。请注意一定要结合数值一起分析。

**自动刷新**

当我们需要实时观察数据库的流量分布情况是，可以点击 **Auto Refresh** 按钮来让热力图每分钟自动刷新。请注意，如果您进行了时间范围或者 Region 范围的调整，自动刷新会被关闭。

**选择指标**

您可以通过 **指标选择框** 来查看您关心的指标，目前我们支持如下指标：

* Read (bytes) 读流量
* Write (bytes) 写流量
* Read (keys) 读取行数
* Write (keys) 写入行数
* All 读写流量的总和

**查看详情**

您可以将鼠标悬停在您关心的 Bucket 上，来查看这个区域的详细信息。

![view tooltip](/media/dashboard/keyvisualizer/tooltip.png)

如果您有复制某个信息的需要，可以在 bucket 进行点击。此时这个详细信息的页面会被暂时钉住。点击您关心的信息，即可将其复制到剪切板。

![copy tooltip](/media/dashboard/keyvisualizer/tooltip-copy.png)

### 常见热力图解读

**均衡：期望结果**

![view balance](/media/dashboard/keyvisualizer/balance.png)

如图所示，热力图颜色均匀或者深色和亮色混合良好，说明读取或写入在时间和 Region 空间范围上都分布得比较均衡，访问压力均匀地分摊在所有的机器上。这种负载是最适合分布式数据库的，也是我们最希望见到的。

**X 轴明暗交替：需要关注高峰期的资源情况**

![view period-x](/media/dashboard/keyvisualizer/period-x.png)

如图所示，热力图在 X 轴（时间）上表现出明暗交替，但 Y 轴（Region）则比较均匀，说明读取或写入负载具有周期性的变化。这种情况可能出现在周期性的定时任务场景，如大数据平台每天定时从 TiDB 中抽取数据。一般来说可以关注一下使用高峰时期资源是否充裕。

**Y 轴明暗交替：需要关注产生的热点聚集程度**

![view period-y](/media/dashboard/keyvisualizer/period-y.png)

如图所示，热力图包含几个明亮的条纹，从 Y 轴来看条纹周围都是暗的，这表明，明亮条纹区域的 Region 具有很高的读写流量，可以从业务角度观察一下是否符合预期。例如，所有业务都关联用户表的情况下，用户表的整体流量就会很高，那么在热力图中表现为亮色区域就非常合理。另外，明亮区域的高度 （Y 轴方向的粗细）非常关键。由于TiKV 自身拥有以 Region 为单位的热点平衡机制，因此涉及热点的 Region 越多其实越能有利于在所有 TiKV 节点上均衡流量。明亮条纹越粗、数量越多则意味着热点越分散、更多的 TiKV 能得到利用；明亮条纹越细、数量越少意味着热点越集中、热点 TiKV 越显著、越需要人工介入并关注。

**局部突然变亮：需要关注突增的读写请求**

![view burst](/media/dashboard/keyvisualizer/burst.png)

如图所示，热力图中某些区域突然由暗色变为了亮色。这说明在短时间内这些 Region 数据流量突然增加。这种时候，需要依据业务关注流量突变是否符合预期，并评估系统资源是否充足。另外，明亮区域的高度 （Y 轴方向的粗细）同样非常关键，理由同上。

**明亮斜线：需要关注业务模式**

![view slash](/media/dashboard/keyvisualizer/slash.png)

如图所示，热力图显示了明亮的斜线，表明读写的 Region 是连续的。这种场景常常出现在带索引的数据导入或者扫描阶段。例如，向自增 ID 的表进行连续写入等等。图中明亮部分对应的 Region 是读写流量的热点，往往会成为整个集群的性能问题所在。这种时候，可能需要业务重新调整主键，尽可能打散以将压力分散在多个 Region 上，或者选择将业务任务安排在低峰期。

> 注意：这里只是列出了几种常见的热力图模式。Key Visualizer 中实际展示的是整个集群上所有数据库、数据表的热力图，因此非常有可能在不同的区域观察到不同的热力图模式，也可能观察到多种热力图模式的混合结果。使用的时候应当视实际情况灵活判断。

### 解决热点问题

TiDB 内置了不少帮助缓解常见热点问题的功能，深入了解请参考[《TiDB 高并发写入常见热点问题及规避方法》](https://pingcap.com/blog-cn/tidb-in-high-concurrency-scenarios/)。
