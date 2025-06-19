---
title: SQL 性能优化概述
summary: 为 TiDB 应用程序开发人员提供 SQL 性能调优的概述。
---

# SQL 性能优化概述

本文介绍如何在 TiDB 中优化 SQL 语句的性能。要获得良好的性能，您可以从以下方面入手：

* SQL 性能调优
* 模式设计：根据您的应用程序工作负载模式，您可能需要更改表模式以避免事务冲突或热点。

## SQL 性能调优

要获得良好的 SQL 语句性能，您可以遵循以下准则：

* 扫描尽可能少的行。建议只扫描您需要的数据，避免扫描多余的数据。
* 使用正确的索引。确保 SQL 中 `WHERE` 子句中的列有相应的索引。如果没有，语句会进行全表扫描，从而导致性能不佳。
* 使用正确的连接类型。根据查询中涉及的表的相对大小选择正确的连接类型很重要。通常，TiDB 的基于成本的优化器会选择性能最佳的连接类型。但是，在少数情况下，您可能需要手动指定更好的连接类型。
* 使用正确的存储引擎。对于混合 OLTP 和 OLAP 工作负载，建议使用 TiFlash 引擎。详情请参见 [HTAP 查询](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)。

## 模式设计

在[调优 SQL 性能](#sql-性能调优)之后，如果您的应用程序仍然无法获得良好的性能，您可能需要检查您的模式设计和数据访问模式，以避免以下问题：

<CustomContent platform="tidb">

* 事务冲突。有关如何诊断和解决事务冲突，请参见[排查锁冲突问题](/troubleshoot-lock-conflicts.md)。
* 热点。有关如何诊断和解决热点问题，请参见[排查热点问题](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* 事务冲突。有关如何诊断和解决事务冲突，请参见[排查锁冲突问题](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。
* 热点。有关如何诊断和解决热点问题，请参见[排查热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)。

</CustomContent>

### 另请参阅

<CustomContent platform="tidb">

* [SQL 性能调优](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [SQL 性能调优](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
