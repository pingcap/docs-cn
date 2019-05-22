# TiDB 中文用户文档

## 目录

+ [关于 TiDB](overview.md)
+ 主要概念
  - [整体架构](architecture.md)
  + [核心特性](key-features.md)
    - [水平扩展](key-features.md#水平扩展)
    - [高可用](key-features.md#高可用)
+ 操作指南
  + 快速上手
    + 创建本地集群
      - [使用 Docker Compose](dev/how-to/get-started/local-cluster/install-from-docker-compose.md)
    - [SQL 基本操作](dev/how-to/get-started/explore-sql.md)
    - [读取历史数据](dev/how-to/get-started/read-historical-data.md)
  + 部署
    - [软硬件环境需求](dev/how-to/deploy/hardware-recommendations.md)
    + 集群部署方式
      - [使用 Ansible 部署（推荐）](dev/how-to/deploy/orchestrated/ansible.md)
      - [使用 Ansible 离线部署](dev/how-to/deploy/orchestrated/offline-ansible.md)
      - [使用 Docker 部署](dev/how-to/deploy/orchestrated/docker.md)
    + 跨地域冗余
      - [跨数据中心部署方案](dev/how-to/deploy/geographic-redundancy/overview.md)
      - [配置集群拓扑](dev/how-to/deploy/geographic-redundancy/location-awareness.md)
    - [TiSpark 快速上手](dev/how-to/deploy/tispark.md)
    - [使用 Ansible 部署 DM 集群](dev/how-to/deploy/data-migration-with-ansible.md)
  + 配置
    - [时区](dev/how-to/configure/time-zone.md)
    - [内存控制](dev/how-to/configure/memory-control.md)
  + 安全
    + 安全传输层协议 (TLS)
      - [为 MySQL 客户端开启 TLS](dev/how-to/secure/enable-tls-clients.md)
      - [为 TiDB 组件间开启 TLS](dev/how-to/secure/enable-tls-between-components.md)
    - [生成自签名证书](dev/how-to/secure/generate-self-signed-certificates.md)
  + 监控
    - [概述](dev/how-to/monitor/overview.md)
    - [监控 TiDB 集群](dev/how-to/monitor/monitor-a-cluster.md)
  + 迁移
    - [概述](dev/how-to/migrate/overview.md)
    + 从 MySQL 迁移
      - [全量迁移](dev/how-to/migrate/from-mysql.md)
      - [增量复制](dev/how-to/migrate/incrementally-from-mysql.md)
    - [从 CSV 迁移](tools/lightning/csv.md)
  + 运维
    - [Ansible 常见运维操作](dev/how-to/maintain/ansible-operations.md)
    + [备份与恢复](dev/how-to/maintain/backup-and-restore.md)
    - [定位慢查询](dev/how-to/maintain/identify-slow-queries.md)
  + 扩容缩容
    - [使用 Ansible 扩容缩容](dev/how-to/scale/with-ansible.md)
    - [集群扩容缩容方案](dev/how-to/scale/horizontally.md)
  + 升级
    - [升级至 TiDB 3.0](dev/how-to/upgrade/to-tidb-3.0.md)
    - [升级至 TiDB 2.1](dev/how-to/upgrade/to-tidb-2.1.md)
    - [使用 Ansible 滚动升级](dev/how-to/upgrade/rolling-updates-with-ansible.md)
    - [升级 Data Migration](tools/dm/dm-upgrade.md)
  + 故障诊断
    - [集群配置诊断](dev/how-to/troubleshoot/cluster-setup.md)
    - [Data Migration 故障诊断](tools/dm/troubleshooting.md)
    - [TiDB-Lightning 故障诊断](tools/lightning/errors.md)
+ 参考手册
  + [与 MySQL 兼容性对比](sql/mysql-compatibility.md)
  + SQL
    - [TiDB SQL 语法图](https://pingcap.github.io/sqlgram/)
    + SQL 语言结构
      - [字面值](sql/literal-values.md)
      - [Schema 对象名](sql/schema-object-names.md)
      - [关键字和保留字](sql/keywords-and-reserved-words.md)
      - [用户自定义变量](sql/user-defined-variables.md)
      - [表达式语法](sql/expression-syntax.md)
      - [注释语法](sql/comment-syntax.md)
    + 数据类型
      - [数值类型](sql/datatype.md#数值类型)
      - [日期和时间类型](sql/datatype.md#日期时间类型)
      - [字符串类型](sql/datatype.md#字符串类型)
      - [JSON 类型](sql/datatype.md#json-类型)
      - [枚举类型](sql/datatype.md#枚举类型)
      - [集合类型](sql/datatype.md#集合类型)
      - [数据类型默认值](sql/datatype.md#数据类型的默认值)
    + 函数与操作符
      - [函数与操作符概述](sql/functions-and-operators-reference.md)
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
      - [其它函数](sql/miscellaneous-functions.md)
      - [精度数学](sql/precision-math.md)
    + SQL 语句
      - [数据定义语句 (DDL)](sql/ddl.md)
      - [数据操作语句 (DML)](sql/dml.md)
      - [事务语句](sql/transaction.md)
      - [数据库管理语句](sql/admin.md)
      - [Prepared SQL 语句语法](sql/prepare.md)
      - [实用工具语句](sql/util.md)
    - [约束](sql/constraints.md)
    - [生成列](sql/generated-columns.md)
    - [字符集](sql/character-set-support.md)
  + 配置
    + tidb-server
      - [MySQL 系统变量](sql/variable.md)
      - [TiDB 特定系统变量](sql/tidb-specific.md)
      - [配置参数](op-guide/configuration.md)
    + pd-server
      - [配置参数](op-guide/pd-configuration.md)
    + tikv-server
      - [配置参数](op-guide/tikv-configuration.md)
  + 监控指标
    - [Overview 面板](op-guide/dashboard-overview-info.md)
    - [TiDB 面板](op-guide/tidb-dashboard-info.md)
    - [PD 面板](op-guide/dashboard-pd-info.md)
    - [TiKV 面板](op-guide/dashboard-tikv-info.md)
  + 安全
    - [与 MySQL 的安全特性差异](sql/security-compatibility.md)
    - [TiDB 数据库权限管理](sql/privilege.md)
    - [TiDB 用户账户管理](sql/user-account-management.md)
  + 事务
    - [事务模型](sql/transaction-model.md)
    - [隔离级别](sql/transaction-isolation.md)
  + 系统数据库
    - [`mysql`](sql/system-database.md)
    - [`information_schema`](sql/information-schema.md)
  - [错误码](sql/error.md)
  - [支持的连接器和 API](sql/connection-and-APIs.md)
  - [垃圾回收 (GC)](op-guide/gc.md)
  + 性能调优
    - [SQL 优化流程](sql/sql-optimizer-overview.md)
    - [理解 TiDB 执行计划](sql/understanding-the-query-execution-plan.md)
    - [统计信息概述](sql/statistics.md)
    - [Optimizer Hints](sql/optimizer-hints.md)
    - [TiKV 调优](op-guide/tune-tikv.md)
    - [TiDB 最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)
  + [TiSpark 使用指南](tispark/tispark-user-guide.md)
  + 生态工具
    - [Mydumper](dev/reference/tools/mydumper.md)
    - [Loader](dev/reference/tools/loader.md)
    - [Syncer](dev/reference/tools/syncer.md)
    + Data Migration
      + [概述](dev/reference/tools/data-migration/overview.md)
        - [DM 架构](dev/reference/tools/data-migration/overview.md#dm-架构)
        - [同步功能介绍](dev/reference/tools/data-migration/overview.md#同步功能介绍)
        - [使用限制](dev/reference/tools/data-migration/overview.md#使用限制)
      + 核心特性
        - [Table Routing](dev/reference/tools/data-migration/features/overview.md#table-routing)
        - [Black & White Lists](dev/reference/tools/data-migration/features/overview.md#black-white-table-lists)
        - [Binlog Event Filter](dev/reference/tools/data-migration/features/overview.md#binlog-event-filter)
        - [Column Mapping](dev/reference/tools/data-migration/features/overview.md#column-mapping)
        - [同步延迟监控](dev/reference/tools/data-migration/features/overview.md#同步延迟监控)
        + Shard Support
          - [简介](dev/reference/tools/data-migration/features/shard-merge.md)
          - [使用限制](dev/reference/tools/data-migration/features/shard-merge.md#使用限制)
          - [手动处理 Sharding DDL Lock](dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)
      + 使用场景
        - [简单的从库同步场景](dev/reference/tools/data-migration/usage-scenarios/simple-synchronization-scenario.md)
        - [分库分表合并场景](dev/reference/tools/data-migration/usage-scenarios/shard-merge-scenario.md)
      + [部署使用](dev/reference/tools/data-migration/practice.md)
      + 配置
        - [概述](dev/reference/tools/data-migration/configure/overview.md)
        - [任务配置](dev/reference/tools/data-migration/configure/task-configuration-file.md)
      - [监控 DM 集群](dev/reference/tools/data-migration/monitor.md)
      - [管理数据同步任务](dev/reference/tools/data-migration/manage-tasks.md)
      - [DM 集群操作](dev/reference/tools/data-migration/cluster-operations.md)
      + 从与 MySQL 兼容的数据库迁移数据
        - [从 AWS Aurora MySQL 迁移数据](dev/reference/tools/data-migration/from-aurora.md)
    + TiDB-Lightning
      - [概述](dev/reference/tools/tidb-lightning/overview.md)
      - [部署执行](dev/reference/tools/tidb-lightning/deployment.md)
      - [断点续传](dev/reference/tools/tidb-lightning/checkpoints.md)
      - [表库过滤](dev/reference/tools/tidb-lightning/table-filter.md)
      - [CSV 支持](dev/reference/tools/tidb-lightning/csv.md)
      - [监控告警](dev/reference/tools/tidb-lightning/monitor.md)
    + TiDB-Binlog
      - [概述](dev/reference/tools/tidb-binlog/overview.md)
      - [部署使用](dev/reference/tools/tidb-binlog/deploy.md)
      - [监控告警](dev/reference/tools/tidb-binlog/monitor.md)
      - [运维管理](dev/reference/tools/tidb-binlog/operation.md)
      - [版本升级](dev/reference/tools/tidb-binlog/upgrade.md)
    - [PD Control](dev/reference/tools/pd-control.md)
    - [PD Recover](dev/reference/tools/pd-recover.md)
    - [TiKV Control](https://github.com/tikv/tikv/blob/master/docs/tools/tikv-control.md)
    - [TiDB Controller](dev/reference//tidb-control.md)
    - [工具下载](dev/reference/tools/download.md)
+ 常见问题 (FAQ)
  - [TiDB FAQ](FAQ.md)
  - [TiDB-Lightning FAQ](tools/lightning/faq.md)
  - [升级 FAQ](op-guide/upgrade-faq.md)
+ 技术支持
  - [支持渠道](support.md)
  - [反馈问题](report-issue.md)
+ [贡献](contribute.md)
  - [贡献代码](contribute.md#成为-tidb-的贡献者)
  - [改进文档](contribute.md#改进文档)
- [TiDB 路线图](ROADMAP.md)
+ [版本发布历史](releases/rn.md)
  + v3.0
    - [3.0.0-rc.1](releases/3.0.0-rc.1.md)
    - [3.0.0-beta.1](releases/3.0.0-beta.1.md)
    - [3.0.0-beta](releases/3.0beta.md)
  + v2.1
    - [2.1.9](releases/2.1.9.md)
    - [2.1.8](releases/2.1.8.md)
    - [2.1.7](releases/2.1.7.md)
    - [2.1.6](releases/2.1.6.md)
    - [2.1.5](releases/2.1.5.md)
    - [2.1.4](releases/2.1.4.md)
    - [2.1.3](releases/2.1.3.md)
    - [2.1.2](releases/2.1.2.md)
    - [2.1.1](releases/2.1.1.md)
    - [2.1 GA](releases/2.1ga.md)
    - [2.1 RC5](releases/21rc5.md)
    - [2.1 RC4](releases/21rc4.md)
    - [2.1 RC3](releases/21rc3.md)
    - [2.1 RC2](releases/21rc2.md)
    - [2.1 RC1](releases/21rc1.md)
    - [2.1 Beta](releases/21beta.md)
  + v2.0
    - [2.0.11](releases/2.0.11.md)
    - [2.0.10](releases/2.0.10.md)
    - [2.0.9](releases/209.md)
    - [2.0.8](releases/208.md)
    - [2.0.7](releases/207.md)
    - [2.0.6](releases/206.md)
    - [2.0.5](releases/205.md)
    - [2.0.4](releases/204.md)
    - [2.0.3](releases/203.md)
    - [2.0.2](releases/202.md)
    - [2.0.1](releases/201.md)
    - [2.0](releases/2.0ga.md)
    - [2.0 RC5](releases/2rc5.md)
    - [2.0 RC4](releases/2rc4.md)
    - [2.0 RC3](releases/2rc3.md)
    - [2.0 RC1](releases/2rc1.md)
    - [1.1 Beta](releases/11beta.md)
    - [1.1 Alpha](releases/11alpha.md)
  + v1.0
    - [1.0](releases/ga.md)
    - [Pre-GA](releases/prega.md)
    - [RC4](releases/rc4.md)
    - [RC3](releases/rc3.md)
    - [RC2](releases/rc2.md)
    - [RC1](releases/rc1.md)
