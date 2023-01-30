---
title: Witness 使用文档
summary: 如何使用 Witness。
---

# Witness 使用文档

> **警告：**
>
> - 此功能开启且通过 PD placement rule 设置 witness 后，witness 副本只存储 Raft 日志但不应用，请在存储可靠性高的环境下使用；当此功能开启，但没有通过 PD placement rule 设置 witness 副本时，不受存储可靠性约束，可提高 TiKV Down 场景下的可用性。
> - 由于 witness 副本没有应用 Raft 日志，因此无法对外提供读写服务，当其为 leader 且无法及时 transfer leader 出去时，客户端 Backoff 超时后，应用可能收到 IsWitness 错误。
> - 该功能自 v6.6.0 版本开始引入，与低版本不兼容，因此不支持降级。

## 功能说明

在云环境上，TiKV 为单节点配备了 AWS EBS 存储，提供 99.9% 的持久性。此外，TiKV 使用了 3 个 Raft 副本，这对于保证耐用性来说可能有点矫枉过正。为了降低成本，我们可以引入一种名为 “2 Replicas With 1 Log Only” 的机制，即 Witness，而不是标准 3 个副本，以节省 30% 的存储资源，并根据经验在云端减少大约 100%（1 核）的 CPU 使用率。与原来的3副本架​​构相比，“1 Log Only” 副本存储 Raft 日志但不 apply，仍然通过 Raft 协议保证了数据的一致性。

除上述描述的存储可靠性高的场景外，witness 可用于快速恢复 Failover 来提高可用性。例如对于 3 缺 1 的情况，虽然也满足多数派，但是这个时候的系统是很脆弱的，而要完整恢复一个新的成员的时间通常是比较长的（先拷贝 Snapshot 然后 Apply 最新的日志），尤其是 Region Snapshot 比较大的情况，且拷贝副本的过程可能会对本就不健康的 Group member 造成更多的压力，因此通过先添加一个 witness，快速下掉不健康的节点，保证恢复数据的过程中日志的安全性，后续再由 PD 的 rule checker 将 witness 变为普通的 Voter。

## 适用场景

Witness 功能适用于以下场景：

* 高可靠的存储环境（99.9%+），比如 AWS EBS 存储，开启并配置 Witness 节点来节约成本。
* 快速恢复 Failover 提高可用性的场景，开启但不配置 Witness 节点。

## 使用步骤

### 第 1 步：开启 Witness

使用 PD Control 执行 [`config set enable-witness true`](/pd-control.md#config-set-enable-witness-true) 命令开启 Witness。

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set enable-witness true 
```

命令输出 `Success` 表示开启成功。如果 Placement rule 没有配置 witness 副本，则默认不会有 Witness 产生，只有当出现 TiKV down 后，会立刻添加一个 witness 节点，后续会根据 PD placement rule 规则将其转换为普通的 Voter。

### 第 2 步：开启 transfer witness leader scheduler

使用 PD Control 执行 

{{< copyable "shell-regular" >}}

```bash
pd-ctl scheduler add transfer-witness-leader-scheduler
```

命令输出 `Success` 表示开启成功。通常情况下 witness 的选举优先级比普通 Voter 低，且在 Leader 发起 transfer leader 时会拒绝掉，但当 Leader down，另一个 Voter 的 Raft 日志数量小于 witness 时，Raft 会选举 witness 成为 leader，由于 witness 没有应用 Raft 日志，无法对外提供读写服务，因此我们需要让 PD 在 witness leader 上报 region 信息时迅速 transfer 出去，也就是 `transfer-witness-leader-scheduler` 的职责。若在 witness transfer leader 的过程中 TiKV 内部出现了问题，Back off 重试失败后，客户端将返回 IsWitness 错误。

如果仅将 Witness 用于快速恢复 Failover 提高可用性的场景，执行到这一步就结束了。若确定使用的存储环境为高可靠（99.9%+），且有节约成本的需求，则可继续执行后续操作。

### 第 3 步：配置 Witness 副本 (注意：仅适用于高可靠存储)

以三副本为例，修改 rule.json 为 [场景六在高可靠的存储环境下配置-witness-副本](/configure-placement-rules.md#场景六在高可靠的存储环境下配置-witness-副本)。

编辑完文件后，使用下面的命令将配置保存至 PD 服务器：
```bash
pd-ctl config placement-rules save --in=rule.json
```