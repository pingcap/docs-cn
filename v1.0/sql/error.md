---
title: 错误码与故障诊断
category: user guide
---

# 错误码与故障诊断

本篇文档描述在使用 TiDB 过程中会遇到的问题以及解决方法。

## 错误码

TiDB 兼容 MySQL 的错误码，在大多数情况下，返回和 MySQL 一样的错误码。另外还有一些特有的错误码：

| 错误码 | 说明 |
| --------------------- | -------------------------------------------------- |
| 9001 | 请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络 |
| 9002 | 请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络 |
| 9003 | TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志 |
| 9004 | 当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码 |
| 9005 | 某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志 |
| 9006 | GC Life Time 间隔时间过短，长事务本应读到的数据可能被清理了,应增加GC Life Time |
| 9500 | 单个事务过大，原因及解决方法请参考[这里](../FAQ.md#出现-transaction-too-large-报错怎么办) |

## 故障诊断

参见[故障诊断文档](../trouble-shooting.md)以及 [FAQ](../FAQ.md)。

## 错误信息

> [!WARNING]
We cannot open this file for you. please try again later.
