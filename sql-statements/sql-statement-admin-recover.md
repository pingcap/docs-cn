---
title: ADMIN RECOVER INDEX
summary: TiDB 数据库中 ADMIN RECOVER INDEX 的使用概览。
---

# ADMIN RECOVER INDEX

当行数据和索引数据不一致时，你可以使用 `ADMIN RECOVER INDEX` 语句基于冗余索引恢复一致性。注意，此语法目前还不支持[外键约束](/foreign-key.md)。

## 语法图

```ebnf+diagram
AdminRecoverStmt ::=
    'ADMIN' 'RECOVER' 'INDEX' TableName IndexName
```

## 示例

假设数据库中的 `tbl` 表由于某些原因（例如，在灾难恢复场景中集群中的某些行数据丢失）导致行数据和索引不一致：

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 2 isn't equal to value count 3

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

从 `SELECT` 查询的错误消息可以看出，`tbl` 表包含三行数据和两行索引数据，这意味着行数据和索引数据不一致。同时，至少有一行数据没有对应的索引。在这种情况下，你可以使用 `ADMIN RECOVER INDEX` 语句来补充缺失的索引：

```sql
ADMIN RECOVER INDEX tbl idx;
```

执行结果如下：

```sql
ADMIN RECOVER INDEX tbl idx;
+-------------+------------+
| ADDED_COUNT | SCAN_COUNT |
+-------------+------------+
|           1 |          3 |
+-------------+------------+
1 row in set (0.00 sec)
```

你可以再次执行 `ADMIN CHECK INDEX` 语句来检查数据和索引的一致性，并验证数据是否已恢复正常：

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

<CustomContent platform="tidb">

> **注意：**
>
> 当由于副本丢失导致数据和索引不一致时：
>
> - 可能同时存在行数据和索引数据的丢失。要解决此问题，请同时使用 [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) 和 `ADMIN RECOVER INDEX` 语句来恢复行数据和索引数据的一致性。
> - `ADMIN RECOVER INDEX` 语句始终以单线程执行。当表数据较大时，建议通过重建索引来恢复索引数据。
> - 执行 `ADMIN RECOVER INDEX` 语句时，相应的表或索引不会被锁定，TiDB 允许其他会话同时修改表记录。但是，在这种情况下，`ADMIN RECOVER INDEX` 可能无法正确处理所有表记录。因此，执行 `ADMIN RECOVER INDEX` 时，应避免同时修改表数据。
> - 如果你使用 TiDB 企业版，可以[提交请求](/support.md)联系支持工程师寻求帮助。
>
> `ADMIN RECOVER INDEX` 语句不是原子性的：如果语句在执行过程中被中断，建议重新执行直到成功。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 当由于副本丢失导致数据和索引不一致时：
>
> - 可能同时存在行数据和索引数据的丢失。要解决此问题，请同时使用 [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) 和 `ADMIN RECOVER INDEX` 语句来恢复行数据和索引数据的一致性。
> - `ADMIN RECOVER INDEX` 语句始终以单线程执行。当表数据较大时，建议通过重建索引来恢复索引数据。
> - 执行 `ADMIN RECOVER INDEX` 语句时，相应的表或索引不会被锁定，TiDB 允许其他会话同时修改表记录。但是，在这种情况下，`ADMIN RECOVER INDEX` 可能无法正确处理所有表记录。因此，执行 `ADMIN RECOVER INDEX` 时，应避免同时修改表数据。
> - 如果你使用 TiDB 企业版，可以[提交请求](https://tidb.support.pingcap.com/)联系支持工程师寻求帮助。
>
> `ADMIN RECOVER INDEX` 语句不是原子性的：如果语句在执行过程中被中断，建议重新执行直到成功。

</CustomContent>

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
* [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)
