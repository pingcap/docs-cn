---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

发版日期：2021 年 4 月 2 日

TiDB 版本：4.0.12

## 新功能

+ TiFlash

    - 新增工具用于检测当前 `tiflash replica` 的状态

## 改进提升

+ TiDB

    - 优化 `EXPLAIN` 语句在 `batch cop` 模式下的输出信息 [#23164](https://github.com/pingcap/tidb/pull/23164)
    - 在 `EXPLAIN` 语句的输出中，为无法下推到存储层的表达式增加告警信息 [#23020](https://github.com/pingcap/tidb/pull/23020)
    - 调整 DDL 包中部分 `Execute`/`ExecRestricted` 的使用为安全 API (2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    - 调整 DDL 包中部分 `Execute`/`ExecRestricted` 的使用为安全 API (1) [#22929](https://github.com/pingcap/tidb/pull/22929)
    - 添加 `optimization-time` 和 `wait-TS-time` 到慢日志中 [#22918](https://github.com/pingcap/tidb/pull/22918)
    - 支持从 `infoschema.partitions` 表中查询 `partition_id` [#22489](https://github.com/pingcap/tidb/pull/22489)
    - 添加 `last_plan_from_binding` 以帮助用户了解 SQL 执行计划是否与 binding 的 hint 相匹配 [#21430](https://github.com/pingcap/tidb/pull/21430)
    - 支持在没有 `pre-split` 选项时也能执行 `TRUNCATE` 表操作 [#22872](https://github.com/pingcap/tidb/pull/22872)
    - 为 `str_to_date` 表达式添加三种新的格式限定符 [#22812](https://github.com/pingcap/tidb/pull/22812)
    - 在 metrics 监控中记录 `PREPARE` 执行失败的问题为 `Failed Query OPM` [#22672](https://github.com/pingcap/tidb/pull/22672)
    - 当设置了 `tidb_snapshot` 时，不对 `PREPARE` 语句的执行报错 [#22641](https://github.com/pingcap/tidb/pull/22641)

+ TiKV

    - 消除短时间内大量重连接的现象 [#9879](https://github.com/tikv/tikv/pull/9879)
    - 对多 Tombstones 场景下的写操作和 Batch Get 进行优化 [#9729](https://github.com/tikv/tikv/pull/9729)
    - 将 `leader-transfer-max-log-lag` 的默认值改为 `128`，以增加切换 leader 的成功率 [#9605](https://github.com/tikv/tikv/pull/9605)

+ PD

    - 只有当 `pending-peer` 或 `down-peer` 变更时才更新 Region Cache，减少心跳更新压力 [#3471](https://github.com/pingcap/pd/pull/3471)
    - 防止 `split-cache` 中的 Region 成为合并的目标 [#3459](https://github.com/pingcap/pd/pull/3459)

+ TiFlash

    - 优化配置文件并删除无用项
    - 减小 TiFlash 二进制文件大小
    - 使用自适应的 GC 策略以减少内存使用

+ Tools

    + TiCDC

        - 若任务的暂停同步时间超过 1 天，再次启动该任务时需要二次确认 [#1497](https://github.com/pingcap/ticdc/pull/1497)
        - 为 Old Value 功能添加监控面板 [#1571](https://github.com/pingcap/ticdc/pull/1571)

    + Backup & Restore (BR)

        - 记录 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量 [#827](https://github.com/pingcap/br/pull/827)
        - 提升多表场景下的备份性能 [#745](https://github.com/pingcap/br/pull/745)
        - 在 service safe point 检查失败时报告错误 [#826](https://github.com/pingcap/br/pull/826)
        - 在 `backupmeta` 中记录集群版本和 BR 版本 [#803](https://github.com/pingcap/br/pull/803)
        - 遇到外部存储错误时，重试备份以便提高备份成功率 [#851](https://github.com/pingcap/br/pull/851)
        - 减少 BR 备份的内存使用 [#886](https://github.com/pingcap/br/pull/886)

    + TiDB Lightning

        - 运行 TiDB Lightning 前检查 TiDB 集群版本以防止未知错误 [#787](https://github.com/pingcap/br/pull/787)
        - 在遇到 cancel 错误时及时退出 [#867](https://github.com/pingcap/br/pull/867)
        - 添加 `tikv-importer.engine-mem-cache-size` 和 `tikv-importer.local-writer-mem-cache-size` 参数以便调整内存占用和性能之间的平衡 [#866](https://github.com/pingcap/br/pull/866)
        - Local-backend 并发运行 `batch split region` 以提高导入速度 [#868](https://github.com/pingcap/br/pull/868)
        - 从 S3 存储导入数据时，TiDB Lightning 不再要求 `s3:ListBucket` 权限 [#919](https://github.com/pingcap/br/pull/919)
        - 从 checkpoint 恢复时，TiDB Lightning 会继续使用之前的导入引擎 [#924](https://github.com/pingcap/br/pull/924)

## Bug 修复

+ TiDB

    - 修复当变量为十六进制字面量时，`get` 表达式出错的问题 [#23372](https://github.com/pingcap/tidb/pull/23372)
    - 修复生成 `Enum` 和 `Set` 类型的快速执行计划时使用了错误 Collation 的问题 [#23292](https://github.com/pingcap/tidb/pull/23292)
    - 修复 `nullif` 和 `is-null` 表达式一起使用时可能出现结果错误的问题 [#23279](https://github.com/pingcap/tidb/pull/23279)
    - 修复自动搜集统计信息在规定时间窗口外被触发的问题 [#23219](https://github.com/pingcap/tidb/pull/23219)
    - 修复 `point-get` 计划中 `CAST` 函数可能忽略错误的问题 [#23211](https://github.com/pingcap/tidb/pull/23211)
    - 修复 `CurrentDB` 为空时 SPM 可能不生效的问题 [#23209](https://github.com/pingcap/tidb/pull/23209)
    - 修复 IndexMerge 执行计划中可能出现错误过滤条件的问题 [#23165](https://github.com/pingcap/tidb/pull/23165)
    - 修复 `NULL` 常量的返回类型中可能出现 `NotNullFlag` 的问题 [#23135](https://github.com/pingcap/tidb/pull/23135)
    - 修复 Text 类型可能遗漏处理 Collation 的问题 [#23092](https://github.com/pingcap/tidb/pull/23092)
    - 修复 Range 分区表处理 `IN` 表达式可能出错的问题 [#23074](https://github.com/pingcap/tidb/pull/23074)
    - 修复将 TiKV 标记为 Tombstone 后，在相同地址和端口启动不同 StoreID 的新 TiKV 会持续返回 `StoreNotMatch` 的问题 [#23071](https://github.com/pingcap/tidb/pull/23071)
    - INT 类型为 `NULL` 且和 `YEAR` 进行比较时不进行类型调整 [#22844](https://github.com/pingcap/tidb/pull/22844)
    - 修复当表含有 `auto_random` 列 load data 时失去连接的问题 [#22736](https://github.com/pingcap/tidb/pull/22736)
    - 修复取消 DDL 操作 panic 时可能阻塞其他 DDL 操作的问题 [#23297](https://github.com/pingcap/tidb/pull/23297)
    - 修复进行 `NULL` 和 `YEAR` 比较时可能生成错误 key range 的问题 [#23104](https://github.com/pingcap/tidb/pull/23104)
    - 修复创建视图成功但是使用时可能失败的问题 [#23083](https://github.com/pingcap/tidb/pull/23083)

+ TiKV

    - 修复 `IN` 表达式没有正确处理有符号和无符号整型数的问题 [#9850](https://github.com/tikv/tikv/pull/9850)
    - 修复 Ingest 操作不可重入问题 [#9779](https://github.com/tikv/tikv/pull/9779)
    - 修复 TiKV 在处理 JSON 向字符串转换时空格缺失的问题 [#9666](https://github.com/tikv/tikv/pull/9666)

+ PD

    - 修复在 store 缺失 label 的情况下隔离级别错误的问题 [#3474](https://github.com/pingcap/pd/pull/3474)

+ TiFlash

    - 修复当 `binary` 列的默认值前后包含 `0` 字节时查询结果错误的问题
    - 修复当数据库名称中包含特殊字符时无法同步数据的问题
    - 修复 `IN` 表达式中出现 `Decimal` 列时查询结果错误的问题
    - 修复 Grafana 中已打开文件数指标过高的问题
    - 修复当表达式中包含 `Timestamp` 类型时查询结果错误的问题
    - 修复处理 `FROM_UNIXTIME` 表达式时可能发生的无响应的问题
    - 修复字符串转换为整数结果不正确的问题
    - 修复 `like` 表达式可能返回错误结果的问题

+ Tools

    + TiCDC

        - 修复 `resolved ts` 时间乱序的问题 [#1464](https://github.com/pingcap/ticdc/pull/1464)
        - 修复由于网络不稳定而导致的表调度出错引发的数据丢失问题 [#1508](https://github.com/pingcap/ticdc/pull/1508)
        - 修复终止 processor 时不能及时释放资源的问题 [#1547](https://github.com/pingcap/ticdc/pull/1547)
        - 修复因事务计数器未正确更新而导致下游数据库链接可能泄露的问题 [#1524](https://github.com/pingcap/ticdc/pull/1524)
        - 修复因 PD 抖动时多个 owner 共存可能导致数据表丢失的问题 [#1540](https://github.com/pingcap/ticdc/pull/1540)

    + Backup & Restore (BR)

        - 修复 `WalkDir` 在目标为 bucket name 的时候无返回值的问题 [#733](https://github.com/pingcap/br/pull/733)
        - 修复 `status` 端口无 TLS 的问题 [#839](https://github.com/pingcap/br/pull/839)

    + TiDB Lightning

        - 修复 TiKV Importer 可能忽略文件已存在的错误 [#848](https://github.com/pingcap/br/pull/848)
        - 修复 TiDB Lightning 可能使用错误的时间戳而读到错误数据的问题 [#850](https://github.com/pingcap/br/pull/850)
        - 修复 TiDB Lightning 非预期退出时可能造成 checkpoint 文件损坏的问题 [#889](https://github.com/pingcap/br/pull/889)
        - 修复由于忽略 `cancel` 错误而可能导致的数据错误的问题 [#874](https://github.com/pingcap/br/pull/874)
