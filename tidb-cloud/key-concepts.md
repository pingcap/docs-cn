---
title: 关键概念概述
summary: 了解 TiDB Cloud 中的关键概念。
---

# 关键概念概述

本文档提供了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 中关键概念的概述。理解这些概念有助于您更好地使用 TiDB Cloud 的功能和特性。

## 架构

TiDB Cloud 基于云原生分布式架构构建，实现了计算与存储分离，从而支持弹性扩展和高可用性。[了解更多 TiDB Cloud 架构信息](/tidb-cloud/architecture-concepts.md)。

## 数据库模式

TiDB Cloud 使您能够使用数据库、表、列、索引和约束等对象来组织和构建数据。它还支持临时表、向量索引和缓存表等高级功能。[了解更多数据库模式信息](/tidb-cloud/database-schema-concepts.md)。

## 事务

TiDB 提供完整的分布式事务支持，其模型在 [Google Percolator](https://research.google.com/pubs/pub36726.html) 的基础上进行了一些优化。[了解更多事务信息](/tidb-cloud/transaction-concepts.md)。

## SQL

TiDB 高度兼容 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法。[了解更多 TiDB Cloud 中的 SQL 信息](/tidb-cloud/sql-concepts.md)。

## AI 功能

TiDB Cloud 中的 AI 功能使您能够充分利用先进技术进行数据探索、搜索和集成。[了解更多 AI 功能信息](/tidb-cloud/ai-feature-concepts.md)。

## 数据服务（Beta）

数据服务使您能够通过自定义 API 端点使用 HTTPS 请求访问 TiDB Cloud 数据。[了解更多数据服务信息](/tidb-cloud/data-service-concepts.md)。

## 可扩展性

TiDB Cloud Dedicated 让您可以根据数据量或工作负载的变化分别调整其计算和存储资源。[了解更多可扩展性信息](/tidb-cloud/scalability-concepts.md)。

## 高可用性

TiDB Cloud 在 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群中都确保高可用性：

- [TiDB Cloud Serverless 中的高可用性](/tidb-cloud/serverless-high-availability.md)
- [TiDB Cloud Dedicated 中的高可用性](/tidb-cloud/high-availability-with-multi-az.md)

## 监控

TiDB Cloud 为集群性能和健康状况提供全面的监控功能。[了解更多监控信息](/tidb-cloud/monitoring-concepts.md)。

## 数据流

TiDB Cloud 允许您将数据变更从 TiDB 集群流式传输到 Kafka、MySQL 和对象存储等其他系统。[了解更多数据流信息](/tidb-cloud/data-streaming-concepts.md)。

## 备份和恢复

TiDB Cloud 提供自动备份解决方案和时间点恢复（PITR）功能。[了解更多备份和恢复信息](/tidb-cloud/backup-and-restore-concepts.md)。

## 安全性

TiDB Cloud 提供了一个强大而灵活的安全框架，旨在保护数据、执行访问控制并满足现代合规标准。[了解更多安全性信息](/tidb-cloud/security-concepts.md)。
