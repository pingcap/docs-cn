---
title: TiDB Roadmap
category: Roadmap
aliases: ['/docs-cn/ROADMAP/','/docs-cn/roadmap/']
---

# TiDB V4.0 Roadmap

## TiDB

### TiDB

#### 功能

* 支持 TiFlash 存储引擎
* Optimizer Trace
* Multi-Column Statistics
* Normal CM-Sketch with TOPN Statistics
* 完善 Plan Cache 功能
* 简单的自适应 SQL 引擎
* SQL Tuning Advisor
* SQL Plan Management

#### 性能

* 提升 load CSV/data 性能
* 提升 Prepare 语句性能
* Generated Column 支持 Index
* 优化 SQL 引擎部份算子
    + 提升通过索引回表查询的性能
    + Index Join 拆分为 Index Merge Join 和 Index Hash Join
    + Radix Hash Join
    + Index Merge
    + Parallel Stream Aggregate
    + Parallel Merge Sort
    + Parallel Merge Join
    + Full Vectorized Expression Evaluation
* Indexes on Expressions
* Multi-Index Scan
* Join，Aggregate，Sort 算子支持外部存储
* 优化执行引擎并发模型
* 支持新 Cascades 优化器，支持 Cascades Planner，扩大优化器的搜索空间

#### 易用性

* 完善 Optimizer Hint 功能
* 快速修复数据库或者表元信息及数据
* 动态修改配置项
* 空闲连接自动断开
* 完善支持 MySQL 5.7 DDL 语句
* 重构日志内容
* 支持 admin checksum from … to … 校验数据完整性
* 标准 SQL 查询 DDL 历史记录
* 标准 SQL 管理 Binlog
* 标准 SQL 管理集群
* 多个 Ctrl 工具合并一个工具

#### 高可用

* Binlog 支持服务高可用

### TiKV

#### 功能

* 集群规模最大支持 200+节点
* 全量物理备份恢复
* 动态 Split,Merge 热点 Region
* 精细的内存控制
* Raft
    + Joint consensus
    + 只读副本
* 事务
    + 悲观锁 GA
    + 事务内不限制语句数量
    + 支持 10GB 事务

#### 性能

* 提升 Scan 性能
* 动态扩展工作线程数量
* 弹性扩展只读副本
* 优化调度系统确保 QPS 不抖动

#### 易用性

* 重构日志内容

### TiFlash

#### 功能

* 列式存储
* 通过 Raft learner 从 TiKV 同步数据
* snapshot read

### TiSpark

#### 功能

* 支持 batch write
* 接入 TiFlash

## Data Migration

### 功能

* 完善前向检查
* 可视化管理同步规则
* 可视化管理同步任务

### 易用性

* Ctrl 工具集成数据一致性校验功能
* Ctrl 工具输出任务详细信息
* 重构日志格式及内容

### 高可用

* 支持服务高可用

## TiDB Toolkit

### 功能

* Loader 集成到 TiDB
* TiDB Lightning 集成到 TiDB

### 性能

* TiDB Lightning 支持并行导入
* TiDB Lightning 优化导入回放路径

# TiDB 未来规划

## TiDB

### TiDB

#### 功能

* Common Table Expression
* Invisible Index
* 支持修改列类型
* 分区表支持二级分区
* Table Partition 与 普通表相互转换
* 视图支持写入及更新
* Mutil-Schema Change
* 按 Table 配置副本数及分布策略
* 精细的 QoS 控制
* 闪回到任意时间点

#### 性能

* Coprocessor Cache
* 新 Row 存储格式
* Distributed Execution Engine

#### 易用性

* 全链路 Trace 工具
* Help 信息补齐

#### 安全

* 列级别权限

#### 高可靠用

* Binlog 支持数据高可靠

### TiKV

#### 功能

* 增量物理备份恢复
* 闪回到任意时间点
* 分级存储
* 精细的 QoS 控制
* 按 Region 配置副本数及分布策
* Raft
    + 链式复制数据
    + Witness Role
* 存储引擎
    + RocksDB Gaurd，compaction 按特定逻辑切分 SST
    + 冷热数据分离

#### 性能

* 提升物理备份性能
* 提升增量物理备份性能
* 1PC
* 支持 Storage Class Memory 硬件
* 新 Raft 引擎

## Data Migration

### 功能

* 下游支持 Oracle

### 高可靠

* 支持数据高可靠
