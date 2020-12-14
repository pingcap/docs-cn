---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 Release Notes

发版日期：2020 年 12 月 10 日

TiDB 版本：4.0.9

## 兼容性更改

+ TiDB

- 废弃配置文件中 `enable-streaming` 配置项 [#21055](https://github.com/pingcap/tidb/pull/21055)

## 新功能

+ TiFlash

    - 支持将存储引擎的新数据分布在多个硬盘上，分摊 I/O 压力（实验特性）

## 优化提升

+ TiDB

    - 在转换等值条件为其它条件时，通过使用启发式规则，避免生成 (index) merge join 以得到更好的执行计划 [#21146](https://github.com/pingcap/tidb/pull/21146)
    - 区分用户变量的类型 [#21107](https://github.com/pingcap/tidb/pull/21107)
    - 在配置文件中添加了 `performance.gogc` 配置项，用于设置 `GOGC` [#20922](https://github.com/pingcap/tidb/pull/20922)
    - 提升了 `Timestamp` 和 `Datetime` 类型的二进制输出结果的 MySQL 兼容性 [#21135](https://github.com/pingcap/tidb/pull/21135)
    - 为使用 `LOCK IN SHARE MODE` 语法的 SQL 语句提供报错信息 [#21005](https://github.com/pingcap/tidb/pull/21005)
    - 对于可剪切的表达式进行常量折叠时，避免输出不必要的警告或错误 [#21040](https://github.com/pingcap/tidb/pull/21040)
    - 优化了 `LOAD DATA` 语句执行 `PREPARE` 操作的报错信息 [#21199](https://github.com/pingcap/tidb/pull/21199)
    - 修改列类型的时候，忽略掉整型字段的零值填充大小属性 [#20986](https://github.com/pingcap/tidb/pull/20986)
    - 在 `EXPLAIN ANALYZE` 结果中正确显示 DML 语句执行器相关的运行时信息 [#21066](https://github.com/pingcap/tidb/pull/21066)
    - 禁止在一条语句中对主键做出多次不同的修改 [#21113](https://github.com/pingcap/tidb/pull/21113)
    - 添加了对于连接的空闲时间的监控项 [#21301](https://github.com/pingcap/tidb/pull/21301)

+ TiKV

    - 添加标记以跟踪 `split` 命令的来源 [#8936](https://github.com/tikv/tikv/pull/8936)
    - 支持动态更改配置 `pessimistic-txn.pipelined` [#9100](https://github.com/tikv/tikv/pull/9100)
    - 减少运行 Backup & Restore 和 TiDB Lightning 时对系统的性能影响 [#9098](https://github.com/tikv/tikv/pull/9098)
    - 添加关于 Ingesting SST 报错的监控项 [#9096](https://github.com/tikv/tikv/pull/9096)
    - 如果还有副本在追日志，则停止进入休眠状态 [#9093](https://github.com/tikv/tikv/pull/9093)
    - 提高悲观锁流水线的成功率 [#9086](https://github.com/tikv/tikv/pull/9086)
    - 调整配置项 `apply-max-batch-size` 和 `store-max-batch-size` 的默认值为 `1024` [#9020](https://github.com/tikv/tikv/pull/9020)
    - 添加 `max-background-flushes` 配置 [#8947](https://github.com/tikv/tikv/pull/8947)
    - 对 storage 模块默认开启统一线程池 [#8887](https://github.com/tikv/tikv/pull/8887)
    - 默认关闭 Rocksdb consistency check 以提高性能 [#9029](https://github.com/tikv/tikv/pull/9029)

+ PD

    - TiKV store 转变为 `Tombstone` 状态时检查 TiKV 集群的版本 [#3213](https://github.com/pingcap/pd/pull/3213)
    - 不允许低版本的 TiKV 强制从 `Tombstone` 状态转为 `Up` [#3206](https://github.com/pingcap/pd/pull/3206)
    - 升级 Dashboard 版本到 v2020.11.26.1 [#3219](https://github.com/pingcap/pd/pull/3219)

+ TiFlash

    - 降低 Replica read 时的延迟
    - 优化 TiFlash 的错误信息
    - 优化在大数据量下，对缓存数据大小的限制
    - 添加正在处理的 coprocessor 请求数量的 metric

+ Tools

    + Backup & Restore (BR)

        - BR 不再接受存在歧义的 `--checksum false` 命令行参数，正确用法为 `--checksum=false` [#588](https://github.com/pingcap/br/pull/588)
        - 支持暂时性地调整 PD 的参数 [#596](https://github.com/pingcap/br/pull/596)
        - 支持恢复数据表的统计信息 [#622](https://github.com/pingcap/br/pull/622)
        - 对于可恢复错误 `read index not ready` 和 `proposal in merging mode` 进行重试 [#626](https://github.com/pingcap/br/pull/626)

    + TiCDC

        - 添加对 TiKV 开启 Hibernate Region 的告警规则 [#1120](https://github.com/pingcap/ticdc/pull/1120)
        - 优化 schema storage 的内存使用 [#1127](https://github.com/pingcap/ticdc/pull/1127)

    + Dumpling

        - 对导出失败部分的数据进行重试 [#182](https://github.com/pingcap/dumpling/pull/182)
        - 支持同时设置 `-F` 和 `-r` 两个参数 [#177](https://github.com/pingcap/dumpling/pull/177)
        - 默认不导出系统表 [#194](https://github.com/pingcap/dumpling/pull/194)
        - 在设置 `--transactional-consistency` 参数时支持重建 MySQL 链接 [#199](https://github.com/pingcap/dumpling/pull/199)

    + TiDB Lightning

        - 默认不恢复系统表 [#459](https://github.com/pingcap/tidb-lightning/pull/459)
        - 支持为 auto-random 的主键设置默认值 [#457](https://github.com/pingcap/tidb-lightning/pull/457)
        - 完善 local 模式下分裂 Region 的精度 [#422](https://github.com/pingcap/tidb-lightning/pull/422)
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
    - 修复在 Read Committed 隔离级别下，index merge 结果不正确的问题 [#21253](https://github.com/pingcap/tidb/pull/21253)
    - 修复了由于事务写冲突重试导致的 auto-ID 分配失败 [#21079](https://github.com/pingcap/tidb/pull/21079)
    - 修复了 JSON 数据无法通过 `load data` 无法正确导入到 TiDB 的问题 [#21074](https://github.com/pingcap/tidb/pull/21074)
    - 修复新增加 `Enum` 类型列的默认值问题 [#20998](https://github.com/pingcap/tidb/pull/20998)
    - 对于日期类型的数学计算，保留原始的数据类型信息，修复 `adddata` 函数插入非法值的问题 [#21176](https://github.com/pingcap/tidb/pull/21176)
    - 修复了部分场景错误地生成了 PointGet 的执行计划，导致执行结果不正确 [#21244](https://github.com/pingcap/tidb/pull/21244)

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

+ PD

    - 修复在特殊情况下 Placement rule 指定的 leader 绑定不生效的问题 [#3208](https://github.com/pingcap/pd/pull/3208)
    - 修复 `trace-region-flow` 在配置更新时被置为 `false` 的问题 [#3120](https://github.com/pingcap/pd/pull/3120)
    - 修复特殊情况下 safepoint 有无限 TTL 的问题 [#3143](https://github.com/pingcap/pd/pull/3143)

+ TiFlash

    - 修复 `INFORMATION_SCHEMA.CLUSTER_HARDWARE` 中可能包含未被使用的硬盘信息的问题
    - 修复 Delta cache 内存占用量估算偏少的问题
    - 修复由线程统计信息引起的内存泄露问题

+ Tools

    + Backup & Restore (BR)

        - 修复因 S3 secret access keys 中存在特殊字符而导致失败的问题 [#617](https://github.com/pingcap/br/pull/617)

    + TiCDC

        - 修复某些异常情况下存在多个 Owner 的问题 [#1104](https://github.com/pingcap/ticdc/pull/1104)

    + Dumpling

        - 修复在某些情况下 MySQL 链接关闭导致 Dumpling 卡住的问题 [#190](https://github.com/pingcap/dumpling/pull/190)

    + TiDB Lightning

        - 修复使用错误信息编码 key 的问题 [#437](https://github.com/pingcap/tidb-lightning/pull/437)
        - 修复 GC life time TTL 不生效的问题 [#448](https://github.com/pingcap/tidb-lightning/pull/448)
        - 修复手动关闭时可能出现的 panic 问题 [#484](https://github.com/pingcap/tidb-lightning/pull/484)
