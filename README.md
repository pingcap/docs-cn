# TiDB 中文技术文档

## 目录

+ [TiDB 简介与整体架构](overview.md)
  - [TiDB 简介](overview.md#tidb-简介)
  - [TiDB 整体架构](overview.md#tidb-整体架构)
+ [TiDB 快速入门指南](QUICKSTART.md)
  - [关于 TiDB](QUICKSTART.md#关于-tidb)
  - [关于本指南](QUICKSTART.md#关于本指南)
  - [集群部署](QUICKSTART.md#tidb-集群部署)
  - [基本操作](QUICKSTART.md#tidb-基本操作)
  - [集群监控](QUICKSTART.md#tidb-集群监控)
  - [扩容缩容](QUICKSTART.md#tidb-集群扩容缩容方案)
  - [集群销毁](QUICKSTART.md#集群销毁)
+ TiDB 运维文档
  - [软硬件环境需求](op-guide/recommendation.md)
  + 部署集群
    - [Ansible 部署方案 (强烈推荐)](op-guide/ansible-deployment.md)
    - [Docker 部署方案](op-guide/docker-deployment.md)
    - [跨机房部署方案](op-guide/location-awareness.md)
  + 配置集群
    - [配置参数](op-guide/configuration.md)
  + 监控集群
    - [整体监控框架概述](op-guide/monitor-overview.md)
    - [重要监控指标详解](op-guide/dashboard-overview-info.md)
    - [组件状态 API & 监控](op-guide/monitor.md)
  - [扩容缩容](op-guide/horizontal-scale.md)
  + 升级
    - [使用 Ansible 升级](op-guide/ansible-deployment.md)
  + 性能调优
    - [TiKV 性能参数调优](op-guide/tune-tikv.md)
  + 备份与迁移
    - [备份与恢复](op-guide/backup-restore.md)
    + [数据迁移](op-guide/migration.md)
      - [全量导入](op-guide/migration.md#使用-mydumperloader-全量导入数据)
      - [增量导入](op-guide/migration.md#使用-syncer-增量导入数据)
  + 手动运维
    - [Binary 部署方案](op-guide/binary-deployment.md)
+ [TiDB 用户文档](sql/README.md)
  + TiDB 数据库管理
    - [TiDB 服务器启动参数](sql/server-command-option.md)
    - [TiDB 专用系统变量和语法](sql/tidb-specific.md)
  + TiDB 安全
    - [TiDB 访问权限管理](sql/privilege.md)
  + 优化
    - [理解 TiDB 执行计划](sql/understanding-the-query-execution-plan.md)
  + [数据类型](sql/datatype.md)
    - [数值类型](sql/datatype.md#数值类型)
    - [字符串类型](sql/datatype.md#字符串类型)
    - [数据类型默认值](sql/datatype.md#数据类型的默认值)
  + 函数与操作符
    - [操作符](sql/operators.md)
    - [日期和时间函数](sql/date-and-time-functions.md)
    - [位函数和操作符](sql/bit-functions-and-operators.md)
    - [Cast 函数和操作符](sql/cast-functions-and-operators.md)
    - [信息函数](sql/information-functions.md)
  + SQL 语句语法
    - [数据定义语句(DDL)](sql/ddl.md)
    - [数据操作语句(DML)](sql/dml.md)
    - [与 MySQL 兼容性对比](sql/mysql-compatibility.md)
    - [TiDB SQL 语法图](https://pingcap.github.io/sqlgram/)
  - [文档型数据库](sql/json-functions-generated-column.md)
+ 高级功能
  - [历史数据回溯](op-guide/history-read.md)
+ 工具
  - [Loader 使用文档](tools/loader.md)
  - [Syncer 使用文档](tools/syncer.md)
  - [TiDB-binlog 使用文档](op-guide/tidb-binlog.md)
  - [PD 命令行工具](op-guide/pd-control.md)
+ TiSpark 文档
  - [TiSpark 快速入门指南](op-guide/tispark-quick-start-guide.md)
  - [TiSpark 用户指南](op-guide/tispark-user-guide.md)
- [常见问题与解答](FAQ.md)
- [故障诊断](trouble-shooting.md)
- [最佳实践](https://pingcap.com/blog-TiDB-Best-Practice-zh)
+ 版本发布声明
  - [Pre-GA](releases/prega.md)
  - [RC4](releases/rc4.md)
  - [RC3](releases/rc3.md)
  - [RC2](releases/rc2.md)
  - [RC1](releases/rc1.md)
+ 更多资源
  - [PingCAP 团队技术博客](https://pingcap.com/bloglist-zh.html)

## TiDB 简介

TiDB 是 PingCAP 公司基于 Google [Spanner](http://research.google.com/archive/spanner.html) / [F1](http://research.google.com/pubs/pub41344.html) 论文实现的开源分布式 NewSQL 数据库。

TiDB 具备如下 NewSQL 核心特性：

* SQL支持 （TiDB 是 MySQL 兼容的）
* 水平线性弹性扩展
* 分布式事务
* 跨数据中心数据强一致性保证
* 故障自恢复的高可用

TiDB 的设计目标是 100% 的 OLTP 场景和 80% 的 OLAP 场景。

TiDB 对业务没有任何侵入性，能优雅的替换传统的数据库中间件、数据库分库分表等 Sharding 方案。同时它也让开发运维人员不用关注数据库 Scale 的细节问题，专注于业务开发，极大的提升研发的生产力。

## TiDB 整体架构

要深入了解 TiDB 的水平扩展和高可用特点，首先需要了解 TiDB 的整体架构。

![TiDB Architecture](media/tidb-architecture.png)

TiDB 集群主要分为三个组件：

### TiDB Server

TiDB Server 负责接收 SQL 请求，处理 SQL 相关的逻辑，并通过 PD 找到存储计算所需数据的 TiKV 地址，与 TiKV 交互获取数据，最终返回结果。
TiDB Server 是无状态的，其本身并不存储数据，只负责计算，可以无限水平扩展，可以通过负载均衡组件（如 LVS、HAProxy 或 F5）对外提供统一的接入地址。

### PD Server

Placement Driver (简称 PD) 是整个集群的管理模块，其主要工作有三个： 一是存储集群的元信息（某个 Key 存储在哪个 TiKV 节点）；二是对 TiKV 集群进行调度和负载均衡（如数据的迁移、Raft group leader 的迁移等）；三是分配全局唯一且递增的事务 ID。

PD 是一个集群，需要部署奇数个节点，一般线上推荐至少部署 3 个节点。

### TiKV Server

TiKV Server 负责存储数据，从外部看 TiKV 是一个分布式的提供事务的 Key-Value 存储引擎。存储数据的基本单位是 Region，每个 Region 负责存储一个 Key Range （从 StartKey 到 EndKey 的左闭右开区间）的数据，每个 TiKV 节点会负责多个 Region 。TiKV 使用 Raft 协议做复制，保持数据的一致性和容灾。副本以 Region 为单位进行管理，不同节点上的多个 Region 构成一个 Raft Group，互为副本。数据在多个 TiKV 之间的负载均衡由 PD 调度，这里也是以 Region 为单位进行调度。

## 核心特性

### 水平扩展

无限水平扩展是 TiDB 的一大特点，这里说的水平扩展包括两方面：计算能力和存储能力。TiDB Server 负责处理 SQL 请求，随着业务的增长，可以简单的添加 TiDB Server 节点，提高整体的处理能力，提供更高的吞吐。TiKV 负责存储数据，随着数据量的增长，可以部署更多的 TiKV Server 节点解决数据 Scale 的问题。PD 会在 TiKV 节点之间以 Region 为单位做调度，将部分数据迁移到新加的节点上。所以在业务的早期，可以只部署少量的服务实例（推荐至少部署 3 个 TiKV， 3 个 PD，2 个 TiDB），随着业务量的增长，按照需求添加 TiKV 或者 TiDB 实例。

### 高可用

高可用是 TiDB 的另一大特点，TiDB/TiKV/PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。下面分别说明这三个组件的可用性、单个实例失效后的后果以及如何恢复。

+   TiDB

    TiDB 是无状态的，推荐至少部署两个实例，前端通过负载均衡组件对外提供服务。当单个实例失效时，会影响正在这个实例上进行的 Session，从应用的角度看，会出现单次请求失败的情况，重新连接后即可继续获得服务。单个实例失效后，可以重启这个实例或者部署一个新的实例。

+   PD

    PD 是一个集群，通过 Raft 协议保持数据的一致性，单个实例失效时，如果这个实例不是 Raft 的 leader，那么服务完全不受影响；如果这个实例是 Raft 的 leader，会重新选出新的 Raft leader，自动恢复服务。PD 在选举的过程中无法对外提供服务，这个时间大约是3秒钟。推荐至少部署三个 PD 实例，单个实例失效后，重启这个实例或者添加新的实例。

+   TiKV

    TiKV 是一个集群，通过 Raft 协议保持数据的一致性（副本数量可配置，默认保存三副本），并通过 PD 做负载均衡调度。单个节点失效时，会影响这个节点上存储的所有 Region。对于 Region 中的 Leader 节点，会中断服务，等待重新选举；对于 Region 中的 Follower 节点，不会影响服务。当某个 TiKV 节点失效，并且在一段时间内（默认 10 分钟）无法恢复，PD 会将其上的数据迁移到其他的 TiKV 节点上。
