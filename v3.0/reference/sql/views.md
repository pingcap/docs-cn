---
title: Views
summary: Learn how to use views in TiDB.
category: reference
---

# Views

TiDB supports views. A view acts as a virtual table and its table schema is defined by the `SELECT` statement when you create the view. Using views has the following benefits:

- Exposing only safe fields and data to users to ensure security of sensitive fields and data stored in the underlying table
- Defining complex queries that frequently appear as views to make complex queries easier and more convenient

## Query views

Querying a view is similar to querying an ordinary table. However, when TiDB queries a view, it actually queries the `SELECT` statement associated with the view.

## Examples

The following example creates a view, queries this view, and delete this view:

```sql
tidb> create table t(a int, b int);
Query OK, 0 rows affected (0.01 sec)

tidb> insert into t values(1, 1),(2,2),(3,3);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

tidb> create table s(a int);
Query OK, 0 rows affected (0.01 sec)

tidb> insert into s values(2),(3);
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

tidb> create view v as select s.a from t left join s on t.a = s.a;
Query OK, 0 rows affected (0.01 sec)

tidb> select * from v;
+------+
| a    |
+------+
| NULL |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)

tidb> drop view v;
Query OK, 0 rows affected (0.02 sec)
```

## Limitations

Currently, the TiDB view has the following limitations:

- TiDB does not support materialized views.
- TiDB views are read-only and do not support write operations like `UPDATE`, `INSERT`, `DELETE` and so on.
- For created views, TiDB only support the `DROP [VIEW | TABLE]` DDL operation.

## See also

- [CREATE VIEW](/reference/sql/statements/create-view.md)
- [DROP VIEW](/reference/sql/statements/drop-view.md)
