<<<<<<< HEAD
---
title: PD Recover 使用文档
category: reference
---

# PD Recover 使用文档

PD Recover 是对 PD 进行灾难性恢复的工具，用于恢复无法正常启动或服务的 PD 集群。

## 源码编译

1. [Go](https://golang.org/) Version 1.9 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 `bin/pd-recover`

## 使用方法

### 参数说明

```
  -alloc-id uint
        指定比原集群已分配过的 ID 更大的数
  -cacert string
        指定 PEM 格式的受信任 CA 的证书文件路径
  -cert string
        指定 PEM 格式的 SSL 证书文件路径
  -key string
        指定 PEM 格式的 SSL 证书密钥文件路径，即 `--cert` 所指定的证书的私钥
  -cluster-id uint
        指定原集群的 cluster ID
  -endpoints string
        指定 PD 的地址 (default "http://127.0.0.1:2379")
```

### 恢复流程

1. 从当前集群中找到集群的 Cluster ID 和 Alloc ID。一般在 PD，TiKV 或 TiDB 的日志中都可以获取 Cluster ID。已经分配过的 Alloc ID 可以从 PD 日志获得。另外也可以从 PD 的监控面板的 Metadata Information 监控项中获得。在指定 alloc-id 时需指定一个比当前最大的 Alloc ID 更大的值。如果没有途径获取 Alloc ID，可以根据集群中的 Region，Store 数预估一个较大的数，一般可取高几个数量级的数。
2. 停止整个集群，清空 PD 数据目录，重启 PD 集群。
3. 使用 PD recover 进行恢复，注意指定正确的 cluster-id 和合适的 alloc-id。
4. 提示恢复成功后，重启整个集群。
=======
---
title: PD Recover 使用文档
category: reference
---

# PD Recover 使用文档

PD Recover 是对 PD 进行灾难性恢复的工具，用于恢复无法正常启动或服务的 PD 集群。PD Recover 会随 tidb-ansible 一起下载，位于 resource/bin/pd-recover。

## 快速开始

### 获取 Cluster ID

一般在 PD、TiKV 或 TiDB 的日志中都可以获取 Cluster ID。可以从中控机使用 `ansible ad-hoc`，也可以直接去服务器上查看日志。

#### 从 PD 日志获取 [info] Cluster ID（推荐）

使用以下命令，从 PD 日志中获取 [info] Cluster ID：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd.log | grep "init cluster id" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
……
```

或者也可以从 TiDB 或 TiKV 的日志中获取。

#### 从 TiDB 日志获取 [info] cluster id

使用以下命令，从 TiDB 日志中获取 [info] cluster id：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tidb_servers -m shell -a 'cat {{deploy_dir}}/log/tidb*.log | grep "init cluster id" | head -10'
```

```
10.0.1.15 | CHANGED | rc=0 >>
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
……
```

#### 从 TiKV 日志获取 [info] PD cluster

使用以下命令，从 TiKV 日志中获取 [info] PD cluster：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tikv_servers -m shell -a 'cat {{deploy_dir}}/log/tikv* | grep "PD cluster" | head -10'
```

```
10.0.1.15 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
……
```

### 获取 Alloc ID (TiKV StoreID)

在指定 `alloc-id` 时需指定一个比当前最大的 `Alloc ID` 更大的值。可以从中控机使用 `ansible ad-hoc`，也可以直接去服务器上翻日志。

#### 从 PD 日志获取 [info] allocates id（推荐）

使用以下命令，从 PD 日志中获取 [info] allocates id：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd* | grep "allocates" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.824 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=3000]
[2019/10/15 08:55:01.275 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=4000]
……
```

或者也可以从 TiKV 的日志中获取。

#### 从 TiKV 日志获取 [info] alloc store id

使用以下命令，从 TiKV 日志获取 [info] alloc store id：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tikv_servers -m shell -a 'cat {{deploy_dir}}/log/tikv* | grep "alloc store" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.516 +00:00] [INFO] [node.rs:229] ["alloc store id 4 "]

10.0.1.14 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.734 +00:00] [INFO] [node.rs:229] ["alloc store id 5 "]

10.0.1.15 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.418 +00:00] [INFO] [node.rs:229] ["alloc store id 1 "]

10.0.1.21 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.826 +00:00] [INFO] [node.rs:229] ["alloc store id 2001 "]

10.0.1.20 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.987 +00:00] [INFO] [node.rs:229] ["alloc store id 2002 "]
```

### 部署一套新的 PD 集群

{{< copyable "shell-regular" >}}

```
ansible-playbook bootsrap.yml --tags=pd
```

```
ansible-playbook deploy.yml --tags=pd
```

```
ansible-playbook start.yml --tags=pd
```

旧集群可以通过删除 `data.pd` 目录后，重新启动 PD 服务。

### 使用 pd-recover

{{< copyable "shell-regular" >}}

```
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### 重启 PD 集群

{{< copyable "shell-regular" >}}

```
ansible-playbook rolling_update.yml --tags=pd
```

### 重启 TiDB 或 TiKV

{{< copyable "shell-regular" >}}

```
ansible-playbook rolling_update.yml --tags=tidb,tikv
```

## 常见问题

### 获取 Cluster ID 时发现有多个 Cluster ID

新建 PD 集群时，会生成新的 Cluster ID。可以通过日志判断旧集群的 Cluster ID。

### 执行 pd-recover 时返回错误 `dial tcp 10.0.1.13:2379: connect: connection refused`

执行 pd-recover 时需要 PD 提供服务，请先部署并启动 PD 集群。
>>>>>>> 3d49b5d... pd: update docs for pd-recover (#2410)
