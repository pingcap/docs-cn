---
title: 错误码与故障诊断
aliases: ['/docs-cn/dev/error-codes/','/docs-cn/dev/reference/error-codes/']
---

# 错误码与故障诊断

本篇文档描述在使用 TiDB 过程中会遇到的问题以及解决方法。

## 错误码

TiDB 兼容 MySQL 的错误码，在大多数情况下，返回和 MySQL 一样的错误码。关于 MySQL 的错误码列表，详见 [[MySQL 5.7 Error Message Reference](https://dev.mysql.com/doc/mysql-errors/5.7/en/)。另外还有一些 TiDB 特有的错误码：

> **注意：**
>
> 有一部分错误码属于内部错误，正常情况下 TiDB 会自行处理不会直接返回给用户，故没有在此列出。
>
> 如果您遇到了这里没有列出的错误码，请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8001

    请求使用的内存超过 TiDB 内存使用的阈值限制。出现这种错误，可以通过调整系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 来增大单个 SQL 使用的内存上限。

* Error Number: 8002

    带有 `SELECT FOR UPDATE` 语句的事务，在遇到写入冲突时，为保证一致性无法进行重试，事务将进行回滚并返回该错误。出现这种错误，应用程序可以安全地重新执行整个事务。

* Error Number: 8003

    `ADMIN CHECK TABLE` 命令在遇到行数据跟索引不一致的时候返回该错误，在检查表中数据是否有损坏时常出现。出现该错误时，请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8004

    单个事务过大，原因及解决方法请参考[这里](/faq/migration-tidb-faq.md#transaction-too-large-是什么原因怎么解决)

* Error Number: 8005

    完整的报错信息为 `ERROR 8005 (HY000) : Write Conflict, txnStartTS is stale`。

    事务在 TiDB 中遇到了写入冲突。请检查业务逻辑，重试写入操作。

* Error Number: 8018

    当执行重新载入插件时，如果之前插件没有载入过，则会出现该错误。出现该错误，进行插件首次载入即可。

* Error Number: 8019

    重新载入的插件版本与之前的插件版本不一致，无法重新载入插件并报告该错误。可重新载入插件，确保插件的版本与之前载入的插件版本一致。

* Error Number: 8020

    当表被加锁时，如果对该表执行写入操作，将出现该错误。请将表解锁后，再进行尝试写入。

* Error Number: 8021

    当向 TiKV 读取的 key 不存在时将出现该错误，该错误用于内部使用，对外表现为读到的结果为空。

* Error Number: 8022

    事务提交失败，已经回滚，应用程序可以安全的重新执行整个事务。

* Error Number: 8023

    在事务内，写入事务缓存时，设置了空值，将返回该错误。这是一个内部使用的错误，将由内部进行处理，不会返回给应用程序。

* Error Number: 8024

    非法的事务。当事务执行时，发现没有获取事务的 ID (Start Timestamp)，代表正在执行的事务是一个非法的事务，将返回该错误。通常情况下不会出现该问题，当发生时，请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8025

    写入的单条键值对过大。TiDB 默认支持最大 6MB 的单个键值对，超过该限制可适当调整 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-从-v50-版本开始引入) 配置项以放宽限制。

* Error Number: 8026

    使用了没有实现的接口函数。该错误仅用于数据库内部，应用程序不会收到这个错误。

* Error Number: 8027

    表结构版本过期。TiDB 采用在线变更表结构的方法。当 TiDB server 表结构版本落后于整个系统的时，执行 SQL 将遇到该错误。遇到该错误，请检查该 TiDB server 与 PD leader 之间的网络。

* Error Number: 8028

    TiDB v6.3.0 引入了[元数据锁](/metadata-lock.md)特性。在关闭元数据锁的情况下，当事务执行时，事务无法感知到 TiDB 的表结构发生了变化。因此，TiDB 在事务提交时，会对事务涉及表的结构进行检查。如果事务执行中表结构发生了变化，则事务将提交失败，并返回该错误。遇到该错误，应用程序可以安全地重新执行整个事务。

    在打开元数据锁的情况下，非 RC 隔离级别中，如果从事务开始到初次访问一个表之间，该表进行了有损的列类型变更操作（例如 `INT` 类型变成 `CHAR` 类型是有损的，`TINYINT` 类型变成 `INT` 类型这种不需要重写数据的则是无损的），则访问该表的语句报错，事务不会自动回滚。用户可以继续执行其他语句，并决定是否回滚或者提交事务。

* Error Number: 8029

    当数据库内部进行数值转换发生错误时，将会出现该错误，该错误仅在内部使用，对外部应用将转换为具体类型的错误。

* Error Number: 8030

    将值转变为带符号正整数时发生了越界，将结果显示为负数。多在告警信息里出现。

* Error Number: 8031

    将负数转变为无符号数时，将负数转变为了正数。多在告警信息里出现。

* Error Number: 8032

    使用了非法的 year 格式。year 只允许 1 位、2 位和 4 位数。

* Error Number: 8033

    使用了非法的 year 值。year 的合法范围是 (1901, 2155)。

* Error Number: 8037

    week 函数中使用了非法的 mode 格式。mode 必须是一位数字，范围 [0, 7]。

* Error Number: 8038

    字段无法获取到默认值。一般作为内部错误使用，转换成其他具体错误类型后，返回给应用程序。

* Error Number: 8040

    尝试进行不支持的操作，比如在 View 和 Sequence 上进行 lock table。

* Error Number: 8047

    设置了不支持的系统变量值，通常在用户设置了数据库不支持的变量值后的告警信息里出现。

* Error Number: 8048

    设置了不支持的隔离级别，如果是使用第三方工具或框架等无法修改代码进行适配的情况，可以考虑通过 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check) 来绕过这一检查。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_skip_isolation_level_check = 1;
    ```

* Error Number: 8050

    设置了不支持的权限类型，遇到该错误请参考 [TiDB 权限说明](/privilege-management.md#tidb-各操作需要的权限)进行调整。

* Error Number: 8051

    TiDB 在解析客户端发送的 Exec 参数列表时遇到了未知的数据类型。如果遇到这个错误，请检查客户端是否正常，如果客户端正常请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8052

    来自客户端的数据包的序列号错误。如果遇到这个错误，请检查客户端是否正常，如果客户端正常请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8055

    当前快照过旧，数据可能已经被 GC。可以调大 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 的值来避免该问题。从 TiDB v4.0.8 版本起，TiDB 会自动为长时间运行的事务保留数据，一般不会遇到该错误。

    有关 GC 的介绍和配置可以参考 [GC 机制简介](/garbage-collection-overview.md)和 [GC 配置](/garbage-collection-configuration.md)文档。

* Error Number: 8059

    自动随机量可用次数用尽无法进行分配。当前没有恢复这类错误的方法。建议在使用 auto random 功能时使用 bigint 以获取最大的可分配次数，并尽量避免手动给 auto random 列赋值。相关的介绍和使用建议可以参考 [auto random 功能文档](/auto-random.md)。

* Error Number: 8060

    非法的自增列偏移量。请检查 `auto_increment_increment` 和 `auto_increment_offset` 的取值是否符合要求。

* Error Number: 8061

    不支持的 SQL Hint。请参考 [Optimizer Hints](/optimizer-hints.md) 检查和修正 SQL Hint。

* Error Number: 8062

    SQL Hint 中使用了非法的 token，与 Hint 的保留字冲突。请参考 [Optimizer Hints](/optimizer-hints.md) 检查和修正 SQL Hint。

* Error Number: 8063

    SQL Hint 中限制内存使用量超过系统设置的上限，设置被忽略。请参考 [Optimizer Hints](/optimizer-hints.md) 检查和修正 SQL Hint。

* Error Number: 8064

    解析 SQL Hint 失败。请参考 [Optimizer Hints](/optimizer-hints.md) 检查和修正 SQL Hint。

* Error Number: 8065

    SQL Hint 中使用了非法的整数。请参考 [Optimizer Hints](/optimizer-hints.md) 检查和修正 SQL Hint。

* Error Number: 8066

    JSON_OBJECTAGG 函数的第二个参数是非法参数。

* Error Number: 8101

    插件 ID 格式错误，正确的格式是 `[name]-[version]` 并且 name 和 version 中不能带有 '-'。

* Error Number: 8102

    无法读取插件定义信息。请检查插件相关的配置。

* Error Number: 8103

    插件名称错误，请检查插件的配置。

* Error Number: 8104

    插件版本不匹配，请检查插件的配置。

* Error Number: 8105

    插件被重复载入。

* Error Number: 8106

    插件定义的系统变量名称没有以插件名作为开头，请联系插件的开发者进行修复。

* Error Number: 8107

    载入的插件未指定版本或指定的版本过低，请检查插件的配置。

* Error Number: 8108

    不支持的执行计划类型。该错误为内部处理的错误，如果遇到该报错请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8109

    analyze 索引时找不到指定的索引。

* Error Number: 8110

    不能进行笛卡尔积运算，需要将配置文件里的 `cross-join` 设置为 `true`。

* Error Number: 8111

    execute 语句执行时找不到对应的 prepare 语句。

* Error Number: 8112

    execute 语句的参数个数与 prepare 语句不符合。

* Error Number: 8113

    execute 语句涉及的表结构在 prepare 语句执行后发生了变化。

* Error Number: 8115

    不支持 prepare 多行语句。

* Error Number: 8116

    不支持 prepare DDL 语句。

* Error Number: 8120

    获取不到事务的 start tso，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络。

* Error Number: 8121

    权限检查失败，请检查数据库的权限配置。

* Error Number: 8122

    指定了通配符，但是找不到对应的表名。

* Error Number: 8123

    带聚合函数的 SQL 中返回非聚合的列，违反了 `only_full_group_by` 模式。请修改 SQL 或者考虑关闭 `only_full_group_by` 模式。

* Error Number: 8129

    TiDB 尚不支持键长度 >= 65536 的 JSON 对象。

* Error Number: 8130

    完整的报错信息为 `ERROR 8130 (HY000): client has multi-statement capability disabled`。

    从早期版本的 TiDB 升级后，可能会出现该问题。为了减少 SQL 注入攻击的影响，TiDB 目前默认不允许在同一 `COM_QUERY` 调用中执行多个查询。

    可通过系统变量 [`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-从-v4011-版本开始引入) 控制是否在同一 `COM_QUERY` 调用中执行多个查询。

* Error Number: 8138

    事务试图写入的行值有误，请参考[数据索引不一致报错](/troubleshoot-data-inconsistency-errors.md#error-8138)。

* Error Number: 8139

    事务试图写入的行和索引的 handle 值不一致，请参考[数据索引不一致报错](/troubleshoot-data-inconsistency-errors.md#error-8139)。

* Error Number: 8140

    事务试图写入的行和索引的值不一致，请参考[数据索引不一致报错](/troubleshoot-data-inconsistency-errors.md#error-8140)。

* Error Number: 8141

    事务写入时，对 key 的存在性断言报错，请参考[数据索引不一致报错](/troubleshoot-data-inconsistency-errors.md#error-8141)。

* Error Number: 8143

    非事务 DML 语句的一个 batch 报错，语句中止，请参考[非事务 DML 语句](/non-transactional-dml.md)

* Error Number: 8147

   当 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 设置为 `OFF` 时，为保证事务的正确性，SQL 语句执行时产生的任何错误都可能导致 TiDB 返回 `8147` 报错并中止当前事务。具体的错误原因，请参考对应的报错信息。详见[约束](/constraints.md#悲观事务)。

* Error Number: 8200

    尚不支持的 DDL 语法。请参考[与 MySQL DDL 的兼容性](/mysql-compatibility.md#ddl-的限制)。

* Error Number: 8214

    DDL 操作被 admin cancel 操作终止。

* Error Number: 8215

    Admin Repair 表失败，如果遇到该报错请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8216

    自动随机列使用的方法不正确，请参考 [auto random 功能文档](/auto-random.md)进行修改。

* Error Number: 8223

    检测出数据与索引不一致的错误，如果遇到该报错请向 PingCAP 工程师或通过官方论坛寻求帮助。

* Error Number: 8224

    找不到 DDL job，请检查 restore 操作指定的 job id 是否存在。

* Error Number: 8225

    DDL 已经完成，无法被取消。

* Error Number: 8226

    DDL 几乎要完成了，无法被取消。

* Error Number: 8227

    创建 Sequence 时使用了不支持的选项，支持的选项的列表可以参考 [Sequence 使用文档](/sql-statements/sql-statement-create-sequence.md#参数说明)。

* Error Number: 8228

    在 Sequence 上使用 `setval` 时指定了不支持的类型，该函数的示例可以在 [Sequence 使用文档](/sql-statements/sql-statement-create-sequence.md#示例)中找到。

* Error Number: 8229

    事务超过存活时间，遇到该问题可以提交或者回滚当前事务，开启一个新事务。

* Error Number: 8230

    TiDB 目前不支持在新添加的列上使用 Sequence 作为默认值，如果尝试进行这类操作会返回该错误。

* Error Number: 9001

    完整的报错信息为 `ERROR 9001 (HY000) : PD Server Timeout`。

    请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络。

* Error Number: 9002

    完整的报错信息为 `ERROR 9002 (HY000) : TiKV Server Timeout`。

    请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络。

* Error Number: 9003

    完整的报错信息为 `ERROR 9003 (HY000) : TiKV Server is Busy`。

    TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志。

* Error Number: 9004

    完整的报错信息为 `ERROR 9004 (HY000) : Resolve Lock Timeout`。

    清理锁超时，当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码是否有锁争用。

* Error Number: 9005

    完整的报错信息为 `ERROR 9005 (HY000) : Region is unavailable`。

    访问的 Region 不可用，某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志。

* Error Number: 9006

    完整的报错信息为 `ERROR 9006 (HY000) : GC life time is shorter than transaction duration`。

    GC Life Time 间隔时间过短，长事务本应读到的数据可能被清理了。你可以使用如下命令修改 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 的值：

    ```sql
    SET GLOBAL tidb_gc_life_time = '30m';
    ```

    其中 30m 代表仅清理 30 分钟前的数据，这可能会额外占用一定的存储空间。

* Error Number: 9007

    报错信息以 `ERROR 9007 (HY000) : Write conflict` 开头。

    如果报错信息中含有 "reason=LazyUniquenessCheck"，说明是悲观事务并且设置了 `@@tidb_constraint_check_in_place_pessimistic=OFF`，业务中存在唯一索引上的写冲突，此时悲观事务不能保证执行成功。可以在应用测重试事务，或将该变量设置成 `ON` 绕过。详见[约束](/constraints.md#悲观事务)。

* Error Number: 9008

    同时向 TiKV 发送的请求过多，超过了限制。请调大 `tidb_store_limit` 或将其设置为 `0` 来取消对请求流量的限制。

* Error Number: 9010

    TiKV 无法处理这条 raft log，请检查 TiKV Server 状态/监控/日志。

* Error Number: 9012

    请求 TiFlash 超时。请检查 TiFlash Server 状态/监控/日志以及 TiDB Server 与 TiFlash Server 之间的网络。

* Error Number: 9013

    TiFlash 操作繁忙。该错误一般出现在数据库负载比较高时。请检查 TiFlash Server 的状态/监控/日志。

### MySQL 原生报错汇总

* Error Number: 2013 (HY000)

    完整的报错信息为 `ERROR 2013 (HY000): Lost connection to MySQL server during query`。

    排查方法如下：

    - log 中是否有 panic
    - dmesg 中是否有 oom，命令：`dmesg -T | grep -i oom`
    - 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用，会被操作系统 kill。

* Error Number: 1105 (HY000)

    完整的报错信息为 `ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004))`

    这类问题一般是 TiDB 和 TiKV 版本不匹配，在升级过程尽量一起升级，避免版本 mismatch。

* Error Number: 1148 (42000)

    完整的报错信息为 `ERROR 1148 (42000): the used command is not allowed with this TiDB version`。

    这个问题是因为在执行 `LOAD DATA LOCAL` 语句的时候，MySQL 客户端不允许执行此语句（即 `local_infile` 选项为 0）。解决方法是在启动 MySQL 客户端时，用 `--local-infile=1` 选项。具体启动指令类似：`mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`。有些 MySQL 客户端需要设置而有些不需要设置，原因是不同版本的 MySQL 客户端对 `local-infile` 的默认值不同。

* Error Number: 9001 (HY000)

    完整的报错信息为 `ERROR 9001 (HY000): PD server timeout start timestamp may fall behind safe point`

    这个报错一般是 TiDB 访问 PD 出了问题，TiDB 后台有个 worker 会不断地从 PD 查询 safepoint，如果超过 100s 查不成功就会报这个错。一般是因为 PD 磁盘操作过忙、反应过慢，或者 TiDB 和 PD 之间的网络有问题。TiDB 常见错误码请参考[错误码与故障诊断](/error-codes.md)。

* TiDB 日志中的报错信息：EOF

    当客户端或者 proxy 断开连接时，TiDB 不会立刻察觉连接已断开，而是等到开始往连接返回数据时，才发现连接已断开，此时日志会打印 EOF 错误。

## 故障诊断

参见[故障诊断文档](/troubleshoot-tidb-cluster.md)。
