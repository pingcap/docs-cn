# TiDB 中文技术文档

<!-- markdownlint-disable MD007 -->

## 目录

+ TiDB 简介与整体架构
  - [TiDB 简介](overview.md#tidb-简介)
  - [TiDB 整体架构](overview.md#tidb-整体架构)
+ [TiDB 快速入门指南](QUICKSTART.md)
+ TiDB 用户文档
  + TiDB 数据库管理
    - [TiDB 服务](sql/tidb-server.md)
    - [TiDB 进程启动参数](sql/server-command-option.md)
    - [TiDB 数据目录](sql/tidb-server.md#tidb-数据目录)
    - [TiDB 系统数据库](sql/system-database.md)
    - [TiDB 系统变量](sql/variable.md)
    - [TiDB 专用系统变量和语法](sql/tidb-specific.md)
    - [TiDB 服务器日志文件](sql/tidb-server.md#tidb-服务器日志文件)
    - [TiDB 访问权限管理](sql/privilege.md)
    - [TiDB 用户账户管理](sql/user-account-management.md)
    - [使用加密连接](sql/encrypted-connections.md)
  + SQL 优化
    - [理解 TiDB 执行计划](sql/understanding-the-query-execution-plan.md)
    - [统计信息](sql/statistics.md)
  + 语言结构
    - [字面值](sql/literal-values.md)
    - [数据库、表、索引、列和别名](sql/schema-object-names.md)
    - [关键字和保留字](sql/keywords-and-reserved-words.md)
    - [用户变量](sql/user-defined-variables.md)
    - [表达式语法](sql/expression-syntax.md)
    - [注释语法](sql/comment-syntax.md)
  + 字符集和时区
    - [字符集支持](sql/character-set-support.md)
    - [字符集配置](sql/character-set-configuration.md)
    - [时区](sql/time-zone.md)
  + 数据类型
    - [数值类型](sql/datatype.md#数值类型)
    - [日期和时间类型](sql/date-and-time-types.md)
    - [字符串类型](sql/datatype.md#字符串类型)
    - [JSON 数据类型](sql/datatype.md#json-类型)
    - [枚举类型](sql/datatype.md#枚举类型)
    - [集合类型](sql/datatype.md#集合类型)
    - [数据类型默认值](sql/datatype.md#数据类型的默认值)
  + 函数和操作符
    - [函数和操作符概述](sql/functions-and-operators-reference.md)
    - [表达式求值的类型转换](sql/type-conversion-in-expression-evaluation.md)
    - [操作符](sql/operators.md)
    - [控制流程函数](sql/control-flow-functions.md)
    - [字符串函数](sql/string-functions.md)
    - [数值函数与操作符](sql/numeric-functions-and-operators.md)
    - [日期和时间函数](sql/date-and-time-functions.md)
    - [位函数和操作符](sql/bit-functions-and-operators.md)
    - [Cast 函数和操作符](sql/cast-functions-and-operators.md)
    - [加密和压缩函数](sql/encryption-and-compression-functions.md)
    - [信息函数](sql/information-functions.md)
    - [JSON 函数](sql/json-functions.md)
    - [GROUP BY 聚合函数](sql/aggregate-group-by-functions.md)
    - [其他函数](sql/miscellaneous-functions.md)
    - [精度数学](sql/precision-math.md)
  + SQL 语句语法
    - [数据定义语句 (DDL)](sql/ddl.md)
    - [数据操作语句 (DML)](sql/dml.md)
    - [事务语句](sql/transaction.md)
    - [数据库管理语句](sql/admin.md)
    - [Prepared SQL 语句语法](sql/prepare.md)
    - [实用工具语句](sql/util.md)
    - [TiDB SQL 语法图](https://pingcap.github.io/sqlgram/)
  - [JSON 支持](sql/json-functions-generated-column.md)
  - [Connectors 和 API](sql/connection-and-APIs.md)
  - [TiDB 事务隔离级别](sql/transaction-isolation.md)
  - [错误码与故障诊断](sql/error.md)
  - [与 MySQL 兼容性对比](sql/mysql-compatibility.md)
  + 高级功能
    - [历史数据回溯](op-guide/history-read.md)
+ TiDB 运维文档
  - [软硬件环境需求](op-guide/recommendation.md)
  + 部署集群
    - [Ansible 部署方案（强烈推荐）](op-guide/ansible-deployment.md)
    - [离线 Ansible 部署方案](op-guide/offline-ansible-deployment.md)
    - [Docker 部署方案](op-guide/docker-deployment.md)
    - [Docker Compose 部署方案](op-guide/docker-compose.md)
    - [跨机房部署方案](op-guide/location-awareness.md)
  + 配置集群
    - [参数解释](op-guide/configuration.md)
    - [开启 TLS 验证](op-guide/security.md)
    - [生成自签名证书](op-guide/generate-self-signed-certificates.md)
  + 监控集群
    - [整体监控框架概述](op-guide/monitor-overview.md)
    - [重要监控指标详解](op-guide/dashboard-overview-info.md)
    - [组件状态 API & 监控](op-guide/monitor.md)
  + 扩容缩容
     - [使用 Ansible 扩容缩容](QUICKSTART.md#tidb-集群扩容缩容方案)
     - [集群扩容缩容方案](op-guide/horizontal-scale.md)
  - [升级](op-guide/ansible-deployment.md#滚动升级)
  - [性能调优](op-guide/tune-tikv.md)
  + 备份与迁移
    - [备份与恢复](op-guide/backup-restore.md)
    + 数据迁移
      - [数据迁移概述](op-guide/migration-overview.md)
      - [全量导入](op-guide/migration.md#使用-mydumperloader-全量导入数据)
      - [增量导入](op-guide/migration.md#使用-syncer-增量导入数据)
  - [Binary 部署方案](op-guide/binary-deployment.md)
  - [故障诊断](trouble-shooting.md)
+ TiDB 周边工具
  - [Syncer 使用文档](tools/syncer.md)
  - [Loader 使用文档](tools/loader.md)
  - [TiDB-Binlog 使用文档](tools/tidb-binlog-kafka.md)
  - [PD Control 使用文档](tools/pd-control.md)
+ TiSpark 文档
  - [TiSpark 快速入门指南](tispark/tispark-quick-start-guide.md)
  - [TiSpark 用户指南](tispark/tispark-user-guide.md)
+ [常见问题与解答(FAQ)](FAQ.md)
+ [最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)
+ [版本发布历史](releases/README.md)
+ [TiDB 路线图](https://github.com/pingcap/docs-cn/blob/master/ROADMAP.md)
+ 用户案例
  - [海航](http://t.cn/REXx0Qe)
  - [Mobike](http://t.cn/RT8FbP6)
  - [易果生鲜](http://t.cn/RTYVhzH)
  - [一面数据](http://t.cn/RT9r5di)
  - [凤凰网](http://t.cn/RHRQfNT)
  - [猿辅导](http://t.cn/RTKnKSX)
  - [二维火](http://t.cn/R8bXM2f)
  - [Ping++](http://t.cn/RE5xYKn)
  - [去哪儿](http://t.cn/RTKnsL7)
  - [G7](http://t.cn/RQVePoX)
  - [零氪科技](http://t.cn/REj7tSv)
  - [盖娅互娱](http://t.cn/RT9r7hx)
  - [游族网络](http://t.cn/R8k4AWB)
  - [万达网络](http://t.cn/RTKm6ds)
  - [佐助金融](http://t.cn/RQeoKaa)
  - [360金融](http://t.cn/RTKnTev)
  - [某电信运营商](http://t.cn/RTYWADg)
+ 更多资源
  - [常用工具](https://github.com/pingcap/tidb-tools)
  - [PingCAP 团队技术博客](https://pingcap.com/blog-cn/)
  - [知乎专栏](https://zhuanlan.zhihu.com/newsql)
  - [Weekly](https://pingcap.com/weekly/)
  - [英文文档](https://pingcap.com/docs)

## TiDB 简介

TiDB 是 PingCAP 公司受 Google [Spanner](http://research.google.com/archive/spanner.html) / [F1](http://research.google.com/pubs/pub41344.html) 论文启发而设计的开源分布式 NewSQL 数据库。

TiDB 具备如下 NewSQL 核心特性：

* SQL支持（TiDB 是 MySQL 兼容的）
* 水平弹性扩展（吞吐可线性扩展）
* 分布式事务
* 跨数据中心数据强一致性保证
* 故障自恢复的高可用
* 海量数据高并发实时写入与实时查询（HTAP 混合负载）

TiDB 的设计目标是 100% 的 OLTP 场景和 80% 的 OLAP 场景，更复杂的 OLAP 分析可以通过 [TiSpark 项目](https://github.com/pingcap/docs-cn/blob/master/tispark/tispark-user-guide.md)来完成。

TiDB 对业务没有任何侵入性，能优雅的替换传统的数据库中间件、数据库分库分表等 Sharding 方案。同时它也让开发运维人员不用关注数据库 Scale 的细节问题，专注于业务开发，极大的提升研发的生产力。

三篇文章了解 TiDB 技术内幕：

- [说存储](https://pingcap.com/blog-cn/tidb-internal-1/)
- [说计算](https://pingcap.com/blog-cn/tidb-internal-2/)
- [谈调度](https://pingcap.com/blog-cn/tidb-internal-3/)

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

+ TiDB

    TiDB 是无状态的，推荐至少部署两个实例，前端通过负载均衡组件对外提供服务。当单个实例失效时，会影响正在这个实例上进行的 Session，从应用的角度看，会出现单次请求失败的情况，重新连接后即可继续获得服务。单个实例失效后，可以重启这个实例或者部署一个新的实例。

+ PD

    PD 是一个集群，通过 Raft 协议保持数据的一致性，单个实例失效时，如果这个实例不是 Raft 的 leader，那么服务完全不受影响；如果这个实例是 Raft 的 leader，会重新选出新的 Raft leader，自动恢复服务。PD 在选举的过程中无法对外提供服务，这个时间大约是3秒钟。推荐至少部署三个 PD 实例，单个实例失效后，重启这个实例或者添加新的实例。

+ TiKV

    TiKV 是一个集群，通过 Raft 协议保持数据的一致性（副本数量可配置，默认保存三副本），并通过 PD 做负载均衡调度。单个节点失效时，会影响这个节点上存储的所有 Region。对于 Region 中的 Leader 节点，会中断服务，等待重新选举；对于 Region 中的 Follower 节点，不会影响服务。当某个 TiKV 节点失效，并且在一段时间内（默认 10 分钟）无法恢复，PD 会将其上的数据迁移到其他的 TiKV 节点上。
