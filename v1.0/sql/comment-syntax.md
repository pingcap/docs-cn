---
title: Comment Syntax
category: user guide
---

# Comment Syntax

TiDB supports three comment styles:

- Use `#` to comment a line.
- Use `--` to comment a line, and this style requires at least one whitespace after `--`.
- Use `/* */` to comment a block or multiple lines.

Example:

```
mysql> SELECT 1+1;     # This comment continues to the end of line
+------+
| 1+1  |
+------+
|    2 |
+------+
1 row in set (0.00 sec)

mysql> SELECT 1+1;     -- This comment continues to the end of line
+------+
| 1+1  |
+------+
|    2 |
+------+
1 row in set (0.00 sec)

mysql> SELECT 1 /* this is an in-line comment */ + 1;
+--------+
| 1  + 1 |
+--------+
|      2 |
+--------+
1 row in set (0.01 sec)

mysql> SELECT 1+
    -> /*
   /*> this is a
   /*> multiple-line comment
   /*> */
    -> 1;
+-------+
| 1+

1 |
+-------+
|     2 |
+-------+
1 row in set (0.00 sec)

mysql> SELECT 1+1--1;
+--------+
| 1+1--1 |
+--------+
|      3 |
+--------+
1 row in set (0.01 sec)
```

Similar to MySQL, TiDB supports a variant of C comment style:

```
/*! Specific code */
```

In this comment style, TiDB runs the statements in the comment. The syntax is used to make these SQL statements ignored in other databases and run only in TiDB.

For example:

```
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

In TiDB, you can also use another version:

```
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

If the server version number is specified in the comment, for example, `/*!50110 KEY_BLOCK_SIZE=1024 */`, in MySQL it means that the contents in this comment is processed only when the MySQL version is or higher than 5.1.10. But in TiDB, the version number does not work and all contents in the comment are processed.  

Another type of comment is specially treated as the Hint optimizer:

```
SELECT /*+ hint */ FROM ...;
```

Since Hint is involved in comments like `/*+ xxx */`, the MySQL client clears the comment by default in versions earlier than 5.7.7. To use Hint in those earlier versions, add the `--comments` option when you start the client. For example:

```
mysql -h 127.0.0.1 -P 4000 -uroot --comments`
```

Currently, TiDB supports the following specific types of Hint:

- TIDB_SMJ(t1, t2)
  
  ```
  SELECT /*+ TIDB_SMJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
  ```
  
  The Hint optimizer uses the Sort Merge Join algorithm, which usually consumes less memory but takes longer to run. This is recommended when the amount of data is too large, or the system memory is insufficient.
  
- TIDB_INLJ(t1, t2)

  ```
  SELECT /*+ TIDB_INLJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
  ```
  
  The Hint optimizer uses the Index Nested Loop Join algorithm. This algorithm is faster in some scenarios and consumes less system resources, while it may be slower in some other scenarios and consumes more system resources. For the scenarios that have a small result set (less than 10,000 lines) after the filtration of `WHERE` condition, you can try to use it. The parameter in `TIDB_INLJ()` is the candidate table of the driving table (outer table) when the query plan is created. In other words, `TIDB_INLJ(t1)` only uses `t1` as the driving table to create the query plan.
  
For more information, see [Comment Syntax](https://dev.mysql.com/doc/refman/5.7/en/comments.html).
