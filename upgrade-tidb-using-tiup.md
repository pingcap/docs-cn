---
title: 使用 TiUP 升级 TiDB
aliases: ['/docs-cn/stable/upgrade-tidb-using-tiup/','/docs-cn/v4.0/upgrade-tidb-using-tiup/','/docs-cn/stable/how-to/upgrade/using-tiup/','/docs-cn/v4.0/how-to/upgrade/using-tiup/']
---

# 使用 TiUP 升级 TiDB

本文档适用于使用 TiUP 从 TiDB 3.0 或 3.1 版本升级至 TiDB 4.0 版本，以及从 4.0 版本升级至后续版本。

如果原集群使用 TiDB Ansible 部署，TiUP 也支持将 TiDB Ansible 配置导入，并完成升级。

## 1. 升级兼容性说明

- 不支持在升级后回退至 3.0 或更旧版本。
- 3.0 之前的版本，需要先通过 TiDB Ansible 升级到 3.0 版本，然后按照本文档的说明，使用 TiUP 将 TiDB Ansible 配置导入，再升级到 4.0 版本。
- TiDB Ansible 配置导入到 TiUP 中管理后，不能再通过 TiDB Ansible 对集群进行操作，否则可能因元信息不一致造成冲突。
- 对于满足以下情况之一的 TiDB Ansible 部署的集群，暂不支持导入：
    - 启用了 `TLS` 加密功能的集群
    - 纯 KV 集群（没有 TiDB 实例的集群）
    - 启用了 `Kafka` 的集群
    - 启用了 `Spark` 的集群
    - 启用了 `Lightning` / `Importer` 的集群
    - 仍使用老版本 `'push'` 的方式收集监控指标（从 3.0 默认为 `'pull'` 模式，如果没有特意调整过则可以支持）
    - 在 `inventory.ini` 配置文件中单独为机器的 node_exporter / blackbox_exporter 通过 `node_exporter_port` / `blackbox_exporter_port` 设置了非默认端口（在 `group_vars` 目录中统一配置的可以兼容）或者单独为某一台机器的 node_exporter / blackbox_exporter 设置了和其他机器的 node_exporter / blackbox_exporter 不同的 `deploy_dir`
- 如果使用 TiDB Ansible 部署的集群中有部分节点未部署监控，应当先使用 TiDB Ansible 在 `inventory.ini` 文件的 `monitored_servers` 分组中补充对应节点的信息，并通过 `deploy.yaml` playbook 将补充的监控组件部署完整。否则在数据导入 TiUP 后进行其他运维操作时，可能会因监控组件缺失而出错。
- 支持 TiDB Binlog，TiCDC，TiFlash 等组件版本的升级。
- 从 2.0.6 之前的版本升级到 4.0 版本之前，需要确认集群中是否存在正在运行中的 DDL 操作，特别是耗时的 `Add Index` 操作，等 DDL 操作完成后再执行升级操作
- 2.1 及之后版本启用了并行 DDL，早于 2.0.1 版本的集群，无法滚动升级到 4.0 版本，可以选择下面两种方案：
    - 停机升级，直接从早于 2.0.1 的 TiDB 版本升级到 4.0 版本
    - 先滚动升级到 2.0.1 或者之后的 2.0.x 版本，再滚动升级到 4.0 版本

> **注意：**
>
> 在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

## 2. 在中控机器上安装 TiUP

1. 在中控机上执行如下命令安装 TiUP：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 重新声明全局环境变量：

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. 确认 TiUP 工具是否安装：

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

4. 安装 TiUP 的 cluster 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

如果之前安装过 TiUP，使用如下命令更新至最新版本即可：

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

> **注意：**
>
> 如果 `tiup --version` 显示 `tiup` 版本低于 `v1.0.0`，请在执行 `tiup update cluster` 之前先执行 `tiup update --self` 命令更新 `tiup` 版本。

## 3. 将 TiDB Ansible 及 `inventory.ini` 配置导入到 TiUP

> **注意：**
>
> + 目前 TiUP 仅支持 `systemd` 的进程管理模式。如果此前使用 TiDB Ansible 部署时选择了 `supervise`，需要先按[使用 TiDB Ansible 部署 TiDB 集群](/online-deployment-using-ansible.md#如何调整进程监管方式从-supervise-到-systemd)迁移到 `systemd`。
> + 如果原集群已经是 TiUP 部署，可以跳过此步骤。
> + 目前默认识别 `inventory.ini` 配置文件，如果你的配置为其他名称，请指定。
> + 你需要确保当前集群的状态与 `inventory.ini` 中的拓扑一致，并确保集群的组件运行正常，否则导入后会导致集群元信息异常。
> + 如果在一个 TiDB Ansible 目录中管理多个不同的 `inventory.ini` 配置文件和 TiDB 集群，将其中一个集群导入到 TiUP 时，需要指定 `--no-backup` 以避免将 Ansible 目录移动到 TiUP 管理目录下面。

### 3.1 将 TiDB Ansible 集群导入到 TiUP 中

1. 以 `/home/tidb/tidb-ansible` 为示例路径，使用如下命令将 TiDB Ansible 集群导入到 TiUP 中：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible
    ```

2. 执行导入命令后，若集群 `Inventory` 信息解析成功，将出现如下提示：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible/
    ```

    ```
    Found inventory file /home/tidb/tidb-ansible/inventory.ini, parsing...
    Found cluster "ansible-cluster" (v3.0.12), deployed with user tidb.
    Prepared to import TiDB v3.0.12 cluster ansible-cluster.
    Do you want to continue? [y/N]:
    ```

3. 核对解析得到的集群名和版本无误后，输入`y` 确认继续执行。

    + 若 `Inventory` 信息解析出错，导入过程将会终止，终止不会对原 Ansible 部署方式有任何影响，之后需根据错误提示调整并重试。

    + 若 Ansible 中原集群名与 TiUP 中任一已有集群的名称重复，将会给出警示信息并提示输入一个新的集群名。因此，请注意**不要重复对同一个集群执行导入**，导致 TiUP 中同一个集群有多个名字

导入完成后，可以通过 `tiup cluster display <cluster-name>` 查看当前集群状态以验证导入结果。由于 `display` 命令会查询各节点的实时状态，所以命令执行可能需要等待少许时间。

### 3.2 编辑 TiUP 拓扑配置文件

> **注意：**
>
> 以下情况可跳过该步骤：
>
> - 原集群没有修改过配置参数。
> - 升级后希望使用 `4.0` 默认参数。

1. 进入 TiDB Ansible 的备份目录 `~/.tiup/storage/cluster/clusters/{cluster_name}/ansible-imported-configs`，确认配置模板中修改过的参数。

2. 进入拓扑文件的 `vi` 编辑模式：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

3. 参考 [topology](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml) 配置模板的格式，将原集群修改过的参数填到拓扑文件的 `server_configs` 下面。

修改完成后 `wq` 保存并退出编辑模式，输入 `Y` 确认变更。

> **注意：**
>
> 升级到 4.0 版本前，请确认已在 3.0 修改的参数在 4.0 版本中是兼容的，可参考[配置模板](/tikv-configuration-file.md)。
>
> TiUP 版本 <= v1.0.8 可能无法正确获取 TiFlash 的数据目录，需要确认 `data_dir` 与 TiFlash 配置的 `path` 值是否一致。若不一致需要进行如下操作把 TiFlash 的 `data_dir` 改成与 `path` 一致的值：
>
>    1. 执行 `tiup cluster edit-config <cluster-name>` 命令修改配置文件。
>
>    2. 修改对应 TiFlash 的 `data_dir` 配置：
>
>        ```yaml
>          tiflash_servers:
>            - host: 10.0.1.14
>              data_dir: /data/tiflash-11315 # 修改为 TiFlash 配置文件的 `path` 值
>        ```

## 4. 滚动升级 TiDB 集群

本部分介绍如何滚动升级 TiDB 集群以及升级后的验证。

### 4.1 将集群升级到指定版本

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

以升级到 v4.0.0 版本为例：

{{< copyable "shell-regular" >}}

```
tiup cluster upgrade <cluster-name> v4.0.0
```

滚动升级会逐个升级所有的组件。升级 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟，超过后会直接停止实例。

如果不希望驱逐 leader，而希望立刻升级，可以在上述命令中指定 `--force`，该方式会造成性能抖动，不会造成数据损失。

如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 `--transfer-timeout` 为一个超大值，如 `--transfer-timeout 100000000`，单位为 s。

### 4.2 升级后验证

执行 `display` 命令来查看最新的集群版本 `TiDB Version`：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Starting /home/tidblk/.tiup/components/cluster/v1.0.0/cluster display <cluster-name>
TiDB Cluster: <cluster-name>
TiDB Version: v4.0.0
```

> **注意：**
>
> TiUP 及 TiDB（v4.0.2 起）默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。

## 5. 升级 FAQ

本部分介绍使用 TiUP 升级 TiDB 集群遇到的常见问题。

### 5.1 升级时报错中断，处理完报错后，如何继续升级

重新执行 `tiup cluster upgrade` 命令进行升级，升级操作会重启之前已经升级完成的节点。TiDB 4.0 后续版本将支持从中断的位置继续升级。

### 5.2 升级过程中 evict leader 等待时间过长，如何跳过该步骤快速升级

可以指定 `--force`，升级时会跳过 `PD transfer leader` 和 `TiKV evict leader` 过程，直接重启并升级版本，对线上运行的集群影响较大。命令如下：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0 --force
```

### 5.3 升级完成后，如何更新 pd-ctl 等周边工具版本

目前 TiUP 没有对周边工具的版本进行管理更新，如需下载最新版本的工具包，直接下载 TiDB 安装包即可，将 `{version}` 替换为对应的版本如 `v4.0.0`，下载地址如下：

{{< copyable "" >}}

```
https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
```

### 5.4 升级过程中 TiFlash 组件升级失败

TiFlash 在 `v4.0.0-rc.2` 之前的版本可能有一些不兼容的问题。因此，如果将包含 TiFlash 组件的集群由此前版本升级至 `v4.0.0-rc.2` 之后版本的过程中遇到问题，可在 [ASK TUG](https://asktug.com/) 反馈，寻求研发人员支持。

## 6. TiDB 4.0 兼容性变化

- `oom-action` 参数设置为 `cancel` 时，当查询语句触发 OOM 阈值后会被 kill 掉，升级到 4.0 版本后除了 `select` 语句，还可能 kill 掉 `insert`/`update`/`delete` 等 DML 语句。
- 4.0 版本增加了 `rename` 时对表名长度的检查，长度限制为 `64` 个字符。升级后 `rename` 后的表名长度超过这个限制会报错，3.0 及之前的版本则不会报错。
- 4.0 版本增加了对分区表的分区名长度的检查，长度限制为 `64` 个字符。升级后，当你创建和修改分区表时，如果分区名长度超过这个限制会报错，3.0 及之前的版本则不会报错。
- 4.0 版本对 `explain` 执行计划的输出格式做了改进，需要注意是否有针对 `explain` 制订了自动化的分析程序。
- 4.0 版本支持 [Read Committed 隔离级别](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。升级到 4.0 后，在悲观事务里隔离级别设置为 `READ-COMMITTED` 会生效，3.0 及之前的版本则不会生效。
- 4.0 版本执行 `alter reorganize partition` 会报错，之前的版本则不会报错，只是语法上支持没有实际效果。
- 4.0 版本创建 `linear hash partition` 和 `subpartition` 分区表时实际不生效，会转换为普通表，之前的版本则转换为普通分区表。
