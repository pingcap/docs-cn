---
title: TimeStamp Oracle (TSO) in TiDB
summary: Learn about TimeStamp Oracle (TSO) in TiDB.
---

# TimeStamp Oracle (TSO) in TiDB

In TiDB, the Placement Driver (PD) plays a pivotal role in allocating timestamps to various components within a cluster. These timestamps are instrumental in the assignment of temporal markers to transactions and data, a mechanism crucial for enabling the [Percolator](https://research.google.com/pubs/pub36726.html) model within TiDB. The Percolator model is used to support Multi-Version Concurrency Control (MVCC) and [transaction management](/transaction-overview.md).

The following example shows how to get the current TSO in TiDB:

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

Note that this is done in a transaction with `BEGIN; ...; ROLLBACK` because TSO timestamps are assigned per transaction.

The TSO timestamp you get from the preceding example is a decimal number. You can use the following SQL functions to parse the timestamp:

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

The following example shows what a TSO timestamp looks like in binary:

```shell
0000011000101000111000010001011110111000110111000000000000000100  ← This is 443852055297916932 in binary
0000011000101000111000010001011110111000110111                    ← The first 46 bits are the physical timestamp
                                              000000000000000100  ← The last 18 bits are the logical timestamp
```

There are two parts in a TSO timestamp:

- The physical timestamp: a UNIX timestamp in milliseconds since 1 January 1970.
- The logical timestamp: an incrementing counter, used in scenarios requiring multiple timestamps within the same millisecond, or in cases where certain events might trigger a reversal of the clock's progression. In such cases, the physical timestamp remains unchanged while the logical timestamp steadily advances. This mechanism ensures the integrity of the TSO timestamp, which always moves forward and never regresses.

With this knowledge, you can inspect the TSO timestamp a bit more in SQL:

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

The `>> 18` operation signifies a bitwise [right shift](/functions-and-operators/bit-functions-and-operators.md) by 18 bits, which is used to extract the physical timestamp. Because the physical timestamp is expressed in milliseconds, deviating from the more common UNIX timestamp format measured in seconds, you need to divide it by 1000 to convert it into a format compatible with [`FROM_UNIXTIME()`](/functions-and-operators/date-and-time-functions.md). This process aligns with the functionality of `TIDB_PARSE_TSO()`.

You can also extract the logical timestamp `000000000000000100` in binary, which is equivalent to `4` in decimal.

You can also parse the timestamp via the CLI tool as follows:

```shell
$ tiup ctl:v7.1.0 pd tso 443852055297916932
```

```
system:  2023-08-27 20:33:41.687 +0200 CEST
logic:   4
```

Here you can see the physical timestamp in the line that starts with `system:` and the logical timestamp in the line that starts with `logic:`.
