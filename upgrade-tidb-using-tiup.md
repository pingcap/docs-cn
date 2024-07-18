---
title: 使用 TiUP 升级 TiDB
summary: TiUP 可用于 TiDB 升级。升级过程中需注意不支持 TiFlash 组件从 5.3 之前的老版本在线升级至 5.3 及之后的版本，只能采用停机升级。在升级过程中，不要执行 DDL 语句，避免出现行为未定义的问题。升级前需查看集群中是否有正在进行的 DDL Job，并等待其完成或取消后再进行升级。升级完成后，可使用 TiUP 安装对应版本的 `ctl` 组件来更新相关工具版本。
---

# 使用 TiUP 升级 TiDB

本文档适用于以下升级路径：

- 使用 TiUP 从 TiDB 4.0 版本升级至 TiDB 8.2。
- 使用 TiUP 从 TiDB 5.0-5.4 版本升级至 TiDB 8.2。
- 使用 TiUP 从 TiDB 6.0-6.6 版本升级至 TiDB 8.2。
- 使用 TiUP 从 TiDB 7.0-7.6 版本升级至 TiDB 8.2。
- 使用 TiUP 从 TiDB 8.0-8.1 版本升级至 TiDB 8.2。

> **警告：**
>
> 1. 不支持将 TiFlash 组件从 5.3 之前的老版本在线升级至 5.3 及之后的版本，只能采用停机升级。如果集群中其他组件（如 tidb，tikv）不能停机升级，参考[不停机升级](#不停机升级)中的注意事项。
> 2. 在升级 TiDB 集群的过程中，**请勿执行** DDL 语句，否则可能会出现行为未定义的问题。
> 3. 集群中有 DDL 语句正在被执行时（通常为 `ADD INDEX` 和列类型变更等耗时较久的 DDL 语句），**请勿进行**升级操作。在升级前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令查看集群中是否有正在进行的 DDL Job。如需升级，请等待 DDL 执行完成或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消该 DDL Job 后再进行升级。
>
> 从 TiDB v7.1 版本升级至更高的版本时，可以不遵循上面的限制 2 和 3，建议参考[平滑升级 TiDB 的限制](/smooth-upgrade-tidb.md#使用限制)。

> **注意：**
>
> - 如果原集群是 3.0 或 3.1 或更早的版本，不支持直接升级到 v8.2.0 及后续修订版本。你需要先从早期版本升级到 4.0 后，再从 4.0 升级到 v8.2.0 及后续修订版本。
> - 如果原集群是 6.2 之前的版本，升级到 6.2 及以上版本时，部分场景会遇到升级卡住的情况，你可以参考[如何解决升级卡住的问题](#42-升级到-v620-及以上版本时如何解决升级卡住的问题)。
> - 配置参数 [`server-version`](/tidb-configuration-file.md#server-version) 的值会被 TiDB 节点用于验证当前 TiDB 的版本。因此在进行 TiDB 集群升级前，请将 `server-version` 的值设置为空或者当前 TiDB 真实的版本值，避免出现非预期行为。
> - 配置项 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 设置为 `ON` 会延长 TiDB 的启动时间，这可能会造成启动超时，升级失败。为避免这种情况，建议为 TiUP 设置更长的等待超时。
>     - 可能受影响的场景：
>         - 原集群版本低于 v6.5.7、v7.1.0（尚未支持 `performance.force-init-stats`），目标版本为 v7.2.0 及更高。
>         - 原集群版本高于或等于 v6.5.7、v7.1.0，且配置项 `performance.force-init-stats` 被设置为 `ON`。 
>     - 查看配置项 `performance.force-init-stats` 的值：
>
>         ```
>         SHOW CONFIG WHERE type = 'tidb' AND name = 'performance.force-init-stats';
>         ```
>
>     - 通过增加命令行选项 [`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeoutuint默认-120) 可以延长 TiUP 超时等待。如下命令可将超时等待设置为 1200 秒（即 20 分钟）。
>
>         ```shell
>         tiup update cluster --wait-timeout 1200 [other options]
>         ```
>
>         通常情况下，20 分钟超时等待能满足绝大部分场景的需求。如果需要更准确的预估，可以在 TiDB 日志中搜索 `init stats info time` 关键字，获取上次启动的统计信息加载时间作为参考。例如：
>
>         ```
>         [domain.go:2271] ["init stats info time"] [lite=true] ["take time"=2.151333ms]
>         ```
>
>          如果原集群是 v7.1.0 或更早的版本，升级到 v7.2.0 或以上版本时，由于 [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 的引入，统计信息加载时间会大幅减少。这个情况下，升级前的 `init stats info time` 会比升级后加载所需的时间偏长。
>     - 如果想要缩短 TiDB 滚动升级的时间，并且在升级过程中能够承受初始统计信息缺失带来的潜在性能影响，可以在升级前[用 TiUP 修改目标实例的配置](/maintain-tidb-using-tiup.md#修改配置参数)，将 `performance.force-init-stats` 设置为 `OFF`。升级完成后可酌情改回。

升级过程中还有一些[用户操作限制](/smooth-upgrade-tidb.md#用户操作限制)，强烈建议在升级之前先阅读相关内容。

## 1. 升级兼容性说明

- TiDB 目前暂不支持版本降级或升级后回退。
- 使用 TiDB Ansible 管理的 4.0 版本集群，需要先按照 [4.0 版本文档的说明](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-tiup)将集群导入到 TiUP (`tiup cluster`) 管理后，再按本文档说明升级到 v8.2.0 版本。
- 若要将 v3.0 之前的版本升级至 v8.2.0 版本：
    1. 首先[通过 TiDB Ansible 升级到 3.0 版本](https://docs.pingcap.com/zh/tidb/v3.0/upgrade-tidb-using-ansible)。
    2. 然后按照 [4.0 版本文档的说明](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-tiup)，使用 TiUP (`tiup cluster`) 将 TiDB Ansible 配置导入。
    3. 将集群升级至 v4.0 版本。
    4. 按本文档说明将集群升级到 v8.2.0 版本。
- 支持 TiDB Binlog，TiCDC，TiFlash 等组件版本的升级。
- 将 v6.3.0 之前的 TiFlash 升级至 v6.3.0 及之后的版本时，需要特别注意：在 Linux AMD64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 AVX2 指令集。而在 Linux ARM64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 ARMv8 架构。具体请参考 [6.3.0 版本 Release Notes](/releases/release-6.3.0.md#其他) 中的描述。
- 具体不同版本的兼容性说明，请查看各个版本的 [Release Note](/releases/release-notes.md)。请根据各个版本的 Release Note 的兼容性更改调整集群的配置。
- 升级 v5.3 之前版本的集群到 v5.3 及后续版本时，TiUP 默认部署的 Prometheus 生成的 Alert 存在时间格式变化。该格式变化是从 Prometheus v2.27.1 开始引入的，详情见 [Prometheus commit](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)。

## 2. 升级前准备

本部分介绍实际开始升级前需要进行的更新 TiUP 和 TiUP Cluster 组件版本等准备工作。

### 2.1 查阅兼容性变更

查阅 TiDB v8.2.0 release notes 中的[兼容性变更](/releases/release-8.2.0.md#兼容性变更)。如果有任何变更影响到了你的升级，请采取相应的措施。

### 2.2 升级 TiUP 或更新 TiUP 离线镜像

#### 升级 TiUP 和 TiUP Cluster

> **注意：**
>
> 如果原集群中控机不能访问 `https://tiup-mirrors.pingcap.com` 地址，可跳过本步骤，然后[更新 TiUP 离线镜像](#更新-tiup-离线镜像)。

1. 先升级 TiUP 版本（建议 `tiup` 版本不低于 `1.11.3`）：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self
    tiup --version
    ```

2. 再升级 TiUP Cluster 版本（建议 `tiup cluster` 版本不低于 `1.11.3`）：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### 更新 TiUP 离线镜像

> **注意：**
>
> 如果原集群不是通过离线部署方式部署的，可忽略此步骤。

可以参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)的步骤下载部署新版本的 TiUP 离线镜像，上传到中控机。在执行 `local_install.sh` 后，TiUP 会完成覆盖升级。

{{< copyable "shell-regular" >}}

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

> **建议：**
>
> 关于 `TiDB-community-server` 软件包和 `TiDB-community-toolkit` 软件包的内容物，请查阅 [TiDB 离线包](/binary-package.md)。

覆盖升级完成后，需将 server 和 toolkit 两个离线镜像合并，执行以下命令合并离线组件到 server 目录下。

{{< copyable "shell-regular" >}}

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

离线镜像合并后，执行下列命令升级 Cluster 组件：

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

此时离线镜像已经更新成功。如果覆盖后发现 TiUP 运行报错，可能是 manifest 未更新导致，可尝试 `rm -rf ~/.tiup/manifests/*` 后再使用。

### 2.3 编辑 TiUP Cluster 拓扑配置文件

> **注意：**
>
> 以下情况可跳过此步骤：
>
> - 原集群没有修改过配置参数，或通过 tiup cluster 修改过参数但不需要调整。
> - 升级后对未修改过的配置项希望使用 `8.2.0` 默认参数。

1. 进入拓扑文件的 `vi` 编辑模式：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. 参考 [topology](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) 配置模板的格式，将希望修改的参数填到拓扑文件的 `server_configs` 下面。

修改完成后 `:wq` 保存并退出编辑模式，输入 `Y` 确认变更。

> **注意：**
>
> 升级到 v8.2.0 版本前，请确认已在 4.0 修改的参数在 v8.2.0 版本中是兼容的，可参考 [TiKV 配置文件描述](/tikv-configuration-file.md)。

### 2.4 检查当前集群的 DDL 和 Backup 情况

为避免升级过程中出现未定义行为或其他故障，建议检查以下指标后再进行升级操作。

- 集群 DDL 情况：建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令查看集群中是否有正在进行的 DDL Job。如需升级，请等待 DDL 执行完成或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消该 DDL Job 后再进行升级。
- 集群 Backup 情况：建议使用 [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md) 命令查看集群中是否有正在进行的 Backup 或者 Restore 任务。如需升级，请等待 Backup 执行完成后，得到一个有效的备份后再执行升级。

### 2.5 检查当前集群的健康状况

为避免升级过程中出现未定义行为或其他故障，建议在升级前对集群当前的 region 健康状态进行检查，此操作可通过 `check` 子命令完成。

{{< copyable "shell-regular" >}}

```shell
tiup cluster check <cluster-name> --cluster
```

执行结束后，最后会输出 region status 检查结果。如果结果为 "All regions are healthy"，则说明当前集群中所有 region 均为健康状态，可以继续执行升级；如果结果为 "Regions are not fully healthy: m miss-peer, n pending-peer" 并提示 "Please fix unhealthy regions before other operations."，则说明当前集群中有 region 处在异常状态，应先排除相应异常状态，并再次检查结果为 "All regions are healthy" 后再继续升级。

## 3. 升级 TiDB 集群

本部分介绍如何滚动升级 TiDB 集群以及如何进行升级后的验证。

### 3.1 将集群升级到指定版本

升级的方式有两种：不停机升级和停机升级。TiUP Cluster 默认的升级 TiDB 集群的方式是不停机升级，即升级过程中集群仍然可以对外提供服务。升级时会对各节点逐个迁移 leader 后再升级和重启，因此对于大规模集群需要较长时间才能完成整个升级操作。如果业务有维护窗口可供数据库停机维护，则可以使用停机升级的方式快速进行升级操作。

#### 不停机升级

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

以升级到 v8.2.0 版本为例：

{{< copyable "shell-regular" >}}

```
tiup cluster upgrade <cluster-name> v8.2.0
```

> **注意：**
>
> - 滚动升级会逐个升级所有的组件。升级 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟（300 秒），超时后会直接停止该实例。
> - 使用 `--force` 参数可以在不驱逐 leader 的前提下快速升级集群至新版本，但是该方式会忽略所有升级中的错误，在升级失败后得不到有效提示，请谨慎使用。
> - 如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 `--transfer-timeout` 为一个更大的值，如 `--transfer-timeout 3600`，单位为秒。
> - 如需将 TiFlash 从 v5.3.0 之前的版本升级到 v5.3.0 及之后的版本，必须进行 TiFlash 的停机升级，且 TiUP 版本小于 v1.12.0。具体升级步骤，请参考[使用 TiUP 升级](/tiflash-upgrade-guide.md#使用-tiup-升级)。
> - 在对使用 TiDB Binlog 的集群进行滚动升级过程中，请避免新创建聚簇索引表。

#### 升级时指定组件版本

从 tiup-cluster v1.14.0 开始，支持在升级集群的时候指定其中某些组件到特定版本。指定的组件在后续升级中保持固定版本，除非重新指定版本。

> **注意：**
>
> 对于 TiDB、TiKV、PD、TiCDC 等共用版本号的组件，尚未有完整的测试保证它们在跨版本混合部署的场景下能正常工作。请仅在测试场景或在[获取支持](/support.md)的情况下使用此配置。

```shell
tiup cluster upgrade -h | grep "version"
      --alertmanager-version string        Fix the version of alertmanager and no longer follows the cluster version.
      --blackbox-exporter-version string   Fix the version of blackbox-exporter and no longer follows the cluster version.
      --cdc-version string                 Fix the version of cdc and no longer follows the cluster version.
      --ignore-version-check               Ignore checking if target version is bigger than current version.
      --node-exporter-version string       Fix the version of node-exporter and no longer follows the cluster version.
      --pd-version string                  Fix the version of pd and no longer follows the cluster version.
      --tidb-dashboard-version string      Fix the version of tidb-dashboard and no longer follows the cluster version.
      --tiflash-version string             Fix the version of tiflash and no longer follows the cluster version.
      --tikv-cdc-version string            Fix the version of tikv-cdc and no longer follows the cluster version.
      --tikv-version string                Fix the version of tikv and no longer follows the cluster version.
      --tiproxy-version string             Fix the version of tiproxy and no longer follows the cluster version.
```

#### 停机升级

在停机升级前，首先需要将整个集群关停。

{{< copyable "shell-regular" >}}

```shell
tiup cluster stop <cluster-name>
```

之后通过 `upgrade` 命令添加 `--offline` 参数来进行停机升级，其中 `<cluster-name>` 为集群名，`<version>` 为升级的目标版本，例如 `v8.2.0`。

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --offline
```

升级完成后集群不会自动启动，需要使用 `start` 命令来启动集群。

{{< copyable "shell-regular" >}}

```shell
tiup cluster start <cluster-name>
```

### 3.2 升级后验证

执行 `display` 命令来查看最新的集群版本 `TiDB Version`：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Cluster type:       tidb
Cluster name:       <cluster-name>
Cluster version:    v8.2.0
```

## 4. 升级 FAQ

本部分介绍使用 TiUP 升级 TiDB 集群遇到的常见问题。

### 4.1 升级时报错中断，处理完报错后，如何继续升级

重新执行 `tiup cluster upgrade` 命令进行升级，升级操作会重启之前已经升级完成的节点。如果不希望重启已经升级过的节点，可以使用 `replay` 子命令来重试操作，具体方法如下：

1. 使用 `tiup cluster audit` 命令查看操作记录：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster audit
    ```

    在其中找到失败的升级操作记录，并记下该操作记录的 ID，下一步中将使用 `<audit-id>` 表示操作记录 ID 的值。

2. 使用 `tiup cluster replay <audit-id>` 命令重试对应操作：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster replay <audit-id>
    ```

### 4.2 升级到 v6.2.0 及以上版本时，如何解决升级卡住的问题

从 v6.2.0 开始，TiDB 默认开启[并发 DDL 框架](/ddl-introduction.md#tidb-在线-ddl-异步变更的原理)执行并发 DDL。该框架改变了 DDL 作业存储方式，由 KV 队列变为表队列。这一变化可能会导致部分升级场景卡住。下面是一些会触发该问题的场景及解决方案：

- 加载插件导致的卡住

    升级过程中加载部分插件时需要执行 DDL 语句，此时会卡住升级。

    **解决方案**：升级过程中避免加载插件。待升级完成后再执行插件加载。

- 使用 `kill -9` 命令停机升级导致的卡住

    - 预防措施：避免使用 `kill -9` 命令停机升级。如需使用，应在 2 分钟后再启动新版本 TiDB 节点。
    - 如果升级已经被卡住：重启受影响的 TiDB 节点。如果问题刚发生，建议等待 2 分钟后再重启。

- DDL Owner 变更导致的卡住

    在多 TiDB 实例场景升级时，网络或机器故障可能引起 DDL Owner 变更。如果此时存在未完成的升级阶段 DDL 语句，升级可能会卡住。

    **解决方案**：

    1. 先 Kill 卡住的 TiDB 节点（避免使用 `kill -9`）。
    2. 重新启动新版本 TiDB 节点。

### 4.3 升级过程中 evict leader 等待时间过长，如何跳过该步骤快速升级

可以指定 `--force`，升级时会跳过 `PD transfer leader` 和 `TiKV evict leader` 过程，直接重启并升级版本，对线上运行的集群性能影响较大。命令如下，其中 `<version>` 为升级的目标版本，例如 `v8.2.0`：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### 4.4 升级完成后，如何更新 pd-ctl 等周边工具版本

可通过 TiUP 安装对应版本的 `ctl` 组件来更新相关工具版本：

{{< copyable "" >}}

```
tiup install ctl:v8.2.0
```
