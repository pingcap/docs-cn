---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 Release Notes

发版日期：2020 年 9 月 29 日

TiDB 版本：4.0.7

## 新功能

+ PD

    - PD 客户端中添加 `GetAllMembers` 函数，用于获取 PD 成员信息 [#2980](https://github.com/pingcap/pd/pull/2980)

+ TiDB Dashboard

    - 支持生成统计指标关系图 [#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## 优化提升

+ TiDB

    - 为 `join` 算子添加更多执行信息 [#20093](https://github.com/pingcap/tidb/pull/20093)
    - 为 `EXPLAIN ANALYZE` 语句添加协处理器缓存命中率信息 [#19972](https://github.com/pingcap/tidb/pull/19972)
    - 支持将 `ROUND` 函数下推至 TiFlash [#19967](https://github.com/pingcap/tidb/pull/19967)
    - 在 `ANALYZE` 过程中为 `CMSketch` 添加默认值 [#19927](https://github.com/pingcap/tidb/pull/19927)
    - 重新更改某些日志错误信息以使其脱敏 [#20004](https://github.com/pingcap/tidb/pull/20004)
    - 支持接受来自 MySQL 8.0 客户端的连接 [#19959](https://github.com/pingcap/tidb/pull/19959)

+ TiKV

    - 支持日志输出为 JSON 格式 [#8382](https://github.com/tikv/tikv/pull/8382)

+ PD

    - operator 统计计数器增加的时间点，从创建时改为执行完毕时 [#2983](https://github.com/pingcap/pd/pull/2983)
    - 将 `make-up-replica` operator 调整为高优先级 [#2977](https://github.com/pingcap/pd/pull/2977)

+ TiFlash

    - 完善数据读取过程中遇到 Region meta 变更的错误处理

+ Tools

    + TiCDC

        - 提升开启 Old Value 后 MySQL Sink 的同步效率 [#955](https://github.com/pingcap/ticdc/pull/955)

    + Backup & Restore (BR)

        - 增加备份时链接中断重试 [#508](https://github.com/pingcap/br/pull/508)

    + TiDB Lightning

        - 增加动态设置 log 级别的 HTTP 接口 [#393](https://github.com/pingcap/tidb-lightning/pull/393)

## Bug 修复

+ TiDB

    - 修复向量化函数 `and`/`or`/`COALESCE` 因为提前计算导致的问题 [#20092](https://github.com/pingcap/tidb/pull/20092)
    - 修复不同存储类型导致相同的执行计划摘要的问题 [#20076](https://github.com/pingcap/tidb/pull/20076)
    - 修复错误函数 `!= any()` 的错误表现 [#20062](https://github.com/pingcap/tidb/pull/20062)
    - 修复当慢日志文件不存在时输出慢日志报错的问题 [#20051](https://github.com/pingcap/tidb/pull/20051)
    - 修复当上下文取消后 Region 请求不断重试的问题 [#20031](https://github.com/pingcap/tidb/pull/20031)
    - 修复查询 `cluster_slow_query` 表的时间类型在 streaming 的请求下报错的问题 [#19943](https://github.com/pingcap/tidb/pull/19943)
    - 修复 DML 语句使用 `case when` 函数时可能导致 schema 改变的问题 [#20095](https://github.com/pingcap/tidb/pull/20095)
    - 修复 slow log 中 `prev_stmt` 的信息未脱敏的问题 [#20048](https://github.com/pingcap/tidb/pull/20048)
    - 修复当 tidb-server 不正常退出时没有释放表锁的问题 [#20020](https://github.com/pingcap/tidb/pull/20020)
    - 修复当插入 `ENUM` 和 `SET` 类型的字段产生不正确的错误信息的问题 [#19950](https://github.com/pingcap/tidb/pull/19950)
    - 修复 `IsTrue` 函数在某些情况下的错误表现 [#19903](https://github.com/pingcap/tidb/pull/19903)
    - 修复在 PD 扩容或缩容情况下 `CLUSTER_INFO` 系统表可能不正常运行的问题 [#20026](https://github.com/pingcap/tidb/pull/20026)
    - 修复在控制表达式中某些情况下产生不必要的错误或报警信息 [#19910](https://github.com/pingcap/tidb/pull/19910)
    - 改变更新统计信息的方式以避免造成 OOM 的情况 [#20013](https://github.com/pingcap/tidb/pull/20013)

+ TiKV

    - 修复 TLS 握手失败后会导致 Status API 不可用的问题 [#8649](https://github.com/tikv/tikv/pull/8649)
    - 修复一些平台上可能存在潜在未定义行为的问题 [#7782](https://github.com/tikv/tikv/pull/7782)
    - 修复执行 `UnsafeDestroyRange` 操作时生成快照可能导致 Panic 的问题 [#8681](https://github.com/tikv/tikv/pull/8681)

+ PD

    - 修复当 `balance-region` 开启时，如果存在 Region 没有 Leader，可能会导致 PD panic 的问题 [#2994](https://github.com/pingcap/pd/pull/2994)
    - 修复 Region 合并后 Region 大小和 Region key 数量的统计偏差 [#2985](https://github.com/pingcap/pd/pull/2985)
    - 修复热点统计不正确的问题 [#2991](https://github.com/pingcap/pd/pull/2991)
    - 修复 `redirectSchedulerDelete` 中未进行 `nil` 判断的问题 [#2974](https://github.com/pingcap/pd/pull/2974)

+ TiFlash

    - 修正 right outer join 结果错误的问题

+ Tools

    + Backup & Restore (BR)

        - 修复了在恢复数据后导致 TiDB 配置变更的错误 [#509](https://github.com/pingcap/br/pull/509)

    + Dumpling

        - 修复了在某些变量为空的情况下 metadata 解析失败的问题 [#150](https://github.com/pingcap/dumpling/pull/150)
