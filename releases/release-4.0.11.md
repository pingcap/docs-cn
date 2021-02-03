---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 Release Notes

发版日期：2021 年 2 月 4 日

TiDB 版本：4.0.11

## 兼容性更改

## 新功能

+ TiKV

    - 支持 `utf8mb4_unicode_ci` 函数 [#9577](https://github.com/tikv/tikv/pull/9577)
    - 支持 `cast_year_as_time` 函数 [#9299](https://github.com/tikv/tikv/pull/9299)

+ TiFlash

    - 增加排队处理 Coprocessor 任务的线程池以减小 OOM 几率, 随之增加两项配置项 `cop_pool_size` 与 `batch_cop_pool_size`, 默认为 `物理核数 * 2`. [#1312](https://github.com/pingcap/tics/pull/1312)

## 改进提升

+ TiKV

    - 为 DBasS 添加 server 信息的 metrics  [#9591](https://github.com/tikv/tikv/pull/9591)
    - Grafana dashboards 支持监控多个集群 [#9572](https://github.com/tikv/tikv/pull/9572)
    - 汇报 RocksDB 的 metrics 到 TiDB [#9316](https://github.com/tikv/tikv/pull/9316)
    - 为 coprocessor 任务记录暂停时间 [#9277](https://github.com/tikv/tikv/pull/9277)
    - 为 load-base-split 添加 key 数量和大小的阀值 [#9354](https://github.com/tikv/tikv/pull/9354)
    - 在 import 前检查文件是否存在 [#9544](https://github.com/tikv/tikv/pull/9544)
    - 改进 Fast Tune 面板 [#9180](https://github.com/tikv/tikv/pull/9180)

+ TiFlash

    - 优化 date_format 函数的性能 [#1339](https://github.com/pingcap/tics/pull/1339)
    - 优化处理 ingest SST 时的内存开销

+ Tools

    + TiCDC

        - 在 Capture 元信息添加版本信息和在 Changefeed 元信息中创建该 Changefeed 的 CLI 版本 [#1342](https://github.com/pingcap/ticdc/pull/1342)

    + TiDB Lightning

        * 并行创建数据表以改进导入速度 [#502](https://github.com/pingcap/tidb-lightning/pull/502)
        * 跳过分裂小 region 以改进导入速度 [#524](https://github.com/pingcap/tidb-lightning/pull/524)
        * 添加导入进度条并改进导入进度精度 [#506](https://github.com/pingcap/tidb-lightning/pull/506)

## Bug 修复

+ TiKV

    - 修复当设置 PROST=1 时构建 TiKV 失败的问题 [#9604](https://github.com/tikv/tikv/pull/9604)
    - 修复不匹配的内存诊断信息 [#9589](https://github.com/tikv/tikv/pull/9589)
    - 修复在恢复 rawkv 数据时部分 key range 的 end key 的包含性问题 [#9583](https://github.com/tikv/tikv/pull/9583)
    - 修复当 CDC 增量扫数据时读取一个被回滚的事务的某个 key 的旧值时 TiKV 可能会 panic 的问题 [#9569](https://github.com/tikv/tikv/pull/9569)
    - 修复使用不同配置的连接拉取同一个 region 的变更时旧值配置不匹配的问题 [#9565](https://github.com/tikv/tikv/pull/9565)
    - 修复 TiVK 运行在网络接口缺少 MAC 地址的设备上会崩溃的问题（自 v4.0.9 引入）[#9516](https://github.com/tikv/tikv/pull/9516)
    - 修复 TiKV 在备份大 region 时会 OOM 的问题 [#9448](https://github.com/tikv/tikv/pull/9448)
    - 修复 `region-split-check-diff` 无法配置的问题 [#9530](https://github.com/tikv/tikv/pull/9530)
    - 修复系统时间回退时 TiKV 会 panic 的问题 [#9542](https://github.com/tikv/tikv/pull/9542)

+ TiFlash

    - 修正 decimal 类型计算 `min/max`的结果错误
    - 修正读取数据时有可能导致 crash 的问题 [#1358](https://github.com/pingcap/tics/pull/1358)
    - 修正 DDL 操作后写入的数据可能会在 compaction 后丢失的问题 [#1350](https://github.com/pingcap/tics/pull/1350)

+ Tools

    + TiCDC

        * 修复 TiCDC 服务在同时发生 ErrTaskStatusNotExists 和 Capture 会话关闭的情况下的非预期的退出 [#1240](https://github.com/pingcap/ticdc/pull/1240)
        * 修复不用 Changefeed 之间不同 old-value 设置的互相影响问题 [#1347](https://github.com/pingcap/ticdc/pull/1347)
        * 修复 TiCDC 服务在遇见错误 sort-engine 参数时卡住的问题 [#1309](https://github.com/pingcap/ticdc/pull/1309)
        * 修复在非 Owner 节点上获取 debug 信息退出的问题 [#1349](https://github.com/pingcap/ticdc/pull/1349)
        * 修复 `ticdc_processor_num_of_tables` and `ticdc_processor_table_resolved_ts` 两个监控指标在增删数据表时没有被正确更新的问题 [#1351](https://github.com/pingcap/ticdc/pull/1351)
        * 修复 Processor 在添加同步数据表时退出而造成的潜在的数据丢失问题 [#1363](https://github.com/pingcap/ticdc/pull/1363)
        * 修复 Owner 在数据表迁移期间造成非正常的状态的 TiCDC 服务的退出问题 [#1352](https://github.com/pingcap/ticdc/pull/1352)
        * 修复 TiCDC 服务在丢失 service gc safepoint 是没有及时退出的问题 [#1367](https://github.com/pingcap/ticdc/pull/1367)
        * 修复 kv client 潜在的跳过创建 event feed 的问题 [#1336](https://github.com/pingcap/ticdc/pull/1336)
        * 修复同步事务到下游时事务原子性被破坏的问题 [#1375](https://github.com/pingcap/ticdc/pull/1375)

    + Backup & Restore (BR)

        * 修复恢复备份后可能产生大 region 的问题 [#702](https://github.com/pingcap/br/pull/702)
        * 修复在没有 auto id 的数据表上恢复 auto id 的问题 [#720](https://github.com/pingcap/br/pull/720)

    + TiDB Lightning

        * 修复使用 TiDB backend 时可能触发的 "column count mismatch" 问题 [#535](https://github.com/pingcap/tidb-lightning/pull/535)
        * 修复 TiDB backend 在导入数据源 column 个数和数据表 column 个数不匹配时非预期退出的问题 [#528](https://github.com/pingcap/tidb-lightning/pull/528)
        * 修复导入期间 TiKV 可能发生的非预期退出的问题 [#554](https://github.com/pingcap/tidb-lightning/pull/554)
