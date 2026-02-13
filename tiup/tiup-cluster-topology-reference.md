---
title: 通过 TiUP 部署 TiDB 集群的拓扑文件配置
summary: 介绍通过 TiUP 部署或扩容 TiDB 集群时提供的拓扑文件配置和示例。
---

# 通过 TiUP 部署 TiDB 集群的拓扑文件配置

通过 TiUP 部署或扩容 TiDB 集群时，需要提供一份拓扑文件（[示例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)）来描述集群拓扑。

同样，修改集群配置也是通过编辑拓扑文件来实现的，区别在于修改配置时仅允许修改部分字段。本文档介绍拓扑文件的各个区块以各区块中的各字段。

使用 TiUP 部署 TiDB 集群时，TiUP 会同时自动部署 Prometheus、Grafana 和 Alertmanager 等监控组件，并且在集群扩容中自动为新增节点添加监控配置。如果需要自定义 Prometheus、Grafana 和 Alertmanager 等监控组件的配置，请参考[自定义监控组件的配置](/tiup/customized-montior-in-tiup-environment.md)。

## 文件结构

一个通过 TiUP 部署的 TiDB 集群拓扑文件可能包含以下区块：

- [global](/tiup/tiup-cluster-topology-reference.md#global)：集群全局配置，其中一些是集群的默认值，可以在实例里面单独配置
- [monitored](/tiup/tiup-cluster-topology-reference.md#monitored)：监控服务配置，即 blackbox exporter 和 node exporter，每台机器上都会部署一个 node exporter 和一个 blackbox exporter
- [server_configs](/tiup/tiup-cluster-topology-reference.md#server_configs)：组件全局配置，可单独针对每个组件配置，若在实例中存在同名配置项，那么以实例中配置的为准
- [component_versions](/tiup/tiup-cluster-topology-reference.md#component_versions)：组件版本号，当某个组件需要使用与集群不一致的版本时使用此配置。tiup-cluster v1.14.0 引入该配置
- [pd_servers](/tiup/tiup-cluster-topology-reference.md#pd_servers)：PD 实例的配置，用来指定 PD 组件部署到哪些机器上
- [tidb_servers](/tiup/tiup-cluster-topology-reference.md#tidb_servers)：TiDB 实例的配置，用来指定 TiDB 组件部署到哪些机器上
- [tikv_servers](/tiup/tiup-cluster-topology-reference.md#tikv_servers)：TiKV 实例的配置，用来指定 TiKV 组件部署到哪些机器上
- [tiflash_servers](/tiup/tiup-cluster-topology-reference.md#tiflash_servers)：TiFlash 实例的配置，用来指定 TiFlash 组件部署到哪些机器上
- [tiproxy_servers](#tiproxy_servers)：TiProxy 实例的配置，用来指定 TiProxy 组件部署到哪些机器上
- [kvcdc_servers](/tiup/tiup-cluster-topology-reference.md#kvcdc_servers)：[TiKV-CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/) 实例的配置，用来指定 TiKV-CDC 组件部署到哪些机器上
- [cdc_servers](/tiup/tiup-cluster-topology-reference.md#cdc_servers)：CDC 实例的配置，用来指定 CDC 组件部署到哪些机器上
- [tso_servers](/tiup/tiup-cluster-topology-reference.md#tso_servers)：TSO 实例的配置，用来指定 `tso` 微服务部署在哪些机器上（需要在 [`global`](#global) 中配置 `pd_mode: "ms"` 开启 [PD 微服务](/pd-microservices.md)）
- [scheduling_servers](/tiup/tiup-cluster-topology-reference.md#scheduling_servers)：Scheduling 实例的配置，用来指定 `scheduling` 微服务部署在哪些机器上（需要在 [`global`](#global) 中配置 `pd_mode: "ms"` 开启 [PD 微服务](/pd-microservices.md)）
- [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers)：用来指定 Prometheus 和 NGMonitoring 部署在哪些机器上，TiUP 支持部署多台 Prometheus 实例，但真实投入使用的只有第一个
- [grafana_servers](/tiup/tiup-cluster-topology-reference.md#grafana_servers)：Grafana 实例的配置，用来指定 Grafana 部署在哪台机器上
- [alertmanager_servers](/tiup/tiup-cluster-topology-reference.md#alertmanager_servers)：Alertemanager 实例的配置，用来指定 Alertmanager 部署在哪些机器上

### `global`

`global` 区块为集群的全局配置，包含以下字段：

- `user`：以什么用户来启动部署的集群，默认值："tidb"，如果 `<user>` 字段指定的用户在目标机器上不存在，会自动尝试创建
- `group`：自动创建用户时指定用户所属的用户组，默认和 `<user>` 字段值相同，若指定的组不存在，则自动创建
- `systemd_mode`：部署集群过程中在目标机器上使用的 `systemd` 模式，默认值为 `system`。若设置为 `user`，则表示在目标机器上不使用 sudo 权限，即使用 [TiUP no-sudo 模式](/tiup/tiup-cluster-no-sudo-mode.md)。
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，默认值：22
- `enable_tls`：是否对集群启用 TLS。启用之后，组件之间、客户端与组件之间都必须使用生成的 TLS 证书进行连接，默认值：false
- `listen_host`：默认使用的监听 IP。如果为空，每个实例会根据其 `host` 字段是否包含 `:` 来自动设置为 `::` 或 `0.0.0.0`。tiup-cluster v1.14.0 引入该配置
- `deploy_dir`：每个组件的部署目录，默认值："deploy"。其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `deploy_dir`，那么实际部署目录为该实例设定的 `deploy_dir`
    - 对于每个实例，如果用户未配置 `deploy_dir`，其默认值为相对路径 `<component-name>-<component-port>`
    - 如果 `global.deploy_dir` 为绝对路径，那么组件会部署到 `<global.deploy_dir>/<instance.deploy_dir>` 目录
    - 如果 `global.deploy_dir` 为相对路径，那么组件会部署到 `/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>` 目录
- `data_dir`：数据目录，默认值："data"。其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `data_dir`，那么实际数据目录为该实例设定的 `data_dir`
    - 对于每个实例，如果用户未配置 `data_dir`，其默认值为 `<global.data_dir>`
    - 如果 `data_dir` 为相对路径，那么组件数据将放到 `<deploy_dir>/<data_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
- `log_dir`：日志目录，默认值："log"。其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `log_dir`，那么实际日志目录为该实例设定的 `log_dir`
    - 对于每个实例，如果用户未配置 `log_dir`，其默认值为 `<global.log_dir>`
    - 如果 `log_dir` 为相对路径，那么组件日志将放到 `<deploy_dir>/<log_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
- `os`：目标机器的操作系统，该字段决定了向目标机器推送适配哪个操作系统的组件，默认值：linux
- `arch`：目标机器的 CPU 架构，该字段决定了向目标机器推送哪个平台的二进制包，支持 amd64 和 arm64，默认值：amd64
- `pd_mode`：PD 工作模式。该字段控制是否启用 [PD 微服务](/pd-microservices.md)。取值选项为 "ms"。指定该参数代表启用 PD 微服务模式。
- `resource_control`：运行时资源控制，该字段下所有配置都将写入 systemd 的 service 文件中，默认无限制。支持控制的资源如下：
    - `memory_limit`：限制运行时最大内存，例如 "2G" 表示最多使用 2GB 内存
    - `cpu_quota`：限制运行时最大 CPU 占用率，例如 "200%"
    - `io_read_bandwidth_max`：读磁盘 I/O 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
    - `io_write_bandwidth_max`：写磁盘 I/O 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
    - `limit_core`：控制 core dump 的大小
    - `timeout_stop_sec`：控制 systemd 服务停止的超时时间
    - `timeout_start_sec`：控制 systemd 服务启动的超时时间

`global` 配置示例：

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上述配置指定使用 `tidb` 用户启动集群，同时限制每个组件运行时最多只能使用 2GB 内存。

### `monitored`

`monitored` 用于配置目标机上的监控服务：[node_exporter](https://github.com/prometheus/node_exporter) 和 [blackbox_exporter](https://github.com/prometheus/blackbox_exporter)。包含以下字段：

- `node_exporter_port`：node_exporter 的服务端口，默认值：9100
- `blackbox_exporter_port`：blackbox_exporter 的服务端口，默认值：9115
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成

`monitored` 配置示例：

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

上述配置指定了 node_exporter 使用 9100 端口，blackbox_exporter 使用 9115 端口。

### `server_configs`

`server_configs` 用于配置服务，生成各组件的配置文件，类似 `global` 区块，该区块内的配置可以在具体的实例中被覆盖。主要包含以下字段：

- `tidb`：TiDB 服务的相关配置，支持的完整配置请参考 [TiDB 配置文件描述](/tidb-configuration-file.md)
- `tikv`：TiKV 服务的相关配置，支持的完整配置请参考 [TiKV 配置文件描述](/tikv-configuration-file.md)
- `pd`：PD 服务的相关配置，支持的完整配置请参考 [PD 配置文件描述](/pd-configuration-file.md)
- `tiflash`：TiFlash 服务的相关配置，支持的完整配置请参考 [TiFlash 配置参数](/tiflash/tiflash-configuration.md)
- `tiflash_learner`：每个 TiFlash 中内置了一个特殊的 TiKV，该配置项用于配置这个特殊的 TiKV，一般不建议修改这个配置项下的内容
- `tiproxy`：TiProxy 服务的相关配置，支持的完整配置请参考 [TiProxy 参数配置](/tiproxy/tiproxy-configuration.md)
- `cdc`：CDC 服务的相关配置，支持的完整配置请参考 [TiCDC 安装部署](/ticdc/deploy-ticdc.md)
- `tso`：`tso` 微服务的相关配置，支持的完整配置请参考 [TSO 配置文件描述](/tso-configuration-file.md)
- `scheduling`：`scheduling` 微服务的相关配置，支持的完整配置请参考 [Scheduling 配置文件描述](/scheduling-configuration-file.md)

`server_configs` 配置示例：

```yaml
server_configs:
  tidb:
    lease: "45s"
    split-table: true
    token-limit: 1000
    instance.tidb_enable_ddl: true
  tikv:
    log-level: "info"
    readpool.unified.min-thread-count: 1
```

上述配置指定了 TiDB 和 TiKV 的全局配置。

### `component_versions`

> **注意：**
>
> 对于 TiDB、TiKV、PD、TiCDC 等共用版本号的组件，尚未有完整的测试保证它们在跨版本混合部署的场景下能正常工作。请仅在测试场景或在[获取支持](/support.md)的情况下使用此配置。

`component_versions` 用于指定某个组件的版本号。

- 如果没有配置 `component_versions`，各个组件默认使用与 TiDB 集群相同的版本号（如 PD、TiKV），或使用组件的最新版本号（如 Alertmanager）。
- 如果配置了该字段，对应的组件将会固定使用对应的版本，并且在后续的扩容和升级集群操作中都使用该版本。

请仅在需要使用某个固定组件的版本号时配置该参数。

`component_versions` 区块主要包含以下字段：

- `tikv`：TiKV 组件的版本
- `tiflash`：TiFlash 组件的版本
- `pd`：PD 组件的版本
- `tidb_dashboard`：独立部署的 TiDB Dashboard 组件的版本
- `cdc`：CDC 组件的版本
- `kvcdc`：TiKV-CDC 组件的版本
- `tiproxy`：TiProxy 组件的版本
- `prometheus`：Prometheus 组件的版本
- `grafana`：Grafana 组件的版本
- `alertmanager`：Alertmanager 组件的版本
- `tso`：TSO 组件的版本
- `scheduling`：Scheduling 组件的版本

`component_versions` 配置示例：

```yaml
component_versions:
  kvcdc: "v1.1.1"
```

上述配置指定了 TiKV-CDC 的版本号为 v1.1.1。

### `pd_servers`

`pd_servers` 指定了将 PD 的服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`pd_servers` 是一个数组，每个数组的元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `listen_host`：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 `0.0.0.0`
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `name`：指定该 PD 实例的名字，不同实例的名字必须唯一，否则无法部署
- `client_port`：指定 PD 的客户端连接端口，默认值：2379
- `peer_port`：指定 PD 之间互相通信的端口，默认值：2380
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)。在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 `pd` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `pd` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制。如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `listen_host`
- `name`
- `client_port`
- `peer_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`pd_servers` 配置示例：

```yaml
pd_servers:
  - host: 10.0.1.11
    config:
      schedule.max-merge-region-size: 20
      schedule.max-merge-region-keys: 200000
  - host: 10.0.1.12
```

上述配置指定了将 PD 部署到 `10.0.1.11` 和 `10.0.1.12`，并针对 `10.0.1.11` 的 PD 进行一些特殊配置。

### `tidb_servers`

`tidb_servers` 指定了将 TiDB 服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`tidb_servers` 是一个数组，每个数组的元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `listen_host`：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 `0.0.0.0`
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `port`：TiDB 服务的监听端口，用于提供给 MySQL 客户端连接，默认值：4000
- `status_port`：TiDB 状态服务的监听端口，用于外部通过 http 请求查看 TiDB 服务的状态，默认值：10080
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 `tidb` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `tidb` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：host 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `listen_host`
- `port`
- `status_port`
- `deploy_dir`
- `log_dir`
- `arch`
- `os`

`tidb_servers` 配置示例：

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### `tikv_servers`

`tikv_servers` 约定了将 TiKV 服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`tikv_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `listen_host`：当机器上有多个 IP 时，可以指定服务的监听 IP，默认为 `0.0.0.0`
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `port`：TiKV 服务的监听端口，默认值：20160
- `status_port`：TiKV 状态服务的监听端口，默认值：20180
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：该字段配置规则和 server_configs 里的 tikv 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `tikv` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：host 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：host 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `listen_host`
- `port`
- `status_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`tikv_servers` 配置示例：

```yaml
tikv_servers:
  - host: 10.0.1.14
    config:
      server.labels: { zone: "zone1", host: "host1" }
  - host: 10.0.1.15
    config:
      server.labels: { zone: "zone1", host: "host2" }
```

### `tiflash_servers`

`tiflash_servers` 约定了将 TiFlash 服务部署到哪些机器上，同时可以指定每台机器上的服务配置。该区块是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 global 区块中的 `ssh_port`
- `tcp_port`：TiFlash TCP 服务的端口，用于执行内部测试，默认 9000。自 TiUP v1.12.5 起，如果部署的集群版本 >= v7.1.0，则该配置项不生效
- `flash_service_port`：TiFlash 提供服务的端口，TiDB 通过该端口从 TiFlash 读数据，默认 3930
- `metrics_port`：TiFlash 的状态端口，用于输出 metric 数据，默认 8234
- `flash_proxy_port`：内置 TiKV 的端口，默认 20170
- `flash_proxy_status_port`：内置 TiKV 的状态端口，默认为 20292
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成，TiFlash 的数据目录支持多个，采用逗号分割
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `tmp_path`：TiFlash 临时文件的存放路径，默认使用 [`path` 或者 `storage.latest.dir` 的第一个目录] + "/tmp"
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 `tiflash` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `tiflash` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `learner_config`：每个 TiFlash 中内置了一个特殊的 TiKV 模块，该配置项用于配置这个特殊的 TiKV 模块，一般不建议修改这个配置项下的内容
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

以上字段中，`data_dir` 在部署完成之后只能新增目录，而下列字段部署完成之后不能再修改：

- `host`
- `tcp_port`
- `flash_service_port`
- `flash_proxy_port`
- `flash_proxy_status_port`
- `metrics_port`
- `deploy_dir`
- `log_dir`
- `tmp_path`
- `arch`
- `os`

`tiflash_servers` 配置示例：

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### `tiproxy_servers`

`tiproxy_servers` 约定了将 TiProxy 服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`tiproxy_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略。
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`。
- `port`：TiProxy SQL 服务的监听端口，默认值：`6000`。
- `status_port`：TiProxy 状态服务的监听端口，用于外部通过 HTTP 请求查看 TiProxy 服务的状态，默认值：`3080`。
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成。
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 `"0,1"`。
- `config`：该字段配置规则和 `server_configs` 里的 `tiproxy` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `tiproxy` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器。
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`。
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`。

在上述字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `arch`
- `os`

`tiproxy_servers` 配置示例：

```yaml
tiproxy_servers:
  - host: 10.0.1.21
    port: 6000
    status_port: 3080
    config:
      labels: { zone: "zone1" }
  - host: 10.0.1.22
    port: 6000
    status_port: 3080
    config:
      labels: { zone: "zone2" }
```

关于更多配置示例，请参见 [TiProxy 部署拓扑](/tiproxy/tiproxy-deployment-topology.md)。

### `kvcdc_servers`

`kvcdc_servers` 约定了将 [TiKV-CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/) 服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`kvcdc_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定 TiKV-CDC 部署到哪台机器，字段值填 IP 地址，不可省略。
- `ssh_port`：指定连接目标机器进行操作时使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`。
- `port`：TiKV-CDC 服务的监听端口，默认 8600。
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成。
- `data-dir`：可选项，指定 TiKV-CDC 存储临时文件的目录，主要用于排序。建议确保该目录所在磁盘的可用空间大于等于 500 GiB。
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成。
- `gc-ttl`：可选项，TiKV-CDC 在 PD 设置服务级别 GC safepoint 的 TTL (Time to Live) 时长。同时也是 TiKV-CDC 同步任务暂停的最大时长。单位为秒，默认值为 `86400`，即 24 小时。注意：TiKV-CDC 同步任务的暂停会影响集群 GC safepoint 的推进。`gc-ttl` 越大，同步任务可以暂停的时间越长，但同时会保留更多的过期数据，并占用更多的存储空间。反之亦然。
- `tz`：TiKV-CDC 服务使用的时区。TiKV-CDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：可选项，指定 TiKV-CDC 使用的配置文件路径。
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`。
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`。
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`。

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`kvcdc_servers` 配置示例：

```yaml
kvcdc_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### `cdc_servers`

`cdc_servers` 约定了将 TiCDC 服务部署到哪些机器上，同时可以指定每台机器上的服务配置，`cdc_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `port`：TiCDC 服务的监听端口，默认 8300
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录。若不指定该字段或指定为相对目录，数据目录则按照 `global` 中配置的 `data_dir` 生成。
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `gc-ttl`：TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 86400，即 24 小时
- `tz`：TiCDC 服务使用的时区。TiCDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 `cdc` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`
- `ticdc_cluster_id`：指定该服务器对应的 TiCDC 集群 ID。若不指定该字段，则自动加入默认 TiCDC 集群。该配置只在 v6.3.0 及以上 TiDB 版本中才生效。

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`
- `ticdc_cluster_id`

`cdc_servers` 配置示例：

```yaml
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

### `tso_servers`

`tso_servers` 约定了将 `tso` 微服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`tso_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略。
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`。
- `port`：`tso` 微服务的监听端口，默认值：`3379`。
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成。
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成。
- `config`：该字段配置规则和 `server_configs` 里的 `tso` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `tso` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器。
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`。
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`。

在上述字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `arch`
- `os`

`tso_servers` 配置示例：

```yaml
tso_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### `scheduling_servers`

`scheduling_servers` 约定了将 `scheduling` 微服务部署到哪些机器上，同时可以指定每台机器上的服务配置。`scheduling_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略。
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`。
- `port`：`scheduling` 微服务的监听端口，默认值：`3379`。
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成。
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成。
- `config`：该字段配置规则和 `server_configs` 里的 `scheduling` 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 `scheduling` 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器。
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`。
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`。

在上述字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `arch`
- `os`

`scheduling_servers` 配置示例：

```yaml
scheduling_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### `monitoring_servers`

`monitoring_servers` 约定了将 Prometheus 服务部署到哪台机器上，同时可以指定这台机器上的服务配置，`monitoring_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，必填项
- `ng_port`：指定 NgMonitoring 组件监听的端口，在 TiUP v1.7.0 引入，用于支持 TiDB Dashboard 中[持续性能分析](/dashboard/continuous-profiling.md)和 [Top SQL](/dashboard/top-sql.md) 功能。默认值：12020
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 global 区块中的 `ssh_port`
- `port`：指定 Prometheus 提供服务的端口，默认值：9090
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `storage_retention`：Prometheus 监控数据保留时间，默认 "30d"
- `rule_dir`：该字段指定一个本地目录，该目录中应当含有完整的 `*.rules.yml` 文件，这些文件会在集群配置初始化阶段被传输到目标机器上，作为 Prometheus 的规则
- `remote_config`：用于支持将 Prometheus 数据写到远端，或从远端读取数据，该字段下有两个配置：
    - `remote_write`：参考 Prometheus [`<remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write) 文档
    - `remote_read`：参考 Prometheus [`<remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read) 文档
- `external_alertmanagers`：若配置了 `external_alertmanagers`，Prometheus 会将配置行为报警通知到集群外的 Alertmanager。该字段为一个数组，数组的元素为每个外部的 Alertmanager，由 `host` 和 `web_port` 字段构成
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`
- `additional_args`：从 TiUP v1.15.0 开始引入，用于配置 Prometheus 额外运行参数。该字段是一个数组，数组元素为 Prometheus 运行参数。例如，要开启 Prometheus 热加载功能，可以将该字段配置为 `--web.enable-lifecycle`
- `additional_scrape_conf`：自定义 Prometheus scrape 配置。在集群进行 deploy/scale-out/scale-in/reload 操作时，TiUP 会将 `additional_scrape_conf` 字段的内容添加到 Prometheus 配置文件的对应参数中。更多信息，请参考[自定义监控组件的配置](/tiup/customized-montior-in-tiup-environment.md#自定义-prometheus-scrape-配置)

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`monitoring_servers` 配置示例：

```yaml
monitoring_servers:
  - host: 10.0.1.11
    rule_dir: /local/rule/dir
    additional_args:
    - --web.enable-lifecycle
    remote_config:
      remote_write:
      - queue_config:
          batch_send_deadline: 5m
          capacity: 100000
          max_samples_per_send: 10000
          max_shards: 300
        url: http://127.0.0.1:8003/write
      remote_read:
      - url: http://127.0.0.1:8003/read
    external_alertmanagers:
    - host: 10.1.1.1
      web_port: 9093
    - host: 10.1.1.2
      web_port: 9094
```

### `grafana_servers`

`grafana_servers` 约定了将 Grafana 服务部署到哪台机器上，同时可以指定这台机器上的服务配置，`grafana_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `port`：指定 Grafana 提供服务的端口，默认值：3000
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `username`：Grafana 登录界面的用户名
- `password`：Grafana 对应的密码
- `dashboard_dir`：该字段指定一个本地目录，该目录中应当含有完整的 `dashboard(*.json)` 文件，这些文件会在集群配置初始化阶段被传输到目标机器上，作为 Grafana 的 dashboards
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`
- `config`：该字段用于添加 Grafana 自定义配置。在集群进行 deploy/scale-out/scale-in/reload 等操作时，TiUP 会将 `config` 字段的内容添加到 Grafana 的配置文件 `grafana.ini` 中。更多信息，请参考[自定义 Grafana 其他配置](/tiup/customized-montior-in-tiup-environment.md#自定义-grafana-其他配置)

> **注意：**
>
> 如果配置了 `grafana_servers` 的 `dashboard_dir` 字段，在执行 `tiup cluster rename` 命令进行集群重命名后，需要完成以下操作：
>
> 1. 对于本地的 dashboards 目录中的 `*.json` 文件，将 `datasource` 字段的值更新为新的集群名（这是因为 `datasource` 是以集群名命名的）
> 2. 执行 `tiup cluster reload -R grafana` 命令

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `port`
- `deploy_dir`
- `arch`
- `os`

`grafana_servers` 配置示例：

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### `alertmanager_servers`

`alertmanager_servers` 约定了将 Alertmanager 服务部署到哪些机器上，同时可以指定这台机器上的服务配置，`alertmanager_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `web_port`：指定 Alertmanager 提供网页服务的端口，默认值：9093
- `cluster_port`：指定 Alertmanger 和其他 Alertmanager 通讯的端口，默认值：9094
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点的 ID，例如 "0,1"
- `config_file`：该字段指定一个本地文件，该文件会在集群配置初始化阶段被传输到目标机器上，作为 Alertmanager 的配置
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`
- `listen_host`：指定监听地址，从而可以通过代理访问 Alertmanager。推荐使用 `0.0.0.0`。更多信息，请参考[自定义 Alertmanager 配置](/tiup/customized-montior-in-tiup-environment.md#自定义-alertmanager-配置)

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `web_port`
- `cluster_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`alertmanager_servers` 配置示例：

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
