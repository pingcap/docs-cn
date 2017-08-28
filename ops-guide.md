# TiDB 运维技术文档
## 目录

+ [软硬件环境需求]()
+ 下载
  - [TiDB, TiKV, PD]()
  - [TiDB Ansible Playbook]()
+ TiDB 简介 & 整体架构
  - [TiDB 简介](overview.md#tidb-简介)
  - [TiDB 整体架构](overview.md#tidb-整体架构)
+ 安装 & 部署
  - [部署建议](op-guide/recommendation.md)
  - [Ansible 部署方案 (强烈推荐)](op-guide/ansible-deployment.md)
  - [Binary 部署方案](op-guide/binary-deployment.md)
  - [Docker 部署方案](op-guide/docker-deployment.md)
  - [跨机房部署方案](op-guide/location-awareness.md)
+ [命令行参数](op-guide/configuration.md)
+ [启动/停止 TiDB 集群]()
+ 运维 & 监控
  - [集群扩容缩容方案](op-guide/horizontal-scale.md)
  - [整体监控框架概述](op-guide/monitor-overview.md)
  - [重要监控指标详解](op-guide/dashboard-overview-info.md)
  - [组件状态 API & 监控](op-guide/monitor.md)
  - [PD 命令行工具](op-guide/pd-control.md)
+ [扩容缩容](op-guide/horizontal-scale.md)  
+ 升级
  - [ansible 升级](op-guide/ansible-deployment.md)
  - [二进制升级]()
+ [备份与恢复]()
+ 性能调优
  - [TiKV 性能参数调优](op-guide/tune-tikv.md) 
+ 导入导出
  - [全量导入](op-guide/migration.md)
  - [增量导入](tools/syncer.md)