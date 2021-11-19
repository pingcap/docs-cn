---
title: TiDB 3.1 GA Release Notes
---

# TiDB 3.1 GA Release Notes

发版日期：2020 年 4 月 16 日

TiDB 版本：3.1.0 GA

TiDB Ansible 版本：3.1.0 GA

## 兼容性变化

+ TiDB

    - 支持 TiDB 在启动服务时，在开启 `report-status` 配置项情况下，如果发现 HTTP 监听端口不可用，则直接退出启动 [#16291](https://github.com/pingcap/tidb/pull/16291)

+ Tools

    - Backup & Restore (BR)

        * BR 不支持在 3.1 GA 版本之前的 TiKV 集群上进行恢复 [#233](https://github.com/pingcap/br/pull/233)

## 新功能

+ TiDB

    - 支持在 `explain format = "dot"` 中展示 coprocessor 任务的信息 [#16125](https://github.com/pingcap/tidb/pull/16125)
    - 通过 `disable-error-stack` 配置项减少日志的冗余 stack 信息 [#16182](https://github.com/pingcap/tidb/pull/16182)

+ Placement Driver (PD)

    - 优化热点 Region 调度 [#2342](https://github.com/pingcap/pd/pull/2342)

+ TiFlash

    - 添加上报 DeltaTree 引擎读写负载相关 metrics 信息
    - 支持 `fromUnixTime` 和 `dateFormat` 函数下推
    - 默认禁用粗粒度索引过滤器

+ TiDB Ansible

    - 新增 TiFlash 监控 [#1253](https://github.com/pingcap/tidb-ansible/pull/1253) [#1257](https://github.com/pingcap/tidb-ansible/pull/1257)
    - 优化 TiFlash 配置参数 [#1262](https://github.com/pingcap/tidb-ansible/pull/1262) [#1265](https://github.com/pingcap/tidb-ansible/pull/1265) [#1271](https://github.com/pingcap/tidb-ansible/pull/1271)
    - 优化 TiDB 启动脚本 [#1268](https://github.com/pingcap/tidb-ansible/pull/1268)

## Bug 修复

+ TiDB

    - 修复 merge join 在某些场景下 panic 的问题 [#15920](https://github.com/pingcap/tidb/pull/15920)
    - 修复在计算选择率时重复考虑某些表达式的问题 [#16052](https://github.com/pingcap/tidb/pull/16052)
    - 修复极端情况下 load 统计信息可能出现的 panic 的问题 [#15710](https://github.com/pingcap/tidb/pull/15710)
    - 修复 SQL query 中存在等价表达式在某些情况下无法识别导致报错的问题 [#16015](https://github.com/pingcap/tidb/pull/16015)
    - 修复从一个数据库中查询另一个数据库的 `view` 时报错的问题 [#15867](https://github.com/pingcap/tidb/pull/15867)
    - 修复 fast analyze handle 列时 panic 的问题 [#16080](https://github.com/pingcap/tidb/pull/16080)
    - 修复 `current_role` 输出结果字符集不正确的问题 [#16084](https://github.com/pingcap/tidb/pull/16084)
    - 完善 MySQL 连接握手错误相关日志 [#15799](https://github.com/pingcap/tidb/pull/15799)
    - 修复加载审计插件后端口探测活动导致 panic 的问题 [#16065](https://github.com/pingcap/tidb/pull/16065)
    - 修复因 `TypeNull` 类被错误识别为变长类型，导致 left join 上的 `sort` 算子 panic 的问题 [#15739](https://github.com/pingcap/tidb/pull/15739)
    - 修复监控 session 重试错误计数不准确的问题 [#16120](https://github.com/pingcap/tidb/pull/16120)
    - 修复在 `ALLOW_INVALID_DATES` 模式下，`weekday` 结果出错的问题 [#16171](https://github.com/pingcap/tidb/pull/16171)
    - 修复在集群中存在 TiFlash 节点时，GC 可能不能正常工作的问题 [#15761](https://github.com/pingcap/tidb/pull/15761)
    - 修复创建 hash 分区表时指定非常大的分区数量导致 TiDB OOM 的问题 [#16219](https://github.com/pingcap/tidb/pull/16219)
    - 让 `union` 语句的行为和 `select` 语句保持相同，修复把 warnings 当 error 的问题 [#16138](https://github.com/pingcap/tidb/pull/16138)
    - 修复 `TopN` 下推到 mocktikv 中的执行错误 [#16200](https://github.com/pingcap/tidb/pull/16200)
    - 增大 `chunk.column.nullBitMap` 的初始化长度，以避免多余的 `runtime.growslice` 开销 [#16142](https://github.com/pingcap/tidb/pull/16142)

+ TiKV

    - 修复 replica read 导致 TiKV panic 的问题 [#7418](https://github.com/tikv/tikv/pull/7418) [#7369](https://github.com/tikv/tikv/pull/7369)
    - 修复 restore 产生许多空 Region 的问题 [#7419](https://github.com/tikv/tikv/pull/7419)
    - 修复重复的 resolve lock 请求可能会破坏悲观事务原子性的问题 [#7389](https://github.com/tikv/tikv/pull/7389)

+ TiFlash

    - 修复从 TiDB 同步 schema 时，进行 `rename table` 时潜在的问题
    - 修复多数据路径配置下进行 `rename table` 会导致数据丢失的问题
    - 修复某些场景下 TiFlash 存储空间上报错误的问题
    - 修复开启 Region Merge 情况下从 TiFlash 读取时潜在的问题

+ Tools

    - TiDB Binlog

        * 修复因为 TiFlash 相关的 DDL job 导致 Drainer 同步中断的问题 [#948](https://github.com/pingcap/tidb-binlog/pull/948) [#942](https://github.com/pingcap/tidb-binlog/pull/942)

    - BR
    
        * 修复关闭 checksum 情况下，仍然执行 checksum 的问题 [#223](https://github.com/pingcap/br/pull/223)
        * 修复 TiDB 开启 auto-random 或 alter-pk 时，增量备份失败的问题 [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)
