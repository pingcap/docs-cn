---
title: TiDB 6.5.7 Release Notes
summary: 了解 TiDB 6.5.7 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.7 Release Notes

发版日期：2024 年 1 月 8 日

TiDB 版本：6.5.7

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup)

## 兼容性变更

+ 新增 TiDB 配置项 [`performance.force-init-stats`](https://docs.pingcap.com/zh/tidb/v6.5/tidb-configuration-file#force-init-stats-从-v657-版本开始引入)，用于控制 TiDB 启动时是否在统计信息初始化完成后再对外提供服务 [#43385](https://github.com/pingcap/tidb/issues/43385) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
+ 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8568](https://github.com/pingcap/tiflash/issues/8568) @[xzhangxian1008](https://github.com/xzhangxian1008)

## 改进提升

+ TiDB

    - 优化 `ANALYZE` 分区表的内存使用和性能 [#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @[hawkingrei](https://github.com/hawkingrei)
    - 支持以 Optimizer Fix Controls 的方式让 Plan Cache 对在物理优化阶段形成的 `PointGet` 计划进行缓存 [#44830](https://github.com/pingcap/tidb/issues/44830) @[qw4990](https://github.com/qw4990)
    - 增强特定情况下 `OUTER JOIN` 转 `INNER JOIN` 的能力 [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)

+ TiFlash

    - 降低磁盘性能抖动对读取延迟的影响 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - 解决了基于 EBS 的快照备份与 TiDB Lightning 导入的兼容性问题 [#46850](https://github.com/pingcap/tidb/issues/46850) @[YuJuncen](https://github.com/YuJuncen)
        - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 当下游为 Kafka 时，topic 表达式中允许 `schema` 为可选项，并且支持直接指定 topic 名 [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)

## 错误修复

+ TiDB

    - 修复在短时间内执行大量 `CREATE TABLE` 语句时，TiDB 可能不会同步创建这些表的新统计信息元信息，导致后续的查询估算无法获取准确行数信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复 TiDB server 在使用企业插件审计日志时可能占用大量资源的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 `ErrLoadDataInvalidURI`（无效的 S3 URI 错误）报错中的信息内容 [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - 修复 `tidb_server_memory_limit` 导致内存长期压力较高时，TiDB CPU 利用率过高的问题 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复当内存使用超限时包含公共表表达式 (CTE) 的查询非预期卡住的问题 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - 修复某些情况下相同的查询计划拥有不同的 `PLAN_DIGEST` 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - 修复当 `tidb_max_chunk_size` 值较小时，包含 CTE 的查询出现 `runtime error: index out of range [32] with length 32` 错误的问题 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiDB server 在优雅关闭 (graceful shutdown) 时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - 修复导入从早期版本的 TiDB 导出的统计信息时，可能出现数据错误的问题 [#42931](https://github.com/pingcap/tidb/issues/42931) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复构造统计信息时因为 Golang 隐式转换算法导致统计信息误差过大的问题 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - 修复特定情况下优化器将 TiFlash 选择路径错误转化为 DUAL Table 的问题 [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - 修复在解析 `ENUM` 或 `SET` 类型的非法值时会导致 SQL 语句报错的问题 [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - 修复包含递归 (`WITH RECURSIVE`) CTE 的 `UPDATE` 或 `DELETE` 语句可能会产生错误结果的问题 [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - 修复数据中包含后导空格时，在 `LIKE` 中使用 `_` 通配符可能会导致查询结果出错的问题 [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - 修复包含 IndexHashJoin 算子的查询由于内存超过 `tidb_mem_quota_query` 而卡住的问题 [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复在嵌套的 `UNION` 查询中 `LIMIT` 和 `OPRDERBY` 可能无效的问题 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - 修复在非严格模式下 (`sql_mode = ''`)，`INSERT` 过程中产生截断仍然会报错的问题 [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB panic 并报错 `invalid memory address or nil pointer dereference` 的问题 [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 CTE 查询在重试过程中可能会报错 `type assertion for CTEStorageMap failed` 的问题 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在某些时区下夏令时显示有误的问题 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - 修复有依赖关系的两个 DDL 任务的完成时间顺序不正确的问题 [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)

+ TiKV

    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - 修复跟踪大型事务时，Stale Read 中的 Resolved TS 可能导致 TiKV OOM 的问题 [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - 修复 TiKV 由于无法 append Raft log 导致报错 `ServerIsBusy` [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - 修复 Placement Rules in SQL 设置的 `location-labels` 在特定条件下不按预期调度的问题 [#6637](https://github.com/tikv/pd/issues/6637) @[rleungx](https://github.com/rleungx)
    - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当查询遇到内存限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - 修复 Grafana 中部分面板的最大分位数耗时显示不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复数据同步到下游 MySQL 时可能出现 `checkpoint-ts` 卡住的问题 [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)
        - 修复 `kv-client` 初始化过程中可能出现数据竞争的问题 [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
