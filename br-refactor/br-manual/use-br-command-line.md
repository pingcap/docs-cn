---
title: 介绍 br 工具命令行
summary: 介绍 br 工具命令行
---

# 使用 BR 命令行进行备份恢复

本文介绍如何 BR 命令行进行 TiDB 集群数据的备份和恢复。

在阅读本文前，请确保你已通读[备份与恢复工具 BR 简介](/br/backup-and-restore-overview.md)，尤其是[使用限制](/br/backup-and-restore-overview.md#使用限制)和[使用建议](/br/backup-and-restore-overview.md#使用建议)这两节。

## BR 命令行描述

一条 `br` 命令是由子命令、选项和参数组成的。子命令即不带 `-` 或者 `--` 的字符。选项即以 `-` 或者 `--` 开头的字符。参数即子命令或选项字符后紧跟的、并传递给命令和选项的字符。

以下是一条完整的 `br` 命令行：

`br backup full --pd "${PDIP}:2379" -s "s3://backup-101/snapshot-202209081330/"`

命令行各部分的解释如下：

* `backup`：`br` 的子命令
* `full`：`backup` 的子命令
* `-s` 或 `--storage`：备份保存的路径
* `"s3://backup-data/2022-01-30/"`：`-s` 的参数值，保存备份数据到 s3 的名为 backup-data 的 bucket 下面的 `2022-01-30/` 前缀目录下
* `--pd`：PD 服务地址
* `"${PDIP}:2379"`：`--pd` 的参数

### 命令和子命令

BR 由多层命令组成。目前，BR 包含 `backup` 和 `restore` 两个子命令：

* `br backup` 用于备份 TiDB 集群的数据
* `br log` 用于启动和管理日志备份任务
* `br restore` 用于恢复备份数据到 TiDB 集群

`br backup` 和 `br restore`  还包含这些子命令：

* `full`：可用于备份或恢复全部数据。
* `db`：可用于备份或恢复集群中的指定数据库。
* `table`：可用于备份或恢复集群指定数据库中的单张表。

### 常用选项

* `--pd`：用于连接的选项，表示 PD 服务地址，例如 `"${PDIP}:2379"`
* `-s, --storage`: 数据备份到的存储地址。快照备份支持以 S3/GCS/Azure Blob Storage 为备份存储。详细配置参考[备份存储](xxx) 
* `--ca`：指定 PEM 格式的受信任 CA 的证书文件路径。
* `--cert`：指定 PEM 格式的 SSL 证书文件路径。
* `--key`：指定 PEM 格式的 SSL 证书密钥文件路径。
* `--status-addr`：BR 向 Prometheus 提供统计数据的监听地址。

## 使用 BR 命令行备份集群

使用 `br backup` 命令来备份集群数据。可选择添加 `full` 或 `table` 子命令来指定备份的范围：全部集群数据或单张表的数据。

- [备份集群快照数据](/br-refactor/br-manual/br-snapshot-manual.md#备份-tidb-集群快照)
- [备份单个数据库的数据](/br-refactor/br-manual/br-snapshot-manual.md#备份单个数据库的数据)
- [备份单张表的数据](/br-refactor/br-manual/br-snapshot-manual.md#备份单张表的数据)
- [使用表库过滤功能备份多张表的数据](/br-refactor/br-manual/br-snapshot-manual.md#使用表库过滤功能备份多张表的数据)
- [加密快照备份数据](/br-refactor/br-manual/br-snapshot-manual.md#备份端加密备份数据)

## 使用 BR 命令行打开和管理日志备份

你可以使用 `br log` 命令来打开和管理备份日志，通过该命令的子命令，你可以完成如下操作：

- [启动日志备份](/br-refactor/br-manual/br-pitr-manual.md#启动日志备份)
- [查询备份状态](/br-refactor/br-manual/br-pitr-manual.md#查询日志备份任务)
- [暂停和重启备份](/br-refactor/br-manual/br-pitr-manual.md#暂停和重启日志备份任务)
- [停止备份任务并删除备份数据](/br-refactor/br-manual/br-pitr-manual.md#永久停止日志备份任务)
- [清理备份数据](/br-refactor/br-manual/br-pitr-manual.md#清理日志备份数据)
- [查看元信息](/br-refactor/br-manual/br-pitr-manual.md#查看备份数据元信息) 

## 使用 BR 命令行恢复集群数据

使用 `br restore` 命令来恢复备份数据。可选择添加 `full`、`db` 或 `table` 子命令来指定恢复操作的范围：全部集群数据、某个数据库或某张数据表。

- [Point in Time Recovery](/br-refactor/br-manual/br-pitr-manual.md#恢复到指定时间点-pitr)
- [恢复快照备份数据](/br-refactor/br-manual/br-snapshot-manual.md#恢复快照备份数据)
- [恢复单个数据库的快照备份数据](/br-refactor/br-manual/br-snapshot-manual.md#恢复单个数据库的数据)
- [恢复单张表的快照备份数据](/br-refactor/br-manual/br-snapshot-manual.md#恢复单张表的数据)
- [使用表库功能过滤恢复快照数据](/br-refactor/br-manual/br-snapshot-manual.md#使用表库功能过滤恢复数据)
- [恢复加密的快照备份数据](/br-refactor/br-manual/br-snapshot-manual.md#恢复加密的备份数据)
