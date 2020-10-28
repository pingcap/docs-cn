---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 Release Notes

发版日期：2020 年 10 月 29 日

TiDB 版本：4.0.8

## 新功能

+ TiDB

    - 

+ TiFlash

    - 支持 CAST 函数下推

+ Tools

    + TiCDC

        - 支持快照级别一致性复制 [#932](https://github.com/pingcap/ticdc/pull/932)

## 优化提升

+ TiDB

    - 

+ TiKV

    - 添加 **Fast-Tune** 监控页辅助性能诊断 [#8804](https://github.com/tikv/tikv/pull/8804)
    - 添加 `security.redact-info-log` 配置，用于从日志中删除用户数据 [#8746](https://github.com/tikv/tikv/pull/8746)
    - 修改 error code 的 metafile 格式 [#8877](https://github.com/tikv/tikv/pull/8877)
    - 开启动态修改 `pessimistic-txn.pipelined` 配置 [#8853](https://github.com/tikv/tikv/pull/8853)
    - 默认开启 memory profile 功能 [#8801](https://github.com/tikv/tikv/pull/8801)

+ PD

    - 修改 error code meta file 的格式 [#3090](https://github.com/pingcap/pd/pull/3090)
    - 为 operator 日志添加更多有用信息 [#3009](https://github.com/pingcap/pd/pull/3009)

+ TiFlash

    - 添加关于 Raft log 的监控
    - 添加关于 `cop` 任务内存使用的监控
    - 在存在删除数据的情况下使 min-max 索引更加准确
    - 提高小批量数据下的查询性能
    - 添加 `error.toml` 文件以支持标准错误码

+ Tools

    + Backup & Restore (BR)

        - 通过将 split 和 restore 流水线来加速恢复 [#428](https://github.com/pingcap/br/pull/428)
        - 支持手动恢复 PD 的调度器 [#530](https://github.com/pingcap/br/pull/530)
        - 将移除 PD 调度器接口改为暂停调度器 [#551](https://github.com/pingcap/br/pull/551)

    + TiCDC

        - 在 MySQL sink 中定期输出统计信息 [#1023](https://github.com/pingcap/ticdc/pull/1023)

    + Dumpling

        - 支持导出 S3 [#155](https://github.com/pingcap/dumpling/pull/155)
        - 支持导出 View 视图 [#158](https://github.com/pingcap/dumpling/pull/158)
        - 支持导出全是生成列的数据表 [#166](https://github.com/pingcap/dumpling/pull/166)

    + TiDB Lightning

        - 支持多字节的 CSV delimiter 和 separator [#406](https://github.com/pingcap/tidb-lightning/pull/406)
        - 通过禁止一些 PD 调度器加速导入 [#408](https://github.com/pingcap/tidb-lightning/pull/408)
        - 在 v4.0 集群上使用 GC-TTL 接口来防止 checksum 阶段的 GC 报错 [#396](https://github.com/pingcap/tidb-lightning/pull/396)

## Bug 修复

+ TiDB

    - 

+ TiKV

    - 修复加密功能中锁冲突导致 pd-worker 处理心跳慢的问题 [#8869](https://github.com/tikv/tikv/pull/8869)
    - 修复生成 memory profile 的问题 [#8790](https://github.com/tikv/tikv/pull/8790)
    - 修复备份时指定 GCS 储存类别 (storage class) 报错的问题 [#8763](https://github.com/tikv/tikv/pull/8763)
    - 修复了重启或者新切分的 Learner 节点找不到 Leader 的问题 [#8864](https://github.com/tikv/tikv/pull/8864)

+ PD

    - 修复了 TiDB Dashboard 在某些场景下引起 PD panic 的错误 [#3096](https://github.com/pingcap/pd/pull/3096)
    - 修复了某个 PD store 下线超过十分钟后可能引起 PD panic 的错误 [#3069](https://github.com/pingcap/pd/pull/3069)

+ TiFlash

    - 修复了日志信息中时间戳错误的问题
    - 修复了使用多路径部署时错误的容量导致创建 TiFlash 副本失败的问题
    - 修复了 TiFlash 重启后可能提示数据文件损坏的问题
    - 修复了 TiFlash 崩溃后磁盘上可能残留损坏文件的问题
    - 修复了在写流量较小情况下，由于 Raft Learner 协议中的状态不能及时更新而导致 `wait index duration` 变长，造成查询慢的问题
    - 修复了在重放过期 Raft 日志时，proxy 会向 key-value 引擎写入大量 Region state 信息的问题

+ Tools

    + Backup & Restore (BR)

        - 修复 restore 期间可能发生的 `send on closed channel panic` 问题 [#559](https://github.com/pingcap/br/pull/559)

    + TiCDC

        - 修复 owner 因更新 GC safepoint 失败而非预期退出的问题 [#979](https://github.com/pingcap/ticdc/pull/979)
        - 修复非预期的任务信息更新 [#1017](https://github.com/pingcap/ticdc/pull/1017)
        - 修复非预期的空 Maxwell 消息 [#978](https://github.com/pingcap/ticdc/pull/978)

    + TiDB Lightning

        - 修复列信息错误的问题 [#420](https://github.com/pingcap/tidb-lightning/pull/420)
        - 修复 Local 模式下获取 Region 信息出现死循环的问题 [#418](https://github.com/pingcap/tidb-lightning/pull/418)
