---
title: TiDB 3.0.17 Release Notes
---

# TiDB 3.0.17 Release Notes

发版日期：2020 年 8 月 3 日

TiDB 版本：3.0.17

## Bug 修复

+ TiDB

    - 当一个查询中含有 `IndexHashJoin` 或 `IndexMergeJoin` 算子，且该算子的子节点发生 panic 时，返回客户端 panic 的原因，而非返回空结果 [#18498](https://github.com/pingcap/tidb/pull/18498)
    - 修复形如 `SELECT a FROM t HAVING t.a` 的查询返回 `UnknowColumn` 错误的问题 [#18432](https://github.com/pingcap/tidb/pull/18432)
    - 当一张表没有主键，或其主键为整型时，禁止在这张表上执行添加主键 [#18342](https://github.com/pingcap/tidb/pull/18342)
    - 对 `EXPLAIN FORMAT="dot" FOR CONNECTION` 始终返回空结果 [#17157](https://github.com/pingcap/tidb/pull/17157)
    - 修复 `STR_TO_DATE` 函数处理 `'%r'` 和 `'%h'` 的行为 [#18725](https://github.com/pingcap/tidb/pull/18725)

+ TiKV

    - 修复在 Region 合并过程中可能导致读到旧数据的问题 [#8111](https://github.com/tikv/tikv/pull/8111)
    - 修复调度时可能产生内存泄漏的问题 [#8355](https://github.com/tikv/tikv/pull/8355)

+ TiDB Lightning

    - 解决 `log-file` 参数不生效的问题 [#345](https://github.com/pingcap/tidb-lightning/pull/345)

## 优化

+ TiDB

    - 将配置项 `query-feedback-limit` 默认值从 1024 修改为 512, 并优化统计信息反馈机制，降低其对集群的性能影响 [#18770](https://github.com/pingcap/tidb/pull/18770)
    - 限制单次 split 请求中的 Region 个数 [#18694](https://github.com/pingcap/tidb/pull/18694)
    - 加速 HTTP API `/tiflash/replica` 在集群中存在大量历史 DDL 记录时的访问速度 [#18386](https://github.com/pingcap/tidb/pull/18386)
    - 提升索引等值条件下的行数估算准确率 [#17609](https://github.com/pingcap/tidb/pull/17609)
    - 加快 `kill tidb conn_id` 的响应速度 [#18506](https://github.com/pingcap/tidb/pull/18506)

+ TiKV

    - 新增 `hibernate-timeout` 配置支持推后 Region 休眠时间，减少 Region 休眠对滚动升级的影响 [#8207](https://github.com/tikv/tikv/pull/8207)

+ TiDB Lightning

    - 废弃 `[black-white-list]` 参数，新增一种更加简单易用的过滤规则 [#332](https://github.com/pingcap/tidb-lightning/pull/332)
