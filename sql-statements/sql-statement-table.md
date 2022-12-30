---
title: TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of TABLE for the TiDB database.
---

# TABLE

The `TABLE` statement can be used instead of `SELECT * FROM` when no aggregation or complex filtering is needed.

## Synopsis

```ebnf+diagram
TableStmt ::=
    "TABLE" Table ( "ORDER BY" Column )? ( "LIMIT" NUM )?
```

## Examples

Create table `t1`:

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

Insert some data into `t1`:

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

View the data in table `t1`:

```sql
TABLE t1;
```

```sql
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.01 sec)
```

Query `t1` and sort the result by the `id` field in descending order:

```sql
TABLE t1 ORDER BY id DESC;
```

```sql
+----+
| id |
+----+
|  3 |
|  2 |
|  1 |
+----+
3 rows in set (0.01 sec)
```

Query the first record in `t1`:

```sql
TABLE t1 LIMIT 1;
```

```sql
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

## MySQL compatibility

The `TABLE` statement was introduced in MySQL 8.0.19.

## See also

- [`SELECT`](/sql-statements/sql-statement-select.md)
- [`TABLE` statements in MySQL](https://dev.mysql.com/doc/refman/8.0/en/table.html)
