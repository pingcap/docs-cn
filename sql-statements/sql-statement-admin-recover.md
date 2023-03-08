---
title: ADMIN RECOVER INDEX
summary: TiDB 数据库中 ADMIN RECOVER INDEX 的使用概况。
---

# ADMIN RECOVER INDEX

`ADMIN RECOVER INDEX` 语句用于在表发生行数据和索引的一致性故障时，根据表中多余的索引，使表的行数据和索引重新恢复到一致状态。注意，该语法尚不支持外键约束。

## 语法图

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'RECOVER' 'INDEX' TableName IndexName
```

## 示例

假设由于一些原因（例如灾难恢复场景，集群中丢失了部分索引数据），数据库中的 `tbl` 表出现行数据和索引不一致现象：

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 2 isn't equal to value count 3

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

从 `SELECT` 查询的错误信息可以看到，`tbl` 表中包含 3 条行数据和 2 条索引数据，这意味着行数据与索引数据出现了不一致故障，同时至少有 1 条行数据缺少了对应的索引。此时可以使用 `ADMIN RECOVER INDEX` 语句补充缺少的索引：

```sql
ADMIN RECOVER INDEX tbl idx;
```

执行结果示例如下：

```sql
ADMIN RECOVER INDEX tbl idx;
+-------------+------------+
| ADDED_COUNT | SCAN_COUNT |
+-------------+------------+
|           1 |          3 |
+-------------+------------+
1 row in set (0.00 sec)
```

此时，可以重新使用 `ADMIN CHECK INDEX` 语句对数据索引的一致性进行检查，验证数据恢复到正常状态：

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

> **注意：**
>
> 当由于副本丢失导致数据索引出现不一致时：
>
> - 通常行数据与索引数据都有丢失，此时需要同时使用 [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) 与 `ADMIN RECOVER INDEX` 语句保证行数据与索引数据的一致性。
> - `ADMIN RECOVER INDEX` 总是单并发执行。在表数据量大时，建议通过重建索引的方式进行索引数据的恢复。
> - `ADMIN RECOVER INDEX` 在执行期间，不会为对应的表或索引记录加锁，这意味着 TiDB 允许同时有其他的会话对表记录进行更新或修改。然而，在此情况下 `ADMIN RECOVER INDEX` 可能无法正确处理所有数据。因此，在执行 `ADMIN RECOVER INDEX` 时，请避免同时修改表数据。
> - 若你使用 TiDB 企业版，此时建议[提交工单](https://support.pingcap.cn/)联系 PingCAP 支持工程师进行处理。
>
> `ADMIN RECOVER INDEX` 命令不具有原子性：若该命令在执行期间中断，建议重新执行直到成功。

## MySQL 兼容性

`ADMIN RECOVER INDEX` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
* [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)
