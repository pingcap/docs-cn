---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 Release Notes

发版日期：2021 年 2 月 4 日

TiDB 版本：4.0.11

## 兼容性更改

## 新功能

+ TiFlash

    - 增加排队处理 Coprocessor 任务的线程池以减小 OOM 几率, 随之增加两项配置项 `cop_pool_size` 与 `batch_cop_pool_size`, 默认为 `物理核数 * 2`. [#1312](https://github.com/pingcap/tics/pull/1312)

## 改进提升

+ TiFlash

    - 优化 date_format 函数的性能 [#1339](https://github.com/pingcap/tics/pull/1339)
    - 优化处理 ingest SST 时的内存开销

## Bug 修复

+ TiFlash

    - 修正读取数据时有可能导致 crash 的问题 [#1358](https://github.com/pingcap/tics/pull/1358)
    - 修正 DDL 操作后写入的数据可能会在 compaction 后丢失的问题 [#1350](https://github.com/pingcap/tics/pull/1350)
