---
title: SQL or Transaction Issues
summary: Learn how to troubleshoot SQL or transaction issues that might occur during application development.
---

# SQL or Transaction Issues

This document introduces problems that may occur during application development and related documents.

## Troubleshoot SQL query problems

If you want to improve SQL query performance, follow the instructions in [SQL Performance Tuning](/develop/dev-guide-optimize-sql-overview.md) to solve performance problems such as full table scans and missing indexes.

<CustomContent platform="tidb">

If you still have performance issues, see the following documents:

- [Analyze Slow Queries](/analyze-slow-queries.md)
- [Identify Expensive Queries Using Top SQL](/dashboard/top-sql.md)

If you have questions about SQL operations, see [SQL FAQs](/faq/sql-faq.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

If you have questions about SQL operations, see [SQL FAQs](https://docs.pingcap.com/tidb/stable/sql-faq).

</CustomContent>

## Troubleshoot transaction issues

See [Handle transaction errors](/develop/dev-guide-transaction-troubleshoot.md).

## See also

- [Unsupported features](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

- [Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [TiDB FAQs](/faq/tidb-faq.md)

</CustomContent>
