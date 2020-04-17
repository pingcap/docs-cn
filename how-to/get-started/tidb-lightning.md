---
title: TiDB Lightning 教程
category: how-to
---

# TiDB Lightning 教程

TiDB Lightning 是一个将全量数据高速导入到 TiDB 集群的工具，目前支持 Mydumper 或 CSV 输出格式的数据源。你可以在以下两种场景下使用 Lightning：

- **迅速**导入**大量新**数据。
- 备份恢复所有数据。

TiDB Lightning 主要包含两个部分:

- **`tidb-lightning`**（“前端”）：主要完成适配工作，通过读取数据源，在下游 TiDB 集群建表、将数据转换成键/值对 (KV 对) 发送到 `tikv-importer`、检查数据完整性等。
- **`tikv-importer`**（“后端”）：主要完成将数据导入 TiKV 集群的工作，把 `tidb-lightning` 写入的 KV 对缓存、排序、切分并导入到 TiKV 集群。

![TiDB Lightning 整体架构](/media/tidb-lightning-architecture.png)

本教程假设使用的是若干新的、纯净版 CentOS 7 实例，你可以（使用 VMware、VirtualBox 及其他工具）在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。因为 TiDB Lightning 对计算机资源消耗较高，建议分配 4 GB 以上的内存。

> **警告：**
>
> 本教程中的部署方法只适用于测试及功能体验，并不适用于生产或开发环境。

## 准备全量备份数据

我们使用 [`mydumper`](/reference/tools/mydumper.md) 从 MySQL 导出数据，如下：

{{< copyable "shell-regular" >}}

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-T t1,t2`：只导出 `t1` 和 `t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256`：将每张表切分成多个文件，每个文件大小约为 256 MB。
- `--skip-tz-utc`：添加这个参数则会忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

这样全量备份数据就导出到了 `/data/my_database` 目录中。

## 部署 TiDB Lightning

### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群（版本要求 2.0.9 以上），本教程使用 TiDB 3.0.4 版本。部署方法可参考 [TiDB 快速入门指南](/overview.md#部署方式)。

### 第 2 步：下载 TiDB Lightning 安装包

通过以下链接获取 TiDB Lightning 安装包（选择与 TiDB 集群相同的版本）：

- **v3.0.4**: [tidb-toolkit-v3.0.4-linux-amd64.tar.gz](https://download.pingcap.org/tidb-toolkit-v3.0.0-linux-amd64.tar.gz)

### 第 3 步：启动 `tikv-importer`

1. 将安装包里的 `bin/tikv-importer` 上传至部署 TiDB Lightning 的服务器。

2. 配置 `tikv-importer.toml`。

    ```toml
    # TiKV Importer 配置文件模版

    # 日志文件。
    log-file = "tikv-importer.log"
    # 日志等级：trace、debug、info、warn、error、off。
    log-level = "info"

    [server]
    # tikv-importer 监听的地址，tidb-lightning 需要连到这个地址进行数据写入。
    addr = "192.168.20.10:8287"

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/mnt/ssd/data.import/"
    ```

3. 运行 `tikv-importer`。

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

### 第 4 步：启动 `tidb-lightning`

1. 将安装包里的 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl` 上传至部署 TiDB Lightning 的服务器。

2. 将数据源也上传到同样的服务器。

3. 配置合适的参数运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning \
                --importer 172.16.31.10:8287 \
                -d /data/my_database/ \
                --tidb-server 172.16.31.2 \
                --tidb-user root \
                --log-file tidb-lightning.log \
            > nohup.out &
    ```

### 第 5 步：检查数据

导入完毕后，TiDB Lightning 会自动退出。若导入成功，日志的最后一行会显示 `tidb lightning exit`。

如果出错，请参见 [TiDB Lightning 错误排解](/how-to/troubleshoot/tidb-lightning.md)。

## 总结

本教程对 TiDB Lightning 进行了简单的介绍，并快速部署了一套简单的 TiDB Lightning 集群，将全量备份数据导入到 TiDB 集群中。

关于 TiDB Lightning 的详细功能和使用，参见 [TiDB Lightning 简介](/reference/tools/tidb-lightning/overview.md)。
