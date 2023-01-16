---
title: Connect to Your TiDB Cluster
summary: Learn how to connect to your TiDB cluster via different methods.
---

# Connect to Your TiDB Cluster

After your TiDB cluster is created on TiDB Cloud, you can connect to your TiDB cluster. Depending on whether you are using a Serverless Tier cluster or a Dedicated Tier cluster, you can find the available connection methods as follows:

## Serverless Tier

For Serverless Tier clusters, you can connect to your cluster via standard connection or via Chat2Query (Beta) in the TiDB Cloud console.

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop.

    Serverless Tier only [supports TLS connections](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

- Connect via [Chat2Query (beta)](/tidb-cloud/explore-data-with-chat2query.md)

    TiDB Cloud is powered by artificial intelligence (AI). You can use Chat2Query (beta), an AI-powered SQL editor in the [TiDB Cloud console](https://tidbcloud.com/), to maximize your data value.

    In Chat2Query, you can either simply type `--` followed by your instructions to let AI generate SQL queries automatically or write SQL queries manually, and then run SQL queries against databases without a terminal. You can find the query results in tables intuitively and check the query logs easily.

## Dedicated Tier

For Dedicated Tier clusters, you can connect to your cluster via one of the following methods:

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md#dedicated-tier)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.

- [Connect via private endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Connect via VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)

    If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account.

- [Connect via SQL Shell](/tidb-cloud/connect-via-sql-shell.md): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
