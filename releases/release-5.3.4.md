---
title: TiDB 5.3.4 Release Notes
---

# TiDB 5.3.4 Release Notes

发版日期：2022 年 11 月 24 日

TiDB 版本： 5.3.4

## 提升改进

+ TiKV

    - 当 TLS 证书更新时自动重新加载，以提升可用性 [#12546](https://github.com/tikv/tikv/issues/12546)

## Bug 修复

+ TiDB

    - 修复 Region 合并情况下 Region cache 没有及时被清理的问题 [#37141](https://github.com/pingcap/tidb/issues/37141)
    - 修复 `ENUM` 或 `SET` 类型的列因为编码错误导致写入数据错误的问题 [#32302](https://github.com/pingcap/tidb/issues/32302)
    - 修复数据库级别的权限清理不正确的问题 [#38363](https://github.com/pingcap/tidb/issues/38363)
    - 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293)
    - 修复 `KILL TIDB` 在空闲链接上无法立即生效的问题 [#24031](https://github.com/pingcap/tidb/issues/24031)
    - 修复 `date_add` 和 `date_sub` 函数返回类型的行为与 MySQL 不一致的问题 [#36394](https://github.com/pingcap/tidb/issues/36394), [#27573](https://github.com/pingcap/tidb/issues/27573)
    - 修复 Parser 恢复 `table option` 中 `INSERT_METHOD` 字段错误的问题 [#38368](https://github.com/pingcap/tidb/issues/38368)
    - 修复 MySQL 5.1 及之前版本客户端连接 TiDB Server 时鉴权失败的问题 [#29725](https://github.com/pingcap/tidb/issues/29725)
    - 修复当 `GREATEST` 和 `LEAST`  函数传入无符号整型值时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - 修复 `concat(ifnull(time(3))` 的结果与 MySQL 不一致的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复当从 TiFlash 查询 `avg()` 函数时，返回错误 `ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.` 的问题 [#29952](https://github.com/pingcap/tidb/issues/29952)
    - 修复查询 HashJoin 时，返回错误 `ERROR 1105 (HY000): close of nil channel` 的问题 [#30289](https://github.com/pingcap/tidb/issues/30289)
    - 修复 TiKV 和 TiFlash 在进行逻辑运算时结果不一致的问题 [#37258](https://github.com/pingcap/tidb/issues/37258)
    - 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373)
    - 修复合并多个 Region 后 Region cache 没有正确清理的问题 [#37174](https://github.com/pingcap/tidb/issues/37174)
    - 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)
    - 修复当 `ORDER BY` 子句里包含关联子查询时与 `GROUP CONCAT` 一起执行可能会导致出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216)
    - 修复使用 Plan Cache 时，由于 Decimal 和 Real 的 length 和 width 设置错误而导致的结果出错问题 [#29565](https://github.com/pingcap/tidb/issues/29565)

+ PD

    - 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - 修复 PD 在特定条件下不会创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)
    - 修复 Stream 超时问题，提高 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207)

+ TiFlash

    - 修复逻辑运算符在 UInt8 类型下查询结果出错的问题 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - 修复由于使用 `0.0` 作为整数类型的默认值导致 TiFlash 节点失败的问题，比如`` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + Dumpling

        - 修复 Dumpling 同时指定 `--compress` 配置和 S3 导出目录时无法导出数据的问题 [#30534](https://github.com/pingcap/tidb/issues/30534)

    + TiCDC

        - 修复由于没有及时上报 MySQL 相关错误导致同步任务状态不正确的问题 [#6698](https://github.com/pingcap/tiflow/issues/6698)
