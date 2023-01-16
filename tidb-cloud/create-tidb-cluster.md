---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# Create a TiDB Cluster

This tutorial guides you through signing up and creating a TiDB cluster.

## Step 1. Create a TiDB Cloud account

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

    - For Google users, you can also sign up with Google. To do that, click **Sign up with Google** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by Google and cannot be changed using TiDB Cloud console.
    - For GitHub users, you can also sign up with GitHub. To do that, click **Sign up with GitHub** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by GitHub and cannot be changed using TiDB Cloud console.
    - For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
    - For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

## Step 2. Select a cluster tier

TiDB Cloud provides the following two cluster tier options. Before creating a TiDB cluster, consider which option suits your need better:

- Serverless Tier (Beta)

    The TiDB Cloud Serverless Tier is a fully managed service of TiDB. It is still in the beta phase and cannot be used in production. However, you can use Serverless Tier clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for your datasets.

- Dedicated Tier

    The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For more information about the two options, see [Select Your Cluster Tier](/tidb-cloud/select-cluster-tier.md).

## Step 3. Use your default project or create a new project

If you are an organization owner, once you log in to TiDB Cloud, you have a default project. For more information about projects, see [Organizations and projects](/tidb-cloud/manage-user-access.md#organizations-and-projects).

- For free trial users, you can rename the default project if needed.
- For Dedicated Tier users, you can either rename the default project or create a new project if needed.

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. Do one of the following:

    - To rename the default project, click **Rename** in the **Actions** column.
    - To create a project, click **Create New Project**, enter a name for your project, and then click **Confirm**.

4. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

If you are a project member, you can access only the specific projects to which your organization owner invited you, and you cannot create new projects. To check which project you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

## Step 4. Create a TiDB cluster

<SimpleTab>
<div label="Serverless Tier">

To create a Serverless Tier cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, select **Serverless Tier**, and update the default cluster name if necessary.

4. Note that the cloud provider of Serverless Tier is AWS, and then select the region where you want to create your cluster.

5. Click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

6. After the cluster is created, follow the instructions in [Connect via Standard Connection](/tidb-cloud/connect-via-standard-connection.md#serverless-tier) to create a password for your cluster.

    > **Note:**
    >
    > If you do not set a password, you cannot connect to the cluster.

</div>

<div label="Dedicated Tier">

To create a Dedicated Tier cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, select **Dedicated Tier**, update the default cluster name and port number if necessary, choose a cloud provider and a region, and then click **Next**.

    > **Note:**
    >
    > - If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), the cloud provider is AWS, and you cannot change it in TiDB Cloud.
    > - If you signed up TiDB Cloud through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), the cloud provider is GCP, and you cannot change it in TiDB Cloud.

4. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR, and then click **Next**. If you do not see the **Project CIDR** field, it means that CIDR has already been configured for this project.

    > **Note:**
    >
    > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. You cannot modify your project CIDR once it is set.

5. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively, and then click **Next**.

6. Confirm the cluster information on the page and the billing information in the lower-left corner.

7. If you have not added a payment method, click **Add Credit Card** in the lower-right corner.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

8. Click **Create**.

    Your TiDB Cloud cluster will be created in approximately 20 to 30 minutes.

9. In the row of your target cluster, click **...** and select **Security Settings**.

10. Set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

</div>
</SimpleTab>
