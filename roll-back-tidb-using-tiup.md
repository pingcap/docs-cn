---
title: 使用 TiUP 回退 TiDB 的版本
summary: TiUP 可用于回退 TiDB 版本。本文档介绍如何使用 TiUP 回退到某个版本。
---

# 使用 TiUP 回退 TiDB 的版本

本文档介绍如何使用 TiUP 将 TiDB 回退到之前的某个版本。

## 支持回退的版本

本文档适用于以下回退路径：

- 从 v7.5.Y 版本回退至 v7.5.X，其中 Y > 0, X ≥ 0, 且 Y > X。

> **警告：**
>
> 其他补丁版本的回退未经验证，如直接回退，可能会产生非预期的问题。

## 注意事项

回退版本时，请注意以下事项：

- 对于无法进行连接重试的客户端，版本回退会导致连接到被关闭的 TiDB 节点的数据库的连接失效，造成部分业务请求失败。对于这类业务，推荐在客户端添加重试功能，或者在低峰期进行 TiDB 的滚动更新操作。
- 在回退 TiDB 集群的过程中，请勿执行 DDL 语句，否则可能会出现行为未定义的问题。
- 回退的集群内的各组件应该使用相同版本。 
- Changefeed 默认配置值在回退过程中不会被更改，已经修改的值，在回退过程中也不会被修改。

## 回退前的准备工作

开始回退前需要[更新 TiUP 和 TiUP 集群组件版本](/tiup/tiup-component-management.md#升级组件)。

### 兼容性变更

- TiDB 目前仅支持有限的补丁版本回退。请参见[支持回退的版本](#支持回退的版本)。
- 仅支持 PD、TiDB、TiKV、TiFlash、TiCDC、BR、PITR 这些组件的补丁版本回退。
- 查看对应版本的 [Release Notes](/releases/release-notes.md) 中的兼容性变更。如果有任何变更影响到回退，请采取相应的措施。例如，从 TiDB v7.5.2 回退至 v7.5.1 时，需查阅以下各版本的兼容性变更：

    - [TiDB v7.5.1 Release Notes](/releases/release-7.5.1.md#兼容性变更) 中的兼容性变更
    - [TiDB v7.5.2 Release Notes](/releases/release-7.5.2.md#兼容性变更) 中的兼容性变更

### 检查当前集群的 DDL

集群中有 DDL 语句正在被执行时，请勿进行版本回退操作。被执行的 DDL 语句通常为 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和列类型变更等耗时较久的 DDL 语句。

在回退前，为避免回退过程中出现未定义行为或其他故障，建议执行下列操作：

1. 使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令查看集群中是否有正在进行的 DDL Job。

2. 如需回退，请等待 DDL 执行完成，或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消该 DDL Job。

### 检查当前集群的健康状况

为避免回退过程中出现未定义行为或其他故障，建议在回退前对使用 `check` 子命令检查集群的 Region 健康状态。

```shell
tiup cluster check <cluster-name> --cluster
```

执行结束后，会输出 `region status` 检查结果。

- 如果结果为 `All regions are healthy`，则说明当前集群中所有 Region 均为健康状态，可以继续执行回退。
- 如果结果为 `Regions are not fully healthy: m miss-peer, n pending-peer`，并提示 `Please fix unhealthy regions before other operations.`，则说明当前集群中有 Region 处在异常状态。此时应先排除相应异常状态，并再次检查结果为 `All regions are healthy` 后再继续回退。

### 修改配置项 `server-version`

- 配置项 [`server-version`](/tidb-configuration-file.md#server-version) 的值会被 TiDB 节点用于验证当前 TiDB 的版本。因此在进行 TiDB 集群回退前，请将 `server-version` 的值设置为空或者当前 TiDB 真实的版本值，避免出现非预期行为。

### 修改配置项 `performance.force-init-stats`

配置项 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 设置为 `true` 会延长 TiDB 的启动时间，这可能会造成启动超时，回退失败。为避免这种情况，建议为 TiUP 设置更长的等待超时。

可能受影响的场景：

- 原集群版本低于 v6.5.7、v7.1.0（尚未支持 `performance.force-init-stats`），目标版本为 v7.2.0 或更高。
- 原集群版本高于或等于 v6.5.7、v7.1.0，且配置项 `performance.force-init-stats` 被设置为 `true`。

设置 TiUP 的等待超时的步骤如下：

1. 查看配置项 `performance.force-init-stats` 的值。通常情况下，`20` 分钟超时等待能满足绝大部分场景的需求。如果需要更准确的预估，可以在 TiDB 日志中搜索 `init stats info time` 关键字，获取上次启动的统计信息加载时间作为参考。
 
2. 通过增加命令行选项 [`--wait-timeout`](/tiup/tiup-component-dm.md#--wait-timeoutuint默认-120) 设置 TiUP 超时等待时间。如下命令可将超时等待设置为 `1200` 秒（即 `20` 分钟）:
 
    ```shell
    tiup update cluster --wait-timeout 1200 [other options]
    ```

## 执行回退操作

回退补丁版本仅支持不停机回退，回退过程中集群仍然可以对外提供服务。

回退时，TiDB 会对各节点逐个迁移 leader 后再回退和重启。对于大规模集群需要较长时间才能完成整个回退操作，因此请提前预估预留足够的时间。

以 v7.5.1 回退到 v7.5.0 版本为例，执行下列命令：

```shell
tiup ctl:v7.5.0 pd config set cluster-version "v7.5.0" -u \"pd-1-peer:2379\"
tiup cluster patch {cluster_name} {/tmp/cdc-v7.5.0-linux-amd64.tar.gz} -R cdc -y
tiup cluster patch {cluster_name} {/tmp/tidb-v7.5.0-linux-amd64.tar.gz} -R tidb -y
tiup cluster patch {cluster_name} {/tmp/tikv-v7.5.0-linux-amd64.tar.gz} -R tikv -y
tiup cluster patch {cluster_name} {/tmp/pd-v7.5.0-linux-amd64.tar.gz} -R pd -y
tiup cluster patch {cluster_name} {/tmp/tiflash-v7.5.0-linux-amd64.tar.gz} -R tiflash -y
```

> **注意：**
>
> - 必须按上面命令行的顺序执行回退操作。
> - 滚动回退会逐个回退所有的组件。回退 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟（300 秒），超时后会直接停止该实例。
> - 使用 [`--force`](/tiup//tiup-component-cluster-upgrade.md#--force) 参数可以在不驱逐 leader 的前提下快速回退集群至指定版本，但是该方式会忽略所有回退中的错误，在回退失败后得不到有效提示，请谨慎使用。

如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 [`--transfer-timeout`](/tiup/tiup-component-cluster-reload.md#--transfer-timeoutuint默认-600) 为一个更大的值，如 `--transfer-timeout 3600`，单位为秒。

## 验证回退结果

执行 `display` 命令来查看最新的集群版本 TiDB 版本：

```shell
tiup cluster display <cluster-name>
```

输出结果如下，版本成功回退到 v7.5.0：

```shell
Cluster type:       tidb
Cluster name:       <cluster-name>
Cluster version:    v7.5.0
```
