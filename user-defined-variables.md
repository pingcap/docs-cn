---
title: 用户自定义变量
summary: 本文介绍 TiDB 的用户自定义变量。
---

# 用户自定义变量

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

本文介绍 TiDB 的用户自定义变量的概念，以及设置和读取用户自定义变量的方法。

用户自定义变量格式为 `@var_name`。组成 `var_name` 的字符可以是任何能够组成标识符 (identifier) 的字符，包括数字 `0-9`、字母 `a-zA-Z`、下划线 `_`、美元符号 `$` 以及 UTF-8 字符。此外，还包括英文句号 `.`。用户自定义变量是大小写不敏感的。

用户自定义变量跟 session 绑定，当前设置的用户变量只在当前连接中可见，其他客户端连接无法查看。

## 设置用户自定义变量

用 `SET` 语句可以设置用户自定义变量，语法为 `SET @var_name = expr [, @var_name = expr] ...;`。例如：

{{< copyable "sql" >}}

```sql
SET @favorite_db = 'TiDB';
```

{{< copyable "sql" >}}

```sql
SET @a = 'a', @b = 'b', @c = 'c';
```

其中赋值符号还可以使用 `:=`。例如：

{{< copyable "sql" >}}

```sql
SET @favorite_db := 'TiDB';
```

赋值符号右边的内容可以是任意合法的表达式。例如：

{{< copyable "sql" >}}

```sql
SET @c = @a + @b;
```

{{< copyable "sql" >}}

```sql
SET @c = b'1000001' + b'1000001';
```

## 读取用户自定义变量

要读取一个用户自定义变量，可以使用 `SELECT` 语句查询：

{{< copyable "sql" >}}

```sql
SELECT @a1, @a2, @a3
```

```
+------+------+------+
| @a1  | @a2  | @a3  |
+------+------+------+
|    1 |    2 |    4 |
+------+------+------+
```

还可以在 `SELECT` 语句中赋值：

```sql
SELECT @a1, @a2, @a3, @a4 := @a1+@a2+@a3;
```

```
+------+------+------+--------------------+
| @a1  | @a2  | @a3  | @a4 := @a1+@a2+@a3 |
+------+------+------+--------------------+
|    1 |    2 |    4 |                  7 |
+------+------+------+--------------------+
```

其中变量 `@a4` 在被修改或关闭连接之前，值始终为 `7`。

如果设置用户变量时用了十六进制字面量或者二进制字面量，TiDB 会把它当成二进制字符串。如果要将其设置成数字，那么可以手动加上 `CAST` 转换，或者在表达式中使用数字的运算符：

{{< copyable "sql" >}}

```sql
SET @v1 = b'1000001';
SET @v2 = b'1000001'+0;
SET @v3 = CAST(b'1000001' AS UNSIGNED);
```

{{< copyable "sql" >}}

```sql
SELECT @v1, @v2, @v3;
```

```
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    | 65   | 65   |
+------+------+------+
```

如果获取一个没有设置过的变量，会返回一个 NULL：

{{< copyable "sql" >}}

```sql
SELECT @not_exist;
```

```
+------------+
| @not_exist |
+------------+
| NULL       |
+------------+
```

除了 `SELECT` 读取用户自定义变量以外，常见的用法还有 `PREPARE` 语句，例如：

{{< copyable "sql" >}}

```sql
SET @s = 'SELECT SQRT(POW(?,2) + POW(?,2)) AS hypotenuse';
PREPARE stmt FROM @s;
SET @a = 6;
SET @b = 8;
EXECUTE stmt USING @a, @b;
```

```
+------------+
| hypotenuse |
+------------+
|         10 |
+------------+
```

用户自定义变量的内容不会在 SQL 语句中被当成标识符，例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM t;
```

```
+---+
| a |
+---+
| 1 |
+---+
```

{{< copyable "sql" >}}

```sql
SET @col = "`a`";
SELECT @col FROM t;
```

```
+------+
| @col |
+------+
| `a`  |
+------+
```

## MySQL 兼容性

除 `SELECT ... INTO <variable>` 外，MySQL 和 TiDB 支持的语法相同。

更多细节，请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/user-variables.html)。
