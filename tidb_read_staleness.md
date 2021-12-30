---
title: 通过系统变量 tidb_read_staleness 读取历史数据
summary: 了解如何通过系统变量 tidb_read_staleness 读取历史数据。
---

# 通过系统变量 tidb_read_staleness 读取历史数据

本文档介绍如何通过系统变量 `tidb_read_staleness` 读取历史数据，包括具体的操作流程以及历史数据的保存策略。

## 操作流程

为支持读取历史版本数据，TiDB 引入了一个新的系统变量 [`tidb_read_staleness`](/system-variables.md#tidb_read_staleness)：

- 这个变量的作用域为 `SESSION`。
- 你可以通过标准的 `SET` 语句修改这个变量的值。
- 这个变量的数据类型为 int 类型，代表了 TiDB 会从变量值秒前到当前时间范围内选择中选出一个合适的时间戳，TiDB 会在保证 TiKV 拥有对应版本的数据的同时选择尽量新的时间戳。
- 当这个变量被设置时，TiDB 会根据所设置的值找到一个最合适的时间戳，随后所有的 SELECT 操作都会依据这个时间戳来读取数据。

当读取历史版本操作结束后，可以结束当前 Session 或者是通过 `SET` 语句将 tidb_read_staleness 变量的值设为 ""，即可读取最新版本的数据。

> **注意：**
> 
> 当开启 tidb_read_staleness 以后，你仍可以在当前会话进行插入、修改、删除数据，或者进行 DML 操作，这些语句不会受到 tidb_read_staleness 的影响。
>
> 同时，开启 tidb_read_staleness 以后，你仍可以在当前会话开启交互式事务，在该事务内的查询依旧是以最新版本进行读取数据。

## 示例

1. 初始化阶段，创建一个表，并插入几行数据：

    {{< copyable "sql" >}}

    ```sql
    create table t (c int);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    insert into t values (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查看表中的数据：

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. 查看当前时间：

    {{< copyable "sql" >}}

    ```sql
    select now();
    ```

    ```
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4. 更新某一行数据：

    {{< copyable "sql" >}}

    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

5. 确认数据已经被更新：

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6. 设置一个特殊的环境变量，这个是一个 session scope 的变量，其意义为读取这个时间之前的最新的一个版本。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    > - 这里的设置的是指读取从 5 秒前到现在的时间范围内选择一个合适的时间戳作为历史数据读取的时间戳。
    > - 在 `tidb_read_staleness` 前须使用 `@@` 而非 `@`，因为 `@@` 表示系统变量，`@` 表示用户变量。

    这里读取到的内容即为 update 之前的内容，也就是历史版本：

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

7. 清空这个变量后，即可读取最新版本数据：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```
