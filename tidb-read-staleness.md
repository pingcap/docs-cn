---
title: 使用 `tidb_read_staleness` 系统变量读取历史数据
summary: 了解如何使用 `tidb_read_staleness` 系统变量读取历史数据。
---

# 使用 `tidb_read_staleness` 系统变量读取历史数据

为了支持读取历史数据，TiDB 在 v5.4 中引入了新的系统变量 `tidb_read_staleness`。本文档描述如何通过这个系统变量读取历史数据，包括详细的操作步骤。

## 功能说明

`tidb_read_staleness` 系统变量用于设置当前会话中 TiDB 可以读取的历史数据的时间范围。该变量的数据类型为整数类型，作用域为 `SESSION`。设置该值后，TiDB 会从该变量允许的范围内选择一个尽可能新的时间戳，所有后续的读取操作都将基于这个时间戳执行。例如，如果将该变量的值设置为 `-5`，在 TiKV 具有相应历史版本数据的条件下，TiDB 会在 5 秒的时间范围内选择一个尽可能新的时间戳。

启用 `tidb_read_staleness` 后，你仍然可以执行以下操作：

- 在当前会话中插入、修改、删除数据或执行 DML 操作。这些语句不受 `tidb_read_staleness` 的影响。
- 在当前会话中启动交互式事务。该事务中的查询仍然读取最新数据。

读取历史数据后，你可以通过以下两种方式读取最新数据：

- 启动新的会话。
- 使用 `SET` 语句将 `tidb_read_staleness` 变量的值设置为 `""`。

> **注意：**
>
> 为了减少延迟并提高 Stale Read 数据的时效性，你可以修改 TiKV 的 `advance-ts-interval` 配置项。详情请参见[减少 Stale Read 延迟](/stale-read.md#reduce-stale-read-latency)。

## 使用示例

本节通过示例说明如何使用 `tidb_read_staleness`。

1. 创建一个表，并向表中插入几行数据：

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

3. 更新一行数据：

    {{< copyable "sql" >}}

    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

4. 确认数据已更新：

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

5. 设置 `tidb_read_staleness` 系统变量。

    该变量的作用域为 `SESSION`。设置其值后，TiDB 会读取该值设定时间之前的最新版本数据。

    以下设置表示 TiDB 会在 5 秒前到现在的时间范围内选择一个尽可能新的时间戳，并将其用作读取历史数据的时间戳：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    >  - 在 `tidb_read_staleness` 前使用 `@@` 而不是 `@`。`@@` 表示系统变量，`@` 表示用户变量。
    >  - 你需要根据在步骤 3 和步骤 4 中花费的总时间来设置历史时间范围（`tidb_read_staleness` 的值）。否则，查询结果中将显示最新数据，而不是历史数据。因此，你需要根据操作所花费的时间来调整这个时间范围。例如，在本例中，由于设置的时间范围是 5 秒，你需要在 5 秒内完成步骤 3 和步骤 4。

    此处读取的是更新前的数据，即历史数据：

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

6. 取消设置此变量后，TiDB 可以读取最新数据：

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
