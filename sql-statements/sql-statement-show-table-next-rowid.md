---
title: SHOW TABLE NEXT_ROW_ID
summary: Learn the usage of `SHOW TABLE NEXT_ROW_ID` in TiDB.
category: reference
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` can be used to show the implicitly allocated global Row ID of a table.

- For most of the tables, TiDB allocates a unique number for each record. The max allocated ID is persisted in the storage layer. Each TiDB server applies for a range of IDs on demand and caches them for ID allocation. This syntax can be used to query the next value to allocate, recorded in the storage layer. 
- For the tables with integer primary key for optimization, TiDB maps the values in the primary key column to Row ID. Thus, `SHOW TABLE NEXT_ROW_ID` is meaningless for these tables. 

## Synopsis

**ShowTableNextRowIDStmt:**

![ShowTableNextRowIDStmt](/media/sqlgram/ShowTableNextRowIDStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## Examples

{{< copyable "sql" >}}

```sql
create table t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
# For newly created tables, NEXT_GLOBAL_ROW_ID is 1 because no Row ID is allocated.
show table t next_row_id;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

```sql
insert into t values (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
show table t next_row_id;
# Data have been written to the table. The TiDB server that inserts the data allocates and caches 30000 IDs at once. Thus, NEXT_GLOBAL_ROW_ID is 30001 now.
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

`SHOW TABLE NEXT_ROW_ID` is specific to TiDB.
