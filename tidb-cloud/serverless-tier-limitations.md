---
title: Serverless Tier Limitations
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tier Limitations

<!-- markdownlint-disable MD026 -->

This document describes the limitations of Serverless Tier.

We are constantly filling in the feature gaps between Serverless Tier and Dedicated Tier. If you require these features or capabilities in the gap, use [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## General limitations

- For each TiDB Cloud account, you can create a maximum of five complimentary Serverless Tier clusters during the beta phase.
- Each Serverless Tier cluster has the following limitations:
    - The storage size is limited to 5 GiB (logical size) of OLTP storage and 5 GiB (logical size) of OLAP storage.
    - The compute resource is limited to 1 vCPU and 1 GiB RAM.
    - **Note**: In the coming months, we intend to offer a usage-based billing plan for additional resources and higher performance, while still keeping offering the free starter plan. In the coming releases, the limitations of the free Serverless Tier might be changed.

## SQL

- [Time to live (TTL)](/time-to-live.md) is not available for Serverless Tier clusters currently.
- The [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) syntax is not applicable to TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

## System tables

- Tables `CLUSTER_SLOW_QUERY`, `SLOW_QUERY`, `CLUSTER_STATEMENTS_SUMMARY`, `CLUSTER_STATEMENTS_SUMMARY_HISTORY`, `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY` are not available for Serverless Tier clusters.

## Transaction

- The total size of a single transaction is set to no more than 10 MB on Serverless Tier during the beta phase.

## Connection

- Only [Standard Connection](/tidb-cloud/connect-via-standard-connection.md) can be used. You cannot use [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) or [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to Serverless Tier clusters. 
- No "IP Access List" support.

## Backup and Restore

- [Backup and Restore](/tidb-cloud/backup-and-restore.md) are not supported for Serverless Tier currently.

## Monitoring

- [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md) is currently not available for Serverless Tier.
- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently not available for Serverless Tier.

## Diagnosis

- [SQL Diagnosis](/tidb-cloud/tune-performance.md) is currently not available for Serverless Tier.

## Stream data

* [Changefeed](/tidb-cloud/changefeed-overview.md) is not supported for Serverless Tier currently.
* [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) is not supported for Serverless Tier currently.
