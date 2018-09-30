---
title: TiDB 路线图
category: Roadmap
---

# TiDB 路线图

## TiDB：

- [ ] 优化器
    - [x] 重构 Ranger
    - [x] 代价模型优化
    - [ ] Cascades model planner
    - [ ] Join Reorder
- [ ] 统计信息
    - [x] 基于 Query Feedback 动态更新统计信息
    - [x] 自动 Analyze
    - [x] 提升 Row Count 估算精度
- [ ] 执行引擎
    - [ ] 下推 Projection 到 Coprocessor
    - [x] 优化 HashJoin 算子执行速度
    - [ ] 算子并行化
        - [x] 并行 Projection
        - [x] 并行聚合
        - [ ] 并行 Sort
    - [x] Compact Row Format，节省内存占用
    - [ ] File Sort
- [ ] View
- [ ] 窗口函数
- [ ] Common Table Expression
- [ ] 分区表
    - [x] Range 分区
    - [ ] Hash 分区
- [ ] 聚簇索引
- [ ] 新的 storage row format
- [ ] Query Ttracing
- [ ] DDL 改进
    - [x] Add Index 加速
    - [x] 并行 DDL
    - [ ] 支持锁表
    - [ ] 支持改变 column 类型
    - [ ] 支持修改主键
    - [ ] 支持一条语句中多个 DDL 操作
- [ ] 支持 `utf8_general_ci` collation

## TiKV:

- [ ] Raft
    - [x] Region 合并
    - [ ] Local read thread
    - [ ] 多线程 Raftstore
    - [x] None voter
    - [ ] Pre-vote
- [x] RocksDB
    - [x] 使用 DeleteRange 特性
- [x] Transaction
    - [x] 提升冲突严重的场景下 Transaction 的性能
- [x] Coprocessor
    - [x] 支持 Streaming 接口
- [ ] Tool
    - [x] 分布式数据导入
    - [ ] 分布式数据导出
    - [ ] 灾难恢复
- [ ] 流控和降级处理

## PD:

- [x] Namespace 完善
    - [x] 不同 Namespace 或者 Table 配置不同的副本策略
- [x] Table Region 分散调度
- [x] 调度支持优先级，更加可控
- [ ] 使用机器学习优化调度

## TiSpark:

- [ ] Limit/Order 下推
- [x] DAG 接口接入（废除 Select 接口）
- [ ] Index Join 和并行 merge join
- [ ] Data Federation（桥接其他数据源，最好能和社区同步，这个接进来可以比较好扩展 Usecase，如果再做一个 InputFormat 适配就可以接 Hive 和 Presto 这些 Hadoop 上的数仓）

## Tools:

- [x] 集群部署工具
- [X] 高性能数据导入工具
- [X] 集群备份和恢复工具 (包括全量+增量备份)
- [ ] 数据在线迁移工具 (Syncer 升级版)
- [ ] 集群诊断和分析工具
