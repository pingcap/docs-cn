# TiDB 专用系统变量和语法

TiDB 在 MySQL 的基础上，定义了一些专用的系统变量和语法用来优化性能。

## System Variable

变量可以通过 SET 语句设置，例如

```set @@tidb_distsql_scan_concurrency = 10 ```

如果需要设值全局变量，执行

```set @@global.tidb_distsql_scan_concurrency = 10 ```

### tidb_distsql_scan_concurrency

作用域: SESSION | GLOBAL

默认值: 10

这个变量用来设置 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_lookup_size

作用域: SESSION | GLOBAL

默认值: 20000

这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_lookup_concurrency

作用域: SESSION | GLOBAL

默认值: 4

这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_serial_scan_concurrency

作用域：SESSION | GLOBAL

默认值：1

这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

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

提示优化器使用 Index Nested Loop Join 算法，这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表结果集较小（小于 1 万行）的场景，可以尝试使用。

