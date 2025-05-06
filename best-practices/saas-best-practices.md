---
title: SaaS 多租户场景最佳实践
summary: 介绍 TiDB 在 SaaS (Software as a service) 多租户场景的最佳实践，特别适用于单集群表数量超过百万级别的场景。
---

# SaaS 多租户场景最佳实践

本文档介绍 TiDB 在 SaaS (Software as a service) 多租户环境中的最佳实践，特别适用于**单集群表数量超过百万级别**的场景。通过合理的配置和选择，可以实现 TiDB 在 SaaS 场景下的高效稳定运行，同时降低资源消耗和成本。

> **注意：**
> 
> 推荐使用 TiDB v8.5.0 及以上版本。

## 硬件配置建议

建议使用高内存规格的 TiDB 实例，例如：

- 100 万张表：使用 32 GiB 或更高内存。
- 300 万张表：使用 64 GiB 或更高内存。

高内存规格的 TiDB 实例可以为 Infoschema、Statistics 和执行计划缓存分配更多的缓存空间，提高缓存命中率，从而提升业务性能。同时，更大的内存可以缓解 TiDB GC 带来的性能波动和稳定性问题。

TiKV 和 PD 推荐的硬件配置如下：

* **TiKV**：8 vCPU 和 32 GiB 或更高内存。
* **PD**：8 CPU 和 16 GiB 或更高内存。

## 控制 Region 数量

如果需要创建大量的表（例如 10 万张以上），建议将 TiDB 的配置 [`split-table`](/tidb-configuration-file.md#split-table) 设置为 `false`，减少集群 Region 数量，从而降低 TiKV 内存压力。

## 缓存配置

* 从 TiDB v8.4.0 开始，TiDB 在执行 SQL 语句时，会按需将 SQL 语句涉及的表信息加载到 Infoschema 缓存中。

    * 通过 TiDB 监控中 **Schema Load** 面板下的 **Infoschema v2 Cache Size** 和 **Infoschema v2 Cache Operation** 子面板，可以查看 Infoschema 缓存的大小和命中率。
    * 使用系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入) 可以调整 Infoschema 缓存的内存上限，以满足业务需求。Infoschema 缓存大小与执行 SQL 语句涉及的不同表数量呈线性关系。在实际测试中，全量缓存 100 万张表（每张表含 4 列、1 个主键和 1 个索引）的元数据大约需要 2.4 GiB 内存。

* TiDB 在执行 SQL 语句时，也会按需将相关表的统计信息加载到 Statistics 缓存中。

    * 通过 TiDB 监控中 **Statistics & Plan Management** 面板下的 **Stats Cache Cost** 和 **Stats Cache OPS** 子面板，可以查看 Statistics 缓存的使用情况。
    * 使用系统变量 [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-从-v610-版本开始引入) 可以调整 Statistics 缓存的内存上限，以满足业务需求。在实际测试中，执行 10 万张表的简单 SQL（使用 IndexRangeScan 操作符）时，Statistics 缓存大约消耗 3.96 GiB 内存。

## 统计信息收集

* 从 TiDB v8.4.0 开始，TiDB 引入了 [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-从-v840-版本开始引入) 系统变量，用来设置 TiDB 集群中自动更新统计信息操作的并发度。多表场景下，适当提升并发度可提高自动分析吞吐量。随着并发值的增加，自动分析的吞吐量和 TiDB Owner 节点的 CPU 使用率会线性增加。在实际测试中，使用并发度 16 时，每分钟可自动分析 320 张表（每张表有 1 万行数据、4 列和 1 个索引），占用 TiDB Owner 节点一个 CPU 核心。
* [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-从-v650-版本开始引入) 和 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入) 影响 TiDB 统计信息构建的并发度，需根据具体场景调整：
    - 分区表较多时，优先提高 `tidb_auto_build_stats_concurrency` 的值。
    - 列数较多时，优先提高 `tidb_build_sampling_stats_concurrency` 的值。
* 建议确保 `tidb_auto_analyze_concurrency`、`tidb_auto_build_stats_concurrency` 和 `tidb_build_sampling_stats_concurrency` 三个变量的值的乘积不超过 TiDB CPU 核心数，避免过度占用资源。

## 系统表查询

在查询系统表时，建议添加 `TABLE_SCHEMA` 和 `TABLE_NAME` 或 `TIDB_TABLE_ID` 等过滤条件，以避免扫描大量无关数据，从而提高查询速度并降低资源消耗。

例如，在 300 万表的场景下：

- 执行以下 SQL 语句要消耗约 8 GiB 内存：

    ```sql
    SELECT COUNT(*) FROM information_schema.tables;
    ```

- 执行以下 SQL 语句需要约 20 分钟：

    ```sql
    SELECT COUNT(*) FROM information_schema.views;
    ```

在以上示例中的两个 SQL 语句加上建议的查询条件之后，内存消耗可以忽略不计，查询耗时降至毫秒级别。

## 大量连接场景

在 SaaS 多租户场景中，通常每个用户连接到 TiDB 操作各自租户 (database) 的数据。为支持更多连接数，建议：

* 调高 TiDB 的配置项 [`token-limit`](/tidb-configuration-file.md#token-limit)（默认值为 `1000`）以支持更多并发请求。
* TiDB 内存使用量与连接数基本上呈线性关系。在实际测试中，20 万个空闲连接将使 TiDB 进程增加约 30 GiB 内存。建议根据实际连接数调整 TiDB 内存规格。
* 使用 `PREPARED` 语句时，每个连接都会维护一个会话级的 Prepared Plan Cache。如果长时间未执行 `DEALLOCATE` 预编译语句，可能导致缓存中的计划数量过多，增加内存消耗。在实际测试中，40 万条涉及 IndexRangeScan 的执行计划占用约 5 GiB 内存。建议相应提高内存规格。

## Stale Read

使用 [Stale Read](/stale-read.md) 时，如果使用的 schema 版本过于陈旧，可能触发历史 schema 全量加载，影响性能。建议通过提高 [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-从-v740-版本开始引入) 的值（例如 `255`）来缓解此问题。

## BR 备份恢复

* 在全量恢复百万张表的场景中，建议使用高内存 BR 实例。例如：
    - 100 万张表：使用 32 GiB 或更高内存的 BR 实例
    - 300 万张表：使用 64 GiB 或更高内存的 BR 实例
* BR 日志备份和快照恢复会额外消耗 TiKV 内存，建议 TiKV 使用 32 GiB 或更高规格的内存。
* 可根据业务需求，适当增加 BR 的 [`pitr-batch-count` 和 `pitr-concurrency`](/br/use-br-command-line-tool.md#常用选项) 配置以提升 BR 日志恢复速度。

## TiDB Lightning 数据导入

在使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 导入百万张表数据时，建议：

- 对大表（超过 100 GiB）使用 TiDB Lightning [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)。
- 对小表（通常数量较多）使用 TiDB Lightning [逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)。
