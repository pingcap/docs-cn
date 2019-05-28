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
