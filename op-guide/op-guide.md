---
title: TiDB 运维文档
category: deployment
---

# TiDB 运维文档

## 软硬件环境需求

- [软硬件环境需求](recommendation.md)

## 部署集群

- [Ansible 部署方案 (强烈推荐)](ansible-deployment.md)
- [离线 Ansible 部署方案 (强烈推荐)](offline-ansible-deployment.md)
- [Docker 部署方案](docker-deployment.md)
- [跨机房部署方案](location-awareness.md)

## 配置集群

- [配置参数](configuration.md)

## 监控集群

- [整体监控框架概述](monitor-overview.md)
- [重要监控指标详解](dashboard-overview-info.md)
- [组件状态 API & 监控](monitor.md)

## 扩容缩容

- [使用 Ansible 扩容缩容](../QUICKSTART.md#tidb-集群扩容缩容方案)
- [集群扩容缩容方案](horizontal-scale.md)

## 升级

- [使用 Ansible 升级](ansible-deployment.md)

## 性能调优

- [TiKV 性能参数调优](tune-tikv.md)

## 备份与迁移

- [备份与恢复](backup-restore.md)
+ [数据迁移](migration.md)
    - [全量导入](migration.md#使用-mydumperloader-全量导入数据)
    - [增量导入](migration.md#使用-syncer-增量导入数据)

## Binary 部署方案

- [Binary 部署方案](binary-deployment.md)
