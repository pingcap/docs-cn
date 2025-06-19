---
title: SQL 或事务问题
summary: 了解如何排查应用程序开发过程中可能出现的 SQL 或事务问题。
---

# SQL 或事务问题

本文介绍应用程序开发过程中可能出现的问题和相关文档。

## 排查 SQL 查询问题

如果您想提高 SQL 查询性能，请按照 [SQL 性能调优](/develop/dev-guide-optimize-sql-overview.md) 中的说明解决全表扫描和缺少索引等性能问题。

<CustomContent platform="tidb">

如果您仍然遇到性能问题，请参见以下文档：

- [分析慢查询](/analyze-slow-queries.md)
- [使用 Top SQL 识别高开销查询](/dashboard/top-sql.md)

如果您对 SQL 操作有疑问，请参见 [SQL 常见问题](/faq/sql-faq.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果您对 SQL 操作有疑问，请参见 [SQL 常见问题](https://docs.pingcap.com/tidb/stable/sql-faq)。

</CustomContent>

## 排查事务问题

请参见[处理事务错误](/develop/dev-guide-transaction-troubleshoot.md)。

## 另请参阅

- [不支持的功能](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

- [集群管理常见问题](/faq/manage-cluster-faq.md)
- [TiDB 常见问题](/faq/tidb-faq.md)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
