---
title: TiDB 4.0.3 Release Notes
---

# TiDB 4.0.3 Release Notes

发版日期：2020 年 7 月 24 日

TiDB 版本：4.0.3

## 新功能

+ TiDB Dashboard

    - 显示详细的 TiDB Dashboard 版本信息 [#679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    - 显示不受支持的浏览器或过时的浏览器的兼容性通知 [#654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    - 支持在 **SQL 语句**分析页面搜索 [#658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)

+ TiFlash

    - TiFlash proxy 支持文件加密功能

+ Tools

    + Backup & Restore (BR)

        - 支持使用 zstd、lz4、snappy 算法压缩备份文件 [#404](https://github.com/pingcap/br/pull/404)

    + TiCDC

        - 支持 sink-uri 中配置 Kafka 客户端的 ID [#706](https://github.com/pingcap/ticdc/pull/706)
        - 支持离线更新同步任务的配置 [#699](https://github.com/pingcap/ticdc/pull/699)
        - 支持自定义同步任务的 ID [#727](https://github.com/pingcap/ticdc/pull/727)
        - 支持使用 SSL 加密链接向 MySQL 输出数据 [#347](https://github.com/pingcap/ticdc/pull/347)
        - 支持输出 Avro 格式的变更数据 [#753](https://github.com/pingcap/ticdc/pull/753)
        - 支持向 Apache Pulsar 输出变更数据 [#751](https://github.com/pingcap/ticdc/pull/751)

    + Dumpling

        - 支持自定义 CSV 文件的分隔符和换行符 [#116](https://github.com/pingcap/dumpling/pull/116)
        - 支持自定义输出文件名格式 [#122](https://github.com/pingcap/dumpling/pull/122)

## 改进提升

+ TiDB

    - 增加全局变量 `tidb_log_desensitization` 来控制在日志中记录 SQL 时是否脱敏 [#18581](https://github.com/pingcap/tidb/pull/18581)
    - 默认打开 `tidb_allow_batch_cop` [#18552](https://github.com/pingcap/tidb/pull/18552)
    - 加速 `kill tidb sesesion_id` 的执行速度 [#18505](https://github.com/pingcap/tidb/pull/18505)
    - 函数 `tidb_decode_plan` 的结果增加表头输出 [#18501](https://github.com/pingcap/tidb/pull/18501)
    - 配置检查器可以兼容旧版本的配置文件 [#18046](https://github.com/pingcap/tidb/pull/18046)
    - 默认打开执行信息的收集 [#18518](https://github.com/pingcap/tidb/pull/18518)
    - 增加系统表 `tiflash_tables` 和 `tiflash_segments` [#18536](https://github.com/pingcap/tidb/pull/18536)
    - `AUTO RANDOM` 被移出实验特性并正式 GA，有如下的改进和兼容性修改：
        - 在配置文件中，将 `experimental.allow-auto-random` 废弃，该无论该选项如何配置，都可以在列上定义 `AUTO_RANDOM` 属性 [#18613](https://github.com/pingcap/tidb/pull/18613) [#18623](https://github.com/pingcap/tidb/pull/18623)
        - 为避免显式写入 `AUTO_RANDOM` 列造成非预期的 `AUTO_RANDOM_BASE` 的更新，新增 session 变量 `tidb_allow_auto_random_explicit_insert` 用于控制 `AUTO_RANDOM` 列的显式写入，该变量默认值为 `false` [#18508](https://github.com/pingcap/tidb/pull/18508)
        - 为避免分配空间被快速消耗，`AUTO_RANDOM` 列现在仅允许在 `BIGINT` 和 `UNSIGNED BIGINT` 列上定义，并将最大的 Shard Bit 数量限制为 `15` [#18538](https://github.com/pingcap/tidb/pull/18538)
        - 当在 `BIGINT` 列上定义 `AUTO_RANDOM` 属性，并显示插入负值的整型主键时，将不会再触发 `AUTO_RANDOM_BASE` 的更新 [#17987](https://github.com/pingcap/tidb/pull/17987)
        - 当在 `UNSIGNED BIGINT` 列上定义 `AUTO_RANDOM` 属性，分配 ID 时将利用整数的最高位以获得更大的分配空间 [#18404](https://github.com/pingcap/tidb/pull/18404)
        - 在 `SHOW CREATE TABLE` 的结果中支持 `AUTO_RANDOM_BASE` 属性的更新 [#18316](https://github.com/pingcap/tidb/pull/18316)

+ TiKV

    - 添加了新的配置项 `backup.num-threads` 用语控制 backup 线程池的大小 [#8199](https://github.com/tikv/tikv/pull/8199)
    - 收取 snapshot 时不再发送 store heartbeat [#8136](https://github.com/tikv/tikv/pull/8136)
    - 支持动态调整 `shared block cache` 的大小 [#8232](https://github.com/tikv/tikv/pull/8232)

+ PD

    - 支持 JSON 格式日志 [#2565](https://github.com/pingcap/pd/pull/2565)

+ TiDB Dashboard

    - 优化 key Visualizer 中冷表的 bucket 合并 [#674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)
    - 重命名配置项 `disable-telemetry` 以使遥测更一致 [#684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    - 切换页面时显示进度条 [#661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    - 保证慢日志查询和日志查询行为的一致性，即使在空格存在的情况 [#682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

+ TiFlash

    - 将 Grafana **DDL Jobs** 面板中的单位修改为 `operations per minute`
    - 在 Grafana 中新增关于 **TiFlash-Proxy** 的详细监控指标面板
    - 降低 TiFlash Proxy 的 IOPS

+ Tools

    + TiCDC

        - 将监控指标总的表 ID 替换为表名 [#695](https://github.com/pingcap/ticdc/pull/695)

    + Backup & Restore (BR)

        - 支持输出 JSON 格式的日志 [#336](https://github.com/pingcap/br/issues/336)
        - 支持在运行 BR 期间动态开启 pprof [#372](https://github.com/pingcap/br/pull/372)
        - 加速恢复时 DDL 的执行速度 [#377](https://github.com/pingcap/br/pull/377)

    + TiDB Lightning

        - 使用一种更加简单易懂的表过滤机制替换原先的黑白名单机制 [#332](https://github.com/pingcap/tidb-lightning/pull/332)

## Bug 修复

+ TiDB

    - 当 `IndexHashJoin` 遇到执行中发生非内存相关的错误时，返回错误而不是空结果集 [#18586](https://github.com/pingcap/tidb/pull/18586)
    - 修复 gRPC transportReader 导致的反复异常 [#18562](https://github.com/pingcap/tidb/pull/18562)
    - 修复因为 Green GC 不会扫描已下线 store 上的锁而可能导致数据不完整的问题 [#18550](https://github.com/pingcap/tidb/pull/18550)
    - 非只读语句不会使用 TiFlash 引擎 [#18534](https://github.com/pingcap/tidb/pull/18534)
    - 当查询连接异常时返回真实的错误信息 [#18500](https://github.com/pingcap/tidb/pull/18500)
    - 修复非 repair mode 的 TiDB 节点不会重新读取修复的表元信息的错误 [#18323](https://github.com/pingcap/tidb/pull/18323)
    - 修复当锁住的 primary key 在当前事务被插入/删除时可能造成的结果不一致问题 [#18291](https://github.com/pingcap/tidb/pull/18291)
    - 修复数据落盘为正确生效导致的内存溢出 [#18288](https://github.com/pingcap/tidb/pull/18288)
    - 修复 `REPLACE INTO` 语句作用在包含生成列的表时会错误报错的问题 [#17907](https://github.com/pingcap/tidb/pull/17907)
    - 当 `IndexHashJoin` 及 `IndexMergeJoin` 执行异常时抛出 `Out Of Memory Quota!` 错误 [#18527](https://github.com/pingcap/tidb/pull/18527)
    - 修复当 `Index Join` 使用的索引包含整型主键时，特殊情况下执行结果可能出错的问题 [#18565](https://github.com/pingcap/tidb/pull/18565)
    - 修复当开启 new collation 时，若在事务内的更新涉及了 new collation 列，并在该事务内通过唯一索引读取更新数据时，被更新的数据无法被读取到的问题 [#18703](https://github.com/pingcap/tidb/pull/18703)

+ TiKV

    - 修复 merge 期间可能读到过期数据的问题 [#8113](https://github.com/tikv/tikv/pull/8113)
    - 修复聚合函数 `min`/`max` 下推到 TiKV 时，collation 不能正确工作的问题 [#8108](https://github.com/tikv/tikv/pull/8108)

+ PD

    - 修复如果服务器崩溃，创建 TSO 流可能会被阻塞一段时间的问题 [#2648](https://github.com/pingcap/pd/pull/2648)
    - 修复 `getSchedulers` 可能导致数据争用的问题 [#2638](https://github.com/pingcap/pd/pull/2638)
    - 修复删除 `scheduler` 时导致死锁的问题 [#2637](https://github.com/pingcap/pd/pull/2637)
    - 修复 `balance-leader-scheduler` 没有考虑 placement rule 的问题 [#2636](https://github.com/pingcap/pd/pull/2636)
    - 修复有时无法正确设置 `safepoint` 的问题，这可能会使 BR 和 dumpling 失败 [#2635](https://github.com/pingcap/pd/pull/2635)
    - 修复 `hot region scheduler` 中目标 store 选择错误的问题 [#2627](https://github.com/pingcap/pd/pull/2627)
    - 修复 PD Leader 切换时 TSO 请求可能花费太长时间的问题 [#2622](https://github.com/pingcap/pd/pull/2622)
    - 修复 PD Leader 切换后过期 `scheduler` 的问题 [#2608](https://github.com/pingcap/pd/pull/2608)
    - 修复了启用 placement rule 时，有时 Region 的副本可能无法调整到最佳位置的问题 [#2605](https://github.com/pingcap/pd/pull/2605)
    - 修复了存储的部署路径不会随着部署目录移动而更新的问题 [#2600](https://github.com/pingcap/pd/pull/2600)
    - 修复了 `store limit` 可能为零的问题 [#2588](https://github.com/pingcap/pd/pull/2588)

+ TiDB Dashboard

    - 修复 TiDB 扩容时的 TiDB 连接错误 [#689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    - 修复 TiFlash 实例未显示在日志搜索页面的问题 [#680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)
    - 修复概况页面刷新之后 metrics 会重置的问题 [#663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)
    - 修复某些 TLS 方案中的连接问题 [#660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    - 修复在某些情况下无法正确显示语言的下拉列表 [#677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

+ TiFlash

    - 修复更改主键列名后 TiFlash 崩溃的问题
    - 修复 Learner Read 与 Remove Region 并发时可能的死锁问题

+ Tools

    + TiCDC

        - 解决了某些场景下可能发生的 OOM 问题 [#704](https://github.com/pingcap/ticdc/pull/704)
        - 解决了某些特殊表名可能导致 SQL 语法出错的问题 [#676](https://github.com/pingcap/ticdc/pull/676)
        - 解决了同步任务处理单元无法正常退出的问题 [#693](https://github.com/pingcap/ticdc/pull/693)

    + Backup & Restore (BR)

        - 解决了备份汇总报告中时间为负数的问题 [#405](https://github.com/pingcap/br/pull/405)

    + Dumpling

        - 解决了 `NULL` 值在有 `--r` 参数时被忽略的问题 [#119](https://github.com/pingcap/dumpling/pull/119)
        - 解决了导出数据时 flush table 没有正常工作的问题 [#117](https://github.com/pingcap/dumpling/pull/117)

    + TiDB Lightning

        - 解决了 `--log-file` 参数不生效的问题 [#345](https://github.com/pingcap/tidb-lightning/pull/345)

    + TiDB Binlog

        - 修复开启 TLS 写下游时用来保存 checkpoint 的 DB 没有开启 TLS 导致 Drainer 无法启动的问题 [#988](https://github.com/pingcap/tidb-binlog/pull/988)
