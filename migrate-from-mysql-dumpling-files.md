---
title: 使用 TiDB Lightning 从 MySQL SQL 文件迁移数据
summary: 使用 TiDB Lightning 从 MySQL 迁移数据。
---

# 使用 TiDB Lightning 从 MySQL SQL 文件迁移数据

本文介绍如何使用 TiDB Lightning 从 MySQL SQL 文件迁移数据到 TiDB。关于如何生成 MySQL SQL 文件，可以参考 [Dumpling](/dumpling-overview.md) 文档。

## 第 1 步：部署 TiDB Lightning

使用 TiDB Lightning 将数据导入 TiDB。TiDB Lightning 具体的部署方法见 [TiDB Lightning 部署](/tidb-lightning/deploy-tidb-lightning.md)。

> **注意：**
>
> - 如果选用 Local-backend 来导入数据，导入期间集群无法提供正常的服务，速度更快，适用于导入大量的数据（TB 以上级别）。
> - 如果选用 TiDB-backend 来导入数据，导入期间集群可以正常提供服务, 但相对导入速度较慢。
> - 二者的具体差别参见 [TiDB Lightning Backend](/tidb-lightning/tidb-lightning-backends.md)。

## 第 2 步：配置 TiDB Lightning 的数据源

本文以选用 TiDB-backend 导入数据为例。增加 `tidb-lightning.toml 配置文件`，在文件中添加以下主要配置：

1. 将 `[mydumper]` 下的 `data-source-dir` 设置为 MySQL 的 SQL 文件路径。

    ```
    [mydumper]
    # 数据源目录
    data-source-dir = "/data/export"
    ```

    > **注意：**
    >
    > 如果下游已经存在对应的 schema，那么可以设置 `no-schema=true` 来跳过 schema 创建的步骤。

2. 增加目标集群 TiDB 的配置。

    ```
    [tidb]
    # 目标集群的信息。tidb-server 的地址，填一个即可
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    ```

3. 增加 TiDB-backend 的必要参数。本文采用 TiDB-backend 模式。此处也可以根据实际应用场景设置为 "local" 或 "importer"。具体请参考[后端模式](/tidb-lightning/tidb-lightning-backends.md)。

    ```
    [tikv-importer]
    backend = "tidb"
    ```

4. 增加导入 TiDB 集群必要参数

    ```
    [tidb]
    host = "{{tidb-host}}"
    port = {{tidb-port}}
    user = "{{tidb-user}}"
    password = "{{tidb-password}}"
    ```

其它配置参考 [TiDB Lightning 配置](/tidb-lightning/tidb-lightning-configuration.md)。

## 第 3 步：开启 TiDB Lightning 进行数据导入

运行 TiDB Lightning。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

```
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入开始后，可以采用以下两种方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，具体参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
