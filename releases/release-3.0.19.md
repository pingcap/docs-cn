---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 Release Notes

发版日期：2020 年 9 月 25 日

TiDB 版本：3.0.19

## 兼容性变化


## 提升改进

+ TiDB

    - 缓解故障恢复对 QPS 的影响 [#19764](https://github.com/pingcap/tidb/pull/19764)
    - 支持调整 `union` 运算符的并发数 [#19885](https://github.com/pingcap/tidb/pull/19885)

+ TiKV

    - 永久开启 `sync_log` [#8636](https://github.com/tikv/tikv/pull/8636)

+ PD

    -

## Bug 修复

+ TiDB

    - 修复 `slow-log` 文件不存在导致查询出错的问题。 [#20050](https://github.com/pingcap/tidb/pull/20050)
    - 添加对 `SHOW STATS_META` 和 `SHOW STATS_BUCKET` 这两个命令的权限检查 [#19759](https://github.com/pingcap/tidb/pull/19759)
    - 禁止将 integer 的类型改成 decimal 的类型 [#19681](https://github.com/pingcap/tidb/pull/19681)
    - 修复 alter enum/set 没有检查一些限制的问题 [#20045](https://github.com/pingcap/tidb/pull/20045)
    - 修复 tidb-server 在 panic 后没有释放 table lock 的问题 [#20021](https://github.com/pingcap/tidb/pull/20021)
    - 修复 `OR` 运算符在 `WHERE` 子句中没有正确处理的问题 [#19901](https://github.com/pingcap/tidb/pull/19901)

+ TiKV

    - 修复 TiKV 的 status server 解析响应出错导致 panic 的问题 [#8540](https://github.com/tikv/tikv/pull/8540)

+ Tools

    + TiDB Lightning

        - 修复了严格模式下 CSV 中遇到不合法 UTF 字符集没有及时退出的问题 [#378](https://github.com/pingcap/tidb-lightning/pull/378)
