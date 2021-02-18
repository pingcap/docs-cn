---
title: 系统变量
aliases: ['/docs-cn/v2.1/system-variables/','/docs-cn/v2.1/reference/configuration/tidb-server/mysql-variables/']
---

# 系统变量

MySQL 系统变量 (System Variables) 是一些系统参数，用于调整数据库运行时的行为，根据变量的作用范围分为全局范围有效（Global Scope）以及会话级别有效（Session Scope）。TiDB 支持 MySQL5.7 的所有系统变量，大部分变量仅仅是为了兼容性而支持，不会影响运行时行为。

## 设置系统变量

通过 [`SET` 语句](/sql-statements/sql-statement-set-variable.md) 可以修改系统变量的值。进行修改时，还要考虑变量可修改的范围，不是所有的变量都能在全局/会话范围内进行修改。具体的可修改范围参考 [MySQL 动态变量文档](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html)。

### 全局范围值

* 在变量名前加 `GLOBAL` 关键词或者是使用 `@@global.` 作为修饰符:

<<<<<<< HEAD
    ```sql
    SET GLOBAL autocommit = 1;
    SET @@global.autocommit = 1;
    ```
=======
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

- 作用域：SESSION
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

### `tidb_enable_clustered_index` <span class="version-mark">从 v5.0.0-rc 版本开始引入</span>

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
>>>>>>> 6bd9362e... Update system-variables.md (#5531)

> **注意：**
>
> 在分布式 TiDB 中，`GLOBAL` 变量的设置会持久化到存储层中，单个 TiDB 实例每 2 秒会主动进行一次全变量的获取并形成 `gvc` (global variables cache) 缓存，该缓存有效时间最多可持续 2 秒。在设置 `GLOBAL` 变量之后，为了保证新会话的有效性，请确保两个操作之间的间隔大于 2 秒。相关细节可以查看 [Issue #14531](https://github.com/pingcap/tidb/issues/14531)。

### 会话范围值

* 在变量名前加 `SESSION` 关键词或者是使用 `@@session.` 作为修饰符，或者是不加任何修饰符:

    ```sql
    SET SESSION autocommit = 1;
    SET @@session.autocommit = 1;
    SET @@autocommit = 1;
    ```

* `LOCAL` 以及 `@@local.` 是 `SESSION` 以及 `@@session.` 的同义词

### 系统变量的作用机制

* 会话范围的系统变量仅仅会在创建会话时才会根据全局范围系统变量初始化自己的值。更改全局范围的系统变量不会改变已经创建的会话正在使用的系统变量的值。

    ```sql
    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | ON                  |
    +---------------------+
    1 row in set (0.00 sec)

    mysql> SELECT @@SESSION.autocommit;
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)

    mysql> SET GLOBAL autocommit = OFF;
    Query OK, 0 rows affected (0.01 sec)

    mysql> SELECT @@SESSION.autocommit; -- 会话范围的系统变量不会改变，会话中执行的事务依旧是以自动提交的形式来进行。
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)

    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | OFF                 |
    +---------------------+
    1 row in set (0.00 sec)

    mysql> exit
    Bye
    $ mysql -h127.0.0.1 -P4000 -uroot -D test
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 3
    Server version: 5.7.25-TiDB-None MySQL Community Server (Apache License 2.0)

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SELECT @@SESSION.autocommit; -- 新建的会话会使用新的全局变量。
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

> **注意：**
>
> `max_execution_time` 目前对所有类型的 `statement` 生效，并非只对 `SELECT` 语句生效。实际精度在 100ms 级别，而非更准确的毫秒级别。

## TiDB 特有的系统变量

参见 [TiDB 专用系统变量](/tidb-specific-system-variables.md)。
