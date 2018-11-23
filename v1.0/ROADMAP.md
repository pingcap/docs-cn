## TiDB：

- [ ] 优化器
  - [ ] 重构 Ranger
  - [ ] 统计信息优化
  - [ ] 代价模型优化
- [ ] 执行引擎
  - [ ] 算子并行化
  - [ ] Compact Row Foramt，节省内存占用
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
  - [ ] Region 合并
  - [ ] Local read thread
  - [ ] 多线程 Raftstore
  - [ ] None voter
  - [ ] Pre-vote
- [ ] RocksDB
  - [ ] 使用 DeleteRange 特性
- [ ] Transaction
  - [ ] 提升冲突严重的场景下 Transaction 的性能
- [ ] Coprocessor
  - [ ] 支持 Streaming 接口
- [ ] Tool
  - [ ] 分布式数据导入
  - [ ] 分布式数据导出
  - [ ] 灾难恢复
- [ ] 流控和降级处理

## PD:

- [ ] Namespace 完善
  - [ ] 不同 Namespace 或者 Table 配置不同的副本策略
- [ ] Table region 分散调度
- [ ] 调度支持优先级，更加可控
- [ ] 使用机器学习优化调度

## TiSpark:

- [ ] limit / Order下推
- [ ] DAG接口接入（废除Select接口）
- [ ] Index Join和并行merge join
- [ ] Data Federation（桥接其他数据源，最好能和社区同步，这个接进来可以比较好扩展Usecase，如果再做一个InputFormat适配就可以接Hive和Presto这些Hadoop上的数仓）

## SRE&Tools:
- [ ] On-Premise 版本集成部署 (K8s based)
- [ ] On-Premise 版本 Dashboard UI
- [ ] 集群备份和恢复工具（结合物理备份）
- [ ] 数据迁移工具（Wormhole 二期）
- [ ] 安全与系统诊断