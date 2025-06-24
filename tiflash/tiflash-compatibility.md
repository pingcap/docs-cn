---
title: TiFlash 兼容性说明
summary: 了解与 TiFlash 不兼容的 TiDB 功能。
---

# TiFlash 兼容性说明

TiFlash 在以下情况下与 TiDB 不兼容：

* 在 TiFlash 计算层：
    * 不支持检查数值溢出。例如，对两个 `BIGINT` 类型的最大值进行相加 `9223372036854775807 + 9223372036854775807`。在 TiDB 中，此计算的预期行为是返回 `ERROR 1690 (22003): BIGINT value is out of range` 错误。但是，如果在 TiFlash 中执行此计算，则会返回溢出值 `-2` 而不会报错。
    * 不支持窗口函数。
    * 不支持从 TiKV 读取数据。
    * 目前，TiFlash 中的 `sum` 函数不支持字符串类型参数。但是 TiDB 在编译期间无法识别是否有字符串类型参数传入 `sum` 函数。因此，当您执行类似 `select sum(string_col) from t` 的语句时，TiFlash 会返回 `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.` 错误。要避免这种情况下的错误，您需要将此 SQL 语句修改为 `select sum(cast(string_col as double)) from t`。
    * 目前，TiFlash 的 decimal 除法计算与 TiDB 不兼容。例如，在进行 decimal 除法时，TiFlash 始终使用从编译推断出的类型进行计算。但是，TiDB 使用比编译推断出的类型更精确的类型进行计算。因此，一些涉及 decimal 除法的 SQL 语句在 TiDB + TiKV 和 TiDB + TiFlash 中执行时会返回不同的结果。例如：

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

        在上面的示例中，`a/b` 在 TiDB 和 TiFlash 中从编译推断出的类型都是 `Decimal(7,4)`。受 `Decimal(7,4)` 约束，`a/b` 的返回类型应该是 `0.0000`。在 TiDB 中，`a/b` 的运行时精度高于 `Decimal(7,4)`，因此原始表数据不会被 `where a/b` 条件过滤。但是，在 TiFlash 中，`a/b` 的计算使用 `Decimal(7,4)` 作为结果类型，因此原始表数据会被 `where a/b` 条件过滤。
