---
title: EXPLAIN ANALYZE | TiDB SQL 语句参考
summary: TiDB 数据库中 EXPLAIN ANALYZE 的使用概述。
---

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 语句的工作方式类似于 `EXPLAIN`，主要区别在于它会实际执行该语句。这使你可以比较查询规划中使用的估计值与执行期间遇到的实际值。如果估计值与实际值有显著差异，你应该考虑对受影响的表运行 `ANALYZE TABLE`。

> **注意：**
>
> 当你使用 `EXPLAIN ANALYZE` 执行 DML 语句时，数据修改通常会被执行。目前，DML 语句的执行计划**尚不能**显示。

## 语法

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

与 `EXPLAIN` 不同，`EXPLAIN ANALYZE` 执行相应的 SQL 语句，记录其运行时信息，并将这些信息与执行计划一起返回。因此，你可以将 `EXPLAIN ANALYZE` 视为 `EXPLAIN` 语句的扩展。与 `EXPLAIN`（用于调试查询执行）相比，`EXPLAIN ANALYZE` 的返回结果还包括 `actRows`、`execution info`、`memory` 和 `disk` 等信息列。这些列的详细信息如下：

| 属性名          | 描述 |
|:----------------|:---------------------------------|
| actRows       | 算子输出的行数。 |
| execution info  | 算子的执行信息。`time` 表示从进入算子到离开算子的总 `wall time`，包括所有子算子的总执行时间。如果该算子被父算子多次调用（在循环中），则时间指累积时间。`loops` 是当前算子被父算子调用的次数。 |
| memory  | 算子占用的内存空间。 |
| disk  | 算子占用的磁盘空间。 |

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```sql
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

```sql
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                            | operator info                  | memory    | disk |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5     | 10000.00 | 3       | root      |               | time:278.2µs, loops:2, cop_task: {num: 1, max: 437.6µs, proc_keys: 3, copr_cache_hit_ratio: 0.00}, rpc_info:{Cop:{num_rpc:1, total_time:423.9µs}}                                                                                         | data:TableFullScan_4           | 251 Bytes | N/A  |
| └─TableFullScan_4 | 10000.00 | 3       | cop[tikv] | table:t1      | tikv_task:{time:0s, loops:1}, scan_detail: {total_process_keys: 3, total_process_keys_size: 111, total_keys: 4, rocksdb: {delete_skipped_count: 0, key_skipped_count: 3, block: {cache_hit_count: 0, read_count: 0, read_byte: 0 Bytes}}} | keep order:false, stats:pseudo | N/A       | N/A  |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## 算子的执行信息

除了基本的 `time` 和 `loop` 执行信息外，`execution info` 还包含算子特定的执行信息，主要包括算子发送 RPC 请求所消耗的时间以及其他步骤的持续时间。

### Point_Get

`Point_Get` 算子的执行信息通常包含以下信息：

- `Get:{num_rpc:1, total_time:697.051µs}`：发送到 TiKV 的 `Get` RPC 请求数量（`num_rpc`）和所有 RPC 请求的总持续时间（`total_time`）。
- `ResolveLock:{num_rpc:1, total_time:12.117495ms}`：如果 TiDB 在读取数据时遇到锁，它必须先解决锁，这通常发生在读写冲突的场景中。此信息表示解决锁的持续时间。
- `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}`：当 RPC 请求失败时，TiDB 会等待回退时间后重试请求。回退统计信息包括回退类型（如 `regionMiss` 和 `tikvRPC`）、总等待时间（`total_time`）和总回退次数（`num`）。

### Batch_Point_Get

`Batch_Point_Get` 算子的执行信息与 `Point_Get` 算子类似，但 `Batch_Point_Get` 通常会发送 `BatchGet` RPC 请求到 TiKV 来读取数据。

`BatchGet:{num_rpc:2, total_time:83.13µs}`：发送到 TiKV 的 `BatchGet` 类型 RPC 请求数量（`num_rpc`）和所有 RPC 请求消耗的总时间（`total_time`）。

### TableReader

`TableReader` 算子的执行信息通常如下：

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, copr_cache_hit_ratio: 0.00}, rpc_info:{Cop:{num_rpc:6, total_time:5.313996ms}}
```

- `cop_task`：包含 `cop` 任务的执行信息。例如：
    - `num`：cop 任务的数量。
    - `max`、`min`、`avg`、`p95`：执行 cop 任务消耗的执行时间的最大值、最小值、平均值和 P95 值。
    - `max_proc_keys` 和 `p95_proc_keys`：所有 cop 任务中 TiKV 扫描的最大和 P95 键值数。如果最大值和 P95 值之间的差异很大，数据分布可能不均衡。
    - `copr_cache_hit_ratio`：`cop` 任务请求的 Coprocessor Cache 命中率。
- `rpc_info`：按请求类型聚合的发送到 TiKV 的 RPC 请求总数和总时间。
- `backoff`：包含不同类型的回退和回退的总等待时间。

### Insert

`Insert` 算子的执行信息通常如下：

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}
```

- `prepare`：准备写入的时间消耗，包括表达式、默认值和自增值的计算。
- `check_insert`：此信息通常出现在 `insert ignore` 和 `insert on duplicate` 语句中，包括冲突检查和将数据写入 TiDB 事务缓存的时间消耗。注意，这个时间消耗不包括事务提交的时间消耗。它包含以下信息：
    - `total_time`：`check_insert` 步骤花费的总时间。
    - `mem_insert_time`：将数据写入 TiDB 事务缓存的时间消耗。
    - `prefetch`：从 TiKV 获取需要检查冲突的数据的持续时间。此步骤向 TiKV 发送 `Batch_Get` RPC 请求以获取数据。
    - `rpc`：发送 RPC 请求到 TiKV 消耗的总时间，通常包括两种类型的 RPC 时间，`BatchGet` 和 `Get`，其中：
        - `BatchGet` RPC 请求在 `prefetch` 步骤中发送。
        - `Get` RPC 请求在 `insert on duplicate` 语句执行 `duplicate update` 时发送。
- `backoff`：包含不同类型的回退和回退的总等待时间。

### IndexJoin

`IndexJoin` 算子有 1 个外部工作线程和 N 个内部工作线程用于并发执行。连接结果保持外表的顺序。详细的执行过程如下：

1. 外部工作线程读取 N 个外部行，然后将其包装成任务，并发送到结果通道和内部工作线程通道。
2. 内部工作线程接收任务，从任务构建键范围，并根据键范围获取内部行。然后构建内部行哈希表。
3. 主 `IndexJoin` 线程从结果通道接收任务，并等待内部工作线程完成处理任务。
4. 主 `IndexJoin` 线程通过查找内部行哈希表来连接每个外部行。

`IndexJoin` 算子包含以下执行信息：

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

- `Inner`：内部工作线程的执行信息：
    - `total`：内部工作线程消耗的总时间。
    - `concurrency`：并发内部工作线程的数量。
    - `task`：内部工作线程处理的任务总数。
    - `construct`：内部工作线程在读取任务对应的内部表行之前的准备时间。
    - `fetch`：内部工作线程读取内部表行消耗的总时间。
    - `Build`：内部工作线程构建对应内部表行哈希表消耗的总时间。
- `probe`：主 `IndexJoin` 线程执行外表行与内部表行哈希表连接操作消耗的总时间。

### IndexHashJoin

`IndexHashJoin` 算子的执行过程类似于 `IndexJoin` 算子。`IndexHashJoin` 算子也有 1 个外部工作线程和 N 个内部工作线程并行执行，但输出顺序不保证与外表一致。详细的执行过程如下：

1. 外部工作线程读取 N 个外部行，构建任务，并发送到内部工作线程通道。
2. 内部工作线程从内部工作线程通道接收任务，并对每个任务按顺序执行以下三个操作：
   a. 从外部行构建哈希表
   b. 从外部行构建键范围并获取内部行
   c. 探测哈希表并将连接结果发送到结果通道。注意：步骤 a 和步骤 b 并行运行。
3. `IndexHashJoin` 的主线程从结果通道接收连接结果。

`IndexHashJoin` 算子包含以下执行信息：

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

- `Inner`：内部工作线程的执行信息：
    - `total`：内部工作线程消耗的总时间。
    - `concurrency`：内部工作线程的数量。
    - `task`：内部工作线程处理的任务总数。
    - `construct`：内部工作线程在读取内部表行之前的准备时间。
    - `fetch`：内部工作线程读取内部表行消耗的总时间。
    - `Build`：内部工作线程构建外表行哈希表消耗的总时间。
    - `join`：内部工作线程执行内部表行与外表行哈希表连接操作消耗的总时间。

### HashJoin

`HashJoin` 算子有一个内部工作线程、一个外部工作线程和 N 个连接工作线程。详细的执行过程如下：

1. 内部工作线程读取内部表行并构建哈希表。
2. 外部工作线程读取外部表行，然后将其包装成任务并发送给连接工作线程。
3. 连接工作线程等待步骤 1 中的哈希表构建完成。
4. 连接工作线程使用任务中的外部表行和哈希表执行连接操作，然后将连接结果发送到结果通道。
5. `HashJoin` 的主线程从结果通道接收连接结果。

`HashJoin` 算子包含以下执行信息：

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

- `build_hash_table`：读取内部表数据并构建哈希表的执行信息：
    - `total`：总时间消耗。
    - `fetch`：读取内部表数据消耗的总时间。
    - `build`：构建哈希表消耗的总时间。
- `probe`：连接工作线程的执行信息：
    - `concurrency`：连接工作线程的数量。
    - `total`：所有连接工作线程消耗的总时间。
    - `max`：单个连接工作线程执行的最长时间。
    - `probe`：与外部表行和哈希表连接消耗的总时间。
    - `fetch`：连接工作线程等待读取外部表行数据消耗的总时间。

### TableFullScan (TiFlash)

在 TiFlash 节点上执行的 `TableFullScan` 算子包含以下执行信息：

```sql
tiflash_scan: {
  dtfile: {
    total_scanned_packs: 2, 
    total_skipped_packs: 1, 
    total_scanned_rows: 16000, 
    total_skipped_rows: 8192, 
    total_rough_set_index_load_time: 2ms, 
    total_read_time: 20ms
  }, 
  total_create_snapshot_time: 1ms
}
```

+ `dtfile`：表扫描期间的 DTFile（DeltaTree File）相关信息，反映了 TiFlash Stable 层的数据扫描状态。
    - `total_scanned_packs`：DTFile 中已扫描的 pack 总数。pack 是 TiFlash DTFile 中可以读取的最小单位。默认情况下，每 8192 行构成一个 pack。
    - `total_skipped_packs`：DTFile 中扫描时跳过的 pack 总数。当 `WHERE` 子句命中粗糙集索引或匹配主键的范围过滤时，会跳过不相关的 pack。
    - `total_scanned_rows`：DTFile 中已扫描的行总数。如果由于 MVCC 存在多个版本的更新或删除，每个版本都会被独立计数。
    - `total_skipped_rows`：DTFile 中扫描时跳过的行总数。
    - `total_rs_index_load_time`：读取 DTFile 粗糙集索引使用的总时间。
    - `total_read_time`：读取 DTFile 数据使用的总时间。
+ `total_create_snapshot_time`：表扫描期间创建快照使用的总时间。

### lock_keys 执行信息

当在悲观事务中执行 DML 语句时，算子的执行信息可能还包括 `lock_keys` 的执行信息。例如：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

- `time`：执行 `lock_keys` 操作的总持续时间。
- `region`：执行 `lock_keys` 操作涉及的 Region 数量。
- `keys`：需要 `Lock` 的 `Key` 数量。
- `lock_rpc`：向 TiKV 发送 `Lock` 类型 RPC 请求消耗的总时间。因为多个 RPC 请求可以并行发送，所以总 RPC 时间消耗可能大于 `lock_keys` 操作的总时间消耗。
- `rpc_count`：向 TiKV 发送的 `Lock` 类型 RPC 请求总数。

### commit_txn 执行信息

当在 `autocommit=1` 的事务中执行写类型的 DML 语句时，写算子的执行信息还将包括事务提交的持续时间信息。例如：

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

- `prewrite`：事务 2PC 提交的 `prewrite` 阶段消耗的时间。
- `wait_prewrite_binlog`：等待写入 prewrite Binlog 消耗的时间。
- `get_commit_ts`：获取事务提交时间戳消耗的时间。
- `commit`：事务 2PC 提交的 `commit` 阶段消耗的时间。
- `write_keys`：事务中写入的总 `keys`。
- `write_byte`：事务中写入的 `key-value` 总字节数，单位为字节。

### RU（请求单元）消耗

[请求单元（Request Unit，RU）](/tidb-resource-control.md#什么是请求单元-ru)是系统资源的统一抽象单位，在 TiDB 资源控制中定义。顶层算子的 `execution info` 显示了这个特定 SQL 语句的总体 RU 消耗。

```
RU:273.842670
```

> **注意：**
>
> 这个值显示了此次执行实际消耗的 RU。由于缓存的影响（例如[协处理器缓存](/coprocessor-cache.md)），同一条 SQL 语句每次执行可能会消耗不同数量的 RU。

你可以从 `EXPLAIN ANALYZE` 中的其他值计算 RU，特别是 `execution info` 列。例如：

```json
'executeInfo':
   time:2.55ms, 
   loops:2, 
   RU:0.329460, 
   Get:{
       num_rpc:1,
       total_time:2.13ms
   }, 
   total_process_time: 231.5µs,
   total_wait_time: 732.9µs, 
   tikv_wall_time: 995.8µs,
   scan_detail: {
      total_process_keys: 1, 
      total_process_keys_size: 150, 
      total_keys: 1, 
      get_snapshot_time: 691.7µs,
      rocksdb: {
          block: {
              cache_hit_count: 2,
              read_count: 1,
              read_byte: 8.19 KB,
              read_time: 10.3µs
          }
      }
  },
```

基本成本在 [`tikv/pd` 源代码](https://github.com/tikv/pd/blob/aeb259335644d65a97285d7e62b38e7e43c6ddca/client/resource_group/controller/config.go#L58C19-L67)中定义，计算在 [`model.go`](https://github.com/tikv/pd/blob/54219d649fb4c8834cd94362a63988f3c074d33e/client/resource_group/controller/model.go#L107) 文件中执行。

如果你使用的是 TiDB v7.1，计算是 `pd/pd-client/model.go` 中 `BeforeKVRequest()` 和 `AfterKVRequest()` 的总和，即：

```
在处理键/值请求之前：
      consumption.RRU += float64(kc.ReadBaseCost) -> kv.ReadBaseCost * rpc_nums

在处理键/值请求之后：
      consumption.RRU += float64(kc.ReadBytesCost) * readBytes -> kc.ReadBytesCost * total_process_keys_size
      consumption.RRU += float64(kc.CPUMsCost) * kvCPUMs -> kc.CPUMsCost * total_process_time
```

对于写入和批量获取，计算方式类似，但基本成本不同。

### 其他常见执行信息

Coprocessor 算子通常包含两部分执行时间信息：`cop_task` 和 `tikv_task`。`cop_task` 是 TiDB 记录的时间，从发送请求到服务器到接收响应的时刻。`tikv_task` 是 TiKV Coprocessor 自身记录的时间。如果两者之间存在较大差异，可能表明等待响应的时间太长，或者 gRPC 或网络消耗的时间太长。

## MySQL 兼容性

`EXPLAIN ANALYZE` 是 MySQL 8.0 的特性，但 TiDB 中的输出格式和潜在的执行计划与 MySQL 有很大不同。

## 另请参阅

* [理解查询执行计划](/explain-overview.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
