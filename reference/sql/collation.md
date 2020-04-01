---
title: 排序规则支持
category: reference
---

# 排序规则支持

名词解释，下面的阐述中会交错使用中文或者英文，请互相对照：

* Character Set：字符集
* Collation：排序规则

collation 的语法支持和语义支持受到配置项 new_collation_enable 的影响，这里我们区分语法支持和语义支持，语法支持是指 TiDB 能够解析和设置 collation，语义支持是指 TiDB 能够在字符串比较时正确地使用 collation。如果new_collation_enable = true, 则只能设置和使用语义支持的 collation。如果 new_collation_enable = false，则能设置语法支持的 collation，语义上所有的 collation 都当成 binary collation。

# 不使用 new collation 的情况

如果没有使用 new collation， 则所有的 collation 都当成 binary collation 处理。

# \[utf8|utf8mb4\]_general_ci

在开启 new collation 后，TiDB 能够支持 utf8_general_ci 和 utf8mb4_general_ci 这两种 collation, 其排序规则与 MySQL 兼容。
使用 utf8_general_ci 或者 utf8mb4_general_ci 时， 字符串之间的比较是大小写不敏感的。

# 新 collation 与旧 collation 的区别

在旧的 collation 中，TiDB 只支持 binary collation，其他的 collation 在实现上都是 binary collation。 binary collation 是没有 padding 的，即 `"a" = "a "` 的结果为 `0`。在新的 collation 中，除了 binary collation 之外，其他的 collation 都是 padding 的，因此有 "a" = "a "。
TiDB 的 padding 与 MySQl 的 padding 有一些区别，在实现上， TiDB 采用裁剪掉尾端空格的方式，MySQL 使用的是补齐空格的方式。两种方式在绝大多数情况下是一致的，唯一的例外是尾部包含小于空格(0x20)的字符时：
`'a' < 'a\t'` 在 TiDB 中的结果为`1`， 而在 MySQL 中，其等价于`'a ' < 'a\t'`，结果为`0`。

# 表达式中 collation 的 coercibility 值

如果一个表达式涉及多个不同 collation 的子表达式时，需要对计算时用的 collation 进行推断，规则如下：
1. 显式COLLATE子句的 coercibility 值为0
2. 两个不同 collation 的字符串的 concat 结果的 coercibility 值为1
3. 列的 collation 的 coercibility 值为2
4. 系统常量（USER（）或者VERSION（）返回的字符串）的 coercibility 值为3
5. 常量的 coercibility 值为4
6. 数字或者中间变量的 coercibility 值为5
7.  `NULL` 或者由 `NULL` 派生出的表达式的 coercibility 值为6

在推断 collation 时，优先使用 coercibility 值低的表达式的 collation。如果coercibility 值相同，则按以下优先级决定 collation：

binary > utf8mb4_bin > utf8mb4_general_ci > utf8_bin > utf8_general_ci > latin1_bin > ascii_bin

如果有两个不同的 collation 的子表达式且其 coercibility 值都为0时，TiDB无法推断 collation 并报错。

# collate 子句

TiDB 支持使用 collate 子句来指定一个表达式的 collation， 并在推断 collation 时具有最高的优先级。例子如下：

{{< copyable "sql" >}}

```sql
mysql> select 'a' = 'A' collate utf8mb4_general_ci;
+--------------------------------------+
| 'a' = 'A' collate utf8mb4_general_ci |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```
