---
title: 使用 TiDB Lightning 从 Amazon Aurora MySQL 迁移全量数据
summary: 使用 TiDB Lightning 从 Amazon Aurora MySQL 迁移全量数据。
aliases: ['/docs-cn/dev/migrate-from-aurora-using-lightning/','/docs-cn/dev/how-to/migrate/from-aurorausing-lightning/','/docs-cn/dev/how-to/migrate/from-aurora-using-lightning/']
---

# 使用 Lighting 从 MySQL SQL 文件迁移数据

本文介绍如何使用 TiDB Lightning 从 Amazon Aurora MySQL 迁移数据到 TiDB。

## 第一步：从 Aurora 导出全量数据至 S3

请参考 [AWS 官方文档：将数据库快照数据导出到 Amazon S3](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html) 将 Aurora 数据的快照导出到 S3。

## 第二步：部署 TiDB Lightning

使用 Lightning 将数据导入 TiDB，Lightning 具体的部署方法见 [TiDB Lightning 部署](/tidb-lightning/deploy-tidb-lightning.md)。

## 第三步：配置 TiDB Lightning 的数据源

1. 将 `[mydumper]` 下的 `data-source-dir` 设置为第一步导出的 S3 Bucket 路径。

    ```
    [mydumper]
    # 数据源目录
    data-source-dir = "s3://bucket-name/data-path"
    ```

2. 增加目标集群 TiDB 的配置。

    ```
    [tidb]
    # 目标集群的信息。tidb-server 的地址，填一个即可
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # 集群 pd 的地址
    pd-addr = "127.0.0.1:2379"
    ```

3. 设置运行后端模式

    ```
    [tikv-importer]
    # 使用 local backend
    backend = "local"
    # 本地临时文件存储路径，请确保对应的路径不存在或目录为空，并且所在的磁盘中有足够大的存储空间
    sorted-kv-dir = "/path/to/local-temp-dir"
    ```

4. 设置文件路由

    ```
    [mydumper]
    no-schema = true

    [mydumper.files]
    # 注意此处使用单引号字符串避免转义
    pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
    schema = '$1'
    table = '$2'
    type = '$3'
    ```

> **注意：**
> 
> - 本示例选择使用 Local Backend, 可以提供最优性能，你也可用根据实际需要使用 TiDB 或 Importer Backend. 三种 Backend 的具体差别参见 [TiDB Lightning Backend](/tidb-lightning/tidb-lightning-backends.md)。
> - 由于 Aurora Snapshot 导出的数据路径与 Lightning 支持的默认文件命名格式不同，因此需要额外设置文件路由配置。
> - 如果目标 TiDB 集群开启了 TLS，还需要设置 TLS 相关的设置

其它配置参考 [TiDB Lightning 配置](/tidb-lightning/tidb-lightning-configuration.md)。

## 第四步： 创建表结构

由于从 Aurora 导出至 S3 的快照数据没有包含创建库表的 SQL 语句文件，所以需要手动将对应库表的建表语句导出并导入至 TiDB。可以使用 dumpling + TiDB-Lightning 的方式创建所有表结构:

1. 使用 dumpling 导出表结构文件：

    ```
    ./dumpling --host 127.0.0.1 --port 4000 --user root --password password --no-data --output ./schema --filter "mydb.*"
    ```

    > **注意：**
    > 
    > - 请根据实际情况设置数据源地址的相关参数和输出文件的路径
    > - 如果需要导出所有库表，则不需要设置 "--filter" 相关参数, 如果只需要导出部分库表，可参考 [table-filter](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)

2. 使用 Lightning 创建表结构

    ```
    ./tidb-lightning -config tidb-lightning.toml -d ./schema -no-schema=false 
    ```

    此次启动 Lightning 只用于创建表结构，执行应该迅速完成(在常规速度下，每秒可以执行 10 条建表语句)。

> **注意：**
> 
> - 如果需要创建的库表较少，也可以直接手动在 TiDB 创建对应的库和表，或者使用 mysqldump 等其他工具导出 Schema 然后导入至 TiDB。

## 第五步：开启 TiDB Lightning 进行数据导入

运行 TiDB Lightning。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

```
# !/bin/bash
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

导入开始后，可以采用以下两种方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，具体参见 [TiDB-Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
