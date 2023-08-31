---
title: Create a TiDB Serverless Cluster
summary: Learn how to create your TiDB Serverless cluster.
---

# Create a TiDB Serverless Cluster

This document describes how to create a TiDB Serverless cluster in the [TiDB Cloud console](https://tidbcloud.com/).

> **Tip:**
>
> To learn how to create a TiDB Dedicated cluster, see [Create a TiDB Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

## Steps

If you are in the `Organization Owner` or the `Project Owner` role, you can create a TiDB Serverless cluster as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, **Serverless** is selected by default.

4. The cloud provider of TiDB Serverless is AWS. You can select an AWS region where you want to host your cluster.

5. (Optional) Change the spending limit if you plan to use more storage and compute resources than the [free quota](/tidb-cloud/select-cluster-tier.md#usage-quota). If you have not added a payment method, you need to add a credit card after editing the limit.

    > **Note:**
    >
    > For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spending limit](/tidb-cloud/tidb-cloud-glossary.md#spending-limit) for the usage.

6. Update the default cluster name if necessary, and then click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

## What's next

After your cluster is created, follow the instructions in [Connect to TiDB Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your cluster.

> **Note:**
>
> If you do not set a password, you cannot connect to the cluster.