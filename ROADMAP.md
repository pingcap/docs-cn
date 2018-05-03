# TiDB 路线图

## TiDB：

- [ ] 优化器
  - [ ] 重构 Ranger
  - [ ] 统计信息优化
  - [ ] 代价模型优化
- [ ] 执行引擎
  - [ ] 算子并行化
  - [ ] Compact Row Format，节省内存占用
  - [ ] File Sort
- [ ] 支持 View
- [ ] 支持窗口函数
- [ ] 支持 Common Table Expression
- [ ] 支持分区表
- [ ] Hash 时间索引，解决写入热点 Region 问题
- [ ] 逆序索引
- [ ] 聚簇索引
- [ ] DDL 改进
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
- [ ] DAG 接口接入（废除 Select 接口）
- [ ] Index Join 和并行 merge join
- [ ] Data Federation（桥接其他数据源，最好能和社区同步，这个接进来可以比较好扩展 Usecase，如果再做一个 InputFormat 适配就可以接 Hive 和 Presto 这些 Hadoop 上的数仓）

## SRE&Tools:

- [ ] On-Premise 版本集成部署 (K8s based)
- [ ] On-Premise 版本 Dashboard UI
- [ ] 集群备份和恢复工具（结合物理备份）
- [ ] 数据迁移工具（Wormhole 二期）
- [ ] 安全与系统诊断
