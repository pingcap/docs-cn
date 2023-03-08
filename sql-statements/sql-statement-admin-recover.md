---
title: ADMIN RECOVER INDEX
summary: An overview of the usage of ADMIN RECOVER INDEX for the TiDB database.
---

# ADMIN RECOVER INDEX

When the row data and index data are inconsistent, you can use the `ADMIN RECOVER INDEX` statement to recover the consistency based on the redundant indexes. Note that this syntax does not support [foreign key constraints](/foreign-key.md) yet.

## Synopsis

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'RECOVER' 'INDEX' TableName IndexName
```

## Examples

Assume that the `tbl` table in a database has inconsistent row data and index due to some reasons (for example, some row data is lost in the cluster in a disaster recovery scenario):

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 2 isn't equal to value count 3

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

It can be seen from the error message of the `SELECT` query that, the `tbl` table contains three rows of data and two rows of index data, which means inconsistent row data and index data. At the same time, at least one row of data has no corresponding index. In this case, you can use the `ADMIN RECOVER INDEX` statement to supplement the missing index:

```sql
ADMIN RECOVER INDEX tbl idx;
```

The execution result is as follows:

```sql
ADMIN RECOVER INDEX tbl idx;
+-------------+------------+
| ADDED_COUNT | SCAN_COUNT |
+-------------+------------+
|           1 |          3 |
+-------------+------------+
1 row in set (0.00 sec)
```

You can execute the `ADMIN CHECK INDEX` statement again to check the consistency of data and index, and verify whether the data has been restored to normal state:

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

> **Note:**
>
> When the data and index are inconsistent due to the loss of replicas:
>
> - There might be a loss of both row data and index data. To address the issue, use the [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) and `ADMIN RECOVER INDEX` statements together to recover the consistency of row data and index data.
> - The `ADMIN RECOVER INDEX` statement is always executed in a single thread. When the table data is large, it is recommended to recover the index data by rebuilding the index.
> - When you execute the `ADMIN RECOVER INDEX` statement, the corresponding table or index is not locked and TiDB allows other sessions to modify the table records at the same time. However, in this case, `ADMIN RECOVER INDEX` might not be able to handle all table records correctly. Therefore, when you execute `ADMIN RECOVER INDEX`, avoid modifying the table data at the same time.
> - If you use the enterprise edition of TiDB, you can [submit a request](https://support.pingcap.com/hc/en-us) to contact the support engineer for help.
>
> The `ADMIN RECOVER INDEX` statement is not atomic: if the statement is interrupted during execution, it is recommended to execute it again until it succeeds.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
* [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)
