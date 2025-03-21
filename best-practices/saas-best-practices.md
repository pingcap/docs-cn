---
title: SaaS 多租户场景最佳实践
summary: 介绍 TiDB 在 SaaS 多租户场景最佳实践。
---

# SaaS 多租户场景最佳实践

本文档介绍 TiDB 在 SaaS 多租户环境中的最佳实践，特别是在**单集群表数量超过百万级别**的情况下。通过合理的配置和选择，使得 TiDB 能够在 SaaS 场景下实现高效、稳定的运行，同时降低资源消耗和成本。

## 最佳实践

### TiDB 版本推荐

推荐使用 8.5 及其之后的版本。

### 硬件配置

* 建议使用高内存规格的 TiDB 实例（例如，100 万张表使用 32GB 或更高内存，300 万张表使用 64GB 或更高内存）。高内存规格的 TiDB 实例可以为 Infoschema、Statistics 和执行计划缓存分配更多的缓存空间，高缓存命中率可以提升业务性能；另外可以有效的缓解 TiDB GC 带来的稳定性问题。
* TiKV：8vCPU 32GiB 或更高。
* PD：8vCPU 16GiB 或更高。

### 控制 Region 数量

如果需要创建大量的表（例如 10 万张以上），建议将 TiDB 的配置  [split-table](/tidb-configuration-file.md#split-table) 设置为 false，减少 Region 数量，降低 TiKV 内存压力。

### 缓存配置

* 从 TiDB v8.4.0 开始，TiDB 在执行 SQL 语句时，会按需将 SQL 语句涉及到的表信息加载到 Infoschema 缓存中。可以通过观测 TiDB 监控中 **Schema Load** 下的 **Infoschema v2 Cache Size** 和 **Infoschema v2 Cache Operation** 子面板来查看 Infoschema 缓存的大小和命中率。用户可以使用 [tidb_schema_cache_size](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入) 系统变量调整 Infoschema 缓存的内存上限以适应其业务需求。Infoschema 缓存使用大小与执行 SQL 语句涉及到的不同表数量呈线性关系。在实际测试中，全量缓存 100 万表（4 columns, 1 primary key, 1 index）的元数据约需 2.4GiB 缓存。
* TiDB 在执行 SQL 语句时，会按需将 SQL 语句涉及到的表统计信息加载到 Statistics 缓存中。可以通过观测 TiDB 监控中 **Statistics & Plan Management** 下的 **Stats Cache Cost** 和 **Stats Cache OPS** 子面板来查看 Statistics 缓存的大小和命中率。用户可以使用 [tidb_stats_cache_mem_quota](/system-variables.md#tidb_stats_cache_mem_quota-从-v610-版本开始引入) 系统变量调整 Statistics 缓存的内存上限以适应其业务需求。在实际测试中，执行 10 万张表的简单 SQL（使用 IndexRangeScan 操作符）时，Stats 缓存成本约为 3.96GB。

### 统计信息收集

从 TiDB v8.4.0 开始，TiDB 引入了 [tidb_auto_analyze_concurrency](/system-variables.md#tidb_auto_analyze_concurrency-从-v840-版本开始引入) 系统变量用来控制单个自动统计信息收集任务内部的并发度。多表场景下，你可以按需提升该并发度，以提高自动分析的吞吐量。随着并发值的增加，自动分析的吞吐量和 TiDB Owner 节点的 CPU 使用率会线性增加。在实际测试中，使用并发值 16，可以在一分钟内自动分析 320 张表（每张表有 1 万行数据、4 列和 1 个索引），消耗 TiDB Owner 节点一个 CPU 核心资源。

### 系统表查询

在系统表的查询中添加 TABLE_SCHEMA 和 TABLE_NAME 或 TIDB_TABLE_ID 等条件，避免扫描集群中大量的数据库和表信息，从而提高查询速度并减少资源消耗。例如在 300 万表的场景下，执行 `select count(*) from information_schema.tables` 消耗约 8GB 内存；执行 `select count(*) from information_schema.views` 需要约 20 分钟。


### 大量链接场景

SAAS 多租户场景中，每个用户连接到 TiDB 来操作自己租户(database) 中的数据。为了节省成本，用户希望 TiDB 节点能够支持尽可能多的连接。
* 调高 TiDB 的配置 [token-limit](/tidb-configuration-file.md#token-limit)（默认 1000）以支持更多并发请求。
* TiDB 的内存使用量与连接数量基本上呈线性关系。在实际测试中，20 万个空闲连接时，TiDB 进程内存增加约 30GB。建议调大 TiDB 内存规格。
* 如果用户使用 PREPARED 语句，每个连接都会维护一个会话级的 Prepared Plan Cache。在实际使用中，用户可能长时间不 DEALLOCATE 预编译语句，这可能导致预编译语句的 Execute 语句的 QPS 不高，但计划缓存中的计划数量相对较高。计划缓存所占用的内存量与计划缓存中的计划数量呈线性关系。在实际测试中，40 万个涉及 IndexRangeScan 的执行计划约消耗 5GiB TiDB 内存。建议调大 TiDB 内存规格。

### Stale Read

使用 stale read 时候，如果使用的 schema version 过于陈旧，可能会导致历史 schema 的全量加载，从而对性能产生显著影响。可以通过增加[tidb_schema_version_cache_limit](/system-variables.md#tidb_schema_version_cache_limit-从-v740-版本开始引入) 的值（例如255）来缓解此问题。

### BR 备份恢复

* 在全量恢复百万表的场景中，我们建议使用高内存 BR 实例。例如，100 万表恢复建议使用 32GiB 及其以上内存 BR 实例，300 万表恢复建议使用 64GiB 及其以上内存 BR 实例。
* BR 日志备份和快照恢复会额外消耗 TiKV 内存，建议 TiKV 使用 32 GiB 或更高规格的内存。
* 可根据业务需求，适当增加 BR 的 pitr-batch-count 和 pitr-concurrency 配置以提升 BR 日志恢复速度。

### Lighting 数据导入
在使用 Lightning 导入百万表数据的场景中，我们建议对大表（如超过 100GB 的表，通常数量较少）使用 Lightning 物理导入模式，对小表（通常数量较多）使用 Lightning 逻辑导入模式。