---
title: GC 配置
aliases: ['/docs-cn/dev/garbage-collection-configuration/','/docs-cn/dev/reference/garbage-collection/configuration/']
---

# GC 配置

你可以通过以下系统变量进行 GC 配置：

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-从-v50-版本开始引入)
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-从-v50-版本开始引入)
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入)
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)

## 流控

TiDB 支持 GC 流控，可通过配置 `gc.max-write-bytes-per-sec` 限制 GC worker 每秒数据写入量，降低对正常请求的影响，`0` 为关闭该功能。该配置可通过 tikv-ctl 动态修改：

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB
```

## TiDB 5.0 引入的变化

在 TiDB 5.0 之前的版本中，GC 是通过系统表 `mysql.tidb` 进行配置的。从 TiDB 5.0 版本起，GC 仍然可以通过系统表 `mysql.tidb` 进行配置，但建议你使用系统变量进行配置，这样可以确保对配置的任何更改都能得到验证，防止造成异常行为 ([#20655](https://github.com/pingcap/tidb/issues/20655))。

TiDB 5.0 及之后的版本不再需要向各个 TiKV Region 都发送触发 GC 的请求，因此不再提供 `CENTRAL` GC 模式的支持，取而代之的是效率更高的 `DISTRIBUTED` GC 模式 （自 TiDB 3.0 起的默认 GC 模式）。

如果要了解 TiDB 历史版本中 GC 配置的变化信息，请使用左侧导航栏中的 _"TIDB 版本选择器"_ 切换到本文档的历史版本。

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
