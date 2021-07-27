---
title: TiDB 集群监控 API
aliases: ['/docs-cn/dev/tidb-monitoring-api/']
---

# TiDB 集群监控 API

TiDB 提供了以下两种接口来监控集群状态：

- [状态接口](#运行状态)：通过 HTTP 接口对外汇报组件的信息。
- [存储信息](#存储信息)：通过 HTTP 接口对外汇报表的存储信息。
- [Metrics 接口](#使用-metrics-接口)：使用 Prometheus 记录组件中各种操作的详细信息，使用 Grafana 进行可视化展示。

## 使用状态接口

状态接口用于监控组件的一些基本信息，并且可以作为 keepalive 的监测接口。另外，通过 PD 的状态接口可以看到整个 TiKV 集群的详细信息。

### TiDB Server

- TiDB API 地址：`http://${host}:${port}`
- 默认端口：10080

#### 运行状态

以下示例中，通过访问 `http://${host}:${port}/status` 获取当前 TiDB Server 的状态，并判断该 TiDB Server 是否存活。结果以 **JSON** 格式返回：

{{< copyable "shell-regular" >}}

```bash
curl http://127.0.0.1:10080/status
```

```
{
    connections: 0,  # 当前 TiDB Server 上的客户端连接数
    version: "5.7.25-TiDB-v4.0.0-rc-141-g7267747ae",  # TiDB 版本号
    git_hash: "7267747ae0ec624dffc3fdedb00f1ed36e10284b"  # TiDB 当前代码的 Git Hash
}
```

#### 存储信息

以下示例中，通过访问 `http://${host}:${port}/status` 获取当前 TiDB Server 的状态，并判断该 TiDB Server 是否存活。结果以 JSON 格式返回：

以下示例中，通过访问 `http://${host}:${port}/schema_storage/${db}/${table}` 获取指定数据表的存储信息。结果以 JSON 格式返回：

{{< copyable "shell-regular" >}}

```bash
curl http://127.0.0.1:10080/schema_storage/mysql/stats_histograms
```

```
{
    "table_schema": "mysql", 
    "table_name": "stats_histograms", 
    "table_rows": 0, 
    "avg_row_length": 0, 
    "data_length": 0, 
    "max_data_length": 0, 
    "index_length": 0, 
    "data_free": 0
}
```

```bash
curl http://127.0.0.1:10080/schema_storage/test
```

```
[
    {
        "table_schema": "test", 
        "table_name": "test", 
        "table_rows": 0, 
        "avg_row_length": 0, 
        "data_length": 0, 
        "max_data_length": 0, 
        "index_length": 0, 
        "data_free": 0
    }
]
```

### PD Server

- PD API 地址：`http://${host}:${port}/pd/api/v1/${api_name}`
- 默认端口：2379
- 各类 `api_name` 详细信息：参见 [PD API Doc](https://download.pingcap.com/pd-api-doc.html)

通过该接口可以获取当前所有 TiKV 节点的状态以及负载均衡信息。下面以一个单节点的 TiKV 集群为例，说明用户需要了解的信息：

{{< copyable "shell-regular" >}}

```bash
curl http://127.0.0.1:2379/pd/api/v1/stores
```

```
{
  "count": 1,  # TiKV 节点数量
  "stores": [  # TiKV 节点的列表
    # 集群中单个 TiKV 节点的信息
    {
      "store": {
        "id": 1,
        "address": "127.0.0.1:20160",
        "version": "4.0.0-rc.2",
        "status_address": "172.16.5.90:20382",
        "git_hash": "2fdb2804bf8ffaab4b18c4996970e19906296497",
        "start_timestamp": 1590029618,
        "deploy_path": "/data2/tidb_test/v4.0.rc.2/tikv-20372/bin",
        "last_heartbeat": 1590030038949235439,
        "state_name": "Up"
      },
      "status": {
        "capacity": "3.581TiB",  # 存储总容量
        "available": "3.552TiB",  # 存储剩余容量
        "used_size": "31.77MiB",
        "leader_count": 174,
        "leader_weight": 1,
        "leader_score": 174,
        "leader_size": 174,
        "region_count": 531,
        "region_weight": 1,
        "region_score": 531,
        "region_size": 531,
        "start_ts": "2020-05-21T10:53:38+08:00",
        "last_heartbeat_ts": "2020-05-21T11:00:38.949235439+08:00",
        "uptime": "7m0.949235439s"
      }
    }
  ]
```

## 使用 metrics 接口

Metrics 接口用于监控整个集群的状态和性能。

- 如果使用其他方式部署 TiDB 集群，在使用 metrics 接口前，需先[部署 Prometheus 和 Grafana](/deploy-monitoring-services.md)。

成功部署 Prometheus 和 Grafana 之后，[配置 Grafana](/deploy-monitoring-services.md)。
