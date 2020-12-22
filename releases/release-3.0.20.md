---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 Release Notes

发版日期：2020 年 12 月 23 日

TiDB 版本：3.0.20

## 改进提升

+ TiKV

    - 增加 `end_point_slow_log_threshold` 配置 [#9145](https://github.com/tikv/tikv/pull/9145)

## Bug 修复

+ TiDB

    - 修复错误缓存悲观事务提交状态的问题。 [#21706](https://github.com/pingcap/tidb/pull/21706)
    - 修复当查询  `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` 是，统计信息不准确的问题。 [#21319](https://github.com/pingcap/tidb/pull/21319)
    - 修复 pepare 语句 `load data` 时应该报错的问题。  [#21222](https://github.com/pingcap/tidb/pull/21222)
    - 修复当数据库名不是完全小写时，`DELETE` 语句没法正确删除数据的问题。 [#21205](https://github.com/pingcap/tidb/pull/21205)
    - 修复当生成递归视图时栈溢出的问题。 [#21000](https://github.com/pingcap/tidb/pull/21000)
    - 修复 TiKV 客户端 goroutine 泄漏的问题。 [#20863](https://github.com/pingcap/tidb/pull/20863)
    - 修复 year 类型默认值为 0 的问题 [#20828](https://github.com/pingcap/tidb/pull/20828)
    - 修复 Index Lookup Join 的 goroutine 泄漏问题。 [#20791](https://github.com/pingcap/tidb/pull/20791)
    - 修复悲观事务时 "insert select for update" 客户端收到 malformed packet 的问题。 [#20681](https://github.com/pingcap/tidb/pull/20681)
    - 修复 'posixrules' 时区错误的问题。 [#20605](https://github.com/pingcap/tidb/pull/20605)
    - 修复转换无符号整形到 bit 类型时的错误。 [#20362](https://github.com/pingcap/tidb/pull/20362)
    - 修复 bit 列类型默认值错误的问题。 [#20339](https://github.com/pingcap/tidb/pull/20339)
    - 修复当等值条件中有 Enum 和 Set 类型时结果可能错误的问题。 [#20296](https://github.com/pingcap/tidb/pull/20296)
    - 修复 `!= any()` 时的错误问题。 [#20061](https://github.com/pingcap/tidb/pull/20061)
    - 修复类型转换在 BETWEEN...AND... 中会遇到结果错误的问题。 [#21503](https://github.com/pingcap/tidb/pull/21503)
    - 修复 `ADDDATE` 函数兼容性的问题。 [#21008](https://github.com/pingcap/tidb/pull/21008)
    - 对新增的 Enum 列，设置正确的默认值。 [#20999](https://github.com/pingcap/tidb/pull/20999)
    - 修复 `select DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)` 这种 SQL 的结果问题，使之兼容 MySQL。 [#20627](https://github.com/pingcap/tidb/pull/20627)
    - 修复当修改列属性时，默认类型设置错误的问题。 [#20532](https://github.com/pingcap/tidb/pull/20532)
    - 修复 timestamp 函数的参数为 float 和 decimal 时，结果错误的问题。 [#20469](https://github.com/pingcap/tidb/pull/20469)
    - 修复统计信息可能会死锁的问题。 [#20424](https://github.com/pingcap/tidb/pull/20424)
    - 当 float 类型的数据溢出时，不应该被 INSERT。 [#20251](https://github.com/pingcap/tidb/pull/20251)

+ TiKV

    - 修复当 key 被已提交事务锁住并是删除操作时，会报出 key-exist 错误的问题 [#8931](https://github.com/tikv/tikv/pull/8931)

+ PD

    - 修复当 stale region 过多时，启动 PD 会打印过量日志的问题 [#3064](https://github.com/tikv/pd/pull/3064)