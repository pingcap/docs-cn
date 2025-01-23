---
title: TiDB Data Migration 快速上手指南
summary: 了解如何使用 TiUP Playground 快速部署试用 TiDB Data Migration 数据迁移工具。
---

# TiDB Data Migration 快速上手指南

[TiDB Data Migration (DM)](/dm/dm-overview.md) 是一个强大的数据迁移工具，用于将数据从兼容 MySQL 的数据库迁移到 TiDB。本指南介绍如何使用 [TiUP Playground](/tiup/tiup-playground.md) 在本地快速搭建用于开发或测试的 TiDB DM 环境，并完成一个将数据从源数据库 MySQL 迁移到目标数据库 TiDB 的简单任务。

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
    > 如果你已经安装了 TiUP，请确保其版本为 v1.16.1 或之后版本，以便使用 `--dm-master` 和 `--dm-worker` 参数。如果要检查当前版本，执行以下命令：
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

2. 启动包含目标数据库 TiDB 和 DM 组件的 TiUP Playground：

    ```shell
    tiup playground v8.5.1 --dm-master 1 --dm-worker 1 --tiflash 0 --without-monitor
    ```

3. 验证环境，查看输出中 TiDB 和 DM 是否已启动：

    ```text
    TiDB Playground Cluster is started, enjoy!

    Connect TiDB:    mysql --host 127.0.0.1 --port 4000 -u root
    Connect DM:      tiup dmctl --master-addr 127.0.0.1:8261
    TiDB Dashboard:  http://127.0.0.1:2379/dashboard
    ```

4. 保持 `tiup playground` 在当前终端中运行，并在新终端中执行后续步骤。

    这个 Playground 环境提供了目标 TiDB 数据库和数据复制引擎（DM-master 和 DM-worker）的运行进程。它将处理的数据流为：MySQL（源数据库）→ DM（数据复制引擎）→ TiDB（目标数据库）。

## 第 2 步：准备源数据库（可选）

你可以使用一个或多个 MySQL 实例作为源数据库。如果你已经有一个兼容 MySQL 的实例，请跳到[第 3 步](#第-3-步配置-tidb-dm-源)；如果没有，则按照以下步骤创建一个用于测试的 MySQL 实例。

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

3. 创建一个 DM 测试专用用户，并授予测试所需的权限：

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

2. 将 MySQL 命令添加到系统路径中：

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

1. 从 [MySQL Yum 仓库下载页面](https://dev.mysql.com/downloads/repo/yum)下载并安装 MySQL Yum 仓库包。对于非 Linux 9 版本，你需要将以下 URL 中的 `el9`（企业级 Linux 9 版本）替换为相应版本，同时保留 `mysql80` 以用于 MySQL 8.0 版本：

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

7. 创建一个 DM 测试专用用户，并授予测试所需的权限：

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

5. 创建一个 DM 测试专用用户，并授予测试所需的权限：

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

准备好源 MySQL 数据库后，配置 TiDB DM 连接到它。为此，创建一个包含连接详细信息的源配置文件，并使用 `dmctl` 工具应用该配置。

1. 创建源配置文件 `mysql-01.yaml`：

    > **注意：**
    >
    > 这里假设你已经在源数据库中创建了具有数据复制权限的 `tidb-dm` 用户，如[第 2 步](#第-2-步准备源数据库可选)所述。

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "tidb-dm"
      password: "MyPassw0rd!"    # In production environments, it is recommended to use a password encrypted with dmctl.
      port: 3306
    ```

2. 创建 DM 数据源：

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 operate-source create mysql-01.yaml
    ```

## 第 4 步：创建 TiDB DM 任务

配置好源数据库后，在 TiDB DM 中创建一个迁移任务，指定 MySQL 实例作为数据源，并定义目标数据库 TiDB 的详细连接信息。

1. 创建 DM 任务配置文件 `tiup-playground-task.yaml`：

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

2. 使用配置文件启动任务：

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 start-task tiup-playground-task.yaml
    ```

## 第 5 步：验证数据迁移

启动数据迁移任务后，验证数据复制是否符合预期。使用 `dmctl` 工具检查任务状态，并连接到目标数据库 TiDB，确认数据是否已成功从源数据库 MySQL 迁移到了目标数据库 TiDB。

1. 检查 TiDB DM 任务的状态：

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 query-status
    ```

2. 连接到目标数据库 TiDB：

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root --prompt 'tidb> '
    ```

3. 验证迁移的数据。如果在[第 2 步](#第-2-步准备源数据库可选)中创建了示例数据，你将看到从源数据库 MySQL 复制到目标数据库 TiDB 的 `hello_tidb` 表：

    ```sql
    SELECT * FROM hello.hello_tidb;
    ```

    输出如下：

    ```sql
    +----+-------------+
    | id | name        |
    +----+-------------+
    |  1 | Hello World |
    +----+-------------+
    1 row in set (0.00 sec)
    ```

## 第 6 步：清理环境（可选）

测试完成后，可以清理环境，包括停止 TiUP Playground、删除 MySQL 实例数据源（如果是专为测试创建的），以及删除不必要的文件。

1. 停止 TiUP Playground：

    在运行 TiUP Playground 的终端中，按 <kbd>Control</kbd>+<kbd>C</kbd> 终止进程。这将停止所有的 TiDB 和 DM 组件，并删除目标数据库环境。

2. 停止并删除数据源 MySQL 实例：

    如果你在[第 2 步](#第-2-步准备源数据库可选)中为测试创建了 MySQL 实例作为数据源，可按以下步骤停止并删除它：

    <SimpleTab groupId="os">

    <div label="Docker" value="docker">

    停止并删除 Docker 容器：

    ```shell
    docker stop mysql80
    docker rm mysql80
    ```

    </div>

    <div label="macOS" value="macos">

    如果你使用 Homebrew 安装的 MySQL 8.0 仅用于测试，则停止服务并卸载：

    ```shell
    brew services stop mysql@8.0
    brew uninstall mysql@8.0
    ```

    > **注意：**
    >
    > 如果你要删除所有 MySQL 数据文件，则删除 MySQL 数据目录（通常位于 `/opt/homebrew/var/mysql`）。

    </div>

    <div label="CentOS" value="centos">

    如果你从 MySQL Yum 仓库安装的 MySQL 8.0 仅用于测试，则停止服务并卸载：

    ```shell
    sudo systemctl stop mysqld
    sudo yum remove -y mysql-community-server
    ```

    > **注意：**
    >
    > 如果你要删除所有 MySQL 数据文件，则删除 MySQL 数据目录（通常位于 `/var/lib/mysql`）。

    </div>

    <div label="Ubuntu" value="ubuntu">

    如果你从官方 Ubuntu 仓库安装的 MySQL 仅用于测试，则停止服务并卸载：

    ```shell
    sudo systemctl stop mysql
    sudo apt-get remove --purge -y mysql-server
    sudo apt-get autoremove -y
    ```

    > **注意：**
    >
    > 如果你要删除所有 MySQL 数据文件，则删除 MySQL 数据目录（通常位于 `/var/lib/mysql`）。

    </div>

    </SimpleTab>

3. 如果不再需要 TiDB DM 配置文件，则删除：

    ```shell
    rm mysql-01.yaml tiup-playground-task.yaml
    ```

4. 如果不再需要 TiUP，则卸载：

    ```shell
    rm -rf ~/.tiup
    ```

## 探索更多

现在，你已经成功在测试环境中完成了一个从源数据库 MySQL 迁移数据到目标数据库 TiDB 的任务，接下来可以：

- 探索 [TiDB DM 的特性](/dm/dm-overview.md)
- 了解 [TiDB DM 的架构](/dm/dm-arch.md)
- [在生产环境中部署 TiDB DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)
- 了解 [TiDB DM 数据迁移任务的高级配置](/dm/dm-task-configuration-guide.md)
