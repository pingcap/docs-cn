---
title: TiDB Cloud 数据服务（Beta）概述
summary: 了解 TiDB Cloud 中的数据服务及其应用场景。
---

# TiDB Cloud 数据服务（Beta）概述

TiDB Cloud [数据服务（beta）](https://tidbcloud.com/project/data-service)是一个完全托管的低代码后端即服务解决方案，它简化了后端应用程序开发，使开发人员能够快速构建高度可扩展、安全的数据驱动应用程序。

数据服务使你能够通过使用自定义 API 端点的 HTTPS 请求访问 TiDB Cloud 数据。此功能使用无服务器架构来处理计算资源和弹性扩展，因此你可以专注于端点中的查询逻辑，而无需担心基础设施或维护成本。

> **注意：**
>
> 数据服务适用于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。要在 TiDB Cloud Dedicated 集群中使用数据服务，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

数据服务中的端点是一个可以自定义执行 SQL 语句的 Web API。你可以为 SQL 语句指定参数，例如在 `WHERE` 子句中使用的值。当客户端调用端点并在请求 URL 中为参数提供值时，端点会使用提供的参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

为了更有效地管理端点，你可以使用数据应用。数据服务中的数据应用是一组可用于访问特定应用程序数据的端点的集合。通过创建数据应用，你可以对端点进行分组，并使用 API 密钥配置授权设置来限制对端点的访问。这样，你可以确保只有授权用户才能访问和操作你的数据，使你的应用程序更加安全。

> **提示：**
>
> TiDB Cloud 为 TiDB 集群提供了 Chat2Query API。启用后，TiDB Cloud 将在数据服务中自动创建一个名为 **Chat2Query** 的系统数据应用和一个 Chat2Data 端点。你可以调用此端点，通过提供指令让 AI 生成并执行 SQL 语句。
>
> 更多信息，请参见[开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 应用场景

数据服务允许你将 TiDB Cloud 与任何支持 HTTPS 的应用程序或服务无缝集成。以下是一些典型的使用场景：

- 从移动或 Web 应用程序直接访问 TiDB 集群的数据库。
- 使用无服务器边缘函数调用端点，避免数据库连接池导致的可扩展性问题。
- 通过使用数据服务作为数据源将 TiDB Cloud 与数据可视化项目集成。这避免了暴露数据库连接用户名和密码，使你的 API 更安全且更易于使用。
- 从不支持 MySQL 接口的环境连接到数据库。这为你访问数据提供了更多的灵活性和选择。

## 下一步

- [开始使用数据服务](/tidb-cloud/data-service-get-started.md)
- [开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [管理数据应用](/tidb-cloud/data-service-manage-data-app.md)
- [管理端点](/tidb-cloud/data-service-manage-endpoint.md)
