---
title: 通过 TiUP 部署 DM 集群的拓扑文件配置
---

# 通过 TiUP 部署 DM 集群的拓扑文件配置

在部署或扩容 TiDB Data Migration (DM) 集群时，需要提供一份拓扑文件来描述集群拓扑，同样，修改配置也是通过编辑拓扑文件来实现的，区别在于修改配置时仅允许修改部分字段。

拓扑文件[示例参考](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)。

## 文件结构

一个 DM 集群的拓扑文件可能包含以下区块：

- [global](/tiup/tiup-dm-topology-reference.md#global)：集群全局配置，其中一些是集群的默认值，可以在实例里面单独配置
- [server_configs](/tiup/tiup-dm-topology-reference.md#server_configs)：组件全局配置，可单独针对每个组件配置，若在实例中存在同名配置项，那么以实例中配置的为准
- [master_servers](/tiup/tiup-dm-topology-reference.md#master_servers)：DM master 实例的配置，用来指定 DM 组件的 master 服务部署到哪些机器上
- [worker_servers](/tiup/tiup-dm-topology-reference.md#worker_servers)：DM worker 实例的配置，用来指定 DM 组件的 worker 服务部署到哪些机器上
- [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers)：用来指定 Prometheus 部署在哪机器上，TiUP 支持部署多台 Prometheus 实例，但真实投入使用的只有第一个
- [grafana_servers](/tiup/tiup-cluster-topology-reference.md#grafana_servers)：Grafana 实例的配置，用来指定 Grafana 部署在哪台机器上
- [alertmanager_servers](/tiup/tiup-cluster-topology-reference.md#alertmanager_servers)：Alertemanager 实例的配置，用来指定 Alertmanager 部署在哪些机器上

### `global`

`global` 区块为集群的全局配置，包含以下字段：

- `user`：以什么用户来启动部署的集群，默认值："tidb"，如果 `<user>` 字段指定的用户在目标机器上不存在，会自动尝试创建
- `group`：自动创建用户时指定用户所属的用户组，默认和 `<user>` 字段值相同，若指定的组不存在，则自动创建
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，默认值：22
- `deploy_dir`：每个组件的部署目录，默认值："deploy"，其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `deploy_dir`，那么实际部署目录为该实例设定的 `deploy_dir`
    - 对于每个实例，如果用户未配置 `deploy_dir`，其默认值为相对路径 `<component-name>-<component-port>`
    - 如果 `global.deploy_dir` 为绝对路径，那么组件会部署到 `<global.deploy_dir>/<instance.deploy_dir>` 目录
    - 如果 `global.deploy_dir` 为相对路径，那么组件会部署到 `/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>` 目录
- `data_dir`：数据目录, 默认值："data"，其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `data_dir`，那么实际数据目录为该实例设定的 `data_dir`
    - 对于每个实例，如果用户未配置 `data_dir`，其默认值为 `<global.data_dir>`
    - 如果 `data_dir` 为相对路径，那么组件数据将放到 `<deploy_dir>/<data_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
- `log_dir`：数据目录, 默认值："log"，其应用规则如下：
    - 如果在实例级别配置了绝对路径的 `log_dir`，那么实际日志目录为该实例设定的 `log_dir`
    - 对于每个实例，如果用户未配置 `log_dir`，其默认值为 `<global.log_dir>`
    - 如果 `log_dir` 为相对路径，那么组件日志将放到 `<deploy_dir>/<log_dir>` 中，其中 `<deploy_dir>` 的计算规则请参考 `deploy_dir` 字段的应用规则
- `os`：目标机器的操作系统，该字段决定了向目标机器推送适配哪个操作系统的组件，默认值：linux
- `arch`：目标机器的 CPU 架构，该字段决定了向目标机器推送哪个平台的二进制包，支持 amd64 和 arm64，默认值：amd64
- `resource_control`：运行时资源控制，该字段下所有配置都将写入 systemd 的 service 文件中，默认不限制，支持控制的资源：
    - `memory_limit`: 限制运行时最大内存，例如 "2G" 表示最多使用 2GB 内存
    - `cpu_quota`：限制运行时最大 CPU 占用率，例如 "200%"
    - `io_read_bandwidth_max`：读磁盘 IO 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
    - `io_write_bandwidth_max`：写磁盘 IO 的最大带宽，例如："/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"
    - `limit_core`：控制 core dump 大小

`global` 配置示例：

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上述配置指定使用 `tidb` 用户启动集群，同时限制每个组件运行时最多只能使用 2GB 内存。

### `server_configs`

`server_configs` 用于配置服务，生成各组件的配置文件，类似 `global` 区块，该区块内的配置可以在具体的实例中被覆盖。主要包含以下字段：

- `master`：DM master 服务的相关配置，支持的完整配置请参考[DM-master 配置文件介绍](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-master-configuration-file)
- `worker`：DM worker 服务的相关配置，支持的完整配置请参考[DM-worker 配置文件介绍](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-worker-configuration-file)

`server_configs` 配置示例：

```yaml
server_configs:
  master:
    log-level: info
    rpc-timeout: "30s"
    rpc-rate-limit: 10.0
    rpc-rate-burst: 40
  worker:
    log-level: info
```

## `master_servers`

`master_servers` 约定了将 DM 组件的 master 节点部署到哪些机器上，同时可以指定每台机器上的服务配置，`master_servers` 是一个数组，每个数组的元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `name`：指定该 DM master 实例的名字，不同实例的名字必须唯一，否则无法部署
- `port`：指定 DM master 提供给服务的端口，默认 8261
- `peer_port`：指定 DM master 之间互相通信的端口，默认值：8291
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点 ID，比如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 master 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 master 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`
- v1_source_path：从 v1.0.x 升级时，可指定该目录，该目录中应当存放有 V1 的源的配置文件

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `name`
- `port`
- `peer_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`
- `v1_source_path`

`master_servers` 配置示例：

```yaml
master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    peer_port: 8291
    deploy_dir: "/dm-deploy/dm-master-8261"
    data_dir: "/dm-data/dm-master-8261"
    log_dir: "/dm-deploy/dm-master-8261/log"
    numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      rpc-timeout: "30s"
      rpc-rate-limit: 10.0
      rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
  - host: 10.0.1.19
    name: master3
```

## `worker_servers`

`worker_servers` 约定了将 DM 组件的 worker 节点部署到哪些机器上，同时可以指定每台机器上的服务配置，`worker_servers` 是一个数组，每个数组的元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `name`：指定该 DM worker 实例的名字，不同实例的名字必须唯一，否则无法部署
- `port`：指定 DM worker 提供给服务的端口，默认 8262
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点 ID，比如 "0,1"
- `config`：该字段配置规则和 `server_configs` 里的 worker 配置规则相同，若配置了该字段，会将该字段内容和 `server_configs` 里的 worker 内容合并（若字段重叠，以本字段内容为准），然后生成配置文件并下发到 `host` 指定的机器
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

以上所有字段中，部分字段部署完成之后不能再修改。如下所示：

- `host`
- `name`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

`worker_servers` 配置示例：

```yaml
worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    deploy_dir: "/dm-deploy/dm-worker-8262"
    log_dir: "/dm-deploy/dm-worker-8262/log"
    numa_node: "0,1"
    # config is used to overwrite the `server_configs.worker` values
    config:
      log-level: info
  - host: 10.0.1.19
```

### `monitoring_servers`

`monitoring_servers` 约定了将 Prometheus 服务部署到哪台机器上，同时可以指定这台机器上的服务配置，`monitoring_servers` 是一个数组，每个数组元素包含以下字段：

- `host`：指定部署到哪台机器，字段值填 IP 地址，不可省略
- `ssh_port`：指定连接目标机器进行操作的时候使用的 SSH 端口，若不指定，则使用 `global` 区块中的 `ssh_port`
- `port`：指定 Prometheus 提供服务的端口，默认值：9090
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点 ID，比如 "0,1"
- `storage_retention`：Prometheus 监控数据保留时间，默认 "15d"
- `rule_dir`：该字段指定一个本地目录，该目录中应当含有完整的 `*.rules.yml` 文件，这些文件会在集群配置初始化阶段被传输到目标机器上，作为 Prometheus 的规则
- `remote_config`：用于支持将 Prometheus 数据写到远端，或从远端读取数据，该字段下有两个配置：
    - `remote_write`：参考 Prometheus [`<remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write) 文档
    - `remote_read`：参考 Prometheus [`<remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read) 文档
- `external_alertmanagers`：若配置了 `external_alertmanagers`，Prometheus 会将配置行为报警通知到集群外的 Alertmanager。该字段为一个数组，数组的元素为每个外部的 Alertmanager，由 `host` 和 `web_port` 字段构成
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

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
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global`中的 `resource_control`

> **注意：**
>
> 如果配置了 `grafana_servers` 的 `dashboard_dir` 字段，在执行 `tiup cluster rename` 命令进行集群重命名后，需要完成以下操作：
>
> 1. 在本地的 dashboards 目录中，将 datasource 字段的值更新为新的集群名（datasource 是以集群名命名的）
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
- `cluster_port`：指定 Alertmanger 和 其他 Alertmanager 通讯的端口，默认值：9094
- `deploy_dir`：指定部署目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `deploy_dir` 生成
- `data_dir`：指定数据目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `data_dir` 生成
- `log_dir`：指定日志目录，若不指定，或指定为相对目录，则按照 `global` 中配置的 `log_dir` 生成
- `numa_node`：为该实例分配 NUMA 策略，如果指定了该参数，需要确保目标机装了 [numactl](https://linux.die.net/man/8/numactl)，在指定该参数的情况下会通过 [numactl](https://linux.die.net/man/8/numactl) 分配 cpubind 和 membind 策略。该字段参数为 string 类型，字段值填 NUMA 节点 ID，比如 "0,1"
- `config_file`：该字段指定一个本地文件，该文件会在集群配置初始化阶段被传输到目标机器上，作为 Alertmanager 的配置
- `os`：`host` 字段所指定的机器的操作系统，若不指定该字段，则默认为 `global` 中的 `os`
- `arch`：`host` 字段所指定的机器的架构，若不指定该字段，则默认为 `global` 中的 `arch`
- `resource_control`：针对该服务的资源控制，如果配置了该字段，会将该字段和 `global` 中的 `resource_control` 内容合并（若字段重叠，以本字段内容为准），然后生成 systemd 配置文件并下发到 `host` 指定机器。`resource_control` 的配置规则同 `global` 中的 `resource_control`

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
