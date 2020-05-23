# 部署需求

设置默认部署目录 `/tidb-deploy` 和数据目录 `/tidb-data`，通过 TiDB Binlog 同步到下游机器 10.0.1.12:4000。


# 拓扑信息

| 实例 |个数| 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
|TiDB | 3 | 16 VCore 32 GB | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口配置；<br>开启 enable_binlog； <br> 开启 ignore-error |
| PD | 3 | 4 VCore 8 GB | 10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | 默认端口配置 |
| TiKV | 3 | 16 VCore 32 GB | 10.0.1.7 <br> 10.0.1.8 <br> 10.0.1.9 | 默认端口配置 |
| Pump| 3 |8 VCore 16GB |10.0.1.1 <br> 10.0.1.7 <br> 10.0.1.8 | 默认端口配置； <br> 设置 GC 时间 7 天 |
| Drainer | 1 | 8 VCore 16GB | 10.0.1.12 | 默认端口配置；<br> 设置默认初始化 commitTS -1 为最近的时间戳 <br> 配置下游目标 TiDB 10.0.1.12:4000 |

# 配置文件模版 topology.yaml

[简单 TiDB-binlog 配置](/simple-tidb-binlog.yaml)
[复杂 TiDB-binlog 配置](/complex-tidb-binlog.yaml)

> **注意：**
>
> - 配置文件模版时，如无需自定义端口或者目录，仅修改 IP 即可。

# 关键 TIDB 参数

- `binlog.enable: true`

    开启 binlog 服务，默认为 false。

- `binlog.ignore-error: true`

    高可用场景建议开启，如果设置为 true，发生错误时，TiDB 会停止写入 binlog，并且在监控项 tidb_server_critical_error_total 上计数加 1；如果设置为 false，一旦写入 binlog 失败，会停止整个 TiDB 的服务。