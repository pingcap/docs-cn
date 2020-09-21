---
title: TiDB  Roadmap
category: Roadmap
aliases: ['/docs-cn/ROADMAP/','/docs-cn/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## 提升系统的稳定性

- [ ] [`CREATE BINDING` 语名支持绑定 `update`/`delete`/`insert` 语句](https://github.com/pingcap/tidb/issues/15827)。
- [ ] [优化同时执行 DDL 和 DML 语句时悲观事务的模型，提升系统稳定性](https://github.com/pingcap/tidb/issues/18098)。
- [ ] [优化延时的抖动](https://github.com/pingcap/tidb/issues/18005)。

## 提升系统性能，降低系统延时

- [ ] [优化批量删除的性能](https://github.com/pingcap/tidb/issues/18028)。
- [ ] [优化系统内存管理，降低系统占用内存的量](https://github.com/pingcap/tidb/issues/17479)。
- [ ] [提升索引选择的准确性和鲁棒性](https://github.com/pingcap/tidb/issues/18065)。
- [ ] [提升分区表上的分区修剪和数据访问性能](https://github.com/pingcap/tidb/issues/18016)。
- [ ] [支持异步提交数据，写完预写阶段的语句能直接返回客户端，降低系统延时](https://github.com/tikv/tikv/issues/8316)。
- [ ] [支持聚族索引](https://github.com/pingcap/tidb/issues/4841)。
- [ ] [支持跨地区部署，分区表支持配置地理位置策略](https://github.com/pingcap/tidb/issues/18273)。

## 提升系统安全性

### 认证方式

- [ ] [TiFlash 支持 TLS 功能](https://github.com/pingcap/tidb/issues/18080)。
- [ ] [TiDB 集群内部通信息支持 TLS 功能](https://github.com/pingcap/tiup/issues/529)。
- [ ] [TiUP 支持 SSH LDAP 扩展](https://github.com/pingcap/tiup/issues/528)。

### 透明数据加密

- [ ] [TiFlash 支持透明数据加密](https://github.com/pingcap/tidb/issues/18082)。
- [ ] [PD 支持透明数据加密](https://github.com/pingcap/tidb/issues/18262)。

### 数据脱敏

- [ ] [TiDB 的日志支持脱敏](https://github.com/pingcap/tidb/issues/18034)。

## 降低成本

- [ ] [优化在 AWS i3.xlarge/i3.2xlarge 配置上跑 TiDB 的性能和稳定性](https://github.com/pingcap/tidb/issues/18025)。
- [ ] [优化 TiDB 的存储使用云盘性能和稳定性，例如：AWS EBS gp2](https://github.com/pingcap/tidb/issues/18024)。

## 新功能

- [ ] [恢复到任意时间点（PITR)](https://github.com/pingcap/br/issues/325)。
- [ ] [支持修改列的类型](https://github.com/pingcap/tidb/issues/17526)。
- [ ] [字符集的排序规则支持 `utf8mb4_unicode_ci` 和 `utf8_unicode_ci`](https://github.com/pingcap/tidb/issues/17596)。
- [ ] [提升发现及诊断性能问题的效率，降低用户的使用成本](https://github.com/pingcap/tidb/issues/18867)。
- [ ] [TiCDC 兼容 TiDB-Binlog 相关的特性，降低用户使用 TiCDC 的成本](https://github.com/pingcap/ticdc/issues/690)
    - [ ] 支持分类更新和插入一行数据事件。
    - [ ] 通过删除或者更新语句修改一行数据时，系统自动记录原始值。
- [ ] [容灾中支持快照级别的一致性数据复制](https://github.com/pingcap/ticdc/issues/691)。
    - [ ] 支持 MySQL 接收器在上游遇到灾难时将其复制到快照级别的一致状态。
- [ ] [支持通过 API 管理 TiCDC](https://github.com/pingcap/ticdc/issues/736)。
- [ ] [支持 `import` SQL 命令](https://github.com/pingcap/tidb/issues/18089)。
- [ ] [支持 Avro 接收器，使TiCDC 与 Kafka connect 兼容](https://github.com/pingcap/ticdc/issues/660)。
- [ ] [支持 Spark-3.0](https://github.com/pingcap/tispark/issues/1173)。
- [ ] [支持 `EXCEPT`/`INTERSECT`  操作](https://github.com/pingcap/tidb/issues/18031)。
- [ ] [支持通过 TiUP/Operator 部署和运维 DM 2.0](https://github.com/pingcap/tidb-operator/issues/2868)。
- [ ] [TiDB Operator 支持异构设计](https://github.com/pingcap/tidb-operator/issues/2240)。
- [ ] [支持将云上的 RDS 迁移到 TiDB，例如：云上的 MySQL 或者 Aurora](https://github.com/pingcap/tidb/issues/18629)。
