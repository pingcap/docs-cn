---
title: Data Migration API 概览
summary: 了解 Data Migration (DM) 的 API。
---

# Data Migration API 概览

[TiDB Data Migration](/dm/dm-overview.md) (DM) 是一款便捷的数据迁移工具，支持从与 MySQL 协议兼容的数据库（例如 MySQL、MariaDB、Aurora MySQL）到 TiDB 的全量数据迁移和增量数据同步。

DM 提供了用于查询与操作 DM 集群的 OpenAPI，其功能范围与 [dmctl 工具](/dm/dmctl-introduction.md)相当。

你可以使用 DM API 对 DM 集群执行以下运维操作：

- [集群管理](/dm/dm-open-api.md#集群相关-api)：获取 DM-master 与 DM-worker 节点信息，或下线相应节点。
- [数据源管理](/dm/dm-open-api.md#数据源相关-api)：创建、更新、删除、启用或停用数据源，管理 relay-log 功能，更新数据源与 DM-worker 的绑定关系。
- [同步任务管理](/dm/dm-open-api.md#同步任务相关-api)：创建、更新、删除、开始或停止同步任务；管理 schema 与迁移规则。

关于各个 API 的请求参数、响应示例与使用说明，请参阅[使用 OpenAPI 运维 TiDB Data Migration 集群](/dm/dm-open-api.md)。
