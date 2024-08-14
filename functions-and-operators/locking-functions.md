---
title: 锁函数
summary: 了解 TiDB 中的用户级锁函数。
---

# 锁函数

TiDB 支持 MySQL 8.0 中的大部分用户级[锁函数](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html)。

## 支持的函数

| 函数名                                                                                                                 | 功能描述                                                           |
|:---------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)    | 获取咨询锁。`lockName` 参数不得超过 64 个字符。在超时前，TiDB 最长等待 `timeout` 秒并返回失败。        |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock) | 检查锁是否空闲。 |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock) | 检查锁是否正在使用。如果正在使用，则返回相应的连接 ID。 |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)     | 释放先前获取的锁。`lockName` 参数不得超过 64 个字符。  |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks)   | 释放当前会话持有的所有锁。                       |

## MySQL 兼容性

* TiDB 允许的最短超时时间为 1 秒，最长超时时间为 1 小时（即 3600 秒）。而 MySQL 允许最短 0 秒和最长无限超时（`timeout=-1`）。TiDB 会自动将超出范围的值转换为最接近的允许值，`timeout=-1` 会被转换为 3600 秒。
* TiDB 不会自动检测用户级锁导致的死锁。死锁会话将在 1 小时内超时，但你也可以在任一受影响的会话上使用 [`KILL`](/sql-statements/sql-statement-kill.md) 语句手动终止死锁。你还可以通过始终用相同顺序获取用户级锁的方法来防止死锁。
* 在 TiDB 中，锁对集群中所有 TiDB 服务器生效。而在 MySQL Cluster 和 Group Replication 中，锁只对本地单个服务器生效。
* 如果从另一个会话调用 `IS_USED_LOCK()` 并且无法返回持有锁的进程 ID，则返回 `1`。
