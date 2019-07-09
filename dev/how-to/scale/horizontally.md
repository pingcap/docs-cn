---
title: TiDB 集群扩容缩容方案
category: how-to
---

# TiDB 集群扩容缩容方案

TiDB 集群可以在不影响线上服务的情况下动态进行扩容和缩容。

> **注意：**
>
> 如果使用 Ansible 部署 TiDB 集群，请参考[使用 Ansible 扩容缩容](/how-to/scale/with-ansible.md)。

下面分别介绍如何增加或者删除 PD，TiKV 以及 TiDB 的节点。

下面用到的 pd-ctl 文档可以参考 [pd-control](/reference/tools/pd-control.md)。

## PD

假设现在我们有三个 PD 服务，详细信息如下：

|Name|ClientUrls|PeerUrls|
|----|----------|--------|
|pd1|`http://host1:2379`|`http://host1:2380`|
|pd2|`http://host2:2379`|`http://host2:2380`|
|pd3|`http://host3:2379`|`http://host3:2380`|

我们可以通过 pd-ctl 来查看当前所有 PD 节点的信息：

```bash
./pd-ctl -u http://host1:2379
>> member
```

### 动态添加节点

我们可以使用 `join` 参数，将一个新的 PD 服务加入到现有的 PD 集群里面。
如果我们需要添加 `pd4`，只需要在 `--join` 参数里面填入当前 PD 集群任意一个 PD 服务的 client url，比如：

```bash
./bin/pd-server --name=pd4 \
                --client-urls="http://host4:2379" \
                --peer-urls="http://host4:2380" \
                --join="http://host1:2379"
```

### 动态删除节点

如果我们需要删除 `pd4`，可以通过 pd-ctl 来完成：

```bash
./pd-ctl -u http://host1:2379
>> member delete name pd4
```

### 动态迁移节点

如果想把现有的 PD 节点迁移到新的机器上，我们可以先在新的机器上添加节点，然后把旧的机器上的节点删除掉。迁移过程中应该一个节点一个节点逐个迁移，每完成一个步骤可以先查看一下当前的所有节点信息来进行确认。

## TiKV

我们可以通过 pd-ctl 来查看当前所有 TiKV 节点的信息：

```bash
./pd-ctl -u http://host1:2379
>> store
```

### 动态添加节点

动态添加一个新的 TiKV 服务非常容易，只需要在新的机器上启动一个 TiKV 服务，不需要其他特殊操作。
新启动的 TiKV 服务会自动注册到现有集群的 PD 中，PD 会自动做负载均衡，逐步地把一部分数据迁移到新的TiKV 服务中，从而降低现有 TiKV 服务的压力。

### 动态删除节点

安全地删除（下线）一个 TiKV 服务需要先告诉 PD，这样 PD 可以先把这个 TiKV 服务上面的数据迁移到其他 TiKV 服务上，保证数据有足够的副本数。

假设我们需要删除 store id 为 1 的 TiKV 服务，可以通过 pd-ctl 来完成：

```bash
./pd-ctl -u http://host1:2379
>> store delete 1
```

然后可以查看这个 TiKV 服务的状态：

```bash
./pd-ctl -u http://host1:2379
>> store 1
{
  "store": {
    "id": 1,
    "address": "127.0.0.1:21060",
    "state": 1,
    "state_name": "Offline"
  },
  "status": {
    ...
  }
}
```

我们可以通过这个 store 的 state_name 来确定这个 store 的状态：

- Up：这个 store 正常服务
- Disconnected：当前没有检测到这个 store 的心跳，可能是故障或网络连接中断
- Down：超过一小时（可通过 `max-down-time` 配置）没有收到 store 心跳，此时 PD 会为这个 store 上的数据添加副本
- Offline：这个 store 正在将其中的 Region 转移到其他节点，此时这个 store 仍在服务中
- Tombstone：这个 store 已经完成下线，此时 store 上已经没有数据，可以关闭实例

### 动态迁移节点

迁移 TiKV 服务也是通过先在新的机器上添加节点，然后把旧的机器上的节点下线来完成。迁移过程中可以先把新集群的机器全部添加到已有的集群中，然后再把旧的节点一个一个地下线。可以通过查看正在下线的节点的状态信息来确定这个节点是否已经完成下线，确认完成以后再下线下一个节点。

## TiDB

TiDB 是一个无状态的服务，这也就意味着我们能直接添加和删除 TiDB。需要注意的是，如果我们在 TiDB 的服务的前面搭建了一个 proxy（譬如 HAProxy），则需要更新 proxy 的配置并重新载入。
