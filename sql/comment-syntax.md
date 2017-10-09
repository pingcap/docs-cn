---
title: 注释语法
category: user guide
---

# 注释语法

TiDB 支持三种注释风格：

* 用 `#` 注释一行
* 用 `--` 注释一行，用 `--` 注释必须要在其之后留出至少一个空格。
* 用 `/* */` 注释一块，可以注释多行。

例：

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

TiDB 也跟 MySQL 保持一致，支持一种 C 风格注释的变体：

```
/*! Specific code */
```

在这种格式中，TiDB 会执行注释中的语句，这个语法是为了让这些 SQL 在其他的数据库中被忽略，而在 TiDB 中被执行。

例如： `SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...`

在 TiDB 中，这种写法等价于 `SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...`

如果注释中指定了 Server 版本号，例如 `/*!50110 KEY_BLOCK_SIZE=1024 */`，在 MySQL 中表示只有 MySQL 的版本大于等于 5.1.10 才会处理这个 comment 中的内容。但是在 TiDB 中，这个版本号不会起作用，所有的 comment 都会处理。


还有一种注释会被当做是优化器 Hint 特殊对待：

```
SELECT /*+ hint */ FROM ...;
```

由于 hint 包含在类似 /*+ xxx */ 的 comment 里，MySQL 客户端在 5.7.7 之前，会默认把 comment 清除掉，如果需要在旧的客户端使用 hint，需要在启动客户端时加上 --comments 选项，例如 mysql -h 127.0.0.1 -P 4000 -uroot --comments

目前支持的 TiDB 特有的 Hint 有以下：

* TIDB_SMJ(t1, t2)

    `SELECT /*+ TIDB_SMJ(t1, t2) */ * from t1，t2 where t1.id = t2.id`

    提示优化器使用 Sort Merge Join 算法，这个算法通常会占用更少的内存，但执行时间会更久。当数据量太大，或系统内存不足时，建议尝试使用。

* TIDB_INLJ(t1, t2)

    `SELECT /*+ TIDB_INLJ(t1, t2) */ * from t1，t2 where t1.id = t2.id`

    提示优化器使用 Index Nested Loop Join 算法，这个算法可能会在某些场景更快，消耗更少系统资源，有的场景会更慢，消耗更多系统资源。对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用。TIDB_INLJ() 中的参数是建立查询计划时，驱动表（外表）的候选表。即 TIDB_INLJ(t1) 只会考虑使用 t1 作为驱动表构建查询计划。

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/comments.html)。
