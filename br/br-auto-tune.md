---
title: BR 自动调节
summary: 了解 BR 特性的详细介绍。
---

# BR 自动调节 <span class="version-mark">从 v5.4 版本开始引入</span>

在 v5.4.0 之前，BR 默认情况下使用的线程数量是总逻辑 CPU 数量的 75%。在没有限速的前提下，BR 会消耗大量的集群资源，对在线集群的性能造成相当大的影响。

即便这些影响可以通过调节线程池的大小完成，观察负载、手动调节线程池大小也是一件繁琐的事情。

为了减少 BR 对在线集群的影响，在 v5.4.0 之后，BR 引入了“自动调节”功能，在集群资源占用率较高的情况下，自动限制备份使用的资源以求减少对集群的影响。该功能默认开启。

## 使用场景

如果你希望减少 BR 备份对集群的影响，并且没有使用 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) 或者 `--ratelimit` 参数进行备份限速，那么你可以开启自动调节功能。此时 BR 会尝试在不过度影响集群的前提下以最快速度运行。

## 使用方法

如需开启 BR 自动调节功能，将 TiKV 配置项 [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-从-v54-版本开始引入) 设置为 `true`。

TiKV 支持[动态配置](/tikv-control.md#动态修改-tikv-的配置)自动调节功能，无需重启集群。运行以下命令，即可动态启动或停止 BR 自动调节：

{{< copyable "shell-regular" >}}

```shell
tikv-ctl modify-tikv-config -n backup.enable-auto-tune -v <true|false>
```

> **注意：**
>
> - v5.4.0 及以上集群，自动调节功能默认打开，无需额外配置。
> - v5.4.0 以下的集群，在升级到 v5.4.0 及以上版本后，自动调节功能默认关闭。如需开启，需手动设置 `backup.enable-auto-tune` 为 `true`。

## 使用限制

自动调节是一个粗粒度的限流方案，它的优势在无需手动调节，但是调节粒度不够精确，也可能无法彻底移除备份对集群的影响。

已知的问题包括：

- 问题：**对于以写负载为主的集群**，自动调节可能会让工作负载和备份进入一种“正反馈循环”：备份占用了资源，让工作负载使用的资源变少了，自动调节误以为资源使用下降了，从而让 BR 更加激进。这种情况下，自动调节实际上失效。
    - 解决方法：手动调节 `backup.num-threads`，限制处理备份的工作线程数量。
- 问题：**集群存在热点**，热点 TiKV 节点可能会被过度限流，从而拉慢备份整体的进度。
    - 解决方法：消除热点节点，或者在热点节点上关闭自动调节（可能导致集群性能降低）。
- 问题：**流量抖动非常大的场景下**，因为自动调节每隔 `auto-tune-refresh-interval`（默认为一分钟）才会计算出新的限流，所以可能无法很好地应对流量抖动非常厉害的场景。
    - 解决方法：关闭自动调节。

## 原理

自动调节的理念是：通过调节 backup 的线程池大小，保证集群的 CPU 总体使用率不超过某个特定的值。

这个特性还有两个配置项未在 TiKV 文档中列出，仅在内部调试使用，正常备份时**无需**配置这两个参数。

- `backup.auto-tune-remain-threads`：自动调节通过控制 backup 的资源占用，保证集群至少有 `auto-tune-remain-threads` 个核心保持空闲状态。这个参数的默认值是 `round(0.2 * vCPU)`。
- `backup.auto-tune-refresh-interval`：每隔多长时间，自动调节会刷新统计信息并重新计算出备份核心数量上限。

以下是一个示例，其中 * 代表被备份任务占用的 CPU，^ 代表被集群中的其它任务占用的 CPU，- 代表空闲 CPU。

```
|--------| 系统总共有 8 颗逻辑 CPU。
|****----| 默认配置 `backup.num-threads` 为 4，注意在任何时候自动调节都不会让线程池大小大于 backup.num-threads。
|^^****--| 默认情况下，`auto-tune-remain-threads` = round(8 * 0.2) = 2, 自动调节会将 backup 的线程池大小调节至 4。
|^^^^**--| 集群的工作负载加重了，自动调节将备份的线程池大小调节至 2，如此集群中仍旧还有两个核心保持空闲。
```

在监控面板的 “Backup CPU Utilization” 中，可以看到自动限流目前选择的线程池的大小：

![Grafana dashboard example of backup auto-tune metrics](/media/br/backup-auto-throttle.png)

背景中黄色半透明的填充即为自动限流生效后 Backup 可用的线程，可以看到 Backup 的 CPU 使用率不会超过黄色部分。
