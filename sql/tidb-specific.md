---
title: TiDB 专用系统变量和语法
category: compatibility
---

# TiDB 专用系统变量和语法

TiDB 在 MySQL 的基础上，定义了一些专用的系统变量和语法用来优化性能。

## System Variable

变量可以通过 SET 语句设置，例如

```set @@tidb_distsql_scan_concurrency = 10 ```

如果需要设值全局变量，执行

```set @@global.tidb_distsql_scan_concurrency = 10 ```

### tidb_snapshot

作用域: SESSION

默认值: 空字符串

这个变量用来设置当前会话期待读取的历史数据所处时刻。
比如当设置为 "2017-11-11 20:20:20" 时或者一个 TSO 数字 "400036290571534337"，当前会话将能读取到该时刻的数据。

### tidb_import_data

作用域: SESSION

默认值: 0

这个变量用来表示当前状态是否为从 dump 文件中导入数据。
当这个变量被设置为 1 时，唯一索引约束不被检查以加速导入速度。
这个变量不对外用，只是给 lightning 使用，请用户不要自行修改。

### tidb_opt_agg_push_down

作用域: SESSION

默认值: 0

这个变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作。
当查询中聚合操作执行很慢时，可以尝试设置该变量为 1。

### tidb_opt_insubquery_unfold

作用域: SESSION

默认值: 0

这个变量用来设置优化器是否执行 in-子查询展开的优化操作。

### tidb_build_stats_concurrency

作用域: SESSION

默认值: 4

这个变量用来设置 ANALYZE 语句执行时并发度。
当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### tidb_checksum_table_concurrency

作用域: SESSION

默认值: 4

这个变量用来设置 ADMIN CHECKSUM TABLE 语句执行时扫描索引的并发度。
当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### tidb_current_ts

作用域: SESSION

默认值: 0

这个变量是一个只读变量，用来获取当前事务的时间戳。

### tidb_config

作用域: SESSION

默认值: 空字符串

这个变量是一个只读变量，用来获取当前 TiDB Server 的配置信息。

### tidb_distsql_scan_concurrency

作用域: SESSION | GLOBAL

默认值: 15

这个变量用来设置 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。
对于 AP 类应用，最大值建议不要超过所有 TiKV 节点的 CPU 核数。

### tidb_index_lookup_size

作用域: SESSION | GLOBAL

默认值: 20000

这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_lookup_concurrency

作用域: SESSION | GLOBAL

默认值: 4

这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_lookup_join_concurrency

作用域: SESSION | GLOBAL

默认值: 4

这个变量用来设置 index lookup join 算法的并发度。

### tidb_hash_join_concurrency

作用域: SESSION | GLOBAL

默认值: 5

这个变量用来设置 hash join 算法的并发度。

### tidb_index_serial_scan_concurrency

作用域：SESSION | GLOBAL

默认值：1

这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_join_batch_size

作用域：SESSION | GLOBAL

默认值：25000

这个变量用来设置 index lookup join 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_skip_utf8_check

作用域: SESSION | GLOBAL

默认值: 0

这个变量用来设置是否跳过 UTF-8 字符的验证。
验证 UTF-8 字符需要消耗一定的性能，当可以确认输入的字符串为有效的 UTF-8 字符时，可以将其设置为 1。

### tidb_batch_insert

作用域: SESSION

默认值: 0

这个变量用来设置是否自动切分插入数据。仅在 autocommit 开启时有效。
当插入大量数据时，可以将其设置为 true，这样插入数据会被自动切分为多个 batch，每个 batch 使用一个单独的事务进行插入。

### tidb_batch_delete

作用域: SESSION

默认值: 0

这个变量用来设置是否自动切分待删除的数据。仅在 autocommit 开启时有效。
当删除大量数据时，可以将其设置为 true，这样待删除数据会被自动切分为多个 batch，每个 batch 使用一个单独的事务进行删除。

### tidb_dml_batch_size

作用域: SESSION

默认值: 20000

这个变量用来设置自动切分插入/待删除数据的的 batch 大小。仅在 tidb_batch_insert 或 tidb_batch_delete 开启时有效。
需要注意的是，当单行总数据大小很大时，20k 行总数据量数据会超过单个事务大小限制。因此在这种情况下，用户应当将其设置为一个较小的值。

### tidb_max_chunk_size

作用域: SESSION | GLOBAL

默认值: 1024

这个变量用来设置执行过程中一个 chunk 最大的行数。

### tidb_mem_quota_query

作用域：SESSION

默认值：32 GB

这个变量用来设置一条查询语句的内存使用阈值。
如果一条查询语句执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_hashjoin

作用域：SESSION

默认值：32 GB

这个变量用来设置 HashJoin 算子的内存使用阈值。
如果 HashJoin 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_mergejoin

作用域：SESSION

默认值：32 GB 

这个变量用来设置 MergeJoin 算子的内存使用阈值。
如果 MergeJoin 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_sort

作用域：SESSION

默认值：32 GB 

这个变量用来设置 Sort 算子的内存使用阈值。
如果 Sort 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_topn

作用域：SESSION

默认值：32 GB 

这个变量用来设置 TopN 算子的内存使用阈值。
如果 TopN 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_indexlookupreader

作用域：SESSION

默认值：32 GB 

这个变量用来设置 IndexLookupReader 算子的内存使用阈值。

如果 IndexLookupReader 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_indexlookupjoin

作用域：SESSION

默认值：32 GB 

这个变量用来设置 IndexLookupJoin 算子的内存使用阈值。
如果 IndexLookupJoin 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_mem_quota_nestedloopapply

作用域：SESSION

默认值：32 GB 

这个变量用来设置 NestedLoopApply 算子的内存使用阈值。
如果 NestedLoopApply 算子执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。

### tidb_general_log

作用域：SERVER

默认值：0

这个变量用来设置是否在日志里记录所有的 SQL 语句。

### tidb_enable_streaming

作用域：SESSION

默认值：0

这个变量用来设置是否启用 Streaming。

### tidb_retry_limit

作用域：SESSION | GLOBAL

默认值：10

这个变量用来设置最多可重试次数, 即在一个事务执行中遇到可重试的错误(例如事务冲突、TiKV 繁忙等)时，这个事务可以被重新执行，这个变量值表明最多可重试的次数。

## Optimizer Hint

TiDB 在 MySQL 的 Optimizer Hint 语法上，增加了一些 TiDB 专有的 Hint 语法, 使用这些 Hint 的时候，TiDB 优化器会尽量使用指定的算法，在某些场景下会比默认算法更优。

由于 hint 包含在类似 `/*+ xxx */` 的 comment 里，MySQL 客户端在 5.7.7 之前，会默认把 comment 清除掉，如果需要在旧的客户端使用 hint，需要在启动客户端时加上
`--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`

### TIDB_SMJ(t1, t2)

```SELECT /*+ TIDB_SMJ(t1, t2) */ * from t1，t2 where t1.id = t2.id```

提示优化器使用 Sort Merge Join 算法，这个算法通常会占用更少的内存，但执行时间会更久。
当数据量太大，或系统内存不足时，建议尝试使用。

### TIDB_INLJ(t1, t2)

```SELECT /*+ TIDB_INLJ(t1, t2) */ * from t1，t2 where t1.id = t2.id```

提示优化器使用 Index Nested Loop Join 算法，这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。`TIDB_INLJ()`中的参数是建立查询计划时，驱动表（外表）的候选表。即`TIDB_INLJ(t1)`只会考虑使用t1作为驱动表构建查询计划。

### TIDB_HJ(t1, t2)

```SELECT /*+ TIDB_HJ(t1, t2) */ * from t1，t2 where t1.id = t2.id```
提示优化器使用 Hash Join 算法，这个算法多线程并发执行，执行速度较快，但会消耗较多内存。


## _tidb_rowid

这个是一个 TiDB 的隐藏列，代表隐式的 ROW ID 的列名，只存在于 PK 非整数或没有 PK 的表上，可以进行增减改查的操作。

SELECT 语句示例：```SELECT *, _tidb_rowid from t;```

INSERT 语句示例：```INSERT t (c, _tidb_rowid) VALUES (1, 1);```

UPDATE 语句示例：```UPDATE t SET c = c + 1 WHERE _tidb_rowid = 1;```

DELETE 语句示例：```DELETE FROM t WHERE _tidb_rowid = 1;```

## SHARD_ROW_ID_BITS

这个 TABLE OPTION 是用来设置隐式 _tidb_rowid 的分片数量的 bit 位数。

对于 PK 非整数或没有 PK 的表，TiDB 会使用一个隐式的自增 rowid，大量 INSERT 时会把数据集中写入单个 region，造成写入热点。
通过设置 SHARD_ROW_ID_BITS 可以把 rowid 打散写入多个不同的 region，缓解写入热点问题。
但是设置的过大会造成 RPC 请求数放大，增加 CPU 和网络开销。

`SHARD_ROW_ID_BITS = 4` 代表 16 个分片， `SHARD_ROW_ID_BITS = 6` 表示 64 个分片，`SHARD_ROW_ID_BITS = 0` 就是默认值 1 个分片 。

CREATE TABLE 语句示例: ```CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;```

ALTER TABLE 语句示例： ```ALTER TABLE t SHARD_ROW_ID_BITS = 4;```
