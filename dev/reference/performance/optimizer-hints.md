---
title: Optimizer Hints
category: reference
---

# Optimizer Hints

TiDB 支持 Optimizer Hints 语法，它基于 MySQL 5.7 中介绍的类似 comment 的语法，例如 `/*+ HINT_NAME(t1, t2) */`。当 TiDB 优化器选择的不是最优查询计划时，建议使用 Optimizer Hints。

> **注意：**
>
> MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 `Hint` 语法，需要在启动客户端时加上 `--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

## 语法

Optimizer Hints 通过 `/*+ ... */` 注释的形式跟在 `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面，常见形式如 `/*+ HINT_NAME([t1_name [, t2_name] ...]) */`。Hint 名称不区分大小写，多个不同的 Hint 之间需用逗号隔开。例如：

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) from t t1, t t2 where t1.a = t2.b;
```

TiDB 目前支持两类 Hint，具体用法上有一些差别。第一类 Hint 用于控制优化器的行为，例如 [`/*+ HASH_AGG() */`](#hash_agg)。第二类 Hint 用于对单条查询设置一些运行参数，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

## 优化器相关 Hint 语法

用于控制优化器行为的 Hint 跟在语句中**任意** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面。Hint 的生效范围以及 Hint 中使用的表的生效范围可通过 [Query Block](#query-block) 来指定，若不显式地指定 Query Block， Hint 的默认生效范围为当前 Query Block。

### Query Block

一条语句中每一个查询和子查询都对应着一个不同的 Query Block，每个 Query Block 有自己对应的 `QB_NAME`。以下面这条语句为例：

{{< copyable "sql" >}}

```sql
select * from (select * from t) t1, (select * from t) t2;
```

该查询语句有 3 个 Query Block，最外面一层 `SELECT` 所在的 Query Block 的 `QB_NAME` 为 `sel_1`，两个 `SELECT` 子查询的 `QB_NAME` 依次为 `sel_2` 和 `sel_3`。其中数字序号根据 `SELECT` 出现的位置从左到右计数。如果分别用 `DELETE` 和 `UPDATE` 查询替代第一个 `SELECT` 查询，则对应的 `QB_NAME` 分别为 `del_1` 和 `upd_1`。

### QB_NAME

你可以为当前 Query Block 的 `QB_NAME` 指定新的值，同时原本默认的 `QB_NAME` 值仍然有效。例如：

{{< copyable "sql" >}}

```sql
select /*+ QB_NAME(QB1) */ * from (select * from t) t1, (select * from t) t2;
```

这条 Hint 将 `SELECT` 查询的 `QB_NAME` 设为 `QB1`，此时 `QB1` 和默认名称 `sel_1` 对于这个 Query Block 来说都是有效的。

> **注意：**
>
> 上述例子中，如果指定的 `QB_NAME` 为 `sel_2`，并且不给原本 `sel_2` 对应的第二个 Query Block 指定新的 `QB_NAME`，则第二个 Query Block 的 `QB_NAME` 默认值 `sel_2` 会失效。

### `@QB_NAME` 参数

除 `QB_NAME` 外，其余优化器相关的 Hint 都可以通过可选参数 `@QB_NAME` 来指定该 Hint 的生效范围。该参数需写在最前面，与其他参数用空格隔开。例如：

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * from (select t1.a, t1.b from t t1, t t2 where t1.a = t2.a) t1, t t3 where t1.b = t3.b;
```

同时，你也可以在参数中的每一个表名后面加 `@QB_NAME` 来指定是哪个 Query Block 中的表。

### SM_JOIN(t1_name [, tl_name ...])

`SM_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Sort Merge Join 算法。这个算法通常会占用更少的内存，但执行时间会更久。当数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
select /*+ SM_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

> **注意：**
>
> `SM_JOIN` 的别名是 `TIDB_SMJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称。

### INL_JOIN(t1_name [, tl_name ...])

`INL_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Index Nested Loop Join 算法。这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。例如：

{{< copyable "sql" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

`INL_JOIN()` 中的参数是建立查询计划时内表的候选表，比如 `INL_JOIN(t1)` 只会考虑使用 t1 作为内表构建查询计划。表如果指定了别名，就只能使用表的别名作为 `INL_JOIN()` 的参数；如果没有指定别名，则用表的本名作为其参数。比如在 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` 中，`INL_JOIN()` 的参数只能使用 t 的别名 t1 或 t2，不能用 t。

> **注意：**
>
> `INL_JOIN` 的别名是 `TIDB_INLJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称。

### HASH_JOIN(t1_name [, tl_name ...])

`HASH_JOIN(t1_name [, tl_name ...])` 提示优化器对指定表使用 Hash Join 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

> **注意：**
>
> `HASH_JOIN` 的别名是 `TIDB_HJ`，在 3.0.x 及之前版本仅支持使用该别名；之后的版本同时支持使用这两种名称。

### HASH_AGG()

`HASH_AGG()` 提示优化器使用 Hash Aggregation 算法。这个算法多线程并发执行，执行速度较快，但会消耗较多内存。例如：

{{< copyable "sql" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1，t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG()

`STREAM_AGG()` 提示优化器使用 Stream Aggregation 算法。这个算法通常会占用更少的内存，但执行时间会更久。数据量太大，或系统内存不足时，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1，t2 where t1.a > 10 group by t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表仅使用给出的索引。

下面例子的效果等价于 `select * from t t1 use index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示优化器对指定表忽略给出的索引。

下面例子的效果等价于 `select * from t t1 ignore index(idx1, idx2);`：

{{< copyable "sql" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### AGG_TO_COP()

`AGG_TO_COP()` 提示优化器将聚合操作下推到 coprocessor。如果优化器没有下推某些适合下推的聚合函数，建议尝试使用。例如：

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` 提示优化器从指定的存储引擎来读取指定的表，目前支持的存储引擎参数有 `TIKV` 和 `TIFLASH`。例如：

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` 提示优化器通过 index merge 的方式来访问指定的表，其中索引列表为可选参数。若显式地指出索引列表，会尝试在索引列表中选取索引来构建 index merge。若不给出索引列表，会尝试在所有可用的索引中选取索引来构建 index merge。例如：

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * from t t1 where t1.a > 10 or t1.b > 10;
```

## 运行参数相关 Hint 语法

运行参数相关的 Hint 只能跟在语句中**第一个** `SELECT`、`UPDATE` 或 `DELETE` 关键字的后面，对当前的这条查询的相关运行参数进行修改。

其优先级高于默认设置以及环境变量。

### MAX_EXECUTION_TIME(N)

`MAX_EXECUTION_TIME(N)` 把语句的执行时间限制在 `N` 毫秒以内，超时后服务器会终止这条语句的执行。

下面的 Hint 设置了 1000 毫秒（即 1 秒）超时：

{{< copyable "sql" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

除了 Hint 之外，环境变量 `global.max_execution_time` 也能对语句执行时间进行限制。

### MEMORY_QUOTA(N)

`MEMORY_QUOTA(N)` 用于限制语句执行时的内存使用。该 Hint 支持 MB 和 GB 两种单位。内存使用超过该限制时会根据当前设置的内存超限行为来打出一条 log 或者终止语句的执行。

下面的 Hint 设置了 1024 MB 的内存限制：

{{< copyable "sql" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

除了 Hint 外，环境变量 `tidb_mem_quota_query` 也能限制语句执行的内存使用。

### READ_FROM_REPLICA()

`READ_FROM_REPLICA()` 会开启从数据一致的 TiKV follower 节点读取数据的特性。

下面的例子会从 follower 节点读取数据：

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_REPLICA() */ * from t;
```

除了 Hint 外，环境变量 `tidb_replica_read` 设为 `'follower'` 或者 `'leader'` 也能决定是否开启该特性。

### NO_INDEX_MERGE()

`NO_INDEX_MERGE()` 会关闭优化器的 index merge 功能。

下面的例子不会使用 index merge：

{{< copyable "sql" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

除了 Hint 外，环境变量 `tidb_enable_index_merge` 也能决定是否开启该功能。

### USE_TOJA(boolean_value)

参数 `boolean_value` 可以是 `TRUE` 或者 `FALSE`。`USE_TOJA(TRUE)` 会开启优化器尝试将 in (subquery) 条件转换为 join 和 aggregation 的功能。相对地，`USE_TOJA(FALSE)` 会关闭该功能。

下面的例子会将 `in (select t2.a from t2) subq` 转换为等价的 join 和 aggregation：

{{< copyable "sql" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

除了 Hint 外，环境变量 `tidb_opt_insubq_to_join_and_agg` 也能决定是否开启该功能。
