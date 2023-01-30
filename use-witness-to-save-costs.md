---
title: 使用 Witness 节约成本
summary: 如何使用 Witness 节约成本。
---

# 使用 Witness 节约成本

> **警告：**
>
> - 在开启 Witness 功能并通过 PD Placement Rules 设置 Witness 副本后，Witness 副本只会存储最近的 Raft 日志来进行多数派确认，但不会存储数据。所以，如果你的数据本身设置了 3 副本冗余，当设置 Witness 副本后，仅只有两个副本存储着完整的数据；这种情况下，只有当你的磁盘可靠性达到一定程度（如使用 Amazon EBS 的 gp3 磁盘，可靠性有 99.8%~99.9%）时，才考虑设置 Witness 副本；
> - 由于 Witness 副本没有应用 Raft 日志，因此无法对外提供读写服务，当 Witness 副本为 Leader 且无法及时 transfer leader 时，客户端 Backoff 超时后，应用可能收到 IsWitness 错误。
> - Witness 功能自 v6.6.0 版本开始引入，与低版本不兼容，因此不支持降级。

## 功能说明

在云环境中，当 TiKV 使用如 Amazon EBS 作为单节点存储时，Amazon EBS 能提供 99.9% 的持久性。此时，TiKV 使用 3 个 Raft 副本虽然可行，但并不必要。为了降低成本，TiKV 引入了 Witness 功能，即 2 Replicas With 1 Log Only 机制。其中 1 Log Only 副本仅存储 Raft 日志但不进行数据 apply，依然可以通过 Raft 协议保证数据一致性。与标准的 3 副本架构相比，Witness 可以节省存储资源及 CPU 使用率。

## 适用场景

* 高可靠的存储环境 (99.8%~99.9%)，比如 Amazon EBS 存储，可以开启并配置 Witness 副本来节约成本。

## 使用步骤

### 第 1 步：开启 Witness

使用 PD Control 执行 [`config set enable-witness true`](/pd-control.md#config-set-enable-witness-true) 命令开启 Witness：

```bash
pd-ctl config set enable-witness true
```

命令输出 `Success` 表示开启成功。如果 Placement Rules 没有配置 Witness 副本，则默认不会有 Witness 产生。只有出现 TiKV down 后，才会立刻添加一个 Witness 节点，后续会根据 PD Placement Rules 规则将其转换为普通的 Voter。

### 第 2 步：配置 Witness 副本

以三副本为例，修改 `rule.json` 为[场景六：在高可靠的存储环境下配置 Witness 副本](/configure-placement-rules.md#场景六在高可靠的存储环境下配置-witness-副本)中的配置。

编辑完文件后，使用下面的命令将配置保存至 PD 服务器：

```bash
pd-ctl config placement-rules save --in=rule.json
```