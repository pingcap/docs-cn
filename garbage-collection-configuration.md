---
title: Garbage Collection Configuration
summary: Learn about GC configuration parameters.
aliases: ['/docs/dev/garbage-collection-configuration/','/docs/dev/reference/garbage-collection/configuration/']
---

# Garbage Collection Configuration

Garbage collection is configured via the following system variables:

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

## GC I/O limit

TiKV supports the GC I/O limit. You can configure `gc.max-write-bytes-per-sec` to limit writes of a GC worker per second, and thus to reduce the impact on normal requests.

`0` indicates disabling this feature.

You can dynamically modify this configuration using tikv-ctl:

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB
```

## Changes in TiDB 5.0

In previous releases of TiDB, garbage collection was configured via the `mysql.tidb` system table. While changes to this table continue to be supported, it is recommended to use the system variables provided. This helps ensure that any changes to configuration can be validated, and prevent unexpected behavior ([#20655](https://github.com/pingcap/tidb/issues/20655)).

The `CENTRAL` garbage collection mode is no longer supported. The `DISTRIBUTED` GC mode (which has been the default since TiDB 3.0) will automatically be used in its place. This mode is more efficient, since TiDB no longer needs to send requests to each TiKV region to trigger garbage collection.

For information on changes in previous releases, refer to earlier versions of this document using the _TIDB version selector_ in the left hand menu.

### GC in Compaction Filter

Based on the `DISTRIBUTED` GC mode, the mechanism of GC in Compaction Filter uses the compaction process of RocksDB, instead of a separate GC worker thread, to run GC. This new GC mechanism helps to avoid extra disk read caused by GC. Also, after clearing the obsolete data, it avoids a large number of left tombstone marks which degrade the sequential scan performance. The following example shows how to enable the mechanism in the TiKV configuration file:

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

You can also enable this GC mechanism by modifying the configuration online. See the following example:

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
