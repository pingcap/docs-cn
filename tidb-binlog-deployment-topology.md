---
title: TiDB Binlog Deployment Topology
summary: Learn the deployment topology of TiDB Binlog based on the minimal TiDB topology.
aliases: ['/docs/dev/tidb-binlog-deployment-topology/']
---

# TiDB Binlog Deployment Topology

This document describes the deployment topology of TiDB Binlog based on the minimal TiDB topology.

TiDB Binlog is the widely used component for replicating incremental data. It provides near real-time backup and replication.

## Topology information

| Instance | Count | Physical machine configuration | IP | Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 3 | 16 VCore 32 GB | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | Default port configuration; <br/> Enable `enable_binlog`; <br/> Enable `ignore-error` |
| PD | 3 | 4 VCore 8 GB | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | Default port configuration |
| TiKV | 3 | 16 VCore 32 GB | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | Default port configuration |
| Pump| 3 | 8 VCore 16GB | 10.0.1.1 <br/> 10.0.1.7 <br/> 10.0.1.8 | Default port configuration; <br/> Set GC time to 7 days |
| Drainer | 1 | 8 VCore 16GB | 10.0.1.12 | Default port configuration; <br/> Set the default initialization commitTS -1 as the latest timestamp; <br/> Configure the downstream target TiDB as `10.0.1.12:4000` |

### Topology templates

- [The simple template for the TiDB Binlog topology (with `mysql` as the downstream type)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml)
- [The simple template for the TiDB Binlog topology (with `file` as the downstream type)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml)
- [The complex template for the TiDB Binlog topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml)

### Key parameters

The key parameters in the topology configuration templates are as follows:

- `server_configs.tidb.binlog.enable: true`

    - Enables the binlog service.
    - Default value: `false`.

- `server_configs.tidb.binlog.ignore-error: true`

    - It is recommended to enable this configuration in high availability scenarios.
    - If set to `true`, when an error occurs, TiDB stops writing data into binlog, and adds `1` to the value of the `tidb_server_critical_error_total` monitoring metric.
    - If set to `false`, when TiDB fails to write data into binlog, the whole TiDB service is stopped.

- `drainer_servers.config.syncer.db-type`

    The downstream type of TiDB Binlog. Currently, `mysql`, `tidb`, `kafka`, and `file` are supported.

- `drainer_servers.config.syncer.to`

    The downstream configuration of TiDB Binlog. Depending on different `db-type`s, you can use this configuration item to configure the connection parameters of the downstream database, the connection parameters of Kafka, and the file save path. For details, refer to [TiDB Binlog Configuration File](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto).

> **Note:**
>
> - When editing the configuration file template, if you do not need custom ports or directories, modify the IP only.
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.
