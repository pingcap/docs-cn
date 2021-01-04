---
title: 系统变量
aliases: ['/docs-cn/dev/system-variables/','/docs-cn/dev/reference/configuration/tidb-server/mysql-variables/','/docs-cn/dev/tidb-specific-system-variables/','/docs-cn/dev/reference/configuration/tidb-server/tidb-specific-variables/','/zh/tidb/dev/tidb-specific-system-variables/']
---

# 系统变量

TiDB 系统变量的行为与 MySQL 相似但有一些不同，变量的作用范围可以是全局范围有效 (Global Scope)、实例级别有效 (Instance Scope) 或会话级别有效 (Session Scope)，或组合了上述多个范围。其中：

- 对 `GLOBAL` 作用域变量的更改，设置后**只对新 TiDB 连接会话生效**，当前活动连接会话不受影响。更改会被持久化，重启后仍然生效。

- 对 `INSTANCE` 作用域变量的更改，设置后会立即对当前 TiDB 实例所有活动连接会话或新连接会话生效，其他 TiDB 实例不生效。更改**不会**被持久化，重启 TiDB 后会**失效**。

使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md)可以设置变量的作用范围为全局级别、实例级别或会话级别。

```sql
# 以下两个语句等价地改变一个 Session 变量
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# 以下两个语句等价地改变一个 Global 变量
SET @@global.tidb_distsql_scan_concurrency = 10;
SET  GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **注意：**
>
> - 在 TiDB 中，`GLOBAL` 变量的设置即使重启后也仍然有效。每隔 2 秒，其他 TiDB server 会获取到对变量设置的更改。详情见 [TiDB #14531](https://github.com/pingcap/tidb/issues/14531)。
> - 此外，由于应用和连接器通常需要读 MySQL 变量，为了兼容这一需求，在 TiDB 中，部分 MySQL 5.7 的变量既可读取也可设置。例如，尽管 JDBC 连接器不依赖于查询缓存 (query cache) 的行为，但仍然可以读取和设置查询缓存。

## 变量参考

### `autocommit`

- 作用域：SESSION | GLOBAL
- 默认值：ON
- 用于设置在非显式事务时是否自动提交事务。更多信息，请参见[事务概述](/transaction-overview.md#自动提交)。

### `allow_auto_random_explicit_insert` <span class="version-mark">从 v4.0.3 版本开始引入</span>

- 作用域：SESSION（v4.0.5 开始为 SESSION | GLOBAL）
- 默认值：0
- 是否允许在 `INSERT` 语句中显式指定含有 `AUTO_RANDOM` 属性的列的值，`1` 为允许，`0` 为不允许。

### `ddl_slow_threshold`

- 作用域：INSTANCE
- 默认值：300
- 耗时超过该阈值的 DDL 操作会被输出到日志，单位为毫秒。

### `foreign_key_checks`

- 作用域：NONE
- 默认值：OFF
- 为保持兼容，TiDB 对外键检查返回 OFF。

### `hostname`

- 作用域：NONE
- 默认值：（系统主机名）
- 这个变量一个只读变量，表示 TiDB server 的主机名。

### `innodb_lock_wait_timeout`

- 作用域：SESSION | GLOBAL
- 默认值：50
- 悲观事务语句等锁时间，单位为秒。

### `last_plan_from_cache` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：0
- 这个变量用来显示上一个 `execute` 语句所使用的执行计划是不是直接从 plan cache 中取出来的。

### `last_plan_from_binding` <span class="version-mark">从 v4.0 版本开始引入</span>

作用域：SESSION

默认值：0

这个变量用来显示上一条执行的语句所使用的执行计划是不是来自 binding 的执行计划。

### `max_execution_time`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 语句最长执行时间，单位为毫秒。默认值 (0) 表示无限制。

> **注意：**
>
> `max_execution_time` 目前对所有类型的语句生效，并非只对 `SELECT` 语句生效，与 MySQL 不同（只对`SELECT` 语句生效）。实际精度在 100ms 级别，而非更准确的毫秒级别。

### `interactive_timeout`

- 作用域：SESSION | GLOBAL
- 默认值：28800
- 该变量表示交互式用户会话的空闲超时，单位为秒。交互式用户会话是指使用 `CLIENT_INTERACTIVE` 选项调用 [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API 建立的会话（例如：MySQL shell 客户端）。该变量与 MySQL 完全兼容。

### `sql_mode`

- 作用域：SESSION | GLOBAL
- 默认值：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- 这个变量控制许多 MySQL 兼容行为。详情见 [SQL 模式](/sql-mode.md)。

### `sql_select_limit` <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：`2^64 - 1` (18446744073709551615)
- `SELECT` 语句返回的最大行数。

### `tidb_allow_batch_cop` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量用于控制 TiDB 向 TiFlash 发送 coprocessor 请求的方式，有以下几种取值：

    * 0：从不批量发送请求
    * 1：aggregation 和 join 的请求会进行批量发送
    * 2：所有的 cop 请求都会批量发送

### `tidb_allow_remove_auto_inc` <span class="version-mark">从 v2.1.18 和 v3.0.4 版本开始引入</span>

- 作用域：SESSION
- 默认值：0
- 这个变量用来控制是否允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 来移除某个列的 `AUTO_INCREMENT` 属性。默认 (`0`) 为不允许。

### `tidb_auto_analyze_end_time`

- 作用域：GLOBAL
- 默认值：23:59 +0000
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的结束时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

### `tidb_auto_analyze_ratio`

- 作用域：GLOBAL
- 默认值：0.5
- 这个变量用来设置 TiDB 在后台自动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息的阈值。`0.5` 指的是当表中超过 50% 的行被修改时，触发自动 ANALYZE 更新。可以指定 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 来限制自动 ANALYZE 的时间

> **注意：**
>
> 只有在 TiDB 的启动配置文件中开启了 `run-auto-analyze` 选项，该 TiDB 才会触发 `auto_analyze`。

### `tidb_auto_analyze_start_time`

- 作用域：GLOBAL
- 默认值：00:00 +0000
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的开始时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

### `tidb_backoff_lock_fast`

- 作用域：SESSION | GLOBAL
- 默认值：100
- 这个变量用来设置读请求遇到锁的 backoff 时间。

### `tidb_backoff_weight`

- 作用域：SESSION | GLOBAL
- 默认值：2
- 这个变量用来给 TiDB 的 `backoff` 最大时间增加权重，即内部遇到网络或其他组件（TiKV、PD）故障时，发送重试请求的最大重试时间。可以通过这个变量来调整最大重试时间，最小值为 1。

    例如，TiDB 向 PD 取 TSO 的基础超时时间是 15 秒，当 `tidb_backoff_weight = 2` 时，取 TSO 的最大超时时间为：基础时间 \* 2 等于 30 秒。

    在网络环境较差的情况下，适当增大该变量值可以有效缓解因为超时而向应用端报错的情况；而如果应用端希望更快地接到报错信息，则应该尽量减小该变量的值。

### `tidb_build_stats_concurrency`

- 作用域：SESSION
- 默认值：4
- 这个变量用来设置 ANALYZE 语句执行时并发度。
- 当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### `tidb_capture_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：off
- 这个变量用于控制是否开启[自动捕获绑定](/sql-plan-management.md#自动捕获绑定-baseline-capturing)功能。该功能依赖 Statement Summary，因此在使用自动绑定之前需打开 Statement Summary 开关。
- 开启该功能后会定期遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动创建绑定。

### `tidb_check_mb4_value_in_utf8`

- 作用域：INSTANCE
- 默认值：1
- 这个变量用来设置是否开启对字符集为 UTF8 类型的数据做合法性检查，默认值 `1` 表示开启检查。这个默认行为和 MySQL 是兼容的。
- 如果是旧版本升级时，可能需要关闭该选项，否则由于旧版本（v2.1.1 及之前）没有对数据做合法性检查，所以旧版本写入非法字符串是可以写入成功的，但是新版本加入合法性检查后会报写入失败。具体可以参考[升级后常见问题](/faq/upgrade-faq.md)。

### `tidb_checksum_table_concurrency`

- 作用域：SESSION
- 默认值：4
- 这个变量用来设置 `ADMIN CHECKSUM TABLE` 语句执行时扫描索引的并发度。
当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### `tidb_config`

- 作用域：SESSION
- 默认值：""
- 这个变量是一个只读变量，用来获取当前 TiDB Server 的配置信息。

### `tidb_constraint_check_in_place`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 该变量仅适用于乐观事务模型。当这个变量设置为 0 时，唯一索引的重复值检查会被推迟到事务提交时才进行。这有助于提高性能，但对于某些应用，可能导致非预期的行为。详情见[约束](/constraints.md)。

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 0：

        {{< copyable "sql" >}}

        ```sql
        create table t (i int key);
        insert into t values (1);
        begin optimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        {{< copyable "sql" >}}

        ```sql
        tidb> commit; -- 事务提交时才检查
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 1：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place=1;
        begin optimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

悲观事务模型中，始终默认执行约束检查。

### `tidb_current_ts`

- 作用域：SESSION
- 默认值：0
- 这个变量是一个只读变量，用来获取当前事务的时间戳。

### `tidb_ddl_error_count_limit`

- 作用域：GLOBAL
- 默认值：512
- 这个变量用来控制 DDL 操作失败重试的次数。失败重试次数超过该参数的值后，会取消出错的 DDL 操作。

### `tidb_ddl_reorg_batch_size`

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
- 若表的分区较多可以适当调小该参数，避免 TiKV 内存溢出 (OOM)。

### `tidb_dml_batch_size`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 样本值：20000
- 这个变量的值大于 `0` 时，TiDB 会将 `INSERT` 或 `LOAD DATA` 等语句在更小的事务中批量提交。这样可减少内存使用，确保大批量修改时事务大小不会达到 `txn-total-size-limit` 限制。
- 只有变量值为 `0` 时才符合 ACID 要求。否则无法保证 TiDB 的原子性和隔离性要求。

### `tidb_enable_amend_pessimistic_txn` <span class="version-mark">从 v4.0.7 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量用于控制是否开启 `AMEND TRANSACTION` 特性。在[悲观事务模式](/pessimistic-transaction.md)下开启该特性后，如果该事务相关的表存在并发 DDL 操作和 SCHEMA VERSION 变更，TiDB 会尝试对该事务进行 amend 操作，修正该事务的提交内容，使其和最新的有效 SCHEMA VERSION 保持一致，从而成功提交该事务而不返回 `Information schema is changed` 报错。该特性对以下并发 DDL 变更生效：

    - `ADD COLUMN` 或 `DROP COLUMN` 类型的 DDL 操作。
    - `MODIFY COLUMN` 或 `CHANGE COLUMN` 类型的 DDL 操作，且只对增大字段长度的操作生效。
    - `ADD INDEX` 或 `DROP INDEX` 类型的 DDL 操作，且操作的索引列须在事务开启之前创建。

> **注意：**
>
> 目前该特性可能造成事务语义的变化，且与 TiDB Binlog 存在部分不兼容的场景，可以参考[事务语义行为区别](https://github.com/pingcap/tidb/issues/21069)和[与 TiDB Binlog 兼容问题汇总](https://github.com/pingcap/tidb/issues/20996)了解更多关于该特性的使用注意事项。

### `tidb_enable_cascades_planner`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量用于控制是否开启 cascades planner。

### `tidb_enable_clustered_index` <!-- 从 v5.0 版本开始引入 -->

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量用于控制是否开启[聚簇索引](/clustered-indexes.md)特性。
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
- 默认值：0
- 这个变量用于控制是否开启 index merge 功能。

### `tidb_enable_noop_functions` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：0
- 默认情况下，用户尝试将某些语法用于尚未实现的功能时，TiDB 会报错。若将该变量值设为 `1`，TiDB 则自动忽略此类功能不可用的情况，即不会报错。若用户无法更改 SQL 代码，可考虑将变量值设为 `1`。
- 启用 `noop` 函数可以控制以下行为：
    * `get_lock` 和 `release_lock` 函数
    * `LOCK IN SHARE MODE` 语法
    * `SQL_CALC_FOUND_ROWS` 语法

> **注意：**
>
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

    - 默认值 `on` 表示开启 range partition、hash partition 以及 range column 单列的分区表。
    - `auto` 目前作用和 `on` 一样。
    - `nightly` 表示开启 `on` 的分区表类型，并开启 list partition 和 list columns partition。
    - `off` 表示关闭 `TABLE PARTITION` 特性，此时语法还是保持兼容，只是创建的表并不是真正的分区表，而是普通的表。

> **注意：**
>
> 目前 TiDB 默认只支持 Range partition 和 Hash partition。
> List partition 和 List COLUMNS partition 目前还属于实验特性。

### `tidb_enable_telemetry` <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：GLOBAL
- 默认值：1
- 这个变量用于动态地控制 TiDB 遥测功能是否开启。设置为 `0` 可以关闭 TiDB 遥测功能。当所有 TiDB 实例都设置 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 为 `false` 时将忽略该系统变量并总是关闭 TiDB 遥测功能。参阅[遥测](/telemetry.md)了解该功能详情。

### `tidb_enable_vectorized_expression` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用于控制是否开启向量化执行。

### `tidb_enable_window_function`

- 作用域：SESSION | GLOBAL
- 默认值：1
- 这个变量用来控制是否开启窗口函数的支持。默认值 1 代表开启窗口函数的功能。
- 由于窗口函数会使用一些保留关键字，可能导致原先可以正常执行的 SQL 语句在升级 TiDB 后无法被解析语法，此时可以将 `tidb_enable_window_function` 设置为 `0`。

### `tidb_evolve_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：off
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
- 默认值：NO_PRIORITY
- 这个变量用于改变 TiDB server 上执行的语句的默认优先级。例如，你可以通过设置该变量来确保正在执行 OLAP 查询的用户优先级低于正在执行 OLTP 查询的用户。
- 可设置为 `NO_PRIORITY`、`LOW_PRIORITY`、`DELAYED` 或 `HIGH_PRIORITY`。

### `tidb_general_log`

- 作用域：INSTANCE
- 默认值：0
- 这个变量用来设置是否在[日志](/tidb-configuration-file.md#logfile)里记录所有的 SQL 语句。该功能默认关闭。如果系统运维人员在定位问题过程中需要追踪所有 SQL 记录，可考虑开启该功能。
- 通过查询 `"GENERAL_LOG"` 字符串可以定位到该功能在日志中的所有记录。日志会记录以下内容：
    - `conn`：当前会话对应的 ID
    - `user`：当前会话用户
    - `schemaVersion`：当前 schema 版本
    - `txnStartTS`：当前事务的开始时间戳
    - `forUpdateTS`：事务模型为悲观事务时，SQL 语句的当前时间戳。悲观事务内发生写冲突时，会重试当前执行语句，该时间戳会被更新。重试次数由 [`max-retry-count`](/tidb-configuration-file.md#max-retry-count) 配置。事务模型为乐观事务时，该条目与 `txnStartTS` 等价。
    - `isReadConsistency`：当前事务隔离级别是否是读已提交 (RC)
    - `current_db`：当前数据库名
    - `txn_mode`：事务模型。可选值：`OPTIMISTIC`（乐观事务模型），或 `PESSIMISTIC`（悲观事务模型）
    - `sql`：当前查询对应的 SQL 语句

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
- 默认值：tikv, tiflash, tidb
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
- 默认值：60
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 range duration，单位为秒。

### `tidb_metric_query_step` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：60
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 step，单位为秒。

### `tidb_opt_agg_push_down`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。
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

在以下示例中，`tidb_opt_distinct_agg_push_down` 开启前，TiDB 需要从 TiKV 读取所有数据，并在 TiDB 侧执行 `distinct`。`tidb_opt_distinct_agg_push_down` 开启后， `distinct a` 被下推到了 Coprocessor，在 `HashAgg_5` 里新增里一个 `group by` 列 `test.t.a`。

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

    {{< copyable "sql" >}}

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    将子查询转成如下 join：

    {{< copyable "sql" >}}

    ```sql
    select * from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    如果 t1 在列 `aa` 上有 unique 且 not null 的限制，可以直接改写为如下，不需要添加 aggregation。

    {{< copyable "sql" >}}

    ```sql
    select * from t, t1 where t.a=t1.a;
    ```

### `tidb_opt_write_row_id`

- 作用域：SESSION
- 默认值：0
- 这个变量用来设置是否允许 `INSERT`、`REPLACE` 和 `UPDATE` 操作 `_tidb_rowid` 列，默认是不允许操作。该选项仅用于 TiDB 工具导数据时使用。

### `tidb_projection_concurrency`

- 作用域：SESSION | GLOBAL
- 默认值：4
- 这个变量用来设置 `Projection` 算子的并发度。

### `tidb_query_log_max_len`

- 作用域：INSTANCE
- 默认值：4096 (bytes)
- 最长的 SQL 输出长度。当语句的长度大于 query-log-max-len，将会被截断输出。

示例：

{{< copyable "sql" >}}

```sql
set tidb_query_log_max_len = 20;
```

### `tidb_pprof_sql_cpu` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：INSTANCE
- 默认值：0
- 这个变量用来控制是否在 profile 输出中标记出对应的 SQL 语句，用于定位和排查性能问题。

### `tidb_record_plan_in_slow_log`

- 作用域：INSTANCE
- 默认值：1
- 这个变量用于控制是否在 slow log 里包含慢查询的执行计划。

### `tidb_replica_read` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：leader
- 这个变量用于控制 TiDB 读取数据的位置，有以下三个选择：

    * leader：只从 leader 节点读取
    * follower：只从 follower 节点读取
    * leader-and-follower：从 leader 或 follower 节点读取

更多细节，见 [Follower Read](/follower-read.md)。

### `tidb_retry_limit`

- 作用域：SESSION | GLOBAL
- 默认值：10
- 这个变量用来设置最大重试次数。一个事务执行中遇到可重试的错误（例如事务冲突、事务提交过慢或表结构变更）时，会根据该变量的设置进行重试。注意当 `tidb_retry_limit = 0` 时，也会禁用自动重试。

### `tidb_row_format_version`

- 作用域：GLOBAL

- 默认值：2

- 控制新保存数据的表数据格式版本。TiDB v4.0 中默认使用版本号为 2 的[新表数据格式](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)保存新数据。

- 但如果从 4.0.0 之前的版本升级到 4.0.0，不会改变表数据格式版本，TiDB 会继续使用版本为 1 的旧格式写入表中，即**只有新创建的集群才会默认使用新表数据格式**。

- 需要注意的是修改该变量不会对已保存的老数据产生影响，只会对修改变量后的新写入数据使用对应版本格式保存。

### `tidb_scatter_region`

- 作用域：GLOBAL

- 默认值：0

- TiDB 默认会在建表时为新表分裂 Region。开启该变量后，会在建表语句执行时，同步打散刚分裂出的 Region。适用于批量建表后紧接着批量写入数据，能让刚分裂出的 Region 先在 TiKV 分散而不用等待 PD 进行调度。为了保证后续批量写入数据的稳定性，建表语句会等待打散 Region 完成后再返回建表成功，建表语句执行时间会是关闭该变量的数倍。

### `tidb_skip_isolation_level_check`

- 作用域：SESSION | GLOBAL

- 默认值：0

- 开启这个开关之后，如果对 `tx_isolation` 赋值一个 TiDB 不支持的隔离级别，不会报错，有助于兼容其他设置了（但不依赖于）不同隔离级别的应用。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### `tidb_skip_utf8_check`

- 作用域：SESSION | GLOBAL

- 默认值：0

- 这个变量用来设置是否跳过 UTF-8 字符的验证。

- 验证 UTF-8 字符需要消耗一定的性能，当可以确认输入的字符串为有效的 UTF-8 字符时，可以将其设置为 1。

### `tidb_slow_log_threshold`

- 作用域：INSTANCE

- 默认值：300

- 输出慢日志的耗时阈值。当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。默认为 300 ms。

示例：

{{< copyable "sql" >}}

```sql
set tidb_slow_log_threshold = 200;
```

### `tidb_enable_collect_execution_info`

- 作用域：INSTANCE

- 默认值：1

- 这个变量用于控制是否同时将各个执行算子的执行信息记录入 slow query log 中。

### `tidb_redact_log`

- 作用域：SESSION | GLOBAL

- 默认值：0

- 这个变量用于控制在记录 TiDB 日志和慢日志时，是否将 SQL 中的用户信息遮蔽。

- 将该变量设置为 `1` 即开启后，假设执行的 SQL 为 `insert into t values (1,2)`，在日志中记录的 SQL 会是 `insert into t values (?,?)`，即用户输入的信息被遮蔽。

### `tidb_slow_query_file`

- 作用域：SESSION

- 默认值：""

- 查询 `INFORMATION_SCHEMA.SLOW_QUERY` 只会解析配置文件中 `slow-query-file` 设置的慢日志文件名，默认是 "tidb-slow.log"。但如果想要解析其他的日志文件，可以通过设置 session 变量 `tidb_slow_query_file` 为具体的文件路径，然后查询 `INFORMATION_SCHEMA.SLOW_QUERY` 就会按照设置的路径去解析慢日志文件。更多详情可以参考 [SLOW_QUERY 文档](/identify-slow-queries.md)。

### `tidb_snapshot`

- 作用域：SESSION

- 默认值：""

- 这个变量用来设置当前会话期待读取的历史数据所处时刻。比如当设置为 `"2017-11-11 20:20:20"` 时或者一个 TSO 数字 "400036290571534337"，当前会话将能读取到该时刻的数据。

### `tidb_stmt_summary_history_size` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：24（受配置文件影响，这里给出的是默认配置文件取值）

- 这个变量设置了 statement summary 的历史记录容量。

### `tidb_stmt_summary_internal_query` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：0（受配置文件影响，这里给出的是默认配置文件取值）

- 这个变量用来控制是否在 statement summary 中包含 TiDB 内部 SQL 的信息。

### `tidb_stmt_summary_max_sql_length` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：4096（受配置文件影响，这里给出的是默认配置文件取值）

- 这个变量控制 statement summary 显示的 SQL 字符串长度。

### `tidb_stmt_summary_max_stmt_count` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：200（受配置文件影响，这里给出的是默认配置文件取值）

- 这个变量设置了 statement summary 在内存中保存的语句的最大数量。

### `tidb_stmt_summary_refresh_interval` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：1800（受配置文件影响，这里给出的是默认配置文件取值）

- 这个变量设置了 statement summary 的刷新时间，单位为秒。

### `tidb_store_limit` <span class="version-mark">从 v3.0.4 和 v4.0 版本开始引入</span>

- 作用域：INSTANCE | GLOBAL

- 默认值：0

- 这个变量用于限制 TiDB 同时向 TiKV 发送的请求的最大数量，0 表示没有限制。

### `tidb_txn_mode`

- 作用域：SESSION | GLOBAL

- 默认值："pessimistic"

- 这个变量用于设置事务模式。TiDB v3.0 支持了悲观事务，自 v3.0.8 开始，默认使用[悲观事务模式](/pessimistic-transaction.md)。

- 但如果从 3.0.7 及之前的版本升级到 >= 3.0.8 的版本，不会改变默认事务模型，即**只有新创建的集群才会默认使用悲观事务模型**。

- 将该变量设置为 "optimistic" 或 "" 时，将会使用[乐观事务模式](/optimistic-transaction.md)。

### `tidb_use_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：on

- 这个变量用于控制是否开启执行计划绑定功能，默认打开，可通过赋值 off 来关闭。关于执行计划绑定功能的使用可以参考[执行计划绑定文档](/sql-plan-management.md#创建绑定)。

### `tidb_wait_split_region_finish`

- 作用域：SESSION

- 默认值：1

- 由于打散 region 的时间可能比较长，主要由 PD 调度以及 TiKV 的负载情况所决定。这个变量用来设置在执行 `SPLIT REGION` 语句时，是否同步等待所有 region 都打散完成后再返回结果给客户端。默认 1 代表等待打散完成后再返回结果。0 代表不等待 Region 打散完成就返回。

- 需要注意的是，在 region 打散期间，对正在打散 region 上的写入和读取的性能会有一定影响，对于批量写入，导数据等场景，还是建议等待 region 打散完成后再开始导数据。

### `tidb_wait_split_region_timeout`

- 作用域：SESSION

- 默认值：300

- 这个变量用来设置 `SPLIT REGION` 语句的执行超时时间，单位是秒，默认值是 300 秒，如果超时还未完成，就返回一个超时错误。

### `tidb_window_concurrency` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL

- 默认值：4

- 这个变量用于设置 window 算子的并行度。

### `time_zone`

- 作用域：SESSION | GLOBAL
- 默认值：SYSTEM
- 数据库所使用的时区。这个变量值可以写成时区偏移的形式，如 '-8:00'，也可以写成一个命名时区，如 'America/Los_Angeles'。

### `transaction_isolation`

- 作用域：SESSION | GLOBAL
- 默认值：REPEATABLE-READ
- 这个变量用于设置事务隔离级别。TiDB 为了兼容 MySQL，支持可重复读 (`REPEATABLE-READ`)，但实际的隔离级别是快照隔离。详情见[事务隔离级别](/transaction-isolation-levels.md)。

### `tx_isolation`

这个变量是 `transaction_isolation` 的别名。

### `version`

- 作用域：NONE
- 默认值：5.7.25-TiDB-(tidb version)
- 这个变量的值是 MySQL 的版本和 TiDB 的版本，例如 '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'。

### `version_comment`

- 作用域：NONE
- 默认值：(string)
- 这个变量的值是 TiDB 版本号的其他信息，例如 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'。

### `wait_timeout`

- 作用域：SESSION | GLOBAL
- 默认值：0
- 这个变量表示用户会话的空闲超时，单位为秒。`0` 代表没有时间限制。

### `windowing_use_high_precision`

- 作用域：SESSION | GLOBAL
- 默认值：ON
- 这个变量用于控制计算窗口函数时是否采用高精度模式。

### `tidb_opt_prefer_range_scan`

- 作用域：SESSION
- 默认值：0
- 将该变量值设为 `1` 后，优化器总是偏好索引扫描而不是全表扫描。
- 在以下示例中，`tidb_opt_prefer_range_scan` 开启前，TiDB 优化器需要执行全表扫描。`tidb_opt_prefer_range_scan` 开启后，优化器选择了索引扫描。

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
3 rows in set (0.00 sec)
```

### `tidb_enable_rate_limit_action`

- 作用域：SESSION | GLOBAL
- 默认值：ON
- 这个变量控制是否为读数据的算子开启动态内存控制功能。读数据的算子默认启用 [`tidb_disql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 所允许的最大线程数来读取数据。当单条 SQL 语句的内存使用每超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 一次，读数据的算子会停止一个线程。
- 当读数据的算子只剩 1 个线程且当单条 SQL 语句的内存使用继续超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，该 SQL 语句会触发其它的内存控制行为，例如[落盘](/tidb-configuration-file.md#spilled-file-encryption-method)。

### `tidb_memory_usage_alarm_ratio`

- 作用域：SESSION
- 默认值：0.8
- TiDB 内存使用占总内存的比例超过一定阈值时会报警。该功能的详细介绍和使用方法可以参考 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入)。
- 该变量的初始值可通过 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入) 进行配置。

### `tidb_track_aggregate_memory_usage` <!-- 从 v5.0.0-rc 版本开始引入 -->

> **警告：**
>
> `tidb_track_aggregate_memory_usage` 目前为实验特性，不建议在生产环境中使用。

- 作用域：SESSION | GLOBAL
- 默认值：OFF
- 这个变量表示是否追踪聚合函数的内存使用情况。当开启该功能时，聚合函数的内存使用情况会被统计，进而可能会造成整个 SQL 内存统计值超阈值 [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query)，然后被 [`oom-action`](/tidb-configuration-file.md#oom-action) 定义的行为影响。

### `tidb_enable_async_commit` <!-- 从 v5.0.0-rc 版本开始引入 -->

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。目前存在已知问题有：
>
> + 暂时与 [TiCDC](/ticdc/ticdc-overview.md) 不兼容，可能导致 TiCDC 运行不正常。
> + 暂时与 [Compaction Filter](/tikv-configuration-file.md#enable-compaction-filter) 不兼容，共同使用时有小概率发生写丢失。
> + 本特性与 TiDB Binlog 不兼容，开启 TiDB Binlog 时本配置将不生效。 

- 作用域：SESSION | GLOBAL
- 默认值：OFF
- 该变量控制是否启用 Async Commit 特性，使事务两阶段提交的第二阶段于后台异步进行。开启本特性能降低事务提交的延迟。

> **警告：**
>
> 开启本特性时，默认不保证事务的外部一致性。具体请参考 [`tidb_guarantee_external_consistency`](#tidb_guarantee_external_consistency) 系统变量。

### `tidb_guarantee_external_consistency` <!-- 从 v5.0.0-rc 版本开始引入 -->

- 作用域：SESSION | GLOBAL
- 默认值：OFF
- 该变量控制在开启 Async Commit <!--和一阶段提交-->特性时，是否需要保证外部一致性。该选项关闭时，如果两个事务修改的内容没有交集，其他事务观测到它们的提交顺序可能与它们实际的提交顺序不一致。在不使用 Async Commit <!--或一阶段提交-->特性时，无论该选项是否开启，都能保证外部一致性。
