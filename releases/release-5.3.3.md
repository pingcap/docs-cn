---
title: TiDB 5.3.3 Release Note
---

# TiDB 5.3.3 Release Note

发版日期：2022 年 9 月 14 日

TiDB 版本：5.3.3

## Bug 修复

+ TiKV

    - 修复了 PD leader 发生切换或重启 PD 后，在集群中执行 SQL 语句会出现持续报错的问题。

        - 问题原因：该问题是由于 TiKV 存在 bug，TiKV 向 PD client 发送心跳请求失败后不会重试，只能等待与 PD client 重连。这样，故障 TiKV 节点上的 Region 的信息会逐步变旧，使得 TiDB 无法获取最新的 Region 信息，导致 SQL 执行出错。
        - 影响版本：v5.3.2 和 v5.4.2。目前该问题已在 v5.3.3 上修复。如果你使用 v5.3.2 的 TiDB 集群，可以升级至 v5.3.3。
        - 规避方法：除升级外，你还可以重启无法向 PD 发送 Region 心跳的 TiKV 节点，直至不再有待发送的 Region 心跳为止。

        Bug 详情参见 [#12934](https://github.com/tikv/tikv/issues/12934)。
