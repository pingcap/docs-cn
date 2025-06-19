---
title: 垃圾回收配置
summary: 了解 GC 配置参数。
---

# 垃圾回收配置

你可以使用以下系统变量配置垃圾回收（GC）：

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)：控制是否启用 TiKV 的垃圾回收。
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)：指定 GC 的运行间隔。
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)：指定每次 GC 时保留数据的时间限制。
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)：指定 GC 的 [Resolve Locks](/garbage-collection-overview.md#resolve-locks) 步骤中的线程数。
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)：指定 GC 的 Resolve Locks 步骤中扫描锁的方式。
* [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)：指定活跃事务阻塞 GC 安全点的最长时间。

关于如何修改系统变量的值，请参考[系统变量](/system-variables.md)。

## GC I/O 限制

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节仅适用于 TiDB Self-Managed。TiDB Cloud 默认没有 GC I/O 限制。

</CustomContent>

TiKV 支持 GC I/O 限制。你可以配置 `gc.max-write-bytes-per-sec` 来限制每个 GC worker 每秒的写入量，从而减少对正常请求的影响。

`0` 表示禁用此功能。

你可以使用 tikv-ctl 动态修改此配置：

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 的变化

在 TiDB 的早期版本中，垃圾回收是通过 `mysql.tidb` 系统表配置的。虽然对该表的更改仍然受支持，但建议使用提供的系统变量。这有助于确保对配置的任何更改都可以被验证，并防止意外行为（[#20655](https://github.com/pingcap/tidb/issues/20655)）。

不再支持 `CENTRAL` 垃圾回收模式。将自动使用 `DISTRIBUTED` GC 模式（自 TiDB 3.0 以来一直是默认模式）。这种模式更有效，因为 TiDB 不再需要向每个 TiKV region 发送请求来触发垃圾回收。

有关早期版本变更的信息，请使用左侧菜单中的 _TIDB 版本选择器_ 参考本文档的早期版本。

## TiDB 6.1.0 的变化

在 TiDB v6.1.0 之前，TiDB 中的事务不会影响 GC 安全点。从 v6.1.0 开始，TiDB 在计算 GC 安全点时会考虑事务的 startTS，以解决要访问的数据已被清除的问题。如果事务时间过长，安全点将被长时间阻塞，这会影响应用程序性能。

在 TiDB v6.1.0 中，引入了系统变量 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) 来控制活跃事务阻塞 GC 安全点的最长时间。超过该值后，GC 安全点将被强制推进。

### Compaction Filter 中的 GC

基于 `DISTRIBUTED` GC 模式，Compaction Filter 中的 GC 机制使用 RocksDB 的 compaction 过程，而不是单独的 GC 工作线程来运行 GC。这种新的 GC 机制有助于避免 GC 造成的额外磁盘读取。同时，在清除过时数据后，它避免了大量剩余的墓碑标记，这些标记会降低顺序扫描性能。

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 以下修改 TiKV 配置的示例仅适用于 TiDB Self-Managed。对于 TiDB Cloud，Compaction Filter 中的 GC 机制默认启用。

</CustomContent>

以下示例展示如何在 TiKV 配置文件中启用该机制：

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

你也可以通过动态修改配置来启用这个 GC 机制。请参考以下示例：

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
