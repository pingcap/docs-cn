---
title: FLASHBACK CLUSTER TO TIMESTAMP
aliases: ['/docs-cn/dev/sql-statements/sql-statement-flashback-cluster-to-timestamp/', '/docs-cn/dev/reference/sql/statements/flashback-cluster-to-timestamp/']
---

# FLASHBACK CLUSTER

在 TiDB 6.4 中，引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法，其功能是将集群的数据恢复到特定的时间点。

## 语法

{{< copyable "sql" >}}

```sql
FLASHBACK CLUSTER TO TIMESATMP '2022-09-21 16:02:50';
```

### 语法图

```ebnf+diagram
FlashbackClusterStmt ::=
    "FLASHBACK" "CLUSTER" "TO" "TIMESTAMP" stringLit
```

## 注意事项

* `FLASHBACK` 指定的时间点需要在 Garbage Collection (GC) life time 时间内，可以使用系统变量 `tidb_gc_life_time` 配置数据的历史版本的保留时间（默认值是 10m0s）。可以使用以下 SQL 语句查询当前的 safePoint，即 GC 已经清理到的时间点：

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

* 仅支持拥有 `SUPER` 权限的用户执行 `FLASHBACK CLUSTER` 操作。
* 在 `FLASHBACK CLUSTER` 指定的时间点到开始执行的时间段内不能存在非 `FLASHBACK CLUSTER` 类型的 DDL 记录。
* 在执行 `FLASHBACK CLUSTER` 期间，TiDB 会主动断开所有非 `FLASHBACK CLUSTER` 的链接，并在禁止对相关字段进行读写操作，直到 `FLASHBACK CLUSTER` 完成。
* `FLASHBACK CLUSTER` 命令不能取消，一旦开始执行会一直重试，直到成功。

## 示例

* 恢复新插入的数据

```sql
mysql> create table t(a int);
Query OK, 0 rows affected (0.09 sec)

mysql> select * from t;
Empty set (0.01 sec)

mysql> select now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> insert into t values (1);
Query OK, 1 row affected (0.02 sec)

mysql> select * from t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> flashback cluster to timestamp '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> select * from t;
Empty set (0.00 sec)
```

## 工作原理

在 TiKV 中为了避免数据并发更新时引入锁的开销从而引入了多版本并发控制 (MVCC) 机制。在该机制下，TiDB 对数据进行修改操作时并不会在原始数据库上直接操作，而是会写入一个更新版本的数据将老的数据覆盖。TiDB 后台的 GC Worker 会定期推进 `tikv_gc_safe_point`，并在后台将旧于该时间点的版本删除。`FLASHBACK CLUSTER` 正是基于 TiKV 这一特性实现的。

`FLASHBACK CLUSTER` 可以简单的分为下面几个阶段，

* 在正式开始之前，TiDB 会将 `FLASHBACK` 过程中需要修改的变量值保存在 `Job.Args` 上，并在结束后恢复。
* 进行前置检查，在所有检查通过之后，TiDB 会主动关闭集群的 GC 和调度，具体检查如下，
    * 检查是否有 DDL 记录在要 `FLASHBACK` 到的时间点到现在存在，如有则结束 `FLASHBACK CLUSTER` 操作。
    * 检查要 `FLASHBACK` 到的时间点是否在 `tikv_gc_safe_point` 之前，如是则结束 `FLASHBACK CLUSTER` 操作。
    * 检查集群中是否有别的 DDL job 正在执行，如有则结束 `FLASHBACK CLUSTER` 操作。
* TiDB 向相关 Region 发起 `PrepareFlashbackToVersion` 请求。TiKV 收到请求后会对这些 Region 上锁，禁止对该 Region 进行读写操作。
* 在锁上所有的 Region 之后，DDL Owner 会推进 Schema Version，并同步到所有的 TiDB 上。TiDB 在 apply 类型为 `FLAHSBACK CLUSTER` 的 `Schema Diff` 时，会主动断开所有非 `FLASHBACK CLUSTER` 的链接。
* TiDB 向相关 Region 发起 `FlashbackToVersion` 的 RPC 请求。TiKV 收到请求后会读取旧版本的数据，并将其用最新的 `CommitTS` 重新写回。当所有 Region 处理完后，TiKV 会统一将其解锁。
* `FLASHBACK CLUSTER` 执行完成后，TiDB 会删除对应的 `JobID` 恢复 DDL 功能，同时通知 `Stats Handle` 从 TiKV 处重新加载统计信息。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
