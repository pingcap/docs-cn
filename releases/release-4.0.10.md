---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 Release Notes

发版日期：2021 年 1 月 15 日

TiDB 版本：4.0.10

## 兼容性更改


## 新功能


## 改进提升

+ TiDB

    - 添加 `txn-entry-size-limit` 配置项，用于限制事务中单个 key-value 记录的大小 [#21843](https://github.com/pingcap/tidb/pull/21843)

## Bug 修复

+ TiDB

    - 修复由于并发导致的 batch client 超时问题 [#22336](https://github.com/pingcap/tidb/pull/22336)
    - 修复由于并发地自动捕获 SQL 绑定而导致的重复绑定问题 [#22295](https://github.com/pingcap/tidb/pull/22295)
    - 当日志级别为 'debug' 时，让 SQL 绑定的自动捕获正确运行 [#22293](https://github.com/pingcap/tidb/pull/22293)
    - 当 region 合并正在发生时，正确地释放锁 [#22267](https://github.com/pingcap/tidb/pull/22267)
    - 对 datetime 类型的用户变量返回正确的值 [#22143](https://github.com/pingcap/tidb/pull/22143)
    - 修复错误使用 Index Merge 访问方式的问题 [#22124](https://github.com/pingcap/tidb/pull/22124)
    - 修复由于执行计划缓存导致 TiFlash 报 `wrong precision` 错误的问题 [#21960](https://github.com/pingcap/tidb/pull/21960)
    - 修复由于 schema 变更导致的错误结果 [#21596](https://github.com/pingcap/tidb/pull/21596)
    - 避免在 `ALTER TABLE` 中不必要的 column flag 更改 [#21474](https://github.com/pingcap/tidb/pull/21474)
    - 让包含子查询块别名的 optimizer hint 生效 [#21380](https://github.com/pingcap/tidb/pull/21380)
    - 为 IndexHashJoin 和 IndexMergeJoin 生成正确的 optimizer hint [#21020](https://github.com/pingcap/tidb/pull/21020)
