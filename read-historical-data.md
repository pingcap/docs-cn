---
title: 使用系统变量 `tidb_snapshot` 读取历史数据
summary: 了解如何使用系统变量 `tidb_snapshot` 从历史版本读取数据。
---

# 使用系统变量 `tidb_snapshot` 读取历史数据

本文档介绍如何使用系统变量 `tidb_snapshot` 从历史版本读取数据，包括具体的使用示例和保存历史数据的策略。

> **注意：**
>
> 您也可以使用 [Stale Read](/stale-read.md) 功能来读取历史数据，这是更推荐的方式。

## 功能说明

TiDB 实现了通过标准 SQL 接口直接读取历史数据的功能，无需特殊的客户端或驱动程序。

> **注意：**
>
> - 即使数据被更新或删除，也可以通过 SQL 接口读取其历史版本。
> - 在读取历史数据时，即使当前表结构已经改变，TiDB 也会返回带有旧表结构的数据。

## TiDB 如何读取历史版本数据

TiDB 引入了 [`tidb_snapshot`](/system-variables.md#tidb_snapshot) 系统变量来支持读取历史数据。关于 `tidb_snapshot` 变量：

- 该变量在 `SESSION` 作用域内有效。
- 可以使用 `SET` 语句修改其值。
- 变量的数据类型为文本。
- 变量接受 TSO（时间戳预言机）和日期时间格式。TSO 是从 PD 获取的全局唯一时间服务。可接受的日期时间格式为 "2016-10-08 16:45:26.999"。通常，日期时间可以使用秒级精度设置，例如 "2016-10-08 16:45:26"。
- 当设置该变量时，TiDB 会使用其值作为时间戳创建一个快照，这只涉及数据结构且没有任何开销。之后，所有的 `SELECT` 操作都将从该快照中读取数据。

> **注意：**
>
> 由于 TiDB 事务中的时间戳是由 Placement Driver (PD) 分配的，存储的数据版本也是基于 PD 分配的时间戳进行标记的。当创建快照时，版本号是基于 `tidb_snapshot` 变量的值。如果 TiDB 服务器的本地时间与 PD 服务器时间存在较大差异，请使用 PD 服务器的时间。

从历史版本读取数据后，您可以通过结束当前会话或使用 `SET` 语句将 `tidb_snapshot` 变量的值设置为 ""（空字符串）来读取最新版本的数据。

## TiDB 如何管理数据版本

TiDB 实现了多版本并发控制（MVCC）来管理数据版本。之所以保留数据的历史版本，是因为每次更新/删除都会创建数据对象的新版本，而不是直接在原地更新/删除数据对象。但并非所有版本都会被保留。如果版本早于特定时间，它们将被完全删除，以减少存储占用和过多历史版本导致的性能开销。

在 TiDB 中，垃圾回收（GC）会定期运行以删除过时的数据版本。有关 GC 的详细信息，请参见 [TiDB 垃圾回收（GC）](/garbage-collection-overview.md)

请特别注意以下几点：

- [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)：此系统变量用于配置早期修改的保留时间（默认值：`10m0s`）。
- `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'` 的输出。这是当前可以读取历史数据的 `safePoint`。每次运行垃圾回收进程时都会更新此值。

## 示例

1. 在初始阶段，创建一个表并插入几行数据：

    ```sql
    mysql> create table t (c int);
    Query OK, 0 rows affected (0.01 sec)

    mysql> insert into t values (1), (2), (3);
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查看表中的数据：

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. 查看表的时间戳：

    ```sql
    mysql> select now();
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4. 更新其中一行的数据：

    ```sql
    mysql> update t set c=22 where c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

5. 确认数据已更新：

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6. 设置作用域为 Session 的 `tidb_snapshot` 变量。设置该变量后，可以读取该值之前的最新版本。

    > **注意：**
    >
    > 在本例中，该值被设置为更新操作之前的时间。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    > 您应该在 `tidb_snapshot` 前使用 `@@` 而不是 `@`，因为 `@@` 用于表示系统变量，而 `@` 用于表示用户变量。

    **结果：** 以下语句读取的是更新操作之前的数据，即历史数据。

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

7. 将 `tidb_snapshot` 变量设置为 ""（空字符串），您就可以读取最新版本的数据：

    ```sql
    mysql> set @@tidb_snapshot="";
    Query OK, 0 rows affected (0.00 sec)
    ```

    ```sql
    mysql> select * from t;
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
    > 您应该在 `tidb_snapshot` 前使用 `@@` 而不是 `@`，因为 `@@` 用于表示系统变量，而 `@` 用于表示用户变量。

## 如何恢复历史数据

在从旧版本恢复数据之前，请确保在您处理数据时垃圾回收（GC）不会清除历史数据。这可以通过设置 `tidb_gc_life_time` 变量来实现，如下例所示。恢复完成后，不要忘记将变量设置回之前的值。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **注意：**
>
> 将 GC 生命周期从默认的 10 分钟增加到半小时或更长时间将导致保留更多的行版本，这可能需要更多的磁盘空间。这也可能影响某些操作的性能，例如在数据读取过程中，TiDB 需要跳过同一行的这些额外版本时的扫描操作。

要从旧版本恢复数据，您可以使用以下方法之一：

- 对于简单的情况，在设置 `tidb_snapshot` 变量后使用 [`SELECT`](/sql-statements/sql-statement-select.md) 并复制粘贴输出，或使用 `SELECT ... INTO OUTFILE` 然后使用 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 稍后导入数据。

- 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-historical-data-snapshots-of-tidb) 导出历史快照。Dumpling 在导出较大数据集时表现良好。
