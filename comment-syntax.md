---
title: Comment Syntax
summary: This document introduces the comment syntax supported by TiDB.
aliases: ['/docs/dev/comment-syntax/','/docs/dev/reference/sql/language-structure/comment-syntax/']
---

# Comment Syntax

This document describes the comment syntax supported by TiDB.

TiDB supports three comment styles:

- Use `#` to comment a line:

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

- Use `--` to comment a line:

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
    
    And this style requires at least one whitespace after `--`:

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

- Use `/* */` to comment a block or multiple lines:

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

## MySQL-compatible comment syntax

The same as MySQL, TiDB supports a variant of C comment style:

```
/*! Specific code */
```

or

```
/*!50110 Specific code */
```

In this style, TiDB runs the statements in the comment.

For example:

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

In TiDB, you can also use another version:

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

If the server version number is specified in the comment, for example, `/*!50110 KEY_BLOCK_SIZE=1024 */`, in MySQL it means that the contents in this comment are processed only when the MySQL version is or higher than 5.1.10. But in TiDB, the MySQL version number does not work and all contents in the comment are processed.

## TiDB specific comment syntax

TiDB has its own comment syntax (that is, TiDB specific comment syntax), which can be divided into the following two types:

* `/*T! Specific code */`: This syntax can only be parsed and executed by TiDB, and be ignored in other databases.
* `/*T![feature_id] Specific code */`: This syntax is used to ensure compatibility between different versions of TiDB. TiDB can parse the SQL fragment in this comment only if it implements the corresponding feature of `feature_id` in the current version. For example, as the `AUTO_RANDOM` feature is introduced in v3.1.1, this version of TiDB can parse `/*T![auto_rand] auto_random */` into `auto_random`. Because the `AUTO_RANDOM` feature is not implemented in v3.0.0, the SQL statement fragment above is ignored. **Do not leave any space inside the `/*T![` characters**.

## Optimizer comment syntax

Another type of comment is specially treated as an optimizer hint:

{{< copyable "sql" >}}

```sql
SELECT /*+ hint */ FROM ...;
```

For details about the optimizer hints that TiDB supports, see [Optimizer hints](/optimizer-hints.md).

> **Note:**
>
> In MySQL client, the TiDB-specific comment syntax is treated as comments and cleared by default. In MySQL client before 5.7.7, hints are also seen as comments and are cleared by default. It is recommended to use the `--comments` option when you start the client. For example, `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

For more information, see [Comment Syntax](https://dev.mysql.com/doc/refman/8.0/en/comments.html).
