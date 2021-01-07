---
title: tiup cluster topology reference
aliases: ['/docs-cn/dev/tiup/tiup-cluster-topology-reference/']
---

# tiup cluster topology reference

## 介绍

在部署或扩容 TiDB 集群时，需要提供一份拓扑文件来描述集群拓扑，同样，修改配置也是通过编辑拓扑文件来实现的，区别在于修改配置时仅允许修改部分字段。

拓扑文件[示例参考](https://github.com/pingcap/tiup/blob/master/examples/topology.example.yaml)。

## 文件结构

一个 TiDB 集群的拓扑文件可能包含以下区块：

- [global](/tiup/tiup-cluster-topology-reference.md#global)：集群全局配置，其中一些是集群的默认值，可以在实例里面单独配置
- [monitored](/tiup/tiup-cluster-topology-reference.md#monitored)：监控服务配置，即 blackbox exporter 和 node exporter，每台机器上都会部署一个 node expoter 一个 blackbox exporter
- [server_configs](/tiup/tiup-cluster-topology-reference.md#server_configs)：全局服务配置，针对每种组件配置其默认配置，这个配置可以在每个实例里单独覆盖，该配置用于生成服务的配置文件
- [pd_servers](/tiup/tiup-cluster-topology-reference.md#pd_servers)：PD 实例的配置，用来指定 PD 组件部署到哪些机器上
- [tidb_servers](/tiup/tiup-cluster-topology-reference.md#tidb_servers)： TiDB 实例的配置，用来指定 TiDB 组件部署到哪些机器上
- [tikv_servers](/tiup/tiup-cluster-topology-reference.md#tikv_servers)：TiKV 实例的配置，用来指定 TiKV 组件部署到哪些机器上
- [tiflash_servers](/tiup/tiup-cluster-topology-reference.md#tiflash_servers)：TiFlash 实例的配置，用来指定 TiFlash 组件部署到哪些机器上
- [pump_servers](/tiup/tiup-cluster-topology-reference.md#pump_servers)：Pump 实例的配置，用来指定 Pump 组件部署到哪些机器上
- [drainer_servers](/tiup/tiup-cluster-topology-reference.md#drainer_servers)：Drainer 实例的配置，用来指定 Drainer 组件部署到哪些机器上
- [cdc_servers](/tiup/tiup-cluster-topology-reference.md#cdc_servers)：CDC 实例的配置，用来指定 CDC 组件部署到哪些机器上
- [tispark_masters](/tiup/tiup-cluster-topology-reference.md#tispark_masters)：TiSpark Master 实例的配置，用来指定 TiSpark Master 组件部署到哪台机器上，仅允许部署一个 TiSpark Master 节点
- [tispark_workers](/tiup/tiup-cluster-topology-reference.md#tispark_workers)：TiSpark Worker 实例的配置，用来指定 TiSpark Worker 组件部署到哪些机器上
- [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers)：Prometheus 实例的配置，用来指定 Prometheus 部署在哪台机器上
- [grafana_servers](/tiup/tiup-cluster-topology-reference.md#grafana_servers)：Grafana 实例的配置，用来指定 Grafana 部署在哪台机器上
- [alertmanager_servers](/tiup/tiup-cluster-topology-reference.md#alertmanager_servers)：Alertemanager 实例的配置，用来指定 Alertmanager 部署在哪些机器上

### global

global 区块集群的全局配置，包含以下字段：

- user：以什么用户来启动部署的集群，默认值："tidb"，如果 `<user>` 字段指定的用户在目标机器上不存在，会自动尝试创建
- group：自动创建用户时指定用户所属的用户组，默认和 `<user>` 字段值相同，若指定的组不存在，则自动创建
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，默认值：22
- enable_tls：是否对集群启用 tls，启用之后集群之间，客户端与集群之间都必须用生成的 tls 证书链接，启用后无法关闭，默认值：false
- deploy_dir：每个组件的默认部署目录，默认值："deploy"，其应用规则如下：
  - 如果 `<deploy_dir>` 为绝对路径，那么组件会部署到 `<deploy_dir>/<component-name>-<component-port>` 目录
  - 如果 `<deploy_dir>` 为相对路径，那么组件会部署到 `/home/<user>/<deploy_dir>/<component-name>-<component-port>` 目录
  - 对于在自己的实例中设置了 `deploy_dir` 字段的组件实例，部署路径由实例中的 `deploy_dir` 决定
- data_dir：默认数据目录, 默认值 "data"，其应用规则如下：
  - 如果 `<data_dir>` 为绝对路径，那么组件数据将放到 `<data_dir>/<component-name>-<component-port>`
  - 如果 `<data_dir>` 为相对路径，那么组件数据将放到 `<deploy_dir>/<data_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
  - 对于在自己的实例中设置了 `data_dir` 字段的组件实例，数据路径由实例中的 `data_dir` 决定
- log_dir：默认数据目录, 默认值 "log"，其应用规则如下：
  - 如果 `<log_dir>` 为绝对路径，那么组件日志将放到 `<log_dir>/<component-name>-<component-port>`
  - 如果 `<log_dir>` 为相对路径，那么组件日志将放到 `<deploy_dir>/<log_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
  - 对于在自己的实例中设置了 `log_dir` 字段的组件实例，日志路径由实例中的 `log_dir` 决定
- os：目标机器的操作系统，该字段决定了向目标机器推送适配哪个操作系统的组件，默认值：linux
- arch：目标机器的架构，该字段决定了向目标机器推送哪个平台的二进制包，支持 amd64 和 arm64，默认值 amd64
- resource_control：运行时资源控制，该字段下所有配置都将写入 systemd 的 service 文件中，默认不限制，支持控制的资源：
  - memory_limit: 限制运行时最大内存，例如 "2G" 表示最多使用 2G 内存
  - cpu_quota：限制运行时最大 CPU 占用率，例如 "200%" 
  - io_read_bandwidth_max：读磁盘 IO 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
  - io_write_bandwidth_max：写磁盘 IO 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
  - limit_core：控制 core dump 大小

global 配置示例：

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

### monitored

monitored 用于配置目标机上的监控服务：node_exporter 和 blackbox_exporter，它包含这些字段：

- node_exporter_port: node_exporter 的服务端口，默认值 9100
- blackbox_exporter_port：blackbox_exporter 的服务端口，默认值 9115
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成

monitored 配置示例：

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

### server_configs

server_configs 用于配置服务，生成各组件的配置文件，类似 global 区块，该区块内的配置可以在具体的实例中被覆盖。主要包含以下字段：

- tidb：TiDB 服务的相关配置，支持的所有配置请参考[TiDB 配置文件描述](/tidb-configuration-file.md)
- tikv：TiKV 服务的相关配置，支持的所有配置请参考[TiKV 配置文件描述](/tikv-configuration-file.md)
- pd：PD 服务的相关配置，支持的所有配置请参考[PD 配置文件描述](/pd-configuration-file.md)
- tiflash：TiFlash 服务的相关配置，支持的所有配置请参考[TiFlash 配置参数](/tiflash-configuration.md)
- tiflash_learner：每个 TiFlash 中内置了一个特殊的 TiKV，该配置用于配置这个特殊的 TiKV，一般不建议修改这个配置下的内容
- pump：pump 服务相关配置，支持的所有配置请参考[TiDB Binlog 配置说明](/tidb-binlog-configuration-file.md#pump)
- drainer：drainer 服务相关配置，支持的所有配置请参考[TiDB Binlog 配置说明](/tidb-binlog-configuration-file.md#drainer)
- cdc：cdc 服务相关配置，支持的所有配置请参考[TiCDC 安装部署](/deploy-ticdc.md)

server_configs 配置示例：

```yaml
server_configs:
  tidb:
    run-ddl: true
    lease: "45s"
    split-table: true
    token-limit: 1000
  tikv:
    log-level: "info"
    readpool.unified.min-thread-count: 1
```

### pd_servers

pd_servers 约定了将 PD 的服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组的元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- listen_host：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 host 所指定的 IP
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- name：指定该 PD 实例的名字，不同实例的名字不能相同
- client_port：指定 pd 的客户端链接端口，默认是 2379
- peer_port：指定 pd 之间互相通信的端口，默认是 2380
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 pd 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 pd 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- listen_host
- name
- client_port
- peer_port
- deploy_dir
- data_dir
- log_dir
- arch
- os

pd_servers 配置示例：

```yaml
pd_servers:
  - host: 10.0.1.11
    config:
      schedule.max-merge-region-size: 20
      schedule.max-merge-region-keys: 200000
  - host: 10.0.1.12
```

### tidb_servers

tidb_servers 约定了将 TiDB 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组的元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- listen_host：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 host 所指定的 IP
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：TiDB 服务的监听端口，用于提供给 MySQL 客户端连接，默认 4000
- status_port：TiDB 状态服务的监听端口，用于外部通过 http 请求查看 TiDB 服务的状态，默认 10080
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 tidb 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 tidb 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- listen_host
- port
- status_port
- deploy_dir
- log_dir
- arch
- os

tidb_servers 配置示例：

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### tikv_servers

tikv_servers 约定了将 TiKV 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- listen_host：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 host 所指定的 IP
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：TiKV 服务的监听端口，默认 20160
- status_port：TiKV 状态服务的监听端口，默认 20180
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 tikv 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 tikv 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- listen_host
- port
- status_port
- deploy_dir
- data_dir
- log_dir
- arch
- os

tikv_servers 配置示例：

```yaml
tikv_servers:
  - host: 10.0.1.14
    config:
      server.labels: { zone: "zone1", host: "host1" }
  - host: 10.0.1.15
    config:
      server.labels: { zone: "zone1", host: "host2" }
```

### tiflash_servers

tiflash_servers 约定了将 TiFlash 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- tcp_port：TiFlash TCP 服务的端口，默认 9000
- http_port：TiFlash HTTP 服务的端口，默认 8123
- flash_service_port：TiFlash 提供服务的端口，TiDB 通过该端口从 TiFlash 读数据，默认 3930
- metrics_port：TiFlash 的状态端口，用于输出 metric 数据，默认 8234
- flash_proxy_port：内置 TiKV 的端口，默认 20170
- flash_proxy_status_port：内置 TiKV 的状态端口，默认为 20292
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成，TiFlash 的数据目录支持多个，采用逗号分割
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- tmp_path: TiFlash 临时文件的存放路径，默认使用 [`path` 或者 `storage.latest.dir` 的第一个目录] + "/tmp"
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 tiflash 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 tiflash 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- learner_config：每个 TiFlash 中内置了一个特殊的 TiKV，该配置用于配置这个特殊的 TiKV，一般不建议修改这个配置下的内容
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，data_dir 在部署完成之后只能新增目录，而以下字段在部署完成之后就不能再修改：

- host
- tcp_port
- http_port
- flash_service_port
- flash_proxy_port
- flash_proxy_status_port
- metrics_port
- deploy_dir
- log_dir
- tmp_path
- arch
- os

tiflash_servers 配置示例：

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### pump_servers

pump_servers 约定了将 Binlog 组件的 Pump 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：Pump 服务的监听端口，默认 8250
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 pump 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 pump 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- port
- deploy_dir
- data_dir
- log_dir
- arch
- os

pump_servers 配置示例：

```yaml
pump_servers:
  - host: 10.0.1.21
    config:
      gc: 7
  - host: 10.0.1.22
```

### drainer_servers

drainer_servers 约定了将 Binlog 组件的 Drainer 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：Drainer 服务的监听端口，默认 8249
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- commit_ts：Drainer 启动的时候会去读取 checkpoint，如果读取不到，就会使用该字段做为初次启动开始的同步时间点，该字段默认为 -1（从 PD 总获取最新时间戳作为 commit_ts）
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 drainer 配置规则相同，若配置了该字段，会将该字段内容和 server_configs 里的 drainer 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- port
- deploy_dir
- data_dir
- log_dir
- commit_ts
- arch
- os

drainer_servers 配置示例：

```yaml
drainer_servers:
  - host: 10.0.1.21
    config:
      syncer.db-type: "mysql"
      syncer.to.host: "127.0.0.1"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 3306
      syncer.ignore-table:
        - db-name: test
          tbl-name: log
        - db-name: test
          tbl-name: audit
```

### cdc_servers

cdc_servers 约定了将 CDC 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：CDC 服务的监听端口，默认 8300
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- gc-ttl：TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 86400，即 24 小时
- tz：TiCDC 服务使用的时区。TiCDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config：该字段配置规则和 server_configs 里的 cdc 内容合并（若字段冲突，以该字段为准），然后生成配置文件下发到 host 指定的机器
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- port
- deploy_dir
- log_dir
- gc-ttl
- tz
- arch
- os

cdc_servers 配置示例：

```yaml
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
  - host: 10.0.1.21
```

### tispark_masters

tispark_masters 约定了将 TiSpark 的 master 节点部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- listen_host：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 host 所指定的 IP
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：Spark 的监听端口，节点之前通讯用，默认 7077
- web_port：Spark 的网页端口，提供网页服务，可查看任务情况，默认 8080
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- java_home：指定要使用的 JRE 环境所在的路径。该参数对应系统环境变量 JAVA_HOME
- spark_config：用于配置 TiSpark 服务，生成配置文件下发到 host 指定的机器
- spark_env：配置 Spark 启动时的环境变量
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- listen_host
- port
- web_port
- deploy_dir
- arch
- os

tispark_masters 配置示例：

```yaml
tispark_masters:
  - host: 10.0.1.21
    spark_config:
      spark.driver.memory: "2g"
      spark.eventLog.enabled: "False"
      spark.tispark.grpc.framesize: 2147483647
      spark.tispark.grpc.timeout_in_sec: 100
      spark.tispark.meta.reload_period_in_sec: 60
      spark.tispark.request.command.priority: "Low"
      spark.tispark.table.scan_concurrency: 256
    spark_env:
      SPARK_EXECUTOR_CORES: 5
      SPARK_EXECUTOR_MEMORY: "10g"
      SPARK_WORKER_CORES: 5
      SPARK_WORKER_MEMORY: "10g"
  - host: 10.0.1.22
```

### tispark_workers

tispark_workers 约定了将 TiSpark 的 worker 节点部署到哪些机器上，同时可以指定每台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- listen_host：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 host 所指定的 IP
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：Spark 的监听端口，节点之前通讯用，默认 7077
- web_port：Spark 的网页端口，提供网页服务，可查看任务情况，默认 8080
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- java_home：指定要使用的 JRE 环境所在的路径。该参数对应系统环境变量 JAVA_HOME
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- listen_host
- port
- web_port
- deploy_dir
- arch
- os

tispark_workers 配置示例：

```yaml
tispark_workers:
  - host: 10.0.1.22
  - host: 10.0.1.23
```

### monitoring_servers

monitoring_servers 约定了将 Prometheus 服务部署到哪台机器上，同时可以指定这台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：指定 Prometheus 提供服务的端口，默认是 9090
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- storage_retention：Prometheus 监控数据保留时间，默认 "15d"
- rule_dir：该字段指定一个本地目录，该目录中应当含有完整的 *.rules.yml 文件，这些文件会在集群配置初始化阶段被传输到目标机器上，作为 Prometheus 的规则
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- port
- deploy_dir
- data_dir
- log_dir
- arch
- os

monitoring_servers 配置示例：

```yaml
monitoring_servers:
  - host: 10.0.1.11
    rule_dir: /local/rule/dir
```

### grafana_servers

grafana_servers 约定了将 Grafana 服务部署到哪台机器上，同时可以指定这台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- port：指定 Grafana 提供服务的端口，默认是 3000
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- username：Grafana 登陆界面的用户名
- password：Grafana 对应的密码
- dashboard_dir：该字段指定一个本地目录，该目录中应当含有完整的 dashboard(*.json) 文件，这些文件会在集群配置初始化阶段被传输到目标机器上，作为 Grafana 的 dashboards
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

> **注意：**
>
> 如果配置了 grafana_servers 的 dashboard_dir 字段，在执行 tiup cluster rename 命令进行集群重命名后，需要完成以下操作：
>
> 1. 对于本地的 dashboards 目录中的 `*.json` 文件，将 datasource 字段的值更新为新的集群名（这是因为 datasource 是以集群名命名的）
> 2. 执行 tiup cluster reload -R grafana 命令

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- port
- deploy_dir
- arch
- os

grafana_servers 配置示例：

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### alertmanager_servers

alertmanager_servers 约定了将 Alertmanager 服务部署到哪些机器上，同时可以指定这台机器上的服务配置，它是一个数组，每个数组元素包含以下字段：

- host：部署到哪台机器，填 IP 地址，不可省略
- ssh_port：指定连目标机器进行操作的时候默认连哪个 ssh 端口，若不指定，则使用 global 区块中的 ssh_port
- web_port：指定 Alertmanager 提供网页服务的端口，默认是 9093
- cluster_port：指定 Alertmanger 和 其他 Alertmanager 通讯的端口，默认是 9094
- deploy_dir：指定部署目录，若不指定，则按照 global 中配置的 deploy_dir 生成
- data_dir：指定数据目录，若不指定，则按照 global 中配置的 data_dir 生成
- log_dir：指定日志目录，若不指定，则按照 global 中配置的 log_dir 生成
- numa_node：给改实例分配 numa 节点，如果指定了该参数，需要确保目标机装了numactl，在指定该参数的情况下会通过 numactl 分配 cpubind 和 membind。这个参数类型是一个 string，里面填 numa 节点 id，比如 "0,1"
- config_file：该字段指定一个本地文件，该文件会在集群配置初始化阶段被传输到目标机器上，作为 Alertmanager 的配置
- os：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 global 中的 os
- arch：host 字段所指定的机器的架构，若不指定该字段，则默认为 global 中的 arch
- resource_control：针对该服务的资源控制，所配置了该字段，会将该字段和 global 中的 resource_control 内容合并（若字段冲突，以该字段为准），然后生成 systemd 配置文件下发到 host 指定机器。resource_control 的配置规则同 global 中的 resource_control

以上字段中，这些字段在部署完成之后就不能再修改：

- host
- web_port
- cluster_port
- deploy_dir
- data_dir
- log_dir
- arch
- os

alertmanager_servers 配置示例：

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```