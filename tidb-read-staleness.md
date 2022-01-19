---
title: 通过系统变量 `tidb_read_staleness` 读取历史数据
summary: 了解如何通过系统变量 `tidb_read_staleness` 读取历史数据。
---

# 通过系统变量 `tidb_read_staleness` 读取历史数据

为支持读取历史版本数据，TiDB 从 5.4 版本起引入了一个新的系统变量 `tidb_read_staleness`。本文档介绍如何通过该系统变量读取历史数据，其中包括具体的操作流程。

## 功能介绍

系统变量 `tidb_read_staleness` 用于设置当前会话允许读取的历史数据范围，其数据类型为 int，作用域为 `SESSION`。设置该变量后，TiDB 会从参数允许的范围内选出一个尽可能新的时间戳，并影响后继的所有读操作。比如，如果该变量的值设置为 `-5`，TiDB 会在 5 秒时间范围内，保证 TiKV 拥有对应历史版本数据的情况下，选择尽可能新的一个时间戳。

开启 `tidb_read_staleness` 后，你仍可以进行以下操作：

- 在当前会话中插入、修改、删除数据或进行 DML 操作。这些语句不会受到 `tidb_read_staleness` 的影响。
- 在当前会话开启交互式事务。在该事务内的查询依旧是读取最新版本的数据。

完成对历史版本数据的读取后，你可以通过以下两种方式来读取最新版本的数据。

- 结束当前会话。
- 使用 `SET` 语句，把 `tidb_read_staleness` 变量的值设为 `""`。

## 示例

本节通过具体操作示例介绍系统变量 `tidb_read_staleness`的使用方法。

1. 初始化阶段。创建一个表后，在表中插入几行数据：

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

3. 更新某一行数据：

    {{< copyable "sql" >}}

    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

4. 确认数据已经被更新：

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

5. 设置一个特殊的环境变量 `tidb_read_staleness`。

    该变量的作用域为 `SESSION`，设置变量值后，TiDB 会读取变量值时间之前的最新一个版本的数据。

    以下设置表示 TiDB 会从 5 秒前至现在的时间范围内选择一个尽可能新的时间戳，将其用作为历史数据读取的时间戳：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    > 必须在 `tidb_read_staleness` 前使用 `@@`，而非 `@`。因为 `@@` 表示系统变量，`@` 则表示用户变量。
    > 你需要根据第 3 步到第 4 步所花费的时间，来设定你要读取的历史时间范围，即 `tidb_read_staleness` 的值。否则，查询结果中显示的会是最新数据，而非历史数据。因此，请根据自己的实际操作情况调整该时间范围。比如，在本示例中，由于设定的时间范围是 5 秒，你需要在 5 秒内完成第 3 步和第 4 步。

    这里读取到的内容即为更新前的数据，也就是历史版本的数据：

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

6. 清空这个变量后，即可读取最新版本数据：

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
