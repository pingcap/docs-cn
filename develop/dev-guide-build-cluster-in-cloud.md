---
title: 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群
summary: 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群，并连接 TiDB Cloud 集群。
---

<!-- markdownlint-disable MD029 -->

# 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群

本章节将介绍如何以最快的方式开始使用 TiDB。你将使用 [TiDB Cloud](https://en.pingcap.com/tidb-cloud) 创建并启动一个 Serverless Tier 集群，使用 TiDB SQL 客户端，插入数据。随后将从示例程序读取出数据。

若你需要在本地计算机上启动 TiDB，请参阅[本地启动 TiDB](/quick-start-with-tidb.md)。

## 第 1 步：创建 Serverless Tier 集群

1. 如果你还未拥有 TiDB Cloud 帐号，请先在此[注册](https://tidbcloud.com/free-trial)。
2. 使用你的 TiDB Cloud 帐号[登录](https://tidbcloud.com/)。
3. 在 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中点击 **Create Cluster** 按钮。
4. **Create Cluster** 页面默认选择 **Serverless Tier**。你可以根据需要修改集群名称并选择可用区。
5. 点击 **Create** 创建 Serverless Tier 集群。

    你的 TiDB Cloud 集群将于 30 秒后创建完毕。

6. 集群创建完毕后，点击 **...** 按钮，在下拉框中选择 **Security Settings** 按钮。在对话框中设置连接集群的 root 密码，完成后点击 **Apply**。如果没有设置 root 密码，你将无法连接集群。
7. 点击 **Connect** 按钮，在连接对话框中选择你需要的连接方式和操作系统并保存对应的连接字符串。下面连接到集群步骤以 MySQL 客户端为例。

    > **注意：**
    >
    > 需要特别说明的是，在你使用 [Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier) 集群时，你需要给你设置的用户名加上前缀（如 `2aEp24QWEDLqRFs.root` 中的 `2aEp24QWEDLqRFs`），若使用命令行连接，还需使用单引号包裹用户名。你可以在 [TiDB Cloud 用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix) 中获得更多信息。

## 第 2 步：连接到集群

1. 若未安装 MySQL 客户端，请选择自己的操作系统，按以下步骤安装。

    <SimpleTab>

    <div label="macOS">

    对于 macOS 操作系统，如果你没有安装 Homebrew，请参考 [Homebrew 官网](https://brew.sh/index_zh-cn)进行安装。

    {{< copyable "shell-regular" >}}

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

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
    ```

    完成后，生效该配置文件（例如 `~/.zshrc`），并验证 MySQL 客户端是否安装成功：

    {{< copyable "shell-regular" >}}

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

    {{< copyable "shell-root" >}}

    ```shell
    yum install mysql
    ```

    完成后，请验证 MySQL 客户端是否安装成功：

    {{< copyable "shell-regular" >}}

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

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注意：**
>
> - 在连接 Serverless Tier 集群时，[必须使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)。
> - 如果你在连接时遇到问题，可阅读 [TiDB Cloud Serverless Tier 集群安全连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters) 来获得更多信息。

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