---
title: Online Unsafe Recovery 使用文档
summary: 如何使用 Online Unsafe Recovery。
---

# Online Unsafe Recovery 使用文档

> **警告：**
>
> 此功能为有损恢复，无法保证数据和数据索引完整性。

当多数副本的永久性损坏造成部分数据不可读写时，可以使用 Online Unsafe Recovery 功能进行数据有损恢复。

## 功能说明

在 TiDB 中，根据用户定义的多种副本规则，一份数据可能会同时存储在多个节点中，从而保证在单个或少数节点暂时离线或损坏时，读写数据不受任何影响。但是，当一个 Region 的多数或全部副本在短时间内全部下线时，该 Region 会处于暂不可用的状态，无法进行读写操作。

如果一段数据的多数副本发生了永久性损坏（如磁盘损坏）等问题，从而导致节点无法上线时，此段数据会一直保持暂不可用的状态。这时，如果用户希望集群恢复正常使用，在用户能够容忍数据回退或数据丢失的前提下，用户理论上可以通过手动移除不可用副本的方式，使 Region 重新形成多数派，进而让上层业务可以写入和读取（可能是 stale 的，或者为空）这一段数据分片。

在这个情况下，当存有可容忍丢失的数据的部分节点受到永久性损坏时，用户可以通过使用 Online Unsafe Recovery，快速简单地进行有损恢复。使用 Online Unsafe Recovery 时，PD 会自动暂停调度（包括 split 和 merge），然后收集全部节点内的数据分片元信息，用 PD 的全局视角生成一份更实时、更完整的恢复计划后，将其计划下发给各个存活的节点，使各节点执行数据恢复任务。另外，下发恢复计划后，PD 还会定期查看恢复进度，并在必要时重新向各节点分发恢复计划。

## 适用场景

Online Unsafe Recovery 功能适用于以下场景：

* 部分节点受到永久性损坏，导致节点无法重启，造成业务端的部分数据不可读、不可写。
* 可以容忍数据丢失，希望受影响的数据恢复读写。

## 使用步骤

### 前提条件

在使用 Online Unsafe Recovery 功能进行数据有损恢复前，请确认以下事项：

* 离线节点导致部分数据确实不可用。
* 离线节点确实无法自动恢复或重启。

### 第 1 步：指定无法恢复的节点

使用 PD Control 执行 [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show) 命令，指定已确定无法恢复的 TiKV 节点，并触发自动恢复。

{{< copyable "shell-regular" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

命令输出 `Success` 表示向 PD 注册任务成功。但仅表示请求已被接受，并不代表恢复成功。恢复任务在后台进行，具体进度使用 [`show`](#第-2-步查看进度等待结束) 查看。命令输出 `Failed` 表示注册任务失败，可能的错误有：

- `unsafe recovery is running`：已经有正在进行的恢复任务
- `invalid input store x doesn't exist`：指定的 store ID 不存在
- `invalid input store x is up and connected`：指定的 store ID 仍然是健康的状态，不应该进行恢复

可通过 `--timeout <seconds>` 指定可允许执行恢复的最长时间。若未指定，默认为 5 分钟。当超时后，恢复中断报错。

> **注意：**
>
> - 由于此命令需要收集来自所有 Peer 的信息，可能会造成 PD 短时间内有明显的内存使用量上涨（10 万个 Peer 预计使用约 500 MiB 内存）。
> - 若执行过程中 PD 发生重启，则恢复中断，需重新触发命令。
> - 一旦执行，所指定的节点将被设为 Tombstone 状态，不再允许启动。
> - 执行过程中，所有调度以及 split/merge 都会被暂停，待恢复成功或失败后自动恢复。

### 第 2 步：查看进度等待结束

节点移除命令运行成功后，使用 PD Control 执行 [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules) 命令，查看移除进度。

{{< copyable "shell-regular" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

恢复过程有多个可能的阶段：

- `collect report`：初始阶段，第一次接收 TiKV 的报告获得的全局信息。
- `tombstone tiflash learner`：在不健康的 Region 中，删除比其他健康 Peer 要新的 TiFlash learner，防止极端情况造成 panic。
- `force leader for commit merge`：特殊阶段。在有未完成的 commit merge 时出现，优先对有 commit merge 的 Region 进行 `force leader`，防止极端情况。
- `force leader`：强制不健康的 Region 在剩余的健康 Peer 中指定一个成为 Raft leader。
- `demote failed voter`：将 Region 不健康的 Voter 降级为 Learner，之后 Region 就可以正常地选出 Raft leader。
- `create empty region`：创建一个空 Region 来补足 key range 的空洞，主要针对的是某些 Region 的所有副本所在的 Store 都损坏了。

每一阶段按照 JSON 格式输出，包括信息，时间，以及具体的恢复计划。例如：

```json
[
    {
        "info": "Unsafe recovery enters collect report stage: failed stores 4, 5, 6",
        "time": "......"
    },
    {
        "info": "Unsafe recovery enters force leader stage",
        "time": "......",
        "actions": {
            "store 1": [
                "force leader on regions: 1001, 1002"
            ],
            "store 2": [
                "force leader on regions: 1003"
            ]
        }
    },
    {
        "info": "Unsafe recovery enters demote failed voter stage",
        "time": "......",
        "actions": {
            "store 1": [
                "region 1001 demotes peers { id:101 store_id:4 }, { id:102 store_id:5 }",
                "region 1002 demotes peers { id:103 store_id:5 }, { id:104 store_id:6 }",
            ],
            "store 2": [
                "region 1003 demotes peers { id:105 store_id:4 }, { id:106 store_id:6 }",
            ]
        }
    },
    {
        "info": "Collecting reports from alive stores(1/3)",
        "time": "......",
        "details": [
            "Stores that have not dispatched plan: ",
            "Stores that have reported to PD: 4",
            "Stores that have not reported to PD: 5, 6",
        ]
    }
]
```

PD 下发恢复计划后，会等待 TiKV 上报执行的结果。如上述输出中最后一阶段的 `Collecting reports from alive stores` 显示 PD 下发恢复计划和接受 TiKV 报告的具体状态。

整个恢复过程包括多个阶段，可能存在某一阶段的多次重试。一般情况下，预计时间为 3~10 个 store heartbeat 周期（一个 store heartbeat 默认为 10s)。当恢复完成后，命令执行结果最后一阶段显示 `"Unsafe recovery finished"`，以及受影响的 Region 所属的 table id（若无或使用 RawKV 则不显示）和受影响的 SQL 元数据 Region。如：

```json
{
    "info": "Unsafe recovery finished",
    "time": "......",
    "details": [
        "Affected table ids: 64, 27",
        "Affected meta regions: 1001",
    ]
}
```

> **注意：**
>
> - 恢复操作把一些 failed Voter 变成了 failed Learner，之后还需要 PD 调度经过一些时间将这些 failed Learner 移除。
> - 建议及时添加新的节点。

若执行过程中发生错误，最后一阶段会显示 `"Unsafe recovery failed"` 以及具体错误。如：

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### 第 3 步：检查数据索引一致性（RawKV 不需要）

执行完成后，可能会导致数据索引不一致。请使用 SQL 的 `ADMIN CHECK`、`ADMIN RECOVER`、`ADMIN CLEANUP` 命令对受影响的表（从 `"Unsafe recovery finished"` 输出的 `"Affected table ids"` 可知）进行数据索引的一致性检查及恢复。

> **注意：**
>
> 数据可以读写并不代表没有数据丢失。

### 第 4 步：移除无法恢复的节点（可选）

<SimpleTab>
<div label="通过 TiUP 部署的节点">

{{< copyable "shell-regular" >}}

```bash
tiup cluster prune <cluster-name>
```

</div>
<div label="通过 TiDB Operator 部署的节点">

1. 删除该 `PersistentVolumeClaim`。

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2. 删除 TiKV Pod，并等待新创建的 TiKV Pod 加入集群。

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
