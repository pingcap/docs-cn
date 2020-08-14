---
title: TiDB  Roadmap
category: Roadmap
aliases: ['/docs-cn/ROADMAP/','/docs-cn/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## 提升系统的稳定性

- [ ] `CREATE BINDING` 语名支持绑定 `update`/`delete`/`insert` 语句。
- [ ] 优化同时执行 DDL 和 DML 语句时悲观事务的模型，提升系统稳定性。
- [ ] 优化延时的抖动。

## 提升系统性能，降低系统延时

- [ ] 优化批量删除的性能。
- [ ] 优化系统内存管理，降低系统占用内存的量。
- [ ] 提升索引选择的准确性和鲁棒性。
- [ ] 提升分区表上的分区修剪和数据访问性能。
- [ ] 异步提交数据。
- [ ] 支持聚族索引。
- [ ] 支持跨地区部署，分区表支持配置地理位置策略。

## 提升系统安全性

### 认证方式

- [ ] TiFlash 支持 TLS 功能。
- [ ] TiDB 集群内部通信息支持 TLS 功能。 
- [ ] TiUP 支持 SSH LDAP 扩展。

### 透明数据加密

- [ ] TiFlash 支持透明数据加密。
- [ ] PD 支持透明数据加密。

### 数据脱敏

- [ ] TiDB 的日志支持脱敏。

## 降低成本

- [ ] 优化在 AWS i3.xlarge/i3.2xlarge 配置上跑 TiDB 的性能和稳定性。
- [ ] 优化 TiDB 的存储使用云盘性能和稳定性，例如：AWS EBS gp2。
- [ ] 提升发现及诊断性能问题的效率，降低用户的使用成本。

## 新功能

- [ ] 恢复到任意时间点（PITR)。
- [ ] 支持修改列的类型。
- [ ] TiDB DBaaS 支持根据策略自动弹性伸缩。
- [ ] 字符集的排序规则支持 `utf8mb4_unicode_ci` 和 `utf8_unicode_ci`。
- [ ] TiCDC 兼容 TiDB-Binlog 相关的特性，降低用户使用 TiCDC 的成本
    - [ ] 支持分类更新和插入一行数据事件。
    - [ ] 通过删除或者更新语句修改一行数据时，系统自动记录原始值。
- [ ] 容灾中支持快照级别的一致性数据复制
    - [ ] 支持 MySQL 接收器在上游遇到灾难时将其复制到快照级别的一致状态。
- [ ] 支持通过 SQL 语句管理 TiCDC。
- [ ] 支持通过 API 管理 TiCDC 。
- [ ] 支持 `import` SQL 命令。
- [ ] 支持 Avro 接收器，使TiCDC 与 Kafka connect 兼容。
- [ ] 支持 Spark-3.0。
- [ ] 支持 `EXCEPT`/`INTERSECT`  操作。
- [ ] 支持直接写入数据到 TiFlash。
- [ ] 支持通过 TiUP/Operator 部署和运维 DM 2.0。
- [ ] TiDB Operator 支持跨数据中心或者多个区域部署 TiDB 集群。
- [ ] TiDB Operator 支持异构设计。
- [ ] 支持将云上的 RDS 迁移到 TiDB，例如：云上的 MySQL 或者 Aurora。

