---
title: 使用 TiUP 部署运维 TiDB 线上集群
---

# 使用 TiUP 部署运维 TiDB 线上集群

本文重在介绍如何使用 TiUP 的 cluster 组件，如果需要线上部署的完整步骤，可参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

与 playground 组件用于部署本地测试集群类似，cluster 组件用于快速部署生产集群。对比 playground，cluster 组件提供了更强大的生产集群管理功能，包括对集群的升级、缩容、扩容甚至操作、审计等。

cluster 组件的帮助文档如下：

```bash
tiup cluster
```

```
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.3.0/cluster
Deploy a TiDB cluster for production

Usage:
  tiup cluster [flags]
  tiup [command]

Available Commands:
  deploy      部署集群
  start       启动已部署的集群
  stop        停止集群
  restart     重启集群
  scale-in    集群缩容
  scale-out   集群扩容
  clean       清理数据
  destroy     销毁集群
  upgrade     升级集群
  exec        在集群的一个或多个机器上执行命令
  display     获取集群信息
  list        获取集群列表
  audit       查看集群操作日志
  import      导入一个由 TiDB Ansible 部署的集群
  edit-config 编辑 TiDB 集群的配置
  reload      用于必要时重载集群配置
  patch       使用临时的组件包替换集群上已部署的组件
  help        打印 Help 信息

Flags:
  -h, --help              帮助信息
      --native-ssh        使用系统默认的 SSH 客户端
      --wait-timeout int  等待操作超时的时间
      --ssh-timeout int   SSH 连接超时时间
  -y, --yes               跳过所有的确认步骤
```

## 部署集群

部署集群的命令为 `tiup cluster deploy`，一般用法为：

```bash
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

该命令需要提供集群的名字、集群使用的 TiDB 版本，以及一个集群的拓扑文件。

拓扑文件的编写可参考[示例](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml)。以一个最简单的拓扑为例，将下列文件保存为 `/tmp/topology.yaml`：

> **注意：**
>
> TiUP Cluster 组件的部署和扩容拓扑是使用 [yaml](https://yaml.org/spec/1.2/spec.html) 语法编写，所以需要注意缩进。

```yaml
---

pd_servers:
  - host: 172.16.5.134
    name: pd-134
  - host: 172.16.5.139
    name: pd-139
  - host: 172.16.5.140
    name: pd-140

tidb_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

tikv_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

TiUP 默认部署在 amd64 架构上运行的 binary，若目标机器为 arm64 架构，可以在拓扑文件中进行配置：

```yaml
global:
  arch: "arm64"           # 让所有机器默认使用 arm64 的 binary

tidb_servers:
  - host: 172.16.5.134
    arch: "amd64"         # 这台机器会使用 amd64 的 binary
  - host: 172.16.5.139
    arch: "arm64"         # 这台机器会使用 arm64 的 binary
  - host: 172.16.5.140    # 没有配置 arch 字段的机器，会使用 global 中的默认值，这个例子中是 arm64

...
```

假如我们想要使用 TiDB 的 v3.0.12 版本，集群名字为 `prod-cluster`，则执行以下命令：

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy -p prod-cluster v3.0.12 /tmp/topology.yaml
```

执行过程中会再次确认拓扑结构并提示输入目标机器上的 root 密码（-p 表示使用密码）：

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
Type        Host          Ports        Directories
----        ----          -----        -----------
pd          172.16.5.134  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380    deploy/pd-2379,data/pd-2379
tikv        172.16.5.134  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.139  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.140  20160/20180  deploy/tikv-20160,data/tikv-20160
tidb        172.16.5.134  4000/10080   deploy/tidb-4000
tidb        172.16.5.139  4000/10080   deploy/tidb-4000
tidb        172.16.5.140  4000/10080   deploy/tidb-4000
prometheus  172.16.5.134  9090         deploy/prometheus-9090,data/prometheus-9090
grafana     172.16.5.134  3000         deploy/grafana-3000
Attention:
    1. If the topology is not what you expected, check your yaml file.
    1. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:
```

输入密码后 tiup-cluster 便会下载需要的组件并部署到对应的机器上，当看到以下提示时说明部署成功：

```bash
Deployed cluster `prod-cluster` successfully
```

## 查看集群列表

集群部署成功后，可以通过 `tiup cluster list` 命令在集群列表中查看该集群：

{{< copyable "shell-root" >}}

```bash
tiup cluster list
```

```
Starting /root/.tiup/components/cluster/v1.3.0/cluster list
Name          User  Version    Path                                               PrivateKey
----          ----  -------    ----                                               ----------
prod-cluster  tidb  v3.0.12    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa
```

## 启动集群

集群部署成功后，可以执行以下命令启动该集群。如果忘记了部署的集群的名字，可以使用 `tiup cluster list` 命令查看。

{{< copyable "shell-regular" >}}

```shell
tiup cluster start prod-cluster
```

## 检查集群状态

如果想查看集群中每个组件的运行状态，逐一登录到各个机器上查看显然很低效。因此，TiUP 提供了 `tiup cluster display` 命令，用法如下：

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v1.3.0/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
```

Status 列用 `Up` 或者 `Down` 表示该服务是否正常。对于 PD 组件，同时可能会带有 `|L` 表示该 PD 是 Leader，`|UI` 表示该 PD 运行着 [TiDB Dashboard](/dashboard/dashboard-intro.md)。

## 缩容节点

> **注意：**
>
> 本节只展示缩容命令的语法示例，线上扩缩容具体步骤可参考[使用 TiUP 扩容缩容 TiDB 集群](/scale-tidb-using-tiup.md)。

缩容即下线服务，最终会将指定的节点从集群中移除，并删除遗留的相关文件。

由于 TiKV 和 TiDB Binlog 组件的下线是异步的（需要先通过 API 执行移除操作）并且下线过程耗时较长（需要持续观察节点是否已经下线成功），所以对 TiKV 和 TiDB Binlog 组件做了特殊处理：

- 对 TiKV 及 Binlog 组件的操作
    - TiUP cluster 通过 API 将其下线后直接退出而不等待下线完成
    - 等之后再执行集群操作相关的命令时，会检查是否存在已经下线完成的 TiKV 或者 Binlog 节点。如果不存在，则继续执行指定的操作；如果存在，则执行如下操作：
        1. 停止已经下线掉的节点的服务
        2. 清理已经下线掉的节点的相关数据文件
        3. 更新集群的拓扑，移除已经下线掉的节点
- 对其他组件的操作
    - 下线 PD 组件时，会通过 API 将指定节点从集群中删除掉（这个过程很快），然后停掉指定 PD 的服务并且清除该节点的相关数据文件
    - 下线其他组件时，直接停止并且清除节点的相关数据文件

缩容命令的基本用法：

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

它需要指定至少两个参数，一个是集群名字，另一个是节点 ID。节点 ID 可以参考上一节使用 `tiup cluster display` 命令获取。

比如想缩容 172.16.5.140 上的 TiKV 节点，可以执行：

{{< copyable "shell-regular" >}}

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

通过 `tiup cluster display` 可以看到该 TiKV 已经被标记为 `Offline`：

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v1.3.0/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Offline    data/tikv-20160       deploy/tikv-20160
```

待 PD 将其数据调度到其他 TiKV 后，该节点会被自动删除。

## 扩容节点

> **注意：**
>
> 本节只用于展示扩容命令的语法示例，线上扩缩容可参考[使用 TiUP 扩容缩容 TiDB 集群](/scale-tidb-using-tiup.md)。

扩容的内部逻辑与部署类似，TiUP cluster 组件会先保证节点的 SSH 连接，在目标节点上创建必要的目录，然后执行部署并且启动服务。其中 PD 节点的扩容会通过 join 方式加入到集群中，并且会更新与 PD 有关联的服务的配置；其他服务直接启动加入到集群中。所有服务在扩容时都会做正确性验证，最终返回是否扩容成功。

例如，在集群 `tidb-test` 中扩容一个 TiKV 节点和一个 PD 节点：

1. 新建 scale.yaml 文件，添加新增的 TiKV 和 PD 节点 IP：

    > **注意：**
    >
    > 需要新建一个拓扑文件，文件中只写入扩容节点的描述信息，不要包含已存在的节点。

    ```yaml
    ---

    pd_servers:
      - host: 172.16.5.140

    tikv_servers:
      - host: 172.16.5.140
    ```

2. 执行扩容操作。TiUP cluster 根据 scale.yaml 文件中声明的端口、目录等信息在集群中添加相应的节点：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    执行完成之后可以通过 `tiup cluster display tidb-test` 命令检查扩容后的集群状态。

## 滚动升级

> **注意：**
>
> 本节只用于展示命令的语法示例，线上升级请参考[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md)。

滚动升级功能借助 TiDB 的分布式能力，升级过程中尽量保证对前端业务透明、无感知。升级时会先检查各个组件的配置文件是否合理，如果配置有问题，则报错退出；如果配置没有问题，则工具会逐个节点进行升级。其中对不同节点有不同的操作。

### 不同节点的操作

- 升级 PD 节点
    - 优先升级非 Leader 节点
    - 所有非 Leader 节点升级完成后再升级 Leader 节点
        - 工具会向 PD 发送一条命令将 Leader 迁移到升级完成的节点上
        - 当 Leader 已经切换到其他节点之后，再对旧的 Leader 节点做升级操作
    - 同时升级过程中，若发现有不健康的节点，工具会中止本次升级并退出，此时需要由人工判断、修复后再执行升级。
- 升级 TiKV 节点
    - 先在 PD 中添加一个迁移对应 TiKV 上 Region leader 的调度，通过迁移 Leader 确保升级过程中不影响前端业务
    - 等待迁移 Leader 完成之后，再对该 TiKV 节点进行升级更新
    - 等更新后的 TiKV 正常启动之后再移除迁移 Leader 的调度
- 升级其他服务
    - 正常停止服务再更新

### 升级操作

升级命令参数如下：

```bash
Usage:
  tiup cluster upgrade <cluster-name> <version> [flags]

Flags:
      --force                  在不 transfer leader 的情况下强制升级（危险操作）
  -h, --help                   帮助手册
      --transfer-timeout int   transfer leader 的超时时间

Global Flags:
      --native-ssh        使用系统默认的 SSH 客户端
      --wait-timeout int  等待操作超时的时间
      --ssh-timeout int   SSH 连接的超时时间
  -y, --yes               跳过所有的确认步骤
```

例如，把集群升级到 v5.0.0 的命令为：

{{< copyable "shell-regular" >}}

```bash
tiup cluster upgrade tidb-test v5.0.0
```

## 更新配置

如果想要动态更新组件的配置，TiUP cluster 组件为每个集群保存了一份当前的配置，如果想要编辑这份配置，则执行 `tiup cluster edit-config <cluster-name>` 命令。例如：

{{< copyable "shell-regular" >}}

```bash
tiup cluster edit-config prod-cluster
```

然后 TiUP cluster 组件会使用 vi 打开配置文件供编辑（如果你想要使用其他编辑器，请使用 `EDITOR` 环境变量自定义编辑器，例如 `export EDITOR=nano`），编辑完之后保存即可。此时的配置并没有应用到集群，如果想要让它生效，还需要执行：

{{< copyable "shell-regular" >}}

```bash
tiup cluster reload prod-cluster
```

该操作会将配置发送到目标机器，重启集群，使配置生效。

> **注意：**
>
> 对于监控组件，可以通过执行 `tiup cluster edit-config` 命令在对应实例上添加自定义配置路径来进行配置自定义，例如：

```yaml
---

grafana_servers:
  - host: 172.16.5.134
    dashboard_dir: /path/to/local/dashboards/dir

monitoring_servers:
  - host: 172.16.5.134
    rule_dir: /path/to/local/rules/dir

alertmanager_servers:
  - host: 172.16.5.134
    config_file: /path/to/local/alertmanager.yml
```

路径内容格式如下：

- `grafana_servers` 的 `dashboard_dir` 字段指定的文件夹中应当含有完整的 `*.json` 文件。
- `monitoring_servers` 的 `rule_dir` 字段定义的文件夹中应当含有完整的 `*.rules.yml` 文件。
- `alertmanager_servers` 的 `config_file` 格式请参考 [Alertmanager 配置模板](https://github.com/pingcap/tiup/blob/master/embed/templates/config/alertmanager.yml)。

在执行 `tiup reload` 时，TiUP 会将中控机上对应的配置上传到目标机器对应的配置目录中，上传之前会删除目标机器中已有的旧配置文件。如果想要修改某一个配置文件，请确保将所有的（包含未修改的）配置文件都放在同一个目录中。例如，要修改 Grafana 的 `tidb.json` 文件，可以先将 Grafana 的 `dashboards` 目录中所有的 `*.json` 文件拷贝到本地目录中，再修改 `tidb.json` 文件。否则最终的目标机器上将缺失其他的 JSON 文件。

> **注意：**
>
> 如果配置了 `grafana_servers` 的 `dashboard_dir` 字段，在执行 `tiup cluster rename` 命令进行集群重命名后，需要完成以下操作：
>
> 1. 在本地的 `dashboards` 目录中，将集群名修改为新的集群名。
> 2. 在本地的 `dashboards` 目录中，将 `datasource` 更新为新的集群名（`datasource` 是以集群名命名的）。
> 3. 执行 `tiup cluster reload -R grafana` 命令。

## 更新组件

常规的升级集群可以使用 upgrade 命令，但是在某些场景下（例如 Debug)，可能需要用一个临时的包替换正在运行的组件，此时可以用 patch 命令：

{{< copyable "shell-root" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  tiup cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   帮助信息
  -N, --node strings           指定被替换的节点
      --overwrite              在未来的 scale-out 操作中使用当前指定的临时包
  -R, --role strings           指定被替换的服务类型
      --transfer-timeout int   transfer leader 的超时时间

Global Flags:
      --native-ssh        使用系统默认的 SSH 客户端
      --wait-timeout int  等待操作超时的时间
      --ssh-timeout int   SSH 连接的超时时间
  -y, --yes               跳过所有的确认步骤
```

例如，有一个 TiDB 的 hotfix 包放在 `/tmp/tidb-hotfix.tar.gz`，如果此时想要替换集群上的所有 TiDB，则可以执行：

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

或者只替换其中一个 TiDB：

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## 导入 TiDB Ansible 集群

> **注意：**
>
> TiUP cluster 组件对 TiSpark 的支持目前为实验性特性，暂不支持导入启用了 TiSpark 组件的集群。

在 TiUP 之前，一般使用 TiDB Ansible 部署 TiDB 集群，import 命令用于将这部分集群过渡给 TiUP 接管。import 命令用法如下：

{{< copyable "shell-root" >}}

```bash
tiup cluster import --help
```

```
Import an exist TiDB cluster from TiDB-Ansible

Usage:
  tiup cluster import [flags]

Flags:
  -d, --dir string         TiDB-Ansible 的目录，默认为当前目录
  -h, --help               import 的帮助信息
      --inventory string   inventory 文件的名字 (默认为 "inventory.ini")
      --no-backup          不备份 Ansible 目录, 用于存在多个 inventory 文件的 Ansible 目录
  -r, --rename NAME        重命名被导入的集群

Global Flags:
      --native-ssh        使用系统默认的 SSH 客户端
      --wait-timeout int  等待操作超时的时间
      --ssh-timeout int   SSH 连接的超时时间
  -y, --yes               跳过所有的确认步骤
```

例如，导入一个 TiDB Ansible 集群：

{{< copyable "shell-regular" >}}

```bash
cd tidb-ansible
tiup cluster import
```

或者

{{< copyable "shell-regular" >}}

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## 查看操作日志

操作日志的查看可以借助 audit 命令，其用法如下：

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

在不使用 `[audit-id]` 参数时，该命令会显示执行的命令列表，如下：

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit
```

```
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.3.0/cluster audit
ID      Time                       Command
--      ----                       -------
4BLhr0  2020-04-29T13:25:09+08:00  /home/tidb/.tiup/components/cluster/v1.3.0/cluster deploy test v5.0.0-rc /tmp/topology.yaml
4BKWjF  2020-04-28T23:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.3.0/cluster deploy test v5.0.0-rc /tmp/topology.yaml
4BKVwH  2020-04-28T23:02:08+08:00  /home/tidb/.tiup/components/cluster/v1.3.0/cluster deploy test v5.0.0-rc /tmp/topology.yaml
4BKKH1  2020-04-28T16:39:04+08:00  /home/tidb/.tiup/components/cluster/v1.3.0/cluster destroy test
4BKKDx  2020-04-28T16:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.3.0/cluster deploy test v5.0.0-rc /tmp/topology.yaml
```

第一列为 audit-id，如果想看某个命令的执行日志，则传入这个 audit-id：

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit 4BLhr0
```

## 在集群节点机器上执行命令

`exec` 命令可以很方便地到集群的机器上执行命令，其使用方式如下：

```bash
Usage:
  tiup cluster exec <cluster-name> [flags]

Flags:
      --command string   需要执行的命令 (默认是 "ls")
  -h, --help             帮助信息
  -N, --node strings     指定要执行的节点 ID （节点 id 通过 display 命令获取）
  -R, --role strings     指定要执行的 role
      --sudo             是否使用 root (默认为 false)
```

例如，如果要到所有的 TiDB 节点上执行 `ls /tmp`：

{{< copyable "shell-regular" >}}

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## 集群控制工具 (controllers)

在 TiUP 之前，我们用 `tidb-ctl`、`tikv-ctl`、`pd-ctl` 等工具操控集群，为了方便下载和使用，TiUP 将它们集成到了统一的组件 `ctl` 中：

```bash
Usage:
  tiup ctl {tidb/pd/tikv/binlog/etcd} [flags]

Flags:
  -h, --help   help for tiup
```

这个命令和之前的命令对应关系为：

```bash
tidb-ctl [args] = tiup ctl tidb [args]
pd-ctl [args] = tiup ctl pd [args]
tikv-ctl [args] = tiup ctl tikv [args]
binlogctl [args] = tiup ctl bindlog [args]
etcdctl [args] = tiup ctl etcd [args]
```

例如，以前查看 store 的命令为 `pd-ctl -u http://127.0.0.1:2379 store`，集成到 TiUP 中的命令为：

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 store
```

## 部署机环境检查

使用 `check` 子命令可以对部署机的环境进行一系列检查，并输出检查结果。通过执行 `check` 子命令，可以发现常见的不合理配置或不支持情况。命令参数列表如下：

```bash
Usage:
  tiup cluster check <topology.yml | cluster-name> [flags]

Flags:
      --apply                  Try to fix failed checks
      --cluster                Check existing cluster, the input is a cluster name.
      --enable-cpu             Enable CPU thread count check
      --enable-disk            Enable disk IO (fio) check
      --enable-mem             Enable memory size check
  -h, --help                   help for check
  -i, --identity_file string   The path of the SSH identity file. If specified, public key authentication will be used.
  -p, --password               Use password of target hosts. If specified, password authentication will be used.
      --user string            The user name to login via SSH. The user must has root (or sudo) privilege.
```

默认情况下，此功能用于在部署前进行环境检查，通过指定 `--cluster` 参数切换模式，也可以用于对已部署集群的部署机进行检查，例如：

```bash
# check deploy servers before deploy
tiup cluster check topology.yml --user tidb -p

# check deploy servers of an existing cluster
tiup cluster check <cluster-name> --cluster
```

其中，CPU 线程数检查、内存大小检查和磁盘性能检查三项默认关闭，对于生产环境，建议将此三项检测开启并确保通过，以获得最佳性能。

- CPU：线程数大于等于 16 为通过检查
- 内存：物理内存总大小大于等于 32 GB 为通过检查
- 磁盘：对 `data_dir` 所在分区执行 `fio` 测试并记录结果

在运行检测时，若指定了 `--apply` 参数，程序将尝试对其中未通过的项目自动修复。自动修复仅限于部分可通过修改配置或系统参数调整的项目，其它未修复的项目需要根据实际情况手工处理。

环境检查不是部署集群的必需流程。对于生产环境建议在部署前执行环境检查并通过所有检测项。如果未通过全部检查项，也可能正常部署和运行集群，但可能无法获得最佳性能表现。

## 使用中控机系统自带的 SSH 客户端连接集群

在以上所有操作中，涉及到对集群机器的操作都是通过 TiUP 内置的 SSH 客户端连接集群执行命令，但是在某些场景下，需要使用系统自带的 SSH 客户端来对集群执行操作，比如：

- 使用 SSH 插件来做认证
- 使用定制的 SSH 客户端

此时可以通过命令行参数 `--native-ssh` 启用系统自带命令行：

- 部署集群: `tiup cluster deploy <cluster-name> <version> <topo> --native-ssh`
- 启动集群: `tiup cluster start <cluster-name> --native-ssh`
- 升级集群: `tiup cluster upgrade ... --native-ssh`

所有涉及集群操作的步骤都可以加上 `--native-ssh` 来使用系统自带的客户端。

也可以使用环境变量 `TIUP_NATIVE_SSH` 来指定是否使用本地 SSH 客户端，避免每个命令都需要添加 `--native-ssh` 参数：

```shell
export TIUP_NATIVE_SSH=true
# 或者
export TIUP_NATIVE_SSh=1
# 或者
export TIUP_NATIVE_SSH=enable
```

若环境变量和 `--native-ssh` 同时指定，则以 `--native-ssh` 为准。

> **注意：**
>
> 在部署集群的步骤中，若需要使用密码的方式连接 (-p)，或者密钥文件设置了 passphrase，则需要保证中控机上安装了 sshpass，否则连接时会报错。

## 迁移中控机与备份

TiUP 相关的数据都存储在用户 home 目录的 `.tiup` 目录下，若要迁移中控机只需要拷贝 `.tiup` 目录到对应目标机器即可。

1. 在原机器 home 目录下执行 `tar czvf tiup.tar.gz .tiup`。
2. 把 `tiup.tar.gz` 拷贝到目标机器 home 目录。
3. 在目标机器 home 目录下执行 `tar xzvf tiup.tar.gz`。
4. 添加 `.tiup` 目录到 `PATH` 环境变量。

    如使用 `bash` 并且是 `tidb` 用户，在 `~/.bashrc` 中添加 `export PATH=/home/tidb/.tiup/bin:$PATH` 后执行 `source ~/.bashrc`，根据使用的 shell 与用户做相应调整。

> **注意：**
>
> 为了避免中控机磁盘损坏等异常情况导致 TiUP 数据丢失，建议定时备份 `.tiup` 目录。
