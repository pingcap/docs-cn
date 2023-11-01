---
title: TimeStamp Oracle
summary: 了解 TiDB 中的 TSO (TimeStamp Oracle) timestamps in TiDB.
---

在 TiDB 中，Placement Driver (PD) 在为各种集群组件分配时间戳方面发挥着关键作用。这些时间戳有助于为事务和数据分配时间标记。该机制对于在 TiDB 中启用 [Percolator](https://research.google.com/pubs/pub36726.html) 模型至关重要。Percolator 模型用于支持多版本并发控制（Multi-Version Concurrency Control, MVCC）和[事务管理](/transaction-overview.md)。

下面是 TimeStamp Oracle (TSO) 时间戳的示例：

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

注意由于 TSO 时间戳是分配给事务的，所以该时间戳是在带有 `BEGIN; ...; ROLLBACK` 的事务中生成的。

你可以使用以下 SQL 函数来查看时间戳：

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

下面示例展示了 TSO 时间戳的细节：

```shell
0000011000101000111000010001011110111000110111000000000000000100  ← 该值是二进制形式的 443852055297916932
0000011000101000111000010001011110111000110111                    ← 前 46 位是物理时间戳
                                              000000000000000100  ← 最后 18 位是逻辑时间戳
```

TSO 时间戳由两部分组成：

- 物理时间戳：自 1970 年 1 月 1 日以来的 UNIX 时间戳，单位为毫秒。
- 逻辑时间戳：递增计数器，用于需要在同一毫秒内使用多个时间戳的情况，或某些事件可能触发时钟进程逆转的情况。在这种情况下，物理时间戳保持不变，而逻辑时间戳稳步递增。该机制可以确保 TSO 时间戳的完整性，保证时间戳始终向前，不会倒退。

你可以在 SQL 中更深入地检查 TSO 时间戳，示例如下：

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

`>> 18` 操作表示按位[右移](/functions-and-operators/bit-functions-and-operators.md) 18 位，用于滤除物理时间戳。由于物理时间戳是以毫秒为单位的，与更常用的以秒为单位的 UNIX 时间戳格式不同，因此需要除以 1000 才能将其转换为与 [`FROM_UNIXTIME()`](/functions-and-operators/date-and-f-time-functions.md) 兼容的格式。这个过程基本与 `TIDB_PARSE_TSO()` 的功能一致。

你还可以将二进制中的逻辑时间戳 `000000000000000100`（即十进制中的 `4`）过滤掉。

你也可以通过 CLI 工具查看时间戳，命令如下：

```shell
$ tiup ctl:v7.1.0 pd tso 443852055297916932
system:  2023-08-27 20:33:41.687 +0200 CEST
logic:   4
```

在以 `system:` 开头的行中可以看到物理时间戳，在以 `logic:` 开头的行中可以看到逻辑时间戳。
