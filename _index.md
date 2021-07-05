---
title: TiDB 简介
summary: 了解 TiDB 数据库。
aliases: ['/docs-cn/','/docs-cn/stable/','/docs-cn/v4.0/']
---

<!-- markdownlint-disable MD046 -->

# TiDB 简介

[TiDB](https://github.com/pingcap/tidb) 是 [PingCAP](https://pingcap.com/about-cn/) 公司自主设计、研发的开源分布式关系型数据库，是一款同时支持在线事务处理与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 的融合型分布式数据库产品，具备水平扩容或者缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 5.7 协议和 MySQL 生态等重要特性。目标是为用户提供一站式 OLTP (Online Transactional Processing)、OLAP (Online Analytical Processing)、HTAP 解决方案。TiDB 适合高可用、强一致要求较高、数据规模较大等各种应用场景。

<NavColumns>
<NavColumn>
<ColumnTitle>关于 TiDB</ColumnTitle>

- [TiDB 简介](/overview.md)
- [基本功能](/basic-features.md)
- [What's New in TiDB 4.0](/whats-new-in-tidb-4.0.md)
- [与 MySQL 的兼容性](/mysql-compatibility.md)
- [使用限制](/tidb-limitations.md)

</NavColumn>

<NavColumn>
<ColumnTitle>快速上手</ColumnTitle>

- [快速上手指南](/quick-start-with-tidb.md)
- [SQL 基本操作](/basic-sql-operations.md)

</NavColumn>

<NavColumn>
<ColumnTitle>部署使用</ColumnTitle>

- [软硬件环境需求](/hardware-and-software-requirements.md)
- [环境与系统配置检查](/check-before-deployment.md)
- [使用 TiUP 部署（推荐）](/production-deployment-using-tiup.md)
- [使用 TiFlash](/tiflash/tiflash-overview.md)
- [在 Kubernetes 上部署](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)

</NavColumn>

<NavColumn>
<ColumnTitle>数据迁移</ColumnTitle>

- [概述](/migration-overview.md)
- [使用 Dumpling 与 TiDB Lightning 进行全量迁移](/migrate-from-mysql-dumpling-files.md)
- [从 Aurora 全量迁移](/migrate-from-aurora-using-lightning.md)
- [从 Aurora/MySQL 持续迁移](/migrate-from-aurora-mysql-database.md)
- [从 CSV 文件迁移](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)
- [从 SQL 文件迁移](/migrate-from-mysql-dumpling-files.md)

</NavColumn>

<NavColumn>
<ColumnTitle>运维操作</ColumnTitle>

- [升级 TiDB 版本](/upgrade-tidb-using-tiup.md)
- [扩容与缩容](/scale-tidb-using-tiup.md)
- [备份与恢复](/br/backup-and-restore-tool.md)
- [TiCDC 运维操作及任务管理](/ticdc/manage-ticdc.md)
- [TiUP 常用运维操作](/maintain-tidb-using-tiup.md)
- [TiFlash 常用运维操作](/tiflash/maintain-tiflash.md)

</NavColumn>

<NavColumn>
<ColumnTitle>监控告警</ColumnTitle>

- [监控框架概述](/tidb-monitoring-framework.md)
- [监控 API](/tidb-monitoring-api.md)
- [部署监控](/deploy-monitoring-services.md)
- [将 Grafana 监控数据导出成快照](/exporting-grafana-snapshots.md)
- [TiDB 集群报警规则与处理方法](/alert-rules.md)
- [TiFlash 报警规则与处理方法](/tiflash/tiflash-alert-rules.md)

</NavColumn>

<NavColumn>
<ColumnTitle>故障诊断</ColumnTitle>

- [定位慢查询](/identify-slow-queries.md)
- [分析慢查询](/analyze-slow-queries.md)
- [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)
- [热点问题处理](/troubleshoot-hot-spot-issues.md)
- [磁盘 I/O 过高](/troubleshoot-high-disk-io.md)
- [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)
- [TiFlash 常见问题](/tiflash/troubleshoot-tiflash.md)

</NavColumn>

<NavColumn>
<ColumnTitle>参考指南</ColumnTitle>

- [TiDB 架构](/tidb-architecture.md)
- [监控指标](/grafana-overview-dashboard.md)
- [安全加固](/enable-tls-between-clients-and-servers.md)
- [权限管理](/privilege-management.md)
- [基于角色的访问控制](/role-based-access-control.md)
- [证书鉴权](/certificate-authentication.md)

</NavColumn>

<NavColumn>
<ColumnTitle>FAQ</ColumnTitle>

- [产品 FAQ](/faq/tidb-faq.md)
- [高可用 FAQ](/faq/high-availability-faq.md)
- [SQL FAQ](/faq/sql-faq.md)
- [部署运维 FAQ](/faq/deploy-and-maintain-faq.md)
- [升级 FAQ](/faq/upgrade-faq.md)
- [迁移 FAQ](/faq/migration-tidb-faq.md)

</NavColumn>
</NavColumns>
