---
title: TiDB 基础知识
summary: 介绍 TiDB 的基础知识，包括事务机制和应用程序与 TiDB 交互的方式。
aliases: ['/zh/tidb/dev/developer-guide-overview']
---

# TiDB 基础知识

在你开始使用 TiDB 之前，你需要了解一些关于 TiDB 数据库的一些重要工作机制：

- 阅读 [TiDB 事务概览](/transaction-overview.md)来了解 TiDB 的事务运作方式或查看[为应用开发程序员准备的事务说明](/develop/dev-guide-transaction-overview.md)查看应用开发程序员需要了解的事务部分。
- 学习免费在线课程 [TiDB 架构与特点](https://learn.pingcap.cn/learner/course/600003?utm_source=docs-cn-dev-guide)，了解构建 TiDB 分布式数据库集群的核心组件及其概念。
- 了解[应用程序与 TiDB 交互的方式](#应用程序与-tidb-交互的方式)。

## TiDB 事务机制

TiDB 支持分布式事务，而且提供[乐观事务](/optimistic-transaction.md)与[悲观事务](/pessimistic-transaction.md)两种事务模式。TiDB 当前版本中默认采用 **悲观事务** 模式，这让你在 TiDB 事务时可以像使用传统的单体数据库 (如: MySQL) 事务一样。

你可以使用 [`BEGIN`](/sql-statements/sql-statement-begin.md) 开启一个事务，或者使用 `BEGIN PESSIMISTIC` 显式的指定开启一个**悲观事务**，使用 `BEGIN OPTIMISTIC` 显式的指定开启一个**乐观事务**。随后，使用 [`COMMIT`](/sql-statements/sql-statement-commit.md) 提交事务，或使用 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 回滚事务。

TiDB 会为你保证 `BEGIN` 开始到 `COMMIT` 或 `ROLLBACK` 结束间的所有语句的原子性，即在这期间的所有语句全部成功，或者全部失败。用以保证你在应用开发时所需的数据一致性。

若你不清楚**乐观事务**是什么，请暂时不要使用它。因为使用**乐观事务**的前提是需要应用程序可以正确的处理 `COMMIT` 语句所返回的[所有错误](/error-codes.md)。如果不确定应用程序如何处理，请直接使用**悲观事务**。

## 应用程序与 TiDB 交互的方式

TiDB 高度兼容 MySQL 协议，TiDB 支持[大多数 MySQL 的语法及特性](/mysql-compatibility.md)，因此大部分的 MySQL 的连接库都与 TiDB 兼容。如果你的应用程序框架或语言无 PingCAP 的官方适配，那么建议你使用 MySQL 的客户端库。同时，也有越来越多的三方数据库主动支持 TiDB 的差异特性。

因为 TiDB 兼容 MySQL 协议，且兼容 MySQL 语法，因此大多数支持 MySQL 的 ORM 也兼容 TiDB。

## 扩展阅读

- [快速开始](/develop/dev-guide-build-cluster-in-cloud.md)
- [选择驱动或 ORM 框架](/develop/dev-guide-choose-driver-or-orm.md)
- [连接到 TiDB](/develop/dev-guide-connect-to-tidb.md)
- [数据库模式设计](/develop/dev-guide-schema-design-overview.md)
- [数据写入](/develop/dev-guide-insert-data.md)
- [数据读取](/develop/dev-guide-get-data-from-single-table.md)
- [事务](/develop/dev-guide-transaction-overview.md)
- [优化 SQL 性能](/develop/dev-guide-optimize-sql-overview.md)
- [示例程序](/develop/dev-guide-sample-application-java-spring-boot.md)

## 需要帮助？

- 在 [AskTUG 论坛](https://asktug.com/?utm_source=docs-cn-dev-guide) 上提问
- [提交 TiDB Cloud 工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 工单](/support.md)