---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

发版日期：2021 年 5 月 28 日

TiDB 版本：4.0.13

## 新功能

+ TiDB

    - 支持将列属性 `AUTO_INCREMENT` 变更为 `AUTO_RANDOM` [#24608](https://github.com/pingcap/tidb/pull/24608)
    - 引入 `infoschema.client_errors_summary` 表，用以追踪返回给客户端的错误 [#23267](https://github.com/pingcap/tidb/pull/23267)

## 提升改进

+ TiDB

    - 当内存中的统计信息缓存是最新的时，避免后台作业频繁读取 `mysql.stats_histograms` 表 [#24352](https://github.com/pingcap/tidb/pull/24352)

+ TiKV

    - 使 `store used size` 的计算过程更精确 [9904](https://github.com/tikv/tikv/pull/9904)
    - 在 `EpochNotMatch` 消息中返回更多的 Region 以降低 Region miss 的发生 [9731](https://github.com/tikv/tikv/pull/9731)
    - 加快内存占用的释放速度 [10035](https://github.com/tikv/tikv/pull/10035)

+ PD

    - 优化 TSO 处理时间的统计指标 [#3524](https://github.com/pingcap/pd/pull/3524)
    - 更新 Dashboard 的版本至 v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ TiFlash

    - 自动清除过期历史数据以释放磁盘空间

+ Tools

    + Backup & Restore (BR)

        - 支持备份恢复系统库 `mysql` 下的用户表 [#1077](https://github.com/pingcap/br/pull/1077)
        - 更新 `checkVersion` 以检查集群版本和备份数据版本 [#1090](https://github.com/pingcap/br/pull/1090)
        - 容忍在备份期间集群中出现少数 TiKV 节点宕机 [#1062](https://github.com/pingcap/br/pull/1062)

    + TiCDC

        - 为内部处理单元增加流程控制，避免出现内存溢出问题 [#1751](https://github.com/pingcap/ticdc/pull/1751)
        - 增加 Unified Sorter 清理陈旧临时文件的功能，禁止多个 `cdc` 服务共享 `sort-dir` 目录 [#1741](https://github.com/pingcap/ticdc/pull/1741)
        - 给 Failpoint 增加 HTTP 接口调用 [#1732](https://github.com/pingcap/ticdc/pull/1732)

## Bug 修复

+ TiDB

    - 修复带有子查询的 `UPDATE` 语句更新生成列时会 panic 的问题 [#24658](https://github.com/pingcap/tidb/pull/24658)
    - 修复使用多列索引读取数据时返回结果重复的问题 [#24634](https://github.com/pingcap/tidb/pull/24634)
    - 修复在 DIV 表达式中使用 `BIT` 类型常量作为除数造成查询结果错误的问题 [#24266](https://github.com/pingcap/tidb/pull/24266)
    - 修复 `NO_ZERO_IN_DATE` SQL 模式对 DDL 语句中设置的列默认值无效的问题 [#24185](https://github.com/pingcap/tidb/pull/24185)
    - 修复 `BIT` 类型列与整型列进行 `UNION` 并集运算时，查询结果出错的问题 [#24026](https://github.com/pingcap/tidb/pull/24026)
    - 修复 `BINARY` 类型与 `CHAR` 类型比较时，错误生成了 `TableDual` 执行计划的问题 [#23917](https://github.com/pingcap/tidb/pull/23917)
    - 修复 `insert ignore on duplicate` 非预期的删除表记录的问题 [#23825](https://github.com/pingcap/tidb/pull/23825)
    - 修复 Audit 插件导致 TiDB panic 的问题 [#23819](https://github.com/pingcap/tidb/pull/23819)
    - 修复 `HashJoin` 算子未正确处理排序规则的问题 [#23812](https://github.com/pingcap/tidb/pull/23812)
    - 修复悲观事务中，`batch_point_get` 处理异常值出错导致连接断开的问题 [#23778](https://github.com/pingcap/tidb/pull/23778)
    - 修复 `tidb_row_format_version` 配置项的值被设置为 `1`，且 `enable_new_collation` 的值被设置为 `true` 时，数据索引不一致的问题 [#23772](https://github.com/pingcap/tidb/pull/23772)
    - 修复整型列与字符串类型常量比较时，查询结果出错的问题 [#23705](https://github.com/pingcap/tidb/pull/23705)
    - 修复 `approx_percent` 函数中传入 `BIT` 类型列时出错的问题 [#23702](https://github.com/pingcap/tidb/pull/23702)
    - 修复执行 TiFlash 批量请求时，TiDB 误报 `TiKV server timeout` 的问题 [#23700](https://github.com/pingcap/tidb/pull/23700)
    - 修复 `IndexJoin` 在前缀列索引上计算结果出错的问题 [#23691](https://github.com/pingcap/tidb/pull/23691)
    - 修复由于 `BINARY` 类型列上排序规则处理不当导致查询结果出错的问题 [#23598](https://github.com/pingcap/tidb/pull/23598)
    - 修复当 `UPDATE` 语句中存在含 `HAVING` 子句的连接查询时，执行出错的问题 [#23575](https://github.com/pingcap/tidb/pull/23575)
    - 修复比较类型表达式中使用 `NULL` 常量导致 TiFlash 计算结果出错的问题 [#23474](https://github.com/pingcap/tidb/pull/23474)
    - 修复 `YEAR` 类型列与字符类型常量比较结果出错的问题 [#23335](https://github.com/pingcap/tidb/pull/23335)
    - 修复 `session.group_concat_max_len` 被设置得过小时，`group_concat` 执行崩溃的问题 [#23257](https://github.com/pingcap/tidb/pull/23257)
    - 修复 `TIME` 类型列上使用 `BETWEEN` 表达式计算结果出错的问题 [#23233](https://github.com/pingcap/tidb/pull/23233)
    - 修复 `DELETE` 语句中出现的权限检查问题 [#23215](https://github.com/pingcap/tidb/pull/23215)
    - 修复往 `DECIMAL` 列中插入非法字符串时不报错的问题 [#23196](https://github.com/pingcap/tidb/pull/23196)
    - 修复往 `DECIMAL` 类型列插入数据时解析出错的问题 [#23152](https://github.com/pingcap/tidb/pull/23152)
    - 修复 `USE_INDEX_MERGE` hint 无法生效的问题 [#22924](https://github.com/pingcap/tidb/pull/22924)
    - 修复使用 `ENUM` 或 `SET` 类型列作为 `WHERE` 过滤条件时，查询结果出错的问题 [#22814](https://github.com/pingcap/tidb/pull/22814)
    - 修复 Clustered Index 与 New Collation 同时使用时，查询结果出错的问题 [#21408](https://github.com/pingcap/tidb/pull/21408)
    - 修复 `enable_new_collation` 开启时，`ANALYZE` 出错的问题 [#21299](https://github.com/pingcap/tidb/pull/21299)
    - 修复视图处理默认 ROLE 时，未正确处理相关 DEFINER 的问题 [#24531](https://github.com/pingcap/tidb/pull/24531)
    - 修复取消 DDL Job 时卡住的问题 [#24445](https://github.com/pingcap/tidb/pull/24445)
    - 修复 `concat` 函数错误处理排序规则的问题 [#24300](https://github.com/pingcap/tidb/pull/24300)
    - 修复当 `SELECT` 域中包含 `IN` 子查询且子查询外侧表含有空值元组时，查询结果出错的问题 [#24022](https://github.com/pingcap/tidb/pull/24022)
    - 修复逆序扫表时，TiFlash 被优化器错误选用的问题 [#23974](https://github.com/pingcap/tidb/pull/23974)
    - 修复点查的返回结果中，列名与 MySQL 不一致的问题 [#23970](https://github.com/pingcap/tidb/pull/23970)
    - 修复在数据库名含有大写字母的库中执行 `show table status` 结果为空的问题 [#23958](https://github.com/pingcap/tidb/pull/23958)
    - 修复不同时拥有 `INSERT` 及 `DELETE` 权限的用户可以执行 `REPLACE` 操作的问题 [#23938](https://github.com/pingcap/tidb/pull/23938)
    - 修复由于未正确处理排序规则导致的 `concat`/`make_set`/`insert` 表达式计算结果出错的问题 [#23878](https://github.com/pingcap/tidb/pull/23878)
    - 修复在含有 RANGE 分区的表上查询时，查询崩溃的问题 [#23689](https://github.com/pingcap/tidb/pull/23689)
    - 修复如下问题：在旧版本的集群中，若 `tidb_enable_table_partition` 被设置为 `false`，含有分区的表会被当作普通表处理。此时由旧版本升级至新版本时，在该表上执行 `batch point get` 查询会导致连接崩溃 [#23682](https://github.com/pingcap/tidb/pull/23682)
    - 修复 TiDB 被配置监听 TCP 连接及 UNIX 套接字时，TCP 连接中远程主机未被正确验证的问题 [#23513](https://github.com/pingcap/tidb/pull/23513)
    - 修复由于非默认的排序规则导致查询结果出错的问题 [#22923](https://github.com/pingcap/tidb/pull/22923)
    - 修复 Grafana 的 **Coprocessor Cache** 面板不显示数据的问题 [#22617](https://github.com/pingcap/tidb/pull/22617)
    - 修复优化器访问统计信息缓存时出错的问题 [#22565](https://github.com/pingcap/tidb/pull/22565)

+ TiKV

    - 修复因磁盘写满后 `file_dict` 写入不完全导致 TiKV 无法重启的问题 [9963](https://github.com/tikv/tikv/pull/9963)
    - 限制 TiCDC 默认的扫描速度为 128MB/s [9983](https://github.com/tikv/tikv/pull/9983)
    - 减少 TiCDC 进行初次扫描的内存使用量 [10133](https://github.com/tikv/tikv/pull/10133)
    - 支持反压 TiCDC 扫描的速率 [10142](https://github.com/tikv/tikv/pull/10142)
    - 通过避免不必要的读取来获取 TiCDC 旧值以解决潜在的 OOM 问题 [10031](https://github.com/tikv/tikv/pull/10031)
    - 修复了由于读取旧值而导致的 TiCDC OOM 问题 [10197](https://github.com/tikv/tikv/pull/10197)
    - 为 S3 存储添加超时机制以避免 S3 客户端没有任何响应地挂起 [10132](https://github.com/tikv/tikv/pull/10132)

+ TiFlash

    - 修复未向 Prometheus 报告 `delta-merge-tasks` 数量的问题
    - 修复 `Segment Split` 期间发生进程崩溃的问题
    - 修复 Grafana 中 `Region write Duration` 面板位置错误的问题
    - 修复了存储引擎无法删除数据的潜在问题
    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题
    - 修复当使用通用 CI 排序规则时字符权重错误的问题
    - 修复被逻辑删除的表可能丢失数据的问题
    - 修复比较包含空字符的字符串时产生错误结果的问题
    - 修复输入列包含空常量时逻辑函数返回错误结果的问题
    - 修复逻辑函数仅接受数字类型输入的问题
    - 修复时间戳值为 `1970-01-01` 且时区偏移为负时计算结果不正确的问题
    - 修复 `Decimal256` 的哈希值计算结果不稳定的问题

+ TiCDC

    - 修复当 Sorter 的输入通道卡住时，流控导致的死锁问题 [1779](https://github.com/pingcap/ticdc/pull/1779)
    - 修复 TiCDC changefeed 断点卡住导致 TiKV GC safe point 不推进的问题 [#1756](https://github.com/pingcap/ticdc/pull/1756)
    - 回滚 `explicit_defaults_for_timestamp` 的改动，确保不用 `SUPER` 权限也可以同步数据到 MySQL [#1749](https://github.com/pingcap/ticdc/pull/1749)
