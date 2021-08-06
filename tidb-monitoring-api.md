---
title: TiDB Monitoring API
summary: Learn the API of TiDB monitoring services.
aliases: ['/docs/dev/tidb-monitoring-api/']
---

# TiDB Monitoring API

You can use the following two types of interfaces to monitor the TiDB cluster state:

- [The state interface](#running-status): this interface uses the HTTP interface to get the component information.
- [Storage information](#storage-information): this interface uses the HTTP interface to get the storage information of data tables.
- [The metrics interface](#use-the-metrics-interface): this interface uses Prometheus to record the detailed information of the various operations in components and views these metrics using Grafana.

## Use the state interface

The state interface monitors the basic information of a specific component in the TiDB cluster. It can also act as the monitor interface for Keepalive messages. In addition, the state interface for the Placement Driver (PD) can get the details of the entire TiKV cluster.

### TiDB server

- TiDB API address: `http://${host}:${port}`
- Default port: `10080`

### Running status

The following example uses `http://${host}:${port}/status` to get the current state of the TiDB server and to determine whether the server is alive. The result is returned in **JSON** format.

```bash
curl http://127.0.0.1:10080/status
{
    connections: 0,  # The current number of clients connected to the TiDB server.
    version: "5.7.25-TiDB-v3.0.0-beta-250-g778c3f4a5",  # The TiDB version number.
    git_hash: "778c3f4a5a716880bcd1d71b257c8165685f0d70"  # The Git Hash of the current TiDB code.
}
```

#### Storage information

The following example uses `http://${host}:${port}/schema_storage/${db}/${table}` to get the storage information of the specific data table. The result is returned in **JSON** format.

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

### PD server

- PD API address: `http://${host}:${port}/pd/api/v1/${api_name}`
- Default port: `2379`
- Details about API names: see [PD API doc](https://download.pingcap.com/pd-api-v1.html)

The PD interface provides the state of all the TiKV servers and the information about load balancing. See the following example for the information about a single-node TiKV cluster:

```bash
curl http://127.0.0.1:2379/pd/api/v1/stores
{
  "count": 1,  # The number of TiKV nodes.
  "stores": [  # The list of TiKV nodes.
    # The details about the single TiKV node.
    {
      "store": {
        "id": 1,
        "address": "127.0.0.1:20160",
        "version": "3.0.0-beta",
        "state_name": "Up"
      },
      "status": {
        "capacity": "20 GiB",  # The total capacity.
        "available": "16 GiB",  # The available capacity.
        "leader_count": 17,
        "leader_weight": 1,
        "leader_score": 17,
        "leader_size": 17,
        "region_count": 17,
        "region_weight": 1,
        "region_score": 17,
        "region_size": 17,
        "start_ts": "2019-03-21T14:09:32+08:00",  # The starting timestamp.
        "last_heartbeat_ts": "2019-03-21T14:14:22.961171958+08:00",  # The timestamp of the last heartbeat.
        "uptime": "4m50.961171958s"
      }
    }
  ]
```

## Use the metrics interface

The metrics interface monitors the state and performance of the entire TiDB cluster.

- If you use other deployment ways, [deploy Prometheus and Grafana](/deploy-monitoring-services.md) before using this interface.

After Prometheus and Grafana are successfully deployed, [configure Grafana](/deploy-monitoring-services.md#configure-grafana).
