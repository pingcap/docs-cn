---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 Release Notes

发版日期：2020 年 9 月 25 日

TiDB 版本：3.0.19

## 兼容性变化

+ PD

    - 更改 PD 的导入路径 `pingcap/pd` 为 `tikv/pd` [#2779](https://github.com/pingcap/pd/pull/2779)
    - 更改 PD 的 copyright 信息 `PingCAP, Inc` 为 `TiKV Project Authors` [#2777](https://github.com/pingcap/pd/pull/2777)

## 提升改进

+ TiDB

    - 缓解故障恢复对 QPS 的影响 [#19764](https://github.com/pingcap/tidb/pull/19764)
    - 支持调整 `union` 运算符的并发数 [#19885](https://github.com/pingcap/tidb/pull/19885)

+ TiKV

    - 永久开启 `sync-log` [#8636](https://github.com/tikv/tikv/pull/8636)

+ PD

    - 添加关于 PD 重启的告警规则 [#2789](https://github.com/pingcap/pd/pull/2789)

## Bug 修复

+ TiDB

    - 修复 `slow-log` 文件不存在导致查询出错的问题 [#20050](https://github.com/pingcap/tidb/pull/20050)
    - 添加对 `SHOW STATS_META` 和 `SHOW STATS_BUCKET` 这两个命令的权限检查 [#19759](https://github.com/pingcap/tidb/pull/19759)
    - 禁止将 Decimal 类型改成 Integer 类型 [#19681](https://github.com/pingcap/tidb/pull/19681)
    - 修复更改 `ENUM`/`SET` 类型的列时没有检查限制的问题 [#20045](https://github.com/pingcap/tidb/pull/20045)
    - 修复 tidb-server 在 panic 后没有释放 table lock 的问题 [#20021](https://github.com/pingcap/tidb/pull/20021)
    - 修复 `OR` 运算符在 `WHERE` 子句中没有正确处理的问题 [#19901](https://github.com/pingcap/tidb/pull/19901)

+ TiKV

    - 修复 TiKV 的 status server 解析响应出错导致 panic 的问题 [#8540](https://github.com/tikv/tikv/pull/8540)

+ Tools

    + TiDB Lightning

        - 修复了严格模式下 CSV 中遇到不合法 UTF 字符集没有及时退出进程的问题 [#378](https://github.com/pingcap/tidb-lightning/pull/378)
