---
title: schema 缓存
aliases: ['/docs-cn/dev/information-schema-cache']
summary: TiDB 对于 schema 信息采用缓存机制，在大量数据库和表的场景下能够显著减少 schema 信息的内存占用以及提高性能。
---

# schema 缓存

在一些多租户的场景下，可能会存在几十万甚至上百万个数据库和表。这些数据库和表的 schema 信息如果全部加载到内存中，一方面会占用大量的内存，另一方面会导致相关的访问性能变差。为了解决这个问题，TiDB 引入了 schema 缓存机制。采用类似于 LRU 的机制，只将最近用到的数据库和表的 schema 信息缓存到内存中。

## 配置

可以通过配置系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入) 来打开 schema 缓存特性。

## 最佳实践

- 在大量数据库和表的场景下（例如10万以上的数据库和表数量）或者当数据库和表的数量大到影响系统性能时，建议打开 schema 缓存特性。
- 可以通过观测 TiDB 监控中 Schema load 下的子面板 Infoschema v2 Cache Operation 来查看 schema 缓存的命中率。如果命中率较低，可以调大 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)。
- 可以通过观测 TiDB 监控中 Schema load 下的子面板 Infoschema v2 Cache Size 来查看当前使用的 schema 缓存的大小。
- 建议关闭 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 以减少 TiDB 的启动时间。
- 建议关闭 [`split-table`](/tidb-configuration-file.md#split-table) 以减少 region 数量，从而降低 TiKV 的内存。

## 已知限制

- 在大量数据库和表的场景下，统计信息不一定能够及时收集。
- 在大量数据库和表的场景下，一些元数据信息的访问会变慢。
- 在大量数据库和表的场景下，TiDB 的启动时间会变长。开启 schema 缓冲能够缓解这个问题。
- 在大量数据库和表的场景下，切换 schema 缓存开关需要等待一段时间。
- 在大量数据库和表的场景下，全量列举所有元数据信息的相关操作会变慢，如：
    - `SHOW FULL TABLES`
    - `FLASHBACK`
    - `ALTER TABLE ... SET TIFLASH MODE ...`
