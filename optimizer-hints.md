---
title: Optimizer Hints
aliases: ['/docs-cn/stable/optimizer-hints/','/docs-cn/v4.0/optimizer-hints/','/docs-cn/stable/reference/performance/optimizer-hints/']
---

# Optimizer Hints

TiDB 支持 Optimizer Hints 语法，它基于 MySQL 5.7 中介绍的类似 comment 的语法，例如 `/*+ HINT_NAME(t1, t2) */`。当 TiDB 优化器选择的不是最优查询计划时，建议使用 Optimizer Hints。

> **注意：**
>
> MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 `Hint` 语法，需要在启动客户端时加上 `--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

## 语法

Optimizer Hints 不区分大小写，通过 `/*+ ... */` 注释的形式跟在 `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面。`INSERT` 关键字后不支持 Optimizer Hints。

多个不同的 Hint 之间需用逗号隔开，例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

可以通过 [`Explain`](/sql-statements/sql-statement-explain.md) / [`Explain Analyze`](/sql-statements/sql-statement-explain-analyze.md) 语句的输出，来查看 Optimizer Hints 对查询执行计划的影响。

如果 Optimizer Hints 包含语法错误或不完整，查询语句不会报错，而是按照没有 Optimizer Hints 的情况执行。如果 Hint 不适用于当前语句，TiDB 会返回 Warning，用户可以在查询结束后通过 `Show Warnings` 命令查看具体信息。

> **注意：**
>
> 如果注释不是跟在指定的关键字后，会被当作是普通的 MySQL comment，注释不会生效，且不会上报 warning。

TiDB 目前支持的 Optimizer Hints 根据生效范围的不同可以划分为两类：第一类是在查询块范围生效的 Hint，例如 [`/*+ HASH_AGG() */`](#hash_agg)；第二类是在整个查询范围生效的 Hint，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

每条语句中每一个查询和子查询都对应着一个不同的查询块，每个查询块有自己对应的名字。以下面这条语句为例：

{{< copyable "sql" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

该查询语句有 3 个查询块，最外面一层 `SELECT` 所在的查询块的名字为 `sel_1`，两个 `SELECT` 子查询的名字依次为 `sel_2` 和 `sel_3`。其中数字序号根据 `SELECT` 出现的位置从左到右计数。如果分别用 `DELETE` 和 `UPDATE` 查询替代第一个 `SELECT` 查询，则对应的查询块名字分别为 `del_1` 和 `upd_1`。

## 查询块范围生效的 Hint

这类 Hint 可以跟在查询语句中**任意** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面。通过在 Hint 中使用查询块名字可以控制 Hint 的生效范围，以及准确标识查询中的每一个表（有可能表的名字或者别名相同），方便明确 Hint 的参数指向。若不显式地在 Hint 中指定查询块，Hint 默认作用于当前查询块。以如下查询为例：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

该 Hint 在 `sel_1` 这个查询块中生效，参数分别为 `sel_1` 中的 `t1` 表（`sel_2` 中也有一个 `t1` 表）和 `t3` 表。

如上例所述，在 Hint 中使用查询块名字的方式有两种：第一种是作为 Hint 的第一个参数，与其他参数用空格隔开。除 `QB_NAME` 外，本节所列的所有 Hint 除自身明确列出的参数外都有一个隐藏的可选参数 `@QB_NAME`，通过使用这个参数可以指定该 Hint 的生效范围；第二种在 Hint 中使用查询块名字的方式是在参数中的某一个表名后面加 `@QB_NAME`，用以明确指出该参数是哪个查询块中的表。

> **注意：**
>
> Hint 声明的位置必须在指定生效的查询块之中或之前，不能是在之后的查询块中，否则无法生效。

### QB_NAME

当查询语句是包含多层嵌套子查询的复杂语句时，识别某个查询块的序号和名字很可能会出错，Hint `QB_NAME` 可以方便我们使用查询块。`QB_NAME` 是 Query Block Name 的缩写，用于为某个查询块指定新的名字，同时查询块原本默认的名字依然有效。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

这条 Hint 将最外层 `SELECT` 查询块的命名为 `QB1`，此时 `QB1` 和默认名称 `sel_1` 对于这个查询块来说都是有效的。

> **注意：**
>
> 上述例子中，如果指定的 `QB_NAME` 为 `sel_2`，并且不给原本 `sel_2` 对应的第二个查询块指定新的 `QB_NAME`，则第二个查询块的默认名字 `sel_2` 会失效。

### MERGE_JOIN(t1_name [, tl_name ...])

`MERGE_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Sort Merge Join 算法。这个算法通常会占用更少的内存，但执行时间会更久。当数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1，t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> `MERGE_JOIN` 的别名是 `TIDB_SMJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，但推荐使用 `MERGE_JOIN`。

### INL_JOIN(t1_name [, tl_name ...])

`INL_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Index Nested Loop Join 算法。这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1，t2 WHERE t1.id = t2.id;
```

`INL_JOIN()` 中的参数是建立查询计划时内表的候选表，比如 `INL_JOIN(t1)` 只会考虑使用 t1 作为内表构建查询计划。表如果指定了别名，就只能使用表的别名作为 `INL_JOIN()` 的参数；如果没有指定别名，则用表的本名作为其参数。比如在 `SELECT /*+ INL_JOIN(t1) */ * FROM t t1, t t2 WHERE t1.a = t2.b;` 中，`INL_JOIN()` 的参数只能使用 t 的别名 t1 或 t2，不能用 t。

> **注意：**
>
> `INL_JOIN` 的别名是 `TIDB_INLJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，但推荐使用 `INL_JOIN`。

### INL_HASH_JOIN

`INL_HASH_JOIN(t1_name [, tl_name])` 提示优化器使用 Index Nested Loop Hash Join 算法。该算法与 Index Nested Loop Join 使用条件完全一样，两者的区别是 `INL_JOIN` 会在连接的内表上建哈希表，而 `INL_HASH_JOIN` 会在连接的外表上建哈希表，后者对于内存的使用是有固定上限的，而前者使用的内存使用取决于内表匹配到的行数。

### INL_MERGE_JOIN

`INL_MERGE_JOIN(t1_name [, tl_name])` 提示优化器使用 Index Nested Loop Merge Join 算法。这个 Hint 的适用场景和 `INL_JOIN` 一致，相比于 `INL_JOIN` 和 `INL_HASH_JOIN` 会更节省内存，但使用条件会更苛刻：join keys 中的内表列集合是内表使用的索引的前缀，或内表使用的索引是 join keys 中的内表列集合的前缀。

### HASH_JOIN(t1_name [, tl_name ...])

`HASH_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Hash Join 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1，t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> `HASH_JOIN` 的别名是 `TIDB_HJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称，推荐使用 `HASH_JOIN`。

### HASH_AGG()

`HASH_AGG()` 提示优化器对指定查询块中所有聚合函数使用 Hash Aggregation 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_AGG() */ count(*) FROM t1，t2 WHERE t1.a > 10 GROUP BY t1.id;
```

### STREAM_AGG()

`STREAM_AGG()` 提示优化器对指定查询块中所有聚合函数使用 Stream Aggregation 算法。这个算法通常会占用更少的内存，但执行时间会更久。数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ STREAM_AGG() */ count(*) FROM t1，t2 WHERE t1.a > 10 GROUP BY t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引。

下面例子的效果等价于 `SELECT * FROM t t1 use index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **注意：**
>
> 当该 Hint 中只指定表名，不指定索引名时，表示不考虑使用任何索引，而是选择全表扫。

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表忽略给出的索引。

下面例子的效果等价于 `SELECT * FROM t t1 ignore index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
SELECT /*+ IGNORE_INDEX(t1, idx1, idx2) */ * FROM t t1;
```

### AGG_TO_COP()

`AGG_TO_COP()` 提示优化器将指定查询块中的聚合函数下推到 coprocessor。如果优化器没有下推某些适合下推的聚合函数，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ AGG_TO_COP() */ sum(t1.a) FROM t t1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` 提示优化器从指定的存储引擎来读取指定的表，目前支持的存储引擎参数有 `TIKV` 和 `TIFLASH`。如果为表指定了别名，就只能使用表的别名作为 `READ_FROM_STORAGE()` 的参数；如果没有指定别名，则用表的本名作为其参数。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **注意：**
>
> 如果需要提示优化器使用的表不在同一个数据库内，需要显式指定数据库名。例如 `SELECT /*+ READ_FROM_STORAGE(TIFLASH[test1.t1,test2.t2]) */ t1.a FROM test1.t t1, test2.t t2 WHERE t1.a = t2.a;`。

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` 提示优化器通过 index merge 的方式来访问指定的表，其中索引列表为可选参数。若显式地指出索引列表，会尝试在索引列表中选取索引来构建 index merge。若不给出索引列表，会尝试在所有可用的索引中选取索引来构建 index merge。例如：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

当对同一张表有多个 `USE_INDEX_MERGE` Hint 时，优化器会从这些 Hint 指定的索引列表的并集中尝试选取索引。

> **注意：**
>
> `USE_INDEX_MERGE` 的参数是索引名，而不是列名。对于主键索引，索引名为 `primary`。

目前该 Hint 生效的条件较为苛刻，包括：

- 如果查询有除了全表扫以外的单索引扫描方式可以选择，优化器不会选择 index merge；
- 如果查询在显式事务里，且该条查询之前的语句已经涉及写入，优化器不会选择 index merge；

## 查询范围生效的 Hint

这类 Hint 只能跟在语句中**第一个** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面，等同于在当前这条查询运行时对指定的系统变量进行修改，其优先级高于现有系统变量的值。

> **注意：**
>
> 这类 Hint 虽然也有隐藏的可选变量 `@QB_NAME`，但就算指定了该值，Hint 还是会在整个查询范围生效。

### NO_INDEX_MERGE()

`NO_INDEX_MERGE()` 会关闭优化器的 index merge 功能。

下面的例子不会使用 index merge：

{{< copyable "sql" >}}

```sql
SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE t.a > 0 or t.b > 0;
```

除了 Hint 外，系统变量 `tidb_enable_index_merge` 也能决定是否开启该功能。

> **注意：**
>
> `NO_INDEX_MERGE` 优先级高于 `USE_INDEX_MERGE`，当这两类 Hint 同时存在时，`USE_INDEX_MERGE` 不会生效。

### USE_TOJA(boolean_value)

参数 `boolean_value` 可以是 `TRUE` 或者 `FALSE`。`USE_TOJA(TRUE)` 会开启优化器尝试将 in (subquery) 条件转换为 join 和 aggregation 的功能。相对地，`USE_TOJA(FALSE)` 会关闭该功能。

下面的例子会将 `in (SELECT t2.a FROM t2) subq` 转换为等价的 join 和 aggregation：

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_TOJA(TRUE) */ t1.a, t1.b FROM t1 WHERE t1.a in (SELECT t2.a FROM t2) subq;
```

除了 Hint 外，系统变量 `tidb_opt_insubq_to_join_and_agg` 也能决定是否开启该功能。

### MAX_EXECUTION_TIME(N)

`MAX_EXECUTION_TIME(N)` 把语句的执行时间限制在 `N` 毫秒以内，超时后服务器会终止这条语句的执行。

下面的 Hint 设置了 1000 毫秒（即 1 秒）超时：

{{< copyable "sql" >}}

```sql
SELECT /*+ MAX_EXECUTION_TIME(1000) */ * FROM t1 inner join t2 WHERE t1.id = t2.id;
```

除了 Hint 之外，系统变量 `global.max_execution_time` 也能对语句执行时间进行限制。

### MEMORY_QUOTA(N)

`MEMORY_QUOTA(N)` 用于限制语句执行时的内存使用。该 Hint 支持 MB 和 GB 两种单位。内存使用超过该限制时会根据当前设置的内存超限行为来打出一条 log 或者终止语句的执行。

下面的 Hint 设置了 1024 MB 的内存限制：

{{< copyable "sql" >}}

```sql
SELECT /*+ MEMORY_QUOTA(1024 MB) */ * FROM t;
```

除了 Hint 外，系统变量 `tidb_mem_quota_query` 也能限制语句执行的内存使用。

### READ_CONSISTENT_REPLICA()

`READ_CONSISTENT_REPLICA()` 会开启从数据一致的 TiKV follower 节点读取数据的特性。

下面的例子会从 follower 节点读取数据：

{{< copyable "sql" >}}

```sql
SELECT /*+ READ_CONSISTENT_REPLICA() */ * FROM t;
```

除了 Hint 外，环境变量 `tidb_replica_read` 设为 `'follower'` 或者 `'leader'` 也能决定是否开启该特性。

### IGNORE_PLAN_CACHE()

`IGNORE_PLAN_CACHE()` 提示优化器在处理当前 `prepare` 语句时不使用 plan cache。

该 Hint 用于在 [prepare-plan-cache](/tidb-configuration-file.md#prepared-plan-cache) 开启的场景下临时对某类查询禁用 plan cache。

以下示例强制该 `prepare` 语句不使用 plan cache：

{{< copyable "sql" >}}

```sql
prepare stmt FROM 'SELECT  /*+ IGNORE_PLAN_CACHE() */ * FROM t WHERE t.id = ?';
```
