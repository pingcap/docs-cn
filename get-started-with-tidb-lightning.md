---
title: TiDB Lightning 快速上手
summary: TiDB Lightning 可快速将 MySQL 数据导入到 TiDB 集群中。首先使用 Dumpling 导出数据，然后部署 TiDB 集群。安装最新版本的 TiDB Lightning 并启动，最后检查数据导入情况。详细功能和使用请参考 TiDB Lightning 简介。
---

# TiDB Lightning 快速上手

本文档介绍如何快速上手 TiDB Lightning，将 MySQL 数据导入到 TiDB 集群中。

> **警告：**
>
> 本教程中的部署方法只适用于测试及功能体验，并不适用于生产或开发环境。

## 第 1 步：准备全量备份数据

你可以使用 [Dumpling](/dumpling-overview.md) 从 MySQL 导出数据。

1. 运行 `tiup --version` 检查是否已安装 TiUP。如果已经安装 TiUP，跳过这一步。如果没有安装 TiUP，运行以下命令：

    ```
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 使用 TiUP 安装 Dumpling：

    ```shell
    tiup install dumpling
    ```

3. 从 MySQL 导出数据，详细步骤可参考[使用 Dumpling 导出数据](/dumpling-overview.md#导出为-sql-文件)：

    ```sh
    tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
    ```

    其中：

    - `-t 16`：使用 16 个线程导出数据。
    - `-F 256MB`：将每张表切分成多个文件，每个文件大小约为 256 MB。
    - `-B test`：从 `test` 数据库导出。
    - `-f 'test.t[12]'`：只导出 `test.t1` 和 `test.t2` 这两个表。

    导出的全量备份数据将保存在 `/data/my_database` 目录中。

## 第 2 步：部署 TiDB 集群

在开始导入数据之前，你需要先部署一个要进行导入的 TiDB 集群。如果你已经有 TiDB 集群，可以跳过这一步。

关于部署 TiDB 集群的步骤，请参考 [TiDB 数据库快速上手指南](/quick-start-with-tidb.md)。

## 第 3 步：安装 TiDB Lightning

运行如下命令，安装 TiDB Lightning 的最新版本：

```shell
tiup install tidb-lightning
```

## 第 4 步：启动 TiDB Lightning

> **注意：**
>
> 本节的导入方法只适用于测试及功能体验，生产环境请参考[从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md#第-2-步导入全量数据到-tidb)。

1. 创建配置文件 `tidb-lightning.toml`，并根据你的集群信息填写如下配置：

    ```toml
    [lightning]
    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # 选择使用的导入模式
    backend = "local"
    # 设置排序的键值对的临时存放地址，目标路径需要是一个空目录
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # 源数据目录。
    data-source-dir = "/data/my_datasource/"

    # 配置通配符规则，默认规则会过滤 mysql、sys、INFORMATION_SCHEMA、PERFORMANCE_SCHEMA、METRICS_SCHEMA、INSPECTION_SCHEMA 系统数据库下的所有表
    # 若不配置该项，导入系统表时会出现“找不到 schema”的异常
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']
    [tidb]
    # 目标集群的信息
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    # 集群 pd 的地址。从 v7.6.0 开始支持设置多个地址。
    pd-addr = "172.16.31.3:2379,56.78.90.12:3456"
    ```

2. 运行 `tidb-lightning`。为避免直接在命令行使用 `nohup` 启动程序时因 `SIGHUP` 信号导致的程序退出，建议将 `nohup` 命令放入脚本中。示例如下：

    ```shell
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## 第 5 步：检查数据

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志的最后一行会显示 `tidb lightning exit`。

如果出错，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 总结

本教程对 TiDB Lightning 进行了简单的介绍，并快速部署了一套简单的 TiDB Lightning 集群，将全量备份数据导入到 TiDB 集群中。

关于 TiDB Lightning 的详细功能和使用，参见 [TiDB Lightning 简介](/tidb-lightning/tidb-lightning-overview.md)。
