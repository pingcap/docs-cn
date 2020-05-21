---
title: 使用 TiUP 部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/dev/how-to/deploy/orchestrated/tiup/']
---

# 使用 TiUP 部署 TiDB 集群

[TiUP](https://github.com/pingcap-incubator/tiup) 是 TiDB 4.0 版本引入的集群运维工具，[TiUP cluster](https://github.com/pingcap-incubator/tiup-cluster) 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群；管理 TiDB 集群参数；部署 TiDB Binlog；部署 TiFlash 等。

本文介绍了使用 TiUP 部署 TiDB 集群的流程，具体步骤如下：

- [第 1 步：软硬件环境配置](/hardware-and-software-requirements.md)
- [第 2 步：在中控机上安装 TiUP 组件](/tiup/tiup-cluster.md)
- [第 3 步：在 TiKV 部署目标机器上添加数据盘 EXT4 文件系统挂载参数](/check-before-deployment.md)
- [第 4 步：配置初始化参数文件 `topology.yaml`](/topology.yaml)
- [第 5 步：执行部署命令](#第-5-步执行部署命令)
- [第 6 步：检查 TiUP 管理的集群情况](#第-6-步检查-tiup-管理的集群情况)
- [第 7 步：检查部署的 TiDB 集群情况](#第-7-步检查部署的-tidb-集群情况)
- [第 8 步：执行集群启动命令](#第-8-步执行集群启动命令)
- [第 9 步：通过 TiUP 检查集群状态](#第-9-步通过-tiup-检查集群状态)
- [第 10 步：通过 TiDB Dashboard 和 Grafana 检查集群状态](#第-10-步通过-tidb-dashboard-和-grafana-检查集群状态)
- [第 11 步：登录数据库执行简单 DML、DDL 操作和查询 SQL 语句](#第-11-步登录数据库执行简单-dmlddl-操作和查询-sql-语句)

另外，本文还提供了使用 TiUP 关闭、销毁集群的命令，以及使用 TiUP 部署的常见问题和解决方案。具体参见：

- [关闭集群](#关闭集群)
- [销毁集群](#销毁集群)
- [常见部署问题](#常见部署问题)

## 执行部署命令

> **注意：**
>
> 通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：
>
> - 如果是密钥方式，可以通过 `-i` 或者 `--identity_file` 来指定密钥的路径；
> - 如果是密码方式，无需添加其他参数，`Enter` 即可进入密码交互窗口。

### 第 5 步：执行部署命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v4.0.0-rc.2 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

以上部署命令中：

- 通过 TiUP cluster 部署的集群名称为 `tidb-test`
- 部署版本为 `v4.0.0-rc.2`，其他版本可以参考[如何查看 TiUP 支持管理的 TiDB 版本](#如何查看-tiup-支持管理的-tidb-版本)的介绍
- 初始化配置文件为 `topology.yaml`
- --user root：通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- [-i] 及 [-p]：非必选项，如果已经配置免密登陆目标机，则不需填写。否则选择其一即可，[-i] 为可登录到部署机 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码

预期日志结尾输出会有 ```Deployed cluster `tidb-test` successfully``` 关键词，表示部署成功。

## 验证集群部署状态

### 验证命令介绍

{{< copyable "shell-regular" >}}

```shell
tiup cluster list --help
```

### 第 6 步：检查 TiUP 管理的集群情况

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

预期输出当前通过 TiUP cluster 管理的集群名称、部署用户、版本、密钥信息等：

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v4.0.0-rc      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

### 第 7 步：检查部署的 TiDB 集群情况

例如，执行如下命令检查 `tidb-test` 集群情况：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期输出包括 `tidb-test` 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 Down/inactive）、目录信息：

## 启动集群

### 第 8 步：执行集群启动命令

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

预期结果输出 ```Started cluster `tidb-test` successfully``` 标志启动成功。

## 验证集群运行状态

### 第 9 步：通过 TiUP 检查集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期结果输出，注意 Status 状态信息为 `Up` 说明集群状态正常：

### 第 10 步：通过 TiDB Dashboard 和 Grafana 检查集群状态

#### 查看 TiDB Dashboard 检查 TiDB 集群状态

- 通过 `{pd-ip}:2379/dashboard` 登录 TiDB Dashboard，登录用户和口令为 TiDB 数据库 root 用户和口令，如果你修改过数据库的 root 密码，则以修改后的密码为准，默认密码为空。

    ![TiDB-Dashboard](/media/tiup/tidb-dashboard.png)

- 主页面显示 TiDB 集群中节点信息

    ![TiDB-Dashboard-status](/media/tiup/tidb-dashboard-status.png)

#### 查看 Grafana 监控 Overview 页面检查 TiDB 集群状态

- 通过 `{Grafana-ip}:3000` 登录 Grafana 监控，默认用户名及密码为 admin/admin

    ![Grafana-login](/media/tiup/grafana-login.png)

- 点击 Overview 监控页面检查 TiDB 端口和负载监控信息

    ![Grafana-overview](/media/tiup/grafana-overview.png)

### 第 11 步：登录数据库执行简单 DML、DDL 操作和查询 SQL 语句

> **注意：**
>
> 登录数据库前，你需要安装 MySQL 客户端。

执行如下命令登录数据库：

{{< copyable "shell-regular" >}}

```shell
mysql -u root -h 10.0.1.4 -P 4000
```

数据库操作：

```sql
--
-- 登录成功
--
-- Welcome to the MariaDB monitor.  Commands end with ; or \g.
-- Your MySQL connection id is 1
-- Server version: 5.7.25-TiDB-v4.0.0-beta-446-g5268094af TiDB Server (Apache License 2.0), MySQL 5.7 compatible
-- 
-- Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
-- 
-- Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

--
-- 检查 TiDB 版本
--
select tidb_version()\G
-- 预期结果输出
-- *************************** 1. row ***************************
-- tidb_version(): Release Version: v4.0.0-beta-446-g5268094af
-- Git Commit Hash: 5268094afe05c7efef0d91d2deeec428cc85abe6
-- Git Branch: master
-- UTC Build Time: 2020-03-17 02:22:07
-- GoVersion: go1.13
-- Race Enabled: false
-- TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
-- Check Table Before Drop: false
-- 1 row in set (0.00 sec)
-- MySQL [tidb]> create database pingcap;
-- Query OK, 0 rows affected (0.10 sec)

--
-- 创建 PingCAP database
--
create database pingcap;
-- Query OK, 0 rows affected (0.10 sec)

use pingcap;
-- 预期输出
-- Database changed
--
-- 创建 tab_tidb 表
--
CREATE TABLE `tab_tidb` (
`id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(20) NOT NULL DEFAULT '',
 `age` int(11) NOT NULL DEFAULT 0,
 `version` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `idx_age` (`age`));
-- 预期输出
-- Query OK, 0 rows affected (0.11 sec)
--
-- 插入数据
--
insert into `tab_tidb` values (1,'TiDB',5,'TiDB-v4.0.0');
-- 预期输出
-- Query OK, 1 row affected (0.03 sec)
--
-- 查看 tab_tidb 结果
--
select * from tab_tidb;
-- 预期输出
-- +----+------+-----+-------------+
-- | id | name | age | version     |
-- +----+------+-----+-------------+
-- |  1 | TiDB |   5 | TiDB-v4.0.0 |
-- +----+------+-----+-------------+
-- 1 row in set (0.00 sec)
--
-- 查看 TiKV store 状态、store_id、存储情况以及启动时间
--
select STORE_ID,ADDRESS,STORE_STATE,STORE_STATE_NAME,CAPACITY,AVAILABLE,UPTIME from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
-- 预期输出
-- +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
-- | STORE_ID | ADDRESS            | STORE_STATE | STORE_STATE_NAME | CAPACITY | AVAILABLE | UPTIME             |
-- +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
-- |        1 | 10.0.1.1:20160 |           0 | Up               | 49.98GiB | 46.3GiB   | 5h21m52.474864026s |
-- |        4 | 10.0.1.2:20160 |           0 | Up               | 49.98GiB | 46.32GiB  | 5h21m52.522669177s |
-- |        5 | 10.0.1.3:20160 |           0 | Up               | 49.98GiB | 45.44GiB  | 5h21m52.713660541s |
-- +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
-- 3 rows in set (0.00 sec)

exit
-- 预期输出
-- Bye
```