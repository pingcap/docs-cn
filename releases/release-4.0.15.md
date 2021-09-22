---
title: TiDB 4.0.15 Release Notes
---

# TiDB 4.0.15 Release Notes

发版日期：2021 年 9 月 27 日

TiDB 版本：4.0.15

## 兼容性更改

+ TiDB

    - 修复在新会话中执行 `SHOW VARIABLES` 速度较慢的问题。该修复回退了 [#21045](https://github.com/pingcap/tidb/pull/21045) 中的部分更改，可能会引起兼容性问题。[#24326](https://github.com/pingcap/tidb/issues/24326)

## 功能增强

+ TiKV

    - 支持动态修改 TiCDC 配置 [#10645](https://github.com/tikv/tikv/issues/10645)

## 提升改进

+ TiDB

    - 基于直方图的 row count 来触发 auto-analyze [#26706](https://github.com/pingcap/tidb/pull/26706)

+ TiKV

    - 分离处理读写的 ready 状态以减少读延迟 [#10475](https://github.com/tikv/tikv/issues/10475)
    - TiKV Coprocessor 慢日志只考虑处理请求所花费的时间 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 当 slogger 线程过载且队列已满时，删除日志而不是阻塞线程 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 减少 Resolved TS 消息的大小以节省网络带宽 [#2448](https://github.com/pingcap/ticdc/issues/2448)

+ PD

    - 提升了 PD 之间同步 Region 信息的性能 [#3932](https://github.com/tikv/pd/pull/3932)

+ Tools

    + Backup & Restore (BR)

        - 并发执行分裂和打散 Region 的操作，提升恢复速度 [#1429](https://github.com/pingcap/br/pull/1429)
        - 遇到 PD 请求错误或 TiKV IO 超时错误时进行重试 [#1433](https://github.com/pingcap/br/pull/1433)
        - 进行大量小表时减少空 region 的产生，避免影响恢复后的集群运行 [#1374](https://github.com/pingcap/br/issues/1374) [#1432](https://github.com/pingcap/br/pull/1432)
        - 创建表的时候自动执行 `Rebase auto id` 操作，，省去了单独执行 `Rebase auto id` DDL，加快恢复速度 [#1424](https://github.com/pingcap/br/pull/1424)

    + Dumpling

        - 获取要导出的表之前过滤掉不需要导出的 database，提升过滤效率 [#337](https://github.com/pingcap/dumpling/pull/337)
        - 因为 "show table status" 在某些 mysql 版本中运行存在问题，使用 "show full tables " 来获取需要导出的 tables [#332](https://github.com/pingcap/dumpling/pull/332)
        - 支持从不支持 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 或 `SHOW CREATE TABLE` 的 MySQL 协议数据库据库导出数据 [#329](https://github.com/pingcap/dumpling/pull/329)
        - 完善 Dumpling 的警告日志，避免误解出现导出失败 [#340](https://github.com/pingcap/dumpling/pull/340)

    + TiDB Lightning

        - 支持导入数据到带有表达式索引或基于 `virtual generated column` 的索引的表中 [#1418](https://github.com/pingcap/br/pull/1418)

    + TiCDC

        - 解决了 `new collation` 和 TiCDC 的兼容性问题 [#2304](https://github.com/pingcap/ticdc/pull/2304)
        - 减少 region 在 TiKV 节点上发生转移情况的 goroutines 数量 [#2376](https://github.com/pingcap/ticdc/pull/2376)
        - 优化高并发情况的 workerpool 机制 [#2486](https://github.com/pingcap/ticdc/pull/2486)
        - DDL 执行异步化，不阻塞其他 changefeed 的运行 [#2471](https://github.com/pingcap/ticdc/pull/2471)
        - 添加一个全局 gRPC 连接池，让 `kv client` 能够共享 gRPC 连接 [#2531](https://github.com/pingcap/ticdc/pull/2531)
        - 遇到无法恢复的 DML 错误立即退出，不进行重试 [2315](https://github.com/pingcap/ticdc/pull/2315)
        - 优化 unified sorter 对内存的使用 [#2710](https://github.com/pingcap/ticdc/pull/2710)
        - 增加 DDL 执行的 Prometheus 监控指标 [#2681](https://github.com/pingcap/ticdc/pull/2681)
        - 禁止使用不同 `Major` 或 `Minor` 版本 `cdccli` 操作 `TiCDC` [#2601](https://github.com/pingcap/ticdc/pull/2601)
        - 删除被 `unify sort` 取代的 `file sorter`[#2325](https://github.com/pingcap/ticdc/pull/2325)
        - 清理被删的 changefeed 和退出的处理节点的监控数据 [#2313](https://github.com/pingcap/ticdc/pull/2313)
        - 优化 region 初始化时的 `resolve lock` 算法 [#2264](https://github.com/pingcap/ticdc/pull/2264)

## Bug 修复

+ TiDB

    - 修复 binary literal 构造 range 时的 bug 。[26455](https://github.com/pingcap/tidb/pull/26455)
    - 修复当查询包含 group by 和 union 时报错 "index out of range" 的问题。[26553](https://github.com/pingcap/tidb/pull/26553)
    - 修复有 tombstone 存储时请求发送失败的问题.[25849](https://github.com/pingcap/tidb/pull/25849)
    - 修复 case when 表达式字符集相关问题。[26671](https://github.com/pingcap/tidb/pull/26671)
    - 修复将非法字符串转为 date 类型时的非预期行为。[27935](https://github.com/pingcap/tidb/pull/27935)
    - 修复将 Apply 算子转为 Join 时漏掉 column 信息的问题。[27282](https://github.com/pingcap/tidb/pull/27282)
    - 修复 new collation 打开时 count distinct 结果错误问题。[27830](https://github.com/pingcap/tidb/pull/27830)
    - 修复 extract 表达式参数为负的 Duration 时结果错误问题。[27369](https://github.com/pingcap/tidb/pull/27369)
    - group_concat 聚合函数增加对 collation 信息的处理。[27835](https://github.com/pingcap/tidb/pull/27835)
    - 修复 between 表达式类型推导时 collation 错误问题。[27851](https://github.com/pingcap/tidb/pull/27851)
    - 修复 greatest(datetime) 表达式 union null 结果错误问题。[26564](https://github.com/pingcap/tidb/pull/26564)
    - 修复聚合函数 having 条件被错误地下推的问题。[27741](https://github.com/pingcap/tidb/pull/27741)

+ TiKV

    - 修复恢复时启用TDE时br报告文件已存在错误的问题。 [#10917](https://github.com/tikv/tikv/pull/10917)
    - RaftStore Snapshot GC 修复：修复 1 个快照文件 GC 失败时，快照 GC 漏掉 GC 快照文件的问题。[#10871](https://github.com/tikv/tikv/pull/10871)
    - 修复删除陈旧区域过于频繁的问题。[#10781](https://github.com/tikv/tikv/pull/10781)
    - 修复频繁重新连接 pd 客户端。 [#9818](https://github.com/tikv/tikv/pull/9818)
    - 从加密文件字典中检查陈旧的文件信息。  [#10598](https://github.com/tikv/tikv/pull/10598)

+ PD

    - 修复 PD 不能及时修复 down-peer 的问题 [#4081](https://github.com/tikv/pd/pull/4081)
    - 修复扩容 TiKV 时 PD 可能会 panic 的问题 [#3909](https://github.com/tikv/pd/pull/3909)

+ TiFlash

    - 修复多盘部署时数据不一致的潜在问题
    - 修复当查询过滤条件包含诸如 `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN` 时出现错误结果的问题
    - 修复写压力重时 metrics 中 store size 不准确的问题
    - 修复 TiFlash 多盘部署时无法恢复数据的潜在问题
    - 修复 TiFlash 长时间运行后无法回收 delta 历史数据的潜在问题

+ Tools

    + Backup & Restore (BR)

        - 修复了备份和恢复中平均速度计算不准确的问题 [#1410](https://github.com/pingcap/br/pull/1410)

    + TiCDC

        - 修正 owner 可能会遇到 `ErrSchemaStorageTableMiss` ，并意外地重置了 changefeed 的问题 [#2457](https://github.com/pingcap/ticdc/pull/2457)
        - 修正如果遇到 GcTTL 执行超市后无法删除 changefeed 的问题 [#2455](https://github.com/pingcap/ticdc/pull/2455)
        - 修正下线 TiCDC 节点出现在节点列表查询中的问题 [#2447](https://github.com/pingcap/ticdc/pull/2447)
        - 修复 cdc runtime 死锁问题 [#2017](https://github.com/pingcap/ticdc/pull/2017)
        - 修复表调度导致的出现并发复制的问题，该情况下数据会出现不一致[#2495](https://github.com/pingcap/ticdc/pull/2495)[#2727](https://github.com/pingcap/ticdc/pull/2727)
        - 修复元数据管理出现 EtcdWorker 快照隔离的问题 [#2557](https://github.com/pingcap/ticdc/pull/2557)
        - 修复因为 ddl sink 导致 changefeed 不能被停止的问题 [#2556](https://github.com/pingcap/ticdc/pull/2556)
        - 修复 open protocol 问题 —— 当一个事务中没有任何数据写入时候，TiCDC 产生一个空消息 [#2619](https://github.com/pingcap/ticdc/pull/2619)
        - 修复处理无符号 tinyint 的 panic 问题[#2654](https://github.com/pingcap/ticdc/pull/2654)
        - 修复内存压力大时 gRPC keepalive 错误 [#2718](https://github.com/pingcap/ticdc/pull/2718)
        - 修复 TiCDC 坚挺太多 regions 出现的 OOM 问题 [#2723](https://github.com/pingcap/ticdc/pull/2723)
        - 修复处理 json编码 panic 的问题 [#2781](https://github.com/pingcap/ticdc/pull/2781)
        - 修复了在创建新的 changefeed 时可能发生的内存泄漏 [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - 修复 owner 重新启动时，DDL 处理的 bug [#2609](https://github.com/pingcap/ticdc/pull/2609)
        - 修复在 owner 挂掉的情况下， TiCDC 复制可能丢失 DDL 问题 [#2291](https://github.com/pingcap/ticdc/pull/2291)
        - 修复 runtime panic 问题 [#2298](https://github.com/pingcap/ticdc/pull/2298)
