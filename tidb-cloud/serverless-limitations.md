---
title: TiDB Serverless Limitations and Quotas
summary: Learn about the limitations of TiDB Serverless.
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Serverless Limitations and Quotas

<!-- markdownlint-disable MD026 -->

TiDB Serverless works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Hosted or TiDB Dedicated clusters and TiDB Serverless clusters. This document describes the limitations of TiDB Serverless.

We are constantly filling in the feature gaps between TiDB Serverless and TiDB Dedicated. If you require these features or capabilities in the gap, use [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## Limitations

### Audit logs

- [Database audit logging](/tidb-cloud/tidb-cloud-auditing.md) is currently unavailable.

### Connection

- Only [Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) and [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) can be used. You cannot use [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to TiDB Serverless clusters. 
- No [IP Access list](/tidb-cloud/configure-ip-access-list.md) support.

### Encryption

- Data persisted in your TiDB Serverless cluster is encrypted using the encryption tool provided by the cloud provider that manages your cluster. However, TiDB Serverless does not provide any additional optional measures for protecting data at-rest on disks beyond infrastructure-level encryption.
- Using [customer-managed encryption keys (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek.md) is currently unavailable.

### Maintenance window

- [Maintenance window](/tidb-cloud/configure-maintenance-window.md) is currently unavailable.

### Monitoring and diagnosis

- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently unavailable.
- [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md) is currently unavailable.
- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) is currently unavailable.
- [Index Insight](/tidb-cloud/tune-performance.md#index-insight-beta) is currently unavailable.
- [Cluster Events](/tidb-cloud/tidb-cloud-events.md) is currently unavailable.

### Self-service upgrades

- TiDB Serverless is a fully managed deployment of TiDB. Major and minor version upgrades of TiDB Serverless are handled by TiDB Cloud and therefore cannot be initiated by users.

### Stream data

- [Changefeed](/tidb-cloud/changefeed-overview.md) is not supported for TiDB Serverless currently.
- [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) is not supported for TiDB Serverless currently.

### Others

- [Time to live (TTL)](/time-to-live.md) is currently unavailable.
- Transaction can not last longer than 30 minutes.
- For more details about SQL limitations, refer to [Limited SQL Features](/tidb-cloud/limited-sql-features.md).

## Usage quota

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spending limit](/tidb-cloud/tidb-cloud-glossary.md#spending-limit) for the usage.

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. It is a metric that allows you to estimate the computational resources required to process a specific request in the database. The request unit is also the billing unit for TiDB Cloud Serverless service.

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a TiDB Serverless cluster with an additional quota, you can edit the spending limit on the cluster creation page. For more information, see [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

After creating a TiDB Serverless, you can still check and edit the spending limit on your cluster overview page. For more information, see [Manage Spending Limit for TiDB Serverless Clusters](/tidb-cloud/manage-serverless-spend-limit.md).
