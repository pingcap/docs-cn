---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

发版日期：2021 年 3 月 31 日

TiDB 版本：4.0.12

## 新功能

+ TiFlash

    - 新增工具用于检测当前 `tiflash replica` 的实际状态

## 改进提升

+ TiDB

    - 优化 explain 中 batch cop 的信息展示 [#23164](https://github.com/pingcap/tidb/pull/23164)
    - 为在 explain 语句中不能下推的表达式增加 warning 信息 [#23020](https://github.com/pingcap/tidb/pull/23020)
    - 调整 DDL 包中部分 Execute/ExecRestricted 使用为 ExecuteInternal (2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    - 调整 DDL 包中部分 Execute/ExecRestricted 使用为 ExecuteInternal (1) [#22929](https://github.com/pingcap/tidb/pull/22929)
    - 添加 optimization-time 和 wait-TS-time 到慢日志中 [#22918](https://github.com/pingcap/tidb/pull/22918)
    - 支持从 infoschema.partitions 表中查询 partition_id [#22489](https://github.com/pingcap/tidb/pull/22489)
    - 支持 'last_plan_from_binding' 以帮助知道 SQL 计划是否来自于 binding [#21430](https://github.com/pingcap/tidb/pull/21430)
    - 支持在没有 pre-split 选项时也能执行 truncate 表操作 Scattering truncated tables without pre-split option. [#22872](https://github.com/pingcap/tidb/pull/22872)
    - 为 str_to_date 支持三种新的符号 [#22812](https://github.com/pingcap/tidb/pull/22812)
    - 在 metircs 监控中记录 prepare 执行内存 OOM 问题失败 [#22672](https://github.com/pingcap/tidb/pull/22672)
    - 当 tidb_snapshot 被设置时 prepare 语句执行不进行错误报告 [#22641](https://github.com/pingcap/tidb/pull/22641)

+ TiKV

    - Pd_client：禁止短时间内大量重连现象 [#9879](https://github.com/tikv/tikv/pull/9879)
    - 对于多 tombstones 场景下的写操作进行优化 [#9729](https://github.com/tikv/tikv/pull/9729)
    - 将 `leader-transfer-max-log-lag`默认值改为128，以增加切主的成功率 [#9605](https://github.com/tikv/tikv/pull/9605)

+ TiFlash

    - 优化配置文件并删除无用项
    - 减小 TiFlash 二进制文件大小
    - 使用自适应的 GC 策略以减少内存使用

+ Tools

    + TiCDC

        - 在启动暂停同步时间超过 1 天的任务时需要二次确认 [#1497](https://github.com/pingcap/ticdc/pull/1497)

    + Backup & Restore (BR)

        - 记录 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量 [#827](https://github.com/pingcap/br/pull/827)
        - 提升多表场景下的备份性能 [#745](https://github.com/pingcap/br/pull/745)
        - 在 service safe point 检查失败时汇报错误 [#826](https://github.com/pingcap/br/pull/826)
        - 在 backupmeta 中记录集群版本和 BR 版本 [#803](https://github.com/pingcap/br/pull/803)
        - 重试外部存储错误以便提高备份成功率 [#851](https://github.com/pingcap/br/pull/851)
        - 减少 BR 备份的内存使用 [#886](https://github.com/pingcap/br/pull/886)

    + TiDB Lightning

        - 检查 TiDB 版本以防止未知错误 [#787](https://github.com/pingcap/br/pull/787)
        - 在遇到 cancel 错误时及时退出 [#867](https://github.com/pingcap/br/pull/867)
        - 添加 `tikv-importer.engine-mem-cache-size` 和 `tikv-importer.local-writer-mem-cache-size` 参数以便调整内存占用和性能之间平衡. [#866](https://github.com/pingcap/br/pull/866)
        - Local backend 并发运行 batch split region 已提高导入速度 [#868](https://github.com/pingcap/br/pull/868)
        - 从 S3 导入数据时，Lightning 不在要求 s3:ListBucket 权限 [#919](https://github.com/pingcap/br/pull/919)
        - 从 checkpoint 恢复时, Lightning 会继续使用之前的导入引擎 [#924](https://github.com/pingcap/br/pull/924)

## Bug 修复

+ TiDB

    - 修复当变量为 16 进制字面量时 get 表达式出错问题 [#23372](https://github.com/pingcap/tidb/pull/23372)
    - 修复生成 enum 和 set 类型的快速执行计划时使用了错误 collation 的问题 [#23292](https://github.com/pingcap/tidb/pull/23292)
    - 修复 nullif 和 is-null 表达式使用时可能出现结果错误的问题 [#23279](https://github.com/pingcap/tidb/pull/23279)
    - 修复自动搜集统计信息在规定时间窗口外被触发的问题 [#23219](https://github.com/pingcap/tidb/pull/23219)
    - 修复 point-get 计划中 cast 函数可能忽略错误的问题 [#23211](https://github.com/pingcap/tidb/pull/23211)
    - 修复 CurrentDB 为空时 SPM 可能不生效的问题 [#23209](https://github.com/pingcap/tidb/pull/23209)
    - 修复 IndexMerge 执行计划中可能出现错误过滤条件的问题 [#23165](https://github.com/pingcap/tidb/pull/23165)
    - 修复 null 常量的返回类型中可能出现 NotNullFlag 的问题 [#23135](https://github.com/pingcap/tidb/pull/23135)
    - 修复 text 类型可能遗漏处理 collation 的问题 [#23092](https://github.com/pingcap/tidb/pull/23092)
    - 修复 range 分区表处理 IN 表达式可能出错的问题 [#23074](https://github.com/pingcap/tidb/pull/23074)
    - 修复将 TiKV 标记为 Tombstone 后在相同地址和端口启动不同 StoreID 的新 TiKV 持续返回 StoreNotMatch 的问题 [#23071](https://github.com/pingcap/tidb/pull/23071)
    - int 类型为 null 且和 year 进行比较时不进行类型调整 [#22844](https://github.com/pingcap/tidb/pull/22844)
    - 修复当表含有 auto_random 列 load data 时失去连接的问题 [#22736](https://github.com/pingcap/tidb/pull/22736)
    - 修复取消 DDL 操作 panic 时可能阻塞其他 DDL 操作的问题 [#23297](https://github.com/pingcap/tidb/pull/23297)
    - 修复进行 null 和 year 比较时可能生成错误 key range 的问题 [#23104](https://github.com/pingcap/tidb/pull/23104)
    - 修复创建 view 成功但是使用时可能失败的问题 [#23083](https://github.com/pingcap/tidb/pull/23083)

+ TiKV

    - 解决 `IN` 表达式没有正确处理有符号、无符号整型数的问题 [#9850](https://github.com/tikv/tikv/pull/9850)
    - 解决 ingest 操作不可重入问题 [#9779](https://github.com/tikv/tikv/pull/9779)
    - 解决 TiKV 在处理 Json 向 String 转换时空格缺失的问题 [#9666](https://github.com/tikv/tikv/pull/9666)

+ TiFlash

    - 修复当 `binary` 列的默认值包含前后 `\0` 字节时查询结果错误的问题
    - 修复当数据库名称中包含特殊字符时无法同步数据的问题
    - 修复 `IN` 表达式中出现 `Decimal` 列时查询结果错误的问题
    - 修复 Grafana 中已打开文件数指标过高的问题
    - 修复当表达式中包含 `Timestamp` 类型时查询结果错误的问题
    - 修复处理 `FROM_UNIXTIME` 表达式时可能发生崩溃的问题
    - 修复字符串转换为整数结果不正确的问题
    - 修复 `like` 表达式可能返回错误结果的问题

+ Tools

    + TiCDC

        - 解决 resolved ts 时间乱序的问题 [#1464](https://github.com/pingcap/ticdc/pull/1464)
        - 解决由于网络不稳定而导致的表调度出错引发的数据丢失问题 [#1508](https://github.com/pingcap/ticdc/pull/1508)

    + Backup & Restore (BR)

        - 解决 WalkDir 在 target 为 bucket name 的时候无返回值的问题 [#773](https://github.com/pingcap/br/pull/773)
        - 解决 status 端口无 TLS 的问题 [#839](https://github.com/pingcap/br/pull/839)

    + TiDB Lightning

        - 解决 importer 可能忽略文件已存在的错误 [#848](https://github.com/pingcap/br/pull/848)
        - 解决 Lightning 可能使用错误的时间戳而读到错误数据的问题 [#850](https://github.com/pingcap/br/pull/850)
        - 解决 Lightning 非预期退出时可能造成 checkpoint 损坏的问题 [#889](https://github.com/pingcap/br/pull/889)
        - 解决由于忽略 cancel 错误而可能导致的数据错误的问题 [#874](https://github.com/pingcap/br/pull/874)
