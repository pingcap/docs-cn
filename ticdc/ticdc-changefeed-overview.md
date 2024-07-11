---
title: Changefeed 概述
summary: 了解 Changefeed 的基本概念和 Changefeed 状态的定义与流转
---

# Changefeed 概述

Changefeed 是 TiCDC 中的单个同步任务。Changefeed 将一个 TiDB 集群中数张表的变更数据输出到一个指定的下游。TiCDC 集群可以运行和管理多个 Changefeed。

## Changefeed 状态流转

同步任务状态标识了同步任务的运行情况。在 TiCDC 运行过程中，同步任务可能会运行出错、手动暂停、恢复，或达到指定的 `TargetTs`，这些行为都可以导致同步任务状态发生变化。本节描述 TiCDC 同步任务的各状态以及状态之间的流转关系。

![TiCDC state transfer](/media/ticdc/ticdc-changefeed-state-transfer.png)

以上状态流转图中的状态说明如下：

- Normal：同步任务正常进行，checkpoint-ts 正常推进。处于这个状态的 changefeed 会阻塞 GC 推进。
- Stopped：同步任务停止，由于用户手动暂停 (pause) changefeed。处于这个状态的 changefeed 会阻挡 GC 推进。
- Warning：同步任务报错，由于某些可恢复的错误导致同步无法继续进行。处于这个状态的 changefeed 会不断重试，试图继续推进，直到状态转为 Normal。默认重试时间为 30 分钟（可以通过 [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md) 调整），超过该时间，changefeed 会进入 Failed 状态。处于这个状态的 changefeed 会阻挡 GC 推进。
- Finished：同步任务完成，同步任务进度已经达到预设的 TargetTs。处于这个状态的 changefeed 不会阻挡 GC 推进。
- Failed：同步任务失败。处于这个状态的 changefeed 不会自动尝试恢复。为了让用户有足够的时间处理故障，处于这个状态的 changefeed 会阻塞 GC 推进，阻塞时长为 `gc-ttl` 所设置的值，其默认值为 24 小时。在此期间，如果导致任务失败的问题被修复，用户可以手动恢复 changefeed。超过了 `gc-ttl` 时长后，如果 changefeed 仍然处于 Failed 状态，则同步任务无法恢复。

> **注意：**
> 
> - 如果是因为 changefeed 阻塞了 GC, 则 changefeed 最多阻塞 GC 推进 `gc-ttl` 所指定的时长，超过该时长后，changefeed 会被设置成 `failed` 状态，错误类型为 `ErrGCTTLExceeded`，不再阻塞 GC 推进。
> - 如果 changefeed 遭遇错误码为 `ErrGCTTLExceeded`、`ErrSnapshotLostByGC` 或者 `ErrStartTsBeforeGC` 类型的错误，则不再阻塞 GC 推进。

以上状态流转图中的编号说明如下：

- ① 执行 `changefeed pause` 命令。
- ② 执行 `changefeed resume` 恢复同步任务。
- ③ `changefeed` 运行过程中发生可恢复的错误，自动重试。
- ④ `changefeed` 自动重试成功，checkpoint-ts 已经继续推进。
- ⑤ `changefeed` 自动重试超过 30 分钟，重试失败，进入 failed 状态。此时 `changefeed` 会继续阻塞上游 GC，阻塞时长为 `gc-ttl` 所配置的时长。
- ⑥ `changefeed` 遇到不可重试错误，直接进入 failed 状态。此时 `changefeed` 会继续阻塞上游 GC，阻塞时长为 `gc-ttl` 所配置的时长。
- ⑦ `changefeed` 的同步进度到达 target-ts 设置的值，完成同步。
- ⑧ `changefeed` 停滞时间超过 `gc-ttl` 所指定的时长，遭遇 GC 推进错误，不可被恢复。
- ⑨ `changefeed` 停滞时间小于 `gc-ttl` 所指定的时长，故障原因被修复，执行 `changefeed resume` 恢复同步任务。

## 操作 Changefeed

通过 TiCDC 提供的命令行工具 `cdc cli`，你可以管理 TiCDC 集群和同步任务，具体可参考[管理 TiCDC Changefeed](/ticdc/ticdc-manage-changefeed.md)。你也可以通过 HTTP 接口，即 TiCDC OpenAPI 来管理 TiCDC 集群和同步任务，详见 [TiCDC OpenAPI](/ticdc/ticdc-open-api-v2.md)。

如果你使用的 TiCDC 是用 TiUP 部署的，可以通过 `tiup cdc:v<CLUSTER_VERSION> cli` 来使用 TiCDC 命令行工具，注意需要将 `v<CLUSTER_VERSION>` 替换为 TiCDC 集群版本，例如 v8.1.0。你也可以通过直接执行 `cdc cli` 直接使用命令行工具。
