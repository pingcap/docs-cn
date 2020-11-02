---
title: 系统变量
aliases: ['/docs-cn/v3.0/system-variables/','/docs-cn/v3.0/reference/configuration/tidb-server/mysql-variables/','/docs-cn/sql/variable/']

---

# 系统变量

MySQL 系统变量 (System Variables) 是一些系统参数，用于调整数据库运行时的行为，根据变量的作用范围分为全局范围有效（Global Scope）以及会话级别有效（Session Scope）。TiDB 支持 MySQL5.7 的所有系统变量，大部分变量仅仅是为了兼容性而支持，不会影响运行时行为。

## 设置系统变量

通过 [`SET` 语句](/sql-statements/sql-statement-set-variable.md) 可以修改系统变量的值。进行修改时，还要考虑变量可修改的范围，不是所有的变量都能在全局/会话范围内进行修改。具体的可修改范围参考 [MySQL 动态变量文档](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html)。

### 全局范围值

* 在变量名前加 `GLOBAL` 关键词或者是使用 `@@global.` 作为修饰符:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@global.autocommit = 1;
    ```

> **注意：**
>
<<<<<<< HEAD
> 在分布式 TiDB 中，`GLOBAL` 变量的设置会持久化到存储层中，单个 TiDB 实例每 2 秒会主动进行一次全变量的获取并形成 `gvc` (global variables cache) 缓存，该缓存有效时间最多可持续 2 秒。在设置 `GLOBAL` 变量之后，为了保证新会话的有效性，请确保两个操作之间的间隔大于 2 秒。相关细节可以查看 [Issue #14531](https://github.com/pingcap/tidb/issues/14531)。
=======
> 该变量只有在默认值 `0` 时，才算是安全的。因为设置 `tidb_enable_noop_functions=1` 后，TiDB 会自动忽略某些语法而不报错，这可能会导致应用程序出现异常行为。

### `tidb_enable_slow_log`

- 作用域：INSTANCE
- 默认值：1
- 这个变量用于控制是否开启 slow log 功能，默认开启。

### `tidb_enable_stmt_summary` <span class="version-mark">从 v3.0.4 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：1（受配置文件影响，这里给出的是默认配置文件取值）
- 这个变量用来控制是否开启 statement summary 功能。如果开启，SQL 的耗时等执行信息将被记录到系统表 `information_schema.STATEMENTS_SUMMARY` 中，用于定位和排查 SQL 性能问题。

### `tidb_enable_table_partition`

- 作用域：SESSION | GLOBAL
- 默认值："on"
- 这个变量用来设置是否开启 `TABLE PARTITION` 特性。目前变量支持以下三种值：

    - 默认值 `on` 表示开启 TiDB 当前已实现了的分区表类型，目前 range partition、hash partition 以及 range column 单列的场景会生效。
    - `auto` 目前作用和 `on` 一样。
    - `off` 表示关闭 `TABLE PARTITION` 特性，此时语法还是保持兼容，只是创建的表并不是真正的分区表，而是普通的表。

- 注意，目前 TiDB 只支持 range partition 和 hash partition。

### `tidb_enable_telemetry` <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：GLOBAL
- 默认值: 1
- 这个变量用于动态地控制 TiDB 遥测功能是否开启。设置为 `0` 可以关闭 TiDB 遥测功能。当所有 TiDB 实例都设置 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 为 `false` 时将忽略该系统变量并总是关闭 TiDB 遥测功能。参阅[遥测](/telemetry.md)了解该功能详情。

### `tidb_enable_vectorized_expression` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值: 1
- 这个变量用于控制是否开启向量化执行。

### `tidb_enable_window_function`

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用来控制是否开启窗口函数的支持。默认值 1 代表开启窗口函数的功能。
- 由于窗口函数会使用一些保留关键字，可能导致原先可以正常执行的 SQL 语句在升级 TiDB 后无法被解析语法，此时可以将 `tidb_enable_window_function` 设置为 `0`。

### `tidb_evolve_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值: off
- 这个变量用于控制是否启用自动演进绑定功能。该功能的详细介绍和使用方法可以参考[自动演进绑定](/sql-plan-management.md#自动演进绑定-baseline-evolution)。
- 为了减少自动演进对集群的影响，可以进行以下配置：

    - 设置 `tidb_evolve_plan_task_max_time`，限制每个执行计划运行的最长时间，其默认值为 600s；
    - 设置`tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time`，限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。

### `tidb_evolve_plan_task_end_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 默认值：23:59 +0000
- 这个变量用来设置一天中允许自动演进的结束时间。

### `tidb_evolve_plan_task_max_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 默认值：600
- 该变量用于限制自动演进功能中，每个执行计划运行的最长时间，单位为秒。

### `tidb_evolve_plan_task_start_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 默认值：00:00 +0000
- 这个变量用来设置一天中允许自动演进的开始时间。

### `tidb_expensive_query_time_threshold`

- 作用域：INSTANCE
- 默认值：60
- 这个变量用来控制打印 expensive query 日志的阈值时间，单位是秒，默认值是 60 秒。expensive query 日志和慢日志的差别是，慢日志是在语句执行完后才打印，expensive query 日志可以把正在执行中的语句且执行时间超过阈值的语句及其相关信息打印出来。

### `tidb_force_priority`

- 作用域：INSTANCE
- 默认值：`NO_PRIORITY`
- 这个变量用于改变 TiDB server 上执行的语句的默认优先级。例如，你可以通过设置该变量来确保正在执行 OLAP 查询的用户优先级低于正在执行 OLTP 查询的用户。
- 可设置为 `NO_PRIORITY`、`LOW_PRIORITY`、`DELAYED` 或 `HIGH_PRIORITY`。

### `tidb_general_log`

- 作用域：INSTANCE
- 默认值：0
- 这个变量用来设置是否在日志里记录所有的 SQL 语句。

### `tidb_hash_join_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：5
- 这个变量用来设置 hash join 算法的并发度。

### `tidb_hashagg_final_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：4
- 这个变量用来设置并行 hash aggregation 算法 final 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。

### `tidb_hashagg_partial_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：4
- 这个变量用来设置并行 hash aggregation 算法 partial 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。

### `tidb_index_join_batch_size`

- 作用域：SESSION | GLOBAL
- 默认值：25000
- 这个变量用来设置 index lookup join 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_index_lookup_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：4
- 这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_index_lookup_join_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：4
- 这个变量用来设置 index lookup join 算法的并发度。

### `tidb_index_lookup_size`

- 作用域：SESSION | GLOBAL
- 默认值：20000
- 这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_index_serial_scan_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。
>>>>>>> 3623400c... config: hide & deprecate enable-streaming (#4781)

### 会话范围值

* 在变量名前加 `SESSION` 关键词或者是使用 `@@session.` 作为修饰符，或者是不加任何修饰符:

    {{< copyable "sql" >}}

    ```sql
    SET SESSION autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@session.autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@autocommit = 1;
    ```

* `LOCAL` 以及 `@@local.` 是 `SESSION` 以及 `@@session.` 的同义词

### 系统变量的作用机制

* 会话范围的系统变量仅仅会在创建会话时才会根据全局范围系统变量初始化自己的值。更改全局范围的系统变量不会改变已经创建的会话正在使用的系统变量的值。

    {{< copyable "sql" >}}

    ```sql
    SELECT @@GLOBAL.autocommit;
    ```

    ```
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | ON                  |
    +---------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL autocommit = OFF;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    会话范围的系统变量不会改变，会话中执行的事务依旧是以自动提交的形式来进行：

    {{< copyable "sql" >}}

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT @@GLOBAL.autocommit;
    ```

    ```
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | OFF                 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    exit
    ```

    ```
    Bye
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

    ```
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 3
    Server version: 5.7.25-TiDB-None MySQL Community Server (Apache License 2.0)

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

    新建的会话会使用新的全局变量：

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | OFF                  |
    +----------------------+
    1 row in set (0.00 sec)
    ```

## TiDB 支持的 MySQL 系统变量

下列系统变量是 TiDB 真正支持并且行为和 MySQL 一致：

| 变量名 | 作用域 | 说明 |
| ---------------- | -------- | -------------------------------------------------- |
| autocommit | GLOBAL \| SESSION | 是否自动 Commit 事务 |
| sql_mode | GLOBAL \| SESSION | 支持部分 MySQL SQL mode，|
| time_zone | GLOBAL \| SESSION | 数据库所使用的时区 |
| tx_isolation | GLOBAL \| SESSION | 事务隔离级别 |
| max\_execution\_time | GLOBAL \| SESSION | 语句超时时间，单位为毫秒 |
| innodb\_lock\_wait\_timeout | GLOBAL \| SESSION | 悲观事务语句等锁时间，单位为秒 |
| interactive\_timeout | SESSION \| GLOBAL | 交互式用户会话的空闲超时，单位为秒 |

> **注意：**
>
> `max_execution_time` 目前对所有类型的 `statement` 生效，并非只对 `SELECT` 语句生效。实际精度在 100ms 级别，而非更准确的毫秒级别。

## TiDB 特有的系统变量

参见 [TiDB 专用系统变量](/tidb-specific-system-variables.md)。
