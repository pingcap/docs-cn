---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# Changefeed Billing

TiDB Cloud measures the capacity of [changefeeds](/tidb-cloud/changefeed-overview.md) in TiCDC Replication Capacity Units (RCUs). When you [create a changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) for a cluster, you can select an appropriate specification. The higher the RCU, the better the replication performance. You will be charged for these TiCDC changefeed RCUs.

## Number of TiCDC RCUs

The following table lists the specifications and corresponding replication performances for changefeeds:

| Specification | Maximum replication performance |
|---------------|---------------------------------|
| 2 RCUs        | 5,000 rows/s                    |
| 4 RCUs        | 10,000 rows/s                   |
| 8 RCUs        | 20,000 rows/s                   |
| 16 RCUs       | 40,000 rows/s                   |
| 24 RCUs       | 60,000 rows/s                   |
| 32 RCUs       | 80,000 rows/s                   |
| 40 RCUs       | 100,000 rows/s                  |

> **Note:**
>
> The preceding performance data is for reference only and might vary in different scenarios.

## Price

To learn about the supported regions and the price of TiDB Cloud for each TiCDC RCU, see [Changefeed Cost](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost).
