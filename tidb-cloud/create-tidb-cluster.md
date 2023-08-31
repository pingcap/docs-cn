---
title: Create a TiDB Dedicated Cluster
summary: Learn how to create your TiDB Dedicated cluster.
---

# Create a TiDB Dedicated Cluster

This tutorial guides you through signing up and creating a TiDB Dedicated cluster.

> **Tip:**
>
> To learn how to create a TiDB Serverless cluster, see [Create a TiDB Serverless Cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

## (Optional) Step 1. Use your default project or create a new project

Once you log in to the [TiDB Cloud console](https://tidbcloud.com/), you have a default [project](/tidb-cloud/tidb-cloud-glossary.md#project). When there is only one project in your organization, your cluster will be created in that project. For more information about projects, see [Organizations and projects](/tidb-cloud/manage-user-access.md#organizations-and-projects).

If you are an organization owner, you can rename the default project or create a new project for the cluster according to your need as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. Do one of the following:

    - To rename the default project, click **Rename** in the **Actions** column.
    - To create a project, click **Create New Project**, enter a name for your project, and then click **Confirm**.

4. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

## Step 2. Create a TiDB Dedicated cluster

If you are in the `Organization Owner` or the `Project Owner` role, you can create a TiDB Dedicated cluster as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, select **Dedicated**, and then configure the cluster information as follows:

    1. Choose a cloud provider and a region.

        > **Note:**
        >
        > - If you signed up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), the cloud provider is AWS, and you cannot change it in TiDB Cloud.
        > - If you signed up for TiDB Cloud through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), the cloud provider is Google Cloud, and you cannot change it in TiDB Cloud.

    2. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively.
    3. Update the default cluster name and port number if necessary.
    4. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR. If you do not see the **Project CIDR** field, it means that CIDR has already been configured for this project.

        > **Note:**
        >
        > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. You cannot modify your project CIDR once it is set.

4. Confirm the cluster and billing information on the right side.

5. If you have not added a payment method, click **Add Credit Card** in the lower-right corner.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

6. Click **Create**.

    Your TiDB Cloud cluster will be created in approximately 20 to 30 minutes.

## Step 3. Configure secure settings

After your cluster is created, take the following steps to configure the security settings:

1. In the upper-right corner of your cluster overview page, click **...** and select **Security Settings**.

2. Set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

## What's next

After your cluster is created on TiDB Cloud, you can connect to it via the methods provided in [Connect to Your TiDB Dedicated Cluster](/tidb-cloud/connect-via-standard-connection-serverless.md).