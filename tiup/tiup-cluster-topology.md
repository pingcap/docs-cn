---
tiup-cluster 拓扑文件描述
---

# tiup-cluster 拓扑文件描述

本文档描述 tiup-cluster 的拓扑文件，你可以在 [topology.example.yaml](https://github.com/pingcap/tiup/blob/master/examples/topology.example.yaml) 找到拓扑文件样例。

## global

全局相关配置。

全局相关配置会应用到全部部署实例, 当实例没有相关配置时会使用全局的配置做为默认值。

### `user`

+ 部署用户。
+ 默认值："tidb"

### `group`

+ 部署用户的用户组

### `ssh_port`

+ 登录到部署上时使用的端口。
+ 默认值：22

### `deploy_dir`

+ 部署目录。
+ 默认值："deploy"

### `data_dir`

+ 部署存放数据的目录。
+ 默认值："data"

### `log_dir`

+ 部署组件日志的目录。
+ 默认值：""

### `arch`

+ 部署集群的体系，支持: "amd64", "arm64"
+ 默认值："amd64"

### resource_control

systemd 控制进程资源的相关配置。

#### `memory_limit`

+ 参考 [MemoryLimit](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html#MemoryLimit=bytes)

#### `cpu_quota`

+ 参考 [CPUQuota](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html#CPUQuota=)

#### `io_read_bandwidth_max`

+ 参考 [IOReadBandwidthMax](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html#IOReadBandwidthMax=device%20bytes)

#### `io_write_bandwidth_max`

+ 参考 [IOWriteBandwidthMax](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html#IOReadBandwidthMax=device%20bytes)

### `monitored`

部署集群上监控相关配置，涉及集群上每个机器部署的 node-exporter 跟 blackbox-export 的配置。

#### `node_exporter_port`

+ node-exporter 的端口。
+ 默认值：9100

#### `blackbox_exporter_port`

+ blackbox-exporter 的端口
+ 默认值：9115

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/monitored-{client_port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/monitored-{node_exporter_port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/monitored-{node_exporter_port}/log"

## server_configs

各个组件相关配置，相关组件配置可以看对应组件文档。

### pd

+ PD 配置，参考 [PD 配置文件描述](/pd-configuration-file.md)

### tidb

+ TiDB 配置，参考 [TiDB 配置文件描述](/tidb-configuration-file.md)

### tikv

+ TiKV 配置，参考 [TiKV 配置文件描述](/tikv-configuration-file.md)

### tiflash

+ TiFlash 配置，参考[TiFlash 配置文件描述](/tiflash/tiflash-configuration.md)

### tiflash-learner

+ TiFlash-Learner 配置，参考[TiFlash 配置文件描述](/tiflash/tiflash-configuration.md)

### pump

+ Pump 配置，参考 [TiDB Binlog 配置说明](/tidb-binlog/tidb-binlog-configuration-file.md)

## pd_servers

部署 PD 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/pd-{client_port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/pd-{client_port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/pd-{client_port}/log"

### `name`

+ PD 结点名称。
+ 默认值："pd-{host}:{client_port}"

### `client_port`

+ PD `client-urls` 使用的端口。
+ 默认值：2379

### `peer_port`

+ PD `peer-urls` 使用的端口。
+ 默认值：2380

### config

+ PD 配置，参考 [PD 配置文件描述](/pd-configuration-file.md)
+ 覆盖 {server_configs.pd} 的配置。

## tidb_servers

部署 TiDB 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/tidb-{port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/tidb-{port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/tidb-{port}/log"

### `port`

+ TiDB 提供服务的端口。
+ 默认值：4000

### `status_port`

+ TiDB `status` 端口
+ 默认值：10080

### config

+ TiDB 配置，参考 [TiDB 配置文件描述](/tidb-configuration-file.md)
+ 覆盖 {server_configs.tidb} 的配置。

## tikv_servers

部署 TiKV 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/tikv-{port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/tikv-{port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/tikv-{port}/log"

### `port`

+ 默认值：20160

### `status_port`

+ 默认值：20180

### config

+ TiKV 配置，参考 [TiKV 配置文件描述](/tikv-configuration-file.md)
+ 覆盖 {server_configs.tikv} 的配置。

## tiflash_servers

部署 TiFlash 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/tiflash-{tcp_port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/tiflash-{tcp_port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/tiflash-{tcp_port}/log"

### `tcp_port`

+ 默认值：9000

### `http_port`

+ 默认值：8123

### `flash_service_port`

+ 默认值：3930

### `flash_proxy_port`

+ 默认值：20170

### `flash_proxy_status_port`

+ 默认值：20292

### `metrics_port`

+ 默认值：8234

### config

+ TiFlash 配置。

+ 覆盖 {server_configs.tiflash} 的配置。

    > **注意：**
    >
    > `path_realtime_mode` 只有 `tiflash_servers.data_dir` 配置了多个路径时才有做用。
    > path_realtime_mode:
    >     "true" 除了第一个路径，其它的路径都可以用来保存老数据。
    >     "false" 全部路径都可以用来保存老数据。
    >
    > TiFlash 只使用第一个路径来存放新数据 (i.e. "delta")。 其它路径存放老数据。 (i.e. "stable". 此部分数据占大部分整体数据),
    >
    > E.g, 如果你希望使用一个快速且容量较小的 NVMe SSD (256GB) 来加速 TiFlash 的 data ingestion， 
    > 另外使用 4 个一般的 SSDs (512GB) 做为存储。那么你的配置可以如下：
    >
    > data_dir: /nvme_ssd_256/data,/ssd1_512/data,/ssd2_512/data,/ssd3_512/data,/ssd4_512/data
    > config:
    >     path_realtime_mode: true
    >
    > 如果你的第一个硬盘容量足够大，你可以如下配置来充分使用它：
    >
    > data_dir: /nvme_ssd_256/data,/ssd1_512/data,/ssd2_512/data,/ssd3_512/data,/ssd4_512/data
    > config:
    >     path_realtime_mode: false

### learner_config

+ Learner 配置
+ 覆盖 {server_configs.tiflash-learner} 的配置。

## pump_servers:

部署 Pump 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/pump-{port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/pump-{port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/pump-{port}/log"

### `port`

+ Pump 端口。
+ 默认值：8250

### config

+ Pump 配置，参考 [TiDB Binlog 配置说明](/tidb-binlog/tidb-binlog-configuration-file.md)
+ 覆盖 {server_configs.pump} 的配置。

## drainer_servers:

部署 Drainer 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/drainer-{port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/drainer-{port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/drainer-{port}/log"

### `port`

+ 默认值：8249

### `commit_ts`

+ 即 drainer 的 [`initial-commit-ts`](/tidb-binlog/tidb-binlog-configuration-file.md#initial-commit-ts)

    > **注意：**
    >
    > 请勿在 config 下配置 `initial-commit-ts`，config 下 `initial-commit-ts` 会被此参数覆盖不生效。

### config

+ Drainer 配置，参考 [TiDB Binlog 配置说明](/tidb-binlog/tidb-binlog-configuration-file.md)

## cdc_servers

部署 cdc 的实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/cdc-{port}"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/cdc-{port}/log"

### `port`

+ cdc 使用的端口。
+ 默认值：8300

### `gc-ttl`

+ cdc server 的 `gc-ttl` 命令行参数

### `tz`

+ cdc server 的`tz` 命令行参数

## tispark_masters

部署 tispark master 的实例，目前只支持部署一个实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/tispark-master-{port}"

### `listen_host`

### `port`

+ 默认值：7078

### `web_port`

+ 默认值：8081

### spark_config

### spark_env

## tispark_workers

部署 tispark worker 的实例, 不支持同一 `host` 部署多个实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/tispark-worker-{port}"

## monitoring_servers

部署 Prometheus 实例的配置，目前支持部署一个实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/prometheus-{port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/prometheus-{port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/prometheus-{port}/log"

### `port`

+ 默认值：9090

## grafana_servers

部署 Grafana 实例的配置，目前支持部署一个实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/grafana-{port}"

### `port`

+ 默认值：3000

## alertmanager_servers

部署 Alertmanager 实例的配置，目前支持部署一个实例。

### host

+ 部署机器的 ip 。

### ssh_port

+ 部署机器的 ssh 端口。
+ 默认值: {global.ssh_port} .

### deploy_dir

+ 部署目录
+ 默认值："{global.deploy_dir}/altermanager-{web_port}"

### data_dir

+ 数据目录
+ 默认值："{global.data_dir}/altermanager-{web_port}/data"

### log_dir

+ 日志目录
+ 默认值："{global.data_dir}/altermanager-{web_port}/log"

### `web_port`

+ 默认值：9093

### `cluster_port`

+ 默认值：9094
