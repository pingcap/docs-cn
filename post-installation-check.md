---
title: 验证集群运行状态
summary: 介绍如何验证集群运行状态。
aliases: ['/docs-cn/dev/post-installation-check/']
---

# 验证集群运行状态

在部署完一套 TiDB 集群后，需要检查集群是否正常运行。本文介绍如何通过 TiUP 命令、[TiDB Dashboard](/dashboard/dashboard-intro.md) 和 Grafana 检查集群状态，以及如何登录 TiDB 数据库执行简单的 SQL 操作。

## 通过 TiUP 检查集群状态

检查集群状态的命令是 `tiup cluster display <cluster-name>`，例如：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期结果输出：各节点 Status 状态信息为 `Up` 说明集群状态正常。

## 通过 TiDB Dashboard 和 Grafana 检查集群状态

本节介绍如何通过 [TiDB Dashboard](/dashboard/dashboard-intro.md) 和 Grafana 检查集群状态。

### 查看 TiDB Dashboard 检查 TiDB 集群状态

1. 通过 `{pd-ip}:{pd-port}/dashboard` 登录 TiDB Dashboard，登录用户和口令为 TiDB 数据库 `root` 用户和口令。如果你修改过数据库的 `root` 密码，则以修改后的密码为准，默认密码为空。

    ![TiDB-Dashboard](/media/tiup/tidb-dashboard.png)

2. 主页面显示 TiDB 集群中节点信息

    ![TiDB-Dashboard-status](/media/tiup/tidb-dashboard-status.png)

### 查看 Grafana 监控 Overview 页面检查 TiDB 集群状态

- 通过 `{Grafana-ip}:3000` 登录 Grafana 监控，默认用户名及密码为 `admin`/`admin`。

- 点击 **Overview** 监控页面检查 TiDB 端口和负载监控信息。

    ![Grafana-overview](/media/tiup/grafana-overview.png)

## 登录数据库执行简单 DML/DDL 操作和查询 SQL 语句

> **注意：**
>
> 登录数据库前，你需要安装 MySQL 客户端。

执行以下命令登录数据库：

{{< copyable "shell-regular" >}}

```shell
mysql -u root -h ${tidb_server_host_IP_address} -P 4000
```

其中 `${tidb_server_host_IP_address}` 是在[初始化集群拓扑文件](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)时为 `tidb_servers` 配置的 IP 地址，例如 `10.0.1.7`。

输出下列信息表示登录成功：

```sql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.25-TiDB-v5.0.0 TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible

Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

### 数据库操作

+ 检查 TiDB 版本

    {{< copyable "sql" >}}

    ```sql
    select tidb_version()\G
    ```

    预期结果输出：

    ```sql
    *************************** 1. row ***************************
    tidb_version(): Release Version: v5.0.0
    Edition: Community
    Git Commit Hash: 689a6b6439ae7835947fcaccf329a3fc303986cb
    Git Branch: HEAD
    UTC Build Time: 2020-05-28 11:09:45
    GoVersion: go1.13.4
    Race Enabled: false
    TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
    Check Table Before Drop: false
    1 row in set (0.00 sec)
    ```

+ 创建 PingCAP database

    {{< copyable "sql" >}}

    ```sql
    create database pingcap;
    ```

    ```sql
    Query OK, 0 rows affected (0.10 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    use pingcap;
    ```

    预期输出

    ```sql
    Database changed
    ```

+ 创建 `tab_tidb` 表

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE `tab_tidb` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL DEFAULT '',
    `age` int(11) NOT NULL DEFAULT 0,
    `version` varchar(20) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    KEY `idx_age` (`age`));
    ```

    预期输出

    ```sql
    Query OK, 0 rows affected (0.11 sec)
    ```

+ 插入数据

    {{< copyable "sql" >}}

    ```sql
    insert into `tab_tidb` values (1,'TiDB',5,'TiDB-v5.0.0');
    ```

    预期输出

    ```sql
    Query OK, 1 row affected (0.03 sec)
    ```

+ 查看 `tab_tidb` 结果

    {{< copyable "sql" >}}

    ```sql
    select * from tab_tidb;
    ```

    预期输出

    ```sql
    +----+------+-----+-------------+
    | id | name | age | version     |
    +----+------+-----+-------------+
    |  1 | TiDB |   5 | TiDB-v5.0.0 |
    +----+------+-----+-------------+
    1 row in set (0.00 sec)
    ```

+ 查看 TiKV store 状态、`store_id`、存储情况以及启动时间

    {{< copyable "sql" >}}

    ```sql
    select STORE_ID,ADDRESS,STORE_STATE,STORE_STATE_NAME,CAPACITY,AVAILABLE,UPTIME from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
    ```

    预期输出

    ```sql
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    | STORE_ID | ADDRESS            | STORE_STATE | STORE_STATE_NAME | CAPACITY | AVAILABLE | UPTIME             |
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    |        1 | 10.0.1.1:20160 |           0 | Up               | 49.98GiB | 46.3GiB   | 5h21m52.474864026s |
    |        4 | 10.0.1.2:20160 |           0 | Up               | 49.98GiB | 46.32GiB  | 5h21m52.522669177s |
    |        5 | 10.0.1.3:20160 |           0 | Up               | 49.98GiB | 45.44GiB  | 5h21m52.713660541s |
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    3 rows in set (0.00 sec)
    ```

+ 退出

    {{< copyable "sql" >}}

    ```sql
    exit
    ```

    预期输出

    ```sql
    Bye
    ```
