---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# Changefeed Billing

TiDB Cloud measures the capacity of changefeeds in TiCDC Replication Capacity Units (RCUs). When you create the first changefeed for a cluster, TiDB Cloud automatically sets up TiCDC RCUs for you, and you will be charged for these TiCDC RCUs. All changefeeds that are created in a single cluster share the same TiCDC RCUs.

## Number of TiCDC RCUs

For each TiDB cluster, the number of TiCDC RCUs is set up by TiDB Cloud according to the total vCPU count of all TiKV nodes in your cluster as follows:

| Total vCPUs of all TiKV nodes | Number of RCUs |
|------------------------------|----------------|
| < 48                         | 16             |
| >= 48, and < 120             | 24             |
| >= 120, and <= 168           | 32             |
| > 168                        | 40             |

## Price

The following table lists the price of TiDB Cloud for each TiCDC RCUs:

| Cloud provider | Region                      | RCU price ($/hr) |
|----------------|-----------------------------|------------------|
| AWS            | Oregon (us-west-2)          |          $0.1307 |
| AWS            | N. Virginia (us-east-1)     |          $0.1307 |
| AWS            | Mumbai (ap-south-1)         |          $0.1393 |
| AWS            | Singapore (ap-southeast-1)  |          $0.1623 |
| AWS            | Tokyo (ap-northeast-1)      |          $0.1669 |
| AWS            | Frankfurt (eu-central-1)    |          $0.1564 |
| GCP            | Oregon (us-west1)           |          $0.1452 |
| GCP            | N. Virginia (us-east4)      |          $0.1626 |
| GCP            | Iowa (us-central1)          |          $0.1452 |
| GCP            | Singapore (asia-southeast1) |          $0.1746 |
| GCP            | Taiwan (asia-east1)         |          $0.1628 |
| GCP            | Tokyo (asia-northeast1)     |          $0.1868 |
| GCP            | Osaka (asia-northeast2)     |          $0.1868 |
