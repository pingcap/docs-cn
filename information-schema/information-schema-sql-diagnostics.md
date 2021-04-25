---
title: SQL 诊断
summary: 了解 SQL 诊断功能。
aliases: ['/docs-cn/stable/system-tables/system-table-sql-diagnostics/','/docs-cn/v4.0/system-tables/system-table-sql-diagnostics/','/docs-cn/stable/reference/system-databases/sql-diagnosis/','/docs-cn/stable/system-tables/system-table-sql-diagnosis/','/zh/tidb/stable/check-cluster-status-using-sql-statements','/docs-cn/stable/reference/performance/check-cluster-status-using-sql-statements/','/zh/tidb/stable/system-table-sql-diagnostics/','/docs-cn/stable/check-cluster-status-using-sql-statements/','/zh/tidb/v4.0/check-cluster-status-using-sql-statements','/zh/tidb/v4.0/system-table-sql-diagnostics/']
---

# SQL 诊断

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。

SQL 诊断功能是在 TiDB 4.0 版本中引入的特性，用于提升 TiDB 问题定位的效率。TiDB 4.0 版本以前，用户需要使用不同的工具以异构的方式获取不同信息。新的 SQL 诊断系统对这些离散的信息进行了整体设计，它整合系统各个维度的信息，通过系统表的方式向上层提供一致的接口，提供监控汇总与自动诊断，方便用户查询集群信息。

SQL 诊断共分三大块：

* **集群信息表**：TiDB 4.0 诊断系统添加了集群信息表，为原先离散的各实例信息提供了统一的获取方式。它将整个集群的集群拓扑、硬件信息、软件信息、内核参数、监控、系统信息、慢查询、语句、日志完全整合在表中，让用户能够统一使用 SQL 进行查询。
* **集群监控表**：TiDB 4.0 诊断系统添加了集群监控系统表，所有表都在 `metrics_schema` 中，可以通过 SQL 语句来查询监控信息。比起原先的可视化监控，SQL 查询监控允许用户对整个集群的所有监控进行关联查询，并对比不同时间段的结果，迅速找出性能瓶颈。由于 TiDB 集群的监控指标数量较大，SQL 诊断还提供了监控汇总表，让用户能够更便捷地从众多监控中找出异常的监控项。
* **自动诊断**：尽管用户可以手动执行 SQL 来查询集群信息表、集群监控表与汇总表来定位问题，但自动诊断可以快速对常见异常进行定位。SQL 诊断基于已有的集群信息表和监控表，提供了与之相关的诊断结果表与诊断汇总表来执行自动诊断。

## 集群信息表

集群信息表将一个集群中的所有实例的信息都汇聚在一起，让用户仅通过一条 SQL 就能查询整个集群相关信息。集群信息表列表如下：

* 集群拓扑表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 用于获取集群当前的拓扑信息，以及各个实例的版本、版本对应的 Git Hash、各实例的启动时间、各实例的运行时间。
* 集群配置表 [`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md) 用于获取集群当前所有实例的配置。对于 TiDB 4.0 之前的版本，用户必须逐个访问各个实例的 HTTP API 才能获取这些配置信息。
* 集群硬件表 [`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md) 用于快速查询集群硬件信息。
* 集群负载表 [`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md) 用于查询集群不同实例以及不同硬件类型的负载信息。
* 内核参数表 [`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md) 用于查询集群不同实例的内核配置信息。目前支持查询 sysctl 的信息。
* 集群日志表 [`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md) 用于集群日志查询，通过将查询条件下推到各个实例，降低日志查询对集群的影响，性能影响小于等 grep 命令。

TiDB 4.0 之前的系统表，只能查看当前实例信息，TiDB 4.0 实现了对应的集群表，可以在单个 TiDB 实例上拥有整个集群的全局视图。这些表目前都位于 `information_schema` 中，查询方式与其他 `information_schema` 系统表一致。

## 集群监控表

为了能够动态地观察并对比不同时间段的集群情况，TiDB 4.0 诊断系统添加了集群监控系统表。所有监控表都在 `metrics_schema` 中，可以通过 SQL 的方式查询监控信息。SQL 查询监控允许用户对整个集群的所有监控进行关联查询，并对比不同时间段的结果，迅速找出性能瓶颈。

* [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md)：由于目前添加的系统表数量较多，因此用户可以通过该表查询这些监控表的相关元信息。

由于 TiDB 集群的监控指标数量较大，因此 TiDB 4.0 提供以下监控汇总表：

* 监控汇总表 [`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md) 用于汇总所有监控数据，以提升用户排查各监控指标的效率。
* 监控汇总并按 label 聚合表 [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) 同样用于汇总所有监控数据，但该表会对各项监控的不同的 label 进行聚合统计。

## 自动诊断

以上集群信息表和集群监控表均需要用户手动执行 SQL 语句来排查集群问题。TiDB 4.0 中添加了自动诊断功能，根据已有的基础信息表，提供诊断相关的系统表，使诊断自动执行。自动诊断相关的系统表如下：

* 诊断结果表 [`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md) 用于展示对系统的诊断结果。诊断是惰性触发，使用 `select * from inspection_result` 会触发所有诊断规则对系统进行诊断，并在结果中展示系统中的故障或风险。
* 诊断汇总表 [`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md) 用于对特定链路或模块的监控进行汇总，用户可以根据整个模块或链路的上下文来排查定位问题。
