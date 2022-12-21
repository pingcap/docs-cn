---
title: TiFlash 兼容性说明
summary: 了解与 TiFlash 不兼容的 TiDB 特性。
---

# TiFlash 兼容性说明

TiFlash 在以下情况与 TiDB 存在不兼容问题：

* TiFlash 计算层：
    * 不支持检查溢出的数值。例如将两个 `BIGINT` 类型的最大值相加 `9223372036854775807 + 9223372036854775807`，该计算在 TiDB 中预期的行为是返回错误 `ERROR 1690 (22003): BIGINT value is out of range`，但如果该计算在 TiFlash 中进行，则会得到溢出的结果 `-2` 且无报错。
    * 不支持从 TiKV 读取数据。
    * 目前 TiFlash 中的 `sum` 函数不支持传入字符串类型的参数，但 TiDB 在编译时无法检测出这种情况。所以当执行类似于 `select sum(string_col) from t` 的语句时，TiFlash 会报错 `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`。要避免这类报错，需要手动把 SQL 改写成 `select sum(cast(string_col as double)) from t`。
    * TiFlash 目前的 Decimal 除法计算和 TiDB 存在不兼容的情况。例如在进行 Decimal 相除的时候，TiFlash 会始终按照编译时推断出来的类型进行计算，而 TiDB 则在计算过程中采用精度高于编译时推断出来的类型。这导致在一些带有 Decimal 除法的 SQL 语句在 TiDB + TiKV 上的执行结果会和 TiDB + TiFlash 上的执行结果不一样，示例如下：

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)

        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)

        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)

        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)

        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)

        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)

        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        以上示例中，在 TiDB 和 TiFlash 中，`a/b` 在编译期推导出来的类型都为 `Decimal(7,4)`，而在 `Decimal(7,4)` 的约束下，`a/b` 返回的结果应该为 `0.0000`。但是在 TiDB 中，`a/b` 运行期的精度比 `Decimal(7,4)` 高，所以原表中的数据没有被 `where a/b` 过滤掉。而在 TiFlash 中 `a/b` 在运行期也是采用 `Decimal(7,4)` 作为结果类型，所以原表中的数据被 `where a/b` 过滤掉了。
