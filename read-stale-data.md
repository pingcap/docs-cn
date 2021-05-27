---
title: 通过 as of timestamp 读取历史数据
aliases: ['/docs-cn/dev/read-stale-data/']
---

# 读取历史数据

本文档介绍 TiDB 如何读取历史版本数据，包括具体的操作流程以及历史数据的保存策略。

## 功能说明

TiDB 实现了通过标准 SQL 接口读取历史数据功能，无需特殊的 client 或者 driver。当数据被更新、删除后，依然可以通过 SQL 接口将更新/删除前的数据读取出来。

另外即使在更新数据之后，表结构发生了变化，TiDB 依旧能用旧的表结构将数据读取出来。

## 操作流程

为支持读取历史版本数据，TiDB 扩展了新的语法 AS OF TIMESTAMP。目前支持以下三种方式使用该语法。

- 通过 [START TRANSACTION READ ONLY AS OF TIMESTAMP](/sql-statements/sql-statement-start-transaction.md)
- 通过 [SET TRANSACTION READ ONLY AS OF TIMESTAMP](/sql-statements/sql-statement-set-transaction.md)
- 通过 SELECT 子句中使用 AS OF TIMESTAMP

AS OF TIMESTAMP 支持接收日期时间和时间函数，日期时间的格式为：“2016-10-08 16:45:26.999”，一般来说可以只写到秒，比如”2016-10-08 16:45:26”。

## 历史数据保留策略

参考[历史数据保留策略](/read-historical-data.md#历史数据保留策略)

## 示例

### 准备阶段

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
    | 2021-05-26 16:45:26 |
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

### 通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 读取历史数据

通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 开启一个基于历史时间的只读事务，该事务将会基于所提供的历史时间来读取历史数据。

    {{< copyable "sql" >}}

    ```sql
    start transaction read only as of timestamp '2021-05-26 16:45:26';
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
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    commit;
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

当事务结束后，即可读取最新数据。

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

> **注意：**
>
> 通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 开启的事务将会是一个只读事务。假如在该事务中执行写入操作，将会被该事务拒绝。

### 通过 SET TRANSACTION READ ONLY AS OF TIMESTAMP 读取历史数据

通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 表示下一个事务为基于该历史时间的只读事务，该事务将会基于所提供的历史时间来读取历史数据。

    {{< copyable "sql" >}}

    ```sql
    set transaction read only as of timestamp '2021-05-26 16:45:26';
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    begin;
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
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    commit;
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

当事务结束后，即可读取最新数据。

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

> **注意：**
>
> 通过 SET TRANSACTION READ ONLY AS OF TIMESTAMP 开启的事务将会是一个只读事务。假如在该事务中执行写入操作，将会被该事务拒绝。

### 通过 SELECT 子句中使用 AS OF TIMESTAMP 读取历史数据

通过 SELECT 子句中使用 AS OF TIMESTAMP 对当前的查询语句基于历史时间进行查询数据。

    {{< copyable "sql" >}}
    
    ```sql
    select * from t as of timestamp '2021-05-26 16:45:26';
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

## 历史数据恢复策略

参考[历史数据恢复策略](/read-historical-data.md#历史数据恢复策略)
