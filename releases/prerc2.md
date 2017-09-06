---
title: TiDB RC2 Preview Release
category: Releases
---

# TiDB RC2 Preview Release

1 月 26 日，分布式关系型数据库 TiDB 发布了 RC2 预览版

## TiKV

+ 支持更多下推操作
    - If
    - IsNull
    - IfNull
    - NullIf
    - Raft 支持 PreVote 
+ 增加最大 Raft Log 的限制
+ Scheduler 同时只允许一个 GC 操作
+ 加速 Split 之后新 Region 快速选举
+ 完善 tikv-ctl 工具
+ 优化事务性能，并修复潜在问题
+ 修复 Bug，加入更多 Metrics

## PD

+ pd-ctl 功能完善
    - 添加删除 PD
    - 通过 Key 获取 Region 信息
+ 支持 Label 对副本进行 Localtion 调度
+ 修复 Bug，加入更多统计

## TiDB：

+ SQL 查询优化器
    - 统计信息收集
    - 关联子查询优化
    - 优化 CBO 框架
    - 通过 Unique Key 信息消除聚合
    - 重构 Expression
    - Distinct 转换为 GroupBy
+ 部分支持权限管理（RC2提供完整支持）
+ 新增大量 MySQL 内建函数
+ 支持修改表名
+ 限制单个事务大小，避免大事务阻塞整个集群
+ Load Data 过程中对数据进行自动拆分
+ 修复 Bug

## 工具：

+ 完善 Metrics，更方便监测系统状态以及定位问题
+ Syncer 支持黑名单和白名单
+ 一键部署工具重构：智能检测部署环境检查更智能，支持扩容缩容
+ TiDB Binlog 组件性能优化，同步延迟从分钟级别，降低到秒级，支持多线程同步