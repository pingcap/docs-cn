---
title: GC 配置
summary: TiDB 的 GC 配置可以通过系统变量进行设置，包括启用 GC、运行间隔、数据保留时限、并发线程数量等。此外，TiDB 还支持 GC 流控，可以限制每秒数据写入量。从 TiDB 5.0 版本开始，建议使用系统变量进行配置，避免异常行为。在 TiDB 6.1.0 版本引入了新的系统变量 `tidb_gc_max_wait_time`，用于控制活跃事务阻塞 GC safe point 推进的最长时间。另外，GC in Compaction Filter 机制可以通过配置文件或在线配置开启，但可能会影响 TiKV 扫描性能。
---

# GC 配置

你可以通过以下系统变量进行 GC 配置：

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-从-v50-版本开始引入)：控制是否启用 TiKV 的垃圾回收 (GC) 机制。
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-从-v50-版本开始引入)：指定垃圾回收 (GC) 运行的时间间隔。
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)：指定每次进行垃圾回收 (GC) 时保留数据的时限。
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入)：指定 GC 在 [Resolve Locks（清理锁）](/garbage-collection-overview.md#resolve-locks清理锁)步骤中线程的数量。
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)：指定垃圾回收 (GC) 的 Resolve Locks（清理锁）步骤中扫描锁的方式。
* [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入)：指定活跃事务阻碍 GC safe point 推进的最大时间。

关于如何修改系统变量的值，请参考[系统变量](/system-variables.md)。

## 流控

TiDB 支持 GC 流控，可通过配置 `gc.max-write-bytes-per-sec` 限制 GC worker 每秒数据写入量，降低对正常请求的影响，`0` 为关闭该功能。该配置可通过 tikv-ctl 动态修改：

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 引入的变化

在 TiDB 5.0 之前的版本中，GC 是通过系统表 `mysql.tidb` 进行配置的。从 TiDB 5.0 版本起，GC 仍然可以通过系统表 `mysql.tidb` 进行配置，但建议你使用系统变量进行配置，这样可以确保对配置的任何更改都能得到验证，防止造成异常行为 ([#20655](https://github.com/pingcap/tidb/issues/20655))。

TiDB 5.0 及之后的版本不再需要向各个 TiKV Region 都发送触发 GC 的请求，因此不再提供 `CENTRAL` GC 模式的支持，取而代之的是效率更高的 `DISTRIBUTED` GC 模式 （自 TiDB 3.0 起的默认 GC 模式）。

如果要了解 TiDB 历史版本中 GC 配置的变化信息，请使用左侧导航栏中的 _"TIDB 版本选择器"_ 切换到本文档的历史版本。

## TiDB 6.1.0 引入的变化

在 TiDB 6.1.0 之前的版本中，TiDB 内部事务不会影响 GC safe point 推进。从 TiDB 6.1.0 版本起，计算 safe point 时会考虑内部事务的 startTS，从而解决内部事务因访问的数据被清理掉而导致失败的问题。带来的负面影响是如果内部事务运行时间过长，会导致 safe point 长时间不推进，进而会影响业务性能。

TiDB v6.1.0 引入了系统变量 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入) 控制活跃事务阻塞 GC safe point 推进的最长时间，超过该值后 GC safe point 会强制向后推进。

## GC in Compaction Filter 机制

GC in Compaction Filter 机制是在分布式 GC 模式 (`DISTRIBUTED` GC mode) 的基础上，由 RocksDB 的 Compaction 过程来进行 GC，而不再使用一个单独的 GC worker 线程。这样做的好处是避免了 GC 引起的额外磁盘读取，以及避免清理掉的旧版本残留大量删除标记影响顺序扫描性能。可以由 TiKV 配置文件中的以下开关控制：

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

该 GC 机制可通过在线配置变更开启：

{{< copyable "sql" >}}

```sql
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | false |
+------+-------------------+-----------------------------+-------+
```

{{< copyable "sql" >}}

```sql
set config tikv gc.enable-compaction-filter = true;
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | true  |
+------+-------------------+-----------------------------+-------+
```

> **注意：**
>
> 在使用 Compaction Filter 机制时，可能会出现 GC 进度延迟的情况，从而影响 TiKV 扫描性能。当你的负载中含有大量 coprocessor 请求，并且在 [**TiKV-Details > Coprocessor Detail**](/grafana-tikv-dashboard.md#coprocessor-detail) 面板中发现 Total Ops Details 的 `next()` 或 `prev()` 调用次数远远超过 `processed_keys` 调用的三倍时，可以采取以下措施：
> 
> - 对于 TiDB v7.1.3 之前版本，建议尝试关闭 Compaction Filter，以加快 GC 速度。
> - 从 v7.1.3 开始，TiDB 会根据每个 Region 的冗余版本数量 [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-从-v710-版本开始引入) 和比例 [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-从-v710-版本开始引入) 自动触发 compaction，从而提高 Compaction Filter 的 GC 速度。因此，在 v7.1.3 及之后的版本中，如果遇到上述情况，建议调整这两个参数，无需关闭 Compaction Filter。
