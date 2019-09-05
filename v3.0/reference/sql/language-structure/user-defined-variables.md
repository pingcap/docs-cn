---
title: 用户自定义变量
category: reference
aliases: ['/docs-cn/sql/user-defined-variables/']
---

# 用户自定义变量

用户自定义变量格式为 `@var_name`。`var_name` 目前只支持字母，数字，`_$`组成。用户自定义变量是大小写不敏感的。

用户自定义变量是跟 session 绑定的，也就是说只有当前连接可以看见设置的用户变量，其他客户端连接无法查看到。

用 `SET` 语句可以设置用户自定义变量：

```sql
SET @var_name = expr [, @var_name = expr] ...
或
SET @var_name := expr
```

对于 `SET` 语句，赋值操作符可以是 `=` 也可以是 `:=`

例：

```sql
mysql> SET @a1=1, @a2=2, @a3:=4;
mysql> SELECT @a1, @a2, @t3, @a4 := @a1+@a2+@a3;
+------+------+------+--------------------+
| @a1  | @a2  | @a3  | @a4 := @a1+@a2+@a3 |
+------+------+------+--------------------+
|    1 |    2 |    4 |                  7 |
+------+------+------+--------------------+
```

如果设置用户变量用了 `HEX` 或者 `BIT` 值，TiDB会把它当成二进制字符串。如果你要将其设置成数字，那么需要手动加上 `CAST转换`: `CAST(.. AS UNSIGNED)`：

```sql
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    | 65   | 65   |
+------+------+------+
1 row in set (0.00 sec)

mysql> SET @v1 = b'1000001';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @v2 = b'1000001'+0;
Query OK, 0 rows affected (0.00 sec)

mysql> SET @v3 = CAST(b'1000001' AS UNSIGNED);
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    | 65   | 65   |
+------+------+------+
1 row in set (0.00 sec)
```

如果获取一个没有设置过的变量，会返回一个 NULL：

```sql
mysql> select @not_exist;
+------------+
| @not_exist |
+------------+
| NULL       |
+------------+
1 row in set (0.00 sec)
```

用户自定义变量不能直接在 SQL 语句中被当成 identifier，例：

```sql
mysql> select * from t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> SET @col = "a";
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| a    |
+------+
1 row in set (0.00 sec)

mysql> SELECT `@col` FROM t;
ERROR 1054 (42S22): Unknown column '@col' in 'field list'

mysql> SET @col = "`a`";
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| `a`  |
+------+
1 row in set (0.01 sec)
```

但是有一个例外是如果你在 PREPARE 语句中使用它，是可以的：

```sql
mysql> PREPARE stmt FROM "SELECT @c FROM t";
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE stmt;
+------+
| @c   |
+------+
| a    |
+------+
1 row in set (0.01 sec)

mysql> DEALLOCATE PREPARE stmt;
Query OK, 0 rows affected (0.00 sec)
```

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/user-variables.html)。