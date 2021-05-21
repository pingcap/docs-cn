---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

发版日期：TBD

TiDB 版本：4.0.13

## 新功能

+ TiDB

    - 支持列属性 `AUTO_INCREMENT` 变更为 `AUTO_RANDOM` [#24608](https://github.com/pingcap/tidb/pull/24608)
    - 引入 `infoschema.client_errors_summary` 表，用以追踪返回给客户端的错误 [#23267](https://github.com/pingcap/tidb/pull/23267)

## 提升改进

+ TiDB

    - 当内存中的统计信息缓存是最新的时，避免后台作业频繁读取 mysql.stats_histograms 表 [#24352](https://github.com/pingcap/tidb/pull/24352)

+ PD

    - 优化 tso 处理时间的统计 metrics [#3524](https://github.com/pingcap/pd/pull/3524)
    - 更新 dashboard 的版本至  v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ TiFlash

    - 自动清除过期历史数据以释放磁盘空间

## Bug 修复

+ TiDB

    - Fix panic when subquery update stmt the table with generated columns. [#24658](https://github.com/pingcap/tidb/pull/24658)
    - 修复由多列索引读取数据时造成的返回结果重复的问题 [#24634](https://github.com/pingcap/tidb/pull/24634)
    - 修复在 DIV 表达式中使用 bit 类型常量作为除数造成的正确性问题 [#24266](https://github.com/pingcap/tidb/pull/24266)
    - 修复默认 SQL mode 下，`NO_ZERO_IN_DATE` 无效的问题. [#24185](https://github.com/pingcap/tidb/pull/24185)
    - 修复 bit 类型列与整型列 UNION，查询结果出错的问题 [#24026](https://github.com/pingcap/tidb/pull/24026)
    - 修复 binary 类型与 char 类型比较出错的问题 [#23917](https://github.com/pingcap/tidb/pull/23917)
    - 修复 `insert ignore on duplicate` 非预期的删除表记录的问题 [#23825](https://github.com/pingcap/tidb/pull/23825)
    - 修复 audit 插件导致 tidb panic 的问题 [#23819](https://github.com/pingcap/tidb/pull/23819)
    - 修复 HashJoin 执行未正确处理 collation 的问题 [#23812](https://github.com/pingcap/tidb/pull/23812)
    - 修复悲观事务中，batch_point_get 处理异常值出错导致连接断开的问题 [#23778](https://github.com/pingcap/tidb/pull/23778)
    - 修复 `tidb_row_format_version` 被设置为 1，且 `enable_new_collation` 被设置为 true 时，数据索引不一致的问题 [#23772](https://github.com/pingcap/tidb/pull/23772)
    - 修复整型列与字符串类型常量比较，查询结果出错的问题 [#23705](https://github.com/pingcap/tidb/pull/23705)
    - 修复 `approx_percent` 函数传入 bit 类型列时出错的问题 [#23702](https://github.com/pingcap/tidb/pull/23702)
    - 修复往 TiFlash 发送 batch 请求时，TiDB 误报 `TiKV server timeout` 的问题 [#23700](https://github.com/pingcap/tidb/pull/23700)
    - 修复 IndexJoin 在前缀列索引上计算结果出错的问题 [#23691](https://github.com/pingcap/tidb/pull/23691)
    - 修复由于 binary 类型列上 collation 处理不当导致的查询结果出错的问题 [#23598](https://github.com/pingcap/tidb/pull/23598)
    - 修复 update 语句中存在含 having 子句的 join 查询，执行出错的问题、 [#23575](https://github.com/pingcap/tidb/pull/23575)
    - 修复比较类型表达式中使用 NULL 常量导致 TiFlash 计算结果出错的问题 [#23474](https://github.com/pingcap/tidb/pull/23474)
    - 修复 year 类型列与字符类型常量比较结果出错的问题Fix unexpected result when comparing year column with string constant. [#23335](https://github.com/pingcap/tidb/pull/23335)
    - 修复 `session.group_concat_max_len` 被设置为 `group_concat` 执行出错的问题 [#23257](https://github.com/pingcap/tidb/pull/23257)
    - 修复 time 类型列上计算 between 表达式结果出错的问题 [#23233](https://github.com/pingcap/tidb/pull/23233)
    - 修复 DELETE 语句中权限检查的问题 [#23215](https://github.com/pingcap/tidb/pull/23215)
    - 修复往 decimal 类型列插入数据时，解析出错的问题 Fix some wrong error info when an the result of an expression out of range. [#23152](https://github.com/pingcap/tidb/pull/23152)
    - 修复 `USE_INDEX_MERGE` hint 无法生效的问题 [#22924](https://github.com/pingcap/tidb/pull/22924)
    - 修复使用 enum 或 set 类型列作为过滤条件时，查询结果出错的问题 [#22814](https://github.com/pingcap/tidb/pull/22814)
    - 修复 clustered index 与 new collation 同时使用时，查询结果出错的问题 [#21408](https://github.com/pingcap/tidb/pull/21408)
    - 修复 enable_new_collation 开启时，analyze 出错的问题 [#21299](https://github.com/pingcap/tidb/pull/21299)
    - 修复视图处理默认 ROLE 时，未正确处理 DEFINER 的问题 [#24531](https://github.com/pingcap/tidb/pull/24531)
    - 修复取消 DDL 作业时卡住的问题 [#24445](https://github.com/pingcap/tidb/pull/24445)
    - 修复 Concat 函数处理 collation 错误的问题 [#24300](https://github.com/pingcap/tidb/pull/24300)
    - 修复 select 域中包含 in 子查询，且子查询外侧表含有空值元组时，查询结果出错的问题 [#24022](https://github.com/pingcap/tidb/pull/24022)
    - 修复逆序扫表时，TiFlash 被错误使用的问题 [#23974](https://github.com/pingcap/tidb/pull/23974)
    - 修复点查的返回结果中，列名与 MySQL 不一致的问题 [#23970](https://github.com/pingcap/tidb/pull/23970)
    - 修复 `show table status` for the database with upper-cased name. [#23958](https://github.com/pingcap/tidb/pull/23958)
    - 修复不同时拥有 INSERT 及 DELETE 权限的用户可以执行 REPLACE 操作的问题 [#23938](https://github.com/pingcap/tidb/pull/23938)
    - 修复由于 collation 未正确处理导致的 concat/make_set/insert 表达式计算结果出错的问题 [#23878](https://github.com/pingcap/tidb/pull/23878)
    - 修复在含有 range partition 的表上查询时，查询崩溃的问题 [#23689](https://github.com/pingcap/tidb/pull/23689)
    - 修复如下问题：在旧版本的集群中，若 `tidb_enable_table_partition` 被设置为 false，含有 partition 的表会被作为普通表处理。此时由旧版本升级至新版本时，在该表上执行 batch point get 查询会导致连接崩溃 [#23682](https://github.com/pingcap/tidb/pull/23682)
    - 修复 TiDB 被配置监听 TCP 连接及 UNIX 套接字时，TCP 连接中远程主机未被正确验证的问题 [#23513](https://github.com/pingcap/tidb/pull/23513)
    - 修复由于非默认的 collation 导致的查询结果出错的问题 [#22923](https://github.com/pingcap/tidb/pull/22923)
    - 修复 Grafana 中 coprocessor cache 无显示数据的问题 [#22617](https://github.com/pingcap/tidb/pull/22617)
    - 修复优化器访问统计信息缓存时出错的问题 [#22565](https://github.com/pingcap/tidb/pull/22565)

+ TiFlash

    - 修复未向 Prometheus 报告 `delta-merge-tasks` 数量的问题
    - 修复 `Segment Split` 期间发生进程崩溃的问题
    - 修复 Grafana 中面板 `Region write Duration` 位置错误的问题
    - 修复了存储引擎无法删除数据的潜在问题
    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题
    - 修复当使用通用 CI Collation 时字符权重错误的问题
    - 修复被逻辑删除的表丢失数据的潜在问题
    - 修复比较包含空字符的字符串时产生错误结果的问题
    - 修复输入列包含空常量时逻辑函数返回错误结果的问题
    - 修复逻辑函数仅接受受数字类型输入的问题
    - 修复时间戳值为 `1970-01-01` 且时区偏移为负时计算结果不正确的问题
    - 修复 Decimal256 的哈希值计算结果不稳定的问题
