---
title: TiDB 3.0.7 Release Notes
---

# TiDB 3.0.7 Release Notes

发版日期：2019 年 12 月 4 日

TiDB 版本：3.0.7

TiDB Ansible 版本：3.0.7

## TiDB

- 修复 TiDB server 本地时间落后于 TSO 时间时，可能造成锁的 TTL 过大的问题 [#13868](https://github.com/pingcap/tidb/pull/13868)
- 修复从字符串解析日期时，由于使用本地时区 (`gotime.Local`) 而导致解析结果的时区不正确的问题 [#13793](https://github.com/pingcap/tidb/pull/13793)
- 修复 `builtinIntervalRealSig` 的实现中，`binSearch` 方法不会返回 error，导致最终结果可能不正确的问题 [#13767](https://github.com/pingcap/tidb/pull/13767)
- 修复整型数据被转换为无符号浮点/Decimal 类型时，精度可能丢失造成数据错误的问题 [#13755](https://github.com/pingcap/tidb/pull/13755)
- 修复 Natural Outer Join 和 Outer Join 使用 `USING` 语法时，`not null` 标记没有被重置导致结果错误的问题 [#13739](https://github.com/pingcap/tidb/pull/13739)
- 修复更新统计信息时可能存在数据竞争，导致统计信息不准确的问题 [#13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV

- 判断死锁检测服务的第一个 Region 时，加上 Region 合法检测，防止信息不完整的 Region 导致误判 [#6110](https://github.com/tikv/tikv/pull/6110)
- 修复潜在的内存泄漏问题 [#6128](https://github.com/tikv/tikv/pull/6128)
