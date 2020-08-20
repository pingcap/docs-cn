---
title: TiDB 3.0.18 Release Notes
---

# TiDB 3.0.18 Release Notes

发版日期：2020 年 8 月 21 日

TiDB 版本：3.0.18

## Bug 修复

+ TiDB

    - 修复 Hash 函数对 Decimal 类型的错误处理 [#19185](https://github.com/pingcap/tidb/pull/19185)
    - 修复 Hash 函数对 Set 和 Enum 类型的错误处理  [#19175](https://github.com/pingcap/tidb/pull/19175)

+ TiKV

    - 将 GC 的失败日志从 Error 级别改成 Warning 级别 [#8444](https://github.com/tikv/tikv/pull/8444)

+ TiDB Lightning

    - 修复命令行参数 `--log-file` 无法生效的问题 [#345](https://github.com/pingcap/tidb-lightning/pull/345)
    - 修复 TiDB backend 遇到空的 binary/hex 报语法错误的问题 [#357](https://github.com/pingcap/tidb-lightning/pull/357)
    - 修复使用 TiDB backend 时非预期的 `switch-mode` 调用 [#368](https://github.com/pingcap/tidb-lightning/pull/368)

## 优化

+ TiDB Binlog

    - 支持更加细粒度的 Pump GC 时间 [#996](https://github.com/pingcap/tidb-binlog/pull/996)
