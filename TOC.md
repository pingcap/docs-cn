# TiDB 中文用户文档

<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD032 -->

## 目录

+ 关于 TiDB
  + 基本信息 @段兵
    + [TiDB 简介](/overview.md)
    + [开源信息说明](/licensing.md)
    + [核心用户列表](/adopters.md)
  + [核心特性](/key-features.md) @段兵
    + 数据类型
    + SQL 与功能
    + 安全性
    + 可靠性
    + 可用性
    + 性能数据
    + 配套工具
    + 企业版特性
  + 兼容性 @段兵
    + [与标准 SQL 的兼容性](/differences-from-standard-sql.md)
    + [与 MySQL 的兼容性](/mysql-compatibility.md)
    + [使用限制](/tidb-limitations.md)
  + [使用场景](/use-cases.md) @段兵
  + [荣誉列表](/credits.md) @姚维
+ 快速上手
  + [快速上手指南](/quick-start-with-tidb.md) @李坤
  + [SQL 基本操作](/basic-sql-operations.md) @庄培培
+ 部署集群
  + [软硬件环境需求](/hardware-and-software-requirements.md) @李仲舒
  + [环境与系统配置检查](/check-before-deployment.md) @李仲舒
  + 配置拓扑结构
    + [最小部署拓扑结构](/minimal-deployment-topology.md) @李仲舒
    + [跨机房部署拓扑结构](/geo-distributed-deployment-topology.md) @李仲舒（[参考](/location-awareness.md)）
    + [混合部署拓扑结构](/hybrid-deployment-topology.md) @李仲舒
  + 安装与启动
    + Linux
      + [使用 TiUP 部署](/production-deployment-using-tiup.md) @李仲舒
      + [使用 TiUP 离线部署](/production-offline-deployment-using-tiup.md) @刘金龙
      + [使用 Ansible 部署](/online-deployment-using-ansible.md)
      + [使用 Ansible 离线部署](/offline-deployment-using-ansible.md)
      + [使用 Docker 部署](/test-deployment-using-docker.md)
    + Kubernetes
    + AWS
    + GCP
    + Alibaba Cloud
  + [测试验证](/post-installation-check.md) @李仲舒
  + 性能测试报告及重现指南
    + [如何用 Sysbench 测试 TiDB](/benchmark/benchmark-tidb-using-sysbench.md) @周跃跃
    + [如何对 TiDB 进行 TPC-C 测试](/benchmark/benchmark-tidb-using-tpcc.md) @梁启斌
    + [Sysbench 性能对比 - v3.0 对比 v2.1](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)
    + [TPC-C 性能对比 - v4.0 对比 v3.0](/benchmark/v4.0-performance-benchmarking-with-tpcc.md)
    + [TPC-C 性能对比 - v3.0 对比 v2.1](/benchmark/v3.0-performance-benchmarking-with-tpcc.md)
    + [线上负载与 ADD INDEX 相互影响测试](/benchmark/online-workloads-and-add-index-operations.md)
+ 数据迁移
  + [支持的迁移路径](/ecosystem-tool-user-guide.md) @王相
  + 从 MySQL 迁移至 TiDB
    + [从 CSV 文件迁移](/migrate-from-mysql-csv-files.md) @栾成
    + [从 Mydumper 文件迁移](/migrate-from-mysql-mydumper-files.md) @栾成
    + [使用 DM 工具从 Amazon Aurora MySQL 迁移](/migrate-from-aurora-mysql-database.md) @张学成，王相
  + [从 CSV 文件迁移至 TiDB](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md) @王相
+ 运维操作
  + 升级 TiDB 版本
    + [使用 TiUP](/upgrade-tidb-using-tiup.md) @戚铮
    + [使用 TiDB Operator](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster/)
    + [使用 TiDB Ansible](/upgrade-tidb-using-ansible.md)
  + 扩缩容
    + [使用 TiUP](/scale-tidb-using-tiup.md) @刘金龙
    + [使用 TiDB Operator](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/scale-a-tidb-cluster/)
  + 备份与恢复
    + [使用 Mydumper 和 TiDB Lightning](/backup-and-restore-using-mydumper-lightning.md) @栾成
    + 使用 BR 工具
      + [使用 BR 进行备份与恢复](/br/backup-and-restore-tool.md) @栾成
      + [BR 备份与恢复场景示例](/br/backup-and-restore-use-cases.md) @栾成
  + [日常巡检](/daily-inspection.md) @王军
  + [TiCDC 任务管理](/ticdc/manage-ticdc.md) @沈泰宁
  + [TiUP 常用运维操作](/maintain-tidb-using-tiup.md) @王贤净
  + [TiFlash 常用运维操作](/tiflash/maintain-tiflash.md) @雷宇
+ 监控与告警
  + [监控框架概述](/tidb-monitoring-framework.md) @李宋高
  + [监控 API](/tidb-monitoring-api.md) @李宋高
  + [手动部署监控](/deploy-monitoring-services.md) @李宋高
  + [TiDB 集群报警规则与处理方法](/alert-rules.md) @李宋高
  + [TiFlash 报警规则与处理方法](/tiflash/tiflash-alert-rules.md) @孙若曦
+ 故障诊断
  + 硬件故障 @周强
    + [整机](/troubleshoot-machine-issues.md)
    + [硬盘](/troubleshoot-disk-issues.md)
    + [网络](/troubleshoot-network-issues.md)
    + [内存](/troubleshoot-memory-issues.md)（[相关参考](https://pingcap.com/docs-cn/stable/configure-memory-usage/)）
  + 操作系统故障 @周强
    + [版本](/troubleshoot-operating-system-issues.md)
    + [内核参数](/troubleshoot-kernel-parameter-issues.md)
  + [定位慢查询](/identify-slow-queries.md) @张原嘉
  + [SQL 诊断](/system-tables/system-table-sql-diagnosis.md) @SQL Infra
  + [定位消耗系统资源多的查询](/identify-expensive-queries.md)
  + [SQL 语句统计](/statement-summary-tables.md) @SQL Infra
  + [热点问题处理](/troubleshoot-hot-spot-issues.md) @郭大瑞
  + [CPU 占用过多导致读写延迟增加](/troubleshoot-cpu-issues.md) @高恺迪
  + [写冲突与写性能下降](/troubleshoot-write-conflicts.md) @沈刚
  + [磁盘 I/O 过高](/troubleshoot-high-disk-io.md) @陶政
  + [锁冲突与 TTL 超时](/troubleshoot-lock-conflicts.md) @高振娇
  + [从性能监控分析问题](/performance-tuning-monitor.md) @李坤
  + [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md) @杨非
  + [TiFlash 常见问题](/tiflash/troubleshoot-tiflash.md) @孙若曦
+ 性能调优
  + 系统调优
    + [硬件](/tune-hardware-performance.md) @张文博
    + [操作系统性能参数调优](/tune-operating-system.md) @张文博
  + 软件调优
    + [软件版本](/tune-software-version.md) @张文博
    + 配置
      + [TiKV 调优](/tune-tikv-performance.md) @刘玮
      + [TiFlash 调优](/tiflash/tune-tiflash-performance.md)
  + SQL 性能调优 @崔一丁
    + [SQL 性能调优概览](/sql-tuning-overview.md)
    + [理解 TiDB 执行计划](/query-execution-plan.md)
    + SQL 优化
      + [SQL 优化流程简介](/sql-optimization-concepts.md)
      + 逻辑优化
        + [逻辑优化概览](/sql-logical-optimization.md)
        + [子查询相关的优化](/subquery-optimization.md)
        + [列裁剪](/column-pruning.md)
        + [关联子查询去关联](/correlated-subquery-optimization.md)
        + [Max/Min 消除](/max-min-eliminate.md)
        + [谓词下推](/predicate-push-down.md)
        + [分区裁剪](/partition-pruning.md)
        + [TopN 和 Limit 下推](/topn-limit-push-down.md)
        + [Join Reorder](/join-reorder.md)
      + 物理优化
        + [物理优化概览](/sql-physical-optimization.md)
        + [索引的选择](/index-choose.md)
        + [统计信息简介](/statistics.md)
        + [错误索引的解决方案](/wrong-index-solution.md)
        + [Distinct 优化](/agg-distinct-optimization.md)
      + [执行计划缓存](/sql-prepare-plan-cache.md)
      + 控制执行计划
        + [控制执行计划概览](/control-execution-plan.md)
        + [Optimizer Hints](/optimizer-hints.md)
        + [执行计划绑定](/execution-plan-binding.md)
        + [优化规则及表达式下推的黑名单](/blacklist-control-plan.md)
+ 教程
  + [同城多中心部署](/multi-data-centers-in-one-city-deployment.md)（[参考](https://pingcap.com/docs-cn/stable/geo-redundancy-deployment/)）@侯召墩
  + [两地三中心部署](/three-data-centers-in-two-cities-deployment.md) 侯召墩
  + 最佳实践
    + [TiDB 最佳实践](/tidb-best-practices.md)（[参考相关博客](https://pingcap.com/blog-cn/tidb-best-practice/)）@李坤
    + [Java 应用开发最佳实践](/best-practices/java-app-best-practices.md) @李坤
    + [HAProxy 最佳实践](/best-practices/haproxy-best-practices.md) @李坤
    + [高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md) @李坤
    + [Grafana 监控最佳实践](/best-practices/grafana-monitor-best-practices.md) @李坤
    + [PD 调度策略最佳实践](/best-practices/pd-scheduling-best-practices.md) @李坤
    + [海量 Region 集群调优](/best-practices/massive-regions-best-practices.md) @李建俊
  + [Placement Rules 使用文档](/configure-placement-rules.md) @黄梦龙
+ TiDB 生态工具
  + [工具使用指南](/ecosystem-tool-user-guide.md)
  + [工具下载](/download-ecosystem-tools.md)
  + Backup & Restore (BR)
    + [使用 BR 进行备份和恢复](/br/backup-and-restore-tool.md) @余峻岑
    + [BR 备份与恢复场景示例](/br/backup-and-restore-use-cases.md) @余峻岑
  + TiDB Lightning @kenny
    + [概述](/tidb-lightning/tidb-lightning-overview.md)
    + [快速上手教程](/get-started-with-tidb-lightning.md)
    + [部署执行](/tidb-lightning/deploy-tidb-lightning.md)
    + [参数说明](/tidb-lightning/tidb-lightning-configuration.md)
    + 主要功能
      + [断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)
      + [表库过滤](/tidb-lightning/tidb-lightning-table-filter.md)
      + [CSV 支持](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)
      + [TiDB-backend](/tidb-lightning/tidb-lightning-tidb-backend.md)
      + [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)
    + [监控告警](/tidb-lightning/monitor-tidb-lightning.md)
    + [故障诊断](/troubleshoot-tidb-lightning.md)
    + [FAQ](/tidb-lightning/tidb-lightning-faq.md)
    + [术语表](/tidb-lightning/tidb-lightning-glossary.md)
  + TiCDC
    + [概述](/ticdc/ticdc-overview.md)
    + [部署使用](/ticdc/deploy-ticdc.md)
    + [集群和同步任务管理](/ticdc/manage-ticdc.md)
    + [常见问题和故障处理](/ticdc/troubleshoot-ticdc.md)
    + [Sink URI 配置规则](/ticdc/sink-url.md)
    + [开放数据协议](/ticdc/ticdc-open-protocol.md)
    + [Column 和 DDL 的类型码](/ticdc/column-ddl-type-codes.md)
  + sync-diff-inspector @王相
    + [概述](/sync-diff-inspector/sync-diff-inspector-overview.md)
    + [不同库名或表名的数据校验](/sync-diff-inspector/route-diff.md)
    + [分库分表场景下的数据校验](/sync-diff-inspector/shard-diff.md)
    + [TiDB 主从集群的数据校验](/sync-diff-inspector/upstream-downstream-diff.md)
  + [Loader](/loader-overview.md) @王相
  + [Mydumper](/mydumper-overview.md) @余峻岑
  + [Syncer](/syncer-overview.md) @王相
  + TiUP @龙恒
    + [文档指南](/tiup/tiup-documentation-guide.md)
    + [概览](/tiup/tiup-overview.md)
    + [术语及核心概念](/tiup/tiup-terminology-and-concepts.md)
    + [TiUP 组件管理](/tiup/tiup-component-management.md)
    + [FAQ](/tiup/tiup-faq.md)
    + [故障排查](/tiup/tiup-troubleshooting-guide.md)
    + TiUP 组件文档
      + [tiup-playground 运行本地测试集群](/tiup/tiup-playground.md)
      + [tiup-cluster 部署运维生产集群](/tiup/tiup-cluster.md)
      + [tiup-mirrors 定制离线镜像](/tiup/tiup-mirrors.md)
      + [tiup-package 打包 TiUP 组件](/tiup/tiup-package.md)
      + [tiup-bench 进行 TPCC/TPCH 压力测试](/tiup/tiup-bench.md)
+ 参考指南
  + 架构
    + [概述](/tidb-architecture.md) @黄东旭
    + [存储](/tidb-storage.md) @冯立元
    + [计算](/tidb-computing.md) @黄东旭
    + [调度](/tidb-scheduling.md) @陈书宁
  + 监控指标
    + [Overview 面板](/grafana-overview-dashboard.md) @王聪
    + [TiDB 面板](/grafana-tidb-dashboard.md) @于帅鹏
    + [PD 面板](/grafana-pd-dashboard.md) @PD Team/陈书宁
    + [TiKV 面板](/grafana-tikv-dashboard.md) @刘新韬
    + [TiFlash 监控指标](/tiflash/monitor-tiflash.md) @孙若曦
  + 安全加固
    + [为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients.md) @苏立
    + [为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md) @苏立
    + [为 TiDB 开启数据加密存储](/enable-encrypt-stored-data.md) @苏立
    + [生成自签名证书](/generate-self-signed-certificates.md) @刘新韬
  + 权限
    + [与 MySQL 安全特性差异](/security-compatibility-with-mysql.md) @毛康力
    + [权限管理](/privilege-management.md) @毛康力
    + [TiDB 用户账户管理](/user-account-management.md) @毛康力
    + [基于角色的访问控制](/role-based-access-control.md) @宋翎宇
    + [TiDB 证书鉴权使用指南](/certificate-authentication.md) @苏立
  + SQL
    + SQL 语言结构和语法
      + 属性
        + [AUTO_INCREMENT](/auto-increment.md) @谢腾进
        + [AUTO_RANDOM](/auto-random.md) @谢腾进
      + [字面值](/literal-values.md) @邰凌翔
      + [Schema 对象名](/schema-object-names.md) @邰凌翔
      + [关键字](/keywords.md) @@邰凌翔
      + [用户自定义变量](/user-defined-variables.md) @邰凌翔
      + [表达式语法](/expression-syntax.md) @邰凌翔
      + [注释语法](/comment-syntax.md) @邰凌翔
    + SQL 语句 @张明/李霞
      - [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
      - [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
      - [`ADMIN`](/sql-statements/sql-statement-admin.md)
      - [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)
      - [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md)
      - [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
      - [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)
      - [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
      - [`BEGIN`](/sql-statements/sql-statement-begin.md)
      - [`COMMIT`](/sql-statements/sql-statement-commit.md)
      - [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md)
      - [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)
      - [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md)
      - [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)
      - [`CREATE TABLE LIKE`](/sql-statements/sql-statement-create-table-like.md)
      - [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
      - [`CREATE USER`](/sql-statements/sql-statement-create-user.md)
      - [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)
      - [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md)
      - [`DELETE`](/sql-statements/sql-statement-delete.md)
      - [`DESC`](/sql-statements/sql-statement-desc.md)
      - [`DESCRIBE`](/sql-statements/sql-statement-describe.md)
      - [`DO`](/sql-statements/sql-statement-do.md)
      - [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md)
      - [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
      - [`DROP DATABASE`](/sql-statements/sql-statement-drop-database.md)
      - [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
      - [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md)
      - [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)
      - [`DROP TABLE`](/sql-statements/sql-statement-drop-table.md)
      - [`DROP USER`](/sql-statements/sql-statement-drop-user.md)
      - [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md)
      - [`EXECUTE`](/sql-statements/sql-statement-execute.md)
      - [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)
      - [`EXPLAIN`](/sql-statements/sql-statement-explain.md)
      - [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)
      - [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)
      - [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md)
      - [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md)
      - [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
      - [`INSERT`](/sql-statements/sql-statement-insert.md)
      - [`KILL [TIDB]`](/sql-statements/sql-statement-kill.md)
      - [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)
      - [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)
      - [`PREPARE`](/sql-statements/sql-statement-prepare.md)
      - [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)
      - [`RENAME INDEX`](/sql-statements/sql-statement-rename-index.md)
      - [`RENAME TABLE`](/sql-statements/sql-statement-rename-table.md)
      - [`REPLACE`](/sql-statements/sql-statement-replace.md)
      - [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
      - [`ROLLBACK`](/sql-statements/sql-statement-rollback.md)
      - [`SELECT`](/sql-statements/sql-statement-select.md)
      - [`SET [NAMES|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md)
      - [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md)
      - [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)
      - [`SET [GLOBAL|SESSION] <variable>`](/sql-statements/sql-statement-set-variable.md)
      - [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)
      - [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md)
      - [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)
      - [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
      - [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
      - [`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)
      - [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md)
      - [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)
      - [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)
      - [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)
      - [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)
      - [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)
      - [`SHOW [FULL] FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md)
      - [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)
      - [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-histograms.md)
      - [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)
      - [`SHOW INDEXES [FROM|IN]`](/sql-statements/sql-statement-show-indexes.md)
      - [`SHOW INDEX [FROM|IN]`](/sql-statements/sql-statement-show-index.md)
      - [`SHOW KEYS [FROM|IN]`](/sql-statements/sql-statement-show-keys.md)
      - [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md)
      - [`SHOW [FULL] PROCESSSLIST`](/sql-statements/sql-statement-show-processlist.md)
      - [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md)
      - [`SHOW [FULL] TABLES`](/sql-statements/sql-statement-show-tables.md)
      - [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
      - [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)
      - [`SHOW [GLOBAL|SESSION] VARIABLES`](/sql-statements/sql-statement-show-variables.md)
      - [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)
      - [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md)
      - [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-row-id.md)
      - [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md)
      - [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md)
      - [`TRACE`](/sql-statements/sql-statement-trace.md)
      - [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)
      - [`UPDATE`](/sql-statements/sql-statement-update.md)
      - [`USE`](/sql-statements/sql-statement-use.md)
    + 数据类型 @张原嘉
      + [数据类型概述](/data-type-overview.md)
      + [数据类型默认值](/data-type-default-values.md)
      + [数值类型](/data-type-numeric.md)
      + [日期和时间类型](/data-type-date-and-time.md)
      + [字符串类型](/data-type-string.md)
      + [JSON 类型](/data-type-json.md)
    + 函数与操作符 @张原嘉
      + [函数与操作符概述](/functions-and-operators/functions-and-operators-overview.md)
      + [表达式求值的类型转换](/functions-and-operators/type-conversion-in-expression-evaluation.md)
      + [操作符](/functions-and-operators/operators.md)
      + [控制流程函数](/functions-and-operators/control-flow-functions.md)
      + [字符串函数](/functions-and-operators/string-functions.md)
      + [数值函数与操作符](/functions-and-operators/numeric-functions-and-operators.md)
      + [日期和时间函数](/functions-and-operators/date-and-time-functions.md)
      + [位函数和操作符](/functions-and-operators/bit-functions-and-operators.md)
      + [Cast 函数和操作符](/functions-and-operators/cast-functions-and-operators.md)
      + [加密和压缩函数](/functions-and-operators/encryption-and-compression-functions.md)
      + [信息函数](/functions-and-operators/information-functions.md)
      + [JSON 函数](/functions-and-operators/json-functions.md)
      + [GROUP BY 聚合函数](/functions-and-operators/aggregate-group-by-functions.md)
      + [窗口函数](/functions-and-operators/window-functions.md)
      + [其它函数](/functions-and-operators/miscellaneous-functions.md)
      + [精度数学](/functions-and-operators/precision-math.md)
      + [下推到 TiKV 的表达式列表](/functions-and-operators/expressions-pushed-down.md)
    + [约束](/constraints.md) @于帅鹏
    + [生成列](/generated-columns.md) @黄文俊
    + [SQL 模式](/sql-mode.md) @张原嘉
    + 事务
      + [事务概览](/transaction-overview.md) @于帅鹏
      + [隔离级别](/transaction-isolation-levels.md) @于帅鹏
      + [乐观事务](/optimistic-transaction.md) @于帅鹏
      + [悲观事务](/pessimistic-transaction.md) @于帅鹏
    + 垃圾回收 (GC)
      + [GC 机制简介](/garbage-collection-overview.md)
      + [GC 配置](/garbage-collection-configuration.md)
    + [视图](/views.md) @徐怀宇
    + [分区表](/partitioned-table.md) @毛康力
    + [字符集和排序规则](/character-set-and-collation.md) @黄文俊
    + 系统表 @陈霜
      + [`mysql`](/system-tables/system-table-overview.md)
      + [`information_schema`](/system-tables/system-table-information-schema.md)
      + `sql-diagnosis`
        + [`cluster_info`](/system-tables/system-table-cluster-info.md)
        + [`cluster_hardware`](/system-tables/system-table-cluster-hardware.md)
        + [`cluster_config`](/system-tables/system-table-cluster-config.md)
        + [`cluster_load`](/system-tables/system-table-cluster-load.md)
        + [`cluster_systeminfo`](/system-tables/system-table-cluster-systeminfo.md)
        + [`cluster_log`](/system-tables/system-table-cluster-log.md)
        + [`metrics_schema`](/system-tables/system-table-metrics-schema.md)
        + [`metrics_tables`](/system-tables/system-table-metrics-tables.md)
        + [`metrics_summary`](/system-tables/system-table-metrics-summary.md)
        + [`inspection_result`](/system-tables/system-table-inspection-result.md)
        + [`inspection_summary`](/system-tables/system-table-inspection-summary.md)
  + UI
    + TiDB Dashboard @施闻轩
      + 访问
      + 概况页面
      + 集群信息页面
      + 流量可视化页面
      + SQL 语句分析页面
      + 慢查询页面
      + 集群诊断页面
      + 日志搜索页面
      + 实例性能分析页面
  + CLI
    + [tikv-ctl](/tikv-control.md) @屈鹏
    + [pd-ctl](/pd-control.md) @陈书宁
    + [tidb-ctl](/tidb-control.md) @于帅鹏
    + [binlog-ctl](/tidb-binlog/binlog-control.md) @王相
    + [pd-recover](/pd-recover.md) @陈书宁
  + 命令行参数
    + [tidb-server](/command-line-flags-for-tidb-configuration.md) @于帅鹏
    + [tikv-server](/command-line-flags-for-tikv-configuration.md) @陈书宁
    + [tiflash-server](/tiflash/tiflash-command-line-flags.md) @孙若曦
    + [pd-server](/command-line-flags-for-pd-configuration.md) @陈书宁
  + 配置文件参数
    + [tidb-server](/tidb-configuration-file.md) @于帅鹏
    + [tikv-server](/tikv-configuration-file.md) @陈书宁
    + [tiflash-server](/tiflash/tiflash-configuration.md) @孙若曦
    + [pd-server](/pd-configuration-file.md) @陈书宁
  + 系统变量
    + [MySQL 系统变量](/system-variables.md)
    + [TiDB 特定系统变量](/tidb-specific-system-variables.md)
  + 存储引擎
    + TiKV
      + [RocksDB 简介](/rocksdb/rocksdb-overview.md)
    + TiFlash
  + [错误码](/error-codes.md) @于帅鹏
+ 常见问题解答 (FAQ)
  + [产品 FAQ](/faq/tidb-faq.md) @荣毅龙/启航
  + [SQL FAQ](/faq/sql-faq.md) @荣毅龙/启航
  + [部署运维 FAQ](/faq/deploy-and-maintain-faq.md) @荣毅龙/启航
  + [升级 FAQ](/faq/upgrade-faq.md) @荣毅龙/启航
  + [License FAQ](/faq/licensing-faq.md) @荣毅龙/启航
  + [高可用 FAQ](/faq/high-availability-faq.md) @荣毅龙/启航
  + [高可靠 FAQ](/faq/high-reliability-faq.md) @荣毅龙/启航
+ [术语表](/glossary.md) @李琳
+ [版本发布历史](/releases/release-notes.md)
  + v4.0
    - [4.0.0-rc.2](/releases/release-4.0.0-rc.2.md)
    - [4.0.0-rc.1](/releases/release-4.0.0-rc.1.md)
    - [4.0.0-rc](/releases/release-4.0.0-rc.md)
    - [4.0.0-beta.2](/releases/release-4.0.0-beta.2.md)
    - [4.0.0-beta.1](/releases/release-4.0.0-beta.1.md)
    - [4.0.0-beta](/releases/release-4.0.0-beta.md)
  + v3.1
    - [3.1.1](/releases/release-3.1.1.md)
    - [3.1.0 GA](/releases/release-3.1.0-ga.md)
    - [3.1.0-rc](/releases/release-3.1.0-rc.md)
    - [3.1.0-beta.2](/releases/release-3.1.0-beta.2.md)
    - [3.1.0-beta.1](/releases/release-3.1.0-beta.1.md)
    - [3.1.0-beta](/releases/release-3.1.0-beta.md)
  + v3.0
    - [3.0.14](/releases/release-3.0.14.md)
    - [3.0.13](/releases/release-3.0.13.md)
    - [3.0.12](/releases/release-3.0.12.md)
    - [3.0.11](/releases/release-3.0.11.md)
    - [3.0.10](/releases/release-3.0.10.md)
    - [3.0.9](/releases/release-3.0.9.md)
    - [3.0.8](/releases/release-3.0.8.md)
    - [3.0.7](/releases/release-3.0.7.md)
    - [3.0.6](/releases/release-3.0.6.md)
    - [3.0.5](/releases/release-3.0.5.md)
    - [3.0.4](/releases/release-3.0.4.md)
    - [3.0.3](/releases/release-3.0.3.md)
    - [3.0.2](/releases/release-3.0.2.md)
    - [3.0.1](/releases/release-3.0.1.md)
    - [3.0 GA](/releases/release-3.0-ga.md)
    - [3.0.0-rc.3](/releases/release-3.0.0-rc.3.md)
    - [3.0.0-rc.2](/releases/release-3.0.0-rc.2.md)
    - [3.0.0-rc.1](/releases/release-3.0.0-rc.1.md)
    - [3.0.0-beta.1](/releases/release-3.0.0-beta.1.md)
    - [3.0.0-beta](/releases/release-3.0-beta.md)
  + v2.1
    - [2.1.19](/releases/release-2.1.19.md)
    - [2.1.18](/releases/release-2.1.18.md)
    - [2.1.17](/releases/release-2.1.17.md)
    - [2.1.16](/releases/release-2.1.16.md)
    - [2.1.15](/releases/release-2.1.15.md)
    - [2.1.14](/releases/release-2.1.14.md)
    - [2.1.13](/releases/release-2.1.13.md)
    - [2.1.12](/releases/release-2.1.12.md)
    - [2.1.11](/releases/release-2.1.11.md)
    - [2.1.10](/releases/release-2.1.10.md)
    - [2.1.9](/releases/release-2.1.9.md)
    - [2.1.8](/releases/release-2.1.8.md)
    - [2.1.7](/releases/release-2.1.7.md)
    - [2.1.6](/releases/release-2.1.6.md)
    - [2.1.5](/releases/release-2.1.5.md)
    - [2.1.4](/releases/release-2.1.4.md)
    - [2.1.3](/releases/release-2.1.3.md)
    - [2.1.2](/releases/release-2.1.2.md)
    - [2.1.1](/releases/release-2.1.1.md)
    - [2.1 GA](/releases/release-2.1-ga.md)
    - [2.1 RC5](/releases/release-2.1-rc.5.md)
    - [2.1 RC4](/releases/release-2.1-rc.4.md)
    - [2.1 RC3](/releases/release-2.1-rc.3.md)
    - [2.1 RC2](/releases/release-2.1-rc.2.md)
    - [2.1 RC1](/releases/release-2.1-rc.1.md)
    - [2.1 Beta](/releases/release-2.1-beta.md)
  + v2.0
    - [2.0.11](/releases/release-2.0.11.md)
    - [2.0.10](/releases/release-2.0.10.md)
    - [2.0.9](/releases/release-2.0.9.md)
    - [2.0.8](/releases/release-2.0.8.md)
    - [2.0.7](/releases/release-2.0.7.md)
    - [2.0.6](/releases/release-2.0.6.md)
    - [2.0.5](/releases/release-2.0.5.md)
    - [2.0.4](/releases/release-2.0.4.md)
    - [2.0.3](/releases/release-2.0.3.md)
    - [2.0.2](/releases/release-2.0.2.md)
    - [2.0.1](/releases/release-2.0.1.md)
    - [2.0](/releases/release-2.0-ga.md)
    - [2.0 RC5](/releases/release-2.0-rc.5.md)
    - [2.0 RC4](/releases/release-2.0-rc.4.md)
    - [2.0 RC3](/releases/release-2.0-rc.3.md)
    - [2.0 RC1](/releases/release-2.0-rc.1.md)
    - [1.1 Beta](/releases/release-1.1-beta.md)
    - [1.1 Alpha](/releases/release-1.1-alpha.md)
  + v1.0
    - [1.0](/releases/release-1.0-ga.md)
    - [Pre-GA](/releases/release-pre-ga.md)
    - [RC4](/releases/release-rc.4.md)
    - [RC3](/releases/release-rc.3.md)
    - [RC2](/releases/release-rc.2.md)
    - [RC1](/releases/release-rc.1.md)
