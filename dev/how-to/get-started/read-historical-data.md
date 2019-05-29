---
title: 读取历史数据
category: how-to
aliases: ['/docs-cn/op-guide/history-read/']
---

# 读取历史数据

本文档介绍 TiDB 如何读取历史版本数据，包括具体的操作流程以及历史数据的保存策略。

## 功能说明

TiDB 实现了通过标准 SQL 接口读取历史数据功能，无需特殊的 client 或者 driver。当数据被更新、删除后，依然可以通过 SQL 接口将更新/删除前的数据读取出来。

另外即使在更新数据之后，表结构发生了变化，TiDB 依旧能用旧的表结构将数据读取出来。

## 操作流程

为支持读取历史版本数据， 引入了一个新的 system variable: tidb_snapshot ，这个变量是 Session 范围有效，可以通过标准的 Set 语句修改其值。其值为文本，能够存储 TSO 和日期时间。TSO 即是全局授时的时间戳，是从 PD 端获取的; 日期时间的格式可以为：
“2016-10-08 16:45:26.999”，一般来说可以只写到秒，比如”2016-10-08 16:45:26”。
当这个变量被设置时，TiDB 会用这个时间戳建立 Snapshot（没有开销，只是创建数据结构），随后所有的 Select 操作都会在这个 Snapshot 上读取数据。

> **注意：**
>
> TiDB 的事务是通过 PD 进行全局授时，所以存储的数据版本也是以 PD 所授时间戳作为版本号。在生成 Snapshot 时，是以 tidb_snapshot 变量的值作为版本号，如果 TiDB Server 所在机器和 PD Server 所在机器的本地时间相差较大，需要以 PD 的时间为准。

当读取历史版本操作结束后，可以结束当前 Session 或者是通过 Set 语句将 tidb_snapshot 变量的值设为 ""，即可读取最新版本的数据。

## 历史数据保留策略

TiDB 使用 MVCC 管理版本，当更新/删除数据时，不会做真正的数据删除，只会添加一个新版本数据，所以可以保留历史数据。历史数据不会全部保留，超过一定时间的历史数据会被彻底删除，以减小空间占用以及避免历史版本过多引入的性能开销。

TiDB 使用周期性运行的 GC（Garbage Collection，垃圾回收）来进行清理，关于 GC 的详细介绍参见 [TiDB 垃圾回收 (GC)](/op-guide/gc.md)。

这里需要重点关注的是 `tikv_gc_life_time` 和 `tikv_gc_safe_point` 这条。`tikv_gc_life_time` 用于配置历史版本保留时间，可以手动修改；`tikv_gc_safe_point` 记录了当前的 safePoint，用户可以安全地使用大于 safePoint 的时间戳创建 snapshot 读取历史版本。safePoint 在每次 GC 开始运行时自动更新。

## 示例

1. 初始化阶段，创建一个表，并插入几行数据：

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

3. 查看当前时间：

    ```sql
    mysql> select now();
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4. 更新某一行数据：

    ```sql
    mysql> update t set c=22 where c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

5. 确认数据已经被更新：

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

6. 设置一个特殊的环境变量，这个是一个 session scope 的变量，其意义为读取这个时间之前的最新的一个版本。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注意：**
    >
    > - 这里的时间设置的是 update 语句之前的那个时间。
    > - 在 `tidb_snapshot` 前须使用 `@@` 而非 `@`，因为 `@@` 表示系统变量，`@` 表示用户变量。

    这里读取到的内容即为 update 之前的内容，也就是历史版本：

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

7. 清空这个变量后，即可读取最新版本数据：

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
    > 在 `tidb_snapshot` 前须使用 `@@` 而非 `@`，因为 `@@` 表示系统变量，`@` 表示用户变量。