---
title: Locking Functions
summary: Learn about user-level locking functions in TiDB.
---

# Locking Functions

TiDB supports most of the user-level [locking functions](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html) available in MySQL 5.7.

## Supported functions

| Name                                                                                                                 | Description                                                           |
|:---------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)    | Acquires an advisory lock. The `lockName` parameter must be NO longer than 64 characters. Waits maximum `timeout` seconds before timing out and returns a failure.         |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock) | Checks if a lock is free. |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock) | Checks if a lock is in use. If true, it returns the corresponding connection ID. |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks)   | Releases all locks held by the current session.                        |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)     | Releases a previously acquired lock. The `lockName` parameter must be NO longer than 64 characters. |

## MySQL compatibility

* The minimum timeout permitted by TiDB is 1 second, and the maximum timeout is 1 hour (3600 seconds). This differs from MySQL, where both 0 second and unlimited timeouts (`timeout=-1`) are permitted. TiDB will automatically convert out-of-range values to the nearest permitted value and convert `timeout=-1` to 3600 seconds.
* TiDB does not automatically detect deadlocks caused by user-level locks. Deadlocked sessions will timeout after a maximum of 1 hour, but can also be manually resolved by using `KILL` on one of the affected sessions. You can also prevent deadlocks by always acquiring user-level locks in the same order.
* Locks take effect on all TiDB servers in the cluster. This differs from MySQL Cluster and Group Replication where locks are local to a single server.
* `IS_USED_LOCK()` returns `1` if it is called from another session and is unable to return the ID of the process that is holding the lock.
