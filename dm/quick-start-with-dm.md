---
title: TiDB Data Migration 快速上手试用
summary: 了解如何快速上手部署试用 TiDB Data Migration 工具。
aliases: ['/docs-cn/tidb-data-migration/dev/quick-start-with-dm/','/docs-cn/tidb-data-migration/dev/get-started/']
---

# TiDB Data Migration 快速上手指南

本文介绍如何快速体验使用数据迁移工具 [TiDB Data Migration](https://github.com/pingcap/dm) (DM) 从 MySQL 迁移数据到 TiDB。此文档用于快速体验 DM 产品功能特性，并不建议适合在生产环境中使用。

## 第 1 步：部署 DM 集群

1. 安装 TiUP 工具并通过 TiUP 快速部署 [dmctl](/dm/dmctl-introduction.md)。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    tiup install dm dmctl
    ```

2. 生成 DM 集群最小拓扑文件。

    {{< copyable "shell-regular" >}}

    ```
    tiup dm template
    ```

3. 复制输出的配置信息，修改 IP 地址后保存为 `topology.yaml` 文件，使用 TiUP 部署 DM 集群。

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dm deploy dm-test 6.0.0 topology.yaml -p
    ```

## 第 2 步：准备数据源

你可以使用一个或多个 MySQL 实例作为上游数据源。

1. 为每一个数据源编写如下配置文件：

    {{< copyable "shell-regular" >}}

    ```yaml
    source-id: "mysql-01"

    from:
      host: "127.0.0.1"
      user: "root"
      password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="  # 使用 tiup dmctl --encrypt "123456" 加密。
      port: 3306
    ```

2. 使用如下命令将数据源增加至 DM 集群。其中，`mysql-01.yaml` 是上一步编写的配置文件。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-01.yaml # --master-addr 填写 master_servers 其中之一。
    ```

若环境中并不存在可供测试的 MySQL 实例，可以使用以下方式通过 Docker 快速创建一个测试实例。步骤如下：

1. 编写 MySQL 配置文件：

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /tmp/mysqltest && cd /tmp/mysqltest

    cat > my.cnf <<EOF
    [mysqld]
    bind-address     = 0.0.0.0
    character-set-server=utf8
    collation-server=utf8_bin
    default-storage-engine=INNODB
    transaction-isolation=READ-COMMITTED
    server-id        = 100
    binlog_format    = row
    log_bin          = /var/lib/mysql/mysql-bin.log
    show_compatibility_56 = ON
    EOF
    ```

2. 使用 Docker 启动 MySQL 实例：

    {{< copyable "shell-regular" >}}

    ```shell
    docker run --name mysql-01 -v /tmp/mysqltest:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306  mysql:5.7
    ```

3. 待 MySQL 启动后，即可连接该实例。

    > **注意：**
    >
    > - 该命令仅适用于体验数据迁移过程，不能用于生产环境和压力测试。

    {{< copyable "shell-regular" >}}

    ```shell
    mysql -uroot -p -h 127.0.0.1 -P 3306
    ```

## 第 3 步：准备下游数据库

可以选择已存在的 TiDB 集群作为数据同步目标。

如果没有可以用于测试的 TiDB 集群，则使用以下命令快速构建演示环境。

{{< copyable "shell-regular" >}}

```shell
tiup playground
```

## 第 4 步：准备测试数据

在一个或多个数据源中创建测试表和数据。如果你使用已存在的 MySQL 数据库，且数据库中已有可用数据，可跳过这一步。

{{< copyable "sql" >}}

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

## 第 5 步：编写数据同步任务

1. 创建任务的配置文件 `testdm-task.yaml`：

    {{< copyable "" >}}

    ```yaml
    name: testdm
    task-mode: all

    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

    # 填写一个或多个所需同步的数据源信息
    mysql-instances:
      - source-id: "mysql-01"
        block-allow-list:  "ba-rule1"

    block-allow-list:
      ba-rule1:
        do-dbs: ["testdm"]
    ```

2. 使用 dmctl 创建任务：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

这样就成功创建了一个将 `mysql-01` 数据源迁移到 TiDB 的任务。

## 第 6 步：查看迁移任务状态

在创建迁移任务之后，可以用 `dmctl query-status` 来查看任务的状态。

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status testdm
```
