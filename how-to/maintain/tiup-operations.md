---
title: TiUP 常见运维操作
category: how-to
---

# TiUP 常见运维操作

## 查看集群列表

一个 TiUP 可以管理多个集群，在集群部署完毕之后它会出现在 TiUP 的集群列表里，可以使用 list 命令来查看。

{{< copyable "shell-regular" >}}

```bash
tiup cluster list
```

## 启动集群

此操作会按 PD -> TiKV -> Pump -> TiDB -> TiFlash -> Drainer 的顺序启动整个 TiDB 集群所有组件（同时也会启动监控组件）。

{{< copyable "shell-regular" >}}

```bash
tiup cluster start ${cluster-name}
```

> 请将 `${cluster-name}` 替换成实际的集群名字，若忘记集群名字，可通过 `tiup cluster list` 查看

该命令支持通过 `-R` 和 `-N` 参数来只启动部分组件，例如下面的命令只启动 pd 组件

```bash
tiup cluster start ${cluster-name} -R pd
```

而下面的命令只启动 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 pd 组件

```bash
tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
```

> **注意：**
>
> 若通过 `-R` 和 `-N` 启动指定组件，需要保证启动顺序正确（例如要先启动 PD 才能启动 TiKV），否则可能启动失败

## 查看集群状态

集群启动之后可能需要检查每个组件的运行状态，以确保每个组件工作正常，TiUP 提供了 display 命令可以免去登陆到每台机器上去查看进程的烦恼。

{{< copyable "shell-regular" >}}

```bash
tiup cluster display ${cluster-name}
```

## 关闭集群

此操作会按 Drainer -> TiFlash -> TiDB -> Pump -> TiKV -> PD 的顺序关闭整个 TiDB 集群所有组件（同时也会关闭监控组件）

{{< copyable "shell-regular" >}}

```bash
tiup cluster stop ${cluster-name}
```

和 `start` 命令类似，`stop` 命令也支持通过 `-R` 和 `-N` 参数来只停止部分组件，例如下面的命令只停止 tidb 组件

```bash
tiup cluster stop ${cluster-name} -R tidb
```

而下面的命令只停止 `1.2.3.4` 和 `1.2.3.5` 这两台机器上的 tidb 组件

```bash
tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
```

## 修改配置参数

运行中的集群，如果需要调整某个组件的参数，可以使用 `edit-config` 指令来编辑参数。具体的操作步骤如下：

1. 以编辑模式打开该集群的配置文件：

```bash
tiup cluster edit-config ${cluster-name}
```

2. 设置参数，涉及到生效范围，和参数说明
- 确定配置的生效范围，有 2 种：
  - 配置的生效范围为该组件全局，请配置到 `server_configs`
    例如：
    ```
    server_configs:
      tidb:
        log.slow-threshold: 300
    ```
  - 配置的生效范围为某个 node，请配置到具体的 node 中
    例如：
    ```
    tidb_servers:
      - host: 10.0.1.11
        port: 4000
          config:
            log.slow-threshold: 300
    ```

  参数的格式请参考 [TiUP 配置参数模版](https://github.com/pingcap-incubator/tiup-cluster/blob/master/topology.example.yaml)
 
  **配置项层次结构请使用'.'表示**

- 组件更多具体的配置参数说明，可以在如下链接中找到：

  [tidb](https://github.com/pingcap/tidb/blob/v4.0.0-rc/config/config.toml.example) 
  
  [tikv](https://github.com/tikv/tikv/blob/v4.0.0-rc/etc/config-template.toml)
  
  [pd](https://github.com/pingcap/pd/blob/v4.0.0-rc/conf/config.toml)

3. 执行 `reload` 滚动分发配置、重启相应组件

```bash
tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
```

### 举例：
调整 tidb-server 中事务大小限制参数 `txn-total-size-limit` 为 1G，该参数位于 [performance](https://github.com/pingcap/tidb/blob/v4.0.0-rc/config/config.toml.example) 模块下，调整后的配置如下：

```
server_configs:
  tidb:
    performance.txn-total-size-limit: 1073741824
```
滚动重启
`tiup cluster reload ${cluster-name} -N tidb`


## 销毁集群

此操作会关闭服务，清空数据目录和部署目录，并且无法恢复，请谨慎操作。

{{< copyable "shell-regular" >}}

```bash
tiup cluster destroy ${cluster-name}
```
