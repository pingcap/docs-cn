---
title: 错误码与故障诊断
category: reference
---

# 错误码与故障诊断

本篇文档描述在使用 TiDB 过程中会遇到的问题以及解决方法。

## 错误码

TiDB 兼容 MySQL 的错误码，在大多数情况下，返回和 MySQL 一样的错误码。另外还有一些特有的错误码：

| 错误码 | 说明 |
| --------------------- | -------------------------------------------------- |
| 8001 | 请求使用的内存超过 TiDB 内存使用的阈值限制 |
| 8002 | 带有 `SELECT FOR UPDATE` 语句的事务，在遇到写入冲突时，为保证一致性无法进行重试，事务将进行回滚并返回该错误 |
| 8003 | `ADMIN CHECK TABLE` 命令在遇到行数据跟索引不一致的时候返回该错误 |
| 8004 | 单个事务过大，原因及解决方法请参考[这里](/dev/faq/tidb.md#433-transaction-too-large-是什么原因怎么解决) |
| 8005 | 事务在 TiDB 中遇到了写入冲突，原因及解决方法请参考[这里](/dev/faq/tidb.md#九故障排除) |
| 9001 | 请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络 |
| 9002 | 请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络 |
| 9003 | TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志 |
| 9004 | 当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码 |
| 9005 | 某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志 |
| 9006 | GC Life Time 间隔时间过短，长事务本应读到的数据可能被清理了，应增加 GC Life Time |
| 9007 | 事务在 TiKV 中遇到了写入冲突，原因及解决方法请参考[这里](/dev/faq/tidb.md#九故障排除) |

## 故障诊断

参见[故障诊断文档](/dev/how-to/troubleshoot/cluster-setup.md)以及 [FAQ](/dev/faq/tidb.md)。
