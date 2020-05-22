---
title: 从 MySQL SQL 文件迁移数据
summary: 使用 TiDB Lightning 从 MySQL 迁移数据。
category: how-to
---

# 从 MySQL SQL 文件迁移数据

本文介绍如何使用 TiDB Lightning 从 MySQL SQL 文件迁移数据到 TiDB。

## 第 1 步：部署 TiDB Lighitning

具体的部署方法见 [TiDB Lightning 部署](/tidb-lightning/deploy-tidb-lightning.md)

> **注意：**
>
> 如果选用 Importer Backend 进行数据导入的话，需要额外部署 TiKV Importer 组件。
> 如果选用 TiDB Backend 进行数据导入的话，只需要部署 TiDB Lightning 组件即可。
> 具体的差别见 [TiDB Lightning Backend](/tidb-lightning/tidb-lightning-tidb-backend.md)

## 第 2 步：配置 TiDB Lightning 的数据源，以 TiDB Backend 为例

增加 tidb-lightning.toml 配置文件，在文件中添加以下主要配置。

1. 设置 [mydumper] 下的 data-source-dir 为 MySQL SQL 文件路径。

```
[mydumper]
# 数据源目录
data-source-dir = "/data/export"
```
> **注意：**
>
> 如果下游已经存在对应的 schema，那么可以设置 `no-schema=true`，可以跳过 schema 创建的步骤


2. 增加导入集群 tidb 配置
```
[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
password = ""
```

其它配置可以参考 [TiDB Lightining 配置](/tidb-lightning/tidb-lightning-configuration.md)

## 第 3 步：开启 TiDB Lightning 进行数据导入

运行 tidb-lightning。如果直接在命令行中用 nohup 启动程序，可能会因为 SIGHUP 信号而退出，建议把 nohup 放到脚本里面，如：

```
#!/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

