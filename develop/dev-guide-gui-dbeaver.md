---
title: Connect to TiDB with DBeaver
summary: Learn how to connect to TiDB using DBeaver Community.
---

# Connect to TiDB with DBeaver

TiDB is a MySQL-compatible database, and [DBeaver Community](https://dbeaver.io/download/) is a free cross-platform database tool for developers, database administrators, analysts, and everyone working with data.

In this tutorial, you can learn how to connect to your TiDB cluster using DBeaver Community.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [DBeaver Community **23.0.3** or higher](https://dbeaver.io/download/).
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Connect to TiDB

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `JDBC`
    - **Operating System** matches your environment.

4. Click **Create password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Launch DBeaver and click **New Database Connection** in the upper-left corner. In the **Connect to a database** dialog, select **TiDB** from the list, and then click **Next**.

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

6. Copy the JDBC string from the TiDB Cloud connection dialog. In DBeaver, select **URL** for **Connect by** and paste the JDBC string into the **URL** field. You don't need to replace the `<your_password>` placeholder in the string with your actual password, because DBeaver reads username and password from the **Authentication (Database Native)** section.

7. In the **Authentication (Database Native)** section, enter your **Username** and **Password**. An example is as follows:

    ![Configure connection settings for TiDB Serverless](/media/develop/dbeaver-connection-settings-serverless.jpg)

8. Click **Test Connection** to validate the connection to the TiDB Serverless cluster.

    If the **Download driver files** dialog is displayed, click **Download** to get the driver files.

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    If the connection test is successful, the **Connection test** dialog is displayed as follows. Click **OK** to close it.

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

9. Click **Finish** to save the connection configuration.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**, and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Launch DBeaver and click **New Database Connection** in the upper-left corner. In the **Connect to a database** dialog, select **TiDB** from the list, and then click **Next**.

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

5. Copy and paste the appropriate connection string into the DBeaver connection panel. The mappings between DBeaver fields and TiDB Dedicated connection string are as follows:

    | DBeaver field | TiDB Dedicated connection string |
    |---------------| ------------------------------- |
    | Server Host   | `{host}`                        |
    | Port          | `{port}`                        |
    | Username      | `{user}`                        |
    | Password      | `{password}`                    |

    An example is as follows:

    ![Configure connection settings for TiDB Dedicated](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6. Click **Test Connection** to validate the connection to the TiDB Dedicated cluster.

    If the **Download driver files** dialog is displayed, click **Download** to get the driver files.

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    If the connection test is successful, the **Connection test** dialog is displayed as follows. Click **OK** to close it.

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

7. Click **Finish** to save the connection configuration.

</div>
<div label="TiDB Self-Hosted">

1. Launch DBeaver and click **New Database Connection** in the upper-left corner. In the **Connect to a database** dialog, select **TiDB** from the list, and then click **Next**.

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

2. Configure the following connection parameters:

    - **Server Host**: The IP address or domain name of your TiDB Self-Hosted cluster.
    - **Port**: The port number of your TiDB Self-Hosted cluster.
    - **Username**: The username to use to connect to your TiDB Self-Hosted cluster.
    - **Password**: The password of the username.

    An example is as follows:

    ![Configure connection settings for TiDB Self-Hosted](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3. Click **Test Connection** to validate the connection to the TiDB Self-Hosted cluster.

    If the **Download driver files** dialog is displayed, click **Download** to get the driver files.

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    If the connection test is successful, the **Connection test** dialog is displayed as follows. Click **OK** to close it.

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

4. Click **Finish** to save the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn more usage of DBeaver from [the documentation of DBeaver](https://github.com/dbeaver/dbeaver/wiki).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
