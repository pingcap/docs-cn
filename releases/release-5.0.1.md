---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 Release Notes

发版日期：2021 年 4 月 24 日

TiDB 版本：5.0.1

## 改进提升

+ TiDB
    
    - 支持 `VITESS_HASH()` 函数 [#23915](https://github.com/pingcap/tidb/pull/23915)

+ TiKV

    - 使用 `zstd` 压缩 Region Snapshot [#10005](https://github.com/tikv/tikv/pull/10005)

+ PD

    - 调整 Region 分数公式使其更适用于异构集群 [#3605](https://github.com/pingcap/pd/pull/3605)
    - 避免在添加 `scatter region` 调度器后出现的非预期统计行为 [#3602](https://github.com/pingcap/pd/pull/3602)

+ Tools

    + Backup & Restore (BR)

        - 删除 Summary 日志中一些容易被误解的信息 [#1009](https://github.com/pingcap/br/pull/1009)

## Bug 修复

+ TiDB

    - 修复投影消除在投影结果为空时执行结果可能错误的问题 [#24093](https://github.com/pingcap/tidb/pull/24093)
    - 修复列包含 `NULL` 值时查询结果在某些情况下可能错误的问题 [#24063](https://github.com/pingcap/tidb/pull/24063)
    - 当有虚拟列参与扫描时不允许生成 MPP 计划 [#24058](https://github.com/pingcap/tidb/pull/24058)
    - 修复 Plan Cache 中对 `PointGet` 和 `TableDual` 错误的重复使用 [#24043](https://github.com/pingcap/tidb/pull/24043)
    - 修复优化器在为聚簇索引构建 `IndexMerge` 执行计划时出现的错误 [#24042](https://github.com/pingcap/tidb/pull/24042)
    - 修复 BIT 类型相关错误的类型推导 [#24027](https://github.com/pingcap/tidb/pull/24027)
    - 修复某些优化器 Hint 在 `PointGet` 算子存在时无法生效的问题 [#23685](https://github.com/pingcap/tidb/pull/23685)
    - 修复 DDL 遇到错误回滚时可能失败的问题 [#24080](https://github.com/pingcap/tidb/pull/24080)
    - 修复二进制字面值常量的索引范围构造错误的问题 [#24041](https://github.com/pingcap/tidb/pull/24041)
    - 修复某些情况下 `IN` 语句的执行结果可能错误的问题 [#24023](https://github.com/pingcap/tidb/pull/24023)
    - 修复某些字符串函数的返回结果错误的问题 [#23879](https://github.com/pingcap/tidb/pull/23879)
    - 执行 `REPLACE` 语句需要用户同时拥有 `INSERT` 和 `DELETE` 权限 [#23939](https://github.com/pingcap/tidb/pull/23939)
    - 修复点查时出现的的性能回退 [#24070](https://github.com/pingcap/tidb/pull/24070)
    - 修复因错误比较二进制与字节而导致的 `TableDual` 计划错误的问题 [#23918](https://github.com/pingcap/tidb/pull/23918)

+ TiKV

    - 修复了 Coprocessor 未正确处理 `IN` 表达式有符号整数或无符号整数类型数据的问题 [#10018](https://github.com/tikv/tikv/pull/10018)
    - 修复了在批量 ingest SST 文件后产生大量空 Region 的问题 [#10015](https://github.com/tikv/tikv/pull/10015)
    - 修复了在 `cast_string_as_time` 中输入非法的 UTF-8 字节后导致崩溃的问题 [#9995](https://github.com/tikv/tikv/pull/9995)
    - 修复了 file dictionary 文件损坏之后 TiKV 无法启动的问题 [#9992](https://github.com/tikv/tikv/pull/9992)

+ TiFlash

    - 修复存储引擎无法删除某些范围数据的问题
    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `receiver` 可能无法在 10 秒内找到对应任务的问题
    - 修复 `cancelMPPQuery` 中可能存在无效迭代器的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复当使用 `prefix key` 时出现范围重叠报错的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复列名重复会引发报错的问题
    - 修复 MPP 执行计划无法被解析的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题

+ Tools

    + TiDB Lightning

        - 修复导入过程中进度日志中的表数量不准确的问题 [#1005](https://github.com/pingcap/br/pull/1005)

    + Backup & Restore (BR)
        - 修复实际的备份速度超过 `--ratelimit` 限制的问题 [#1026](https://github.com/pingcap/br/pull/1026)
        - 修复备份期间少数 TiKV 节点不可用导致的备份中断问题 [#1019](https://github.com/pingcap/br/pull/1019)
        - 修复 TiDB Lightning 在导入过程中进度日志中的表数量不准确的问题 [#1005](https://github.com/pingcap/br/pull/1005)

    + TiCDC

        - 修复 Unified Sorter 中的并发问题并过滤无用的错误消息 [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - 修复同步到 MinIO 时，重复创建目录会导致同步中断的问题 [#1672](https://github.com/pingcap/ticdc/pull/1672)
        - 默认开启会话变量 `explicit_defaults_for_timestamp`，使得下游 MySQL 5.7 和上游 TiDB 的行为保持一致 [#1659](https://github.com/pingcap/ticdc/pull/1659)
        - 修复错误地处理 `io.EOF` 可能导致同步中断的问题 [#1648](https://github.com/pingcap/ticdc/pull/1648)
        - 修正 TiCDC 面板中的 TiKV CDC endpoint CPU 统计信息 [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - 增加 `defaultBufferChanSize` 来避免某些情况下同步阻塞的问题 [#1632](https://github.com/pingcap/ticdc/pull/1632)
