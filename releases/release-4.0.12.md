---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

发版日期：2021 年 3 月 31 日

TiDB 版本：4.0.12

## 新功能

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
