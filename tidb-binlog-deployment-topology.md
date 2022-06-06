---
title: TiDB Binlog 部署拓扑
summary: 介绍如何在部署最小拓扑集群的基础上，同时部署 TiDB Binlog。
---

# TiDB Binlog 部署拓扑

本文介绍在部署最小拓扑集群的基础上，同时部署 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。TiDB Binlog 是目前广泛使用的增量同步组件，可提供准实时备份和同步功能。

## 拓扑信息

| 实例 |个数| 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
|TiDB | 3 | 16 VCore 32 GB | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口配置；<br/>开启 enable_binlog； <br/> 开启 ignore-error |
| PD | 3 | 4 VCore 8 GB | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口配置 |
| TiKV | 3 | 16 VCore 32 GB | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口配置 |
| Pump| 3 |8 VCore 16GB |10.0.1.1 <br/> 10.0.1.7 <br/> 10.0.1.8 | 默认端口配置； <br/> 设置 GC 时间 7 天 |
| Drainer | 1 | 8 VCore 16GB | 10.0.1.12 | 默认端口配置；<br/> 设置默认初始化 commitTS -1 为最近的时间戳 <br/> 配置下游目标 TiDB 10.0.1.12:4000 |

### 拓扑模版

[简单 TiDB Binlog 配置模板（下游为 MySQL）](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tidb-binlog.yaml)

[简单 TiDB Binlog 配置模板（下游为 file）](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-file-binlog.yaml)

[详细 TiDB Binlog 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tidb-binlog.yaml)

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

### 关键参数介绍

拓扑配置模版的关键参数如下：

- `server_configs.tidb.binlog.enable: true`

    开启 TiDB Binlog 服务，默认为 false。

- `server_configs.tidb.binlog.ignore-error: true`

    高可用场景建议开启，如果设置为 true，发生错误时，TiDB 会停止写入 TiDB Binlog，并且在监控项 `tidb_server_critical_error_total` 上计数加 1；如果设置为 false，一旦写入 TiDB Binlog 失败，会停止整个 TiDB 的服务。

- `drainer_servers.config.syncer.db-type`

    TiDB Binlog 的下游类型，目前支持 `mysql`、`tidb`、`kafka` 和 `file`。

- `drainer_servers.config.syncer.to`

    TiDB Binlog 的下游配置。根据 `db-type` 的不同，该选项可配置下游数据库的连接参数、Kafka 的连接参数、文件保存路径。详细说明可参见 [TiDB Binlog 配置说明](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)。

> **注意：**
>
> - 编辑配置文件模版时，如无需自定义端口或者目录，仅修改 IP 即可。
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户家目录下。
