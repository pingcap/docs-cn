---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 Release Notes

发版日期：2020 年 8 月 31 日

TiDB 版本：4.0.5

## 兼容性变化

+ TiDB

    - 修改 `drop partition` 和 `truncate partition` 的参数 [#18930](https://github.com/pingcap/tidb/pull/18930)
    - 为 `add partition` 操作添加状态检查 [#18865](https://github.com/pingcap/tidb/pull/18865)

## 新功能

+ TiKV

    - 为错误定义错误码 [#8387](https://github.com/tikv/tikv/pull/8387)

+ TiFlash

    - 支持与 TiDB 统一的 log 格式

+ Tools

    - TiCDC

        - 支持加密 Kafka 链接 [#764](https://github.com/pingcap/ticdc/pull/764)
        - 支持输出 old value [#708](https://github.com/pingcap/ticdc/pull/708)
        - 添加列的特征的标识 [#796](https://github.com/pingcap/ticdc/pull/796)
        - 支持输出上一版本的 DDL 和表结构 [#799](https://github.com/pingcap/ticdc/pull/799)

## 优化提升

+ TiDB

    - 优化 `Union` 场景下 `DecodePlan` 的开销 [#18941](https://github.com/pingcap/tidb/pull/18941)
    - 减少 GC 在遇到 `Region cache miss` 错误时扫描锁的次数 [#18876](https://github.com/pingcap/tidb/pull/18876)
    - 减少统计信息 feedback 对集群性能的影响 [#18772](https://github.com/pingcap/tidb/pull/18772)
    - 支持在 RPC 请求返回结果前取消操作 [#18580](https://github.com/pingcap/tidb/pull/18580)
    - 支持使用 HTTP API 生成带有相关监控项名称的 profile [#18531](https://github.com/pingcap/tidb/pull/18531)
    - 支持分区表的预打散功能 [#17863](https://github.com/pingcap/tidb/pull/17863)
    - 在监控面板中显示每个实例的内存使用详情 [#18679](https://github.com/pingcap/tidb/pull/18679)
    - 在 `EXPLAIN` 中显示 `BatchPointGet` 算子的详细运行信息 [#18892](https://github.com/pingcap/tidb/pull/18892)
    - 在 `EXPLAIN` 中显示 `PointGet` 算子的详细运行信息 [#18817](https://github.com/pingcap/tidb/pull/18817)
    - 解决 `MemTracker` 潜在的死锁问题 [#18395](https://github.com/pingcap/tidb/pull/18395)
    - 提高字符串转换为整数类型和小数类型的兼容性，支持将 JSON 转换为时间日期类型 [#18159](https://github.com/pingcap/tidb/pull/18159)
    - 支持限制 `TableReader` 算子内存使用 [#18392](https://github.com/pingcap/tidb/pull/18392)
    - 在 `batch cop` 请求重试时避免多次 backoff [#18999](https://github.com/pingcap/tidb/pull/18999)
    - 提升 `ALTER TABLE` 的兼容性 [#19270](https://github.com/pingcap/tidb/pull/19270)
    - 单个分区支持 `IndexJoin` [#19151](https://github.com/pingcap/tidb/pull/19151)
    - 支持在 log 中存在非法字符时搜索 log [#18579](https://github.com/pingcap/tidb/pull/18579)

+ PD

    - 支持打散特殊存储引擎节点（例如 TiFlash）上的 Region [#2706](https://github.com/tikv/pd/pull/2706)
    - 支持通过 API 指定某范围内的 Region 优先进行调度 [#2687](https://github.com/tikv/pd/pull/2687)
    - 优化 Region 打散操作，使得 Leader 分布更均匀 [#2684](https://github.com/tikv/pd/pull/2684)
    - 针对 TSO 请求添加更多测试和日志 [#2678](https://github.com/tikv/pd/pull/2678)
    - 避免 Region Leader 变化时可能产生的不必要的缓存更新 [#2672](https://github.com/tikv/pd/pull/2672)
    - 增加选项允许 `store.GetLimit` 返回 tombstone 状态的 store [#2743](https://github.com/tikv/pd/pull/2743)
    - 支持 PD Leader 和 Follower 之间同步 Region Leader 变更 [#2795](https://github.com/tikv/pd/pull/2795)
    - 增加查询 GC safepoint 服务的命令 [#2797](https://github.com/tikv/pd/pull/2797)
    - 替换 filter 中的 `region.Clone` 调用，优化性能 [#2801](https://github.com/tikv/pd/pull/2801)
    - 增加关闭 Region 流量统计缓存更新的选项，用于提升大规模集群的性能 [#2848](https://github.com/tikv/pd/pull/2848)

+ TiFlash

    - 添加更多的 Grafana 监控面板，比如 CPU、I/O、RAM 使用量，以及存储引擎的各项指标
    - 通过优化 Raft logs 的处理逻辑，减少 I/O 操作
    - 加快 `add partition` DDL 之后 Region 的调度速度
    - 优化 DeltaTree 引擎中 delta 数据的整理，减少读写放大
    - 通过使用多线程对 Region snapshot 进行预处理，优化从 TiKV 同步 Region 副本的性能
    - 优化系统负载较低时打开文件描述符的数量，降低系统资源占用量
    - 减少 TiFlash 重启时新创建的文件数量
    - 支持数据存储的静态加密功能
    - 支持数据传输的 TLS 功能

+ Tools

    + TiCDC

        - 减少了获取时间戳的频率 [#801](https://github.com/pingcap/ticdc/pull/801)

    + Backup & Restore (BR)

        - 优化了日志 [#428](https://github.com/pingcap/br/pull/428)

    + Dumpling

        - 减少导出 MySQL 时持锁的时间 [#121](https://github.com/pingcap/dumpling/pull/121)

    + TiDB Lightning

        - 优化了日志 [#352](https://github.com/pingcap/tidb-lightning/pull/352)

## Bug 修复

+ TiDB

    - 修复 `builtinCastRealAsDecimalSig` 函数中未正确处理 `ErrTruncate/Overflow` 错误导致报 `should ensure all columns have the same length` 错误的问题 [#18967](https://github.com/pingcap/tidb/pull/18967)
    - 修复 `pre_split_regions` 对分区表不生效的问题 [#18837](https://github.com/pingcap/tidb/pull/18837)
    - 修复大事务提前终止的问题 [#18813](https://github.com/pingcap/tidb/pull/18813)
    - 修复使用 `collation` 相关函数查询结果错误的问题 [#18735](https://github.com/pingcap/tidb/pull/18735)
    - 修复 `getAutoIncrementID()` 函数逻辑错误导致导出工具报 `table not exist` 错误的问题 [#18692](https://github.com/pingcap/tidb/pull/18692)
    - 修复 `select a from t having t.a` 报 `unknown column error` 的问题 [#18434](https://github.com/pingcap/tidb/pull/18434)
    - 修复 Hash 分区表的分区键为整数类型时，写入 64 位无符号类型导致溢出 panic 的问题 [#18186](https://github.com/pingcap/tidb/pull/18186)
    - 修复 `char` 函数行为错误的问题 [#18122](https://github.com/pingcap/tidb/pull/18122)
    - 修复 `ADMIN REPAIR TABLE` 无法解析 range 分区表表达式中整数的问题 [#17988](https://github.com/pingcap/tidb/pull/17988)
    - 修复 `SET CHARSET` 行为不正确的问题 [#17289](https://github.com/pingcap/tidb/pull/17289)
    - 修复由于错误的设置 collation 导致 `collation` 函数返回错误结果的问题 [#17231](https://github.com/pingcap/tidb/pull/17231)
    - 修复 `STR_TO_DATE` 和 MySQL 行为不一致的问题 [#18727](https://github.com/pingcap/tidb/pull/18727)
    - 修复 `cluster_info` 表中，TiDB 版本和 PD/TiKV 不一致的问题 [#18413](https://github.com/pingcap/tidb/pull/18413)
    - 修复悲观事务未能检查出重复数据导致可以重复写入冲突数据的问题 [#19004](https://github.com/pingcap/tidb/pull/19004)
    - 修复 `union select for update` 存在并发竞态的问题 [#19006](https://github.com/pingcap/tidb/pull/19006)
    - 修复自查询含有 `PointGet` 算子时返回结果错误的问题 [#19046](https://github.com/pingcap/tidb/pull/19046)
    - 修复 `IndexLookUp` 作为 `Apply` 的内连接算子时查询结果不正确的问题 [#19496](https://github.com/pingcap/tidb/pull/19496)
    - 修复 `anti-semi-join` 查询结果不正确的问题 [#19472](https://github.com/pingcap/tidb/pull/19472)
    - 修复 `BatchPointGet` 查询结果不正确的问题 [#19456](https://github.com/pingcap/tidb/pull/19456)
    - 修复 `UnionScan` 作为 `Apply` 的内连接算子时查询结果不正确的问题 [#19496](https://github.com/pingcap/tidb/pull/19496)
    - 修复使用 `EXECUTE` 语句产生大查询日志造成 panic 的问题 [#17419](https://github.com/pingcap/tidb/pull/17419)
    - 修复 `IndexJoin` 在使用 `ENUM` 或 `SET` 类型作为连接键报错的问题 [#19235](https://github.com/pingcap/tidb/pull/19235)
    - 修复在索引值为 `NULL` 时无法构建出查询范围的问题 [#19358](https://github.com/pingcap/tidb/pull/19358)
    - 修复更新全局配置导致的数据竞态问题 [#17964](https://github.com/pingcap/tidb/pull/17964)
    - 修复修改 schema 字符集导致 panic 的问题 [#19286](https://github.com/pingcap/tidb/pull/19286)
    - 修复修改文件夹对中间结果落盘功能的影响 [#18970](https://github.com/pingcap/tidb/pull/18970)
    - 修复 `decimal` 类型哈希值不正确的问题 [#19131](https://github.com/pingcap/tidb/pull/19131)
    - 修复 `PointGet` 和 `BatchPointGet` 在分区表场景下报错的问题 [#19141](https://github.com/pingcap/tidb/issues/19141)
    - 修复共同使用 `Apply` 算子和 `UnionScan` 算子时查询结果不正确的问题 [#19104](https://github.com/pingcap/tidb/issues/19104)
    - 修复生成列索引结果不正确的问题 [#17989](https://github.com/pingcap/tidb/issues/17989)
    - 修复并发收集统计信息 panic 的问题 [#18983](https://github.com/pingcap/tidb/pull/18983)

+ TiKV

    - 修复开启 Hibernate Region 时，某些情况下 leader 选举慢的问题 [#8292](https://github.com/tikv/tikv/pull/8292)
    - 修复 Region 调度产生的一个内存泄露问题 [#8357](https://github.com/tikv/tikv/pull/8357)
    - 增加 `hibernate-timeout` 配置避免 leader 过快变为 Hibernate 状态 [#8208](https://github.com/tikv/tikv/pull/8208)

+ PD

    - 修复 PD leader 切换时可能导致一段时间内 TSO 不可用的问题 [#2666](https://github.com/tikv/pd/pull/2666)
    - 修复开启 Placement Rule 时，某些情况下 Region 无法调度至最佳状态的问题 [#2720](https://github.com/tikv/pd/pull/2720)
    - 修复开启 Placement Rules 后，`Balance Leader` 不工作的问题 [#2726](https://github.com/tikv/pd/pull/2726)
    - 修复不健康的 Store 未从负载统计信息中过滤的问题 [#2805](https://github.com/tikv/pd/pull/2805)

+ TiFlash

    - 修复 TiFlash 从旧版本升级到新版本的过程中，由于包含特殊字符而导致进程无法启动的问题
    - 修复 TiFlash 进程在初始化过程中，一旦出现任何异常就无法退出的问题

+ Tools

    + Backup & Restore (BR)
    
        - 修复 total KV 和 total bytes 被计算两次的问题 [#472](https://github.com/pingcap/br/pull/472)
        - 修复切换模式不及时导致恢复缓慢的问题 [#473](https://github.com/pingcap/br/pull/473)

    + Dumpling
        - 修复 FTWRL 锁没有及时释放的问题 [#128](https://github.com/pingcap/dumpling/pull/128)

    + TiCDC

        - 解决了同步任务不能被移除的问题 [#782](https://github.com/pingcap/ticdc/pull/782)
        - 修正了错误的删除事件 [#787](https://github.com/pingcap/ticdc/pull/787)
        - 解决了已停止的同步任务会卡住 GC 的问题 [#797](https://github.com/pingcap/ticdc/pull/797)
        - 解决了网络阻塞导致同步任务不能退出的问题 [#825](https://github.com/pingcap/ticdc/pull/825)
        - 修复在某些情况下无关数据被错误地到下游的问题 [#743](https://github.com/pingcap/ticdc/issues/743)

    + TiDB Lightning

        - 解决了 TiDB backend 遇到空 binary/hex 的时候出现语法错误的问题 [#357](https://github.com/pingcap/tidb-lightning/pull/357)
