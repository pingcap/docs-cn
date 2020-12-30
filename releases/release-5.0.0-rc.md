---
title: TiDB 5.0 RC Release Notes
---

# TiDB 5.0 RC Release Notes

发版日期：2020 年 12 月 31 日

TiDB 版本：5.0.0-rc

## 兼容性更改

+ TiFlash

    - 支持限制 DeltaIndex 的内存使用量，避免大数据量下内存使用过多的问题
    - 支持限制后台数据整理任务使用的 IO 写流量，降低对前台任务的影响

## 新功能

+ TiDB

    - 支持 `utf8mb4_unicode_ci` and `utf8_unicode_ci` collation
        - [project](https://github.com/pingcap/tidb/issues/17596)
        - [document](https://docs.pingcap.com/tidb/dev/character-set-and-collation#new-framework-for-collations)
    - 支持错误和日志信息脱敏
        - [project](https://github.com/pingcap/tidb/issues/18566)
        - [document](https://github.com/pingcap/tidb/blob/master/errno/logredaction.md)
    - 支持 Invisible Indexes
        - [project](https://github.com/pingcap/tidb/issues/9246)
        - [document](https://github.com/pingcap/tidb/pull/15366)
    - 支持 Async commit. Async Commit 优化了事务提交时间，在所有 prewrite 请求成功执行完后即可返回结果给客户端（实验特性）
        - [project](https://github.com/tikv/tikv/projects/34)
        - [document](https://github.com/pingcap/docs-cn/pull/5181)
    - 支持 clustered Index. 聚集索引可以提高某些查询的性能，例如点查（实验特性）
        - [project](https://github.com/pingcap/tidb/projects/45)
        - [document](https://docs.pingcap.com/tidb/dev/clustered-indexes)
    - 支持 `LIST` 和 `LIST COLUMNS` 分区表（实验特性）
        - [project](https://github.com/pingcap/tidb/issues/20678)
        - [document](https://docs.pingcap.com/zh/tidb/dev/partitioned-table#list-%E5%88%86%E5%8C%BA)
    - 提高 Index Selection 的准确度和鲁棒性（实验特性）
        - [#21817](https://github.com/pingcap/tidb/pull/21817)
        - [document](https://github.com/pingcap/docs-cn/pull/5164)

+ TiKV

    - 支持动态更改 RocksDB rate limiter 的自动调整模式

## 改进提升

+ TiDB

    - 收集更多的算子执行信息。
        - [issue](https://github.com/pingcap/tidb/issues/18663)
        - [document](https://docs.pingcap.com/zh/tidb/stable/sql-statement-explain-analyze#explain-analyze)
    - 优化批量删除场景下的性能。
        - [issue](https://github.com/pingcap/tidb/issues/18028)

+ TiFlash

    - 增加线程池排队处理 coprocessor 任务以降低执行高并发 coprocessor 时的内存压力
