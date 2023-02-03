---
title: 使用临时 Witness 副本来加速副本恢复
summary: 如何使用临时 Witness 副本来加速副本恢复。
---

# 使用临时 Witness 副本来加速副本恢复

这篇文档描述如何使用 Witness 副本提高 TiKV Down 场景下的持久性。如果需要在高可靠存储环境中使用 Witness 节约成本，请参考[使用 Witness 节约成本](/use-witness-to-save-costs.md)。

## 功能说明

Witness 功能可用于快速恢复 failover，以提高系统的可用性和数据持久性。例如在 3 缺 1 的情况下，虽然满足多数派要求，但是系统很脆弱，而完整恢复一个新成员的时间通常很长（需要先拷贝 snapshot 然后 apply 最新的日志），特别是 Region snapshot 比较大的情况。而且拷贝副本的过程可能会对不健康的 Group member 造成更多的压力。因此，先添加一个 Witness 可以快速下掉不健康的节点，降低了在恢复一个新成员的过程中（Learner 无法参与选举和提交），又一个节点挂掉导致 Raft Group 变为不可用的风险，从而保证了恢复数据过程中日志的安全性。

> **警告：**
>
> Witness 功能自 v6.6.0 开始引入，与低版本不兼容，因此不支持降级。

## 适用场景

在快速恢复 failover 以提高持久性的场景下，可以开启 Witness 功能但不配置 Witness 副本。

## 使用方法

使用 PD Control 执行 `config set enable-witness true` 命令开启 Witness：

```bash
pd-ctl config set enable-witness true
```

命令输出 `Success` 表示开启成功。如果没有按照[使用 Witness 节约成本](/use-witness-to-save-costs.md)配置 Witness 副本，则集群正常状态下不会有 Witness 副本产生。只有出现 TiKV Down 后，才会立刻添加一个 Witness 节点，后续会由 rule checker 将其转换为普通的 Voter。

## 注意事项

由于 Witness 副本没有应用 Raft 日志，因此无法对外提供读写服务。仅当连续 Down 两个副本且第二个 Down 的副本为leader，Witness 副本被选为 Leader 且无法及时 transfer leader ，客户端 Backoff 超时后，应用可能收到 IsWitness 错误。
