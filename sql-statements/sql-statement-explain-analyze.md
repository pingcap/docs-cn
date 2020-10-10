---
title: EXPLAIN ANALYZE
summary: TiDB 数据库中 EXPLAIN ANALYZE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-explain-analyze/','/docs-cn/dev/reference/sql/statements/explain-analyze/']
---

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 语句的工作方式类似于 `EXPLAIN`，主要区别在于前者实际上会执行语句。这样可以将查询计划中的估计值与执行时所遇到的实际值进行比较。如果估计值与实际值显著不同，那么应考虑在受影响的表上运行 `ANALYZE TABLE`。

> **注意：**
>
> 在使用 `EXPLAIN ANALYZE` 执行 DML 语句时，数据的修改操作会被正常执行。但目前 DML 语句还无法展示执行计划。

## 语法图

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## EXPLAIN ANALYZE 输出格式

和 `EXPLAIN` 不同，`EXPLAIN ANALYZE` 会执行对应的 SQL 语句，记录其运行时信息，和执行计划一并返回出来。因此，可以将 `EXPLAIN ANALYZE` 视为 `EXPLAIN` 语句的扩展。`EXPLAIN ANALYZE` 语句的返回结果相比 `EXPLAIN`，增加了 `actRows`，`execution info`，`memory`，`disk` 这几列信息：

| 属性名          | 含义 |
|:----------------|:---------------------------------|
| actRows       | 算子实际输出的数据条数。 |
| execution info  | 算子的实际执行信息。time 表示从进入算子到离开算子的全部 wall time，包括所有子算子操作的全部执行时间。如果该算子被父算子多次调用 (loops)，这个时间就是累积的时间。loops 是当前算子被父算子调用的次数。 |
| memory  | 算子占用内存空间的大小。 |
| disk  | 算子占用磁盘空间的大小。 |

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object | execution info                                                 | operator info | memory | disk |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t1      | time:757.205µs, loops:2, Get:{num_rpc:1, total_time:697.051µs} | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                | estRows | actRows | task      | access object | execution info                                                                                                                                                                                                  | operator info                  | memory    | disk |
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5     | 13.00   | 13      | root      |               | time:923.459µs, loops:2, cop_task: {num: 4, max: 839.788µs, min: 779.374µs, avg: 810.926µs, p95: 839.788µs, max_proc_keys: 12, p95_proc_keys: 12, rpc_num: 4, rpc_time: 3.116964ms, copr_cache_hit_ratio: 0.00} | data:TableFullScan_4           | 632 Bytes | N/A  |
| └─TableFullScan_4 | 13.00   | 13      | cop[tikv] | table:t1      | proc max:0s, min:0s, p80:0s, p95:0s, iters:4, tasks:4                                                                                                                                                           | keep order:false, stats:pseudo | N/A       | N/A  |
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## 算子执行信息介绍

`execution info` 信息还包含算子特有的执行信息，主要包含了该算子发送 RPC 的耗时信息以及其他步骤的耗时。下面根据不同的算子分别介绍。

### Point_Get

Pint_get 算子可能包含以下执行信息：

- `Get:{num_rpc:1, total_time:697.051µs}`：向 TiKV 发送 `Get` 类型的 RPC 请求的数量（num_rpc）和所有 RPC 请求的总耗时（total_time）。
- `ResolveLock:{num_rpc:22076, total_time:124.644857ms}`：读数据遇到锁后，进行 resolve lock 的时间。一般在读写冲突的场景下会出现。
- `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}`：发送 RPC 请求失败后会等待 backoff 的时间后重试，包括了 backoff 的类型（如 regionMiss，tikvRPC），backoff 等待的总时间(total_time) 和 backoff 的总次数(num)。

### Batch_Point_Get

Batch_Pint_get 算子的执行信息和 Pint_get 算子类似，不过 Batch_Pint_get 一般向 TiKV 发送 `BatchGet` 类型的 RPC 请求来读取数据。

- `BatchGet:{num_rpc:2, total_time:83.13µs}`：向 TiKV 发送 `BatchGet` 类型的 RPC 请求的数量（num_rpc）和所有 RPC 请求的总耗时（total_time）。

### TableReader

TableReader 算子可能包含以下执行信息：

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996ms, copr_cache_hit_ratio: 0.00}
```

- `cop_task`：包含 cop task 的相关信息，如：
    - `num`：cop task 的数量
    - `max`,`min`,`avg`,`p95`：所有 cop task 中执行时间的最大值，最小值，平均值和 P95 值。
    - `max_proc_keys`, `p95_proc_keys`：所有 cop task 中 tikv 扫描 kv 数据的最大值，P95 值，如果 max 和 p95 的值差距很大，说明数据分布不太均匀。
    - `rpc_num`, `rpc_time`：向 TiKV 发送 `Cop` 类型的 RPC 请求总数量和总时间。
    - `copr_cache_hit_ratio`：cop task 请求的 Coprocessor Cache 缓存命中率。[Coprocessor Cache 配置](/tidb-configuration-file.md)。
- `backoff`：包含不同类型的 backoff 以及等待总耗时。

### Insert

Insert 算子可能包含以下执行信息：

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs}}}
```

- `prepare`：准备写入前的耗时，包括表达式，默认值相关的计算等。
- `check_insert`：这个信息一般出现在 `insert ignore` 和 `insert on duplicate` 语句中，包含冲突检查和写入 TiDB 内存的耗时。注意，这个耗时不包含事务提交的耗时。具体包含以下信息：
    - `total_time`：`check_insert` 步骤的总耗时。
    - `mem_insert_time`：将数据写入 TiDB 事务缓存的耗时。
    - `prefetch`：从 TiKV 中获取需要检查冲突的数据的耗时，该步骤主要是向 TiKV 发送 `BatchGet` 类型的 RPC 请求的获取数据。
    - `rpc`：向 TiKV 发送 RPC 请求的总耗时，一般包含 `BatchGet` 和 `Get` 两种类型的 RPC 耗时，其中：
        - `BatchGet` 请求是 `prefetch` 步骤发送的 RPC 请求。
        - `Get` 请求是 `insert on duplicate` 语句在执行 `duplicate update` 时发送的 RPC 请求。
- `backoff`：包含不同类型的 backoff 以及等待总耗时。

### lock_keys 执行信息

在悲观事务中执行 DML 语句时，算子的执行信息还可能包含 `lock_keys` 的执行信息，示例如下：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

- `time`：执行 `lock_keys` 操作的总耗时。
- `region`：执行 `lock_keys` 操作涉及的 region 数量。
- `keys`：需要 `Lock` 的 `Key` 的数量。
- `lock_rpc`：向 TiKV 发送 `Lock` 类型的 RPC 总耗时。因为可以并行发送多个 RPC 请求，所以总 RPC 耗时可能比 `lock_keys` 操作总耗时大。
- `rpc_count`：向 TiKV 发送 `Lock` 类型的 RPC 总数量。

### commit_txn 执行信息

在 `autocommit=1` 的事务中执行写入类型的 DML 语句时，算子的执行信息还会包括事务提交的耗时信息，示例如下：

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

- `prewrite`：事务 2PC 提交阶段中 `prewrite` 阶段的耗时。
- `wait_prewrite_binlog:`：等待写 prewrite Binlog 的耗时。
- `get_commit_ts`：获取事务提交时间戳的耗时。
- `commit`：事务 2PC 提交阶段中，`commit` 阶段的耗时。
- `write_keys`：事务中写入 `key` 的数量。
- `write_byte`：事务中写入 `key/value` 的总字节数量，单位是 byte。

## MySQL 兼容性

`EXPLAIN ANALYZE` 是 MySQL 8.0 的功能，但该语句在 MySQL 中的输出格式和可能的执行计划都与 TiDB 有较大差异。

## 另请参阅

* [Understanding the Query Execution Plan](/query-execution-plan.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
