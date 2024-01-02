---
title: Connect to Your TiDB Serverless Cluster
summary: Learn how to connect to your TiDB Serverless cluster via different methods.
---

# Connect to Your TiDB Serverless Cluster

This document describes how to connect to your TiDB Serverless cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster, see [Connect to Your TiDB Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

## Connection methods

After your TiDB Serverless cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- Direct connections

  Direct connections mean the MySQL native connection system over TCP. You can connect to your TiDB Serverless cluster using any tool that supports MySQL connection, such as [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html).

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Cloud provides a Data Service feature that enables you to connect to your TiDB Serverless cluster via an HTTPS request using a custom API endpoint. Unlike direct connections, Data Service accesses TiDB Serverless data via a RESTful API rather than raw SQL.

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Cloud provides a serverless driver for JavaScript, which allows you to connect to your TiDB Serverless cluster in edge environments with the same experience as direct connections.

In the preceding connection methods, you can choose your desired one based on your needs:

| Connection method  | User interface     | Scenario                                                                                                                                                       |
|--------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Direct connections | SQL/ORM            | Long-running environment, such as Java, Node.js, and Python.                                                                                                   |
| Data Service       | RESTful API        | All browser and application interactions.                                                                                                                      |
| Serverless Driver  | SQL/ORM            | Serverless and edge environments such as [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) and [Cloudflare Workers](https://workers.cloudflare.com/). |

## Network

There are two network connection types for TiDB Serverless:

- [Private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  The standard connection exposes a public endpoint, so you can connect to your TiDB cluster via a SQL client from your laptop.

  TiDB Serverless requires [TLS connections](/tidb-cloud/secure-connections-to-serverless-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

The following table shows the network you can use in different connection methods:

| Connection method          | Network                      | Description                                                                                                       |
|----------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Direct connections         | Public or private endpoint   | Direct connections can be made via both public and private endpoints.                                             |
| Data Service (beta)        | /                            | Accessing TiDB Serverless via Data Service (beta) does not need to specify the network type.                      |
| Serverless Driver (beta)   | Public endpoint              | Serverless Driver only supports connections via public endpoint.                                                  |

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
