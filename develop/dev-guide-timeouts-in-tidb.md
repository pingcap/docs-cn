---
title: Timeouts in TiDB
summary: Learn about timeouts in TiDB, and solutions for troubleshooting errors.
---

# Timeouts in TiDB

This document describes various timeouts in TiDB to help you troubleshoot errors.

## GC timeout

TiDB's transaction implementation uses the MVCC (Multiple Version Concurrency Control) mechanism. When the newly written data overwrites the old data, the old data will not be replaced, but kept together with the newly written data. The versions are distinguished by the timestamp. TiDB uses the mechanism of periodic Garbage Collection (GC) to clean up the old data that is no longer needed.

By default, each MVCC version (consistency snapshots) is kept for 10 minutes. Transactions that take longer than 10 minutes to read will receive an error `GC life time is shorter than transaction duration`.

If you need longer read time, for example, when you are using **Mydumper** for full backups (**Mydumper** backs up consistent snapshots), you can adjust the value of `tikv_gc_life_time` in the `mysql.tidb` table in TiDB to increase the MVCC version retention time. Note that `tikv_gc_life_time` takes effect globally and immediately. Increasing the value will increase the life time of all existing snapshots, and decreasing it will immediately shorten the life time of all snapshots. Too many MVCC versions will impact TiKV's processing efficiency. So you need to change `tikv_gc_life_time` back to the previous setting in time after doing a full backup with **Mydumper**.

For more information about GC, see [GC Overview](/garbage-collection-overview.md).

## Transaction timeout

GC does not affect ongoing transactions. However, there is still an upper limit to the number of pessimistic transactions that can run, with a limit on the transaction timeout and a limit on the memory used by the transaction. You can modify the transaction timeout by `max-txn-ttl` under the `[performance]` category of the TiDB profile, `60` minutes by default.

SQL statements such as `INSERT INTO t10 SELECT * FROM t1` are not affected by GC, but will be rolled back due to timeout after exceeding `max-txn-ttl`.

## SQL execution timeout

TiDB also provides a system variable (`max_execution_time`, `0` by default, indicating no limit) to limit the execution time of a single SQL statement. Currently, the system variable only takes effect for read-only SQL statements. The unit of `max_execution_time` is `ms`, but the actual precision is at the `100ms` level instead of the millisecond level.

## JDBC query timeout

MySQL JDBC's query timeout setting for `setQueryTimeout()` does **_NOT_** work for TiDB, because the client sends a `KILL` command to the database when it detects the timeout. However, the tidb-server is load balanced, and it will not execute this `KILL` command to avoid termination of the connection on a wrong tidb-server. You need to use `MAX_EXECUTION_TIME` to check the query timeout effect.

TiDB provides the following MySQL-compatible timeout control parameters.

- **wait_timeout**, controls the non-interactive idle timeout for the connection to Java applications. Since TiDB v5.4, the default value of `wait_timeout` is `28800` seconds, which is 8 hours. For TiDB versions earlier than v5.4, the default value is `0`, which means the timeout is unlimited.
- **interactive_timeout**, controls the interactive idle timeout for the connection to Java applications. The value is `8 hours` by default.
- **max_execution_time**, controls the timeout for SQL execution in the connection, only effective for read-only SQL statements. The value is `0` by default, which allows the connection to be infinitely busy, that is, an SQL statement is executed for an infinitely long time.

However, in a real production environment, idle connections and indefinitely executing SQL statements have a negative effect on both the database and the application. You can avoid idle connections and indefinitely executing SQL statements by configuring these two session-level variables in your application's connection string. For example, set the following:

- `sessionVariables=wait_timeout=3600` (1 hour)
- `sessionVariables=max_execution_time=300000` (5 minutes)
