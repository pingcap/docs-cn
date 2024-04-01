---
title: 通过 SQL 表达式过滤 DML
summary: 增量数据迁移时可通过 SQL 表达式过滤 binlog event，例如不向下游迁移 `DELETE` 事件。从 v2.0.5 起，DM 支持使用 `binlog value filter` 过滤迁移数据。在 `ROW` 格式的 binlog 中，可以基于列的值配置 SQL 表达式。如果表达式结果为 `TRUE`，DM 就不会向下游迁移该条行变更。具体操作步骤和实现细节，请参考如何通过 SQL 表达式过滤 DML。
---

# 通过 SQL 表达式过滤 DML

在进行增量数据迁移时，可以通过[如何过滤 binlog 事件](/filter-binlog-event.md)功能过滤某些类型的 binlog event，例如不向下游迁移 `DELETE` 事件以达到归档、审计等目的。但是 binlog event filter 无法以更细粒度判断某一行的 `DELETE` 事件是否要被过滤。

为了解决上述问题，从 v2.0.5 起，DM 支持在增量数据同步阶段使用`binlog value filter`过滤迁移数据。DM 支持的 `ROW` 格式的 binlog 中，binlog event 带有所有列的值。你可以基于这些值配置 SQL 表达式。如果该表达式对于某条行变更的计算结果是 `TRUE`，DM 就不会向下游迁移该条行变更。

具体操作步骤和实现细节，请参考[如何通过 SQL 表达式过滤 DML](/filter-dml-event.md)。
