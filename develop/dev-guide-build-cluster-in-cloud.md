---
title: 构建 TiDB Cloud Serverless 集群
summary: 了解如何在 TiDB Cloud 中构建 TiDB Cloud Serverless 集群并连接到它。
---

<!-- markdownlint-disable MD029 -->

# 构建 TiDB Cloud Serverless 集群

<CustomContent platform="tidb">

本文将指导你快速开始使用 TiDB。你将使用 [TiDB Cloud](https://www.pingcap.com/tidb-cloud) 创建一个 TiDB Cloud Serverless 集群，连接到它，并在其上运行示例应用程序。

如果你需要在本地机器上运行 TiDB，请参阅[在本地启动 TiDB](/quick-start-with-tidb.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

本文将指导你快速开始使用 TiDB Cloud。你将创建一个 TiDB 集群，连接到它，并在其上运行示例应用程序。

</CustomContent>

## 第 1 步：创建 TiDB Cloud Serverless 集群

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册账号。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

3. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击**创建集群**。

4. 在**创建集群**页面，默认选择 **Serverless**。根据需要更新默认集群名称，然后选择要创建集群的区域。

5. 点击**创建**来创建 TiDB Cloud Serverless 集群。

    你的 TiDB Cloud 集群将在大约 30 秒内创建完成。

6. 集群创建完成后，点击集群名称进入集群概览页面，然后点击右上角的**连接**。此时会显示一个连接对话框。

7. 在对话框中，选择你偏好的连接方式和操作系统，以获取相应的连接字符串。本文以 MySQL 客户端为例。

8. 点击**生成密码**来生成随机密码。生成的密码不会再次显示，因此请将密码保存在安全的位置。如果你不设置 root 密码，就无法连接到集群。

<CustomContent platform="tidb">

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，当你连接到集群时，必须在用户名中包含集群的前缀，并用引号将名称括起来。更多信息，请参阅[用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，当你连接到集群时，必须在用户名中包含集群的前缀，并用引号将名称括起来。更多信息，请参阅[用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

</CustomContent>

## 第 2 步：连接到集群

1. 如果未安装 MySQL 客户端，请选择你的操作系统并按照以下步骤进行安装。

<SimpleTab>

<div label="macOS">

对于 macOS，如果你还没有安装 [Homebrew](https://brew.sh/index)，请先安装它，然后运行以下命令来安装 MySQL 客户端：

```shell
brew install mysql-client
```

输出如下：

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

要将 MySQL 客户端添加到你的 PATH 中，请在上述输出中找到以下命令（如果你的输出与文档中的上述输出不一致，请使用你的输出中相应的命令）并运行它：

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

然后，使用 `source` 命令声明全局环境变量，并验证 MySQL 客户端是否安装成功：

```shell
source ~/.zshrc
mysql --version
```

预期输出示例：

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

对于 Linux，以下以 CentOS 7 为例：

```shell
yum install mysql
```

然后，验证 MySQL 客户端是否安装成功：

```shell
mysql --version
```

预期输出示例：

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. 运行在[第 1 步](#第-1-步创建-tidb-cloud-serverless-集群)中获取的连接字符串。

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **注意：**
>
> - 连接到 TiDB Cloud Serverless 集群时，你必须[使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)。
> - 如果你在连接 TiDB Cloud Serverless 集群时遇到问题，可以阅读[连接到 TiDB Cloud Serverless 集群的安全连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)获取更多信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 连接到 TiDB Cloud Serverless 集群时，你必须[使用 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
> - 如果你在连接 TiDB Cloud Serverless 集群时遇到问题，可以阅读[连接到 TiDB Cloud Serverless 集群的安全连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)获取更多信息。

</CustomContent>

3. 输入密码以登录。

## 第 3 步：执行 SQL 语句

让我们尝试在 TiDB Cloud 上执行你的第一条 SQL 语句。

```sql
SELECT 'Hello TiDB Cloud!';
```

预期输出：

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

如果你的实际输出与预期输出类似，恭喜你已经成功在 TiDB Cloud 上执行了一条 SQL 语句。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
