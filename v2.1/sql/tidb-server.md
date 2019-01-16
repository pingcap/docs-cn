---
title: TiDB 数据库管理
category: user guide
---

# TiDB 数据库管理

## TiDB 服务

TiDB 是指 TiDB 数据库系统，本篇文档涉及到 TiDB 集群的基本管理功能。

## TiDB 集群启动配置

可以通过命令行参数或者配置文件设置服务参数，或者是两者一起使用。注意命令行参数的优先级高于配置文件，如果同一个参数两种方式都设置，会以命令行参数中的值为准。具体信息参考[这篇](../sql/server-command-option.md)文档。

## TiDB 数据库系统变量

TiDB 兼容 MySQL 的系统变量，同时定义了一些特有的系统变量用于调整数据库行为，具体信息参考 [TiDB 专用系统变量和语法](../sql/tidb-specific.md) 文档。

## TiDB 系统表

和 MySQL 类似，TiDB 中也有系统表，用于存放数据库运行时所需信息。具体信息参考 [TiDB 系统数据库](../sql/system-database.md)文档。

## TiDB 数据目录

TiDB 数据存放在存储引擎中，数据目录取决于使用的存储引擎，存储引擎的选择参见 [TiDB 启动参数文档](../op-guide/configuration.md#store)。

- 对于使用本地存储引擎的情况，数据存储在本机硬盘上，目录位置通过 [path](../op-guide/configuration.md#path) 参数控制。

- 对于使用 TiKV 引擎的情况，数据存储在 TiKV 节点上，目录位置通过 [data-dir](../op-guide/configuration.md#data-dir-1) 参数控制。

## TiDB 服务器日志文件

TiDB 集群的三个组件（`tidb-server`、`tikv-server`、`pd-server`）默认会将日志输出到标准错误中，并且三个组件都支持设置 `--log-file` [启动参数](../op-guide/configuration.md)（或者是配置文件中的配置项）将日志输出到文件中。

通过配置文件可以调整日志的行为，具体信息请参见各个组件的配置文件说明。例如： [`tidb-server` 日志配置项](https://github.com/pingcap/tidb/blob/master/config/config.toml.example#L46)。
