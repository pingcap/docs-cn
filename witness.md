---
title: Witness 使用文档
summary: 如何使用 Witness。
---

# Witness 使用文档

> **警告：**
>
> - 此功能开启且通过 PD placement rule 设置 witness 后，witness 副本只会存储最近的 Raft 日志来进行多数派确认，但不会存储数据。所以，如果你的数据本身设置了 3 副本冗余，当开启 witness 副本时，仅只有两个副本存储着完整的数据；这种情况下，只有当你的磁盘可靠性达到一定程度（如使用 AWS 的 gp3 磁盘，可靠性有 99.8%~99.9%）时，才考虑开启 witness；当此功能开启，但没有通过 PD placement rule 设置 witness 副本时，不受存储可靠性约束，可提高 TiKV Down 场景下的可用性。
> - 由于 witness 副本没有应用 Raft 日志，因此无法对外提供读写服务，当其为 leader 且无法及时 transfer leader 出去时，客户端 Backoff 超时后，应用可能收到 IsWitness 错误。
> - 该功能自 v6.6.0 版本开始引入，与低版本不兼容，因此不支持降级。

## 功能说明

在云环境中，当 TiKV 使用 Amazon EBS 作为单节点存储时，Amazon EBS 能提供 99.9% 的持久性。此时，TiKV 使用 3 个 Raft 副本虽然可行，但并不必要。为了降低成本，TiDB 引入了 Witness 功能，即 2 Replicas With 1 Log Only 机制。其中 1 Log Only 副本仅存储 Raft 日志但不进行数据 apply，依然可以通过 Raft 协议保证数据一致性。与标准的 3 副本架构相比，Witness 可以节省 30% 的存储资源，并在云端减少大约 100%（1 核）的 CPU 使用率。

除了存储可靠性高的场景外，Witness 功能还可用于快速恢复 failover，以提高系统可用性。例如在 3 缺 1 的情况下，虽然满足多数派要求，但是系统很脆弱，而完整恢复一个新成员的时间通常很长（需要先拷贝 snapshot 然后 apply 最新的日志），特别是 Region snapshot 比较大的情况。而且拷贝副本的过程可能会对不健康的副本造成更多的压力。因此，先添加一个 witness 可以快速下掉不健康的节点，保证恢复数据的过程中日志的安全性，后续再由 PD 的 rule checker 将 witness 副本变为普通的 Voter。

## 适用场景

Witness 功能适用于以下场景：

* 高可靠的存储环境（99.9%+），比如 AWS EBS 存储，开启并配置 Witness 节点来节约成本。
* 快速恢复 Failover 提高可用性的场景，开启但不配置 Witness 节点。

## 使用步骤

### 第 1 步：开启 Witness

使用 PD Control 执行 [`config set enable-witness true`](/pd-control.md#config-set-enable-witness-true) 命令开启 Witness：

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set enable-witness true 
```

命令输出 `Success` 表示开启成功。如果 Placement Rules 没有配置 witness 副本，则默认不会有 witness 产生。只有出现 TiKV down 后，才会立刻添加一个 witness 节点，后续会根据 PD Placement Rules 规则将其转换为普通的 Voter。

### 第 2 步：开启 transfer witness leader scheduler

使用 PD Control 执行 

{{< copyable "shell-regular" >}}

```bash
pd-ctl scheduler add transfer-witness-leader-scheduler
```

命令输出 `Success` 表示开启成功。通常情况下 witness 的选举优先级比普通 Voter 低，并且在 Leader 发起 transfer leader 时会拒绝。但是，当 Leader 出现故障，且另一个 Voter 的 Raft 日志数量小于 witness 时，Raft 会选举 witness 作为 Leader。由于 witness 没有应用 Raft 日志，无法对外提供读写服务，因此需要通过 `transfer-witness-leader-scheduler` 在 witness Leader 上报 Region 信息时尽快 transfer leader。如果在 witness transfer leader 过程中 TiKV 内部出现问题，并且 backoff 重试失败后，客户端将返回 IsWitness 错误。

如果仅将 Witness 用于快速恢复 failover 提高可用性的场景，执行到这一步就结束了。若确定使用的存储环境为高可靠（99.9%+），且有节约成本的需求，则可安装下面的步骤配置 witness 副本。

### 第 3 步：配置 witness 副本（仅适用于高可靠存储）

以三副本为例，修改 `rule.json` 为[场景六：在高可靠的存储环境下配置 witness 副本](/configure-placement-rules.md#场景六在高可靠的存储环境下配置-witness-副本)中的配置。

编辑完文件后，使用下面的命令将配置保存至 PD 服务器：
```bash
pd-ctl config placement-rules save --in=rule.json
```