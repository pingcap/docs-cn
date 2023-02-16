---
title: Limitations and Quotas in TiDB Cloud
summary: Learn the limitations and quotas in TiDB Cloud.
---

# Limitations and Quotas in TiDB Cloud

TiDB Cloud limits how many of each kind of component you can create, and the common usage limitations of TiDB. In addition, there are some organization-level quotas to limit the amount of resources created by users to prevent from creating more resources than you actually need. These tables outline limits and quotas.

> **Note:**
>
> If any of these limits or quotas present a problem for your organization, please contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Cluster Limits

| Component | Limit |
|:-|:-|
| Number of data replicas | 3 |
| Number of Availability Zones for a cross-zone deployment | 3 |

> **Note:**
>
> If you want to learn more about common usage limitations of TiDB, please refer to [TiDB Limitations](https://docs.pingcap.com/tidb/stable/tidb-limitations).

## Cluster Quotas

| Component | Quota (default) |
|:-|:-|
| Maximum number of total TiDB nodes for all clusters in your organization | 10 |
| Maximum number of total TiKV nodes for all clusters in your organization | 15 |
| Maximum number of total TiFlash nodes for all clusters in your organization | 5 |
