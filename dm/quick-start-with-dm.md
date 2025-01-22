---
title: TiDB Data Migration 快速上手指南
summary: 了解如何使用 TiUP Playground 快速部署试用 TiDB Data Migration 工具。
aliases: ['/docs-cn/tidb-data-migration/dev/quick-start-with-dm/','/docs-cn/tidb-data-migration/dev/get-started/']
---

# TiDB Data Migration 快速上手指南

[TiDB Data Migration (DM)](/dm/dm-overview.md) 是一个强大的数据迁移工具，用于将数据从兼容 MySQL 的数据库迁移到 TiDB。本指南将介绍如何使用 [TiUP Playground](/tiup/tiup-playground.md) 在本地快速搭建 TiDB DM 环境，以用于开发和测试。

> **注意：**
>
> 对于生产环境部署，请参阅[使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)。

## 第 1 步：搭建测试环境

[TiUP](/tiup/tiup-overview.md) 是一个集群运维工具。使用它的 Playground 可以快速启动一个用于开发和测试的临时本地环境，包含 TiDB 数据库和 TiDB DM。

1. 安装 TiUP：

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    > **注意：**
    >
    > 如果你已经安装了 TiUP，请确保其版本为 v1.16.1 或更高版本，以便使用 `--dm-master` 和 `--dm-worker` 参数。如果要检查当前版本，执行以下命令：
    >
    > ```shell
    > tiup --version
    > ```
    >
    > 如果要将 TiUP 升级到最新版本，执行以下命令：
    >
    > ```shell
    > tiup update --self
    > ```

2. 启动 TiUP Playground，TiDB 目标数据库，以及 DM 组件：

    ```shell
    tiup playground --dm-master 1 --dm-worker 1 --tiflash 0 --without-monitor
    ```

3. 验证环境，查看输出中 TiDB 和 DM 是否已启动：

    ```text
    TiDB Playground Cluster is started, enjoy!

    Connect TiDB:    mysql --host 127.0.0.1 --port 4000 -u root
    Connect DM:      tiup dmctl --master-addr 127.0.0.1:8261
    TiDB Dashboard:  http://127.0.0.1:2379/dashboard
    ```

4. 保持 `tiup playground` 在当前终端中运行，并在新终端中执行后续步骤。

    这个 Playground 环境提供了目标 TiDB 数据库和复制引擎（DM-master 和 DM-worker）的运行进程。它将处理的数据流为：MySQL（源）→ DM（复制引擎）→ TiDB（目标）。

## 第 2 步：准备源数据库（可选）

你可以使用一个或多个 MySQL 实例作为源数据库。如果你已经有一个兼容 MySQL 的实例，请跳到[第 3 步](#第-3-步配置-tidb-dm-源)；如果没有，则按照以下步骤创建一个用于测试的实例。

<SimpleTab groupId="os">

<div label="Docker" value="docker">

你可以使用 Docker 快速部署一个 MySQL 8.0 测试实例。

1. 运行 MySQL 8.0 Docker 容器：

    ```shell
    docker run --name mysql80 \
        -e MYSQL_ROOT_PASSWORD=MyPassw0rd! \
        -p 3306:3306 \
        -d mysql:8.0
    ```

2. 连接到 MySQL：

    ```shell
    docker exec -it mysql80 mysql -uroot -pMyPassw0rd!
    ```

3. 创建一个 DM 测试专用用户，并授予必要的权限：

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

4. 创建示例数据：

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="macOS" value="macos">

在 macOS 上，你可以使用 [Homebrew](https://brew.sh) 在本地快速安装和启动 MySQL 8.0。

1. 更新 Homebrew 并安装 MySQL 8.0：

    ```shell
    brew update
    brew install mysql@8.0
    ```

2. 使 MySQL 命令可在系统路径中访问：

    ```shell
    brew link mysql@8.0 --force
    ```

3. 启动 MySQL 服务：

    ```shell
    brew services start mysql@8.0
    ```

4. 以 `root` 用户连接到 MySQL：

    ```shell
    mysql -uroot
    ```

5. 创建一个 DM 测试专用用户，并授予必要的权限：

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6. 创建示例数据：

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="CentOS" value="centos">

在 CentOS 等企业级 Linux 发行版上，你可以从 MySQL Yum 仓库安装 MySQL 8.0。

1. 下载并安装 MySQL Yum 仓库包。对于除 9 以外的 Linux 版本，必须在以下 URL 中将 `el9`（企业级 Linux 版本 9）替换为相应版本，同时保留 `mysql80` 以用于 MySQL 8.0 版本：

    ```shell
    sudo yum install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
    ```

2. 安装 MySQL：

    ```shell
    sudo yum install -y mysql-community-server --nogpgcheck
    ```

3. 启动 MySQL：

    ```shell
    sudo systemctl start mysqld
    ```

4. 在 MySQL 日志中找到临时 root 密码：

    ```shell
    sudo grep 'temporary password' /var/log/mysqld.log
    ```

5. 使用临时密码以 `root` 用户连接到 MySQL：

    ```shell
    mysql -uroot -p
    ```

6. 重置 `root` 密码：

    ```sql
    ALTER USER 'root'@'localhost'
        IDENTIFIED BY 'MyPassw0rd!';
    ```

7. 创建一个 DM 测试专用用户，并授予必要的权限：

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

8. 创建示例数据：

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="Ubuntu" value="ubuntu">

在 Ubuntu 上，你可以从官方 Ubuntu 仓库安装 MySQL。

1. 更新软件包列表：

    ```shell
    sudo apt-get update
    ```

2. 安装 MySQL：

    ```shell
    sudo apt-get install -y mysql-server
    ```

3. 检查 `mysql` 服务是否在运行，必要时启动服务：

    ```shell
    sudo systemctl status mysql
    sudo systemctl start mysql
    ```

4. 使用 socket 认证以 `root` 用户连接到 MySQL：

    ```shell
    sudo mysql
    ```

5. 创建一个 DM 测试专用用户，并授予必要的权限：

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6. 创建示例数据：

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

</SimpleTab>

## 第 3 步：配置 TiDB DM 源

After preparing the source MySQL database, configure TiDB DM to connect to it. To do this, create a source configuration file with the connection details and apply the configuration using the `dmctl` tool.

1. Create a source configuration file `mysql-01.yaml`:

    > **Note:**
    >
    > This step assumes you have already created the `tidb-dm` user with replication privileges in the source database, as described in [Step 2](#step-2-prepare-a-source-database-optional).

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "tidb-dm"
      password: "MyPassw0rd!"    # In production environments, it is recommended to use a password encrypted with dmctl.
      port: 3306
    ```

2. Create a DM data source:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 operate-source create mysql-01.yaml
    ```

## Step 4: Create a TiDB DM task

After configuring the source database, you can create a migration task in TiDB DM. This task references the source MySQL instance and defines the connection details for the target TiDB database.

1. Create a DM task configuration file `tiup-playground-task.yaml`:

    ```yaml
    # Task
    name: tiup-playground-task
    task-mode: "all"              # Execute all phases - full data migration and incremental sync.

    # Source (MySQL)
    mysql-instances:
      - source-id: "mysql-01"

    ## Target (TiDB)
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: ""                # If the password is not empty, it is recommended to use a password encrypted with dmctl.
    ```

2. Start the task using the configuration file:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 start-task tiup-playground-task.yaml
    ```

## Step 5: Verify the data replication

After starting the migration task, verify whether data replication is working as expected. Use the `dmctl` tool to check the task status, and connect to the target TiDB database to confirm that the data has been successfully replicated from the source MySQL database.

1. Check the status of the TiDB DM task:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 query-status
    ```

2. Connect to the TiDB target database:

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root --prompt 'tidb> '
    ```

3. Verify the replicated data. If you have created the sample data in [Step 2](#step-2-prepare-a-source-database-optional), you will see the `hello_tidb` table replicated from the MySQL source database to the TiDB target database:

    ```sql
    SELECT * FROM hello.hello_tidb;
    ```

    The output is as follows:

    ```sql
    +----+-------------+
    | id | name        |
    +----+-------------+
    |  1 | Hello World |
    +----+-------------+
    1 row in set (0.00 sec)
    ```

## Step 6: Clean up (optional)

After completing your testing, you can clean up the environment by stopping the TiUP Playground, removing the source MySQL instance (if created for testing), and deleting unnecessary files.

1. Stop the TiUP Playground:

    In the terminal where the TiUP Playground is running, press <kbd>Control</kbd>+<kbd>C</kbd> to terminate the process. This stops all TiDB and DM components and deletes the target environment.

2. Stop and remove the source MySQL instance:

    If you have created a source MySQL instance for testing in [Step 2](#step-2-prepare-a-source-database-optional), stop and remove it by taking the following steps:

    <SimpleTab groupId="os">

    <div label="Docker" value="docker">

    To stop and remove the Docker container:

    ```shell
    docker stop mysql80
    docker rm mysql80
    ```

    </div>

    <div label="macOS" value="macos">

    If you installed MySQL 8.0 using Homebrew solely for testing, stop the service and uninstall it:

    ```shell
    brew services stop mysql@8.0
    brew uninstall mysql@8.0
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/opt/homebrew/var/mysql`).

    </div>

    <div label="CentOS" value="centos">

    If you installed MySQL 8.0 from the MySQL Yum repository, stop the service and uninstall it:

    ```shell
    sudo systemctl stop mysqld
    sudo yum remove -y mysql-community-server
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/var/lib/mysql`).

    </div>

    <div label="Ubuntu" value="ubuntu">

    If you installed MySQL from the official Ubuntu repository, stop the service and uninstall it:

    ```shell
    sudo systemctl stop mysql
    sudo apt-get remove --purge -y mysql-server
    sudo apt-get autoremove -y
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/var/lib/mysql`).

    </div>

    </SimpleTab>

3. Remove the TiDB DM configuration files if they are no longer needed:

    ```shell
    rm mysql-01.yaml tiup-playground-task.yaml
    ```

4. If you no longer need TiUP, you can uninstall it:

    ```shell
    rm -rf ~/.tiup
    ```

## What's next

Now that you successfully created a task that migrates data from a source MySQL database to a target TiDB in a testing environment, you can:

- Explore [TiDB DM Features](/dm/dm-overview.md)
- Learn about [TiDB DM Architecture](/dm/dm-arch.md)
- Set up [TiDB DM for a Proof of Concept or Production](/dm/deploy-a-dm-cluster-using-tiup.md)
- Configure advanced [DM Tasks](/dm/dm-task-configuration-guide.md)
