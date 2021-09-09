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

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|    'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

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

`execution info` 信息除了基本的 `time` 和 `loop` 信息外，还包含算子特有的执行信息，主要包含了该算子发送 RPC 请求的耗时信息以及其他步骤的耗时。

### Point_Get

`Point_Get` 算子可能包含以下执行信息：

- `Get:{num_rpc:1, total_time:697.051µs}`：向 TiKV 发送 `Get` 类型的 RPC 请求的数量 (`num_rpc`) 和所有 RPC 请求的总耗时 (`total_time`)。
- `ResolveLock:{num_rpc:1, total_time:12.117495ms}`：读数据遇到锁后，进行 resolve lock 的时间。一般在读写冲突的场景下会出现。
- `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}`：RPC 请求失败后，会在等待 backoff 的时间后重试，包括了 backoff 的类型（如 regionMiss，tikvRPC），backoff 等待的总时间 (total_time) 和 backoff 的总次数 (num)。

### Batch_Point_Get

`Batch_Point_get` 算子的执行信息和 `Point_Get` 算子类似，不过 `Batch_Point_Get` 一般向 TiKV 发送 `BatchGet` 类型的 RPC 请求来读取数据。

`BatchGet:{num_rpc:2, total_time:83.13µs}`：向 TiKV 发送 `BatchGet` 类型的 RPC 请求的数量 (`num_rpc`) 和所有 RPC 请求的总耗时 (`total_time`)。

### TableReader

`TableReader` 算子可能包含以下执行信息：

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

`Insert` 算子可能包含以下执行信息：

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs}}}
```

- `prepare`：准备写入前的耗时，包括表达式，默认值相关的计算等。
- `check_insert`：这个信息一般出现在 `insert ignore` 和 `insert on duplicate` 语句中，包含冲突检查和写入 TiDB 事务缓存的耗时。注意，这个耗时不包含事务提交的耗时。具体包含以下信息：
    - `total_time`：`check_insert` 步骤的总耗时。
    - `mem_insert_time`：将数据写入 TiDB 事务缓存的耗时。
    - `prefetch`：从 TiKV 中获取需要检查冲突的数据的耗时，该步骤主要是向 TiKV 发送 `BatchGet` 类型的 RPC 请求的获取数据。
    - `rpc`：向 TiKV 发送 RPC 请求的总耗时，一般包含 `BatchGet` 和 `Get` 两种类型的 RPC 耗时，其中：
        - `BatchGet` 请求是 `prefetch` 步骤发送的 RPC 请求。
        - `Get` 请求是 `insert on duplicate` 语句在执行 `duplicate update` 时发送的 RPC 请求。
- `backoff`：包含不同类型的 backoff 以及等待总耗时。

### IndexJoin

`IndexJoin` 算子有 1 个 outer worker 和 N 个 inner worker 并行执行，其 join 结果的顺序和 outer table 的顺序一致，具体执行流程如下：

1. Outer worker 读取 N 行 outer table 的数据，然后包装成一个 task 发送给 result channel 和 inner worker channel。
2. Inner worker 从 inner worker channel 里面接收 task，然后根据 task 生成需要读取 inner table 的 key ranges 范围，然后读取相应范围的 inner table 行数据，并生成一个 inner table row 的 hash table。
3. `IndexJoin` 的主线程从 result channel 中接收 task，然后等待 inner worker 执行完这个 task。
4. `IndexJoin` 的主线程用 outer table rows 和 inner table rows 的 hash table 做 join。

`IndexJoin` 算子包含以下执行信息：

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

- `inner`：inner worker 的执行信息，具体如下：
    - `total`：inner worker 的总耗时。
    - `concurrency`：inner worker 的数量。
    - `task`：inner worker 处理 task 的总数量。
    - `construct`：inner worker 读取 task 对应的 inner table rows 之前的准备时间。
    - `fetch`：inner worker 读取 inner table rows 的总耗时。
    - `build`: inner worker 构造 inner table rows 对应的 hash table 的总耗时。
- `probe`：`IndexJoin` 主线程用 outer table rows 和 inner table rows 的 hash table 做 join 的总耗时。

### IndexHashJoin

`IndexHashJoin` 算子和 `IndexJoin` 算子执行流程类似，也有 1 个 outer worker 和 N 个 inner worker 并行执行，但是其 join 结果的顺序是不和 outer table 一致。具体执行流程如下：

1. Outer worker 读取 N 行 out table 的数据，然后包装成一个 task 发送给 inner worker channel。
2. Inner worker 从 inner worker channel 里面接收 task，然后做以下三件事情，其中步骤 a 和 b 是并行执行。
    a. 用 outer table rows 生成一个 hash table。
    b. 根据 task 生成 key 的范围后，读取 inner table 相应范围的行数据。
    c. 用 inner table rows 和 outer table rows 的 hash table 做 join，然后把 join 结果发送给 result channel。
3. `IndexHashJoin` 的主线程从 result channel 中接收 join 结果。

`IndexHashJoin` 算子包含以下执行信息：

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

- `inner`：inner worker 的执行信息，具体如下：
    - `total`：inner worker 的总耗时。
    - `concurrency`：inner worker 的数量。
    - `task`：inner worker 处理 task 的总数量。
    - `construct`：inner worker 读取 task 对应的 inner table rows 之前的准备时间。
    - `fetch`：inner worker 读取 inner table rows 的总耗时。
    - `build`: inner worker 构造 outer table rows 对应的 hash table 的总耗时。
    - `join`: inner worker 用 inner table rows 和 outer table rows 的 hash table 做 join 的总耗时。

### HashJoin

`HashJoin` 算子有一个 inner worker，一个 outer worker 和 N 个 join worker，其具体执行逻辑如下：

1. inner worker 读取 inner table rows 并构造 hash table。
2. outer worker 读取 outer table rows, 然后包装成 task 发送给 join worker。
3. 等待第 1 步的 hash table 构造完成。
4. join worker 用 task 里面的 outer table rows 和 hash table 做 join，然后把 join 结果发送给 result channel。
5. `HashJoin` 的主线程从 result channel 中接收 join 结果。

`HashJoin` 算子包含以下执行信息：

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

- `build_hash_table`: 读取 inner table 的数据并构造 hash table 的执行信息：
    - `total`：总耗时。
    - `fetch`：读取 inner table 数据的总耗时。
    - `build`：构造 hash table 的总耗时。
- `probe`: join worker 的执行信息：
    - `concurrency`：join worker 的数量。
    - `total`：所有 join worker 执行的总耗时。
    - `max`：单个 join worker 执行的最大耗时。
    - `probe`: 用 outer table rows 和 hash table 做 join 的总耗时。
    - `fetch`：join worker 等待读取 outer table rows 数据的总耗时。

### lock_keys 执行信息

在悲观事务中执行 DML 语句时，算子的执行信息还可能包含 `lock_keys` 的执行信息，示例如下：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

- `time`：执行 `lock_keys` 操作的总耗时。
- `region`：执行 `lock_keys` 操作涉及的 Region 数量。
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
- `write_byte`：事务中写入 `key-value` 的总字节数量，单位是 byte。

## MySQL 兼容性

`EXPLAIN ANALYZE` 是 MySQL 8.0 的功能，但该语句在 MySQL 中的输出格式和可能的执行计划都与 TiDB 有较大差异。

## 另请参阅

* [Understanding the Query Execution Plan](/explain-overview.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
