---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
---

# Changefeed Billing

TiDB Cloud measures the capacity of changefeeds in TiCDC Capacity Units (TCUs). When you create the first changefeed for a cluster, TiDB Cloud automatically sets up TiCDC Capacity Units (TCUs) for you, and you will be charged for these TiCDC Capacity Units. All changefeeds that are created in a single cluster share the same TiCDC Capacity Units. 

## Number of TiCDC Capacity Units

For each TiDB cluster, the number of TiCDC Capacity Units is set up by TiDB Cloud according to the total vCPU count of all TiKV nodes in your cluster as follows:

| Total vCPUs of all TiKV nodes | Number of TCUs |
|------------------------------|----------------|
| < 48                         | 16             |
| >= 48, and < 120             | 24             |
| >= 120, and <= 168           | 32             |
| > 168                        | 40             |

## Price

The following table lists the price of TiDB Cloud for each TiCDC Capacity Unit (TCU):

| Cloud provider | Region                      | TCU Price ($/hr) |
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
