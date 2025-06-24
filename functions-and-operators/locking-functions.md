---
title: 锁定函数
summary: 了解 TiDB 中的用户级锁定函数。
---

# 锁定函数

TiDB 支持 MySQL 8.0 中提供的大多数用户级[锁定函数](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html)。

## 支持的函数

| 名称                                                                                                                 | 描述                                                           |
|:---------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)    | 获取一个建议性锁。`lockName` 参数不能超过 64 个字符。在超时并返回失败之前最多等待 `timeout` 秒。         |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock) | 检查锁是否空闲。 |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock) | 检查锁是否正在使用。如果是，则返回相应的连接 ID。 |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks)   | 释放当前会话持有的所有锁。                        |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)     | 释放先前获取的锁。`lockName` 参数不能超过 64 个字符。 |

## MySQL 兼容性

* TiDB 允许的最小超时时间是 1 秒，最大超时时间是 1 小时（3600 秒）。这与 MySQL 不同，MySQL 允许 0 秒和无限超时（`timeout=-1`）。TiDB 会自动将超出范围的值转换为最接近的允许值，并将 `timeout=-1` 转换为 3600 秒。
* TiDB 不会自动检测用户级锁导致的死锁。死锁的会话将在最多 1 小时后超时，但也可以通过对受影响的会话之一使用 [`KILL`](/sql-statements/sql-statement-kill.md) 来手动解决。你也可以通过始终按相同顺序获取用户级锁来防止死锁。
* 锁在集群中的所有 TiDB 服务器上生效。这与 MySQL Cluster 和 Group Replication 不同，后者的锁仅在单个服务器上本地生效。
* 如果从另一个会话调用 `IS_USED_LOCK()`，且无法返回持有锁的进程 ID，则返回 `1`。
