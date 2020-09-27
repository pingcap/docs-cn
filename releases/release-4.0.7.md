---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 Release Notes

发版日期：2020 年 9 月 29 日

TiDB 版本：4.0.7

## 新功能

+ TiDB

    - 

+ PD

    - PD 客户端中添加 `GetAllMembers` 函数，用于获取 PD 成员信息 [#2980](https://github.com/pingcap/pd/pull/2980)

+ TiDB Dashboard

    - 支持生成统计指标关系图 [#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## 优化提升

+ TiDB

    - 

+ TiKV

    - 

+ PD

    - operator 统计计数器增加的时间点，从创建时改为执行完毕时 [#2983](https://github.com/pingcap/pd/pull/2983)
    - 将 `make-up-replica` operator 调整为高优先级 [#2977](https://github.com/pingcap/pd/pull/2977)

+ TiFlash

    - 完善数据读取过程中遇到 Region meta 变更的错误处理

+ Tools

    + TiCDC

        - 提升开启 Old Value 后 MySQL Sink 的同步效率 [#955](https://github.com/pingcap/ticdc/pull/955)

    + Backup & Restore (BR)
s
        - 增加备份时链接中断重试 [#508](https://github.com/pingcap/br/pull/508)

    + Dumpling

        - 

    + TiDB Lightning

        - 增加动态设置 log 级别的 HTTP 接口 [#393](https://github.com/pingcap/tidb-lightning/pull/393)

    + TiDB Binlog

        - 

## Bug 修复

+ TiDB

    - 

+ TiKV

    - 

+ PD

    - 修复当 `balance-region` 开启时，如果存在 region 没有 leader，可能会导致 PD panic 的问题 [#2994](https://github.com/pingcap/pd/pull/2994)
    - 修复区域合并后 region 大小和 region key 数量的统计偏差 [#2985](https://github.com/pingcap/pd/pull/2985)
    - 修复热点统计不正确的问题 [#2991](https://github.com/pingcap/pd/pull/2991)
    - 修复 `redirectSchedulerDelete` 中未进行 `nil` 判断的问题  [#2974](https://github.com/pingcap/pd/pull/2974)

+ TiFlash

    - 修正 right outer join 结果错误的问题

+ Tools

    + TiCDC

        - 

    + Backup & Restore (BR)

        - 修复 SQL restore 中设置全局变量的问题 [#509](https://github.com/pingcap/br/pull/509)

    + Dumpling

        - 修复了在某些变量为空的情况下，metadata 解析失败的问题 [#150](https://github.com/pingcap/dumpling/pull/150)

    + TiDB Lightning

        - 
