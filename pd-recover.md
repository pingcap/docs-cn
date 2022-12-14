---
title: PD Recover 使用文档
aliases: ['/docs-cn/dev/pd-recover/','/docs-cn/dev/reference/tools/pd-recover/']
---

# PD Recover 使用文档

PD Recover 是对 PD 进行灾难性恢复的工具，用于恢复无法正常启动或服务的 PD 集群。

## 安装 PD Recover

要使用 PD Recover，你可以[从源代码编译](#从源代码编译)，也可以直接[下载 TiDB 工具包](#下载-tidb-工具包)。

### 从源代码编译

* [Go](https://golang.org/)：PD Recover 使用了 Go 模块，请安装 Go v1.16 或更新版本。
* 在 [PD](https://github.com/pingcap/pd) 根目录下，运行 `make pd-recover` 命令来编译源代码并生成 `bin/pd-recover`。

> **注意：**
>
> 一般来说，用户不需要编译源代码，因为发布的二进制文件或 Docker 中已包含 PD Recover 工具。开发者可以参考以上步骤来编译源代码。

### 下载 TiDB 工具包

PD Recover 的安装包位于 TiDB 离线工具包中。下载方式，请参考 [TiDB 工具下载](/download-ecosystem-tools.md)。

## 方式一：从剩余 PD 集群重建

PD 集群一旦超过大多数的节点发生灾难，则无法提供服务。当还有 PD 节点存活时，可以选择一个存活的 PD 节点强制修改 raft group 的成员为，从而使该节点恢复服务。具体方式为：

### 第 1 步：停掉所有节点

把集群中的服务进程都停止 (TiKV/TiFlash/TiDB)，防止在还未恢复过程中与 PD 参数交互，造成数据错乱等无法挽救的异常状况。

### 第 2 步：使用特定地启动参数拉起该存活的 PD 节点

加上特定地启动参数 `--force-new-cluster` 拉起该存活的 PD 节点, 如：

{{< copyable "shell-regular" >}}

```
 ./bin/pd-server --force-new-cluster --name=pd-127.0.0.10-2379 --client-urls=http://0.0.0.0:2379 --advertise-client-urls=http://127.0.0.1:2379 --peer-urls=http://0.0.0.0:2380 --advertise-peer-urls=http://127.0.0.1:2380 --config=conf/pd.toml 
```

### 第 3 步： 使用 pd-recover 修复元数据

由于是从少数派节点直接恢复服务，该节点可能存在数据是落后的，特别是 alloc_id，tso 这种一旦发生回退，则可能会给集群数据错乱或不可用的影响。因此，我们需要通过 pd-recover 来修改一些元数据，从而使得这个 PD 能继续提供正确的分配 ID，TSO 等服务，具体命令参考：

{{< copyable "shell-regular" >}}

```
 ./bin/pd-recover --from-old-member --endpoints=http://127.0.0.1:2379 // 指定对应的 PD 地址
```

> **注意：**
>
> 该步骤会自动将存储中的 alloc_id 加一个 safe guard 的值 100000000, 后续集群中分配的 ID 会偏大。
>
> 此外，pd-recover 不会对 tso 进行修改，请保证本地时间是大于故障发生时的时间的，且确认故障前 PD 组件之间是开启 NTP 时钟同步服务的。否则需要将本地时钟调整到一个比较未来的时间保障 TSO 不回退。

### 第 4 步：重启这个 PD

当出现上一步出现 `recovery is successful` 的提示信息时，重启整个集群。

### 第 5 步：扩容 PD，拉起集群

通过部署工具扩容 PD，并把其他组件都拉起来。至此服务恢复

## 方式二：完全重建 PD 集群

该方式适用于所有 PD 的数据都没在了，但其他组件都还在的情况。

### 第 1 步： 获取 Cluster ID

一般在 PD、TiKV 或 TiDB 的日志中都可以获取 Cluster ID。你可以直接在服务器上查看日志以获取 Cluster ID。

#### 从 PD 日志获取 Cluster ID（推荐）

使用以下命令，从 PD 日志中获取 Cluster ID：

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

或者也可以从 TiDB 或 TiKV 的日志中获取。

#### 从 TiDB 日志获取 Cluster ID

使用以下命令，从 TiDB 日志中获取 Cluster ID：

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### 从 TiKV 日志获取 Cluster ID

使用以下命令，从 TiKV 日志中获取 Cluster ID：

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### 第 2 步：获取已分配 ID

在指定已分配 ID 时，需指定一个比当前最大的已分配 ID 更大的值。可以从监控中获取已分配 ID，也可以直接在服务器上查看日志。

#### 从监控中获取已分配 ID（推荐）

要从监控中获取已分配的 ID，需要确保你所查看的监控指标是**上一任 PD Leader** 的指标。可从 PD Dashboard 中 **Current ID allocation** 面板获取最大的已分配 ID。

#### 从 PD 日志获取已分配 ID

要从 PD 日志中获取分配的 ID，需要确保你所查看的日志是**上一任 PD Leader** 的日志。运行以下命令获取最大的已分配 ID：

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

你也可以在所有 PD server 中运行上述命令，找到最大的值。

### 第 3 步：部署一套新的 PD 集群

部署新的 PD 集群之前，需要停止当前的 PD 集群，然后删除旧的数据目录（或者用 `--data-dir` 指定新的数据目录）。

### 第 4 步：使用 pd-recover

只需在一个 PD 节点上执行 `pd-recover` 即可。

{{< copyable "shell-regular" >}}

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### 第5 步：重启整个集群

当出现 `recovery is successful` 的提示信息时，重启整个集群。

## 常见问题

### 获取 Cluster ID 时发现有多个 Cluster ID

新建 PD 集群时，会生成新的 Cluster ID。可以通过日志判断旧集群的 Cluster ID。

### 执行 pd-recover 时返回错误 `dial tcp 10.0.1.13:2379: connect: connection refused`

执行 pd-recover 时需要 PD 提供服务，请先部署并启动 PD 集群。
