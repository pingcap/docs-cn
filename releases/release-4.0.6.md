---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 Release Notes

发版日期：2020 年 9 月 15 日

TiDB 版本：4.0.6

## 新功能

+ TiFlash

    - 在 TiFlash 中支持在广播 Join 中使用外连接

+ TiDB Dashboard

    - 添加 Query 编辑和执行页面 (实验性功能) [#713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    - 添加 Store 地理拓扑显示页面 [#719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    - 添加集群配置调整页面 (实验性功能) [#733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    - 支持共享当前 session [#741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    - 支持显示 SQL 语句分析中执行计划的数量 [#746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)

+ Tools

    + TiCDC（自 v4.0.6 起，TiCDC 成为**正式功能**，可用于生产环境）

        - 支持输出 `maxwell` 格式的数据 [#869](https://github.com/pingcap/ticdc/pull/869)

## 优化提升

+ TiDB

    - 使用标准错误替换 TiDB 中的错误码和错误信息 [#19888](https://github.com/pingcap/tidb/pull/19888)
    - 提升分区表的写性能 [#19649](https://github.com/pingcap/tidb/pull/19649)
    - 在 Cop Runtime 统计信息中记录更多的 RPC Runtime 信息 [#19264](https://github.com/pingcap/tidb/pull/19264)
    - 禁止在 `metrics_schema` 和 `performance_schema` 中创建表 [#19792](https://github.com/pingcap/tidb/pull/19792)
    - 支持调整 Union 执行算子的并发度 [#19886](https://github.com/pingcap/tidb/pull/19886)
    - 支持在广播 Join 中使用外连接 [#19664](https://github.com/pingcap/tidb/pull/19664)
    - 添加对 process list 的 digest [#19829](https://github.com/pingcap/tidb/pull/19829)
    - 对于自动提交语句的重试转换到悲观锁模式 [#19796](https://github.com/pingcap/tidb/pull/19796)
    - 在 `Str_to_date` 函数中支持 `%r` 和 `%T` 的数据格式 [#19693](https://github.com/pingcap/tidb/pull/19693)
    - 使 `SELECT INTO OUTFILE` 需要文件权限 [#19577](https://github.com/pingcap/tidb/pull/19577)
    - 支持 `stddev_pop` 函数 [#19541](https://github.com/pingcap/tidb/pull/19541)
    - 添加 `TiDB-Runtime` 面板 [#19396](https://github.com/pingcap/tidb/pull/19396)
    - 提升 `ALTER TABLE ALGORITHMS` 的兼容性 [#19364](https://github.com/pingcap/tidb/pull/19364)
    - 在慢日志的计划字段中加入编码好的 `INSERT`/`DELETED`/`UPDATE` 计划 [#19269](https://github.com/pingcap/tidb/pull/19269)

+ TiKV

    - 优化 `DropTable`/`TruncateTable` 时导致的性能下降 [#8627](https://github.com/tikv/tikv/pull/8627)
    - 支持生成标准错误码的 meta 文件 [#8619](https://github.com/tikv/tikv/pull/8619)
    - **scan detail** 中增加 tombstone 个数的 metrics [#8618](https://github.com/tikv/tikv/pull/8618)
    - 添加 **rocksdb perf context** 到 Grafana 默认面板 [#8467](https://github.com/tikv/tikv/pull/8467)

+ PD

    - 升级 Dashboard 到 v2020.09.08.1 [#2928](https://github.com/pingcap/pd/pull/2928)
    - 添加更多关于 store 和 Region 心跳的 metrics [#2891](https://github.com/tikv/pd/pull/2891)
    - 回滚空间不足的阈值策略 [#2875](https://github.com/pingcap/pd/pull/2875)
    - 支持标准错误码
        - [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912)
        - [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

+ TiFlash

    - 在 Grafana 中添加关于数据同步 (`apply Region snapshots` 和 `ingest SST files`) 的监控面板
    - 在 Grafana 中添加关于 `write stall` 的监控面板
    - 添加 `dt_segment_force_merge_delta_rows` 及 `dt_segment_force_merge_delta_deletes` 用于调整阈值以避免 `write stall` 发生
    - 支持在 TiFlash-Proxy 中把 `raftstore.snap-handle-pool-size` 设为 `0` 以禁用多线程同步 Region snapshot，可降低同步数据时内存消耗
    - 在 `https_port` 及 `metrics_port` 上支持 CN 检查

+ Tools

    + TiCDC

        - 在初始化阶段跳过 resolved lock [#910](https://github.com/pingcap/ticdc/pull/910)
        - 减少写 PD 的频率 [#937](https://github.com/pingcap/ticdc/pull/937)

    + Backup & Restore (BR)

        - 在 Summary 中添加真实消耗的时间 [#486](https://github.com/pingcap/br/issues/486)

    + Dumpling

        - 支持输出带有列名的 `INSERT` 语句 [#135](https://github.com/pingcap/dumpling/pull/135)
        - 将 `--filesize` 和 `--statement-size` 参数与 mydumper 保持统一 [#142](https://github.com/pingcap/dumpling/pull/142)

    + TiDB Lightning

        - Split 的 Region 大小更加精确 [#369](https://github.com/pingcap/tidb-lightning/pull/369)

    + TiDB Binlog

        - 支持以 go time 的格式设置 GC 时间 [#996](https://github.com/pingcap/tidb-binlog/pull/996)

## Bug 修复

+ TiDB

    - 修复了在 Metric Profile 中 `tikv_cop_wait` time 的一个问题 [#19881](https://github.com/pingcap/tidb/pull/19881)
    - 修复了 `SHOW GRANTS` 显示错误结果的问题 [#19834](https://github.com/pingcap/tidb/pull/19834)
    - 修复了使用 `!= ALL (subq)` 查询结果不正确的问题 [#19831](https://github.com/pingcap/tidb/pull/19831)
    - 修复了转换 `ENUM` 和 `SET` 类型的一个问题 [#19778](https://github.com/pingcap/tidb/pull/19778)
    - 增加了 `SHOW STATS_META`、`SHOW STATS_BUCKET` 的一个权限检查 [#19760](https://github.com/pingcap/tidb/pull/19760)
    - 修复了由 `builtinGreatestStringSig` 和 `builtinLeastStringSig` 引起的列长度不匹配问题 [#19758](https://github.com/pingcap/tidb/pull/19758)
    - 如果向量化计算抛出多余的 errors 或者 warnings，回退向量化执行到标量执行 [#19749](https://github.com/pingcap/tidb/pull/19749)
    - 修复了在相关列类型是 `Bit` 时 `Apply` 算子出现错误的问题 [#19692](https://github.com/pingcap/tidb/pull/19692)
    - 修复了在 MySQL 8.0 客户端中查询 processlist 和 cluster_log 时出现的问题 [#19690](https://github.com/pingcap/tidb/pull/19690)
    - 修复了相同类型的 plan 具有不同类型的 plan digest 的错误 [#19684](https://github.com/pingcap/tidb/pull/19684)
    - 禁止从 `Decimal` to `Int` 变更列类型 [#19682](https://github.com/pingcap/tidb/pull/19682)
    - 修复了 `SELECT ... INTO OUTFILE` 返回运行时错误的问题 [#19672](https://github.com/pingcap/tidb/pull/19672)
    - 修复了 `builtinRealIsFalseSig` 的不正确的实现 [#19670](https://github.com/pingcap/tidb/pull/19670)
    - 修复了分区表达式检查漏掉括号表达式的问题 [#19614](https://github.com/pingcap/tidb/pull/19614)
    - 修复了当在 `HashJoin` 上具有 `Apply` 算子时的查询错误 [#19611](https://github.com/pingcap/tidb/pull/19611)
    - 修复了向量化将 `Real` cast 成 `Time` 类型时的错误的结果 [#19594](https://github.com/pingcap/tidb/pull/19594)
    - 修复了 `SHOW GRANTS` 可以显示不存在用户的 grants 信息的错误 [#19588](https://github.com/pingcap/tidb/pull/19588)
    - 修复了当在 `IndexLookupJoin` 上具有 `Apply` 算子时的查询错误 [#19566](https://github.com/pingcap/tidb/pull/19566)
    - 修复了当在分区表上将 `Apply` 转化成 `HashJoin` 时的错误结果 [#19546](https://github.com/pingcap/tidb/pull/19546)
    - 修复了当在 `Apply` 的 inner 端具有 `IndexLookUp` 算子时的错误结果 [#19508](https://github.com/pingcap/tidb/pull/19508)
    - 修复了使用视图时非预期的 panic [#19491](https://github.com/pingcap/tidb/pull/19491)
    - 修复了 `anti-semi-join` 查询时的不正确结果 [#19477](https://github.com/pingcap/tidb/pull/19477)
    - 修复了删除统计信息时未删除 topN 的统计信息的错误 [#19465](https://github.com/pingcap/tidb/pull/19465)
    - 修复了因错误使用 batch point get 时产生的错误结果 [#19460](https://github.com/pingcap/tidb/pull/19460)
    - 修复了在带有虚拟生成列的 `IndexLookupJoin` 上无法找到列的错误 [#19439](https://github.com/pingcap/tidb/pull/19439)
    - 修复了在 `SELECT` 和 `UPDATE` 查询上的不同计划比较 datum 的错误 [#19403](https://github.com/pingcap/tidb/pull/19403)
    - 修复了 TiFlash 在 Region cache 上产生的 work index 数据争用 [#19362](https://github.com/pingcap/tidb/pull/19362)
    - 修复了 `logarithm` 函数不返回 warning 的错误 [#19291](https://github.com/pingcap/tidb/pull/19291)
    - 修复了当使用 TiDB 落盘时产生的非预期错误 [#19272](https://github.com/pingcap/tidb/pull/19272)
    - 支持在 Index Join 的 inner 端使用单个分区表 [#19197](https://github.com/pingcap/tidb/pull/19197)
    - 修复了对 decimal 产生的错误的 hash 键值 [#19188](https://github.com/pingcap/tidb/pull/19188)
    - 修复了当 table EndKey 和 Region EndKey 相同时 TiDB 会产生 no regions 的错误 [#19895](https://github.com/pingcap/tidb/pull/19895)
    - 修复了 `alter partition` 的非预期成功 [#19891](https://github.com/pingcap/tidb/pull/19891)
    - 修复了在下推表达式上，默认最大允许的包长的错误 [#19876](https://github.com/pingcap/tidb/pull/19876)
    - 修复了在 `ENUM`/`SET` 列上 `Max`/`Min` 函数的错误行为 [#19869](https://github.com/pingcap/tidb/pull/19869)
    - 修复了当部分 TiFlash 节点下线之后，`tiflash_segments` 和 `tiflash_tables` 系统表读取失败的问题 [#19748](https://github.com/pingcap/tidb/pull/19748)
    - 修复了 `Count()` 聚集函数的错误结果 [#19628](https://github.com/pingcap/tidb/pull/19628)
    - 修复了 `TRUNCATE` 操作的运行时错误 [#19445](https://github.com/pingcap/tidb/pull/19445)
    - 修复了 `PREPARE statement FROM @Var` 语句在 `Var` 包含大写字符时候会失败的错误 [#19378](https://github.com/pingcap/tidb/pull/19378)
    - 修复了在具有大写表名的表上修改 charset 会产生 panic 的错误 [#19302](https://github.com/pingcap/tidb/pull/19302)
    - 修复了当在包含 `tikv/tiflash` 信息时，`information_schema.statements_summary` 和 `explain` 计划的不一致性 [#19159](https://github.com/pingcap/tidb/pull/19159)
    - 修复了在测试中 `select into outfile` 出现文件不存在的错误 [#19725](https://github.com/pingcap/tidb/pull/19725)
    - 修复了 `INFORMATION_SCHEMA.CLUSTER_HARDWARE` 不含有 raid 设备信息的问题 [#19457](https://github.com/pingcap/tidb/pull/19457)
    - 修复一个问题，使具有 `case-when` 表达式生成列的索引添加操作在遇到 parse 错误时能够正常退出 [#19395](https://github.com/pingcap/tidb/pull/19395)
    - 修复 DDL 长时间重试的错误 [#19488](https://github.com/pingcap/tidb/pull/19488)
    - 修复错误，使 `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)` 语句执行不需要先执行 `use db` [#19471](https://github.com/pingcap/tidb/pull/19471)
    - 修复使日志文件中 dispatch errors 从 Error 形式转变为 Info 信息 [#19454](https://github.com/pingcap/tidb/pull/19454)

+ TiKV

    - 修复开启 collation 时对于非 index 列统计信息估算错误的问题 [#8620](https://github.com/tikv/tikv/pull/8620)
    - 修复当迁移 Region 时 Green GC 可能错过 lock 的问题 [#8460](https://github.com/tikv/tikv/pull/8460)
    - 修复 TiKV 在极端繁忙下 Raft 成员变更可能出现 panic 的问题 [#8497](https://github.com/tikv/tikv/pull/8497)
    - 修复 PD client 和其他线程发起 PD sync requests 可能导致死锁的问题 [#8612](https://github.com/tikv/tikv/pull/8612)
    - 升级 jemalloc 到 5.2.1 以解决 huge page 的内存分配问题 [#8463](https://github.com/tikv/tikv/pull/8463)
    - 修复 unified thread pool 可能停止工作的问题 [#8427](https://github.com/tikv/tikv/pull/8427)

+ PD

    - 添加 `initial-cluster-token` 配置避免启动时 cluster 之间的通信 [#2922](https://github.com/pingcap/pd/pull/2922)
    - 修正自动模式下 store limit 的单位 [#2826](https://github.com/pingcap/pd/pull/2826)
    - 添加对于 scheduler 持久化时引发的错误的处理 [#2818](https://github.com/tikv/pd/pull/2818)
    - 修复 scheduler 的 http 接口的返回结果可能为空的问题 [#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)

+ TiFlash

    - 修复在更早版本中修改主键列名后，升级到 v4.0.4/v4.0.5 时 TiFlash 启动失败的问题
    - 修复在修改列的 nullable 属性后访问数据可能抛异常的问题
    - 修复在计算表同步状态时导致的崩溃问题
    - 修复当用户进行一些不兼容的 DDL 操作后，读取 TiFlash 数据遇到异常的问题
    - 修复从 TiDB 同步到不支持的 collation 时，抛出异常的问题
    - 修复 Grafana 中 TiFlash coprocessor executor QPS 面板始终显示为 0 的问题
    - 修复 `FROM_UNIXTIME` 函数遇到 `NULL` 值时返回错误结果的问题

+ Tools

    + TiCDC

        - 解决某些场景下内存泄露的问题 [#942](https://github.com/pingcap/ticdc/pull/942)
        - 解决 Kafka sink 可能会出现的异常退出的问题 [#912](https://github.com/pingcap/ticdc/pull/912)
        - 解决 CRTs 小于 Resolved Ts 而异常退出的问题 [#927](https://github.com/pingcap/ticdc/pull/927)
        - 解决同步任务可能卡在 MySQL 上的问题 [#936](https://github.com/pingcap/ticdc/pull/936)
        - 修复 TiCDC 不合理的 Resolved Ts 超时等待 [#8573](https://github.com/tikv/tikv/pull/8573)

    + Backup & Restore (BR)

        - 解决数据校验期间可能出现的异常退出的问题 [#479](https://github.com/pingcap/br/pull/479)
        - 解决 PD leader 切换后可能出现的异常退出的问题 [#496](https://github.com/pingcap/br/pull/496)

    + Dumpling

        - 解决 binary 类型的 `NULL` 值没有被正确处理的问题 [#137](https://github.com/pingcap/dumpling/pull/137)

    + TiDB Lightning

        - 解决 write 和 ingest 失败后依旧显示成功的问题 [#381](https://github.com/pingcap/tidb-lightning/pull/381)
        - 解决写 checkpoint 不及时的问题 [#386](https://github.com/pingcap/tidb-lightning/pull/386)
