---
title: 使用临时 Witness 副本来加速副本恢复
summary: 如何使用临时 Witness 副本来加速副本恢复。
---

# 使用临时 Witness 副本来加速副本恢复

> **警告：**
>
> - 如果开启了 Witness 功能但没有通过 PD Placement Rules 设置 Witness 副本, 则不受存储可靠性的约束。 此时可提高 TiKV Down 场景下的可用性。若有使用 Witness 节约成本的需求，请参考 [使用 Witness 节约成本](/use-witness-to-save-costs.md)；
> - 由于 Witness 副本没有应用 Raft 日志，因此无法对外提供读写服务。当 Witness 副本为 Leader 且无法及时 transfer leader 时，客户端 Backoff 超时后，应用可能收到 IsWitness 错误。
> - Witness 功能自 v6.6.0 版本开始引入，与低版本不兼容，因此不支持降级。

## 功能说明

除了[使用 Witness 节约成本](/use-witness-to-save-costs.md)，Witness 功能还可用于快速恢复 failover，以提高系统可用性。例如在 3 缺 1 的情况下，虽然满足多数派要求，但是系统很脆弱，而完整恢复一个新成员的时间通常很长（需要先拷贝 snapshot 然后 apply 最新的日志），特别是 Region snapshot 比较大的情况。而且拷贝副本的过程可能会对不健康的副本造成更多的压力。因此，先添加一个 Witness 可以快速下掉不健康的节点，保证恢复数据的过程中日志的安全性，后续再由 PD 的 rule checker 将 Witness 副本变为普通的 Voter。

## 适用场景

Witness 功能适用于以下场景：

* 快速恢复 failover 提高可用性的场景，可以开启 Witness 功能但不配置 Witness 副本。

## 使用步骤

### 第 1 步：开启 Witness

使用 PD Control 执行 [`config set enable-witness true`](/pd-control.md#config-set-enable-witness-true) 命令开启 Witness：

```bash
pd-ctl config set enable-witness true
```

命令输出 `Success` 表示开启成功。如果 Placement Rules 没有配置 Witness 副本，则默认不会有 Witness 产生。只有出现 TiKV down 后，才会立刻添加一个 Witness 节点，后续会根据 PD Placement Rules 规则将其转换为普通的 Voter。