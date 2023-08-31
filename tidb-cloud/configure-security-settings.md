---
title: Configure Cluster Security Settings
summary: Learn how to configure the root password and allowed IP addresses to connect to your cluster.
---

# Configure Cluster Security Settings

For TiDB Dedicated clusters, you can configure the root password and allowed IP addresses to connect to your cluster.

> **Note:**
>
> For TiDB Serverless clusters, this document is inapplicable and you can refer to [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md) instead.

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. In the row of your target cluster, click **...** and select **Security Settings**.
3. In the **Security Settings** dialog, configure the root password and allowed IP addresses.

    To allow your cluster to be accessible by any IP addresses, click **Allow Access from Anywhere**.

4. Click **Apply**.

> **Tip:**
>
> If you are viewing the overview page of your cluster, you can click the **...** in the upper-right corner of the page, select **Security Settings**, and configure these settings, too.
