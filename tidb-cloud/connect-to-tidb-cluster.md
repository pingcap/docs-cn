---
title: Connect to Your TiDB Dedicated Cluster
summary: Learn how to connect to your TiDB Dedicated cluster via different methods.
---

# Connect to Your TiDB Dedicated Cluster

This document introduces the methods to connect to your TiDB Dedicated cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster, see [Connect to Your TiDB Serverless Cluster](/tidb-cloud/connect-to-tidb-cluster-serverless.md).

After your TiDB Dedicated cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.

- [Connect via private endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md) (recommended)

    For TiDB Dedicated clusters hosted on AWS, private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Connect via private endpoint with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md) (recommended)

    For TiDB Dedicated clusters hosted on Google Cloud, private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over Google Cloud Private Service Connect, which provides highly secure and one-way access to database services with simplified network management.

- [Connect via VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)

    If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account.

- [Connect via Chat2Query (beta)](/tidb-cloud/explore-data-with-chat2query.md)

    > **Note:**
    >
    > To use Chat2Query on [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

    TiDB Cloud is powered by artificial intelligence (AI). If your cluster is hosted on AWS and the TiDB version of the cluster is v6.5.0 or later, you can use Chat2Query (beta), an AI-powered SQL editor in the [TiDB Cloud console](https://tidbcloud.com/), to maximize your data value.

    In Chat2Query, you can either simply type `--` followed by your instructions to let AI generate SQL queries automatically or write SQL queries manually, and then run SQL queries against databases without a terminal. You can find the query results in tables intuitively and check the query logs easily.

- [Connect via SQL Shell](/tidb-cloud/connect-via-sql-shell.md): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
