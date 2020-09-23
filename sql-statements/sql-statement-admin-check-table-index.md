---
title: ADMIN CHECK [TABLE|INDEX] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN CHECK [TABLE|INDEX]

The `ADMIN CHECK [TABLE|INDEX]` statement checks for data consistency of tables and indexes.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

## Examples

To check the consistency of all the data and corresponding indexes in the `tbl_name` table, use `ADMIN CHECK TABLE`:

{{< copyable "sql" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table. If the consistency check is passed, an empty result is returned; otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table, with the data range (to be checked) specified. If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN REPAIR`](/sql-statements/sql-statement-admin.md#admin-repair-statement)