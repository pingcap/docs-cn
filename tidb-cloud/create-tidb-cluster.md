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

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

## Step 2. Select a cluster tier

TiDB Cloud provides the following two cluster tier options. Before creating a TiDB cluster, consider which option suits your need better:

- Developer Tier

    The TiDB Cloud Developer Tier is a one-year free trial of [TiDB Cloud](https://pingcap.com/products/tidbcloud), the fully managed service of TiDB. You can use Developer Tier clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for non-commercial datasets.

- Dedicated Tier

    The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For more information about the two options, see [Select Your Cluster Tier](/tidb-cloud/select-cluster-tier.md).

## Step 3. Use your default project or create a new project

If you are an organization owner, once you log in to TiDB Cloud, you have a default project. If you do not want to use the default project, you can take the following steps to create a new one:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. Click **Create New Project**.

4. Enter a name for your project, and then click **Confirm**.

5. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

If you are a project member, you can access only the specific projects to which your organization owner invited you, and you cannot create new projects. To check which project you belong to, take the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

## Step 4. Create a TiDB cluster

<SimpleTab>
<div label="Developer Tier">

To create a Developer Tier cluster, take the following steps:

1. On the **Active Clusters** page, click **Create Cluster**.

2. On the **Create Cluster** page, update the default cluster name if necessary.

3. Note that the cloud provider of Developer Tier is AWS, and then select the region where you want to create your cluster.

4. View the cluster size of the Developer Tier, and then click **Create**.

   The cluster creation process starts and the **Security Settings** dialog box is displayed.

5. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

    Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>

<div label="Dedicated Tier">

To create a Dedicated Tier cluster, take the following steps:

1. On the **Active Clusters** page, click **Create Cluster**.

2. On the **Create Cluster** page, select **Dedicated Tier**, update the default cluster name and port number if necessary, choose a cloud provider and a region, and then click **Next**.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), the cloud provider is AWS, and you cannot change it in TiDB Cloud.

3. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR, and then click **Next**. If you do not see the **project CIDR** field, it means that CIDR has already been configured for this project.

    > **Note:**
    >
    > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. You cannot modify your project CIDR once it is set.

4. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively, and then click **Next**.

5. Confirm the cluster information on the page and the billing information in the lower-left corner.

6. If you have not added a payment method, click **Add Credit Card** in the lower-right corner.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), you can pay through your AWS account directly but cannot add payment methods or download invoices in the TiDB Cloud portal.

7. Click **Create**.

   The cluster creation process starts and the **Security Settings** dialog box is displayed.

8. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

    Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>
</SimpleTab>