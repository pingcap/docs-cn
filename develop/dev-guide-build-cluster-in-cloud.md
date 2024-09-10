---
title: 使用 TiDB Cloud Serverless 构建 TiDB 集群
summary: 使用 TiDB Cloud Serverless 构建 TiDB 集群，并连接 TiDB Cloud Serverless 集群。
---

<!-- markdownlint-disable MD029 -->

# 使用 TiDB Cloud Serverless 构建 TiDB 集群

本文将介绍如何以最快的方式开始使用 TiDB。你将创建并启动一个 [TiDB Cloud Serverless](https://www.pingcap.com/tidb-serverless/) 集群，使用 TiDB SQL 客户端，插入数据。随后将从示例程序读取出数据。

若你需要在本地计算机上启动 TiDB，请参阅[本地启动 TiDB](/quick-start-with-tidb.md)。

## 第 1 步：创建 TiDB Cloud Serverless 集群

1. 如果你还未拥有 TiDB Cloud 账号，请先在此[注册](https://tidbcloud.com/free-trial)。
2. 使用你的 TiDB Cloud 账号[登录](https://tidbcloud.com/)。

    登录后，默认进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面。

3. 对于新注册的用户，TiDB Cloud 会自动为你创建一个 TiDB Cloud Serverless 集群 `Cluster0`。你可以使用这个默认集群进行后续操作，也可以自行创建一个新的 TiDB Cloud Serverless 集群。

    如果你想创建一个新的 TiDB Cloud Serverless 集群，请进行以下操作：

    1. 点击 **Create Cluster**。
    2. **Create Cluster** 页面默认选择 **Serverless**。你可以根据需要修改集群名称、选择可用区，然后点击 **Create**。你的 TiDB Cloud Serverless 集群将于 30 秒后创建完毕。

4. 点击目标集群名称，进入集群概览页面，然后点击右上角的 **Connect** 按钮，弹出连接对话框。

5. 在对话框中，选择你需要的连接方式和操作系统并保存对应的连接字符串。下面连接到集群的步骤将以 MySQL 客户端为例。

6. 点击 **Generate Password** 生成随机密码。生成的密码不会再次显示，因此请将密码妥善保存。如果没有设置 root 密码，你将无法连接到集群。

    > **注意：**
    >
    > 在连接到 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群时，你需要给用户名加上前缀并使用单引号包裹用户名。你可以在 [TiDB Cloud Serverless 用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix) 中获得更多信息。

## 第 2 步：连接到集群

1. 若未安装 MySQL 客户端，请选择自己的操作系统，按以下步骤安装。

    <SimpleTab>

    <div label="macOS">

    对于 macOS 操作系统，如果你没有安装 Homebrew，请参考 [Homebrew 官网](https://brew.sh/zh-cn/)进行安装。

    ```shell
    brew install mysql-client
    ```

    在安装完成的命令行输出中，得到以下信息：

    ```
    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).

    If you need to have mysql-client first in your PATH, run:
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

    For compilers to find mysql-client you may need to set:
    export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
    ```

    请运行其中的此行（命令行输出若与此处文档不一致，请以命令行输出为准）：

    ```shell
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
    ```

    完成后，生效该配置文件（例如 `~/.zshrc`），并验证 MySQL 客户端是否安装成功：

    ```shell
    source ~/.zshrc
    mysql --version
    ```

    预期会得到形如以下的输出：

    ```
    mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
    ```

    </div>

    <div label="Linux">

    对于 Linux 操作系统，下面以 CentOS 7 为例：

    ```shell
    yum install mysql
    ```

    完成后，请验证 MySQL 客户端是否安装成功：

    ```shell
    mysql --version
    ```

    预期会得到形如以下的输出：

    ```
    mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
    ```

    </div>

    </SimpleTab>

2. 运行第 1 步中得到的连接字符串。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注意：**
>
> - 在连接 TiDB Cloud Serverless 集群时，[必须使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)。
> - 如果你在连接时遇到问题，可阅读 [TiDB Cloud Serverless 集群安全连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters) 来获得更多信息。

3. 填写密码，完成登录。

## 第 3 步：运行 SQL

尝试运行一下你在 TiDB Cloud 上的的第一个 SQL 吧：

```sql
SELECT 'Hello TiDB Cloud!';
```

你将看到这样的输出：

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

如果你的实际输出与预期输出一致，表示你已经在 TiDB Cloud 上成功地运行了 SQL 语句。
