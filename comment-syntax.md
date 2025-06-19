---
title: 注释语法
summary: 本文介绍 TiDB 支持的注释语法。
---

# 注释语法

本文描述 TiDB 支持的注释语法。

TiDB 支持三种注释风格：

- 使用 `#` 注释一行：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     # comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

- 使用 `--` 注释一行：

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     -- comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```
    
    这种风格要求在 `--` 后至少有一个空格：

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

- 使用 `/* */` 注释一个块或多行：

   {{< copyable "sql" >}}

    ```sql
    SELECT 1 /* this is an in-line comment */ + 1;
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
    /*> this is a
    /*> multiple-line comment
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

与 MySQL 一样，TiDB 支持 C 风格注释语法的变体：

```
/*! 特定代码 */
```

或

```
/*!50110 特定代码 */
```

在这种风格中，TiDB 会执行注释中的语句。

例如：

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

在 TiDB 中，你也可以使用另一个版本：

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

如果在注释中指定了服务器版本号，例如 `/*!50110 KEY_BLOCK_SIZE=1024 */`，在 MySQL 中这意味着只有当 MySQL 版本是或高于 5.1.10 时才处理此注释中的内容。但在 TiDB 中，MySQL 版本号不起作用，注释中的所有内容都会被处理。

## TiDB 特有的注释语法

TiDB 有自己的注释语法（即 TiDB 特有的注释语法），可以分为以下两种：

* `/*T! 特定代码 */`：这种语法只能被 TiDB 解析和执行，在其他数据库中会被忽略。
* `/*T![feature_id] 特定代码 */`：这种语法用于确保不同版本的 TiDB 之间的兼容性。TiDB 只有在当前版本实现了相应的 `feature_id` 功能时才能解析这个注释中的 SQL 片段。例如，由于 `AUTO_RANDOM` 功能是在 v3.1.1 中引入的，因此这个版本的 TiDB 可以将 `/*T![auto_rand] auto_random */` 解析为 `auto_random`。因为 v3.0.0 中没有实现 `AUTO_RANDOM` 功能，所以上述 SQL 语句片段会被忽略。**不要在 `/*T![` 字符内留有任何空格**。

## 优化器注释语法

另一种注释类型被特别处理为优化器提示：

{{< copyable "sql" >}}

```sql
SELECT /*+ hint */ FROM ...;
```

关于 TiDB 支持的优化器提示的详细信息，请参见[优化器提示](/optimizer-hints.md)。

> **注意：**
>
> 在 MySQL 客户端中，TiDB 特有的注释语法默认被视为注释并被清除。在 MySQL 5.7.7 之前的客户端中，提示也被视为注释并默认被清除。建议在启动客户端时使用 `--comments` 选项。例如，`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

更多信息，请参见 [Comment Syntax](https://dev.mysql.com/doc/refman/8.0/en/comments.html)。
