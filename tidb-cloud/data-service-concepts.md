---
title: 数据服务（Beta）
summary: 了解 TiDB Cloud 的数据服务概念。
---

# 数据服务（Beta）

TiDB Cloud [数据服务（beta）](https://tidbcloud.com/project/data-service)是一个完全托管的低代码后端即服务解决方案，它简化了后端应用程序开发，使开发人员能够快速构建高度可扩展、安全的数据驱动应用程序。

数据服务使你能够通过自定义 API 端点使用 HTTPS 请求访问 TiDB Cloud 数据。此功能使用无服务器架构来处理计算资源和弹性扩展，因此你可以专注于端点中的查询逻辑，而无需担心基础设施或维护成本。

更多信息，请参阅 [TiDB Cloud 数据服务（Beta）概述](/tidb-cloud/data-service-overview.md)。

## 数据应用

[数据服务（beta）](https://tidbcloud.com/project/data-service)中的数据应用是一组可用于访问特定应用程序数据的端点的集合。通过创建数据应用，你可以对端点进行分组，并使用 API 密钥配置授权设置来限制对端点的访问。这样，你可以确保只有授权用户才能访问和操作你的数据，使你的应用程序更加安全。

更多信息，请参阅[管理数据应用](/tidb-cloud/data-service-manage-data-app.md)。

## 数据应用端点

[数据服务（beta）](https://tidbcloud.com/project/data-service)中的端点是一个可以自定义来执行 SQL 语句的 Web API。你可以为 SQL 语句指定参数，例如在 `WHERE` 子句中使用的值。当客户端调用端点并在请求 URL 中为参数提供值时，端点会使用提供的参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

更多信息，请参阅[管理端点](/tidb-cloud/data-service-manage-endpoint.md)。

## Chat2Query API

在 TiDB Cloud 中，Chat2Query API 是一个 RESTful 接口，通过提供指令，使你能够使用 AI 生成和执行 SQL 语句。然后，API 会为你返回查询结果。

更多信息，请参阅[开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## AI 集成

将第三方工具与你的数据应用集成可以通过第三方工具提供的高级自然语言处理和人工智能（AI）功能来增强你的应用程序。这种集成使你的应用程序能够执行更复杂的任务并提供智能解决方案。

目前，你可以在 TiDB Cloud 控制台中集成第三方工具，如 GPTs 和 Dify。

更多信息，请参阅[将数据应用与第三方工具集成](/tidb-cloud/data-service-integrations.md)。

## 配置即代码

TiDB Cloud 提供了配置即代码（Configuration as Code，CaC）方法，使用 JSON 语法将你的整个数据应用配置表示为代码。

通过将你的数据应用连接到 GitHub，TiDB Cloud 可以使用 CaC 方法，将你的数据应用配置作为[配置文件](/tidb-cloud/data-service-app-config-files.md)推送到你首选的 GitHub 仓库和分支。

如果为你的 GitHub 连接启用了自动同步和部署，你还可以通过在 GitHub 上更新配置文件来修改你的数据应用。将配置文件更改推送到 GitHub 后，新的配置将自动部署到 TiDB Cloud。

更多信息，请参阅[使用 GitHub 自动部署数据应用](/tidb-cloud/data-service-manage-github-connection.md)。
