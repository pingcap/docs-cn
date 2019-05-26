---
title: Optimizer Hints
category: reference
aliases: ['/docs-cn/sql/optimizer-hints/']
---

# Optimizer Hints

TiDB 支持 Optimizer Hints 语法，它基于 MySQL 5.7 中介绍的类似 comment 的语法，例如 `/*+ TIDB_XX(t1, t2) */`。当 TiDB 优化器选择的不是最优查询计划时，建议使用 Optimizer Hints。

> **注意：**
>
> MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 `Hint` 语法，需要在启动客户端时加上 `--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

## 语法

### TIDB_SMJ(t1, t2)

```sql
SELECT /*+ TIDB_SMJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
```

提示优化器使用 Sort Merge Join 算法，这个算法通常会占用更少的内存，但执行时间会更久。
当数据量太大，或系统内存不足时，建议尝试使用。

### TIDB_INLJ(t1, t2)

```sql
SELECT /*+ TIDB_INLJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
```

提示优化器使用 Index Nested Loop Join 算法，这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。`TIDB_INLJ()` 中的参数是建立查询计划时，内表的候选表。即 `TIDB_INLJ(t1)` 只会考虑使用 t1 作为内表构建查询计划。

### TIDB_HJ(t1, t2)

```sql
SELECT /*+ TIDB_HJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
```

提示优化器使用 Hash Join 算法，这个算法多线程并发执行，执行速度较快，但会消耗较多内存。

### SHARD_ROW_ID_BITS

对于 PK 非整数或没有 PK 的表，TiDB 会使用一个隐式的自增 rowid，大量 `INSERT` 时会把数据集中写入单个 Region，造成写入热点。

通过设置 `SHARD_ROW_ID_BITS`，可以把 rowid 打散写入多个不同的 Region，缓解写入热点问题。但是设置的过大会造成 RPC 请求数放大，增加 CPU 和网络开销。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认值 1 个分片

语句示例：

- `CREATE TABLE`：`CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;`
- `ALTER TABLE`：`ALTER TABLE t SHARD_ROW_ID_BITS = 4;`

### tidb_slow_log_threshold

作用域：SESSION

默认值：300

输出慢日志的耗时阈值。当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。默认为 300ms。

示例：

```sql
set tidb_slow_log_threshold = 200
```

## tidb_query_log_max_len

作用域：SESSION

默认值：2048 (bytes)

最长的 SQL 输出长度。当语句的长度大于 query-log-max-len，将会被截断输出。

示例：

```sql
set tidb_query_log_max_len = 20
```
