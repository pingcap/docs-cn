---
title: Data Migration Billing
summary: Learn about billing for Data Migration in TiDB Cloud.
---

# Data Migration Billing

This document describes the billing for Data Migration in TiDB Cloud.

## Specifications for Data Migration

TiDB Cloud measures the capacity of Data Migration in Replication Capacity Units (RCUs). When you create a Data Migration job, you can select an appropriate specification. The higher the RCU, the better the migration performance. You will be charged for these Data Migration RCUs.

The following table lists the specifications and corresponding performances for Data Migration.

| Specification | Full data migration | Incremental data migration |
|---------------|---------------------|----------------------------|
| 2 RCUs  | 25 MiB/s | 10,000 rows/s|
| 4 RCUs  | 35 MiB/s | 20,000 rows/s|
| 8 RCUs  | 40 MiB/s | 40,000 rows/s|
| 16 RCUs | 45 MiB/s | 80,000 rows/s|

Note that all the performance values in this table are maximum performances. It is assumed that there are no performance, network bandwidth, or other bottlenecks in the upstream and downstream databases. The performance values are for reference only and might vary in different scenarios.

The Data Migration job measures full data migration performance in MiB/s. This unit indicates the amount of data (in MiB) that is migrated per second by the Data Migration job.

The Data Migration job measures incremental data migration performance in rows/s. This unit indicates the number of rows that are migrated to the target database per second. For example, if the upstream database executes `INSERT`, `UPDATE`, or `DELETE` statements of 10,000 rows in about 1 second, the Data Migration job of the corresponding specification can replicate the 10,000 rows to the downstream in about 1 second.

## Price

To learn about the supported regions and the price of TiDB Cloud for each Data Migration RCU, see [Data Migration Cost](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost).

The Data Migration job is in the same region as the target TiDB cluster.

Note that if you are using AWS PrivateLink or VPC peering connections, and if the source database and the TiDB cluster are not in the same region or not in the same availability zone (AZ), two additional traffic charges will be incurred: cross-region and cross-AZ traffic charges.

- If the source database and the TiDB cluster are not in the same region, cross-region traffic charges are incurred when the Data Migration job collects data from the source database.

    ![Cross-region traffic charges](/media/tidb-cloud/dm-billing-cross-region-fees.png)

- If the source database and the TiDB cluster are in the same region but in different AZs, cross-AZ traffic charges are incurred when the Data Migration job collects data from the source database.

    ![Cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-az-fees.png)

- If the Data Migration job and the TiDB cluster are not in the same AZ, cross-AZ traffic charges are incurred when the Data Migration job writes data to the target TiDB cluster. In addition, if the Data Migration job and the TiDB cluster are not in the same AZ (or region) with the source database, cross-AZ (or cross-region) traffic charges are incurred when the Data Migration job collects data from the source database.

    ![Cross-region and cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-region-and-az-fees.png)

The cross-region and cross-AZ traffic prices are the same as those for TiDB Cloud. For more information, see [TiDB Cloud Pricing Details](https://en.pingcap.com/tidb-cloud-pricing-details/).

## See also

- [Migrate from MySQL-Compatible Databases Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
