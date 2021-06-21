---
title: 使用 TiUP 升级 TiDB
aliases: ['/docs-cn/dev/upgrade-tidb-using-tiup/','/docs-cn/dev/how-to/upgrade/using-tiup/','/docs-cn/dev/upgrade-tidb-using-tiup-offline/', '/zh/tidb/dev/upgrade-tidb-using-tiup-offline']
---

# 使用 TiUP 升级 TiDB

本文档适用于以下升级路径：
- 使用 TiUP 从 TiDB 4.0 版本升级至 TiDB 5.1 及后续修订版本。
- 使用 TiUP 从 TiDB 5.0 版本升级至 TiDB 5.1 及后续修订版本。

>  **注意：**
>
>  如果原集群是 3.0 或 3.1 或更老的版本，不支持直接升级到 5.1 及后续修订版本。你需要先从老版本升级到 4.0 后，再从 4.0 升级到 5.1 及后续修订版本。

## 1. 升级兼容性说明

- TiDB 目前暂不支持版本降级或升级后回退。
- 使用 TiDB Ansible 管理的 4.0 版本集群，需要先按照 [4.0 版本文档的说明](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-tiup)将集群导入到 TiUP (`tiup cluster`) 管理后，再按本文档说明升级到 5.1 版本及后续修订版本。
- 若要将 3.0 之前的版本升级至 5.1 版本：
    1. 首先[通过 TiDB Ansible 升级到 3.0 版本](https://docs.pingcap.com/zh/tidb/v3.0/upgrade-tidb-using-ansible)。
    2. 然后按照 [4.0 版本文档的说明](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-tiup)，使用 TiUP (`tiup cluster`) 将 TiDB Ansible 配置导入。
    3. 将集群升级至 4.0 版本。
    4. 按本文档说明将集群升级到 5.1 版本。
- 支持 TiDB Binlog，TiCDC，TiFlash 等组件版本的升级。
- 具体不同版本的兼容性说明，请查看各个版本的 [Release Note](/release-notes.md)。请根据各个版本的 Release Note 的兼容性更改调整集群的配置。

> **注意：**
>
> 在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

## 2. 升级前准备

本部分介绍实际开始升级前需要进行的更新 TiUP 和 TiUP Cluster 组件版本等准备工作。

### 2.1 升级 TiUP 或更新 TiUP 离线镜像

#### 升级 TiUP 和 TiUP Cluster

> **注意：**
>
> 如果原集群中控机不能访问 `https://tiup-mirrors.pingcap.com` 地址，可跳到步骤 2.2 使用离线升级方式。

1. 先升级 TiUP 版本（建议 `tiup` 版本不低于 `1.5.0`）：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self
    tiup --version
    ```

2. 再升级 TiUP Cluster 版本（建议 `tiup cluster` 版本不低于 `1.5.0`）：

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

覆盖升级完成后，执行下列命令升级 Cluster 组件：

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

此时离线镜像已经更新成功。如果覆盖后发现 TiUP 运行报错，可能是 manifest 未更新导致，可尝试 `rm -rf ~/.tiup/manifests/*` 后再使用。

### 2.2 编辑 TiUP Cluster 拓扑配置文件

> **注意：**
>
> 以下情况可跳过此步骤：
>
> - 原集群没有修改过配置参数，或通过 tiup cluster 修改过参数但不需要调整。
> - 升级后对未修改过的配置项希望使用 `5.1` 默认参数。

1. 进入拓扑文件的 `vi` 编辑模式：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. 参考 [topology](https://github.com/pingcap/tiup/blob/release-1.4/embed/templates/examples/topology.example.yaml) 配置模板的格式，将希望修改的参数填到拓扑文件的 `server_configs` 下面。

修改完成后 `:wq` 保存并退出编辑模式，输入 `Y` 确认变更。

> **注意：**
>
> 升级到 5.1 版本前，请确认已在 4.0 修改的参数在 5.1 版本中是兼容的，可参考 [TiKV 配置文件描述](/tikv-configuration-file.md)。
> 
> 以下 TiKV 参数在 TiDB v5.1 已废弃。如果在原集群配置过以下参数，需要通过 `edit-config` 编辑模式删除这些参数:
> 
> - pessimistic-txn.enabled
> - server.request-batch-enable-cross-command
> - server.request-batch-wait-duration

### 2.3 检查当前集群的健康状况

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

以升级到 5.1.0 版本为例：

{{< copyable "shell-regular" >}}

```
tiup cluster upgrade <cluster-name> v5.1.0
```

> **注意：**
>
> - 滚动升级会逐个升级所有的组件。升级 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟（300 秒），超时后会直接停止该实例。
> - 如果不希望驱逐 leader，而希望快速升级集群至新版本，可以在上述命令中指定 `--force`，该方式会造成性能抖动，不会造成数据损失。
> - 如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 `--transfer-timeout` 为一个更大的值，如 `--transfer-timeout 3600`，单位为秒。

#### 停机升级

在停机升级前，首先需要将整个集群关停。

{{< copyable "shell-regular" >}}

```shell
tiup cluster stop <cluster-name>
```

之后通过 `upgrade` 命令添加 `--offline` 参数来进行停机升级。

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
Cluster version:    v5.1.0
```

> **注意：**
>
> TiUP 及 TiDB 默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。

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

### 4.2 升级过程中 evict leader 等待时间过长，如何跳过该步骤快速升级

可以指定 `--force`，升级时会跳过 `PD transfer leader` 和 `TiKV evict leader` 过程，直接重启并升级版本，对线上运行的集群性能影响较大。命令如下：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### 4.3 升级完成后，如何更新 pd-ctl 等周边工具版本

可通过 TiUP 安装对应版本的 `ctl` 组件来更新相关工具版本：

{{< copyable "" >}}

```
tiup install ctl:v5.1.0
```

## 5. TiDB 5.1 兼容性变化

- 兼容性变化请参考 5.1 Release Notes。
- 请避免在对使用 TiDB-Binlog 的集群进行滚动升级过程中新创建聚簇索引表。
