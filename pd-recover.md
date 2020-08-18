---
title: PD Recover 使用文档
aliases: ['/docs-cn/dev/pd-recover/','/docs-cn/dev/reference/tools/pd-recover/']
---

# PD Recover 使用文档

PD Recover 是对 PD 进行灾难性恢复的工具，用于恢复无法正常启动或服务的 PD 集群。PD Recover 会随 tidb-ansible 一起下载，位于 resource/bin/pd-recover。

## 快速开始

### 获取 Cluster ID

一般在 PD、TiKV 或 TiDB 的日志中都可以获取 Cluster ID。可以从中控机使用 `ansible ad-hoc`，也可以直接去服务器上查看日志。

#### 从 PD 日志获取 [info] Cluster ID（推荐）

使用以下命令，从 PD 日志中获取 [info] 最近的 Cluster ID：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd.log | grep "init cluster id"'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
……
```

或者也可以从 TiDB 或 TiKV 的日志中获取。

#### 从 TiDB 日志获取 [info] cluster id

使用以下命令，从 TiDB 日志中获取 [info] cluster id 获取最近的 cluster id：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tidb_servers -m shell -a 'cat {{deploy_dir}}/log/tidb*.log | grep "init cluster id"'
```

```
10.0.1.15 | CHANGED | rc=0 >>
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
……
```

#### 从 TiKV 日志获取 [info] PD cluster

使用以下命令，从 TiKV 日志中获取 [info] PD cluster 获取最近的 cluster id ：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tikv_servers -m shell -a 'cat {{deploy_dir}}/log/tikv* | grep "PD cluster"'
```

```
10.0.1.15 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
……
```

### 获取 Alloc ID (TiKV StoreID)

在指定 `alloc-id` 时需指定一个比当前最大的 `Alloc ID` 更大的值。可以从中控机使用 `ansible ad-hoc`，也可以直接去服务器上翻日志。

#### 从 PD 监控中获取最大的 alloc id （推荐）

在 PD 监控面板下的 Cluster 栏目下，可以找到 `Current ID allocation`, 代表当前已经分配出去的 id 的最大值。

#### 从 PD 日志获取 [info] allocates id

使用以下命令，从 PD 日志中找出最大的 [info] allocates id：

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd* | grep "allocates"'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.824 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=3000]
[2019/10/15 08:55:01.275 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=4000]
……
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

其中 max-alloc-id 是从日志中或者监控上找到的一个已经分配出去的最大的 alloc id，为了安全，可以将找出来的 id 加个安全的访问，比如加 1000000.
{{< copyable "shell-regular" >}}

```
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id {$max-alloc-id}
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
