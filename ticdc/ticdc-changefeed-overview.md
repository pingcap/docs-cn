---
title: Changefeed 概述
summary: TODO
---

# Changefeed 概述

TODO

#### 同步任务状态流转

同步任务状态标识了同步任务的运行情况。在 TiCDC 运行过程中，同步任务可能会运行出错、手动暂停、恢复，或达到指定的 `TargetTs`，这些行为都可以导致同步任务状态发生变化。本节描述 TiCDC 同步任务的各状态以及状态之间的流转关系。

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

以上状态流转图中的状态说明如下：

- Normal：同步任务正常进行，checkpoint-ts 正常推进。
- Stopped：同步任务停止，由于用户手动暂停 (pause) changefeed。处于这个状态的 changefeed 会阻挡 GC 推进。
- Error：同步任务报错，由于某些可恢复的错误导致同步无法继续进行，处于这个状态的 changefeed 会不断尝试继续推进，直到状态转为 Normal。处于这个状态的 changefeed 会阻挡 GC 推进。
- Finished：同步任务完成，同步任务进度已经达到预设的 TargetTs。处于这个状态的 changefeed 不会阻挡 GC 推进。
- Failed：同步任务失败。由于发生了某些不可恢复的错误，导致同步无法继续进行，并且无法恢复。处于这个状态的 changefeed 不会阻挡 GC 推进。

以上状态流转图中的编号说明如下：

- ① 执行 `changefeed pause` 命令。
- ② 执行 `changefeed resume` 恢复同步任务。
- ③ `changefeed` 运行过程中发生可恢复的错误，自动进行恢复。
- ④ 执行 `changefeed resume` 恢复同步任务。
- ⑤ `changefeed` 运行过程中发生不可恢复的错误。
- ⑥ `changefeed` 已经进行到预设的 TargetTs，同步自动停止。
- ⑦ `changefeed` 停滞时间超过 `gc-ttl` 所指定的时长，不可被恢复。
- ⑧ `changefeed` 尝试自动恢复过程中发生不可恢复的错误。
