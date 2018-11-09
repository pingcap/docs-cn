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
- [ ] Query Tracing
- [ ] DDL 改进
    - [x] Add Index 加速
    - [x] 并行 DDL
    - [ ] 支持锁表
    - [ ] 支持改变 column 类型
    - [ ] 支持修改主键
    - [ ] 支持一条语句中多个 DDL 操作
- [ ] 支持 `utf8_general_ci` collation

## TiKV：

+ Raft
    - [x] Region Merge - 合并小的 Region 以减少开销
    - [x] Local Read Thread - 把读请求放在一个单独的线程处理
    - [x] 批量 Region Split - 加速大的 Region 的分裂
    - [x] Raft Learner - 支持 Raft learner 使得成员变更过程更加平滑
    - [x] Raft Pre-voter - 支持 Raft Pre-vote 避免网络隔离带来不必要的选举
    - [ ] Joint Consensus - 安全地进行多个成员变更
    - [ ] 多线程 Raftstore - 在多个线程处理不同 Region 的 Raft 逻辑
    - [ ] 多线程 Apply Pool - 在多个线程执行不同 Region 已经提交了的命令
+ Engine
    - [ ] Titan - 把大的 key-values 从 LSM-Tree 中分离出来
    - [ ] 可拔插的 Engine 接口 - 简化接口逻辑并且提供可扩展性
+ Storage
    - [ ] 在 scheduler 里做流控提前避免 write stall
+ Transaction
    - [x] 优化事务冲突
    - [ ] 分布式 GC - 把 MVCC 垃圾回收的逻辑分布到 TiKV 控制
+ Coprocessor
    - [x] Streaming - 把大的数据集切成小块返回以减少内存消耗
    - [ ] Chunk Execution - 按 chunk 的方式来处理数据以提高性能
    - [ ] 请求跟踪 - 提供单个请求执行的详细信息
+ Tools
    - [x] TiKV Importer - 通过直接导入 SST 文件的方式加速数据导入
+ Client
    - [ ] 提供 Rust 版本的 TiKV client
    - [ ] gRPC 消息批量化 - 减少消息交互的开销

## PD：

- [x] Namespace 完善
    - [x] 不同 Namespace 或者 Table 配置不同的副本策略
- [x] Table Region 分散调度
- [x] 调度支持优先级，更加可控
- [ ] 使用机器学习优化调度
- [ ] 优化 Region 元信息存储 - 把元信息存储在一个独立的存储引擎里

## TiSpark：

- [ ] Limit/Order 下推
- [x] DAG 接口接入（废除 Select 接口）
- [ ] Index Join 和并行 merge join
- [ ] Data Federation（桥接其他数据源，最好能和社区同步，这个接进来可以比较好扩展 Usecase，如果再做一个 InputFormat 适配就可以接 Hive 和 Presto 这些 Hadoop 上的数仓）

## Tools:

- [x] 集群部署工具
- [X] 高性能数据导入工具（lightning）
- [X] 集群备份和恢复工具（包括全量+增量备份，mydumper + drainer/reparo）
- [X] 改进 TiDB-Binlog 架构
- [ ] 数据在线迁移工具（Syncer 升级版）
- [ ] 集群诊断和分析工具
