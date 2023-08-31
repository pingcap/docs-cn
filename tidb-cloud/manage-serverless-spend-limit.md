---
title: Manage Spending Limit for TiDB Serverless clusters
summary: Learn how to manage spending limit for your TiDB Serverless clusters.
---

# Manage Spending Limit for TiDB Serverless Clusters

> **Note:**
>
> The spending limit is only applicable to TiDB Serverless clusters.

Spending limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that allows you to set a budget for your TiDB Serverless clusters.

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a spending limit for the usage. But if you delete some of your previous clusters before creating more, the new cluster can still be created without a credit card.

## Usage quota

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](#update-spending-limit) or the usage is reset upon the start of a new month. For example, when the storage of a cluster exceeds 5 GiB, the maximum size limit of a single transaction is reduced from 10 MiB to 1 MiB.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a TiDB Serverless cluster with an additional quota, you can edit the spending limit on the cluster creation page. For more information, see [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

## Update spending limit

For an existing TiDB Serverless cluster, you can increase the usage quota by updating the spending limit as follows:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. In the **Usage This Month** area, click **Get more usage quota**.

    If you have previously updated the spending limit for a cluster and want to increase it further, click <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Edit**.

3. Edit the monthly spending limit as needed. If you have not added a payment method, you will need to add a credit card after editing the limit.
4. Click **Update Spending Limit**.
