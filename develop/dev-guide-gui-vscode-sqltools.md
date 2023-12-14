---
title: Connect to TiDB with Visual Studio Code
summary: Learn how to connect to TiDB using Visual Studio Code or GitHub Codespaces.
---

# Connect to TiDB with Visual Studio Code

TiDB is a MySQL-compatible database, and [Visual Studio Code (VS Code)](https://code.visualstudio.com/) is a lightweight but powerful source code editor. This tutorial uses the [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) extension which supports TiDB as an [official driver](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql).

In this tutorial, you can learn how to connect to your TiDB cluster using Visual Studio Code.

> **Note:**
>
> - This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.
> - This tutorial also works with Visual Studio Code Remote Development environments, such as [GitHub Codespaces](https://github.com/features/codespaces), [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), and [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl).

## Prerequisites

To complete this tutorial, you need:

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0** or later versions.
- [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) extension for Visual Studio Code. To install it, you can use one of the following methods:
    - Click <a href="vscode:extension/mtxr.sqltools-driver-mysql">this link</a>  to launch VS Code and install the extension directly.
    - Navigate to [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) and click **Install**.
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

Connect to your TiDB cluster depending on the TiDB deployment option you have selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
    - **Branch** is set to `main`.
    - **Connect With** is set to `VS Code`.
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your VS Code is running on a remote development environment, select the remote operating system from the list. For example, if you are using Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution. This is not necessary if you are using GitHub Codespaces.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Launch VS Code and select the **SQLTools** extension on the navigation pane. Under the **CONNECTIONS** section, click **Add New Connection** and select **TiDB** as the database driver.

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. In the setting pane, configure the following connection parameters:

    - **Connection name**: give this connection a meaningful name.
    - **Connection group**: (optional) give this group of connections a meaningful name. Connections with the same group name will be grouped together.
    - **Connect using**: select **Server and Port**.
    - **Server Address**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Database**: enter the database that you want to connect to.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password mode**: select **SQLTools Driver Credentials**.
    - In the **MySQL driver specific options** area, configure the following parameters:

        - **Authentication Protocol**: select **default**.
        - **SSL**: select **Enabled**. TiDB Serverless requires a secure connection. In the **SSL Options (node.TLSSocket)** area, configure the **Certificate Authority (CA) Certificate File** field as the `CA` parameter from the TiDB Cloud connection dialog.

            > **Note:**
            >
            > If you are running on Windows or GitHub Codespaces, you can leave **SSL** blank. By default SQLTools trusts well-known CAs curated by Let's Encrypt. For more information, see [TiDB Serverless root certificate management](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management).

    ![VS Code SQLTools: configure connection settings for TiDB Serverless](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. Click **TEST CONNECTION** to validate the connection to the TiDB Serverless cluster.

    1. In the pop-up window, click **Allow**.
    2. In the **SQLTools Driver Credentials** dialog, enter the password you created in step 4.

        ![VS Code SQLTools: enter password to connect to TiDB Serverless](/media/develop/vsc-sqltools-password.jpg)

8. If the connection test is successful, you can see the **Successfully connected!** message. Click **SAVE CONNECTION** to save the connection configuration.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Launch VS Code and select the **SQLTools** extension on the navigation pane. Under the **CONNECTIONS** section, click **Add New Connection** and select **TiDB** as the database driver.

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. In the setting pane, configure the following connection parameters:

    - **Connection name**: give this connection a meaningful name.
    - **Connection group**: (optional) give this group of connections a meaningful name. Connections with the same group name will be grouped together.
    - **Connect using**: select **Server and Port**.
    - **Server Address**: enter the `host` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `port` parameter from the TiDB Cloud connection dialog.
    - **Database**: enter the database that you want to connect to.
    - **Username**: enter the `user` parameter from the TiDB Cloud connection dialog.
    - **Password mode**: select **SQLTools Driver Credentials**.
    - In the **MySQL driver specific options** area, configure the following parameters:

        - **Authentication Protocol**: select **default**.
        - **SSL**: select **Disabled**.

    ![VS Code SQLTools: configure connection settings for TiDB Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. Click **TEST CONNECTION** to validate the connection to the TiDB Dedicated cluster.

    1. In the pop-up window, click **Allow**.
    2. In the **SQLTools Driver Credentials** dialog, enter the password of the TiDB Dedicated cluster.

    ![VS Code SQLTools: enter password to connect to TiDB Dedicated](/media/develop/vsc-sqltools-password.jpg)

7. If the connection test is successful, you can see the **Successfully connected!** message. Click **SAVE CONNECTION** to save the connection configuration.

</div>
<div label="TiDB Self-Hosted">

1. Launch VS Code and select the **SQLTools** extension on the navigation pane. Under the **CONNECTIONS** section, click **Add New Connection** and select **TiDB** as the database driver.

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. In the setting pane, configure the following connection parameters:

    - **Connection name**: give this connection a meaningful name.
    - **Connection group**: (optional) give this group of connections a meaningful name. Connections with the same group name will be grouped together.
    - **Connect using**: select **Server and Port**.
    - **Server Address**: enter the IP address or domain name of your TiDB Self-Hosted cluster.
    - **Port**: enter the port number of your TiDB Self-Hosted cluster.
    - **Database**: enter the database that you want to connect to.
    - **Username**: enter the username to use to connect to your TiDB Self-Hosted cluster.
    - **Password mode**:

        - If the password is empty, select **Use empty password**.
        - Otherwise, select **SQLTools Driver Credentials**.

    - In the **MySQL driver specific options** area, configure the following parameters:

        - **Authentication Protocol**: select **default**.
        - **SSL**: select **Disabled**.

    ![VS Code SQLTools: configure connection settings for TiDB Self-Hosted](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. Click **TEST CONNECTION** to validate the connection to the TiDB Self-Hosted cluster.

    If the password is not empty, click **Allow** in the pop-up window, and then enter the password of the TiDB Self-Hosted cluster.

    ![VS Code SQLTools: enter password to connect to TiDB Self-Hosted](/media/develop/vsc-sqltools-password.jpg)

4. If the connection test is successful, you can see the **Successfully connected!** message. Click **SAVE CONNECTION** to save the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn more usage of Visual Studio Code from [the documentation of Visual Studio Code](https://code.visualstudio.com/docs).
- Learn more usage of VS Code SQLTools extension from [the documentation](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) and [GitHub repository](https://github.com/mtxr/vscode-sqltools) of SQLTools.
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
