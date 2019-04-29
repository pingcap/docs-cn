---
title: TiDB-Binlog Cluster 版本升级方法
category: tools
---

# TiDB-Binlog Cluster 版本升级方法

新版本的 TiDB（v2.0.8-binlog、v2.1.0-rc.5 及以上版本）不兼容 [Kafka 版本](/tools/binlog/tidb-binlog-kafka.md)以及 [Local 版本](/tools/binlog/tidb-binlog-local.md)的 TiDB-Binlog，集群升级到新版本后只能使用 Cluster 版本的 TiDB-Binlog。如果在升级前已经使用了 Kafka／Local 版本的 TiDB-Binlog，必须将其升级到 Cluster 版本。
 
 TiDB-Binlog 版本与 TiDB 版本的对应关系如下：
 
| TiDB-Binlog 版本 | TiDB 版本 | 说明 |
|---|---|---|
| Local | TiDB 1.0 及更低版本 ||
| Kafka | TiDB 1.0 ~ TiDB 2.1 RC5 | TiDB 1.0 支持 local 版本和 Kafka 版本的 TiDB-Binlog。 |
| Cluster | TiDB v2.0.8-binlog，TiDB 2.1 RC5 及更高版本 | TiDB v2.0.8-binlog 是一个支持 Cluster 版本 TiDB-Binlog 的 2.0 特殊版本。 |

## 升级流程

* 如果能接受重新导全量数据，则可以直接废弃老版本，按[本文档](deploy.md)部署。

* 如果想从原来的 checkpoint 继续同步，则使用以下升级流程：
    1. 部署新版本 Pump。
    2. 暂停 TiDB 集群业务。
    3. 更新 TiDB 以及配置，写 Binlog 到新的 Pump Cluster。
    4. TiDB 集群重新接入业务。
    5. 确认老版本的 Drainer 已经将老版本的 Pump 的数据完全同步到下游。

        查询 Drainer 的 `status` 接口，示例命令如下：

        ```bash
        $ curl 'http://172.16.10.49:8249/status'
        {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}
        ```

        如果返回的 `Synced` 为 true，则可以认为 Binlog 数据已经全部同步到了下游。
    6. 启动新版本 Drainer；
    7. 下线老版本的 Pump、Drainer 以及依赖的 Kafka 和 ZookeSeper。


