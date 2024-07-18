---
title: ProxySQL 集成指南
summary: 了解如何将本地部署的 TiDB 或 TiDB Cloud 集群与 ProxySQL 集成。
---

# ProxySQL 集成指南

本文简要介绍 ProxySQL，描述如何在[开发环境](#开发环境)和[生产环境](#生产环境)中将 ProxySQL 与 TiDB 集成，并通过[查询规则的场景](#典型场景)展示集成的主要优势。

关于 TiDB 和 ProxySQL 的更多信息，请参考以下文档：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
- [TiDB 开发者指南](/develop/dev-guide-overview.md)
- [ProxySQL 文档](https://proxysql.com/documentation/)

## 什么是 ProxySQL？

[ProxySQL](https://proxysql.com/) 是一个高性能的开源 SQL 代理。它具有灵活的架构，可以通过多种方式部署，适合各类使用场景。例如，ProxySQL 可以通过缓存频繁访问的数据来提高性能。

ProxySQL 的设计目标是快速、高效且易于使用。它完全兼容 MySQL，并支持高质量 SQL 代理的所有功能。此外，ProxySQL 还提供了许多独特功能，使其成为各种应用程序的理想选择。

## 为什么集成 ProxySQL？

- ProxySQL 可以通过降低与 TiDB 交互的延迟来提升应用程序性能。无论你构建什么，无论是使用 Lambda 等无服务器函数的可扩展应用程序（其工作负载不确定并且可能激增），还是构建执行大量数据查询的应用程序，都可以利用 ProxySQL 的强大功能（例如[连接池](https://proxysql.com/documentation/detailed-answers-on-faq/)和[缓存常用查询](https://proxysql.com/documentation/query-cache/)）。
- ProxySQL 可以作为应用程序安全防护的附加层，使用[查询规则](#查询规则)防止 SQL 漏洞（例如 SQL 注入）。
- 由于 [ProxySQL](https://github.com/sysown/proxysql) 和 [TiDB](https://github.com/pingcap/tidb) 都是开源项目，你可以享受到零供应商锁定的好处。

## 部署架构

将 ProxySQL 与 TiDB 集成的最直接方式是在应用层和 TiDB 之间添加 ProxySQL 作为独立中介。但是，这种方式无法保证可扩展性和容错性，而且可能因为网络跳转而增加延迟。为避免这些问题，一种替代部署架构是将 ProxySQL 作为附属容器部署，如下图所示：

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注意：**
>
> 上图仅供参考，你需要根据实际的部署架构进行调整。

## 开发环境

本节介绍如何在开发环境中将 TiDB 与 ProxySQL 集成。在满足[前提条件](#前提条件)的情况下，你可以根据 TiDB 集群类型选择以下选项之一开始集成 ProxySQL：

- 选项 1：[集成 TiDB Cloud 与 ProxySQL](#选项-1-集成-tidb-cloud-与-proxysql)
- 选项 2：[集成本地部署的 TiDB 与 ProxySQL](#选项-2-集成本地部署的-tidb-与-proxysql)

### 前提条件

根据选择的方案，你可能需要以下依赖：

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)
- [Docker Compose](https://docs.docker.com/compose/install/linux/)
- [MySQL Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

你可以按照下面的说明进行安装：

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1. [下载](https://docs.docker.com/get-docker/)并启动 Docker，其中 Docker Desktop 已包含 Docker Compose。
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

    1. 从 [Download for Windows](https://git-scm.com/download/win) 页面下载 **64-bit Git for Windows Setup** 安装程序。
    2. 按照安装向导提示安装 Git。你可以多次点击 **Next** 使用默认的安装设置。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

- 下载并安装 MySQL Shell。

    1. 从 [MySQL Community Server Download](https://dev.mysql.com/downloads/mysql/) 页面下载 MySQL Installer 的 ZIP 文件。
    2. 解压文件，并在 `bin` 文件夹中找到 `mysql.exe`。你需要将该 `bin` 文件夹的路径添加到系统变量中，并在 Git Bash 中将其设置到 `PATH` 变量中。

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

    1. 从 [Docker Download](https://www.docker.com/products/docker-desktop/) 页面下载 Docker Desktop 安装程序。
    2. 双击安装程序运行。安装完成后，会提示你重新启动。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

- 从 [Python Download](https://www.python.org/downloads/) 页面下载最新版的 Python 3 安装程序并运行。

</div>

</SimpleTab>

### 选项 1: 集成 TiDB Cloud 与 ProxySQL

在这个集成中，你将使用 [ProxySQL Docker 镜像](https://hub.docker.com/r/proxysql/proxysql)以及 TiDB Serverless 集群。下面的步骤将在端口 `16033` 上设置 ProxySQL，请确保此端口可用。

#### 步骤 1. 创建一个 TiDB Serverless 集群

1. 参考[创建一个 TiDB Serverless 集群](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)文档。记住为集群设置的 root 密码。
2. 获取集群的 `hostname`、`port` 及 `username` 供后续使用。

    1. 在 [Clusters](https://tidbcloud.com/console/clusters) 页面，点击你的集群名称，进入集群概览页面。
    2. 在集群概览页面的 **Connection** 面板中，复制 `Endpoint`、`Port` 与 `User` 字段，其中 `Endpoint` 是集群的 `hostname`。

#### 步骤 2. 生成 ProxySQL 配置文件

1. 克隆 TiDB 和 ProxySQL 的集成示例代码仓库 [`tidb-proxysql-integration`](https://github.com/pingcap-inc/tidb-proxysql-integration)：

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

2. 进入 `tidb-cloud-connect` 目录：

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

    当出现提示时，输入集群的 `Endpoint` 作为 `Serverless Tier Host`，然后输入集群的 `Port` 与 `User`。

    下面是一个输出示例。可以看到，在当前的 `tidb-cloud-connect` 目录下生成了三个配置文件。

    ```
    [Begin] generating configuration files..
    tidb-cloud-connect.cnf generated successfully.
    proxysql-prepare.sql generated successfully.
    proxysql-connect.py generated successfully.
    [End] all files generated successfully and placed in the current folder.
    ```

#### 步骤 3. 配置 ProxySQL

1. 启动 Docker。如果 Docker 已经启动，请跳过此步骤:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 的图标来启动它。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 的图标来启动它。

    </div>

    </SimpleTab>

2. 拉取 ProxySQL 镜像，并在后台启动一个 ProxySQL 容器:

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

3. 运行以下命令集成 ProxySQL，该命令会在 **ProxySQL Admin Interface** 内执行 `proxysql-prepare.sql`：

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
    > 1. 使用集群的用户名和密码添加一个 ProxySQL 用户。
    > 2. 将该用户分配给监控账户。
    > 3. 将你的 TiDB Serverless 集群添加到主机列表中。
    > 4. 在 ProxySQL 和 TiDB Serverless 集群之间启用安全连接。
    >
    > 为了更好地理解此处的配置流程，强烈建议查看 `proxysql-prepare.sql` 文件。关于 ProxySQL 配置的更多信息，参考 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。

    下面是一个输出示例。输出中显示集群的主机名，这意味着 ProxySQL 和 TiDB Serverless 集群之间的连接建立成功。

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

1. 运行 `proxysql-connect.py` 连接到你的 TiDB 集群。该脚本将自动启动 MySQL 客户端并使用你在[步骤 2](#步骤-2-生成-proxysql-配置文件) 中指定的用户名和密码进行连接。

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

2. 连接 TiDB 集群后，可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果输出了 TiDB 的版本信息，则表示你已经成功通过 ProxySQL 连接到 TiDB Serverless 集群。如需退出 MySQL 客户端，输入 `quit` 并按下 <kbd>Enter</kbd> 键。

    > **注意：**
    >
    > **调试提示：** 如果无法连接到集群，请检查 `tidb-cloud-connect.cnf`、`proxysql-prepare.sql` 和 `proxysql-connect.py` 文件，确保你提供的服务器信息可用且正确。

3. 要停止和删除容器，并返回上一个目录，运行以下命令：

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

### 选项 2: 集成本地部署的 TiDB 与 ProxySQL

在这个集成中，你将使用 [TiDB](https://hub.docker.com/r/pingcap/tidb) 和 [ProxySQL](https://hub.docker.com/r/proxysql/proxysql) 的 Docker 镜像设置环境。你也可以尝试[其他方式安装 TiDB](/quick-start-with-tidb.md)。

下面的步骤将在端口 `6033` 和 `4000` 上分别设置 ProxySQL 和 TiDB，请确保这些端口可用。

1. 启动 Docker。如果 Docker 已经启动，请跳过此步骤：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 的图标来启动它。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 的图标来启动它。

    </div>

    </SimpleTab>

2. 克隆 TiDB 和 ProxySQL 的集成示例代码仓库 [`pingcap-inc/tidb-proxysql-integration`](https://github.com/pingcap-inc/tidb-proxysql-integration)：

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

3. 拉取 ProxySQL 和 TiDB 的最新镜像：

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

4. 使用 TiDB 和 ProxySQL 容器启动一个集成环境：

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

    你可以使用 `root` 用户名及空密码登录到 ProxySQL 的 `6033` 端口。

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

6. 连接 TiDB 集群后，可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果输出了 TiDB 的版本信息，则表示你已经成功通过 ProxySQL 连接到 TiDB 集群。

7. 要停止和删除容器，并返回上一个目录，运行以下命令：

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

对于生产环境，建议直接使用 [TiDB Dedicated](https://www.pingcap.com/tidb-dedicated/) 以获得完全托管的体验。

### 前提条件

下载并安装一个 MySQL 客户端。例如，[MySQL Shell](https://dev.mysql.com/downloads/shell/)。

### 基于 CentOS 集成 TiDB Cloud 与 ProxySQL

你可以在不同的平台上安装 ProxySQL，下面以 CentOS 为例进行说明。

关于 ProxySQL 支持的平台和版本要求的完整列表，见 [ProxySQL 文档](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 1. 创建一个 TiDB Dedicated 集群

具体步骤请参考[创建一个 TiDB Dedicated 集群](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)。

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

要了解更多关于 ProxySQL 支持的平台及其安装方法，参考 [ProxySQL README](https://github.com/sysown/proxysql#installation) 或 [ProxySQL 安装文档](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 3. 配置 ProxySQL

为了使用 ProxySQL 作为 TiDB 的代理，你需要配置 ProxySQL。你可以[在 ProxySQL Admin Interface 中执行 SQL 语句](#选项-1-使用-admin-interface-配置-proxysql)（推荐）或[使用配置文件](#选项-2-使用配置文件配置-proxysql)进行配置。

> **注意：**
>
> 以下章节仅列出 ProxySQL 的必要配置项。
>
> 完整的配置信息，可参考 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。

##### 选项 1: 使用 Admin Interface 配置 ProxySQL

1. 使用标准的 ProxySQL Admin Interface 更新 ProxySQL 的配置。你可以通过任何 MySQL 命令行客户端访问（默认端口为 `6032`）。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    执行以上命令后，系统将显示 `'ProxySQL Admin'` 提示。

2. 你可以在当前 MySQL 命令行客户端中向 ProxySQL 添加一个或多个 TiDB 集群。例如，下面的语句将添加一个 TiDB Dedicated 集群。你需要用集群的 `Endpoint` 和 `Port` 替换 `<tidb cloud dedicated cluster host>` 和 `<tidb cloud dedicated cluster port>`（默认端口为 `4000`）。

    ```sql
    INSERT INTO mysql_servers(hostgroup_id, hostname, port)
    VALUES
      (
        0,
        '<tidb cloud dedicated cluster host>',
        <tidb cloud dedicated cluster port>
      );
    LOAD mysql servers TO runtime;
    SAVE mysql servers TO DISK;
    ```

    > **注意：**
    >
    > - `hostgroup_id`：指定一个 **hostgroup** 的 ID。ProxySQL 使用 **hostgroup** 管理集群。如果需要将 SQL 流量均匀地分配给这些集群，你可以将需要负载均衡的几个 TiDB 集群配置到同一个 **hostgroup** 中。另一方面，为了区分不同的集群，例如为了实现读写分离，你可以将它们配置为不同的 **hostgroup** ID。
    > - `hostname`：TiDB 集群的 `Endpoint`。
    > - `port`：TiDB 集群的 `Port`。

3. 为配置 ProxySQL 的登录用户，你需要确保用户在 TiDB 集群上有适当的权限。在下面的语句中，你需要把 `<tidb cloud dedicated cluster username>` 和 `<tidb cloud dedicated cluster password>` 替换为集群的实际用户名和密码。

    ```sql
    INSERT INTO mysql_users(
      username, password, active, default_hostgroup,
      transaction_persistent
    )
    VALUES
      (
        '<tidb cloud dedicated cluster username>',
        '<tidb cloud dedicated cluster password>',
        1, 0, 1
      );
    LOAD mysql users TO runtime;
    SAVE mysql users TO DISK;
    ```

    > **注意：**
    >
    > - `username`：TiDB 用户名。
    > - `password`：TiDB 密码。
    > - `active`：指定用户是否处于激活状态。`1` 表示该用户是**激活的**，可以用于登录，`0` 表示该用户是非激活的。
    > - `default_hostgroup`：用户使用的默认 `hostgroup`，除非特定的查询规则覆盖了 `hostgroup`，否则 SQL 将会默认路由到 `default_hostgroup`。
    > - `transaction_persistent`：值为 `1` 表示使用持久性事务。即当用户在一个连接中启动一个事务时，所有的查询语句都被路由到同一个 `hostgroup`，直到事务被提交或回滚。

##### 选项 2: 使用配置文件配置 ProxySQL

这个选项只能作为配置 ProxySQL 的备用方案。更多信息，可参考[使用配置文件配置 ProxySQL](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)。

1. 删除现有的 SQLite 数据库，即 ProxySQL 存储配置的位置。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > 删除 SQLite 数据库后，通过 ProxySQL Admin Interface 所做的任何配置更改都会丢失。

2. 根据你的需要修改配置文件 `/etc/proxysql.cnf`。例如：

    ```
    mysql_servers:
    (
        {
            address="<tidb cloud dedicated cluster host>"
            port=<tidb cloud dedicated cluster port>
            hostgroup=0
            max_connections=2000
        }
    )

    mysql_users:
    (
        {
            username = "<tidb cloud dedicated cluster username>"
            password = "<tidb cloud dedicated cluster password>"
            default_hostgroup = 0
            max_connections = 1000
            default_schema = "test"
            active = 1
            transaction_persistent = 1
        }
    )
    ```

    在上面的例子中:

    - `address` 和 `port` 用于指定你的 TiDB Cloud 集群的 `Endpoint` 和 `Port`。
    - `username` 和 `password` 用于指定你的 TiDB Cloud 集群的用户名和密码。

3. 重启 ProxySQL：

    ```bash
    systemctl restart proxysql
    ```

    重新启动后，ProxySQL 将自动创建 SQLite 数据库。

> **警告：**
>
> 在生产环境中，不要使用默认的管理员用户运行 ProxySQL。在启动 `proxysql` 服务之前，你可以通过修改 [`admin_credentials`](https://proxysql.com/documentation/global-variables/admin-variables/#admin-admin_credentials) 变量更改 `/etc/proxysql.cnf` 文件中的默认值。

## 典型场景

本节以查询规则为例，介绍集成 TiDB 与 ProxySQL 能带来的一些优势。

### 查询规则

数据库可能会因为高流量、错误代码或恶意攻击而过载。因此，审核 SQL 是必要的。使用 ProxySQL 的查询规则，你可以有效地应对这些问题，例如通过重路由、改写 SQL 或者拒绝查询等方式。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注意：**
>
> 以下步骤使用 TiDB 和 ProxySQL 的容器镜像配置查询规则。如果你还没有拉取这些镜像，请参考[集成本地部署的 TiDB 与 ProxySQL](#选项-2-集成本地部署的-tidb-与-proxysql) 部分的详细步骤。

1. 克隆 TiDB 和 ProxySQL 的集成示例代码仓库 [`pingcap-inc/tidb-proxysql-integration`](https://github.com/pingcap-inc/tidb-proxysql-integration)。如果你已经在前面的步骤中克隆了它，请跳过这一步。

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

2. 进入 ProxySQL 查询规则的示例目录：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    </SimpleTab>

3. 运行下面的命令启动两个 TiDB 容器和一个 ProxySQL 容器：

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

    如果运行成功，以下容器将被启动：

    - 两个 Docker 容器的 TiDB 集群，端口分别为 `4001` 和 `4002`
    - 一个 Docker 容器的 ProxySQL，端口为 `6034`

4. 在两个 TiDB 容器中，使用 `mysql` 创建一个具有相同 schema 的表，然后插入不同的数据 (`'tidb-server01-port-4001'`, `'tidb-server02-port-4002'`) 以区分这两个容器。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    </SimpleTab>

5. 运行下面的命令配置 ProxySQL，该命令会在 ProxySQL Admin Interface 中执行 `proxysql-prepare.sql`，从而在 TiDB 容器和 ProxySQL 之间建立一个代理连接。

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
    > `proxysql-prepare.sql` 脚本完成以下操作：
    >
    > - 在 ProxySQL 中添加 TiDB 集群，`hostgroup_id` 分别为 `0` 和 `1`。
    > - 添加一个用户 `root`，密码为空，并设置 `default_hostgroup` 为 `0`。
    > - 添加规则 `^SELECT.*FOR UPDATE$`，`rule_id` 为 `1`，`destination_hostgroup` 为 `0`。这代表如果一个 SQL 语句与此规则相匹配，该请求将被转发到 `hostgroup` 为 `0` 的 TiDB 集群。
    > - 添加规则 `^SELECT`，`rule_id` 为 `2`，`destination_hostgroup` 为 `1`。这代表如果一个 SQL 语句与此规则相匹配，该请求将被转发到 `hostgroup` 为 `1` 的 TiDB 集群。
    >
    > 为了更好地理解此处的配置流程，强烈建议查看 `proxysql-prepare.sql` 文件。关于 ProxySQL 配置的更多信息，参考 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。

    下面是关于 ProxySQL 匹配 SQL 查询的规则的一些补充信息：

    - ProxySQL 尝试按照 `rule_id` 的升序逐一匹配规则。
    - 规则中的 `^` 符号用于匹配 SQL 语句的开头，`$` 符号用于匹配语句的结尾。

    关于 ProxySQL 正则表达式和模式匹配的更多信息，参考 ProxySQL 文档 [`mysql-query_processor_regex`](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)。

    关于完整的参数列表，参考 ProxySQL 文档 [`mysql_query_rules`](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)。

6. 验证配置并检查查询规则是否有效。

    1. 使用 `root` 用户登录 ProxySQL MySQL Interface：

        <SimpleTab groupId="os">

        <div label="macOS" value="macOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="CentOS" value="CentOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="Windows (Git Bash)" value="Windows">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        </SimpleTab>

    2. 执行以下 SQL 语句：

        - 执行一个 `SELECT` 语句：

            ```sql
            SELECT * FROM test.tidb_server;
            ```

            这个语句将匹配 `rule_id` 为 `2` 的规则，因此将转发语句到 `hostgroup` 为 `1` 上的 TiDB 集群中。

        - 执行一个 `SELECT ... FOR UPDATE` 语句：

            ```sql
            SELECT * FROM test.tidb_server FOR UPDATE;
            ```

            这个语句将匹配 `rule_id` 为 `1` 的规则，因此将转发语句到 `hostgroup` 为 `0` 上的 TiDB 集群中。

        - 启动一个事务：

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            在这个事务中，`BEGIN` 语句将不会匹配任何规则。因此，它将使用默认的 `hostgroup`（在这个例子中为 `hostgroup 0`）。因为 ProxySQL 默认启用了用户 transaction_persistent，它将在同一事务中，将所有语句都转发至相同的 `hostgroup`，所以 `INSERT` 和 `SELECT * FROM test.tidb_server;` 语句也将被转发到 `hostgroup` 为 `0` 的 TiDB 集群。

        下面是一个输出示例。如果你得到类似的输出，表示你已经成功配置了 ProxySQL 的查询规则。

        ```sql
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server02-port-4002 |
        +-------------------------+
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server01-port-4001 |
        +-------------------------+
        +--------------------------------+
        | server_name                    |
        +--------------------------------+
        | tidb-server01-port-4001        |
        | insert this and rollback later |
        +--------------------------------+
        ```

    3. 如需退出 MySQL 客户端，输入 `quit` 并按下 <kbd>Enter</kbd> 键。

7. 要停止和删除容器，并返回上一个目录，运行以下命令：

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