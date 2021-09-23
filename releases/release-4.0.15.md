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
        - 遇到 PD 请求错误或 TiKV I/O 超时错误时进行重试 BR 任务 [#1433](https://github.com/pingcap/br/pull/1433)
        - 恢复大量小表时减少空 Region 的产生，避免影响恢复后的集群运行 [#1374](https://github.com/pingcap/br/issues/1374) [#1432](https://github.com/pingcap/br/pull/1432)
        - 创建表的时候自动执行 `rebase auto id` 操作，省去了单独的 `rebase auto id` DDL 操作，加快恢复速度 [#1424](https://github.com/pingcap/br/pull/1424)

    + Dumpling

        - 获取表信息前过滤掉不需要导出的数据库，提升 `SHOW TABLE STATUS` 的过滤效率 [#337](https://github.com/pingcap/dumpling/pull/337)
        - 使用 `SHOW FULL TABLES` 来获取需要导出的表，因为 `SHOW TABLE STATUS` 在某些 MySQL 版本上运行存在问题 [#332](https://github.com/pingcap/dumpling/pull/332)
        - 支持对 MySQL 兼容的特定数据库进行备份，这些数据库不支持 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` 和 `SHOW CREATE TABLE` 语法 [#309](https://github.com/pingcap/dumpling/issues/309)
        - 完善 Dumpling 的警告日志，避免让用户误以为导出失败 [#340](https://github.com/pingcap/dumpling/pull/340)

    + TiDB Lightning

        - 支持导入数据到带有表达式索引或带有基于虚拟生成列的索引的表中 [#1418](https://github.com/pingcap/br/pull/1418)

    + TiCDC

        - TiCDC 总是 TiKV 内部拉取 old value [#2304](https://github.com/pingcap/ticdc/pull/2304)
        - 当某张表的 Region 从某个 TiKV 节点全部迁移走时，减少 goroutine 资源的使用 [#2284](https://github.com/pingcap/ticdc/issues/2284)
        - 在高并发下减少 workerpool 中创建的 goroutine 数量 [#2211](https://github.com/pingcap/ticdc/issues/2211)
        - 异步执行 DDL 语句，不阻塞其他 changefeed [#2471](https://github.com/pingcap/ticdc/pull/2471)
        - 为所有 KV 客户端创建全局共享的 gRPC 连接池 [#2531](https://github.com/pingcap/ticdc/pull/2531)
        - 遇到无法恢复的 DML 错误立即退出，不进行重试 [2315](https://github.com/pingcap/ticdc/pull/2315)
        - 优化 Unified Sorter 使用内存排序时的内存管理 [#2553](https://github.com/pingcap/ticdc/issues/2553)
        - 为 DDL 语句的执行新增 Prometheus 监控指标 [#2681](https://github.com/pingcap/ticdc/pull/2681)
        - 禁止使用不同的 major 和 minor 版本启动 TiCDC 节点 [#2601](https://github.com/pingcap/ticdc/pull/2601)
        - 移除 `file sorter` 文件排序器 [#2325](https://github.com/pingcap/ticdc/pull/2325)
        - 清理被删 changefeed 的监控数据和已退出处理节点的监控数据 [#2313](https://github.com/pingcap/ticdc/pull/2313)
        - 优化 Region 初始化后的清锁算法 [#2264](https://github.com/pingcap/ticdc/pull/2264)

## Bug 修复

+ TiDB

    - 修复构建 range 时未正确给二进制字面值设置排序规则的问题 [#26455](https://github.com/pingcap/tidb/pull/26455)
    - 修复 `case when` 表达式的字符集不正确的问题 [#26671](https://github.com/pingcap/tidb/pull/26671)
    - 修复当查询包含 `GROUP BY` 和 `UNION` 时报错 "index out of range" 的问题 [#26553](https://github.com/pingcap/tidb/pull/26553)
    - 修复当 TiKV 有 tombstone store 时 TiDB 发送请求失败的问题 [#25849](https://github.com/pingcap/tidb/pull/25849)
    - 修复将非法字符串转为 `DATE` 类型时的非预期行为 [#27935](https://github.com/pingcap/tidb/pull/27935)
    - 修复将 `Apply` 算子转为 `Join` 时漏掉列信息的问题 [#27282](https://github.com/pingcap/tidb/pull/27282)
    - 修复开启 New Collation 时多列的 `count distinct` 返回结果错误的问题 [#27830](https://github.com/pingcap/tidb/pull/27830)
    - 修复了 `extract` 函数的参数是负数时查询结果错误的问题 [#27236](https://github.com/pingcap/tidb/issues/27236)
    - 修复了当 `group_concat` 函数包含非 `bin` 的 collation 时查询结果错误的问题 [#27429](https://github.com/pingcap/tidb/issues/27429)
    - 修复了当 `between` 表达式两边的 collation 不一致会导致查询结果错误的问题 [#27146](https://github.com/pingcap/tidb/issues/27146)
    - 修复了 `greatest(datetime) union null` 返回空字符串的问题 [#26532](https://github.com/pingcap/tidb/issues/26532)
    - 修复了 `having` 可能执行错误的问题 [#26496](https://github.com/pingcap/tidb/issues/26496)
    - 移除文档中未记录的 `/debug/sub-optimal-plan` HTTP API [#27264](https://github.com/pingcap/tidb/pull/27264)

+ TiKV

    - 修复数据恢复期间启用 TDE 时 BR 报告文件已存在错误的问题 [#10917](https://github.com/tikv/tikv/pull/10917)
    ?- 修复当有快照文件未被 GC 回收时，快照在 GC 的过程中可能遗留 GC 快照文件的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 修复 TiKV 过于频繁删除陈旧 Region 的问题 [#10781](https://github.com/tikv/tikv/pull/10781)
    - 修复 TiKV 频繁重新连接 PD 客户端的问题 [#9818](https://github.com/tikv/tikv/pull/9818)
    - 从加密文件字典中检查陈旧的文件信息 [#10598](https://github.com/tikv/tikv/pull/10598)

+ PD

    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复了 PD 在扩容 TiKV 时可能会 Panic 的问题 [#3868](https://github.com/tikv/pd/issues/3868)

+ TiFlash

    - 修复多盘部署时数据不一致的潜在问题
    - 修复当查询过滤条件包含诸如 `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN` 时出现错误结果的问题
    - 修复写入压力大时 metrics 中 store size 不准确的问题
    - 修复 TiFlash 多盘部署时无法恢复数据的潜在问题
    - 修复 TiFlash 长时间运行后无法回收 Delta 历史数据的潜在问题

+ Tools

    + Backup & Restore (BR)

        - 修复了备份和恢复中平均速度计算不准确的问题 [#1410](https://github.com/pingcap/br/pull/1410)

    + TiCDC

        - 修复集成测试中遇到的由于 DDL Job 重复导致的 `ErrSchemaStorageTableMiss` 错误 [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - 修复遇到 `ErrGCTTLExceeded` 错误时 changefeed 无法被删除的问题 [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - 修复 `capture list` 命令输出中出现已过期 capture 的问题 [#2388](https://github.com/pingcap/ticdc/issues/2388)
        - 修复 TiCDC processor 出现死锁的问题 [#2017](https://github.com/pingcap/ticdc/pull/2017)
        - 修复重新调度一张表时多个处理器将数据写入同一张表引发的数据不一致的问题 [#2495](https://github.com/pingcap/ticdc/pull/2495) [#2727](https://github.com/pingcap/ticdc/pull/2727)
        - 修复元数据管理出现 `EtcdWorker` 快照隔离被破坏的问题 [#2557](https://github.com/pingcap/ticdc/pull/2557)
        - 修复因为 DDL sink 错误导致 changefeed 不能被停止的问题 [#2556](https://github.com/pingcap/ticdc/pull/2556)
        - 修复 TiCDC Open Protocol 的问题：当一个事务中没有任何数据写入时候，TiCDC 产生一个空消息 [#2619](https://github.com/pingcap/ticdc/pull/2619)
        - 修复 TiCDC 在处理无符号 `TINYINT` 类型时崩溃的问题 [#2648](https://github.com/pingcap/ticdc/issues/2648)
        - 修复内存压力大时 gRPC 连接频繁断开的错误 [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - 修复因 TiCDC capture 过多 Regions 出现的 OOM 问题 [#2723](https://github.com/pingcap/ticdc/pull/2723)
        - 修复将 `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar` 等类型的数据编码为 JSON 时进程崩溃的问题 [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - 修复在创建新的 changefeed 时可能发生的内存泄漏问题 [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - 修复同步任务从一个表结构变更的 finish TS 开始时 DDL 处理失败的问题 [#2603](https://github.com/pingcap/ticdc/issues/2603)
        - 修复 owner 在执行 DDL 语句时崩溃可能导致 DDL 任务丢失的问题 [#1260](https://github.com/pingcap/ticdc/issues/1260)
        - 修复 `SinkManager` 中对 map 的不安全并发访问 [#2298](https://github.com/pingcap/ticdc/pull/2298)
