---
title: Build a TiDB Serverless Cluster
summary: Learn how to build a TiDB Serverless cluster in TiDB Cloud and connect to it.
---

<!-- markdownlint-disable MD029 -->

# Build a TiDB Serverless Cluster

<CustomContent platform="tidb">

This document walks you through the quickest way to get started with TiDB. You will use [TiDB Cloud](https://en.pingcap.com/tidb-cloud) to create a TiDB Serverless cluster, connect to it, and run a sample application on it.

If you need to run TiDB on your local machine, see [Starting TiDB Locally](/quick-start-with-tidb.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

This document walks you through the quickest way to get started with TiDB Cloud. You will create a TiDB cluster, connect to it, and run a sample application on it.

</CustomContent>

## Step 1. Create a TiDB Serverless cluster

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up for an account.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

3. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click **Create Cluster**.

4. On the **Create Cluster** page, **Serverless** is selected by default. Update the default cluster name if necessary, and then select the region where you want to create your cluster.

5. Click **Create** to create a TiDB Serverless cluster.

    Your TiDB Cloud cluster will be created in approximately 30 seconds.

6. After your TiDB Cloud cluster is created, click your cluster name to go to the cluster overview page, and then click **Connect** in the upper-right corner. A connection dialog box is displayed.

7. In the dialog, select your preferred connection method and operating system to get the corresponding connection string. This document uses MySQL client as an example.

8. Click **Create password** to generate a random password. The generated password will not show again, so save your password in a secure location. If you do not set a root password, you cannot connect to the cluster.

<CustomContent platform="tidb">

> **Note:**
>
> For [TiDB Serverless clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless), when you connect to your cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> For [TiDB Serverless clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless), when you connect to your cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

</CustomContent>

## Step 2. Connect to a cluster

1. If the MySQL client is not installed, select your operating system and follow the steps below to install it.

<SimpleTab>

<div label="macOS">

For macOS, install [Homebrew](https://brew.sh/index) if you do not have it, and then run the following command to install the MySQL client:

```shell
brew install mysql-client
```

The output is as follows:

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

To add the MySQL client to your PATH, locate the following command in the above output (if your output is inconsistent with the above output in the document, use the corresponding command in your output instead) and run it:

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

Then, declare the global environment variable by the `source` command and verify that the MySQL client is installed successfully:

```shell
source ~/.zshrc
mysql --version
```

An example of the expected output:

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

For Linux, the following takes CentOS 7 as an example:

```shell
yum install mysql
```

Then, verify that the MySQL client is installed successfully:

```shell
mysql --version
```

An example of the expected output:

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. Run the connection string obtained in [Step 1](#step-1-create-a-tidb-serverless-cluster).

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **Note:**
>
> - When you connect to a TiDB Serverless cluster, you must [use the TLS connection](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters).
> - If you encounter problems when connecting to a TiDB Serverless cluster, you can read [Secure Connections to TiDB Serverless Clusters](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) for more information.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - When you connect to a TiDB Serverless cluster, you must [use the TLS connection](/tidb-cloud/secure-connections-to-serverless-clusters.md).
> - If you encounter problems when connecting to a TiDB Serverless cluster, you can read [Secure Connections to TiDB Serverless Clusters](/tidb-cloud/secure-connections-to-serverless-clusters.md) for more information.

</CustomContent>

3. Fill in the password to sign in.

## Step 3. Execute a SQL statement

Let's try to execute your first SQL statement on TiDB Cloud.

```sql
SELECT 'Hello TiDB Cloud!';
```

Expected output:

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

If your actual output is similar to the expected output, congratulations, you have successfully execute a SQL statement on TiDB Cloud.
