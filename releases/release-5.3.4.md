---
title: TiDB 5.3.4 Release Note
---

# TiDB 5.3.4 Release Note

发版日期：2022 年 xx 月 xx 日

TiDB 版本： 5.3.4

## 兼容性变更

## 提升改进

+ TiDB

    <!--sql-infra owner: @Defined2014-->

    <!--executor owner: @zanmato1984-->

    <!--transaction owner: @cfzjywxk-->

    <!--planner owner: @qw4990-->

+ TiKV

    <!--owner: @v01dstar-->

    - (dup) 当 TLS 证书更新时自动重新加载，以提升可用性 [#12546](https://github.com/tikv/tikv/issues/12546)

+ PD

    <!--owner: @nolouch-->

+ TiFlash

    <!--compute owner: @zanmato1984-->

    <!--storage owner: @flowbehappy-->

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Lightning

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

## Bug 修复

+ TiDB

    <!--sql-infra owner: @Defined2014-->

    - (dup) 修复 Region 合并情况下 Region cache 没有及时被清理的问题 [#37141](https://github.com/pingcap/tidb/issues/37141)
    - (dup) 修复 `ENUM` 或 `SET` 类型的列因为编码错误导致写入数据错误的问题 [#32302](https://github.com/pingcap/tidb/issues/32302)
    - (dup) 修复数据库级别的权限清理不正确的问题 [#38363](https://github.com/pingcap/tidb/issues/38363)
    - (dup) 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293)
    - (dup)  修复 `KILL TIDB` 在空闲链接上无法立即生效的问题 [#24031](https://github.com/pingcap/tidb/issues/24031)
    - 修复 `adddate` 和 `subdate` 函数返回值类型的问题 [#36394](https://github.com/pingcap/tidb/issues/36394)
    - 修复 Parser 恢复 `table option` 中 `INSERT_METHOD` 字段错误的问题 [#38368](https://github.com/pingcap/tidb/issues/38368)
    - 修复 MySQL 5.1 及之前客户端连接 TiDB Server 鉴权失败的问题 [#29725](https://github.com/pingcap/tidb/issues/29725)

    <!--executor owner: @zanmato1984-->

    - (dup) 修复当 `GREATEST` 和 `LEAST`  函数传入无符号整型值时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - (dup) 修复 `concat(ifnull(time(3))` 的结果与 MySQL 不一致的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - avoid sum from avg overflow [#29952](https://github.com/pingcap/tidb/issues/29952)
    - add an unit test case for unreasonable invoking Close [#30587](https://github.com/pingcap/tidb/issues/27125)
    - HashJoinExec checks the buildError even if the probeSide is empty [#30289](https://github.com/pingcap/tidb/issues/30289)
    - expression: resize the result for IfXXSig [#37414](https://github.com/pingcap/tidb/issues/37414)
    - change date_add and date_sub string_(int/string/real/decimal) function return type to string. [#27573](https://github.com/pingcap/tidb/issues/27573)
    - fix hashjoin goleak [#39026](https://github.com/pingcap/tidb/issues/39026)
    - fix: the results of tikv and tiflash are different [#37258](https://github.com/pingcap/tidb/issues/37258)

    <!--transaction owner: @cfzjywxk-->

    <!--planner owner: @qw4990-->

    - (dup) 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)
    - (dup) 修复当 `ORDER BY` 子句里包含关联子查询时与 `GROUP CONCAT` 一起执行可能会导致出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216)
    - Fix the issue that set wrong length and width for Decimal and Real when using plan-cache [#29565](https://github.com/pingcap/tidb/issues/29565)
    - add an unit test case for unreasonable invoking Close [#27125](https://github.com/pingcap/tidb/issues/27125)

+ TiKV

    <!--owner: @v01dstar-->

+ PD

    <!--owner: @nolouch-->

    - (dup) 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) 修复 Stream 超时问题，提高 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207)

+ TiFlash

    <!--compute owner: @zanmato1984-->

    - fix: the results of tikv and tiflash are different [#5849](https://github.com/pingcap/tiflash/issues/5849)
    - fix inconsistent result before deleting some rows [#6127](https://github.com/pingcap/tiflash/issues/6127)

    <!--storage owner: @flowbehappy-->

    - Fix an invalid default value cause bootstrap failed [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

        - use white list for retryable error [#6698](https://github.com/pingcap/tiflow/issues/6698)

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Lightning

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->
