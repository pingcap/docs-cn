---
title: 连接到 TiDB Cloud Serverless 集群
summary: 了解如何通过不同方法连接到 TiDB Cloud Serverless 集群。
---

# 连接到 TiDB Cloud Serverless 集群

本文档介绍如何连接到 TiDB Cloud Serverless 集群。

> **提示：**
>
> 如需了解如何连接到 TiDB Cloud Dedicated 集群，请参阅[连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

## 连接方法

在 TiDB Cloud 上创建 Serverless 集群后，你可以通过以下方法之一连接到集群：

- 直接连接

  直接连接是指通过 TCP 的 MySQL 原生连接系统。你可以使用任何支持 MySQL 连接的工具（如 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)）连接到 TiDB Cloud Serverless 集群。

- [数据服务（测试版）](/tidb-cloud/data-service-overview.md)

  TiDB Cloud 提供数据服务功能，使你能够通过自定义 API 端点使用 HTTPS 请求连接到 TiDB Cloud Serverless 集群。与直接连接不同，数据服务通过 RESTful API 而不是原始 SQL 访问 TiDB Cloud Serverless 数据。

- [Serverless 驱动（测试版）](/tidb-cloud/serverless-driver.md)

  TiDB Cloud 为 JavaScript 提供 Serverless 驱动，使你能够在边缘环境中以与直接连接相同的体验连接到 TiDB Cloud Serverless 集群。

在上述连接方法中，你可以根据需求选择合适的方法：

| 连接方法           | 用户界面          | 使用场景                                                                                                                                                      |
|-------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 直接连接           | SQL/ORM          | 长期运行的环境，如 Java、Node.js 和 Python。                                                                                                                    |
| 数据服务           | RESTful API      | 所有浏览器和应用程序交互。                                                                                                                                      |
| Serverless 驱动    | SQL/ORM          | Serverless 和边缘环境，如 [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。 |

## 网络

TiDB Cloud Serverless 有两种网络连接类型：

- [私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)（推荐）

    私有端点连接提供一个私有端点，允许你 VPC 中的 SQL 客户端通过 AWS PrivateLink 安全地访问服务。AWS PrivateLink 提供高度安全的单向访问数据库服务，并简化了网络管理。

- [公共端点](/tidb-cloud/connect-via-standard-connection-serverless.md)

  标准连接暴露一个公共端点，因此你可以从笔记本电脑通过 SQL 客户端连接到 TiDB 集群。

  TiDB Cloud Serverless 要求使用 [TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)，这确保了从应用程序到 TiDB 集群的数据传输安全。

下表显示了不同连接方法可以使用的网络：

| 连接方法                  | 网络                        | 说明                                                                                                      |
|--------------------------|----------------------------|----------------------------------------------------------------------------------------------------------|
| 直接连接                  | 公共或私有端点               | 直接连接可以通过公共和私有端点进行。                                                                          |
| 数据服务（测试版）          | /                          | 通过数据服务（测试版）访问 TiDB Cloud Serverless 不需要指定网络类型。                                          |
| Serverless 驱动（测试版）   | 公共端点                    | Serverless 驱动仅支持通过公共端点连接。                                                                     |

## 下一步

成功连接到 TiDB 集群后，你可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
