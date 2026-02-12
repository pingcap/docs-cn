---
title: SQL 或事务问题
summary: 学习诊断在应用开发过程中可能产生的 SQL 或事务问题的方法。
aliases: ['/zh/tidb/dev/troubleshoot-overview','/zh/tidb/stable/dev-guide-troubleshoot-overview/','/zh/tidb/dev/dev-guide-troubleshoot-overview/','/zh/tidbcloud/dev-guide-troubleshoot-overview/']
---

# SQL 或事务问题

本章介绍在开发应用过程中可能遇到的常见问题的诊断处理方法。

## SQL 操作常见问题

如果你想提高 SQL 的性能，可以阅读 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)来避免一些常见的性能问题。

然后如果依然存在性能问题，推荐阅读：

<SimpleTab groupId="platform">

<div label="TiDB Cloud" value="tidb-cloud">

- [慢查询](https://docs.pingcap.com/zh/tidbcloud/tune-performance/#慢查询)
- [SQL 语句分析](https://docs.pingcap.com/zh/tidbcloud/tune-performance/#语句分析)
- [Key Visualizer](https://docs.pingcap.com/zh/tidbcloud/tune-performance/#key-visualizer)

</div>

<div label="TiDB" value="tidb">

- [分析慢查询](/analyze-slow-queries.md)
- [使用 Top SQL 定位系统资源消耗过多的查询](/dashboard/top-sql.md)

</div>
</SimpleTab>

如果你遇到了一些关于 SQL 操作的问题，可以阅读 [SQL 操作常见问题](/faq/sql-faq.md)。

## 事务错误处理

见[事务错误处理](/develop/dev-guide-transaction-troubleshoot.md)。

## 推荐阅读

- [不支持的功能特性](/mysql-compatibility.md#不支持的功能特性)
- [集群管理 FAQ](/faq/manage-cluster-faq.md)
- [TiDB Cloud 产品 FAQ](https://docs.pingcap.com/zh/tidbcloud/tidb-cloud-faq)
- [TiDB 产品 FAQ](/faq/tidb-faq.md)
