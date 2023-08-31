---
title: TiDB Cloud Data Service (Beta) Overview
summary: Learn about Data Service in TiDB Cloud and its scenarios.
---

# TiDB Cloud Data Service (Beta) Overview

TiDB Cloud provides a [Data Service (beta)](https://tidbcloud.com/console/data-service) feature that enables you to access TiDB Cloud data via an HTTPS request using a custom API endpoint. This feature uses a serverless architecture to handle computing resources and elastic scaling, so you can focus on the query logic in endpoints without worrying about infrastructure or maintenance costs.

> **Note:**
>
> Data Service is available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters. To use Data Service in TiDB Dedicated clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

An endpoint in Data Service is a web API that you can customize to execute SQL statements. You can specify parameters for your SQL statements, such as the value used in the `WHERE` clause. When a client calls an endpoint and provides values for the parameters in a request URL, the endpoint executes the corresponding SQL statement with the provided parameters and returns the results as part of the HTTP response.

To manage endpoints more efficiently, you can use Data Apps. A Data App in Data Service is a collection of endpoints that you can use to access data for a specific application. By creating a Data App, you can group your endpoints and configure authorization settings using API keys to restrict access to endpoints. In this way, you can ensure that only authorized users can access and manipulate your data, making your application more secure.

> **Tip:**
>
> TiDB Cloud provides a Chat2Query API for TiDB clusters. After it is enabled, TiDB Cloud will automatically create a system Data App called **Chat2Query** and a Chat2Data endpoint in Data Service. You can call this endpoint to let AI generate and execute SQL statements by providing instructions.
>
> For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

## Scenarios

Data Service allows you to seamlessly integrate TiDB Cloud with any application or service that is compatible with HTTPS. The following are some typical usage scenarios:

- Access the database of your TiDB cluster directly from a mobile or web application.
- Use serverless edge functions to call endpoints and avoid scalability issues caused by database connection pooling.
- Integrate TiDB Cloud with data visualization projects by using Data Service as a data source. This avoids exposing your database connection username and password, making your API more secure and easier to use.
- Connect to your database from an environment that the MySQL interface does not support. This provides more flexibility and options for you to access data.

## What's next

- [Get Started with Data Service](/tidb-cloud/data-service-get-started.md)
- [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md)
- [Manage an Endpoint](/tidb-cloud/data-service-manage-endpoint.md)
