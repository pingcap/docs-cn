---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 Release Notes

发版日期：2021 年 2 月 26 日

TiDB 版本：4.0.11

## 新功能

+ TiDB

    - 支持 `uft8_unicode_ci` 和 `utf8mb4_unicode_ci` 排序规则 [#22558](https://github.com/pingcap/tidb/pull/22558)

+ TiKV

    - 支持 `utf8mb4_unicode_ci` 排序规则 [#9577](https://github.com/tikv/tikv/pull/9577)
    - 支持 `cast_year_as_time` 排序规则 [#9299](https://github.com/tikv/tikv/pull/9299)

+ TiFlash

    - 增加排队处理 Coprocessor 任务的线程池以降低内存溢出几率，并增加配置项 `cop_pool_size` 和 `batch_cop_pool_size`，默认值为 `物理核数 * 2`

## 改进提升

+ TiDB

    - 重排由 `outer join` 简化的 `inner join` 顺序 [#22402](https://github.com/pingcap/tidb/pull/22402)
    - Grafana 面板支持多集群 [#22534](https://github.com/pingcap/tidb/pull/22534)
    - 为多语句问题提供替代解决方案 [#22468](https://github.com/pingcap/tidb/pull/22468)
    - 将慢查询监控区分为 `internal` 和 `general` 两类 [#22405](https://github.com/pingcap/tidb/pull/22405)
    - 为 `utf8_unicode_ci` 和 `utf8mb4_unicode_ci` 排序规则增加接口 [#22099](https://github.com/pingcap/tidb/pull/22099)

+ TiKV

    - 为 DBaaS 添加 server 信息的监控指标 [#9591](https://github.com/tikv/tikv/pull/9591)
    - Grafana dashboards 支持监控多个集群 [#9572](https://github.com/tikv/tikv/pull/9572)
    - 汇报 RocksDB 的监控指标到 TiDB [#9316](https://github.com/tikv/tikv/pull/9316)
    - 为 Coprocessor 任务记录暂停时间 [#9277](https://github.com/tikv/tikv/pull/9277)
    - 为 Load Base Split 添加 key 数量和大小的阀值 [#9354](https://github.com/tikv/tikv/pull/9354)
    - 在导入数据前检查文件是否存在 [#9544](https://github.com/tikv/tikv/pull/9544)
    - 改进 Fast Tune 面板 [#9180](https://github.com/tikv/tikv/pull/9180)

+ PD

    - Grafana dashboards 支持监控多个集群 [#3398](https://github.com/tikv/tikv/pull/3398)

+ TiFlash

    - 优化 `date_format` 函数的性能
    - 优化处理 ingest SST 时的内存开销
    - 优化 Batch Coprocessor 内部的重试逻辑以降低 Region error 的出现概率

+ Tools

    + TiCDC

        - 在 `capture` 元信息中添加版本信息和在 `changefeed` 元信息中创建该 `changefeed` 的 CLI 版本 [#1342](https://github.com/pingcap/ticdc/pull/1342)

    + TiDB Lightning

        - 并行创建数据表以提升导入速度 [#502](https://github.com/pingcap/tidb-lightning/pull/502)
        - 跳过分裂小 Region 以提升导入速度 [#524](https://github.com/pingcap/tidb-lightning/pull/524)
        - 添加导入进度条并提升恢复进度的精确度 [#506](https://github.com/pingcap/tidb-lightning/pull/506)

## Bug 修复

+ TiDB

    - 修复异常的 `unicode_ci` 常数传递 [#22614](https://github.com/pingcap/tidb/pull/22614)
    - 修复可能导致排序规则和 coercibility 错误的问题 [#22602](https://github.com/pingcap/tidb/pull/22602)
    - 修复可能导致错误排序规则结果的问题 [#22599](https://github.com/pingcap/tidb/pull/22599)
    - 修复不同排序规则的常数替换问题 [#22582](https://github.com/pingcap/tidb/pull/22582)
    - 修复 `like` 函数使用排序规则时可能返回错误结果的问题 [#22531](https://github.com/pingcap/tidb/pull/22531)
    - 修复 `least` 和 `greatest` 函数 `duration` 类型推导错误问题 [#22580](https://github.com/pingcap/tidb/pull/22580)
    - 修复 `like` 函数处理 `_` 宽字符后加 `%` 出错的问题 [#22575](https://github.com/pingcap/tidb/pull/22575)
    - 修复比较函数 `least` 和 `greatest` 类型推导错误的问题 [#22562](https://github.com/pingcap/tidb/pull/22562)
    - 修复使用 `like` 函数处理 Unicode 字符串错误的问题 [#22529](https://github.com/pingcap/tidb/pull/22529)
    - 修复点查请求无法取得 `@@tidb_snapshot` 变量中快照的问题 [#22527](https://github.com/pingcap/tidb/pull/22527)
    - 修复生成多个 join 相关 hint 可能 panic 的问题 [#22518](https://github.com/pingcap/tidb/pull/22518)
    - 修复转换字符串为 `BIT` 类型不准确的问题 [#22420](https://github.com/pingcap/tidb/pull/22420)
    - 修复插入 `tidb_rowid` 列时出现的 `index out of range` 报错问题 [#22359](https://github.com/pingcap/tidb/pull/22359)
    - 修复缓存计划被错误地使用的问题 [#22353](https://github.com/pingcap/tidb/pull/22353)
    - 修复 `WEIGHT_STRING` 函数处理过长字符串出现 panic 的问题 [#22332](https://github.com/pingcap/tidb/pull/22332)
    - 禁止参数数量不合法时使用生成列 [#22174](https://github.com/pingcap/tidb/pull/22174)
    - 在构造执行计划前正确地设置进程执行信息 [#22148](https://github.com/pingcap/tidb/pull/22148)
    - 修复 `IndexLookUp` 执行统计不准的问题 [#22136](https://github.com/pingcap/tidb/pull/22136)
    - 容器部署时为内存使用信息增加缓存 [#22116](https://github.com/pingcap/tidb/pull/22116)
    - 修复解码执行计划错误的问题 [#22022](https://github.com/pingcap/tidb/pull/22022)
    - 使用错误的窗口函数说明时提供报错 [#21976](https://github.com/pingcap/tidb/pull/21976)
    - 使用 `PREPARE` 语句嵌套 `EXECUTE`、`DEALLOCATE` 或 `PREPARE` 时报错 [#21972](https://github.com/pingcap/tidb/pull/21972)
    - 修复使用 `INSERT IGNORE` 到不存在的分区时不报错的问题 [#21971](https://github.com/pingcap/tidb/pull/21971)
    - 统一 `EXPLAIN` 和 slow log 中的执行计划编码 [#21964](https://github.com/pingcap/tidb/pull/21964)
    - 修复聚合算子下 join 出现未知列的问题 [#21957](https://github.com/pingcap/tidb/pull/21957)
    - 修复 `ceiling` 函数中类型推导错误的问题 [#21936](https://github.com/pingcap/tidb/pull/21936)
    - 修复 `Double` 列忽略精度的问题 [#21916](https://github.com/pingcap/tidb/pull/21916)
    - 修复关联聚合在子查询中被计算的问题 [#21877](https://github.com/pingcap/tidb/pull/21877)
    - 当 JSON 数据长度超过 65536 时提供报错 [#21870](https://github.com/pingcap/tidb/pull/21870)
    - 修复 `dyname` 函数和 MySQL 不兼容的问题 [#21850](https://github.com/pingcap/tidb/pull/21850)
    - 修复输入数据过长时 `to_base64` 函数返回 `NULL` 的问题 [#21813](https://github.com/pingcap/tidb/pull/21813)
    - 修复在子查询中比较多个字段失败的问题 [#21808](https://github.com/pingcap/tidb/pull/21808)
    - 修复 JSON 中比较浮点数的问题 [#21785](https://github.com/pingcap/tidb/pull/21785)
    - 修复 JSON 类型比较的问题 [#21718](https://github.com/pingcap/tidb/pull/21718)
    - 修复 `cast` 函数的 coercibility 值设置错误的问题 [#21714](https://github.com/pingcap/tidb/pull/21714)
    - 修复使用 `IF` 函数时可能出现 panic 的问题 [#21711](https://github.com/pingcap/tidb/pull/21711)
    - 修复 JSON 搜索返回 `NULL` 和 MySQL 不兼容的问题 [#21700](https://github.com/pingcap/tidb/pull/21700)
    - 修复 `ORDER BY` 和 `HAVING` 子句检查 `only_full_group_by` 模式的问题 [#21697](https://github.com/pingcap/tidb/pull/21697)
    - 修复 Day/Time 单位和 MySQL 不兼容的问题 [#21676](https://github.com/pingcap/tidb/pull/21676)
    - 修复 `LEAD` 和 `LAG` 函数默认值类型问题 [#21665](https://github.com/pingcap/tidb/pull/21665)
    - `LOAD DATA` 时执行检测以保证只能往基础表中导入数据 [#21638](https://github.com/pingcap/tidb/pull/21638)
    - 修复 `addtime` 和 `subtime` 函数处理非法参数的问题 [#21635](https://github.com/pingcap/tidb/pull/21635)
    - 将近似值的舍入规则更改为“舍入到最接近的偶数” [#21628](https://github.com/pingcap/tidb/pull/21628)
    - 修复 `WEEK()` 在被明确读取前无法识别全局变量 `default_week_format` 的问题 [#21623](https://github.com/pingcap/tidb/pull/21623)

+ TiKV

    - 修复当设置 `PROST=1` 时构建 TiKV 失败的问题 [#9604](https://github.com/tikv/tikv/pull/9604)
    - 修复不匹配的内存诊断信息 [#9589](https://github.com/tikv/tikv/pull/9589)
    - 修复在恢复 RawKV 数据时部分 key range 的 end key 的包含性问题 [#9583](https://github.com/tikv/tikv/pull/9583)
    - 修复当 TiCDC 增量扫数据时读取一个被回滚的事务的某个 key 的旧值时 TiKV 可能会 panic 的问题 [#9569](https://github.com/tikv/tikv/pull/9569)
    - 修复使用不同配置的连接拉取同一个 Region 的变更时旧值配置不匹配的问题 [#9565](https://github.com/tikv/tikv/pull/9565)
    - 修复 TiVK 运行在网络接口缺少 MAC 地址的设备上会崩溃的问题（自 v4.0.9 引入）[#9516](https://github.com/tikv/tikv/pull/9516)
    - 修复 TiKV 在备份大 Region 时会内存溢出的问题 [#9448](https://github.com/tikv/tikv/pull/9448)
    - 修复 `region-split-check-diff` 无法自定义配置的问题 [#9530](https://github.com/tikv/tikv/pull/9530)
    - 修复系统时间回退时 TiKV 会 panic 的问题 [#9542](https://github.com/tikv/tikv/pull/9542)

+ PD

    - 修复成员健康的监控显示不正确的问题 [#3368](https://github.com/pingcap/pd/pull/3368)
    - 禁止有副本的不正常 tombstone store 被清除 [#3352](https://github.com/pingcap/pd/pull/3352)
    - 修复 store limit 无法持久化的问题 [#3403](https://github.com/pingcap/pd/pull/3403)
    - 调整 `scatter range schedler` 的 limit 限制 [#3401](https://github.com/pingcap/pd/pull/3401)

+ TiFlash

    - 修复 Decimal 类型的 `min`/`max` 计算结果错误的问题
    - 修复读取数据时有可能导致 crash 的问题
    - 修复 DDL 操作后写入的数据可能会在 compaction 后丢失的问题
    - 修复 Coprocessor 中错误解析 Decimal 常量的问题
    - 修复 Learner Read 过程中可能导致 crash 的问题
    - 修复 TiFlash 中除以 `0` 或 `NULL` 的行为与 TiDB 不一致的问题

+ Tools

    + TiCDC

        - 修复 TiCDC 服务在同时发生 `ErrTaskStatusNotExists` 和 `capture` 会话关闭的情况下的非预期的退出的问题 [#1240](https://github.com/pingcap/ticdc/pull/1240)
        - 修复 `changefeed` 之间不同 Old Value 设置会互相影响的问题 [#1347](https://github.com/pingcap/ticdc/pull/1347)
        - 修复 TiCDC 服务在遇见错误的 `sort-engine` 参数时卡住的问题 [#1309](https://github.com/pingcap/ticdc/pull/1309)
        - 修复在非 Owner 节点上获取 debug 信息退出的问题 [#1349](https://github.com/pingcap/ticdc/pull/1349)
        - 修复 `ticdc_processor_num_of_tables` 和 `ticdc_processor_table_resolved_ts` 两个监控指标在增删数据表时没有被正确更新的问题 [#1351](https://github.com/pingcap/ticdc/pull/1351)
        - 修复 Processor 在添加同步数据表时退出而造成的潜在的数据丢失问题 [#1363](https://github.com/pingcap/ticdc/pull/1363)
        - 修复 Owner 在数据表迁移期间造成非正常状态的 TiCDC 服务退出的问题 [#1352](https://github.com/pingcap/ticdc/pull/1352)
        - 修复 TiCDC 服务在丢失 service GC safepoint 时没有及时退出的问题 [#1367](https://github.com/pingcap/ticdc/pull/1367)
        - 修复 KV client 可能跳过创建 event feed 的问题 [#1336](https://github.com/pingcap/ticdc/pull/1336)
        - 修复同步事务到下游时事务原子性被破坏的问题 [#1375](https://github.com/pingcap/ticdc/pull/1375)

    + Backup & Restore (BR)

        - 修复恢复备份后 TiKV 可能产生大 Region 的问题 [#702](https://github.com/pingcap/br/pull/702)
        - 修复在没有 Auto ID 的数据表上恢复 Auto ID 的问题 [#720](https://github.com/pingcap/br/pull/720)

    + TiDB Lightning

        - 修复使用 TiDB-backend 时可能触发 `column count mismatch` 的问题 [#535](https://github.com/pingcap/tidb-lightning/pull/535)
        - 修复 TiDB-backend 在导入数据源 column 个数和数据表 column 个数不匹配时非预期退出的问题 [#528](https://github.com/pingcap/tidb-lightning/pull/528)
        - 修复导入期间 TiKV 可能发生的非预期退出的问题 [#554](https://github.com/pingcap/tidb-lightning/pull/554)
