---
title: TiDB Lightning 教程
aliases: ['/docs-cn/dev/get-started-with-tidb-lightning/','/docs-cn/dev/how-to/get-started/tidb-lightning/']
---

# TiDB Lightning 教程

TiDB Lightning 是一个将全量数据高速导入到 TiDB 集群的工具，目前支持 SQL 或 CSV 输出格式的数据源。你可以在以下两种场景下使用 TiDB Lightning：

- **迅速**导入**大量新**数据。
- 备份恢复所有数据。

![TiDB Lightning 整体架构](/media/tidb-lightning-architecture.png)

本教程假设使用的是若干新的、纯净版 CentOS 7 实例，你可以（使用 VMware、VirtualBox 及其他工具）在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。因为 TiDB Lightning 对计算机资源消耗较高，建议分配 16 GB 以上的内存以及 32 核以上的 CPU 以获取最佳性能。

> **警告：**
>
> 本教程中的部署方法只适用于测试及功能体验，并不适用于生产或开发环境。

## 准备全量备份数据

我们使用 [`dumpling`](/dumpling-overview.md) 从 MySQL 导出数据，如下：

{{< copyable "shell-regular" >}}

```sh
./bin/dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-f test.t[12]`：只导出 `test.t1` 和 `test.t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256MB`：将每张表切分成多个文件，每个文件大小约为 256 MB。

这样全量备份数据就导出到了 `/data/my_database` 目录中。

## 部署 TiDB Lightning

### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群。本教程以 TiDB v5.0.0 版本为例，具体部署方法可参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

### 第 2 步：下载 TiDB Lightning 安装包

通过以下链接获取 TiDB Lightning 安装包（TiDB Lightning 完全兼容较低版本的 TiDB 集群，建议选择最新稳定版本）：

- **v5.0.0**: [tidb-toolkit-v5.0.0-linux-amd64.tar.gz](https://download.pingcap.org/tidb-toolkit-v5.0.0-linux-amd64.tar.gz)

### 第 3 步：启动 `tidb-lightning`

1. 将安装包里的 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl` 上传至部署 TiDB Lightning 的服务器。

2. 将数据源也上传到同样的服务器。

3. 配置 `tidb-lightning.toml`。

    ```
    [lightning]
    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # 选择使用的 local 后端
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
    # 集群 pd 的地址
    pd-addr = "172.16.31.3:2379"
    ```

4. 配置合适的参数运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

### 第 4 步：检查数据

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志的最后一行会显示 `tidb lightning exit`。

如果出错，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

## 总结

本教程对 TiDB Lightning 进行了简单的介绍，并快速部署了一套简单的 TiDB Lightning 集群，将全量备份数据导入到 TiDB 集群中。

关于 TiDB Lightning 的详细功能和使用，参见 [TiDB Lightning 简介](/tidb-lightning/tidb-lightning-overview.md)。
