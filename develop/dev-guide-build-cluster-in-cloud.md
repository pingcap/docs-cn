---
title: 创建 {{{ .starter }}} 实例
summary: 使用 {{{ .starter }}} 构建 TiDB 实例，并连接到该实例。
aliases: ['/zh/tidb/dev/build-cluster-in-cloud','/zh/tidb/stable/dev-guide-build-cluster-in-cloud/','/zh/tidb/dev/dev-guide-build-cluster-in-cloud/','/zh/tidbcloud/dev-guide-build-cluster-in-cloud/']
---

<!-- markdownlint-disable MD029 -->

# 创建 {{{ .starter }}} 实例

本文将介绍如何以最快的方式开始使用 TiDB。你将创建并启动一个 [{{{ .starter }}}](https://www.pingcap.com/tidb-cloud-starter/) 实例，使用 TiDB SQL 客户端，插入数据。随后将从示例程序读取出数据。

若你需要在本地计算机上启动 TiDB，请参阅[本地启动 TiDB](/quick-start-with-tidb.md)。

## 第 1 步：创建 {{{ .starter }}} 实例 {#step-1-create-a-starter-instance}

1. 如果你没有 TiDB Cloud 账户，请点击[此处](https://tidbcloud.com/free-trial)注册。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账户。

3. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击 **Create Resource**。

4. 在 **Create Resource*** 页面，**Starter** 为默认选项。为你的 {{{ .starter }}} 实例输入一个名称，选择云服务提供商，然后选择一个可用区。

5. 点击 **Create** 以创建 {{{ .starter }}} 实例。

    你的 {{{ .starter }}} 实例将在约 30 秒内创建完成。

6. 在你的 {{{ .starter }}} 实例创建完成后，点击实例名称进入其概览页面，然后点击右上角的 **Connect**。此时会显示一个连接对话框。

7. 在对话框中，选择你所需的连接方式和操作系统，获取对应的连接字符串。本文档以 MySQL 客户端为例。

8. 点击 **Generate Password** 生成随机密码。生成的密码不会再次显示，因此请将密码妥善保存。如果没有设置 root 密码，你将无法连接到 {{{ .starter }}} 实例。

> **注意：**
>
> 当连接到 {{{ .starter }}} 实例时，必须在用户名前加上前缀并使用单引号包裹用户名。你可以在 [{{{ .starter }}} 用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)中获得更多信息。

## 第 2 步：连接到 {{{ .starter }}} 实例 {#step-2-connect-to-a-starter-instance}

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

    对于 Linux 操作系统，下面以 Ubuntu 为例：

    ```shell
    apt-get install mysql-client
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

2. 运行[第 1 步](#step-1-create-a-starter-instance)中得到的连接字符串。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注意：**
>
> - 在连接 {{{ .starter }}} 实例时，[必须使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)。
> - 如果你在连接时遇到问题，可阅读 [{{{ .starter }}} 实例安全连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)来获得更多信息。

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
