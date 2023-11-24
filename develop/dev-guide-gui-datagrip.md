---
title: Connect to TiDB with JetBrains DataGrip
summary: Learn how to connect to TiDB using JetBrains DataGrip. This tutorial also applies to the Database Tools and SQL plugin available in other JetBrains IDEs, such as IntelliJ, PhpStorm, and PyCharm.
---

# Connect to TiDB with JetBrains DataGrip

TiDB is a MySQL-compatible database, and [JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html) is a powerful integrated development environment (IDE) for database and SQL. This tutorial walks you through the process of connecting to your TiDB cluster using DataGrip.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

You can use DataGrip in two ways:

- As the [DataGrip IDE](https://www.jetbrains.com/datagrip/download) standalone tool.
- As the [Database Tools and SQL plugin](https://www.jetbrains.com/help/idea/relational-databases.html) in JetBrains IDEs, such as IntelliJ, PhpStorm, and PyCharm.

This tutorial mainly focuses on the standalone DataGrip IDE. The steps of connecting to TiDB using the JetBrains Database Tools and SQL plugin in JetBrains IDEs are similar. You can also follow the steps in this document for reference when connecting to TiDB from any JetBrains IDE.

## Prerequisites

To complete this tutorial, you need:

- [DataGrip **2023.2.1** or later](https://www.jetbrains.com/datagrip/download/) or a non-community edition [JetBrains](https://www.jetbrains.com/) IDE.
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

5. Launch DataGrip and create a project to manage your connections.

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6. In the newly created project, click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7. Copy the JDBC string from the TiDB Cloud connection dialog and replace `<your_password>` with your actual password. Then, paste it into the **URL** field, and the remaining parameters will be auto-populated. An example result is as follows:

    ![Configure the URL field for TiDB Serverless](/media/develop/datagrip-url-paste.jpg)

    If a **Download missing driver files** warning displays, click **Download** to acquire the driver files.

8. Click **Test Connection** to validate the connection to the TiDB Serverless cluster.

    ![Test the connection to a TiDB Serverless clustser](/media/develop/datagrip-test-connection.jpg)

9. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Launch DataGrip and create a project to manage your connections.

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

5. In the newly created project, click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

6. Copy and paste the appropriate connection string into the **Data Source and Drivers** window in DataGrip. The mappings between DataGrip fields and TiDB Dedicated connection string are as follows:

    | DataGrip field | TiDB Dedicated connection string |
    | -------------- | ------------------------------- |
    | Host           | `{host}`                        |
    | Port           | `{port}`                        |
    | User           | `{user}`                        |
    | Password       | `{password}`                    |

    An example is as follows:

    ![Configure the connection parameters for TiDB Dedicated](/media/develop/datagrip-dedicated-connect.jpg)

7. Click the **SSH/SSL** tab, select the **Use SSL** checkbox, and input the CA certificate path into the **CA file** field.

    ![Configure the CA for TiDB Dedicated](/media/develop/datagrip-dedicated-ssl.jpg)

    If a **Download missing driver files** warning displays, click **Download** to acquire the driver files.

8. Click the **Advanced** tab, scroll to find the **enabledTLSProtocols** parameter, and set its value to `TLSv1.2,TLSv1.3`.

    ![Configure the TLS for TiDB Dedicated](/media/develop/datagrip-dedicated-advanced.jpg)

9. Click **Test Connection** to validate the connection to the TiDB Dedicated cluster.

    ![Test the connection to a TiDB Dedicated cluster](/media/develop/datagrip-dedicated-test-connection.jpg)

10. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Self-Hosted">

1. Launch DataGrip and create a project to manage your connections.

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

2. In the newly created project, click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

3. Configure the following connection parameters:

    - **Host**: The IP address or domain name of your TiDB Self-Hosted cluster.
    - **Port**: The port number of your TiDB Self-Hosted cluster.
    - **User**: The username to use to connect to your TiDB Self-Hosted cluster.
    - **Password**: The password of the username.

    An example is as follows:

    ![Configure the connection parameters for TiDB Self-Hosted](/media/develop/datagrip-self-hosted-connect.jpg)

    If a **Download missing driver files** warning displays, click **Download** to acquire the driver files.

4. Click **Test Connection** to validate the connection to the TiDB Self-Hosted cluster.

    ![Test the connection to a TiDB Self-Hosted cluster](/media/develop/datagrip-self-hosted-test-connection.jpg)

5. Click **OK** to save the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn more usage of DataGrip from [the documentation of DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
