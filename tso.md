---
title: TiDB 中的时间戳预分配器 (TSO)
summary: 了解 TiDB 中的时间戳预分配器 (TSO)。
---

# TiDB 中的时间戳预分配器 (TSO)

在 TiDB 中，Placement Driver (PD) 在为集群内各个组件分配时间戳方面发挥着关键作用。这些时间戳对于为事务和数据分配时间标记至关重要，这种机制对于在 TiDB 中实现 [Percolator](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/) 模型非常重要。Percolator 模型用于支持[多版本并发控制 (MVCC)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 和[事务管理](/transaction-overview.md)。

以下示例展示了如何在 TiDB 中获取当前的 TSO：

```sql
BEGIN; SET @ts := @@tidb_current_ts; ROLLBACK;
Query OK, 0 rows affected (0.0007 sec)
Query OK, 0 rows affected (0.0002 sec)
Query OK, 0 rows affected (0.0001 sec)

SELECT @ts;
+--------------------+
| @ts                |
+--------------------+
| 443852055297916932 |
+--------------------+
1 row in set (0.00 sec)
```

注意，这是在事务中使用 `BEGIN; ...; ROLLBACK` 完成的，因为 TSO 时间戳是按事务分配的。

从上述示例中获得的 TSO 时间戳是一个十进制数。你可以使用以下 SQL 函数来解析时间戳：

- [`TIDB_PARSE_TSO()`](/functions-and-operators/tidb-functions.md#tidb_parse_tso)
- [`TIDB_PARSE_TSO_LOGICAL()`](/functions-and-operators/tidb-functions.md)

```sql
SELECT TIDB_PARSE_TSO(443852055297916932);
+------------------------------------+
| TIDB_PARSE_TSO(443852055297916932) |
+------------------------------------+
| 2023-08-27 20:33:41.687000         |
+------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(443852055297916932);
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(443852055297916932) |
+--------------------------------------------+
|                                          4 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

以下示例展示了 TSO 时间戳在二进制中的样子：

```shell
0000011000101000111000010001011110111000110111000000000000000100  ← 这是 443852055297916932 的二进制表示
0000011000101000111000010001011110111000110111                    ← 前 46 位是物理时间戳
                                              000000000000000100  ← 后 18 位是逻辑时间戳
```

TSO 时间戳包含两个部分：

- 物理时间戳：自 1970 年 1 月 1 日以来的 UNIX 时间戳（以毫秒为单位）。
- 逻辑时间戳：一个递增计数器，用于在同一毫秒内需要多个时间戳的场景，或在某些事件可能导致时钟回退的情况下。在这些情况下，物理时间戳保持不变，而逻辑时间戳稳步前进。这种机制确保了 TSO 时间戳始终向前移动，永不回退。

有了这些知识，你可以在 SQL 中更深入地检查 TSO 时间戳：

```sql
SELECT @ts, UNIX_TIMESTAMP(NOW(6)), (@ts >> 18)/1000, FROM_UNIXTIME((@ts >> 18)/1000), NOW(6), @ts & 0x3FFFF\G
*************************** 1. row ***************************
                            @ts: 443852055297916932
         UNIX_TIMESTAMP(NOW(6)): 1693161835.502954
               (@ts >> 18)/1000: 1693161221.6870
FROM_UNIXTIME((@ts >> 18)/1000): 2023-08-27 20:33:41.6870
                         NOW(6): 2023-08-27 20:43:55.502954
                  @ts & 0x3FFFF: 4
1 row in set (0.00 sec)
```

`>> 18` 操作表示[右移](/functions-and-operators/bit-functions-and-operators.md#-right-shift) 18 位，用于提取物理时间戳。由于物理时间戳以毫秒为单位表示，与更常见的以秒为单位的 UNIX 时间戳格式不同，你需要将其除以 1000 以转换为与 [`FROM_UNIXTIME()`](/functions-and-operators/date-and-time-functions.md) 兼容的格式。这个过程与 `TIDB_PARSE_TSO()` 的功能一致。

你还可以提取逻辑时间戳 `000000000000000100`（二进制），它等于十进制的 `4`。

你也可以通过 CLI 工具解析时间戳，如下所示：

```shell
$ tiup ctl:v7.1.0 pd tso 443852055297916932
```

```
system:  2023-08-27 20:33:41.687 +0200 CEST
logic:   4
```

在这里，你可以看到以 `system:` 开头的行中的物理时间戳，以及以 `logic:` 开头的行中的逻辑时间戳。
