---
title: TiDB 运维文档
category: deployment
---

# TiDB 运维文档

## 软硬件环境需求

- [软硬件环境需求](recommendation.md)

## 部署集群

- [Ansible 部署方案 (强烈推荐)](ansible-deployment.md)
- [离线 Ansible 部署方案](offline-ansible-deployment.md)
- [Docker 部署方案](docker-deployment.md)
- [跨数据中心部署方案](cross-dc-deployment.md)

## 配置集群

- [配置参数](configuration.md)
- [使用 Ansible 变更组件配置](ansible-deployment-rolling-update.md#变更组件配置)

## 监控集群

- [整体监控框架概述](monitor-overview.md)
- [重要监控指标详解](dashboard-overview-info.md)
- [组件状态 API & 监控](monitor.md)

## 扩容缩容

- [集群扩容缩容方案](horizontal-scale.md)
- [使用 Ansible 扩容缩容](ansible-deployment-scale.md)

## 升级

- [使用 Anisble 升级组件版本](ansible-deployment-rolling-update.md#升级组件版本)
- [TiDB 2.0 升级操作指南](tidb-v2.0-upgrade-guide.md)
- [TiDB 2.1 升级操作指南](tidb-v2.1-upgrade-guide.md)

## 性能调优

- [TiKV 性能参数调优](tune-tikv.md)

## 备份与迁移

- [备份与恢复](backup-restore.md)
+ [数据迁移](migration.md)
    - [全量导入](migration.md#使用-mydumperloader-全量导入数据)
    - [增量导入](migration.md#使用-syncer-增量导入数据)
