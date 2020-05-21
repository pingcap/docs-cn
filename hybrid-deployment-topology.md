#### 部署需求

部署 TiDB 和 TiKV 组件的物理机为 2 路处理器，每路 16 VCore，内存也达标，为提高物理机资源利用率，可为单机多实例，即 TiDB、TiKV 通过 numa 绑核，隔离 CPU 资源。PD 和 Prometheus 混合部署，但两者的数据目录需要使用独立的文件系统。

#### 单机多实例部署的关键参数配置

本节介绍单机多实例的关键参数，主要用于 TiDB、TiKV 的单机多实例部署场景。你需要按照提供的计算公式，将结果填写至下一步的配置文件中。

- TiKV 进行配置优化

    - readpool 线程池自适应，配置 `readpool.unified.max-thread-count` 参数可以使 `readpool.storage` 和 `readpool.coprocessor` 共用统一线程池，同时要分别设置自适应开关。

        - 开启 `readpool.storage` 和 `readpool.coprocessor`：
          
            ```yaml
            readpool.storage.use-unified-pool: false
            readpool.coprocessor.use-unified-pool: true
            ```

        - 计算公式如下：

            ```
            readpool.unified.max-thread-count = cores * 0.8 / TiKV 数量
            ```

    - storage CF (all RocksDB column families) 内存自适应，配置 `storage.block-cache.capacity` 参数即可实现 CF 之间自动平衡内存使用。

        - `storage.block-cache` 默认开启 CF 自适应，无需修改。

            ```yaml
            storage.block-cache.shared: true
            ```
     
        - 计算公式如下：

            ```
            storage.block-cache.capacity = (MEM_TOTAL * 0.5 / TiKV 实例数量)
            ```

    - 如果多个 TiKV 实例部署在同一块物理磁盘上，需要在 tikv 配置中添加 capacity 参数：

        ```
        raftstore.capacity = 磁盘总容量 / TiKV 实例数量
        ```

- label 调度配置

    由于采用单机多实例部署 TiKV，为了避免物理机宕机导致 Region Group 默认 3 副本的 2 副本丢失，导致集群不可用的问题，可以通过 label 来实现 PD 智能调度，保证同台机器的多 TiKV 实例不会出现 Region Group 只有 2 副本的情况。

    - TiKV 配置

        相同物理机配置相同的 host 级别 label 信息：

        ```yml
        config:
          server.labels:
            host: tikv1
        ```

    - PD 配置

        PD 需要配置 labels 类型来识别并调度 Region：

        ```yml
        pd:
          replication.location-labels: ["host"]
        ```

- `numa_node` 绑核

    - 在实例参数模块配置对应的 `numa_node` 参数，并添加对应的物理 CPU 的核数；

    - numa 绑核使用前，确认已经安装 numactl 工具，以及物理机对应的物理机 CPU 的信息后，再进行参数配置；

    - `numa_node` 这个配置参数与 `numactl --membind` 配置对应。 

#### 拓扑信息

| 实例 | 个数 | 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiKV | 6 | 32 VCore 64GB | 10.0.1.1<br> 10.0.1.2<br> 10.0.1.3 | 1. 区分实例级别的 port、status_port；<br> 2. 配置全局参数 readpool、storage 以及 raftstore 参数；<br> 3. 配置实例级别 host 维度的 labels；<br> 4. 配置 numa 绑核操作|
| TiDB | 6 | 32 VCore 64GB | 10.0.1.7<br> 10.0.1.8<br> 10.0.1.9 | 配置 numa 绑核操作 |
| PD | 3 | 16 VCore 32 GB | 10.0.1.4<br> 10.0.1.5<br> 10.0.1.6 | 配置 location_lables 参数 |
| TiFlash | 1 | 32 VCore 64 GB | 10.0.1.10 | 默认端口 <br> 自定义部署目录，配置 data_dir 参数为 `/data1/tiflash/data` |

#### 配置文件模版 topology.yaml

> **注意：**
>
> - 配置文件模版时，注意修改必要参数、IP、端口及目录。
>
> - 各个组件的 deploy_dir，默认会使用 global 中的 <deploy_dir>/<components_name>-<port>。例如 tidb 端口指定 4001，则 deploy_dir 默认为 /tidb-deploy/tidb-4001。因此，在多实例场景下指定非默认端口时，无需再次指定目录。

> **注意：**
>
> - [部署 TiFlash](/tiflash/deploy-tiflash.md) 需要在 topology.yaml 配置文件中将 `replication.enable-placement-rules` 设置为 `true`，以开启 PD 的 [Placement Rules](/configure-placement-rules.md) 功能。
>
> - tiflash_servers 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。
>
> - TiFlash 具体的参数配置介绍可参考 [TiFlash 参数配置](#tiflash-参数)。

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

server_configs:
  tikv:
    readpool.unified.max-thread-count: <取值参考上文计算公式的结果>
    readpool.storage.use-unified-pool: false
    readpool.coprocessor.use-unified-pool: true
    storage.block-cache.capacity: "<取值参考上文计算公式的结果>"
    raftstore.capacity: "<取值参考上文计算公式的结果>"
  pd:
    replication.location-labels: ["host"]
    replication.enable-placement-rules: true

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.7
    port: 4000
    status_port: 10080
    numa_node: "0"
  - host: 10.0.1.7
    port: 4001
    status_port: 10081
    numa_node: "1"
  - host: 10.0.1.8
    port: 4000
    status_port: 10080
    numa_node: "0"
  - host: 10.0.1.8
    port: 4001
    status_port: 10081
    numa_node: "1"
  - host: 10.0.1.9
    port: 4000
    status_port: 10080
    numa_node: "0"
  - host: 10.0.1.9
    port: 4001
    status_port: 10081
    numa_node: "1"

tikv_servers:
  - host: 10.0.1.1
    port: 20160
    status_port: 20180
    numa_node: "0"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.1
    port: 20161
    status_port: 20181
    numa_node: "1"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.2
    port: 20160
    status_port: 20180
    numa_node: "0"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.2
    port: 20161
    status_port: 20181
    numa_node: "1"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.3
    port: 20160
    status_port: 20180
    numa_node: "0"
    config:
      server.labels: { host: "tikv3" }
  - host: 10.0.1.3
    port: 20161
    status_port: 20181
    numa_node: "1"
    config:
      server.labels: { host: "tikv3" }
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data
monitoring_servers:
  - host: 10.0.1.7
grafana_servers:
  - host: 10.0.1.7
alertmanager_servers:
  - host: 10.0.1.7
```

更详细的配置为:

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  deploy_dir: "/tidb-deploy/monitored-9100"
  data_dir: "/tidb-data-monitored-9100"
  log_dir: "/tidb-deploy/monitored-9100/log"

server_configs:
  tikv:
    readpool.unified.max-thread-count: <取值参考上文计算公式的结果>
    readpool.storage.use-unified-pool: false
    readpool.coprocessor.use-unified-pool: true
    storage.block-cache.capacity: "<取值参考上文计算公式的结果>"
    raftstore.capacity: "<取值参考上文计算公式的结果>"
  pd:
    replication.location-labels: ["host"]
    replication.enable-placement-rules: true

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.7
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.7
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"
  - host: 10.0.1.8
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.8
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"
  - host: 10.0.1.9
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.9
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"

tikv_servers:
  - host: 10.0.1.1
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.1
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.2
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.2
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.3
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv3" }
  - host: 10.0.1.3
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv3" }
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data
monitoring_servers:
  - host: 10.0.1.7
grafana_servers:
  - host: 10.0.1.7
alertmanager_servers:
  - host: 10.0.1.7
```