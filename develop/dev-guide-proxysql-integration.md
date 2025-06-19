---
title: 将 TiDB 与 ProxySQL 集成
summary: 了解如何将 ProxySQL 与 TiDB 集成。
---

# 将 TiDB 与 ProxySQL 集成

本文提供了对 ProxySQL 的高级介绍，描述了如何在[开发环境](#开发环境)和[生产环境](#生产环境)中将 ProxySQL 与 TiDB 集成，并通过[查询路由场景](#典型场景)演示了关键的集成优势。

如果您想了解更多关于 TiDB 和 ProxySQL 的信息，可以参考以下有用的链接：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
- [TiDB 开发者指南](/develop/dev-guide-overview.md)
- [ProxySQL 文档](https://proxysql.com/documentation/)

## 什么是 ProxySQL？

[ProxySQL](https://proxysql.com/) 是一个高性能的开源 SQL 代理。它具有灵活的架构，可以以多种不同方式部署，非常适合各种用例。例如，ProxySQL 可以通过缓存频繁访问的数据来提高性能。

ProxySQL 从一开始就被设计为快速、高效和易于使用。它完全兼容 MySQL，并支持您期望从高质量 SQL 代理获得的所有功能。此外，ProxySQL 还具有许多独特的功能，使其成为广泛应用的理想选择。

## 为什么要集成 ProxySQL？

- ProxySQL 可以通过减少与 TiDB 交互时的延迟来帮助提升应用程序性能。无论您是使用 Lambda 等无服务器函数构建可扩展应用程序（其中工作负载是不确定的并且可能出现峰值），还是构建执行加载大量数据的查询的应用程序。通过利用 ProxySQL 的强大功能，如[连接池](https://proxysql.com/documentation/detailed-answers-on-faq/)和[频繁使用的查询缓存](https://proxysql.com/documentation/query-cache/)，应用程序可以立即获得好处。
- ProxySQL 可以通过[查询规则](#查询规则)（ProxySQL 中一个易于配置的功能）充当应用程序安全保护的额外层，防止 SQL 注入等 SQL 漏洞。
- 由于 [ProxySQL](https://github.com/sysown/proxysql) 和 [TiDB](https://github.com/pingcap/tidb) 都是开源项目，您可以获得零供应商锁定的好处。

## 部署架构

将 ProxySQL 与 TiDB 集成最明显的方式是将 ProxySQL 作为应用层和 TiDB 之间的独立中介。但是，这种方式无法保证可扩展性和故障容忍性，而且由于网络跳转也会增加额外的延迟。为了避免这些问题，一种替代的部署架构是将 ProxySQL 作为边车部署，如下所示：

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注意：**
>
> 上述图示仅供参考。您必须根据实际部署架构进行调整。

## 开发环境

本节描述如何在开发环境中将 TiDB 与 ProxySQL 集成。要开始 ProxySQL 集成，在准备好所有[前提条件](#前提条件)后，您可以根据 TiDB 集群类型选择以下任一选项。

- 选项 1：[将 TiDB Cloud 与 ProxySQL 集成](#选项-1-将-tidb-cloud-与-proxysql-集成)
- 选项 2：[将 TiDB（自托管）与 ProxySQL 集成](#选项-2-将-tidb-自托管与-proxysql-集成)

### 前提条件

根据您选择的选项，您可能需要以下软件包：

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)
- [Docker Compose](https://docs.docker.com/compose/install/linux/)
- [MySQL Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

您可以按照以下说明进行安装：

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1. [下载](https://docs.docker.com/get-docker/)并启动 Docker（Docker Desktop 已包含 Docker Compose）。
2. 运行以下命令安装 Python 和 `mysql-client`：

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python mysql-client
    ```

</div>

<div label="CentOS" value="CentOS">

```bash
curl -fsSL https://get.docker.com | bash -s docker
yum install -y git python39 docker-ce docker-ce-cli containerd.io docker-compose-plugin mysql
systemctl start docker
```

</div>

<div label="Windows" value="Windows">

- 下载并安装 Git。

    1. 从 [Git Windows 下载](https://git-scm.com/download/win)页面下载 **64-bit Git for Windows Setup** 包。
    2. 按照安装向导安装 Git 包。您可以点击**下一步**几次使用默认安装设置。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

- 下载并安装 MySQL Shell。

    1. 从 [MySQL Community Server 下载](https://dev.mysql.com/downloads/mysql/)页面下载 MySQL 安装程序的 ZIP 文件。
    2. 解压文件，找到 `bin` 文件夹中的 `mysql.exe`。您需要将 `bin` 文件夹的路径添加到系统变量中，并在 Git Bash 中设置到 `PATH` 变量：

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        例如：

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

- 下载并安装 Docker。

    1. 从 [Docker 下载](https://www.docker.com/products/docker-desktop/)页面下载 Docker Desktop 安装程序。
    2. 双击安装程序运行。安装完成后，系统会提示重启。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

- 从 [Python 下载](https://www.python.org/downloads/)页面下载最新的 Python 3 安装程序并运行。

</div>

</SimpleTab>

### 选项 1. 将 TiDB Cloud 与 ProxySQL 集成

对于此集成，您将使用 [ProxySQL Docker 镜像](https://hub.docker.com/r/proxysql/proxysql)和 TiDB Cloud Serverless 集群。以下步骤将在端口 `16033` 上设置 ProxySQL，因此请确保此端口可用。

#### 步骤 1. 创建 TiDB Cloud Serverless 集群

1. [创建一个免费的 TiDB Cloud Serverless 集群](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)。记住您为集群设置的 root 密码。
2. 获取集群主机名、端口和用户名以供后续使用。

    1. 在[集群](https://tidbcloud.com/project/clusters)页面上，点击集群名称进入集群概览页面。
    2. 在集群概览页面上，找到**连接**窗格，然后复制 `Endpoint`、`Port` 和 `User` 字段，其中 `Endpoint` 是您的集群主机名。

#### 步骤 2. 生成 ProxySQL 配置文件

1. 克隆 TiDB 和 ProxySQL 的[集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

2. 切换到 `tidb-cloud-connect` 文件夹：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    </SimpleTab>

3. 运行 `proxysql-config.py` 生成 ProxySQL 配置文件：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-config.py
    ```

    </div>

    </SimpleTab>

    当出现提示时，输入集群的 `Serverless Tier Host` 端点，然后输入集群的用户名和密码。

    以下是示例输出。您将看到在当前 `tidb-cloud-connect` 文件夹下生成了三个配置文件。

    ```
    [Begin] generating configuration files..
    tidb-cloud-connect.cnf generated successfully.
    proxysql-prepare.sql generated successfully.
    proxysql-connect.py generated successfully.
    [End] all files generated successfully and placed in the current folder.
    ```

#### 步骤 3. 配置 ProxySQL

1. 启动 Docker。如果 Docker 已经启动，跳过此步骤：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 图标启动它。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 图标启动它。

    </div>

    </SimpleTab>

2. 拉取 ProxySQL 镜像并在后台启动 ProxySQL 容器：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

3. 通过运行以下命令与 ProxySQL 集成，该命令在 **ProxySQL Admin Interface** 中执行 `proxysql-prepare.sql`：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    </SimpleTab>

    > **注意：**
    >
    > `proxysql-prepare.sql` 脚本执行以下操作：
    >
    > 1. 使用集群的用户名和密码添加用户。
    > 2. 将用户分配给监控账户。
    > 3. 将您的 TiDB Cloud Serverless 集群添加到主机列表中。
    > 4. 启用 ProxySQL 和 TiDB Cloud Serverless 集群之间的安全连接。
    >
    > 强烈建议您查看 `proxysql-prepare.sql` 文件以更好地理解。要了解更多关于 ProxySQL 配置的信息，请参见 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。

    以下是示例输出。如果您看到集群的主机名显示在输出中，这意味着 ProxySQL 和 TiDB Cloud Serverless 集群之间的连接已建立。

    ```
    *************************** 1. row ***************************
        hostgroup_id: 0
            hostname: gateway01.us-west-2.prod.aws.tidbcloud.com
                port: 4000
            gtid_port: 0
                status: ONLINE
                weight: 1
            compression: 0
        max_connections: 1000
    max_replication_lag: 0
                use_ssl: 1
        max_latency_ms: 0
                comment:
    ```

#### 步骤 4. 通过 ProxySQL 连接到 TiDB 集群

1. 要连接到 TiDB 集群，运行 `proxysql-connect.py`。该脚本将自动启动 MySQL 客户端，并使用您在[步骤 2](#步骤-2-生成-proxysql-配置文件)中指定的用户名和密码进行连接。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-connect.py
    ```

    </div>

    </SimpleTab>

2. 连接到 TiDB 集群后，您可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果显示了 TiDB 版本，说明您已成功通过 ProxySQL 连接到 TiDB Cloud Serverless 集群。要随时退出 MySQL 客户端，输入 `quit` 并按 <kbd>enter</kbd>。

    > **注意：**
    >
    > ***调试提示：*** 如果无法连接到集群，请检查文件 `tidb-cloud-connect.cnf`、`proxysql-prepare.sql` 和 `proxysql-connect.py`。确保您提供的服务器信息可用且正确。

3. 要停止并删除容器，并返回上一个目录，运行以下命令：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

### 选项 2. 将 TiDB（自托管）与 ProxySQL 集成

对于此集成，您将使用 [TiDB](https://hub.docker.com/r/pingcap/tidb) 和 [ProxySQL](https://hub.docker.com/r/proxysql/proxysql) 的 Docker 镜像设置环境。我们鼓励您尝试[其他安装 TiDB（自托管）的方式](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)。

以下步骤将在端口 `6033` 和 `4000` 上分别设置 ProxySQL 和 TiDB，因此请确保这些端口可用。

1. 启动 Docker。如果 Docker 已经启动，跳过此步骤：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 图标启动它。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 图标启动它。

    </div>

    </SimpleTab>

2. 克隆 TiDB 和 ProxySQL 的[集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

3. 拉取最新的 ProxySQL 和 TiDB 镜像：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    </SimpleTab>

4. 使用 TiDB 和 ProxySQL 作为容器启动集成环境：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

    要登录到 ProxySQL 的 `6033` 端口，您可以使用 `root` 用户名和空密码。

5. 通过 ProxySQL 连接到 TiDB：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    </SimpleTab>

6. 连接到 TiDB 集群后，您可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果显示了 TiDB 版本，说明您已成功通过 ProxySQL 连接到 TiDB 容器。

7. 要停止并删除容器，并返回上一个目录，运行以下命令：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

## 生产环境

对于生产环境，建议您直接使用 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated/) 以获得完全托管的体验。

### 前提条件

下载并安装 MySQL 客户端。例如，[MySQL Shell](https://dev.mysql.com/downloads/shell/)。

### 在 CentOS 上将 TiDB Cloud 与 ProxySQL 集成

ProxySQL 可以安装在多个不同的平台上。以下以 CentOS 为例。

有关支持的平台和相应版本要求的完整列表，请参见 [ProxySQL 文档](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 1. 创建 TiDB Cloud Dedicated 集群

有关详细步骤，请参见[创建 TiDB 集群](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)。

#### 步骤 2. 安装 ProxySQL

1. 将 ProxySQL 添加到 YUM 仓库：

    ```bash
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. 安装 ProxySQL：

    ```bash
    yum install -y proxysql
    ```

3. 启动 ProxySQL：

    ```bash
    systemctl start proxysql
    ```

要了解更多关于 ProxySQL 支持的平台及其安装的信息，请参考 [ProxySQL README](https://github.com/sysown/proxysql#installation) 或 [ProxySQL 安装文档](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 3. 配置 ProxySQL

要将 ProxySQL 用作 TiDB 的代理，您需要配置 ProxySQL。为此，您可以选择[在 ProxySQL Admin Interface 中执行 SQL 语句](#选项-1-使用管理界面配置-proxysql)（推荐）或使用[配置文件](#选项-2-使用配置文件配置-proxysql)。

> **注意：**
>
> 以下部分仅列出了 ProxySQL 的必需配置项。
> 有关配置的完整列表，请参见 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。
