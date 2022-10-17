---
title: 系统变量
aliases: ['/docs-cn/dev/system-variables/','/docs-cn/dev/reference/configuration/tidb-server/mysql-variables/','/docs-cn/dev/tidb-specific-system-variables/','/docs-cn/dev/reference/configuration/tidb-server/tidb-specific-variables/','/zh/tidb/dev/tidb-specific-system-variables/']
---

# 系统变量

TiDB 系统变量的行为与 MySQL 相似，变量的作用范围可以是会话级别有效 (Session Scope) 或全局范围有效 (Global Scope)。其中：

- 对 `SESSION` 作用域变量的更改，设置后**只影响当前会话**。
- 对 `GLOBAL` 作用域变量的更改，设置后立即生效。如果该变量也有 `SESSION` 作用域，已经连接的所有会话 (包括当前会话) 将继续使用会话当前的 `SESSION` 变量值。
- 要设置变量值，可使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md)。

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
> 部分 `GLOBAL` 作用域的变量会持久化到 TiDB 集群中。文档中的变量有一个“是否持久化到集群”的说明，可以为“是”或者“否”。
>
> - 对于持久化到集群的变量，当该全局变量被修改后，会通知所有 TiDB 服务器刷新其系统变量缓存。在集群中增加一个新的 TiDB 服务器时，或者重启现存的 TiDB 服务器时，都将自动使用该持久化变量。
> - 对于不持久化到集群的变量，对变量的修改只对当前连接的 TiDB 实例生效。如果需要保留设置过的值，需要在 `tidb.toml` 配置文件中声明。
>
> 此外，由于应用和连接器通常需要读取 MySQL 变量，为了兼容这一需求，在 TiDB 中，部分 MySQL 的变量既可读取也可设置。例如，尽管 JDBC 连接器不依赖于查询缓存 (query cache) 的行为，但仍然可以读取和设置查询缓存。

> **注意：**
>
> 变量取较大值并不总会带来更好的性能。由于大部分变量对单个连接生效，设置变量时，还应考虑正在执行语句的并发连接数量。
>
> 确定安全值时，应考虑变量的单位：
>
> * 如果单位为线程，安全值通常取决于 CPU 核的数量。
> * 如果单位为字节，安全值通常小于系统内存的总量。
> * 如果单位为时间，单位可能为秒或毫秒。
>
> 单位相同的多个变量可能会争夺同一组资源。

## 变量参考

### `allow_auto_random_explicit_insert` <span class="version-mark">从 v4.0.3 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 是否允许在 `INSERT` 语句中显式指定含有 `AUTO_RANDOM` 属性的列的值。

### `auto_increment_increment`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 范围：`[1, 65535]`
- 控制 `AUTO_INCREMENT` 自增值字段的自增步长。该变量常与 `auto_increment_offset` 一起使用。

### `auto_increment_offset`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 范围：`[1, 65535]`
- 控制 `AUTO_INCREMENT` 自增值字段的初始值。该变量常与 `auto_increment_increment` 一起使用。示例如下：

```sql
mysql> CREATE TABLE t1 (a int not null primary key auto_increment);
Query OK, 0 rows affected (0.10 sec)

mysql> set auto_increment_offset=1;
Query OK, 0 rows affected (0.00 sec)

mysql> set auto_increment_increment=3;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (),(),(),();
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+
| a  |
+----+
|  1 |
|  4 |
|  7 |
| 10 |
+----+
4 rows in set (0.00 sec)
```

### `autocommit`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 用于设置在非显式事务时是否自动提交事务。更多信息，请参见[事务概述](/transaction-overview.md#自动提交)。

### character_set_client

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4`
- 这个变量表示从客户端发出的数据所用的字符集。有关更多 TiDB 支持的字符集和排序规则，参阅[字符集和排序规则](/character-set-and-collation.md)文档。如果需要更改字符集，建议使用 [`SET NAMES`](/sql-statements/sql-statement-set-names.md) 语句。

### character_set_connection

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4`
- 若没有为字符串常量指定字符集，该变量表示这些字符串常量所使用的字符集。

### character_set_database

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4`
- 该变量表示当前默认在用数据库的字符集，**不建议设置该变量**。选择新的默认数据库后，服务器会更改该变量的值。

### character_set_results

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4`
- 该变量表示数据发送至客户端时所使用的字符集。

### character_set_server

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4`
- 当 `CREATE SCHEMA` 中没有指定字符集时，该变量表示这些新建的表结构所使用的字符集。

### `collation_connection`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4_bin`
- 该变量表示连接中所使用的排序规则。与 MySQL 中的 `collation_connection` 一致。

### `collation_database`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4_bin`
- 该变量表示当前数据库默认所使用的排序规则。与 MySQL 中的 `collation_database` 一致。**不建议设置此变量**，当前使用的数据库变动时，此变量会被 TiDB 修改。

### `collation_server`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`utf8mb4_bin`
- 该变量表示创建数据库时默认的排序规则。

### `cte_max_recursion_depth`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1000`
- 范围：`[0, 4294967295]`
- 这个变量用于控制公共表表达式的最大递归深度。

### `datadir`

- 作用域：NONE
- 默认值：/tmp/tidb
- 这个变量表示数据存储的位置，位置可以是本地路径。如果数据存储在 TiKV 上，则可以是指向 PD 服务器的路径。
- 如果变量值的格式为 `ip_address:port`，表示 TiDB 在启动时连接到的 PD 服务器。

### `ddl_slow_threshold`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`300`
- 单位：毫秒
- 耗时超过该阈值的 DDL 操作会被输出到日志。

### `default_authentication_plugin`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`mysql_native_password`
- 可选值：`mysql_native_password`，`caching_sha2_password`，`tidb_sm3_password`
- 服务器和客户端建立连接时，这个变量用于设置服务器对外通告的默认身份验证方式。如要了解该变量的其他可选值，参见[可用的身份验证插件](/security-compatibility-with-mysql.md#可用的身份验证插件)。
- 若要在用户登录时使用 `tidb_sm3_password` 插件，需要使用 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3) 进行连接。

### `foreign_key_checks`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 为保持兼容，TiDB 对外键检查返回 `OFF`。

### `hostname`

- 作用域：NONE
- 默认值：（系统主机名）
- 这个变量一个只读变量，表示 TiDB server 的主机名。

### `identity` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 该变量为变量 [`last_insert_id`](#last_insert_id-从-v530-版本开始引入) 的别名。

### `init_connect`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：""
- 用户首次连接到 TiDB 服务器时，`init_connect` 特性允许 TiDB 自动执行一条或多条 SQL 语句。如果你有 `CONNECTION_ADMIN` 或者 `SUPER` 权限，这些 SQL 语句将不会被自动执行。如果这些语句执行报错，你的用户连接将被终止。

### `innodb_lock_wait_timeout`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`50`
- 范围：`[1, 3600]`
- 单位：秒
- 悲观事务语句等锁时间。

### `interactive_timeout`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`28800`
- 范围：`[1, 31536000]`
- 单位：秒
- 该变量表示交互式用户会话的空闲超时。交互式用户会话是指使用 `CLIENT_INTERACTIVE` 选项调用 [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API 建立的会话（例如：MySQL shell 客户端）。该变量与 MySQL 完全兼容。

### `last_insert_id` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 返回由 INSERT 语句产生的最新 `AUTO_INSCRENT` 或者 `AUTO_RANDOM` 值，与 `LAST_INSERT_ID()` 的返回的结果相同。与 MySQL 中的 `last_insert_id` 一致。
- 作用域：SESSION
- 默认值：`0`

### `last_plan_from_binding` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`OFF`
- 该变量用来显示上一条执行的语句所使用的执行计划是否来自 binding 的[执行计划](/sql-plan-management.md)。

### `last_plan_from_cache` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来显示上一个 `execute` 语句所使用的执行计划是不是直接从 plan cache 中取出来的。

### `license`

- 作用域：NONE
- 默认值：`Apache License 2.0`
- 这个变量表示 TiDB 服务器的安装许可证。

### `max_execution_time`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 语句最长执行时间。默认值 (0) 表示无限制。

> **注意：**
>
> `max_execution_time` 目前对所有类型的语句生效，并非只对 `SELECT` 语句生效，与 MySQL 不同（只对`SELECT` 语句生效）。实际精度在 100ms 级别，而非更准确的毫秒级别。

### `max_prepared_stmt_count`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 类型：整数
- 默认值：`-1`
- 范围：`[-1, 1048576]`
- 指定一个会话中 [`PREPARE`](/sql-statements/sql-statement-prepare.md) 语句的最大数量。
- 值为 `-1` 时表示不对会话中的 `PREPARE` 语句数量进行限制。
- 如果将变量值设为超过上限 `1048576`，则使用上限值 `1048576`：

```sql
mysql> SET GLOBAL max_prepared_stmt_count = 1048577;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------+
| Level   | Code | Message                                                      |
+---------+------+--------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect max_prepared_stmt_count value: '1048577' |
+---------+------+--------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'max_prepared_stmt_count';
+-------------------------+---------+
| Variable_name           | Value   |
+-------------------------+---------+
| max_prepared_stmt_count | 1048576 |
+-------------------------+---------+
1 row in set (0.00 sec)
```

### `max_allowed_packet` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：67108864
- 取值范围：`[1024, 1073741824]`，且应当为 1024 的整数倍；若取值无法被 1024 整除，则会提示 warning 并向下取整。例如设置为 1025 时，则 TiDB 中的实际取值为 1024。
- 服务器端和客户端在一次传送数据包的过程中所允许最大的数据包大小，单位为字节。
- 该变量的行为与 MySQL 兼容。

### `plugin_dir`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：""
- 指定加载插件的目录。

### `plugin_load`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：""
- 指定 TiDB 启动时加载的插件，多个插件之间用逗号（,）分隔。

### `port`

- 作用域：NONE
- 默认值：`4000`
- 范围：`[0, 65535]`
- 使用 MySQL 协议时 tidb-server 监听的端口。

### `rand_seed1`

- 作用域：SESSION
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 该变量用于为 SQL 函数 `RAND()` 中使用的随机值生成器添加种子。
- 该变量的行为与 MySQL 兼容。

### rand_seed2

- 作用域：SESSION
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 该变量用于为 SQL 函数 `RAND()` 中使用的随机值生成器添加种子。
- 该变量的行为与 MySQL 兼容。

### require_secure_transport <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 该变量控制是否所有 TiDB 的连接都在本地 socket 上进行通信，或使用 TLS。详情见[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)。
- 该变量设置为 `ON` 时，必须使用开启 TLS 的会话连接到 TiDB，防止在 TLS 配置不正确时出现锁定的情况。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`security.require-secure-transport`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### skip_name_resolve <span class="version-mark">从 v5.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 该变量控制 `tidb-server` 实例是否将主机名作为连接握手的一部分来解析。
- 当 DNS 不可靠时，可以启用该变量来提高网络性能。

> **注意：**
>
> 当 `skip_name_resolve` 设置为 `ON` 时，身份信息中包含主机名的用户将无法登录服务器。例如：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> 该示例中，建议将 `apphost` 替换为 IP 地址或通配符（`%`）。

### `socket`

- 作用域：NONE
- 默认值：""
- 使用 MySQL 协议时，tidb-server 所监听的本地 unix 套接字文件。

### `sql_mode`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- 这个变量控制许多 MySQL 兼容行为。详情见 [SQL 模式](/sql-mode.md)。

### `sql_require_primary_key` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制表是否必须有主键。启用该变量后，如果在没有主键的情况下创建或修改表，将返回错误。
- 该功能基于 MySQL 8.0 的特性 [`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)。
- 强烈推荐在使用 TiCDC 时启用改变量，因为同步数据变更至 MySQL sink 时要求表必须有主键。

### `sql_select_limit` <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`18446744073709551615`
- 范围：`[0, 18446744073709551615]`
- `SELECT` 语句返回的最大行数。

### `system_time_zone`

- 作用域：NONE
- 默认值：（随系统）
- 该变量显示首次引导启动 TiDB 时的系统时区。另请参阅 [`time_zone`](#time_zone)。

### `tidb_adaptive_closest_read_threshold` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`4096`
- 这个变量用于控制当 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 设置为 `closest-adaptive` 时，优先将读请求发送至 TiDB server 所在区域副本的阈值。当读请求预估的返回结果的大小超过此阈值时，TiDB 会将读请求优先发送至同一区域的副本，否则会发送至 leader 副本。

### `tidb_allow_batch_cop` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 范围：`[0, 2]`
- 这个变量用于控制 TiDB 向 TiFlash 发送 coprocessor 请求的方式，有以下几种取值：

    * 0：从不批量发送请求
    * 1：aggregation 和 join 的请求会进行批量发送
    * 2：所有的 cop 请求都会批量发送

### `tidb_allow_fallback_to_tikv` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：""
- 这个变量表示将 TiKV 作为备用存储引擎的存储引擎列表。当该列表中的存储引擎发生故障导致 SQL 语句执行失败时，TiDB 会使用 TiKV 作为存储引擎再次执行该 SQL 语句。目前支持设置该变量为 "" 或者 "tiflash"。如果设置该变量为 "tiflash"，当 TiFlash 返回超时错误（对应的错误码为 ErrTiFlashServerTimeout）时，TiDB 会使用 TiKV 作为存储引擎再次执行该 SQL 语句。

### `tidb_allow_function_for_expression_index` <span class="version-mark">从 v5.2.0 版本开始引入</span>

- 作用域：NONE
- 默认值：`lower, md5, reverse, tidb_shard, upper, vitess_hash`
- 这个变量用于显示创建表达式索引所允许使用的函数。

### `tidb_allow_mpp` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否使用 TiFlash 的 MPP 模式执行查询，可以设置的值包括：
    - 0 或 OFF，代表从不使用 MPP 模式
    - 1 或 ON，代表由优化器根据代价估算选择是否使用 MPP 模式（默认）

MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点之间的数据交换并提供高性能、高吞吐的 SQL 算法。MPP 模式选择的详细说明参见[控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#控制是否选择-mpp-模式)。

### `tidb_allow_remove_auto_inc` <span class="version-mark">从 v2.1.18 和 v3.0.4 版本开始引入</span>

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来控制是否允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 来移除某个列的 `AUTO_INCREMENT` 属性。默认 (`OFF`) 为不允许。

### `tidb_analyze_version` <span class="version-mark">从 v5.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`2`
- 范围：`[1, 2]`
- 这个变量用于控制 TiDB 收集统计信息的行为。
- 在 v5.3.0 及之后的版本中，该变量的默认值为 `2`，具体可参照[统计信息简介](/statistics.md)文档。如果从 v5.3.0 之前版本的集群升级至 v5.3.0 及之后的版本，`tidb_analyze_version` 的默认值不发生变化。

### `tidb_auto_analyze_end_time`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`23:59 +0000`
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的结束时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

### `tidb_auto_analyze_ratio`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0.5`
- 这个变量用来设置 TiDB 在后台自动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息的阈值。`0.5` 指的是当表中超过 50% 的行被修改时，触发自动 ANALYZE 更新。可以指定 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 来限制自动 ANALYZE 的时间

> **注意：**
>
> 当系统变量 `tidb_enable_auto_analyze` 设置为 `ON` 时，TiDB 才会触发 `auto_analyze`。

### `tidb_auto_analyze_start_time`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`00:00 +0000`
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的开始时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

### `tidb_max_auto_analyze_time` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`43200`
- 范围：`[0, 2147483647]`
- 单位：秒
- 这个变量用于指定自动 ANALYZE 的最大执行时间。当执行时间超出指定的时间时，自动 ANALYZE 会被终止。当该变量值为 0 时，自动 ANALYZE 没有最大执行时间的限制。

### `tidb_backoff_lock_fast`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`10`
- 范围：`[1, 2147483647]`
- 这个变量用来设置读请求遇到锁的 backoff 时间。

### `tidb_backoff_weight`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`2`
- 范围：`[0, 2147483647]`
- 这个变量用来给 TiDB 的 `backoff` 最大时间增加权重，即内部遇到网络或其他组件 (TiKV, PD) 故障时，发送重试请求的最大重试时间。可以通过这个变量来调整最大重试时间，最小值为 1。

    例如，TiDB 向 PD 取 TSO 的基础超时时间是 15 秒，当 `tidb_backoff_weight = 2` 时，取 TSO 的最大超时时间为：基础时间 \* 2 等于 30 秒。

    在网络环境较差的情况下，适当增大该变量值可以有效缓解因为超时而向应用端报错的情况；而如果应用端希望更快地接到报错信息，则应该尽量减小该变量的值。

### `tidb_batch_pending_tiflash_count` <span class="version-mark">从 v6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`4000`
- 范围：`[0, 2147483647]`
- 使用 `ALTER DATABASE SET TIFLASH REPLICA` 语句为 TiFlash 添加副本时，能容许的不可用表的个数上限。如果超过该上限，则会停止或者以非常慢的速度为库中的剩余表设置 TiFlash 副本。

### `tidb_broadcast_join_threshold_count` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`10240`
- 范围：`[0, 9223372036854775807]`
- 单位为行数。如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

### `tidb_broadcast_join_threshold_size` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`104857600` (100 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

### `tidb_build_stats_concurrency`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`4`
- 这个变量用来设置 ANALYZE 语句执行时并发度。
- 当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### `tidb_capture_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否开启[自动捕获绑定](/sql-plan-management.md#自动捕获绑定-baseline-capturing)功能。该功能依赖 Statement Summary，因此在使用自动绑定之前需打开 Statement Summary 开关。
- 开启该功能后会定期遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动创建绑定。

### `tidb_check_mb4_value_in_utf8`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`ON`
- 设置该变量为 `ON` 可强制只存储[基本多文种平面 (BMP)](https://zh.wikipedia.org/zh-hans/Unicode字符平面映射) 编码区段内的 `utf8` 字符值。若要存储 BMP 区段外的 `utf8` 值，推荐使用 `utf8mb4` 字符集。
- 早期版本的 TiDB 中 (v2.1.x)，`utf8` 检查更为宽松。如果你的 TiDB 集群是从早期版本升级的，推荐关闭该变量，详情参阅[升级与升级后常见问题](/faq/upgrade-faq.md)。

### tidb_committer_concurrency <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`128`
- 范围：`[1, 10000]`
- 在单个事务的提交阶段，用于执行提交操作相关请求的 goroutine 数量。
- 若提交的事务过大，事务提交时的流控队列等待耗时可能会过长。此时，可以通过调大该配置项来加速提交。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`performance.committer-concurrency`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_checksum_table_concurrency`

- 作用域：SESSION
- 默认值：`4`
- 这个变量用来设置 `ADMIN CHECKSUM TABLE` 语句执行时扫描索引的并发度。当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### `tidb_config`

- 作用域：SESSION
- 默认值：""
- 这个变量是一个只读变量，用来获取当前 TiDB Server 的配置信息。

### `tidb_constraint_check_in_place`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 该变量仅适用于乐观事务模型。悲观事务模式中的行为由 [`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 控制。
- 当这个变量设置为 `OFF` 时，唯一索引的重复值检查会被推迟到事务提交时才进行。这有助于提高性能，但对于某些应用，可能导致非预期的行为。详情见[约束](/constraints.md#乐观事务)。

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 `OFF`：

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

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 `ON`：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place=ON;
        begin optimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

### `tidb_constraint_check_in_place_pessimistic` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 该变量仅适用于悲观事务模型。乐观事务模式中的行为由 [`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place) 控制。
- 当这个变量设置为 `OFF` 时，唯一约束检查会被推迟到下一次需要对这个索引加锁的语句执行时，或事务提交时才进行。这有助于提高性能，但对于某些应用，可能导致非预期的行为。详情见[约束](/constraints.md#悲观事务)。
- 关闭该变量可能会导致悲观事务中返回 `LazyUniquenessCheckFailure` 报错。返回该错误时，TiDB 将会回滚当前事务。
- 关闭该变量后，悲观事务中不支持使用 [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md) 功能。
- 关闭该变量时，commit 语句可能会报出 `Write conflict` 错误或 `Duplicate entry` 错误，两种错误都意味着事务回滚。

    - 悲观事务模型下将 `tidb_constraint_check_in_place_pessimistic` 设置为 `OFF`：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=OFF;
        create table t (i int key);
        insert into t values (1);
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        ```sql
        tidb> commit; -- 事务提交时才检查
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

    - 悲观事务模型下将 `tidb_constraint_check_in_place_pessimistic` 设置为 `ON`：

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

### `tidb_cost_model_version` <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **警告：**
>
> - 当前 Cost Model Version 2 为实验特性，不建议在生产环境中使用。
> - 切换代价模型版本可能会引起查询计划的变动。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 可选值：`[1, 2]`
- TiDB v6.2.0 引入了代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2)，在内部测试中比此前版本的代价模型更加准确。
- 通过将 `tidb_cost_model_version` 设置为 `2` 可以启用 Cost Model Version 2 代价模型，设置为 `1` 则继续使用 Cost Model Version 1 代价模型。
- 代价模型会影响优化器对计划的选择，具体可见[代价模型](/cost-model.md)。

### `tidb_current_ts`

- 作用域：SESSION
- 默认值：`0`
- 这个变量是一个只读变量，用来获取当前事务的时间戳。

### `tidb_ddl_disk_quota` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`107374182400` (100 GiB)
- 范围：`[107374182400, 1125899906842624]` ([100 GiB, 1 PiB])
- 单位：字节
- 这个变量仅在 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 开启的情况下生效，用于设置创建索引的回填过程中本地存储空间的使用限制。

### `tidb_ddl_enable_fast_reorg` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量是用来控制是否开启添加索引加速功能，来提升创建索引回填过程的速度。如果本开关启动，TiDB 在进行创建索引任务时将会采用更加高效的方式完成索引创建。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。
>
> 当前索引加速功能与 [PITR (Point-in-time recovery)](/br/br-pitr-guide.md) 功能不兼容。在使用索引加速功能时，需要确保后台没有启动 PITR 备份任务，否则可能会出现非预期结果。非预期场景包括：
>
> - 如果先启动 PITR 备份任务，再添加索引，此时即使索引加速功能打开，也不会使用加速索引功能，但不影响索引兼容性。
> - 如果先启动添加索引加速任务，再启动 PITR 备份任务，此时 PITR 备份任务会报错，但不影响正在添加索引的任务。
> - 如果同时启动 PITR 备份任务和添加索引加速任务，可能会由于两个任务无法察觉到对方而导致 PITR 不能成功备份增加的索引数据。

### `tidb_ddl_error_count_limit`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`512`
- 范围：`[0, 9223372036854775807]`
- 这个变量用来控制 DDL 操作失败重试的次数。失败重试次数超过该参数的值后，会取消出错的 DDL 操作。

### `tidb_ddl_flashback_concurrency` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`64`
- 范围：`[1, 256]`
- 这个变量用来控制 `flashback cluster` 的并发数。

### `tidb_ddl_reorg_batch_size`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`256`
- 范围：`[32, 10240]`
- 这个变量用来设置 DDL 操作 `re-organize` 阶段的 batch size。比如 `ADD INDEX` 操作，需要回填索引数据，通过并发 `tidb_ddl_reorg_worker_cnt` 个 worker 一起回填数据，每个 worker 以 batch 为单位进行回填。

    - 如果 `ADD INDEX` 操作时有较多 `UPDATE` 操作或者 `REPLACE` 等更新操作，batch size 越大，事务冲突的概率也会越大，此时建议调小 batch size 的值，最小值是 32。
    - 在没有事务冲突的情况下，batch size 可设为较大值（需要参考 worker 数量，见[线上负载与 `ADD INDEX` 相互影响测试](/benchmark/online-workloads-and-add-index-operations.md)），最大值是 10240，这样回填数据的速度更快，但是 TiKV 的写入压力也会变大。

### `tidb_ddl_reorg_priority`

- 作用域：SESSION
- 默认值：PRIORITY_LOW
- 这个变量用来设置 `ADD INDEX` 操作 `re-organize` 阶段的执行优先级，可设置为 `PRIORITY_LOW`/`PRIORITY_NORMAL`/`PRIORITY_HIGH`。

### `tidb_ddl_reorg_worker_cnt`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`4`
- 范围：`[1, 256]`
- 这个变量用来设置 DDL 操作 `re-organize` 阶段的并发度。

### `tidb_default_string_match_selectivity` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`0.8`
- 范围：`[0, 1]`
- 这个变量用来设置过滤条件中的 `like`、`rlike`、`regexp` 函数在行数估算时的默认选择率，以及是否对这些函数启用 TopN 辅助估算。
- TiDB 总是会尝试利用统计信息对过滤条件中的 `like` 进行估算，但是当 `like` 匹配的字符串太复杂时，或者面对 `rlike` 或 `regexp` 时，往往无法充分利用统计信息，转而使用 `0.8` 作为选择率，造成行数估算的误差较大。
- 该变量可以用于修改这个行为，当变量被设为 `0` 以外的值时，会使用变量的值而不是默认的 `0.8` 作为选择率。
- 如果将该变量的值设为 `0`，TiDB 在对上述三个函数进行行数估算时，会尝试利用统计信息中的 TopN 进行求值来提高估算精度，同时也会考虑统计信息中的 NULL 数。求值操作预计会造成少量性能损耗。这个功能生效的前提是统计信息是在 [`tidb_analyze_version`](#tidb_analyze_version-从-v510-版本开始引入) 设为 `2` 时收集的。
- 当该变量的值被设为默认值以外的值的时候，会对 `not like`、`not rlike`、`not regexp` 的行数估算也进行相应的调整。

### `tidb_disable_txn_auto_retry`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来设置是否禁用显式的乐观事务自动重试，设置为 `ON` 时，不会自动重试，如果遇到事务冲突需要在应用层重试。

    如果将该变量的值设为 `OFF`，TiDB 将会自动重试事务，这样在事务提交时遇到的错误更少。需要注意的是，这样可能会导致数据更新丢失。

    这个变量不会影响自动提交的隐式事务和 TiDB 内部执行的事务，它们依旧会根据 `tidb_retry_limit` 的值来决定最大重试次数。

    关于是否需要禁用自动重试，请参考[重试的局限性](/optimistic-transaction.md#重试的局限性)。

    该变量只适用于乐观事务，不适用于悲观事务。悲观事务的重试次数由 [`max_retry_count`](/tidb-configuration-file.md#max-retry-count) 控制。

### `tidb_distsql_scan_concurrency`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`15`
- 范围：`[1, 256]`
- 这个变量用来设置 scan 操作的并发度。
- AP 类应用适合较大的值，TP 类应用适合较小的值。对于 AP 类应用，最大值建议不要超过所有 TiKV 节点的 CPU 核数。
- 若表的分区较多可以适当调小该参数（取决于扫描数据量的大小以及扫描频率），避免 TiKV 内存溢出 (OOM)。

### `tidb_dml_batch_size`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 这个变量的值大于 `0` 时，TiDB 会将 `INSERT` 或 `LOAD DATA` 等语句在更小的事务中批量提交。这样可减少内存使用，确保大批量修改时事务大小不会达到 `txn-total-size-limit` 限制。
- 只有变量值为 `0` 时才符合 ACID 要求。否则无法保证 TiDB 的原子性和隔离性要求。

### `tidb_enable_1pc` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 指定是否在只涉及一个 Region 的事务上启用一阶段提交特性。比起传统两阶段提交，一阶段提交能大幅降低事务提交延迟并提升吞吐。

> **注意：**
>
> - 对于新创建的集群，默认值为 ON。对于升级版本的集群，如果升级前是 v5.0 以下版本，升级后默认值为 `OFF`。
> - 启用 TiDB Binlog 后，开启该选项无法获得性能提升。要获得性能提升，建议使用 [TiCDC](/ticdc/ticdc-overview.md) 替代 TiDB Binlog。
> - 启用该参数仅意味着一阶段提交成为可选的事务提交模式，实际由 TiDB 自行判断选择最合适的提交模式进行事务提交。

### `tidb_enable_amend_pessimistic_txn` <span class="version-mark">从 v4.0.7 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否开启 `AMEND TRANSACTION` 特性。在[悲观事务模式](/pessimistic-transaction.md)下开启该特性后，如果该事务相关的表存在并发 DDL 操作和 SCHEMA VERSION 变更，TiDB 会尝试对该事务进行 amend 操作，修正该事务的提交内容，使其和最新的有效 SCHEMA VERSION 保持一致，从而成功提交该事务而不返回 `Information schema is changed` 报错。该特性对以下并发 DDL 变更生效：

    - `ADD COLUMN` 或 `DROP COLUMN` 类型的 DDL 操作。
    - `MODIFY COLUMN` 或 `CHANGE COLUMN` 类型的 DDL 操作，且只对增大字段长度的操作生效。
    - `ADD INDEX` 或 `DROP INDEX` 类型的 DDL 操作，且操作的索引列须在事务开启之前创建。

> **注意：**
>
> 目前该特性可能造成事务语义的变化，且与 TiDB Binlog 存在部分不兼容的场景，可以参考[事务语义行为区别](https://github.com/pingcap/tidb/issues/21069)和[与 TiDB Binlog 兼容问题汇总](https://github.com/pingcap/tidb/issues/20996)了解更多关于该特性的使用注意事项。

### `tidb_enable_analyze_snapshot` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 该变量控制 `ANALYZE` 读取历史时刻的数据还是读取最新的数据。当该变量设置为 `ON` 时，`ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据。当该变量设置为 `OFF` 时，`ANALYZE` 读取最新的数据。
- 在 v5.2 之前，`ANALYZE` 读取最新的数据。v5.2 至 v6.1 版本 `ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据。

> **警告：**
>
> 如果 `ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据，长时间的 `AUTO ANALYZE` 可能会因为历史数据被 GC 而出现 `GC life time is shorter than transaction duration` 的报错。

### `tidb_enable_async_commit` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 该变量控制是否启用 Async Commit 特性，使事务两阶段提交的第二阶段于后台异步进行。开启本特性能降低事务提交的延迟。

> **注意：**
>
> - 对于新创建的集群，默认值为 ON。对于升级版本的集群，如果升级前是 v5.0 以下版本，升级后默认值为 `OFF`。
> - 启用 TiDB Binlog 后，开启该选项无法获得性能提升。要获得性能提升，建议使用 [TiCDC](/ticdc/ticdc-overview.md) 替代 TiDB Binlog。
> - 启用该参数仅意味着 Async Commit 成为可选的事务提交模式，实际由 TiDB 自行判断选择最合适的提交模式进行事务提交。

### `tidb_enable_auto_analyze` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 该变量控制 TiDB 是否以后台操作自动更新表的统计信息。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`performance.run-auto-analyze`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_enable_auto_increment_in_generated`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否允许在创建生成列或者表达式索引时引用自增列。

### `tidb_enable_cascades_planner`

> **警告：**
>
> 目前 cascades planner 为实验特性，不建议在生产环境中使用。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否开启 cascades planner。

### `tidb_enable_chunk_rpc` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`ON`
- 这个变量用来设置是否启用 Coprocessor 的 `Chunk` 数据编码格式。

### `tidb_enable_clustered_index` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 可选值：`OFF`，`ON`，`INT_ONLY`
- 这个变量用于控制默认情况下表的主键是否使用[聚簇索引](/clustered-indexes.md)。“默认情况”即不显式指定 `CLUSTERED`/`NONCLUSTERED` 关键字的情况。可设置为 `OFF`/`ON`/`INT_ONLY`。
    - `OFF` 表示所有主键默认使用非聚簇索引。
    - `ON` 表示所有主键默认使用聚簇索引。
    - `INT_ONLY` 此时的行为受配置项 `alter-primary-key` 控制。如果该配置项取值为 `true`，则所有主键默认使用非聚簇索引；如果该配置项取值为 `false`，则由单个整数类型的列构成的主键默认使用聚簇索引，其他类型的主键默认使用非聚簇索引。

### `tidb_enable_collect_execution_info`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`ON`
- 这个变量用于控制是否同时将各个执行算子的执行信息记录入 slow query log 中。

### `tidb_enable_column_tracking` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 收集 `PREDICATE COLUMNS` 的统计信息目前为实验特性，不建议在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否开启 TiDB 对 `PREDICATE COLUMNS` 的收集。关闭该变量后，之前收集的 `PREDICATE COLUMNS` 会被清除。详情见[收集部分列的统计信息](/statistics.md#收集部分列的统计信息)。

### `tidb_enable_concurrent_ddl` <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **警告：**
>
> **请勿修改该变量值**，因为关闭后风险不确定，有可能导致集群元数据出错。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否让 TiDB 使用并发 DDL 语句。在开启并发 DDL 语句后，DDL 语句的执行流程有所改变，DDL 语句不容易被其他 DDL 语句阻塞，并且能够同时添加多个索引。 

### `tidb_enable_enhanced_security`

- 作用域：NONE
- 默认值：`OFF`
- 这个变量表示所连接的 TiDB 服务器是否启用了安全增强模式 (SEM)。若要改变该变量值，你需要在 TiDB 服务器的配置文件中修改 `enable-sem` 项的值，并重启 TiDB 服务器。
- 安全增强模式受[安全增强式 Linux](https://zh.wikipedia.org/wiki/安全增强式Linux) 等系统设计的启发，削减拥有 MySQL `SUPER` 权限的用户能力，转而使用细粒度的 `RESTRICTED` 权限作为替代。这些细粒度的 `RESTRICTED` 权限如下：
    - `RESTRICTED_TABLES_ADMIN`：能够写入 `mysql` 库中的系统表，能查看 `information_schema` 表上的敏感列。
    - `RESTRICTED_STATUS_ADMIN`：能够在 `SHOW STATUS` 命令中查看敏感内容。
    - `RESTRICTED_VARIABLES_ADMIN`：能够在 `SHOW [GLOBAL] VARIABLES` 和 `SET` 命令中查看和设置包含敏感内容的变量。
    - `RESTRICTED_USER_ADMIN`：能够阻止其他用户更改或删除用户帐户。

### `tidb_restricted_read_only` <span class="version-mark">从 v5.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 可选值：`OFF` 和 `ON`
- `tidb_restricted_read_only`和 [`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 的作用相似。在大多数情况下，你只需要使用 [`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 即可。
- 拥有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改该变量。如果 TiDB 开启了[安全增强模式](#tidb_enable_enhanced_security)，你还需要额外的 `RESTRICTED_VARIABLES_ADMIN` 权限才能读取或修改该变量。
- `tidb_restricted_read_only` 的设置将影响 [`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 的值：

    - 当设置 `tidb_restricted_read_only` 为 `ON` 时，[`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 的将自动被设置为 `ON`。
    - 当设置 `tidb_restricted_read_only` 为 `OFF` 时，[`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 的值将不受影响。
    - 当 `tidb_restricted_read_only` 为 `ON` 时，[`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 的值无法设置为 `OFF`。

- 对于 TiDB 的 DBaaS 供应商，当 TiDB 为另一个数据库的下游数据库时，如果要将整个 TiDB 集群设置为只读模式，你需要开启[安全增强模式](#tidb_enable_enhanced_security) 并将 `tidb_restricted_read_only` 设置为 `ON`，从而防止你的用户通过 [`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入) 将 TiDB 集群设置为可写。实现方法：首先开启[安全增强模式](#tidb_enable_enhanced_security)，然后由你（作为 DBaaS 的控制面）使用一个 admin 用户控制 `tidb_restricted_read_only`（需要拥有 `SYSTEM_VARIABLES_ADMIN` 和 `RESTRICTED_VARIABLES_ADMIN` 权限），由你的数据库用户使用 root 用户控制 [`tidb_super_read_only`](#tidb_super_read_only-从-v531-版本开始引入)（需要拥有 `SUPER` 权限）。
- 该变量可以控制整个集群的只读状态。开启后（即该值为 `ON`），整个集群中的 TiDB 服务器都将进入只读状态，只有 `SELECT`、`USE`、`SHOW` 等不会修改数据的语句才能被执行，其他如 `INSERT`、`UPDATE` 等语句会被拒绝执行。
- 该变量开启只读模式只保证整个集群最终进入只读模式，当变量修改状态还没被同步到其他 TiDB 服务器时，尚未同步的 TiDB 仍然停留在非只读模式。
- 在执行 SQL 语句之前，TiDB 会检查集群的只读标志。从 v6.2.0 起，在提交 SQL 语句之前，TiDB 也会检查该标志，从而防止在服务器被置于只读模式后某些长期运行的 [auto commit](/transaction-overview.md#自动提交) 语句可能修改数据的情况。
- 在变量开启时，对于尚未提交的事务：
    - 如果有尚未提交的只读事务，可正常提交该事务。
    - 如果尚未提交的事务为非只读事务，在事务内执行写入的 SQL 语句会被拒绝。
    - 如果尚未提交的事务已经有数据改动，其提交也会被拒绝。
- 当集群开启只读模式后，所有用户（包括 `SUPER` 用户）都无法执行可能写入数据的 SQL 语句，除非该用户被显式地授予了 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。

### `tidb_enable_exchange_partition`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`ON`
- 该变量用于设置是否启用 [`exchange partitions with tables`](/partitioned-table.md#分区管理) 特性。默认值为 `ON`，即默认开启该功能。
- 该变量自 v6.3.0 开始废弃，其取值将固定为默认值 `ON`，即默认开启 `exchange partitions with tables`。

### `tidb_enable_fast_analyze`

> **警告：**
>
> 目前快速分析功能为实验特性，不建议在生产环境中使用。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来控制是否启用统计信息快速分析功能。默认值 0 表示不开启。
- 快速分析功能开启后，TiDB 会随机采样约 10000 行的数据来构建统计信息。因此在数据分布不均匀或者数据量比较少的情况下，统计信息的准确度会比较低。这可能导致执行计划不优，比如选错索引。如果可以接受普通 `ANALYZE` 语句的执行时间，则推荐关闭快速分析功能。

### `tidb_enable_foreign_key` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否开启 `FOREIGN KEY` 特性。

### `tidb_enable_general_plan_cache` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来控制是否开启 General Plan Cache。

### `tidb_enable_index_merge` <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> - 当集群从 v4.0.0 以下版本升级到 v5.4.0 及以上版本时，该变量开关默认关闭，防止升级后计划发生变化导致回退。
> - 当集群从 v4.0.0 及以上版本升级到 v5.4.0 及以上版本时，该变量开关保持升级前的状态。
> - 对于 v5.4.0 及以上版本的新建集群，该变量开关默认开启。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否开启 index merge 功能。

### tidb_enable_legacy_instance_scope <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于允许使用 `SET SESSION` 对 `INSTANCE` 作用域的变量进行设置，用法同 `SET GLOBAL`。
- 为了兼容之前的 TiDB 版本，该变量值默认为 `ON`。

### `tidb_enable_list_partition` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来设置是否开启 `LIST (COLUMNS) TABLE PARTITION` 特性。

### `tidb_enable_metadata_lock` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置是否开启[元数据锁](/metadata-lock.md)特性。需要注意，在设置该变量时，集群中不能有 DDL 任务，以免造成非预期数据正确性、一致性问题。

### `tidb_enable_mutation_checker` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于设置是否开启 mutation checker。mutation checker 是一项在 DML 语句执行过程中进行的数据索引一致性校验，校验报错会回滚当前语句。开启该校验会导致 CPU 使用轻微上升。详见[数据索引一致性报错](/troubleshoot-data-inconsistency-errors.md)。
- 对于新创建的 v6.0.0 及以上的集群，默认值为 `ON`。对于升级版本的集群，如果升级前是低于 v6.0.0 的版本，升级后默认值为 `OFF`。

### `tidb_enable_noop_functions` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 默认情况下，用户尝试将某些语法用于尚未实现的功能时，TiDB 会报错。若将该变量值设为 `ON`，TiDB 则自动忽略此类功能不可用的情况，即不会报错。若用户无法更改 SQL 代码，可考虑将变量值设为 `ON`。
- 启用 `noop` 函数可以控制以下行为：
    * `LOCK IN SHARE MODE` 语法
    * `SQL_CALC_FOUND_ROWS` 语法
    * `START TRANSACTION READ ONLY` 和 `SET TRANSACTION READ ONLY` 语法
    * `tx_read_only`、`transaction_read_only`、`offline_mode`、`super_read_only`、`read_only` 以及 `sql_auto_is_null` 系统变量
    * `GROUP BY <expr> ASC|DESC` 语法

> **警告：**
>
> 该变量只有在默认值 `OFF` 时，才算是安全的。因为设置 `tidb_enable_noop_functions=1` 后，TiDB 会自动忽略某些语法而不报错，这可能会导致应用程序出现异常行为。例如，允许使用语法 `START TRANSACTION READ ONLY` 时，事务仍会处于读写模式。

### `tidb_enable_noop_variables` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 若该变量值为 `OFF`，TiDB 具有以下行为：
    * 使用 `SET` 设置 `noop` 的系统变量时会报 `"setting *variable_name* has no effect in TiDB"` 的警告。
    * `SHOW [SESSION | GLOBAL] VARIABLES` 的结果不显示 `noop` 的系统变量。
    * 使用 `SELECT` 读取 `noop` 的系统变量时会报 `"variable *variable_name* has no effect in TiDB"` 的警告。
- 你可以通过 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;` 语句来检查 TiDB 实例是否曾设置和读取 `noop` 系统变量。

### `tidb_enable_null_aware_anti_join` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION ｜GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制 TiDB 对特殊集合算子 `NOT IN` 和 `!= ALL` 引导的子查询产生的 ANTI JOIN 是否采用 Null Aware Hash Join 的执行方式。

### `tidb_enable_outer_join_reorder` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：在 v6.1.0 中为 `ON`，即默认开启。在 v6.1.0 之后的版本中为 `OFF`，即默认关闭。
- 自 v6.1.0 起，TiDB 的 [Join Reorder 算法](/join-reorder.md) 开始支持 Outer Join。该变量用于控制这个支持行为。默认关闭，即不启用 Outer Join 的 Join Reorder。
- 对于从 v6.1.0 之前版本升级到 v6.1.0 及之后的版本，该变量的默认值为 `OFF`。对于从 v6.1.0 版本升级到之后的版本，该变量默认值为 `ON`。

### `tidb_enable_ordered_result_mode`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 指定是否对最终的输出结果进行自动排序。
- 例如，开启该变量后，TiDB 会将 `SELECT a, MAX(b) FROM t GROUP BY a` 处理为 `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`。

### `tidb_enable_paging` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制 `IndexLookUp` 算子是否使用分页 (paging) 方式发送 Coprocessor 请求。
- 适用场景：对于使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 无法下推到 `IndexScan` 上的读请求，可能会出现读请求的延迟高、TiKV 的 Unified read pool CPU 使用率高的情况。在这种情况下，由于 `Limit` 算子只需要少部分数据，开启 `tidb_enable_paging`，能够减少处理数据的数量，从而降低延迟、减少资源消耗。
- 开启 `tidb_enable_paging` 后，`Limit` 无法下推且数量小于 `960` 的 `IndexLookUp` 请求会使用 paging 方式发送 Coprocessor 请求。`Limit` 的值越小，优化效果会越明显。

### `tidb_enable_parallel_apply` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：0
- 这个变量用于控制是否开启 Apply 算子并发，并发数由 `tidb_executor_concurrency` 变量控制。Apply 算子用来处理关联子查询且默认无并发，所以执行速度较慢。打开 Apply 并发开关可增加并发度，提高执行速度。目前默认关闭。

### `tidb_enable_prepared_plan_cache` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制是否开启 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。开启后，对 `Prepare`、`Execute` 请求的执行计划会进行缓存，以便在后续执行时跳过查询计划优化这个步骤，获得性能上的提升。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.enabled`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_enable_pseudo_for_outdated_stats` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来控制优化器在一张表上的统计信息过期时的行为。
- 统计信息过期的判断标准：最近一次对某张表执行 `ANALYZE` 获得统计信息后，该表数据被修改的行数大于该表总行数的 80%，便可判定该表的统计信息已过期。该比例可通过 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) 配置参数调整。
- 默认情况下（即该变量值为 `OFF` 时），某张表上的统计信息过期后，优化器仍会使用该表上的统计信息。将该变量值设为 `ON` 时，当统计信息过期后，优化器认为该表上除总行数以外的统计信息不再可靠，转而使用 pseudo 统计信息。
- 如果表数据修改较频繁，没有及时对表执行 `ANALYZE`，但又希望执行计划保持稳定，推荐将该变量值设为 `OFF`。

### `tidb_enable_rate_limit_action`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量控制是否为读数据的算子开启动态内存控制功能。读数据的算子默认启用 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 所允许的最大线程数来读取数据。当单条 SQL 语句的内存使用每超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 一次，读数据的算子会停止一个线程。
- 当读数据的算子只剩 1 个线程且当单条 SQL 语句的内存使用继续超过 `tidb_mem_quota_query` 时，该 SQL 语句会触发其它的内存控制行为，例如[落盘](/tidb-configuration-file.md#oom-use-tmp-storage)。
- 该变量在单条查询仅涉及读数据的情况下，对内存控制效果较好。若还存在额外的计算操作（如连接、聚合等），打开该变量可能会导致内存不受 `tidb_mem_quota_query` 控制，加剧 OOM 风险。

### `tidb_enable_slow_log`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`ON`
- 这个变量用于控制是否开启 slow log 功能。

### `tidb_enable_stmt_summary` <span class="version-mark">从 v3.0.4 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制是否开启 statement summary 功能。如果开启，SQL 的耗时等执行信息将被记录到系统表 `information_schema.STATEMENTS_SUMMARY` 中，用于定位和排查 SQL 性能问题。

### `tidb_enable_strict_double_type_check` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制是否可以用 `DOUBLE` 类型的无效定义创建表。该设置的目的是提供一个从 TiDB 早期版本升级的方法，因为早期版本在验证类型方面不太严格。
- 该变量的默认值 `ON` 与 MySQL 兼容。

例如，由于无法保证浮点类型的精度，现在将 `DOUBLE(10)` 类型视为无效。将 `tidb_enable_strict_double_type_check` 更改为 `OFF` 后，将会创建表。如下所示：

```sql
CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use
SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)
CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **注意：**
>
> 该设置仅适用于 `DOUBLE` 类型，因为 MySQL 允许为 `FLOAT` 类型指定精度。从 MySQL 8.0.17 开始已弃用此行为，不建议为 `FLOAT` 或 `DOUBLE` 类型指定精度。

### `tidb_enable_table_partition`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 可选值：`OFF`，`ON`，`AUTO`
- 这个变量用来设置是否开启 `TABLE PARTITION` 特性。目前变量支持以下三种值：
    - 默认值 `ON` 表示开启 TiDB 当前已实现了的分区表类型，目前 Range partition、Hash partition 以及 Range column 单列的场景会生效。
    - `AUTO` 目前作用和 `ON` 一样。
    - `OFF` 表示关闭 `TABLE PARTITION` 特性，此时语法还是保持兼容，只是创建的表并不是真正的分区表，而是普通的表。

### `tidb_enable_telemetry` <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于动态地控制 TiDB 遥测功能是否开启。设置为 `OFF` 可以关闭 TiDB 遥测功能。当所有 TiDB 实例都设置 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 为 `false` 时将忽略该系统变量并总是关闭 TiDB 遥测功能。参阅[遥测](/telemetry.md)了解该功能详情。

### `tidb_enable_tiflash_read_for_write_stmt` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制写 SQL 中的读取是否会下推到 TiFlash。

### `tidb_enable_top_sql` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> Top SQL 目前是实验性功能，不建议在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用控制是否开启 [Top SQL 特性](/dashboard/top-sql.md)。

### `tidb_enable_tso_follower_proxy` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来开启 TSO Follower Proxy 特性。当该值为 `OFF` 时，TiDB 仅会从 PD leader 获取 TSO。开启该特性之后，TiDB 在获取 TSO 时会将请求均匀地发送到所有 PD 节点上，通过 PD follower 转发 TSO 请求，从而降低 PD leader 的 CPU 压力。
- 适合开启 TSO Follower Proxy 的场景：
    * PD leader 因高压力的 TSO 请求而达到 CPU 瓶颈，导致 TSO RPC 请求的延迟较高。
    * 集群中的 TiDB 实例数量较多，且调高 [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-从-v530-版本开始引入) 并不能缓解 TSO RPC 请求延迟高的问题。

> **注意：**
>
> 如果 PD leader 的 TSO RPC 延迟升高，但其现象并非由 CPU 使用率达到瓶颈而导致（可能存在网络等问题），此时，打开 TSO Follower Proxy 可能会导致 TiDB 的语句执行延迟上升，从而影响集群的 QPS 表现。

### `tidb_enable_unsafe_substitute` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否对生成列中表达式替换使用不安全的替换方式。默认值为 `OFF`，即默认关闭不安全的替换方式。详情见[生成列](/generated-columns.md)。

### `tidb_enable_vectorized_expression` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否开启向量化执行。

### `tidb_enable_window_function`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制是否开启窗口函数的支持。默认值 1 代表开启窗口函数的功能。
- 由于窗口函数会使用一些保留关键字，可能导致原先可以正常执行的 SQL 语句在升级 TiDB 后无法被解析语法，此时可以将 `tidb_enable_window_function` 设置为 `OFF`。

### `tidb_enforce_mpp` <span class="version-mark">从 v5.1 版本开始引入</span>

- 作用域：SESSION
- 默认值：`OFF`（表示关闭）。如需修改此变量的默认值，请配置 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 参数。
- 这个变量用于控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询，可以设置的值包括：
    - 0 或 OFF，代表不强制使用 MPP 模式（默认）
    - 1 或 ON，代表将忽略代价估算，强制使用 MPP 模式。注意：只有当 `tidb_allow_mpp=true` 时该设置才生效。

MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点之间的数据交换并提供高性能、高吞吐的 SQL 算法。MPP 模式选择的详细说明参见[控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#控制是否选择-mpp-模式)。

### `tidb_evolve_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制是否启用自动演进绑定功能。该功能的详细介绍和使用方法可以参考[自动演进绑定](/sql-plan-management.md#自动演进绑定-baseline-evolution)。
- 为了减少自动演进对集群的影响，可以进行以下配置：

    - 设置 `tidb_evolve_plan_task_max_time`，限制每个执行计划运行的最长时间，其默认值为 600s；
    - 设置`tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time`，限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。

### `tidb_evolve_plan_task_end_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`23:59 +0000`
- 这个变量用来设置一天中允许自动演进的结束时间。

### `tidb_evolve_plan_task_max_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`600`
- 范围：`[-1, 9223372036854775807]`
- 单位：秒
- 该变量用于限制自动演进功能中，每个执行计划运行的最长时间。

### `tidb_evolve_plan_task_start_time` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`00:00 +0000`
- 这个变量用来设置一天中允许自动演进的开始时间。

### `tidb_executor_concurrency` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`5`
- 范围：`[1, 256]`

变量用来统一设置各个 SQL 算子的并发度，包括：

- `index lookup`
- `index lookup join`
- `hash join`
- `hash aggregation`（partial 和 final 阶段）
- `window`
- `projection`

`tidb_executor_concurrency` 整合了已有的系统变量，方便管理。这些变量所列如下：

+ `tidb_index_lookup_concurrency`
+ `tidb_index_lookup_join_concurrency`
+ `tidb_hash_join_concurrency`
+ `tidb_hashagg_partial_concurrency`
+ `tidb_hashagg_final_concurrency`
+ `tidb_projection_concurrency`
+ `tidb_window_concurrency`

v5.0 后，用户仍可以单独修改以上系统变量（会有废弃警告），且修改只影响单个算子。后续通过 `tidb_executor_concurrency` 的修改也不会影响该算子。若要通过 `tidb_executor_concurrency` 来管理所有算子的并发度，需要将以上所列变量的值设置为 `-1`。

对于从 v5.0 之前的版本升级到 v5.0 的系统，如果用户对上述所列变量的值没有做过改动（即 `tidb_hash_join_concurrency` 值为 `5`，其他值为 `4`），则会自动转为使用 `tidb_executor_concurrency` 来统一管理算子并发度。如果用户对上述变量的值做过改动，则沿用之前的变量对相应的算子做并发控制。

### `tidb_expensive_query_time_threshold`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`60`
- 范围：`[10, 2147483647]`
- 单位：秒
- 这个变量用来控制打印 expensive query 日志的阈值时间，默认值是 60 秒。expensive query 日志和慢日志的差别是，慢日志是在语句执行完后才打印，expensive query 日志可以把正在执行中的语句且执行时间超过阈值的语句及其相关信息打印出来。

### `tidb_force_priority`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`NO_PRIORITY`
- 这个变量用于改变 TiDB server 上执行的语句的默认优先级。例如，你可以通过设置该变量来确保正在执行 OLAP 查询的用户优先级低于正在执行 OLTP 查询的用户。
- 默认值 `NO_PRIORITY` 表示不强制改变执行语句的优先级，其它优先级从低到高可设置为 `LOW_PRIORITY`、`DELAYED` 或 `HIGH_PRIORITY`。

### `tidb_generate_binary_plan` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于指定是否在 slow log 和 statement summary 里包含以二进制格式编码的执行计划。
- 开启该变量后，即可在 TiDB Dashboard 中查看查询的图形化执行计划。注意，TiDB Dashboard 只显示变量开启时产生的查询的执行计划。
- 用 `select tidb_decode_binary_plan('xxx...')` SQL 语句可以从编码后的执行计划解析出具体的执行计划。

### `tidb_gc_concurrency` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用于指定 GC 在[Resolve Locks（清理锁）](/garbage-collection-overview.md#resolve-locks清理锁)步骤中线程的数量。默认值 `-1` 表示由 TiDB 自主判断运行 GC 要使用的线程的数量。

### `tidb_gc_enable` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否启用 TiKV 的垃圾回收 (GC) 机制。如果不启用 GC 机制，系统将不再清理旧版本的数据，因此会有损系统性能。

### `tidb_gc_life_time` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`10m0s`
- 范围：`[10m0s, 8760h0m0s]`
- 这个变量用于指定每次进行垃圾回收 (GC) 时保留数据的时限。变量值为 Go 的 Duration 字符串格式。每次进行 GC 时，将以当前时间减去该变量的值作为 safe point。

> **Note:**
>
> - 在数据频繁更新的场景下，将 `tidb_gc_life_time` 的值设置得过大（如数天甚至数月）可能会导致一些潜在的问题，如：
>     - 占用更多的存储空间。
>     - 大量的历史数据可能会在一定程度上影响系统性能，尤其是范围的查询（如 `select count(*) from t`）。
> - 如果一个事务的运行时长超过了 `tidb_gc_life_time` 配置的值，在 GC 时，为了使这个事务可以继续正常运行，系统会保留从这个事务开始时间 `start_ts` 以来的数据。例如，如果 `tidb_gc_life_time` 的值配置为 10 分钟，且在一次 GC 时，集群正在运行的事务中最早开始的那个事务已经运行了 15 分钟，那么本次 GC 将保留最近 15 分钟的数据。

### `tidb_gc_max_wait_time` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`86400`
- 范围：`[600, 31536000]`
- 单位：秒
- 这个变量用于指定活跃事务阻碍 GC safe point 推进的最大时间。每次进行 GC 时，默认 GC safe point 不会超过正在执行中的事务的开始时间。如果活跃事务运行时间未超过该值，GC safe point 会一直被阻塞不更新，直到活跃事务运行时间超过该值 safe point 才会正常推进。

### `tidb_gc_run_interval` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`10m0s`
- 范围：`[10m0s, 8760h0m0s]`
- 这个变量用于指定垃圾回收 (GC) 运行的时间间隔。变量值为 Go 的 Duration 字符串格式，如`"1h30m"`、`"15m"`等。

### `tidb_gc_scan_lock_mode` <span class="version-mark">从 v5.0 版本开始引入</span>

> **警告：**
>
> Green GC 目前是实验性功能，不建议在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`LEGACY`
- 可设置为：`PHYSICAL`，`LEGACY`
    - `LEGACY`：使用旧的扫描方式，即禁用 Green GC。
    - `PHYSICAL`：使用物理扫描方式，即启用 Green GC。
- 这个变量用于指定垃圾回收 (GC) 的 Resolve Locks（清理锁）步骤中扫描锁的方式。当变量值设置为 `LEGACY` 时，TiDB 以 Region 为单位进行扫描。当变量值设置为 `PHYSICAL` 时，每个 TiKV 节点分别绕过 Raft 层直接扫描数据，可以有效地缓解在启用 [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) 功能时，GC 唤醒全部 Region 的影响，从而提升 Resolve Locks（清理锁）这个步骤的执行速度。

### `tidb_general_log`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`OFF`
- 这个变量用来设置是否在[日志](/tidb-configuration-file.md#logfile)里记录所有的 SQL 语句。该功能默认关闭。如果系统运维人员在定位问题过程中需要追踪所有 SQL 记录，可考虑开启该功能。
- 通过查询 `"GENERAL_LOG"` 字符串可以定位到该功能在日志中的所有记录。日志会记录以下内容：
    - `conn`：当前会话对应的 ID
    - `user`：当前会话用户
    - `schemaVersion`：当前 schema 版本
    - `txnStartTS`：当前事务的开始时间戳
    - `forUpdateTS`：事务模式为悲观事务时，SQL 语句的当前时间戳。悲观事务内发生写冲突时，会重试当前执行语句，该时间戳会被更新。重试次数由 [`max-retry-count`](/tidb-configuration-file.md#max-retry-count) 配置。事务模式为乐观事务时，该条目与 `txnStartTS` 等价。
    - `isReadConsistency`：当前事务隔离级别是否是读已提交 (RC)
    - `current_db`：当前数据库名
    - `txn_mode`：事务模式。可选值：`OPTIMISTIC`（乐观事务模式），或 `PESSIMISTIC`（悲观事务模式）
    - `sql`：当前查询对应的 SQL 语句

### `tidb_general_plan_cache_size` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`100`
- 范围：`[1, 100000]`
- 这个变量用来控制 General Plan Cache 最多能够缓存的计划数量。

### `tidb_guarantee_linearizability` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 此变量控制异步提交 (Async Commit) 中提交时间戳的计算方式。默认情况下（使用 `OFF` 值），两阶段提交从 PD 服务器请求一个新的时间戳，并使用该时间戳计算最终提交的时间戳，这样可保证所有并发事务可线性化。
- 如果将该变量值设为 `ON`，从 PD 获取的时间戳的操作会被省掉，这种情况下只保证因果一致性但不保证线性一致性。详情请参考 PingCAP 博文 [Async Commit 原理介绍](https://pingcap.com/zh/blog/async-commit-principle)。
- 对于需要只保证因果一致性的场景，可将此变量设为 `ON` 以提升性能。

### `tidb_hash_join_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置 hash join 算法的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_hashagg_final_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置并行 hash aggregation 算法 final 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_hashagg_partial_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置并行 hash aggregation 算法 partial 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_ignore_prepared_cache_close_stmt` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置是否忽略关闭 Prepared Statement 的指令。
- 如果变量值设为 `ON`，Binary 协议的 `COM_STMT_CLOSE` 信号和文本协议的 [`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md) 语句都会被忽略。

### `tidb_index_join_batch_size`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`25000`
- 范围：`[1, 2147483647]`
- 这个变量用来设置 index lookup join 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_index_lookup_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_index_lookup_join_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置 index lookup join 算法的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_index_lookup_size`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`20000`
- 范围：`[1, 2147483647]`
- 这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_index_serial_scan_concurrency`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 范围：`[1, 256]`
- 这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### `tidb_init_chunk_size`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`32`
- 范围：`[1, 32]`
- 这个变量用来设置执行过程中初始 chunk 的行数。默认值是 32，可设置的范围是 1～32。

### `tidb_isolation_read_engines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`tikv,tiflash,tidb`
- 这个变量用于设置 TiDB 在读取数据时可以使用的存储引擎列表。

### `tidb_last_ddl_info` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 默认值：""
- 类型：字符串
- 该变量为只读变量，TiDB 内部使用该变量获取当前会话中上一个 DDL 操作的信息。
    - "query"：上一个 DDL 查询字符串。
    - "seq_num"：每个 DDL 操作的序列号，用于标识 DDL 操作的顺序。

### `tidb_last_query_info` <span class="version-mark">从 v4.0.14 版本开始引入</span>

- 作用域：SESSION
- 默认值：""
- 这是一个只读变量。用于在 TiDB 内部查询上一条 DML 语句的事务信息。查询的事务信息包括：
    - `txn_scope`：事务的作用域，可能为 `global` 或 `local`。
    - `start_ts`：事务开始的时间戳。
    - `for_update_ts`：先前执行的 DML 语句的 `for_update_ts` 信息。这是 TiDB 用于测试的内部术语。通常，你可以忽略此信息。
    - `error`：错误消息（如果有）。

### `tidb_last_txn_info` <span class="version-mark">从 v4.0.9 版本开始引入</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 类型：字符串
- 此变量用于获取当前会话中最后一个事务的信息。这是一个只读变量。事务信息包括：
    - 事务的范围
    - 开始时间戳和提交时间戳
    - 事务的提交模式，可能是两阶段提交，一阶段提交，或者异步提交
    - 事务从异步提交或一阶段提交到两阶段提交的回退信息
    - 遇到的错误

### `tidb_last_plan_replayer_token` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 类型：字符串
- 这个变量是一个只读变量，用于获取当前会话中最后一个 `PLAN REPLAYER dump` 的结果。

### `tidb_log_file_max_days` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 这个变量可以调整当前 TiDB 实例上日志的最大保留天数。默认值是实例配置文件中指定的值，见配置项 [`max-days`](/tidb-configuration-file.md#max-days)。此变量只影响当前 TiDB 实例上的配置，重启后丢失，且配置文件不受影响。

### `tidb_low_resolution_tso`

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来设置是否启用低精度 TSO 特性。开启该功能之后，新事务会使用一个每 2s 更新一次的 TS 来读取数据。
- 主要场景是在可以容忍读到旧数据的情况下，降低小的只读事务获取 TSO 的开销。

### `tidb_nontransactional_ignore_error` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置是否在非事务语句中立刻返回错误。当设为 `OFF` 时，在碰到第一个报错的 batch 时，非事务 DML 语句即中止，取消其后的所有 batch，返回错误。当设为 `ON` 时，当某个 batch 执行报错时，其后的 batch 会继续执行，直到所有 batch 执行完毕，返回结果时把这些错误合并后返回。

### `tidb_max_chunk_size`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1024`
- 范围：`[32, 2147483647]`
- 这个变量用来设置执行过程中一个 chunk 最大的行数，设置过大可能引起缓存局部性的问题。

### `tidb_max_paging_size` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`50000`
- 范围：`[1, 2147483647]`
- 单位：行
- 这个变量用来设置 coprocessor 协议中 paging size 的最大的行数。请合理设置该值，设置过小，TiDB 与 TiKV 的 RPC 交互会更频繁；设置过大，导数据和全表扫等特定场景会占用更多内存。

### `tidb_max_delta_schema_count`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`1024`
- 范围：`[100, 16384]`
- 这个变量用来设置缓存 schema 版本信息（对应版本修改的相关 table IDs）的个数限制，可设置的范围 100 - 16384。此变量在 2.1.18 及之后版本支持。

### tidb_mem_oom_action <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`CANCEL`
- 可选值：`CANCEL`，`LOG`
- 该变量控制当单个查询使用的内存超过限制 (`tidb_mem_quota_query`) 且不能再利用临时磁盘时，TiDB 所采取的操作。详情见 [TiDB 内存控制](/configure-memory-usage.md)。
- 该变量默认值为 `CANCEL`，但在 TiDB v4.0.2 及之前的版本中，默认值为 `LOG`。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`oom-action`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_mem_quota_analyze` <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> 目前限制 ANALYZE 的内存使用量为实验特性，在生产环境中使用时可能存在内存统计有误差的情况。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 单位：字节
- 这个变量用来控制 TiDB 更新统计信息时的最大总内存占用，包括用户执行的 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 和 TiDB 后台自动执行的统计信息更新任务。当总的内存占用超过这个阈值时，用户执行的 `ANALYZE` 会被终止退出，并通过错误信息提示用户尝试更小的采样率或稍后重试。如果 TiDB 后台自动执行的统计信息更新任务因内存超限而退出，且使用的采样率高于默认值，则会使用默认采样率重试一次。当该变量值为负数或零时，TiDB 不对更新统计信息的前后台任务进行内存限制。

> **注意：**
>
> 只有在 TiDB 的启动配置文件中开启了 `run-auto-analyze` 选项，该 TiDB 集群才会触发 `auto_analyze`。

### `tidb_mem_quota_apply_cache` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`33554432` (32 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 这个变量用来设置 `Apply` 算子中局部 Cache 的内存使用阈值。
- `Apply` 算子中局部 Cache 用来加速 `Apply` 算子的计算，该变量可以设置 `Apply` Cache 的内存使用阈值。设置变量值为 `0` 可以关闭 `Apply` Cache 功能。

### `tidb_mem_quota_binding_cache` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`67108864` (64 MiB)
- 范围：`[0, 2147483647]`
- 单位：字节
- 这个变量用来设置存放 `binding` 的缓存的内存使用阈值。
- 如果一个系统创建或者捕获了过多的绑定，导致绑定所使用的内存空间超过该阈值，TiDB 会在日志中增加警告日志进行提示。这种情况下，缓存无法存放所有可用的绑定，并且无法保证哪些绑定存在于缓存中，因此，可能存在一些查询无法使用可用绑定的情况。此时，可以调大该变量的值，从而保证所有可用绑定都能正常使用。修改变量值以后，需要执行命令 `admin reload bindings` 重新加载绑定，确保变更生效。

### `tidb_mem_quota_query`

- 作用域：SESSION ｜ GLOBAL
- 是否持久化到集群：是
- 默认值：`1073741824` (1 GiB)
- 范围：`[-1, 9223372036854775807]`
- 单位：字节
- 这个变量用来设置一条查询语句的内存使用阈值。
- 如果一条查询语句执行过程中使用的内存空间超过该阈值，会触发系统变量 [`tidb_mem_oom_action`](#tidb_mem_oom_action-从-v610-版本开始引入) 中指定的行为。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`mem-quota-query`) 进行配置，且作用域为 `SESSION`。升级到 v6.1.0 时会自动继承原有设置，作用域变更为 `SESSION | GLOBAL`。

### `tidb_memory_usage_alarm_ratio`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`0.8`
- TiDB 内存使用占总内存的比例超过一定阈值时会报警。该功能的详细介绍和使用方法可以参考 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入)。
- 该变量的初始值可通过 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入) 进行配置。

### `tidb_metric_query_range_duration` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`60`
- 范围：`[10, 216000]`
- 单位：秒
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 range duration。

### `tidb_metric_query_step` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`60`
- 范围：`[10, 216000]`
- 单位：秒
- 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 step。

### `tidb_min_paging_size` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`128`
- 范围：`[1, 2147483647]`
- 单位：行
- 这个变量用来设置 coprocessor 协议中 paging size 的最小的行数。请合理设置该值，设置过小，TiDB 与 TiKV 的 RPC 交互会更频繁；设置过大，IndexLookup 带 Limit 场景会出现性能下降。

### `tidb_multi_statement_mode` <span class="version-mark">从 v4.0.11 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 可选值：`OFF`，`ON`，`WARN`
- 该变量用于控制是否在同一个 `COM_QUERY` 调用中执行多个查询。
- 为了减少 SQL 注入攻击的影响，TiDB 目前默认不允许在同一 `COM_QUERY` 调用中执行多个查询。该变量可用作早期 TiDB 版本的升级路径选项。该变量值与是否允许多语句行为的对照表如下：

| 客户端设置         | `tidb_multi_statement_mode` 值 | 是否允许多语句 |
|------------------------|-----------------------------------|--------------------------------|
| Multiple Statements = ON  | OFF                               | 允许                            |
| Multiple Statements = ON  | ON                                | 允许                            |
| Multiple Statements = ON  | WARN                              | 允许                            |
| Multiple Statements = OFF | OFF                               | 不允许                             |
| Multiple Statements = OFF | ON                                | 允许                            |
| Multiple Statements = OFF | WARN                              | 允许 + 警告提示        |

> **注意：**
>
> 只有默认值 `OFF` 才是安全的。如果用户业务是专为早期 TiDB 版本而设计的，那么需要将该变量值设为 `ON`。如果用户业务需要多语句支持，建议用户使用客户端提供的设置，不要使用 `tidb_multi_statement_mode` 变量进行设置。

>
> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> * [Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> * PHP [mysqli](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.quickstart.multiple-statement.html) (`mysqli_multi_query`)

### `tidb_enable_new_cost_interface` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 可选值：`OFF`，`ON`
- TiDB v6.2.0 对代价模型的实现进行了代码层面的重构，这个变量用来控制是否使用重构后的代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2)。
- 重构后的代价模型使用完全一样的代价公式，因此不会引起计划选择的变动，此开关默认打开。
- 从 v6.1 升级至 v6.2 的用户，此开关保持升级前的 `OFF` 状态，此时建议直接打开；对于从 v6.1 之前版本升级至 v6.2 的用户，此开关默认为 `ON`。

### `tidb_enable_new_only_full_group_by_check` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 可选值：`OFF`，`ON`
- 该变量用于控制用于控制 TiDB 执行 `ONLY_FULL_GOUP_BY` 检查时的行为。有关 `ONLY_FULL_GROUP_BY` 的信息可以参考 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)。在 v6.1 中 TiDB 对该项检查做了更严格正确的处理。
- 由于可能存在版本升级造成的兼容性问题，在 v6.1 中该变量默认值是 `OFF`，即默认关闭。

### `tidb_opt_agg_push_down`

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。当查询中聚合操作执行很慢时，可以尝试设置该变量为 ON。

### `tidb_opt_cartesian_bcj`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：整数
- 默认值：`1`
- 范围：`[0, 2]`
- 表示是否允许 Broadcast Cartesian Join 算法。
- 值为 `0` 时表示不允许使用 Broadcast Cartesian Join 算法。值为 `1` 时表示根据 [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的行数阈值确定是否允许使用 Broadcast Cartesian Join 算法。值为 `2` 时表示总是允许 Broadcast Cartesian Join 算法，即使表的大小超过了该阈值。
- 该变量是 TiDB 内部使用的变量，**不推荐**修改该变量的值。

### `tidb_opt_concurrency_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示在 TiDB 中开启一个 Golang goroutine 的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_cop_cpu_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示 TiKV 协处理器处理一行数据的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_correlation_exp_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`1`
- 范围：`[0, 2147483647]`
- 当交叉估算方法不可用时，会采用启发式估算方法。这个变量用来控制启发式方法的行为。当值为 0 时不用启发式估算方法，大于 0 时，该变量值越大，启发式估算方法越倾向 index scan，越小越倾向 table scan。

### `tidb_opt_correlation_threshold`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`0.9`
- 这个变量用来设置优化器启用交叉估算 row count 方法的阈值。如果列和 handle 列之间的顺序相关性超过这个阈值，就会启用交叉估算方法。
- 交叉估算方法可以简单理解为，利用这个列的直方图来估算 handle 列需要扫的行数。

### `tidb_opt_cpu_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示 TiDB 处理一行数据的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，不建议修改该变量的值。

### `tidb_opt_desc_scan_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示降序扫描时，TiKV 在磁盘上扫描一行数据的开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_disk_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1.5`
- 表示 TiDB 往临时磁盘读写一个字节数据的 I/O 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_distinct_agg_push_down`

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `1`。

在以下示例中，`tidb_opt_distinct_agg_push_down` 开启前，TiDB 需要从 TiKV 读取所有数据，并在 TiDB 侧执行 `distinct`。`tidb_opt_distinct_agg_push_down` 开启后，`distinct a` 被下推到了 Coprocessor，在 `HashAgg_5` 里新增里一个 `group by` 列 `test.t.a`。

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

### `tidb_opt_enable_correlation_adjustment`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制优化器是否开启交叉估算。

### `tidb_opt_insubq_to_join_and_agg`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来设置是否开启优化规则：将子查询转成 join 和 aggregation。

    例如，打开这个优化规则后，会将下面子查询做如下变化：

    {{< copyable "sql" >}}

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    将子查询转成如下 join：

    {{< copyable "sql" >}}

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    如果 t1 在列 `aa` 上有 unique 且 not null 的限制，可以直接改写为如下，不需要添加 aggregation。

    {{< copyable "sql" >}}

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### `tidb_opt_limit_push_down_threshold`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`100`
- 范围：`[0, 2147483647]`
- 这个变量用来设置将 Limit 和 TopN 算子下推到 TiKV 的阈值。
- 如果 Limit 或者 TopN 的取值小于等于这个阈值，则 Limit 和 TopN 算子会被强制下推到 TiKV。该变量可以解决部分由于估算误差导致 Limit 或者 TopN 无法被下推的问题。

### `tidb_opt_memory_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`0.001`
- 表示 TiDB 存储一行数据的内存开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_mpp_outer_join_fixed_build_side` <span class="version-mark">从 v5.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`ON`
- 当该变量值为 `ON` 时，左连接始终使用内表作为构建端，右连接始终使用外表作为构建端。将该变量值设为 `OFF` 后，外连接可以灵活选择任意一边表作为构建端。

### `tidb_opt_network_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1.0`
- 表示传输 1 比特数据的网络净开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_prefer_range_scan` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 将该变量值设为 `ON` 后，优化器总是偏好区间扫描而不是全表扫描。
- 在以下示例中，`tidb_opt_prefer_range_scan` 开启前，TiDB 优化器需要执行全表扫描。`tidb_opt_prefer_range_scan` 开启后，优化器选择了索引区间扫描。

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

### `tidb_opt_projection_push_down` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 类型：布尔型
- 默认值：`OFF`
- 指定是否允许优化器将 `Projection` 算子下推到 TiKV 或者 TiFlash。

### `tidb_opt_scan_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1.5`
- 表示升序扫描时，TiKV 在磁盘上扫描一行数据的开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_seek_factor`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`20`
- 表示 TiDB 从 TiKV 请求数据的初始开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### `tidb_opt_skew_distinct_agg` <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **注意：**
>
> 开启该变量带来的查询性能优化仅对 TiFlash 有效。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置优化器是否将带有 `DISTINCT` 的聚合函数（例如 `SELECT b, count(DISTINCT a) FROM t GROUP BY b`）改写为两层聚合函数（例如 `SELECT b, count(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`）。当聚合列有严重的数据倾斜，且 `DISTINCT` 列有很多不同的值时，这种改写能够避免查询执行过程中的数据倾斜，从而提升查询性能。

### `tidb_opt_three_stage_distinct_agg` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制在 MPP 模式下是否将 `COUNT(DISTINCT)` 聚合改写为三阶段分布式执行的聚合。
- 该变量目前仅对只有一个 `COUNT(DISTINCT)` 的聚合生效。

### `tidb_opt_write_row_id`

- 作用域：SESSION
- 默认值：`OFF`
- 这个变量用来设置是否允许 `INSERT`、`REPLACE` 和 `UPDATE` 操作 `_tidb_rowid` 列，默认是不允许操作。该选项仅用于 TiDB 工具导数据时使用。

### `tidb_opt_force_inline_cte` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制是否强制 inline CTE。默认值为 `OFF`，即默认不强制 inline CTE。注意，此时依旧可以通过 `MERGE()` hint 来开启个别 CTE 的 inline。如果设置为 `ON`，则当前 session 中所有查询的 CTE（递归 CTE 除外）都会 inline。

### `tidb_partition_prune_mode` <span class="version-mark">从 v5.1 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`dynamic`
- 这个变量用来设置是否开启分区表动态裁剪模式。默认值为 `dynamic`。但是注意，`dynamic` 模式仅在表级别汇总统计信息（即 GlobalStats）收集完成的情况下生效。如果选择了 `dynamic` 但 GlobalStats 未收集完成，TiDB 会仍采用 `static` 模式。关于 GlobalStats 更多信息，请参考[动态裁剪模式下的分区表统计信息](/statistics.md#动态裁剪模式下的分区表统计信息)。关于动态裁剪模式更多信息，请参考[分区表动态裁剪模式](/partitioned-table.md#动态裁剪模式)。

### `tidb_persist_analyze_options` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否开启 [ANALYZE 配置持久化](/statistics.md#analyze-配置持久化)特性。

### `tidb_placement_mode` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`STRICT`
- 可选值：`STRICT`，`IGNORE`
- 该变量用于控制 DDL 语句是否忽略 [Placement Rules in SQL](/placement-rules-in-sql.md) 指定的放置规则。变量值为 `IGNORE` 时将忽略所有放置规则选项。
- 该变量可由逻辑转储或逻辑恢复工具使用，确保即使绑定了不合适的放置规则，也始终可以成功创建表。这类似于 mysqldump 将 `SET FOREIGN_KEY_CHECKS=0;` 写入每个转储文件的开头部分。

### `tidb_pprof_sql_cpu` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`0`
- 范围：`[0, 1]`
- 这个变量用来控制是否在 profile 输出中标记出对应的 SQL 语句，用于定位和排查性能问题。

### `tidb_prepared_plan_cache_memory_guard_ratio` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0.1`
- 范围：`[0, 1]`
- 这个变量用来控制 Prepared Plan Cache 触发内存保护机制的阈值，具体可见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.memory-guard-ratio`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_prepared_plan_cache_size` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`100`
- 范围：`[1, 100000]`
- 这个变量用来控制单个 `SESSION` 的 Prepared Plan Cache 最多能够缓存的计划数量，具体可见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.capacity`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### `tidb_projection_concurrency`

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[-1, 256]`
- 这个变量用来设置 `Projection` 算子的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tidb_query_log_max_len`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`4096` (4 KiB)
- 范围：`[0, 1073741824]`
- 单位：字节
- 该变量控制 SQL 语句输出的最大长度。当一条 SQL 语句的输出长度大于 `tidb_query_log_max_len` 时，输出将会被截断。
- 在 v6.1.0 之前这个开关也可以通过 TiDB 配置文件 (`log.query-log-max-len`) 进行配置，升级到 v6.1.0 后仅可通过系统变量配置。

### `tidb_rc_read_check_ts` <span class="version-mark">从 v6.0.0 版本开始引入</span>

> **警告：**
>
> - 该特性与 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 尚不兼容，开启 `tidb_rc_read_check_ts` 的读请求无法使用 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入)，请勿同时开启两项特性。
> - 如果客户端使用游标操作，建议不开启 `tidb_rc_read_check_ts` 这一特性，避免前一批返回数据已经被客户端使用而语句最终会报错的情况。

- 作用域：INSTANCE。自 v6.3.0 起，该变量的作用域由 GLOBAL 或 SESSION 修改为 INSTANCE 级别。
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`OFF`
- 该变量用于优化时间戳的获取，适用于悲观事务 `READ-COMMITTED` 隔离级别下读写冲突较少的场景，开启此变量可以避免获取全局 timestamp 带来的延迟和开销，并优化事务内读语句延迟。
- 如果读写冲突较为严重，开启此功能会增加额外开销和延迟，造成性能回退。更详细的说明，请参考[读已提交隔离级别 (Read Committed) 文档](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。

### `tidb_rc_write_check_ts` <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 该特性与 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 尚不兼容。开启本变量后，客户端发送的所有请求都将无法使用 `replica-read`，因此请勿同时开启 `tidb_rc_write_check_ts` 和 `replica-read`。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 该变量用于优化时间戳的获取，适用于悲观事务 `READ-COMMITTED` 隔离级别下点写冲突较少的场景。开启此变量可以避免点写语句获取全局时间戳带来的延迟和开销。目前该变量适用的点写语句包括 `UPDATE`、`DELETE`、`SELECT ...... FOR UPDATE` 三种类型。点写语句是指将主键或者唯一键作为过滤条件且最终执行算子包含 `POINT-GET` 的写语句。
- 如果点写冲突较为严重，开启此变量会增加额外开销和延迟，造成性能回退。更详细的说明，请参考[读已提交隔离级别 (Read Committed) 文档](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。

### `tidb_read_consistency` <span class="version-mark">New in v5.4.0</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 类型：字符串
- 默认值：`strict`
- 此变量用于控制自动提交的读语句的读一致性。
- 如果将变量值设置为 `weak`，则直接跳过读语句遇到的锁，读的执行可能会更快，这就是弱一致性读模式。但在该模式下，事务语义（例如原子性）和分布式一致性（线性一致性）并不能得到保证。
- 如果用户场景中需要快速返回自动提交的读语句，并且可接受弱一致性的读取结果，则可以使用弱一致性读取模式。

### `tidb_read_staleness` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：`0`
- 范围 `[-2147483648, 0]`
- 这个变量用于设置当前会话允许读取的历史数据范围。设置后，TiDB 会从参数允许的范围内选出一个尽可能新的时间戳，并影响后继的所有读操作。比如，如果该变量的值设置为 `-5`，TiDB 会在 5 秒时间范围内，保证 TiKV 拥有对应历史版本数据的情况下，选择尽可能新的一个时间戳。

### `tidb_record_plan_in_slow_log`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`ON`
- 这个变量用于控制是否在 slow log 里包含慢查询的执行计划。

### `tidb_redact_log`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制在记录 TiDB 日志和慢日志时，是否将 SQL 中的用户信息遮蔽。
- 将该变量设置为 `1` 即开启后，假设执行的 SQL 为 `insert into t values (1,2)`，在日志中记录的 SQL 会是 `insert into t values (?,?)`，即用户输入的信息被遮蔽。

### `tidb_regard_null_as_point` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用来控制优化器是否可以将包含 null 的等值条件作为前缀条件来访问索引。
- 该变量默认开启。开启后，该变量可以使优化器减少需要访问的索引数据量，从而提高查询的执行速度。例如，在有多列索引 `index(a, b)` 且查询条件为 `a<=>null and b=1` 的情况下，优化器可以同时使用查询条件中的 `a<=>null` 和 `b=1` 进行索引访问。如果关闭该变量，因为 `a<=>null and b=1` 包含 null 的等值条件，优化器不会使用 `b=1` 进行索引访问。

### `tidb_remove_orderby_in_subquery` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 指定是否在子查询中移除 `ORDER BY` 子句。

### `tidb_replica_read` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`leader`
- 可选值：`leader`，`follower`，`leader-and-follower`，`closest-replicas`，`closest-adaptive`
- 这个变量用于控制 TiDB 的 Follower Read 功能的行为。
- 关于使用方式与实现原理，见 [Follower Read](/follower-read.md)。

### `tidb_retry_limit`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`10`
- 范围：`[-1, 9223372036854775807]`
- 这个变量用来设置乐观事务的最大重试次数。一个事务执行中遇到可重试的错误（例如事务冲突、事务提交过慢或表结构变更）时，会根据该变量的设置进行重试。注意当 `tidb_retry_limit = 0` 时，也会禁用自动重试。该变量仅适用于乐观事务，不适用于悲观事务。

### `tidb_row_format_version`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`2`
- 范围：`[1, 2]`
- 控制新保存数据的表数据格式版本。TiDB v4.0 中默认使用版本号为 2 的[新表数据格式](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)保存新数据。

- 但如果从 4.0.0 之前的版本升级到 4.0.0，不会改变表数据格式版本，TiDB 会继续使用版本为 1 的旧格式写入表中，即**只有新创建的集群才会默认使用新表数据格式**。

- 需要注意的是修改该变量不会对已保存的老数据产生影响，只会对修改变量后的新写入数据使用对应版本格式保存。

### `tidb_scatter_region`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- TiDB 默认会在建表时为新表分裂 Region。开启该变量后，会在建表语句执行时，同步打散刚分裂出的 Region。适用于批量建表后紧接着批量写入数据，能让刚分裂出的 Region 先在 TiKV 分散而不用等待 PD 进行调度。为了保证后续批量写入数据的稳定性，建表语句会等待打散 Region 完成后再返回建表成功，建表语句执行时间会是该变量关闭时的数倍。
- 如果建表时设置了 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS`，建表成功后会均匀切分出指定数量的 Region。

### `tidb_shard_allocate_step` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`9223372036854775807`
- 范围：`[1, 9223372036854775807]`
- 该变量设置为 [`AUTO_RANDOM`](/auto-random.md) 或 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 属性列分配的最大连续 ID 数。通常，`AUTO_RANDOM` ID 或带有 `SHARD_ROW_ID_BITS` 属性的行 ID 在一个事务中是增量和连续的。你可以使用该变量来解决大事务场景下的热点问题。

### `tidb_simplified_metrics`

- 作用域：GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量开启后，TiDB 将不会收集或记录 Grafana 面板未使用到的 metrics。

### `tidb_skip_ascii_check` <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置是否校验 ASCII 字符的合法性。
- 校验 ASCII 字符会损耗些许性能。当你确认输入的字符串为有效的 ASCII 字符时，可以将其设置为 `ON`。

### `tidb_skip_isolation_level_check`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
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
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来设置是否校验 UTF-8 字符的合法性。
- 校验 UTF-8 字符会损耗些许性能。当你确认输入的字符串为有效的 UTF-8 字符时，可以将其设置为 `ON`。

> **注意：**
>
> 跳过字符检查可能会使 TiDB 检测不到应用写入的非法 UTF-8 字符，进一步导致执行 `ANALYZE` 时解码错误，以及引入其他未知的编码问题。如果应用不能保证写入字符串的合法性，不建议跳过该检查。

### `tidb_slow_log_threshold`

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 默认值：`300`
- 范围：`[-1, 9223372036854775807]`
- 单位：毫秒
- 输出慢日志的耗时阈值。当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。默认为 300 ms。

### `tidb_max_tiflash_threads` <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[-1, 256]`
- TiFlash 中 request 执行的最大并发度。默认值为 -1，表示该系统变量无效。0 表示由 TiFlash 系统自动设置该值。

### `tidb_slow_query_file`

- 作用域：SESSION
- 默认值：""
- 查询 `INFORMATION_SCHEMA.SLOW_QUERY` 只会解析配置文件中 `slow-query-file` 设置的慢日志文件名，默认是 "tidb-slow.log"。但如果想要解析其他的日志文件，可以通过设置 session 变量 `tidb_slow_query_file` 为具体的文件路径，然后查询 `INFORMATION_SCHEMA.SLOW_QUERY` 就会按照设置的路径去解析慢日志文件。更多详情可以参考 [SLOW_QUERY 文档](/identify-slow-queries.md)。

### `tidb_snapshot`

- 作用域：SESSION
- 默认值：""
- 这个变量用来设置当前会话期待读取的历史数据所处时刻。比如当设置为 `"2017-11-11 20:20:20"` 时或者一个 TSO 数字 "400036290571534337"，当前会话将能读取到该时刻的数据。

### `tidb_stats_cache_mem_quota` <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> 该变量为实验特性，不推荐在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 这个变量用于控制 TiDB 内部统计信息缓存使用内存的上限。

### `tidb_stats_load_sync_wait` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 统计信息同步加载目前为实验性特性，不建议在生产环境中使用。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 单位：毫秒
- 范围：`[0, 2147483647]`
- 这个变量用于控制是否开启统计信息的同步加载模式（默认为 `0` 代表不开启，即为异步加载模式），以及开启的情况下，SQL 执行同步加载完整统计信息等待多久后会超时。更多信息，请参考[统计信息的加载](/statistics.md#统计信息的加载)。

### `tidb_stats_load_pseudo_timeout` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 统计信息同步加载目前为实验性特性，不建议在生产环境中使用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制统计信息同步加载超时后，SQL 是执行失败（`OFF`），还是退回使用 pseudo 的统计信息（`ON`）。

### `tidb_stmt_summary_history_size` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`24`
- 范围：`[0, 255]`
- 这个变量设置了 [statement summary tables](/statement-summary-tables.md) 的历史记录容量。

### `tidb_stmt_summary_internal_query` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用来控制是否在 [statement summary tables](/statement-summary-tables.md) 中包含 TiDB 内部 SQL 的信息。

### `tidb_stmt_summary_max_sql_length` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`4096`
- 范围：`[0, 2147483647]`
- 这个变量控制 [statement summary tables](/statement-summary-tables.md) 显示的 SQL 字符串长度。

### `tidb_stmt_summary_max_stmt_count` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`3000`
- 范围：`[1, 32767]`
- 这个变量设置了 [statement summary tables](/statement-summary-tables.md) 在内存中保存的语句的最大数量。

### `tidb_stmt_summary_refresh_interval` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`1800`
- 范围：`[1, 2147483647]`
- 单位：秒
- 这个变量设置了 [statement summary tables](/statement-summary-tables.md) 的刷新时间。

### `tidb_top_sql_max_meta_count` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`5000`
- 范围：`[1, 10000]`
- 这个变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟最多收集 SQL 语句类型的数量。

### `tidb_top_sql_max_time_series_count` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`100`
- 范围：`[1, 5000]`
- 这个变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟保留消耗负载最大的前多少条 SQL（即 Top N) 的数据。

> **注意：**
>
> TiDB Dashboard 中的 Top SQL 页面目前只显示消耗负载最多的 5 类 SQL 查询，这与 `tidb_top_sql_max_time_series_count` 的配置无关。

### `tidb_store_limit` <span class="version-mark">从 v3.0.4 和 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 这个变量用于限制 TiDB 同时向 TiKV 发送的请求的最大数量，0 表示没有限制。

### `tidb_super_read_only` <span class="version-mark">从 v5.3.1 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值: `OFF`。
- `tidb_super_read_only` 用于实现对 MySQL 变量 `super_read_only` 的替代。然而，由于 TiDB 是一个分布式数据库，开启 `tidb_super_read_only` 后数据库各个 TiDB 服务器进入只读模式的时刻不是强一致的，而是最终一致的。
- 拥有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改该变量。
- 该变量可以控制整个集群的只读状态。开启后（即该值为 `ON`），整个集群中的 TiDB 服务器都将进入只读状态，只有 `SELECT`、`USE`、`SHOW` 等不会修改数据的语句才能被执行，其他如 `INSERT`、`UPDATE` 等语句会被拒绝执行。
- 该变量开启只读模式只保证整个集群最终进入只读模式，当变量修改状态还没被同步到其他 TiDB 服务器时，尚未同步的 TiDB 仍然停留在非只读模式。
- 在执行 SQL 语句之前，TiDB 会检查集群的只读标志。从 v6.2.0 起，在提交 SQL 语句之前，TiDB 也会检查该标志，从而防止在服务器被置于只读模式后某些长期运行的 [auto commit](/transaction-overview.md#自动提交) 语句可能修改数据的情况。
- 在变量开启时，对于尚未提交的事务：
    - 如果有尚未提交的只读事务，可正常提交该事务。
    - 如果尚未提交的事务为非只读事务，在事务内执行写入的 SQL 语句会被拒绝。
    - 如果尚未提交的事务已经有数据改动，其提交也会被拒绝。
- 当集群开启只读模式后，所有用户（包括 `SUPER` 用户）都无法执行可能写入数据的 SQL 语句，除非该用户被显式地授予了 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。
- 当系统变量 [`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 为 `ON` 时，`tidb_super_read_only` 的值会受到 [`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 的影响。详情请参见[`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 中的描述。

### `tidb_sysdate_is_now` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`OFF`
- 这个变量用于控制 `SYSDATE` 函数能否替换为 `NOW` 函数，其效果与 MYSQL 中的 [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now) 一致。

### `tidb_table_cache_lease` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`3`
- 范围：`[1, 10]`
- 单位：秒
- 这个变量用来控制[缓存表](/cached-tables.md)的 lease 时间，默认值是 3 秒。该变量值的大小会影响缓存表的修改。在缓存表上执行修改操作后，最长可能出现 `tidb_table_cache_lease` 变量值时长的等待。如果业务表为只读表，或者能接受很高的写入延迟，则可以将该变量值调大，从而增加缓存的有效时间，减少 lease 续租的频率。

### `tidb_tmp_table_max_size` <span class="version-mark">从 v5.3 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`67108864`
- 范围：`[1048576, 137438953472]`
- 单位：字节
- 这个变量用于限制单个[临时表](/temporary-tables.md)的最大大小，临时表超出该大小后报错。

### `tidb_track_aggregate_memory_usage`

- 作用域：SESSION ｜ GLOBAL
- 是否持久化到集群：是
- 类型：布尔型
- 默认值：`ON`
- 本变量控制 TiDB 是否跟踪聚合函数的内存使用情况。

> **警告：**
>
> 如果禁用该变量，TiDB 可能无法准确跟踪内存使用情况，并且无法控制对应 SQL 语句的内存使用。

### `tidb_tso_client_batch_max_wait_time` <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`0`
- 范围：`[0, 10]`
- 单位：毫秒
- 这个变量用来设置 TiDB 向 PD 请求 TSO 时进行一次攒批操作的最大等待时长。默认值为 `0`，即不进行额外的等待。
- 在向 PD 获取 TSO 请求时，TiDB 使用的 PD Client 会一次尽可能多地收集同一时刻的 TSO 请求，将其攒批合并成一个 RPC 请求后再发送给 PD，从而减轻 PD 的压力。
- 将这个变量值设置为非 0 后，TiDB 会在每一次攒批结束前进行一个最大时长为其值的等待，目的是为了收集到更多的 TSO 请求，从而提高攒批效果。
- 适合调高这个变量值的场景：
    * PD leader 因高压力的 TSO 请求而达到 CPU 瓶颈，导致 TSO RPC 请求的延迟较高。
    * 集群中 TiDB 实例的数量不多，但每一台 TiDB 实例上的并发量较高。
- 在实际使用中，推荐将该变量尽可能设置为一个较小的值。

> **注意：**
>
> 如果 PD leader 的 TSO RPC 延迟升高，但其现象并非由 CPU 使用率达到瓶颈而导致（可能存在网络等问题），此时，调高 `tidb_tso_client_batch_max_wait_time` 可能会导致 TiDB 的语句执行延迟上升，影响集群的 QPS 表现。

### `tidb_txn_assertion_level` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`FAST`
- 可选值：`OFF`，`FAST`，`STRICT`
- 这个变量用于设置 assertion 级别。assertion 是一项在事务提交过程中进行的数据索引一致性校验，它对正在写入的 key 是否存在进行检查。如果不符则说明数据索引不一致，会导致事务 abort。详见[数据索引一致性报错](/troubleshoot-data-inconsistency-errors.md)。
- 对于新创建的 v6.0.0 及以上的集群，默认值为 `FAST`。对于升级版本的集群，如果升级前是低于 v6.0.0 的版本，升级后默认值为 `OFF`。

    - `OFF`: 关闭该检查。
    - `FAST`: 开启大多数检查项，对性能几乎无影响。
    - `STRICT`: 开启全部检查项，当系统负载较高时，对悲观事务的性能有较小影响。

### `tidb_txn_commit_batch_size` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 默认值：`16384`
- 范围：`[1, 1073741824]`
- 单位：字节
- 这个变量用于控制 TiDB 向 TiKV 发送的事务提交请求的批量大小。如果业务负载的大部分事务都有大量的写操作，适当调大该变量可以提高批处理的效果。但需要注意的是，设置过大将会超过 TiKV 的 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) 限制，导致提交失败。

### `tidb_txn_mode`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`pessimistic`
- 可选值：`pessimistic`，`optimistic`
- 这个变量用于设置事务模式。TiDB v3.0 支持了悲观事务，自 v3.0.8 开始，默认使用[悲观事务模式](/pessimistic-transaction.md)。
- 但如果从 3.0.7 及之前的版本升级到 >= 3.0.8 的版本，不会改变默认事务模式，即**只有新创建的集群才会默认使用悲观事务模式**。
- 将该变量设置为 "optimistic" 或 "" 时，将会使用[乐观事务模式](/optimistic-transaction.md)。

### `tidb_use_plan_baselines` <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制是否开启执行计划绑定功能，默认打开，可通过赋值 `OFF` 来关闭。关于执行计划绑定功能的使用可以参考[执行计划绑定文档](/sql-plan-management.md#创建绑定)。

### `tidb_wait_split_region_finish`

- 作用域：SESSION
- 默认值：`ON`
- 由于打散 Region 的时间可能比较长，主要由 PD 调度以及 TiKV 的负载情况所决定。这个变量用来设置在执行 `SPLIT REGION` 语句时，是否同步等待所有 Region 都打散完成后再返回结果给客户端。
    - 默认 `ON` 代表等待打散完成后再返回结果
    - `OFF` 代表不等待 Region 打散完成就返回。
- 需要注意的是，在 Region 打散期间，对正在打散 Region 上的写入和读取的性能会有一定影响，对于批量写入、导数据等场景，还是建议等待 Region 打散完成后再开始导数据。

### `tidb_wait_split_region_timeout`

- 作用域：SESSION
- 默认值：`300`
- 范围：`[1, 2147483647]`
- 单位：秒
- 这个变量用来设置 `SPLIT REGION` 语句的执行超时时间，默认值是 300 秒，如果超时还未完成，就返回一个超时错误。

### `tidb_window_concurrency` <span class="version-mark">从 v4.0 版本开始引入</span>

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用于设置 window 算子的并行度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### `tiflash_fastscan` <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：`OFF`
- 范围：`ON | OFF`
- 如果开启 [FastScan 功能](/develop/dev-guide-use-fastscan.md)（设置为 `ON` 时），TiFlash 可以提供更高效的查询性能，但不保证查询结果的精度和数据一致性。

### `tiflash_fine_grained_shuffle_batch_size` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：`8192`
- 范围：`[1, 18446744073709551616]`
- 细粒度 shuffle 功能开启时，下推到 TiFlash 的窗口函数可以并行执行。该变量控制发送端发送数据的攒批大小，即发送端累计行数超过该值就会进行一次数据发送。
- 对性能影响：如果该值设置过小，例如极端值 1 ，会导致每个 Block 都进行一次网络传输。如果设置过大，例如极端值整个表的行数，会导致接收端大部分时间都在等待数据，无法流水线计算。可以观察 TiFlash 接收端收到的行数分布情况，如果大部分线程接收的行数很少，例如只有几百行，可以增加该值以达到减少网络开销的目的。

### `tiflash_fine_grained_shuffle_stream_count` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 默认值：`0`
- 范围：`[-1, 1024]`
- 当窗口函数下推到 TiFlash 执行时，可以通过该变量控制窗口函数执行的并行度。不同取值含义：

    * -1: 表示不使用细粒度 shuffle 功能，下推到 TiFlash 的窗口函数以单线程方式执行
    * 0: 表示使用细粒度 shuffle 功能。如果 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入) 有效（大于 0），则 `tiflash_fine_grained_shuffle_stream_count` 会自动取值为 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入) ，否则为默认值 8 。最终在 TiFlash 上窗口函数的实际并发度为：min(`tiflash_fine_grained_shuffle_stream_count`，TiFlash 节点物理线程数)
    * 大于 0: 表示使用细粒度 shuffle 功能，下推到 TiFlash 的窗口函数会以多线程方式执行，并发度为： min(`tiflash_fine_grained_shuffle_stream_count`, TiFlash 节点物理线程数)
- 理论上窗口函数的性能会随着该值的增加线性提升。但是如果设置的值超过实际的物理线程数，反而会导致性能下降。

### `time_zone`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`SYSTEM`
- 数据库所使用的时区。这个变量值可以写成时区偏移的形式，如 '-8:00'，也可以写成一个命名时区，如 'America/Los_Angeles'。
- 默认值 `SYSTEM` 表示时区应当与系统主机的时区相同。系统的时区可通过 [`system_time_zone`](#system_time_zone) 获取。

### `timestamp`

- 作用域：SESSION
- 默认值：`0`
- 一个 Unix 时间戳。变量值非空时，表示 `CURRENT_TIMESTAMP()`、`NOW()` 等函数的时间戳。该变量通常用于数据恢复或数据复制。

### `transaction_isolation`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`REPEATABLE-READ`
- 可选值：`READ-UNCOMMITTED`，`READ-COMMITTED`，`REPEATABLE-READ`，`SERIALIZABLE`
- 这个变量用于设置事务隔离级别。TiDB 为了兼容 MySQL，支持可重复读 (`REPEATABLE-READ`)，但实际的隔离级别是快照隔离。详情见[事务隔离级别](/transaction-isolation-levels.md)。

### `tx_isolation`

这个变量是 `transaction_isolation` 的别名。

### `version`

- 作用域：NONE
- 默认值：`5.7.25-TiDB-(tidb version)`
- 这个变量的值是 MySQL 的版本和 TiDB 的版本，例如 '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'。

### `version_comment`

- 作用域：NONE
- 默认值：(string)
- 这个变量的值是 TiDB 版本号的其他信息，例如 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'。

### `version_compile_os`

- 作用域：NONE
- 默认值：(string)
- 这个变量值是 TiDB 所在操作系统的名称。

### `version_compile_machine`

- 作用域：NONE
- 默认值：(string)
- 这个变量值是运行 TiDB 的 CPU 架构的名称。

### `wait_timeout`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`28800`
- 范围：`[0, 31536000]`
- 单位：秒
- 这个变量表示用户会话的空闲超时。`0` 代表没有时间限制。

### `warning_count`

- 作用域：SESSION
- 默认值：`0`
- 这个只读变量表示之前执行语句中出现的警告数。

### `windowing_use_high_precision`

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 默认值：`ON`
- 这个变量用于控制计算窗口函数时是否采用高精度模式。
