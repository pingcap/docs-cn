---
title: 双数据中心的同步复制
summary: 了解如何为双数据中心配置同步复制。
---

# 双数据中心的同步复制

本文档介绍如何开启双数据中心之间的同步复制。

> **警告：**
>
> 同步复制功能当前仍为实验特性，请勿在生产环境中使用。

在双数据中心场景下，两个数据中心一个为主数据中心，另一个为数据恢复中心。当某个 Region 的副本数量为奇数时，主中心会存储更多此 Region 的副本。当数据恢复中心宕机超过指定时限后，两个数据中心之间将默认采用异步模式复制数据。

要开启同步复制模式，可以在 PD 配置文件中进行配置，或使用 `pd-ctl` 手动更改复制模式。

## 在 PD 配置文件中开启同步复制

复制模式由 PD 控制。你可以在部署集群时，在 PD 配置文件中进行配置。示例如下：

{{< copyable "" >}}

```toml
[replication-mode]
replication-mode = "dr-auto-sync"
[replication-mode.dr-auto-sync]
label-key = "zone"
primary = "z1"
dr = "z2"
primary-replicas = 2
dr-replicas = 1
wait-store-timeout = "1m"
wait-sync-timeout = "1m"
```

在上方示例中各项配置意义如下：

+ `dr-auto-sync` 用于开启同步复制模式。
+ Label key 设置为 `zone` 用于区别不同的数据中心。
+ 值为 `"z1"` 的 TiKV 实例位于主数据中心，值为 `"z2"` 的 TiKV 实例位于数据恢复中心。
+ `primary-replicas` 表示应该存储在主数据中心的副本数量。
+ `dr-replicas` 表示应该存储在数据恢复中心的副本数量。
+ `wait-store-timeout` 用于设置从同步复制变为异步复制之前的等待时间。

输入下方 URL 可查看集群当前的复制状态：

{{< copyable "shell-regular" >}}

```bash
% curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

```bash
{
  "mode": "dr-auto-sync",
  "dr-auto-sync": {
    "label-key": "zone",
    "state": "sync"
  }
}
```

> **注意：**
>
> 集群的复制状态说明了 Region 被复制的方式，有三个选项：`async`， `sync-recover` 和 `sync`。

集群的复制状态变为 `sync` 后，如果掉线的实例数大于任一数据中心应该存储的副本数，状态会自动变为 `async`。一旦集群的复制状态变为 `async`，PD 会要求 TiKV 将复制模式更改为 `asynchronous` 并时不时检查 TiKV 实例是否已被恢复。而当掉线的实例数恢复到小于任一数据中心应该存储的副本数时，集群会进入 `sync-recover` 复制状态，并要求 TiKV 将复制模式更改为 `synchronous`。直到所有的 Region 都同步完毕后，集群会再次进入 `sync` 复制状态。

## 手动更改复制模式

可以使用 [`pd-ctl`](/pd-control.md) 将集群从 `asynchronous` 改为 `synchronous`：

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode dr-auto-sync
```

或者从 `synchronous` 改回 `asynchronous`：

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode majority
```

也可以更新 label key：

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode dr-auto-sync label-key dc
```
