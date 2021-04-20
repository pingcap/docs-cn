---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 Release Notes

发版日期：2021 年 4 月 23 日

TiDB 版本：5.0.1

## 兼容性更改

## 新功能

## 改进提升

+ TiKV

    - 使用 `zstd` 压缩 Region Snapshot [#10005](https://github.com/tikv/tikv/pull/10005)

## Bug 修复

+ TiDB

    - 修复投影消除在投影结果为空时执行结果可能错误的问题 [#24093](https://github.com/pingcap/tidb/pull/24093)
    - 修复某些情况下列允许为 NULL 时执行结果可能错误的问题 [#24063](https://github.com/pingcap/tidb/pull/24063)
    - 当有虚拟列参与运算时不允许生成 MPP 计划 [#24058](https://github.com/pingcap/tidb/pull/24058)
    - 修复 Plan Cache 中对 PointGet 和 TableDual 错误的重复使用 [#24043](https://github.com/pingcap/tidb/pull/24043)
    - IndexMerge 算子需要保留聚簇索引的输出 [#24042](https://github.com/pingcap/tidb/pull/24042)
    - 修复 BIT 类型相关的错误的类型推导 [#24027](https://github.com/pingcap/tidb/pull/24027)
    - 修复某些优化器 hint 在 PointGet 算子存在时无法生效的问题 [#23685](https://github.com/pingcap/tidb/pull/23685)
    - 修复某些情况下 DDL job 在将状态设置外 rolling back 时可能的参数解析失败的问题 [#24080](https://github.com/pingcap/tidb/pull/24080)
    - 修复二进制字面值常量的索引范围构造错误的问题 [#24041](https://github.com/pingcap/tidb/pull/24041)
    - 修复某些情况下 IN 语句执行结果可能错误的问题 [#24023](https://github.com/pingcap/tidb/pull/24023)
    - 修复某些字符串函数返回结果错误的问题 [#23879](https://github.com/pingcap/tidb/pull/23879)
    - 执行 REPLACE 语句需要用户同时拥有 INSERT 和 DELETE 的权限 [#23939](https://github.com/pingcap/tidb/pull/23939)
    - 修复点差时的性能回退 [#24070](https://github.com/pingcap/tidb/pull/24070)

+ TiKV

    - 修复了 coprocessor 的 IN 表达式未正确处理 unsigned/signed int 类型数据的问题 [#10018](https://github.com/tikv/tikv/pull/10018)
    - 修复了在 batch ingest SST 之后产生大量空 Region 的问题 [#10015](https://github.com/tikv/tikv/pull/10015)
    - 修复了 `cast_string_as_time` 输入非法的 UTF-8 值之和导致 panic 的问题 [#9995](https://github.com/tikv/tikv/pull/9995)
    - 修复了“文件目录”文件损坏之后 TiKV 无法启动的问题 [#9992](https://github.com/tikv/tikv/pull/9992)
