---
title: 注释语法
summary: 本文介绍 TiDB 支持的注释语法。
aliases: ['/docs-cn/dev/comment-syntax/','/docs-cn/dev/reference/sql/language-structure/comment-syntax/']
---

# 注释语法

本文档介绍 TiDB 支持的注释语法。

TiDB 支持三种注释风格：

* 用 `#` 注释一行：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     # 注释文字
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

* 用 `--` 注释一行：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     -- 注释文字
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

    用 `--` 注释时，必须要在其之后留出至少一个空格，否则注释不生效：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1--1;
    ```

    ```
    +--------+
    | 1+1--1 |
    +--------+
    |      3 |
    +--------+
    1 row in set (0.01 sec)
    ```

* 用 `/* */` 注释一块，可以注释多行：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1 /* 这是行内注释文字 */ + 1;
    ```

    ```
    +--------+
    | 1  + 1 |
    +--------+
    |      2 |
    +--------+
    1 row in set (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+
    /*
    /*> 这是一条
    /*> 多行注释
    /*> */
        1;
    ```

    ```
    +-------------------+
    | 1+

            1 |
    +-------------------+
    |                 2 |
    +-------------------+
    1 row in set (0.001 sec)
    ```

## MySQL 兼容的注释语法

TiDB 也跟 MySQL 保持一致，支持一种 C 风格注释的变体：

```
/*! Specific code */
```

或者

```
/*!50110 Specific code */
```

和 MySQL 一样，TiDB 会执行注释中的语句。

例如：`SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...`

在 TiDB 中，这种写法等价于 `SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...`

如果注释中指定了 Server 版本号，例如 `/*!50110 KEY_BLOCK_SIZE=1024 */`，在 MySQL 中表示只有 MySQL 的版本大于等于 5.1.10 才会处理这个 comment 中的内容。但是在 TiDB 中，这个 MySQL 版本号不会起作用，所有的 comment 都被会处理。

## TiDB 可执行的注释语法

TiDB 也有独立的注释语法，称为 TiDB 可执行注释语法。主要分为两种：

* `/*T! Specific code */`：该语法只能被 TiDB 解析执行，而在其他数据库中会被忽略。

* `/*T![feature_id] Specific code */`：该语法用于保证 TiDB 不同版本之间的兼容性。只有在当前版本中实现了 `feature_id` 对应的功能特性的 TiDB，才会试图解析该注释里的 SQL 片段。例如 v3.1.1 中引入了 `AUTO_RANDOM` 特性，该版本能够将 `/*T![auto_rand] auto_random */` 解析为 `auto_random`；而 v3.0.0 中没有实现 `AUTO_RANDOM` 特性，则上述 SQL 语句片段会被忽略。**注意前几个字符 `/*T![` 中，各字符之间没有任何空格**。

## 优化器注释语法

还有一种注释会被当做是优化器 Hint 特殊对待：

{{< copyable "sql" >}}

```sql
SELECT /*+ hint */ FROM ...;
```

TiDB 支持的相关优化器 hint 详见 [Optimizer Hints](/optimizer-hints.md)。

> **注意：**
>
> 在 MySQL 客户端中，TiDB 可执行注释语法会被默认当成注释被清除掉。在 MySQL 客户端 5.7.7 之前的版本中，Hint 也会被默认当成注释被清除掉。推荐在启动客户端时加上 `--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

更多细节，请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/comments.html)。
