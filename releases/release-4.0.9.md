---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 Release Notes

发版日期：2020 年 12 月 21 日

TiDB 版本：4.0.9

## 兼容性更改

+ TiDB

    - 废弃配置文件中 `enable-streaming` 配置项 [#21055](https://github.com/pingcap/tidb/pull/21055)

+ TiKV

    - 减少开启加密时的 I/O 开销和锁冲突。该修改向下不兼容。如果需要降级至 v4.0.9 以下，需要将 `security.encryption.enable-file-dictionary-log` 配置为 `false`，并在降级前重启 [#9195](https://github.com/tikv/tikv/pull/9195)

## 新功能

+ TiFlash

    - 支持将存储引擎的新数据分布在多个硬盘上，分摊 I/O 压力（实验特性）

+ TiDB Dashboard

    - SQL 语句分析功能的列表界面支持显示所有字段并排序 [#749](https://github.com/pingcap/tidb-dashboard/pull/749)
    - 集群拓扑页面支持缩放 [#772](https://github.com/pingcap/tidb-dashboard/pull/772)
    - SQL 语句分析及慢日志页面支持显示 SQL 语句的临时存储占用大小 [#777](https://github.com/pingcap/tidb-dashboard/pull/777)
    - SQL 语句分析及慢日志列表界面支持导出列表数据 [#778](https://github.com/pingcap/tidb-dashboard/pull/778)
    - 支持配置自定义 Prometheus 地址 [#808](https://github.com/pingcap/tidb-dashboard/pull/808)
    - 新增集群实例统计摘要页面 [#815](https://github.com/pingcap/tidb-dashboard/pull/815)
    - 慢日志详情页面新增更多时间字段 [#810](https://github.com/pingcap/tidb-dashboard/pull/810)

## 优化提升

+ TiDB

    - 在转换等值条件为其它条件时，通过使用启发式规则，避免生成 (index) merge join 以得到更好的执行计划 [#21146](https://github.com/pingcap/tidb/pull/21146)
    - 区分用户变量的类型 [#21107](https://github.com/pingcap/tidb/pull/21107)
    - 在配置文件中添加了 `performance.gogc` 配置项，用于设置 `GOGC` [#20922](https://github.com/pingcap/tidb/pull/20922)
    - 提升 `Timestamp` 和 `Datetime` 类型的二进制输出结果与 MySQL 的兼容性 [#21135](https://github.com/pingcap/tidb/pull/21135)
    - 优化用户使用 `LOCK IN SHARE MODE`  SQL 语句时输出的报错信息 [#21005](https://github.com/pingcap/tidb/pull/21005)
    - 优化在可剪切的表达式进行常量折叠时输出的错误信息，避免输出不必要的警告或错误信息 [#21040](https://github.com/pingcap/tidb/pull/21040)
    - 优化 `LOAD DATA` 语句执行 `PREPARE` 时的报错信息 [#21199](https://github.com/pingcap/tidb/pull/21199)
    - 修改整型列的类型时，忽略掉整型字段的零值填充的属性 [#20986](https://github.com/pingcap/tidb/pull/20986)
    - 在 `EXPLAIN ANALYZE` 结果中输出 DML 语句执行器相关运行时的信息 [#21066](https://github.com/pingcap/tidb/pull/21066)
    - 禁止在一条语句中对主键做出多次不同的修改 [#21113](https://github.com/pingcap/tidb/pull/21113)
    - 添加连接空闲时间的监控项 [#21301](https://github.com/pingcap/tidb/pull/21301)
    - 新增运行 `runtime/trace` 分析工具时系统自动临时开启慢日志的功能 [#20578](https://github.com/pingcap/tidb/pull/20578)

+ TiKV

    - 添加标记以跟踪 `split` 命令的来源 [#8936](https://github.com/tikv/tikv/pull/8936)
    - 支持动态修改 `pessimistic-txn.pipelined` 配置项 [#9100](https://github.com/tikv/tikv/pull/9100)
    - 减少运行 Backup & Restore 和 TiDB Lightning 时对系统的性能影响 [#9098](https://github.com/tikv/tikv/pull/9098)
    - 添加 Ingesting SST 报错的监控项 [#9096](https://github.com/tikv/tikv/pull/9096)
    - 阻止 Leader 在任意副本需要复制日志时进入休眠状态 [#9093](https://github.com/tikv/tikv/pull/9093)
    - 提高 Pipelined locking 的成功率 [#9086](https://github.com/tikv/tikv/pull/9086)
    - 调整配置项 `apply-max-batch-size` 和 `store-max-batch-size` 的默认值为 `1024` [#9020](https://github.com/tikv/tikv/pull/9020)
    - 添加 `max-background-flushes` 配置 [#8947](https://github.com/tikv/tikv/pull/8947)
    - 默认关闭 RocksDB consistency check 以提高性能 [#9029](https://github.com/tikv/tikv/pull/9029)
    - 将 Region 大小的查询操作移出 `pd heartbeat worker` 以减轻其压力 [#9185](https://github.com/tikv/tikv/pull/9185)

+ PD

    - TiKV store 转变为 `Tombstone` 状态时检查 TiKV 集群的版本号，防止用户降级和升级过程中的开启不兼容特性[#3213](https://github.com/pingcap/pd/pull/3213)
    - 禁止低版本的 TiKV 强制从 `Tombstone` 状态转为 `Up` [#3206](https://github.com/pingcap/pd/pull/3206)

+ TiDB Dashboard

    - 对于 SQL 语句文本点击 “展开” 后支持保持展开状态 [#775](https://github.com/pingcap/tidb-dashboard/pull/775)
    - 默认在新窗口打开 SQL 语句分析和慢日志详情 [#816](https://github.com/pingcap/tidb-dashboard/pull/816)
    - 改进慢日志页面部分时间字段描述 [#817](https://github.com/pingcap/tidb-dashboard/pull/817)
    - 改进错误信息提示，显示更完整的错误内容 [#794](https://github.com/pingcap/tidb-dashboard/pull/794)

+ TiFlash

    - 降低 Replica read 时的延迟
    - 优化 TiFlash 的错误信息
    - 优化在大数据量下，对缓存数据大小的限制
    - 添加正在处理的 Coprocessor 请求数量的 metric

+ Tools

    + Backup & Restore (BR)

        - BR 不再接受存在歧义的 `--checksum false`（不会正确关闭 checksum） 命令行参数，正确用法为 `--checksum=false` [#588](https://github.com/pingcap/br/pull/588)
        - 支持暂时性地调整 PD 的参数，在 BR 意外退出后，PD 能自动恢复回正常参数 [#596](https://github.com/pingcap/br/pull/596)
        - 支持恢复数据表的统计信息 [#622](https://github.com/pingcap/br/pull/622)
        - 系统自动重试 `read index not ready` 和 `proposal in merging mode` 两种错误 [#626](https://github.com/pingcap/br/pull/626)

    + TiCDC

        - 添加对 TiKV 开启 Hibernate Region 的告警规则 [#1120](https://github.com/pingcap/ticdc/pull/1120)
        - 优化 schema storage 的内存使用 [#1127](https://github.com/pingcap/ticdc/pull/1127)
        - 增加 Unified Sorter 功能，可以在数据量较大的情况下提升增量扫阶段的同步速度（实验特性）[#1122](https://github.com/pingcap/ticdc/pull/1122)
        - 支持在 TiCDC Open Protocol 中配置单条 Kafka 消息的最大大小和包含的最大行变更数量（仅在 Kafka sink 生效）[#1079](https://github.com/pingcap/ticdc/pull/1079)
    + Dumpling

        - 对导出失败部分的数据进行重试 [#182](https://github.com/pingcap/dumpling/pull/182)
        - 支持同时设置 `-F` 和 `-r` 两个参数 [#177](https://github.com/pingcap/dumpling/pull/177)
        - 默认不导出系统表 [#194](https://github.com/pingcap/dumpling/pull/194)
        - 在设置 `--transactional-consistency` 参数时支持重建 MySQL 链接 [#199](https://github.com/pingcap/dumpling/pull/199)
        - 支持使用 `-c,--compress` 参数指定 Dumpling 使用的压缩算法，空字符串代表不压缩 [#202](https://github.com/pingcap/dumpling/pull/202)

    + TiDB Lightning

        - 默认不恢复系统表 [#459](https://github.com/pingcap/tidb-lightning/pull/459)
        - 支持为 auto-random 的主键设置默认值 [#457](https://github.com/pingcap/tidb-lightning/pull/457)
        - 完善 Local 模式下分裂 Region 的精度 [#422](https://github.com/pingcap/tidb-lightning/pull/422)
        - 支持给 `tikv-importer.region-split-size`、`mydumper.read-block-size`、`mydumper.batch-size` 和 `mydumper.max-region-size` 设置可读的参数（比如 "2.5 GiB"）[#471](https://github.com/pingcap/tidb-lightning/pull/471)

    + TiDB Binlog

        - 在写下游出错时给 Drainer 设置非零退出码 [#1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## Bug 修复

+ TiDB

    - 修复了前缀索引和 `OR` 条件一起使用时结果不正确的问题 [#21287](https://github.com/pingcap/tidb/pull/21287)
    - 修复了开启自动重试后可能出现的一处 panic [#21285](https://github.com/pingcap/tidb/pull/21285)
    - 修复了根据列类型检查分区表定义时出现的一处问题 [#21273](https://github.com/pingcap/tidb/pull/21273)
    - 修复了分区表对于列的类型检查的一处问题。分区表达式的值的类型和分区列的类型必须一致 [#21136](https://github.com/pingcap/tidb/pull/21136)
    - 修复了哈希分区表对于分区名唯一性检查的问题 [#21257](https://github.com/pingcap/tidb/pull/21257)
    - 修复非 `INT` 类型的值，插入到哈希分区表后结果不正确的问题 [#21238](https://github.com/pingcap/tidb/pull/21238)
    - 修复了在部分写入类的场景中，使用了 index join 会遇到非预期报错的问题 [#21249](https://github.com/pingcap/tidb/pull/21249)
    - 修复了在 `CASE WHEN` 中 `BigInt` 无符列的值被错误地转换成有符类型的问题 [#21236](https://github.com/pingcap/tidb/pull/21236)
    - 修复了 index hash join 和 index merge join 没有考虑 collation 的问题 [#21219](https://github.com/pingcap/tidb/pull/21219)
    - 修复了分区表在建表和查询时，没有考虑 collation 的问题 [#21181](https://github.com/pingcap/tidb/pull/21181)
    - 修复了慢日志记录的查询结果可能不全的问题 [#21211](https://github.com/pingcap/tidb/pull/21211)
    - 修复了一处数据库名大小写处理不当，导致的 `DELETE` 未正确删除数据的问题 [#21206](https://github.com/pingcap/tidb/pull/21206)
    - 修复了执行 DML 语句导致 schema 的内存被覆盖的问题 [#21050](https://github.com/pingcap/tidb/pull/21050)
    - 修复了使用 join 时，无法查询到合并后的列的问题 [#21021](https://github.com/pingcap/tidb/pull/21021)
    - 修复了一些 semi-join 的查询结果不正确的问题 [#21019](https://github.com/pingcap/tidb/pull/21019)
    - 修复了表锁对于 `UPDATE` 语句不生效的问题 [#21002](https://github.com/pingcap/tidb/pull/21002)
    - 修复创建递归的视图出现栈溢出的问题 [#21001](https://github.com/pingcap/tidb/pull/21001)
    - 修复了 index merge join 在执行外连接的时候，结果不符合预期的问题 [#20954](https://github.com/pingcap/tidb/pull/20954)
    - 修复了一处事务问题，该场景下应该返回结果未知，但是却返回了执行失败 [#20925](https://github.com/pingcap/tidb/pull/20925)
    - 修复 `explain for connection` 无法显示最后一次执行计划的问题 [#21315](https://github.com/pingcap/tidb/pull/21315)
    - 修复在 Read Committed 隔离级别下，Index Merge 结果不正确的问题 [#21253](https://github.com/pingcap/tidb/pull/21253)
    - 修复了由于事务写冲突重试导致的 auto-ID 分配失败 [#21079](https://github.com/pingcap/tidb/pull/21079)
    - 修复了 JSON 数据无法通过 `load data` 无法正确导入到 TiDB 的问题 [#21074](https://github.com/pingcap/tidb/pull/21074)
    - 修复新增加 `Enum` 类型列的默认值问题 [#20998](https://github.com/pingcap/tidb/pull/20998)
    - 对于日期类型的数学计算，保留原始的数据类型信息，修复 `adddate` 函数插入非法值的问题 [#21176](https://github.com/pingcap/tidb/pull/21176)
    - 修复了部分场景错误地生成了 `PointGet` 的执行计划，导致执行结果不正确 [#21244](https://github.com/pingcap/tidb/pull/21244)
    - 在 `ADD_DATE` 函数中忽略夏令时的转换，以和 MySQL 兼容 [#20888](https://github.com/pingcap/tidb/pull/20888)
    - 修复了插入尾部带有超出 `varchar` 和 `char` 长度限制的空白字符的字符串时报错的 bug [#21282](https://github.com/pingcap/tidb/pull/21282)
    - 修复了对比 `int` 和 `year` 类型时没有将 `[1, 69]` 的整数转换为 `[2001, 2060]` 以及没有将 `[70, 99]` 的整数转换为 `[1970, 1999]` 的兼容性 bug [#21283](https://github.com/pingcap/tidb/pull/21283)
    - 修复了 `sum()` 函数计算 `Double` 类型字段的结果溢出导致 panic 的问题 [#21272](https://github.com/pingcap/tidb/pull/21272)
    - 修复了 `DELETE` 语句未能给 unique key 加悲观锁的问题 [#20705](https://github.com/pingcap/tidb/pull/20705)
    - 修复了快照读能够命中 lock cache，返回错误结果的问题 [#21539](https://github.com/pingcap/tidb/pull/21539)
    - 修复了在同一个事务中读取大量数据时可能发生的内存泄漏问题 [#21129](https://github.com/pingcap/tidb/pull/21129)
    - 修复了在子查询中省略表别名时的语法解析错误问题 [#20367](https://github.com/pingcap/tidb/pull/20367)

+ TiKV

    - 修复当列个数大于 255 时，下推返回错误结果集的问题 [#9131](https://github.com/tikv/tikv/pull/9131)
    - 修复网络隔离时 Region Merge 可能会导致数据丢失的问题 [#9108](https://github.com/tikv/tikv/pull/9108)
    - 修复使用 `latin1` 字符集时，`ANALYZE` 语句会导致 panic 的问题 [#9082](https://github.com/tikv/tikv/pull/9082)
    - 修复类型转换中将数字转成时间会得到错误结果的问题 [#9031](https://github.com/tikv/tikv/pull/9031)
    - 修复当开启加密时无法使用 TiDB Lightning 导入数据的问题 [#8995](https://github.com/tikv/tikv/pull/8995)
    - 修复使用 `0.0.0.0` 时 `advertise-status-addr` 异常的问题 [#9036](https://github.com/tikv/tikv/pull/9036)
    - 修复当事务删除 key 时却报 key 已存在的问题 [#8930](https://github.com/tikv/tikv/pull/8930)
    - 修复 RocksDB cache 映射错误导致的数据错误问题 [#9029](https://github.com/tikv/tikv/pull/9029)
    - 修复当 Leader 切换时 Follower Read 可能返回旧数据的问题 [#9240](https://github.com/tikv/tikv/pull/9240)
    - 修复悲观锁下可能读到旧值的问题 [#9282](https://github.com/tikv/tikv/pull/9282)
    - 修复 transfer leader 后 replica read 可能会读到旧值的问题 [#9240](https://github.com/tikv/tikv/pull/9240)
    - 修复 TiKV 在 profiling 结束后再收到 `SIGPROF` 会 panic 的问题 [#9229](https://github.com/tikv/tikv/pull/9229)

+ PD

    - 修复在特殊情况下 Placement Rule 指定的 leader 绑定不生效的问题 [#3208](https://github.com/pingcap/pd/pull/3208)
    - 修复 `trace-region-flow` 在配置更新时被置为 `false` 的问题 [#3120](https://github.com/pingcap/pd/pull/3120)
    - 修复特殊情况下 safepoint 有无限 TTL 的问题 [#3143](https://github.com/pingcap/pd/pull/3143)

+ TiDB Dashboard

    - 修复部分时间显示混杂中英文的问题 [#755](https://github.com/pingcap/tidb-dashboard/pull/755)
    - 修复部分不兼容的浏览器中没有提示不兼容的问题 [#776](https://github.com/pingcap/tidb-dashboard/pull/776)
    - 修复部分情况下事务时间戳显示不正确的问题 [#793](https://github.com/pingcap/tidb-dashboard/pull/793)
    - 修复部分 SQL 文本格式化后成为无效 SQL 语句的问题 [#805](https://github.com/pingcap/tidb-dashboard/pull/805)

+ TiFlash

    - 修复 `INFORMATION_SCHEMA.CLUSTER_HARDWARE` 中可能包含未被使用的硬盘信息的问题
    - 修复 Delta cache 内存占用量估算偏少的问题
    - 修复由线程统计信息引起的内存泄露问题

+ Tools

    + Backup & Restore (BR)

        - 修复因 S3 secret access keys 中存在特殊字符而导致失败的问题 [#617](https://github.com/pingcap/br/pull/617)

    + TiCDC

        - 修复某些异常情况下存在多个 Owner 的问题 [#1104](https://github.com/pingcap/ticdc/pull/1104)
        - 修复在 TiKV 节点意外退出或重启恢复情况下 TiCDC 不能正常同步的问题，该 bug 在 v4.0.8 引入 [#1198](https://github.com/pingcap/ticdc/pull/1198)
        - 修复在表初始化过程中会向 etcd 中重复写入元数据的问题 [#1191](https://github.com/pingcap/ticdc/pull/1191)
        - 修复 schema storage 缓存 TiDB 表信息的过程中因更新表信息延迟或过早 GC 导致同步中断的问题 [#1114](https://github.com/pingcap/ticdc/pull/1114)
        - 修复 schema storage 在 DDL 频繁的情况下会消耗过多内存的问题 [#1127](https://github.com/pingcap/ticdc/pull/1127)
        - 修复在同步任务暂停或取消之后会产生 goroutine 泄露的问题 [#1075](https://github.com/pingcap/ticdc/pull/1075)
        - 增加 Kafka producer 最大重试时间到 600s，避免在下游 Kafka 服务或网络抖动情况下同步中断 [#1118](https://github.com/pingcap/ticdc/pull/1118)
        - 修复 Kafka 消息所包含行变更数量不能正常生效的问题 [#1112](https://github.com/pingcap/ticdc/pull/1112)
        - 修复当 TiCDC 与 PD 间网络出现抖动，并且同时操作 TiCDC changefeed 暂停和恢复，可能会出现部分表数据没有被同步的问题 [#1213](https://github.com/pingcap/ticdc/pull/1213)
        - 修复 TiCDC 与 PD 网络不稳定情况下 TiCDC 可能出现进程非预期退出的问题 [#1218](https://github.com/pingcap/ticdc/pull/1218)
        - 在 TiCDC 内部使用全局 PD client，以及修复 PD client 被错误关闭导致同步阻塞的问题 [#1217](https://github.com/pingcap/ticdc/pull/1217)
        - 修复 TiCDC owner 节点可能在 etcd watch client 里消耗过多内存的问题 [#1224](https://github.com/pingcap/ticdc/pull/1224)

    + Dumpling

        - 修复在某些情况下 MySQL 链接关闭导致 Dumpling 卡住的问题 [#190](https://github.com/pingcap/dumpling/pull/190)

    + TiDB Lightning

        - 修复使用错误信息编码 key 的问题 [#437](https://github.com/pingcap/tidb-lightning/pull/437)
        - 修复 GC life time TTL 不生效的问题 [#448](https://github.com/pingcap/tidb-lightning/pull/448)
        - 修复手动关闭时可能出现的 panic 问题 [#484](https://github.com/pingcap/tidb-lightning/pull/484)
