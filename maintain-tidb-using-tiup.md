---
title: TiUP 常见运维操作
---

# TiUP 常见运维操作

本文介绍了使用 TiUP 运维 TiDB 集群的常见操作，包括查看集群列表、启动集群、查看集群状态、修改配置参数、关闭集群、销毁集群等。

## 查看集群列表

TiUP cluster 组件可以用来管理多个 TiDB 集群，在每个 TiDB 集群部署完毕后，该集群会出现在 TiUP 的集群列表里，可以使用 list 命令来查看。

{{< copyable "shell-regular" >}}

```bash
tiup cluster list
```

## 启动集群

启动集群操作会按 PD -> TiKV -> Pump -> TiDB -> TiFlash -> Drainer 的顺序启动整个 TiDB 集群所有组件（同时也会启动监控组件）：

{{< copyable "shell-regular" >}}

```bash
tiup cluster start ${cluster-name}
```

> **注意：**
>
> 你需要将 `${cluster-name}` 替换成实际的集群名字，若忘记集群名字，可通过 `tiup cluster list` 查看。

该命令支持通过 `-R` 和 `-N` 参数来只启动部分组件。

例如，下列命令只启动 PD 组件：

{{< copyable "shell-regular" >}}

```bash
tiup cluster start ${cluster-name} -R pd
```

下列命令只启动 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 PD 组件：

{{< copyable "shell-regular" >}}

```bash
tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
```

> **注意：**
>
> 若通过 `-R` 和 `-N` 启动指定组件，需要保证启动顺序正确（例如需要先启动 PD 才能启动 TiKV），否则可能导致启动失败。

## 查看集群状态

集群启动之后需要检查每个组件的运行状态，以确保每个组件工作正常。TiUP 提供了 display 命令，节省了登陆到每台机器上去查看进程的时间。

{{< copyable "shell-regular" >}}

```bash
tiup cluster display ${cluster-name}
```

## 修改配置参数

集群运行过程中，如果需要调整某个组件的参数，可以使用 `edit-config` 命令来编辑参数。具体的操作步骤如下：

1. 以编辑模式打开该集群的配置文件：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2. 设置参数：

    首先确定配置的生效范围，有以下两种生效范围：

    - 如果配置的生效范围为该组件全局，则配置到 `server_configs`。例如：

        ```
        server_configs:
          tidb:
            log.slow-threshold: 300
        ```

    - 如果配置的生效范围为某个节点，则配置到具体节点的 `config` 中。例如：

        ```
        tidb_servers:
        - host: 10.0.1.11
            port: 4000
            config:
                log.slow-threshold: 300
        ```

    参数的格式参考 [TiUP 配置参数模版](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml)。

    **配置项层次结构使用 `.` 表示**。

    关于组件的更多配置参数说明，可参考 [tidb `config.toml.example`](https://github.com/pingcap/tidb/blob/release-5.0/config/config.toml.example)、[tikv `config.toml.example`](https://github.com/tikv/tikv/blob/release-5.0/etc/config-template.toml) 和 [pd `config.toml.example`](https://github.com/tikv/pd/blob/release-5.0/conf/config.toml)。

3. 执行 `reload` 命令滚动分发配置、重启相应组件：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### 示例

如果要调整 tidb-server 中事务大小限制参数 `txn-total-size-limit` 为 `1G`，该参数位于 [performance](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 模块下，调整后的配置如下：

```
server_configs:
  tidb:
    performance.txn-total-size-limit: 1073741824
```

然后执行 `tiup cluster reload ${cluster-name} -R tidb` 命令滚动重启。

## Hotfix 版本替换

常规的升级集群请参考[升级文档](/upgrade-tidb-using-tiup.md)，但是在某些场景下（例如 Debug），可能需要用一个临时的包替换正在运行的组件，此时可以用 `patch` 命令：

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

例如，有一个 TiDB 实例的 hotfix 包放在 `/tmp/tidb-hotfix.tar.gz` 目录下。如果此时想要替换集群上的所有 TiDB 实例，则可以执行以下命令：

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

或者只替换其中一个 TiDB 实例：

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## 重命名集群

部署并启动集群后，可以通过 `tiup cluster rename` 命令来对集群重命名：

{{< copyable "shell-regular" >}}

```bash
tiup cluster rename ${cluster-name} ${new-name}
```

> **注意：**
>
> + 重命名集群会重启监控（Prometheus 和 Grafana）。
> + 重命名集群之后 Grafana 可能会残留一些旧集群名的面板，需要手动删除这些面板。

## 关闭集群

关闭集群操作会按 Drainer -> TiFlash -> TiDB -> Pump -> TiKV -> PD 的顺序关闭整个 TiDB 集群所有组件（同时也会关闭监控组件）：

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop ${cluster-name}
```

和 `start` 命令类似，`stop` 命令也支持通过 `-R` 和 `-N` 参数来只停止部分组件。

例如，下列命令只停止 TiDB 组件：

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop ${cluster-name} -R tidb
```

下列命令只停止 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 TiDB 组件：

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
```

## 清除集群数据

此操作会关闭所有服务，并清空其数据目录或/和日志目录，并且无法恢复，需要**谨慎操作**。

清空集群所有服务的数据，但保留日志：

{{< copyable "shell-regular" >}}

```bash
tiup cluster clean ${cluster-name} --data
```

清空集群所有服务的日志，但保留数据：

```bash
tiup cluster clean ${cluster-name} --log
```

清空集群所有服务的数据和日志：

{{< copyable "shell-regular" >}}

```bash
tiup cluster clean ${cluster-name} --all
```

清空 Prometheus 以外的所有服务的日志和数据：

{{< copyable "shell-regular" >}}

```bash
tiup cluster clean ${cluster-name} --all --ignore-role prometheus
```

清空节点 `172.16.13.11:9000` 以外的所有服务的日志和数据：

{{< copyable "shell-regular" >}}

```bash
tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.11:9000
```

清空部署在 `172.16.13.12` 以外的所有服务的日志和数据：

{{< copyable "shell-regular" >}}

```bash
tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.12
```

## 销毁集群

销毁集群操作会关闭服务，清空数据目录和部署目录，并且无法恢复，需要**谨慎操作**。

{{< copyable "shell-regular" >}}

```bash
tiup cluster destroy ${cluster-name}
```
