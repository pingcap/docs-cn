---
title: TiDB Cloud Billing
summary: Learn about TiDB Cloud billing.
---

# TiDB Cloud Billing

> **Note:**
>
> [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier) are free to use for up to one year. You will not be charged for the use of your Developer Tier cluster, and your TiDB Cloud bill will not display any Developer Tier charges.

TiDB Cloud charges according to the resources that you consume, which include:

- Cluster node compute
- Primary data storage
- Data backup storage
- Data transfers in to, out from, and within your cluster

These charges appear as separate items on your monthly TiDB Cloud bills.

## Compute cost

TiDB Cloud lets you pay for database cluster compute resources by hour, which is ideal for dynamic workloads.

In TiDB Cloud, you can control your cluster size easily by specifying the node quantity and node size of TiDB, TiKV, and TiFlash.

The specified node quantity and associated vCPUs determine your hourly compute cost.

Note that the compute cost of TiDB, TiKV, and TiFlash nodes might vary depending on different cloud providers and different regions. For details, see [TiDB Cloud pricing](https://en.pingcap.com/tidb-cloud-pricing/).

## Storage cost

Both TiKV and TiFlash nodes save your data to persistent block storage. The storage costs are generated according to the total volume of storage that all TiKV and TiFlash nodes in your cluster consume.

TiDB Cloud passes the costs onto customers as they are incurred. For details, see [TiDB Cloud pricing](https://en.pingcap.com/tidb-cloud-pricing/).

## Backup storage cost

TiDB Cloud provides automatic backup and ad-hoc backup, both backups consume the storage. We will charge you based on the maximum capacity of total backups per month.

The storage prices for different cloud providers are as follows:

- AWS

    All backups will be saved in Amazon Simple Storage Service (Amazon S3). You only need to pay the S3 fee and we will not charge you an additional fee. For details, see [Amazon S3 pricing](https://aws.amazon.com/s3/pricing/).

- GCP

    All backups will be saved in GCP cloud storage. You only need to pay the Cloud Storage fee and we will not charge you an additional fee. For details, see [GCP Cloud Storage pricing](https://cloud.google.com/storage/pricing).

## Data transfer cost

Both AWS and GCP might charge for data transfer, calculated per GB, whenever data moves within or leaves its cloud. Examples of when these charges are incurred with TiDB Cloud include the following:

- When data moves between the TiDB cluster load balancer and your cluster
- When data moves across different availability zones in the same region within your cluster
- When you perform cluster backup and recovery operations
- When you use TiCDC to stream data to or from your cluster
- Fixed cost of the load balancer

TiDB Cloud passes these charges onto customers as they are incurred, calculated using the published [AWS](https://aws.amazon.com/ec2/pricing/on-demand/) and [GCP](https://cloud.google.com/vpc/network-pricing) price tables as applicable, and without any additional fees.

This cost policy applies to all TiDB Cloud customers with [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters, regardless of how those clusters are licensed.

To make these charges easier to view, your TiDB Cloud bills and invoices aggregate and organize all data transfer charges under the following categories:

- Data transfer – Same Region
- Data transfer – Cross Region
- Data transfer – Internet

## Invoices

If you are the owner or billing administrator of your organization, you can manage the invoice information of TiDB Cloud. Otherwise, skip this section.

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), you can pay through your AWS account directly but cannot add payment methods or download invoices in the TiDB Cloud portal.

After you set up the payment method, TiDB Cloud will generate the invoice for the previous month at the beginning of each month. Invoice costs include TiDB cluster usage consumption, discounts, backup storage costs, and data transmission costs in your organization.

- TiDB Cloud provides the invoice to you on the ninth of each month. From the first to the ninth day, you cannot view the last month's cost details, but can obtain the cluster usage information of this month via the billing console.
- The default method for paying invoices is credit card deduction. If you want to use other payment methods, please send a ticket request to let us know.
- After the invoice is generated, please finish the payment within 30 days.
- You can view the summary and details of charges for the current month and the previous month.

> **Note:**
>
> All billing deductions will be completed through the third-party platform Stripe.

To view the list of invoices, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**. The invoices page is displayed.

## Billing details

If you are the owner or billing administrator of the organization, you can view and export the billing details of TiDB Cloud. Otherwise, skip this section.

After setting the payment method, TiDB Cloud will generate the invoice and billing details of the historical months, and generate the bill details of the current month at the beginning of each month. The billing details include your organization's TiDB cluster usage consumption, discounts, backup storage costs, data transmission costs, and project splitting information.

> **Note:**
>
> Due to delays and other reasons, the billing details of the current month are for reference only, not guaranteed to be accurate. TiDB Cloud ensures the accuracy of historical bills so that you can perform cost accounting and meet other needs.

To view the billing details, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click **Bills**. The billing details page is displayed.

## Trial points

During the [PoC](/tidb-cloud/tidb-cloud-poc.md) period, you can use trial points to pay the TiDB cluster fees. One point is equivalent to one U.S. dollar. All your TiDB clusters will be automatically terminated when the trial points are used up.

> **Note:**
>
> Once you set up the payment method successfully, the unused trial points will become invalid. The cluster fees that have been deducted from trial points will not be included in your new bill.

## Payment method

If you are the owner or billing administrator of your organization, you can manage the payment information of TiDB Cloud. Otherwise, skip this section.

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), you can pay through your AWS account directly but cannot add payment methods or download invoices in the TiDB Cloud portal.

### Add a credit card

The fee is deducted from a bound credit card according to your cluster usage. To add a valid credit card, you can use either of the following methods:

- When you are creating a cluster:

    1. Before you click **Create Cluster** on the **Create a Cluster** page, click **Add Credit Card** at the bottom of the **Billing Calculator** pane.
    2. In the **Add a Card** dialog box, fill in the card information and billing address.
    3. Click **Save Card**.

- Anytime in the billing console:

    1. Click the account name in the upper-right corner of the TiDB Cloud console.
    2. Click **Billing**.
    3. Under the **Payment Method** tab, click **Add a New Card**.
    4. Fill in the billing address and card information, and then click **Save**.

> **Note:**
>
> To ensure the security of credit card sensitive data, TiDB Cloud does not save any customer credit card information and saves them in the third-party payment platform Stripe. All billing deductions are completed through Stripe.

You can bind multiple credit cards, and set one of them as the default credit card in the payment method of the billing console. After setting, subsequent billings will be automatically deducted from the default credit card.

To set the default credit card, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click the **Payment Method** tab.
4. Select a credit card in the credit card list, and click **Set as default**.

### Edit billing profile information

The billing profile information includes the business legal address and tax registration information. By providing your tax registration number, certain taxes might be exempted from your invoice.

To edit the billing profile information, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click the **Payment Method** tab.
4. Edit the billing profile information, and then click **Save**.