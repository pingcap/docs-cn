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
> 在分布式 TiDB 中，`GLOBAL` 变量的设置会持久化到存储层中，单个 TiDB 实例每 2 秒会主动进行一次全变量的获取并形成 `gvc` (global variables cache) 缓存，该缓存有效时间最多可持续 2 秒。在设置 `GLOBAL` 变量之后，为了保证新会话的有效性，请确保两个操作之间的间隔大于 2 秒。相关细节可以查看 [Issue #14531](https://github.com/pingcap/tidb/issues/14531)。

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

<<<<<<< HEAD
    会话范围的系统变量不会改变，会话中执行的事务依旧是以自动提交的形式来进行：
=======
### `tidb_current_ts`

- 作用域：SESSION
- 默认值：0
- 这个变量是一个只读变量，用来获取当前事务的时间戳。

### `tidb_ddl_error_count_limit`

- 作用域：GLOBAL
- 默认值：512
- 这个变量用来控制 DDL 操作失败重试的次数。失败重试次数超过该参数的值后，会取消出错的 DDL 操作。

## `tidb_ddl_reorg_batch_size`

- 作用域：GLOBAL
- 默认值：256
- 这个变量用来设置 DDL 操作 `re-organize` 阶段的 batch size。比如 `ADD INDEX` 操作，需要回填索引数据，通过并发 `tidb_ddl_reorg_worker_cnt` 个 worker 一起回填数据，每个 worker 以 batch 为单位进行回填。

    - 如果 `ADD INDEX` 操作时有较多 `UPDATA` 操作或者 `REPLACE` 等更新操作，batch size 越大，事务冲突的概率也会越大，此时建议调小 batch size 的值，最小值是 32。
    - 在没有事务冲突的情况下，batch size 可设为较大值，最大值是 10240，这样回填数据的速度更快，但是 TiKV 的写入压力也会变大。

### `tidb_ddl_reorg_priority`

- 作用域：SESSION | GLOBAL
- 默认值：PRIORITY_LOW
- 这个变量用来设置 `ADD INDEX` 操作 `re-organize` 阶段的执行优先级，可设置为 `PRIORITY_LOW`/`PRIORITY_NORMAL`/`PRIORITY_HIGH`。

### `tidb_ddl_reorg_worker_cnt`

- 作用域：GLOBAL
- 默认值：4
- 这个变量用来设置 DDL 操作 `re-organize` 阶段的并发度。

### `tidb_disable_txn_auto_retry`

- 作用域：SESSION | GLOBAL
- 默认值：on
- 这个变量用来设置是否禁用显式事务自动重试，设置为 `on` 时，不会自动重试，如果遇到事务冲突需要在应用层重试。

    如果将该变量的值设为 `off`，TiDB 将会自动重试事务，这样在事务提交时遇到的错误更少。需要注意的是，这样可能会导致数据更新丢失。

    这个变量不会影响自动提交的隐式事务和 TiDB 内部执行的事务，它们依旧会根据 `tidb_retry_limit` 的值来决定最大重试次数。

    关于是否需要禁用自动重试，请参考[重试的局限性](/optimistic-transaction.md#重试的局限性)。

### `tidb_distsql_scan_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：15
- 这个变量用来设置 scan 操作的并发度。
- AP 类应用适合较大的值，TP 类应用适合较小的值。对于 AP 类应用，最大值建议不要超过所有 TiKV 节点的 CPU 核数。

### `tidb_enable_cascades_planner`

- 作用域：SESSION | GLOBAL
- 默认值: 0
- 这个变量用于控制是否开启 cascades planner。

### `tidb_enable_clustered_index` <!-- 从 v5.0 版本开始引入 -->

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用于控制是否开启聚簇索引特性。
    - 该特性只适用于新创建的表，对于已经创建的旧表不会有影响。
    - 该特性只适用于主键为单列非整数类型的表和主键为多列的表。对于无主键的表和主键是单列整数类型的表不会有影响。
    - 通过执行 `select tidb_pk_type from information_schema.tables where table_name = '{table_name}'` 可以查看一张表是否使用了聚簇索引特性。
- 特性启用以后，row 会直接存储在主键上，而不再是存储在系统内部分配的 `row_id` 上并用额外创建的主键索引指向 `row_id`。

    开启该特性对性能的影响主要体现在以下几个方面:
    - 插入的时候每行会减少一个索引 key 的写入。
    - 使用主键作为等值条件查询的时候，会节省一次读取请求。
    - 使用单列主键作为范围条件查询的时候，可以节省多次读取请求。 
    - 使用多列主键的前缀作为等值或范围条件查询的时候，可以节省多次读取请求。

### `tidb_enable_chunk_rpc` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：1
- 这个变量用来设置是否启用 Coprocessor 的 `Chunk` 数据编码格式。

### `tidb_enable_fast_analyze`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量用来控制是否启用统计信息快速分析功能。默认值 0 表示不开启。
- 快速分析功能开启后，TiDB 会随机采样约 10000 行的数据来构建统计信息。因此在数据分布不均匀或者数据量比较少的情况下，统计信息的准确度会比较低。这可能导致执行计划不优，比如选错索引。如果可以接受普通 `ANALYZE` 语句的执行时间，则推荐关闭快速分析功能。

### `tidb_enable_index_merge` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值: 0
- 这个变量用于控制是否开启 index merge 功能。

### `tidb_enable_noop_functions` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值: 0
- 这个变量用于控制是否开启 `get_lock` 和 `release_lock` 这两个没有实现的函数。需要注意的是，当前版本的 TiDB 这两个函数永远返回 1。

### `tidb_enable_slow_log`

- 作用域：INSTANCE
- 默认值：1
- 这个变量用于控制是否开启 slow log 功能，默认开启。

### `tidb_enable_stmt_summary` <span class="version-mark">从 v3.0.4 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：1（受配置文件影响，这里给出的是默认配置文件取值）
- 这个变量用来控制是否开启 statement summary 功能。如果开启，SQL 的耗时等执行信息将被记录到系统表 `information_schema.STATEMENTS_SUMMARY` 中，用于定位和排查 SQL 性能问题。

### `tidb_enable_streaming`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置是否启用 Streaming。

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

### `tidb_init_chunk_size`

- 作用域：SESSION | GLOBAL
- 默认值：32
- 这个变量用来设置执行过程中初始 chunk 的行数。默认值是 32，可设置的范围是 1～32。

### `tidb_isolation_read_engines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值: tikv, tiflash, tidb
- 这个变量用于设置 TiDB 在读取数据时可以使用的存储引擎列表。

### `tidb_low_resolution_tso`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置是否启用低精度 tso 特性，开启该功能之后新事务会使用一个每 2s 更新的 ts 来读取数据。
- 主要场景是在可以容忍读到旧数据的情况下，降低小的只读事务获取 tso 的开销。

### `tidb_max_chunk_size`

- 作用域：SESSION | GLOBAL
- 默认值：1024
- 最小值：32
- 这个变量用来设置执行过程中一个 chunk 最大的行数，设置过大可能引起缓存局部性的问题。

### `tidb_max_delta_schema_count`

- 作用域：GLOBAL
- 默认值：1024
- 这个变量用来设置缓存 schema 版本信息（对应版本修改的相关 table IDs）的个数限制，可设置的范围 100 - 16384。此变量在 2.1.18 及之后版本支持。

### `tidb_mem_quota_query`

- 作用域：SESSION
- 默认值：1 GB
- 这个变量用来设置一条查询语句的内存使用阈值。
- 如果一条查询语句执行过程中使用的内存空间超过该阈值，会触发 TiDB 启动配置文件中 OOMAction 项所指定的行为。该变量的初始值由配置项 [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query) 配置。

### `tidb_metric_query_range_duration` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值: 60
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 range duration，单位为秒。

### `tidb_metric_query_step` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值: 60
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 step，单位为秒。

### `tidb_opt_agg_push_down`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作。
当查询中聚合操作执行很慢时，可以尝试设置该变量为 1。

### `tidb_opt_correlation_exp_factor`

- 作用域：SESSION | GLOBAL
- 默认值：1
- 当交叉估算方法不可用时，会采用启发式估算方法。这个变量用来控制启发式方法的行为。当值为 0 时不用启发式估算方法，大于 0 时，该变量值越大，启发式估算方法越倾向 index scan，越小越倾向 table scan。

### `tidb_opt_correlation_threshold`

- 作用域：SESSION | GLOBAL
- 默认值：0.9
- 这个变量用来设置优化器启用交叉估算 row count 方法的阈值。如果列和 handle 列之间的顺序相关性超过这个阈值，就会启用交叉估算方法。
- 交叉估算方法可以简单理解为，利用这个列的直方图来估算 handle 列需要扫的行数。

### `tidb_opt_distinct_agg_push_down`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。
当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `1`。

在以下示例中，`tidb_opt_distinct_agg_push_down` 开启前，TiDB 需要从 TiKV 读取所有数据，并在 TiDB 侧执行 `disctinct`。`tidb_opt_distinct_agg_push_down` 开启后， `distinct a` 被下推到了 Coprocessor，在 `HashAgg_5` 里新增里一个 `group by` 列 `test.t.a`。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### `tidb_opt_insubq_to_join_and_agg`

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用来设置是否开启优化规则：将子查询转成 join 和 aggregation。

    例如，打开这个优化规则后，会将下面子查询做如下变化：
>>>>>>> 8ed9e9a9... Update system-variables.md (#4595)

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
