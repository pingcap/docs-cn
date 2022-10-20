---
title: br 命令行手册
summary: 介绍 br 命令行工具
---

# br 命令行手册

本文详细介绍了 br 各个命令行功能的使用。

## br 命令行描述

`br` 命令是由子命令、选项和参数组成的。子命令即不带 `-` 或者 `--` 的字符。选项即以 `-` 或者 `--` 开头的字符。参数即子命令或选项字符后紧跟的、并传递给命令和选项的字符。

以下是一条完整的 `br` 命令行：

`br backup full --pd "${PD_IP}:2379" -s "s3://backup-data/snapshot-202209081330/"`

命令行各部分的解释如下：

* `backup`：`br` 的子命令
* `full`：`backup` 的子命令
* `-s` 或 `--storage`：备份数据的存储地址选项。`"s3://backup-data/snapshot-202209081330/"` 是 `-s` 的参数值
* `--pd`：PD 访问地址选项。`"${PD_IP}:2379"`是`--pd` 的参数值。

### 命令和子命令

br 由多层命令组成。目前，br 包含的重要命令有：

* `br backup` 用于备份 TiDB 集群的全量数据
* `br log` 用于启动和管理日志备份任务
* `br restore` 用于恢复备份数据到 TiDB 集群

`br backup` 和 `br restore`  还包含这些子命令：

* `full`：可用于备份或恢复整个备份数据。
* `db`：可用于备份或恢复集群中的指定数据库。
* `table`：可用于备份或恢复集群指定数据库中的单张表。

### 常用选项

* `--pd`：PD 访问地址选项，例如 `"${PD_IP}:2379"`
* `-s, --storage`: 备份数据的存储地址选项。BR 支持以 S3/GCS/Azure Blob Storage/NFS 为备份存储。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。 
* `--ca`：指定 PEM 格式的受信任 CA 的证书文件路径。
* `--cert`：指定 PEM 格式的 SSL 证书文件路径。
* `--key`：指定 PEM 格式的 SSL 证书密钥文件路径。
* `--status-addr`：向 Prometheus 提供统计数据的监听地址。

## 全量备份功能命令行介绍

使用 `br backup` 命令来备份集群全量数据。可选择添加 `full` 或 `table` 子命令来指定备份的范围：全部集群数据或单张表的数据。

- [备份集群快照数据](/br/br-snapshot-manual.md#备份-tidb-集群快照)
- [备份单个数据库的数据](/br/br-snapshot-manual.md#备份单个数据库的数据)
- [备份单张表的数据](/br/br-snapshot-manual.md#备份单张表的数据)
- [使用表库过滤功能备份多张表的数据](/br/br-snapshot-manual.md#使用表库过滤功能备份多张表的数据)
- [加密快照备份数据](/br/br-snapshot-manual.md#备份端加密备份数据)

## 日志备份命令行介绍

使用 `br log` 命令来打开和管理备份日志。

- [启动日志备份](/br/br-pitr-manual.md#启动日志备份)
- [查询备份状态](/br/br-pitr-manual.md#查询日志备份任务)
- [暂停和重启备份](/br/br-pitr-manual.md#暂停和重启日志备份任务)
- [停止备份任务并删除备份数据](/br/br-pitr-manual.md#永久停止日志备份任务)
- [清理备份数据](/br/br-pitr-manual.md#清理日志备份数据)
- [查看元信息](/br/br-pitr-manual.md#查看备份数据元信息) 

## 恢复备份数据命令行介绍

使用 `br restore` 命令来恢复备份数据。可选择添加 `full`、`db` 或 `table` 子命令来指定恢复操作的范围：全部集群数据、某个数据库或某张数据表。

- [Point in Time Recovery](/br/br-pitr-manual.md#恢复到指定时间点-pitr)
- [恢复快照备份数据](/br/br-snapshot-manual.md#恢复快照备份数据)
- [恢复单个数据库的快照备份数据](/br/br-snapshot-manual.md#恢复单个数据库的数据)
- [恢复单张表的快照备份数据](/br/br-snapshot-manual.md#恢复单张表的数据)
- [使用表库功能过滤恢复快照数据](/br/br-snapshot-manual.md#使用表库功能过滤恢复数据)
- [恢复加密的快照备份数据](/br/br-snapshot-manual.md#恢复加密的备份数据)
