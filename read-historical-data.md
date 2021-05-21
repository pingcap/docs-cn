---
title: 读取历史数据
aliases: ['/docs-cn/dev/read-historical-data/','/docs-cn/dev/how-to/get-started/read-historical-data/']
---

# 读取历史数据

本文档介绍 TiDB 如何读取历史版本数据，包括具体的操作流程以及历史数据的保存策略。

## 功能说明

TiDB 实现了通过标准 SQL 接口读取历史数据功能，无需特殊的 client 或者 driver。当数据被更新、删除后，依然可以通过 SQL 接口将更新/删除前的数据读取出来。

另外即使在更新数据之后，表结构发生了变化，TiDB 依旧能用旧的表结构将数据读取出来。

## 操作流程

为支持读取历史版本数据， TiDB 引入了一个新的系统变量 [`tidb_snapshot`](/system-variables.md#tidb_snapshot)：

- 这个变量的作用域为 `SESSION`。
- 你可以通过标准的 `SET` 语句修改这个变量的值。
- 这个变量的数据类型为文本类型，能够存储 TSO 和日期时间。TSO 是从 PD 端获取的全局授时的时间戳，日期时间的格式为：“2016-10-08 16:45:26.999”，一般来说可以只写到秒，比如”2016-10-08 16:45:26”。
- 当这个变量被设置时，TiDB 会按照设置的时间戳建立 Snapshot（没有开销，只是创建数据结构），随后所有的 `SELECT` 操作都会从这个 Snapshot 上读取数据。

> **注意：**
>
> TiDB 的事务是通过 PD 进行全局授时，所以存储的数据版本也是以 PD 所授时间戳作为版本号。在生成 Snapshot 时，是以 tidb_snapshot 变量的值作为版本号，如果 TiDB Server 所在机器和 PD Server 所在机器的本地时间相差较大，需要以 PD 的时间为准。

当读取历史版本操作结束后，可以结束当前 Session 或者是通过 `SET` 语句将 tidb_snapshot 变量的值设为 ""，即可读取最新版本的数据。

## 历史数据保留策略

TiDB 使用 MVCC 管理版本，当更新/删除数据时，不会做真正的数据删除，只会添加一个新版本数据，所以可以保留历史数据。历史数据不会全部保留，超过一定时间的历史数据会被彻底删除，以减小空间占用以及避免历史版本过多引入的性能开销。

TiDB 使用周期性运行的 GC（Garbage Collection，垃圾回收）来进行清理，关于 GC 的详细介绍参见 [TiDB 垃圾回收 (GC)](/garbage-collection-overview.md)。

这里需要重点关注的是：

- 使用系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 可以配置历史版本的保留时间（默认值是 `10m0s`）。
- 使用 SQL 语句 `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'` 可以查询当前的 safePoint，即当前可以读的最旧的快照。在每次 GC 开始运行时，safePoint 将自动更新。

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
    set @@tidb_snapshot="2016-10-08 16:45:26";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    > - 这里的时间设置的是 update 语句之前的那个时间。
    > - 在 `tidb_snapshot` 前须使用 `@@` 而非 `@`，因为 `@@` 表示系统变量，`@` 表示用户变量。

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
    set @@tidb_snapshot="";
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

    > **注意：**
    >
    > 在 `tidb_snapshot` 前须使用 `@@` 而非 `@`，因为 `@@` 表示系统变量，`@` 表示用户变量。

## 历史数据恢复策略

在恢复历史版本的数据之前，确保在运行时，GC（垃圾回收）不会清除历史数据。可以通过设置 `tidb_gc_life_time` 变量来实现该过程，如下图所示。不要忘记在恢复历史数据后将该变量设置回之前的值。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **注意：**
>
> 将 GC life time 从默认的 10 分钟增加到半小时或更多时，会导致保留有额外的行数的版本并可能占用更多的磁盘空间。这也可能会影响某些操作的性能，比如扫描，当 TiDB 在读取数据时需要跳过这些额外的有相同行的版本。

想要从恢复历史版本的数据，可以使用以下任意一种方法进行设置：

- 对于简单的情况，在设置 `tidb_snapshot` 变量后使用 `SELECT` 语句并复制粘贴输出结果，或者使用 `SELECT ... INTO LOCAL OUTFLE` 语句并在之后使用 `LOAD DATA` 语句来导入数据。

- 使用 [Dumpling](/dumpling-overview.md#导出-tidb-的历史数据快照) 导出 TiDB 的历史数据快照。Dumpling 在导出较大的数据集时表现良好。