---
title: TiDB Roadmap
aliases: ['/zh/tidb/v5.0/roadmap','/docs-cn/ROADMAP/','/docs-cn/roadmap/','/docs-cn/stable/roadmap/','/docs-cn/v4.0/roadmap/','/zh/tidb/stable/roadmap','/docs-cn/v3.1/roadmap/','/zh/tidb/v3.1/roadmap','/docs-cn/v3.0/roadmap/','/zh/tidb/v3.0/roadmap','/docs-cn/v2.1/roadmap/','/zh/tidb/v2.1/roadmap']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## 提升系统的稳定性

- [x] `CREATE BINDING` 语句支持绑定 `UPDATE`/`DELETE`/`INSERT` 语句 [#15827](https://github.com/pingcap/tidb/issues/15827)
- [x] 优化同时执行 DDL 和 DML 语句时悲观事务的模型，提升系统稳定性 [#18098](https://github.com/pingcap/tidb/issues/18098)
- [x] 优化延时的抖动 [#18005](https://github.com/pingcap/tidb/issues/18005)

## 提升系统性能，降低系统延时

- [x] 优化批量删除的性能 [#18028](https://github.com/pingcap/tidb/issues/18028)
- [x] 优化系统内存管理，降低系统占用内存的量 [#17479](https://github.com/pingcap/tidb/issues/17479)
- [ ] 提升索引选择的准确性和鲁棒性 [#18065](https://github.com/pingcap/tidb/issues/18065)
- [ ] 提升在分区表上裁剪分区和访问数据的性能 [#18016](https://github.com/pingcap/tidb/issues/18016)
- [x] 支持异步提交数据，写完预写阶段的语句能直接返回客户端，降低系统延时 [#8316](https://github.com/tikv/tikv/issues/8316)
- [x] 支持聚族索引 [#4841](https://github.com/pingcap/tidb/issues/4841)
- [ ] 支持跨地区部署，分区表支持配置地理位置策略 [#18273](https://github.com/pingcap/tidb/issues/18273)

## 提升系统安全性

### 认证方式

- [x] TiFlash 支持 TLS 功能 [#18080](https://github.com/pingcap/tidb/issues/18080)
- [x] TiDB 集群内部通信支持 TLS 功能 [#529](https://github.com/pingcap/tiup/issues/529)
- [x] TiUP 支持 SSH LDAP 扩展 [#528](https://github.com/pingcap/tiup/issues/528)

### 透明数据加密

- [ ] TiFlash 支持透明数据加密 [#18082](https://github.com/pingcap/tidb/issues/18082)
- [ ] PD 支持透明数据加密 [#18262](https://github.com/pingcap/tidb/issues/18262)

### 数据脱敏

- [x] TiDB 的日志支持脱敏 [#18034](https://github.com/pingcap/tidb/issues/18034)

## 降低成本

- [ ] 优化在 AWS i3.xlarge/i3.2xlarge 配置上运行 TiDB 的性能和稳定性 [#18025](https://github.com/pingcap/tidb/issues/18025)
- [ ] 优化 TiDB 存储使用云盘的性能和稳定性，例如：AWS EBS gp2 [#18024](https://github.com/pingcap/tidb/issues/18024)

## 新功能

- [ ] 恢复到任意时间点 (PITR) [#325](https://github.com/pingcap/br/issues/325)
- [ ] 支持修改列的类型 [#17526](https://github.com/pingcap/tidb/issues/17526)
- [ ] 提升发现及诊断性能问题的效率，降低用户的使用成本 [#18867](https://github.com/pingcap/tidb/issues/18867)
- [x] 字符集的排序规则支持 `utf8mb4_unicode_ci` 和 `utf8_unicode_ci` [#17596](https://github.com/pingcap/tidb/issues/17596)
- [ ] 数据导入
    - [ ] TiDB Lightning 支持检测导入数据中的冲突
    - [ ] TiDB Lightning 支持分布式并行导入
- [ ] 数据复制：TiCDC 兼容 TiDB Binlog 相关的特性，降低 TiDB Binlog 用户使用 TiCDC 的成本 [#690](https://github.com/pingcap/ticdc/issues/690)
    - [ ] 支持输出数据到文件系统和云端存储 (S3/GCS)
- [ ] 数据容灾：容灾中支持快照级别的一致性数据复制 [#691](https://github.com/pingcap/ticdc/issues/691)
    - [ ] 支持 TiDB 灾备集群在主集群遇到灾难时将备用集群复制到快照级别的一致状态
- [ ] 支持通过 API 管理 TiCDC [#736](https://github.com/pingcap/ticdc/issues/736)
- [x] 数据共享：TiCDC 支持 Avro 接收器，使 TiCDC 与 Kafka connect 兼容 [#660](https://github.com/pingcap/ticdc/issues/660)
- [ ] 支持 Spark 3.0 [#1173](https://github.com/pingcap/tispark/issues/1173)
- [x] 支持 `EXCEPT`/`INTERSECT` 操作 [#18031](https://github.com/pingcap/tidb/issues/18031)
- [x] 支持将云上的 RDS 迁移到 TiDB，例如：云上的 MySQL 或者 Aurora [#18629](https://github.com/pingcap/tidb/issues/18629)

## TiDB Operator

参见 [TiDB Operator Roadmap](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/roadmap)。
