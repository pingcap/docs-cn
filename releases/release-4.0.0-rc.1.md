---
title: TiDB 4.0 RC.1 Release Notes
---

# TiDB 4.0 RC.1 Release Notes

发版日期：2020 年 4 月 28 日

TiDB 版本：4.0.0-rc.1

## 兼容性变化

+ TiKV

    - 默认关闭 hibernate region [#7618](https://github.com/tikv/tikv/pull/7618)

+ TiDB Binlog

    - Drainer 增加对 Sequence DDL 的支持 [#950](https://github.com/pingcap/tidb-binlog/pull/950)

## 重点修复的 Bug

+ TiDB

    - 修复由于未检查 `MemBuffer`，事务内执行 `INSERT ... ON DUPLICATE KEY UPDATE` 语句插入多行重复数据可能出错的问题 [#16689](https://github.com/pingcap/tidb/pull/16689)
    - 修复 lock 多行重复 keys 时导致数据索引不一致的问题 [#16769](https://github.com/pingcap/tidb/pull/16769)
    - 修复回收空闲 gRPC 连接导致 TiDB panic 的问题 [#16303](https://github.com/pingcap/tidb/pull/16303)

+ TiKV

    - 修复 TiDB 探活请求触发的死锁问题 [#7540](https://github.com/tikv/tikv/pull/7540)
    - 修复事务的 min commit ts 可能溢出、影响数据正确性的问题 [#7642](https://github.com/tikv/tikv/pull/7642)

+ TiFlash

    - 修正多数据路径配置下进行 rename table 会导致数据丢失的问题
    - 修正当 Region 处于 merge 状态时读取产生的数据错误
    - 修正当 Region 处于非 normal 状态时读取产生的数据错误
    - 修正 TiFlash 中表名的映射方式以正确支持 `recover table`/`flashback table`
    - 修正数据存储路径以解决 `rename table` 时潜在的数据丢失问题
    - 修正 Super batch 开启后，有一定概率 TiDB panic 的问题
    - 修正在线更新时的读模型以优化读性能

+ TiCDC

    - 修复 TiCDC 内部维护的 schema 信息对于读写操作时序问题没有正确处理导致同步失败问题 [#438](https://github.com/pingcap/ticdc/pull/438) [#450](https://github.com/pingcap/ticdc/pull/450) [#478](https://github.com/pingcap/ticdc/pull/478) [#496](https://github.com/pingcap/ticdc/pull/496)
    - 修复 TiKV client 遇到部分 TiKV 异常没有正确维护内部资源的 bug [#499](https://github.com/pingcap/ticdc/pull/499) [#492](https://github.com/pingcap/ticdc/pull/492)
    - 修复节点异常残留元数据信息没有正确清理的 bug [#488](https://github.com/pingcap/ticdc/pull/488) [#504](https://github.com/pingcap/ticdc/pull/504)
    - 修复 TiKV client 没有正确处理 prewrite 重复发送的问题 [#446](https://github.com/pingcap/ticdc/pull/446)
    - 修复 TiKV client 没有正确处理在初始化前接收到冗余 prewrite 的问题 [#448](https://github.com/pingcap/ticdc/pull/448)

+ Backup & Restore (BR)

    - 修复关闭 checksum 情况下，仍然执行 checksum 的问题 [#223](https://github.com/pingcap/br/pull/223)
    - 修复 TiDB 开启 auto-random 或 alter-pk 时，增量备份失败的问题 [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)

## 新功能

+ TiDB

    - 支持发送 `batch coprocessor` 请求给 TiFlash [#16226](https://github.com/pingcap/tidb/pull/16226)
    - 默认打开 Coprocessor cache [#16710](https://github.com/pingcap/tidb/pull/16710)
    - 在 SQL 语句的特殊注释中，只有被注册了语句片段才能被 parser 正常解析，否则将被忽略 [#16157](https://github.com/pingcap/tidb/pull/16157)
    - 支持使用 `SHOW CONFIG` 语法显示 PD 和 TiKV 的配置 [#16475](https://github.com/pingcap/tidb/pull/16475)

+ TiKV

    - 支持在备份到 S3 时使用用户提供的 KMS key 进行服务端加密 [#7630](https://github.com/tikv/tikv/pull/7630)
    - 支持基于负载的 Region split [#7623](https://github.com/tikv/tikv/pull/7623)
    - 支持 common name 验证 [#7468](https://github.com/tikv/tikv/pull/7468)
    - 通过检查文件锁避免多个 TiKV 实例绑定相同的地址 [#7447](https://github.com/tikv/tikv/pull/7447)
    - Encryption at rest 支持 AWS KMS [#7465](https://github.com/tikv/tikv/pull/7465)

+ Placement Driver (PD)

    - 移除 `config manager` 以使其它组件自行控制它们的配置 [#2349](https://github.com/pingcap/pd/pull/2349)

+ TiFlash

    - 添加 DeltaTree 引擎读写负载相关 metrics 上报
    - 缓存 `handle` 列和 `version` 列减小单次读请求的磁盘 I/O
    - 增加了 TiFlash 对于 `FromUnixTime` 和 `Date_format` 函数的支持
    - 根据第一块盘估算全局状态并上报
    - Grafana 添加 DeltaTree 引擎读写负载相关图表
    - 优化 TiFlash chunk encode decimal 的数据
    - 实现了 Diagnostics（SQL 诊断）的 gRPC API，以支持 `INFORMATION_SCHEMA.CLUSTER_INFO` 等系统表的查询

+ TiCDC

    - 在 Kafka sink 模块提供发送批量消息支持 [#426](https://github.com/pingcap/ticdc/pull/426)
    - 支持在 processor 内使用文件排序 [#477](https://github.com/pingcap/ticdc/pull/477)
    - 增加自动 resolve lock 的支持 [#459](https://github.com/pingcap/ticdc/pull/459)
    - 增加自动向 PD 设置 TiCDC 服务级别 safepoint 的功能 [#487](https://github.com/pingcap/ticdc/pull/487)
    - 增加数据同步时的时区配置 [#498](https://github.com/pingcap/ticdc/pull/498)

+ Backup & Restore (BR)

    - 支持在存储的 URL 中配置 S3/GCS [#246](https://github.com/pingcap/br/pull/246)

## Bug 修复

+ TiDB

    - 修复系统表由于 unsigned 列定义导致无法正确显示负数的问题 [#16004](https://github.com/pingcap/tidb/pull/16004)
    - 当使用 `use_index_merge` hint 包含不存在的索引时添加警告 [#15960](https://github.com/pingcap/tidb/pull/15960)
    - 禁止多个 TiDB server 共享同一个临时目录 [#16026](https://github.com/pingcap/tidb/pull/16026)
    - 修复打开 plan cache 时，执行 `explain for connection` 语句 panic 的问题 [#16285](https://github.com/pingcap/tidb/pull/16285)
    - 修复显示 `tidb_capture_plan_baselines` 系统变量不正确的问题 [#16048](https://github.com/pingcap/tidb/pull/16048)
    - 修复 `prepare` 语句中的 `group by` 语句解析错误的问题 [#16377](https://github.com/pingcap/tidb/pull/16377)
    - 修复 `analyze primary key` 可能 panic 的问题 [#16081](https://github.com/pingcap/tidb/pull/16081)
    - 修复 `cluster_info` 系统表中 TiFlash 节点信息错误的问题 [#16024](https://github.com/pingcap/tidb/pull/16024)
    - 修复 index merge 可能 panic 的问题 [#16360](https://github.com/pingcap/tidb/pull/16360)
    - 修复 index merge 遇到 generated column 时导致结果错误的问题 [#16359](https://github.com/pingcap/tidb/pull/16359)
    - 修复 `show create table` 语句显示 sequence 默认值错误的问题 [#16526](https://github.com/pingcap/tidb/pull/16526)
    - 修复主键使用 sequence 作为默认值时出现 `not-null` 的错误的问题 [#16510](https://github.com/pingcap/tidb/pull/16510)
    - 修复当 TiKV 持续返回 `StaleCommand` 期间执行 SQL 卡住不报错的问题 [#16530](https://github.com/pingcap/tidb/pull/16530)
    - 修复 `CREATE DATABASE` 时仅指定 `COLLATE` 时会报错的问题，同时在 `SHOW CREATE DATABASE` 结果中添加缺失的 `COLLATE` 部分 [#16540](https://github.com/pingcap/tidb/pull/16540)
    - 修复打开 plan-cache 时，分区裁剪失败的问题 [#16723](https://github.com/pingcap/tidb/pull/16723)
    - 修复点查在 handle 溢出时返回错误结果的问题 [#16755](https://github.com/pingcap/tidb/pull/16755)
    - 修复等值时间查询 `slow_query` 系统表返回错误结果的问题 [#16806](https://github.com/pingcap/tidb/pull/16806)

+ TiKV

    - 解决 OpenSSL 的安全性问题：CVE-2020-1967 [#7622](https://github.com/tikv/tikv/pull/7622)
    - 避免将 BatchRollback 产生的 rollback 记录标为保护的记录以改善冲突较多场景下的性能 [#7604](https://github.com/tikv/tikv/pull/7604)
    - 修复锁竞争严重的场景下，不必要地唤醒事务导致多余的重试和性能下降的问题 [#7551](https://github.com/tikv/tikv/pull/7551)
    - 修复多次 merge 时，Region 可能卡住的问题 [#7518](https://github.com/tikv/tikv/pull/7518)
    - 修复删除 learner 时，learner 可能并未被删除的问题 [#7518](https://github.com/tikv/tikv/pull/7518)
    - 修复 follower read 可能使 raft-rs panic 的问题 [#7408](https://github.com/tikv/tikv/pull/7408)
    - 修复 SQL 可能因 "group by constant" 错误失败的问题 [#7383](https://github.com/tikv/tikv/pull/7383)
    - 修复当一个乐观锁对应的 primary lock 是悲观锁时，该乐观锁可能阻塞读的问题 [#7328](https://github.com/tikv/tikv/pull/7328)

+ Placement Driver (PD)

    - 修复部分 API TLS 认证失败的问题 [#2363](https://github.com/pingcap/pd/pull/2363)
    - 修复 `config` API 不能识别带有前缀的配置项的问题 [#2354](https://github.com/pingcap/pd/pull/2354)
    - 修复找不到 scheduler 时会返回 500 错误的问题 [#2328](https://github.com/pingcap/pd/pull/2328)
    - 修复 `scheduler config balance-hot-region-scheduler list` 命令返回 404 错误的问题 [#2321](https://github.com/pingcap/pd/pull/2321)

+ TiFlash

    - 禁用存储引擎的粗糙索引优化
    - 修正对 Region 进行 resolve lock 时遇到需要跳过的 lock 抛异常的问题
    - 修正 Coprocessor 统计信息收集的 NPE
    - 修正 Region meta 的检查以保证 Region Split/Region Merge 流程的正确性
    - 修正对 Coprocessor response 大小未做估算导致的消息大小超过 gRPC 限制的问题
    - 修正 TiFlash 对 `AdminCmdType::Split` 命令的处理
