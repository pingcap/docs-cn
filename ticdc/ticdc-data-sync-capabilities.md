---
title: TiCDC 的数据同步能力说明
summary: 了解 TiCDC 的数据同步能力。
---

# TiCDC 的数据同步能力说明

## 背景知识

TiCDC（TiDB Change Data Capture）是 TiDB 生态中用于实时数据同步的核心组件。
1. TiCDC 监听 TiKV 的变更日志（Raft Log），将行数据的增删改操作转换为下游兼容的 SQL 语句。与 Binlog 不同，TiCDC 并不基于上游的 SQL 获取数据变更。参考 [TiCDC 处理数据变更的实现原理](/ticdc/ticdc-overview.md#ticdc-处理数据变更的实现原理)。

2. TiCDC 生成与 SQL 语义等效的逻辑操作（如 INSERT/UPDATE/DELETE），而非逐条还原上游执行的原始 SQL。参考 [TiCDC 处理数据变更的实现原理](/ticdc/ticdc-overview.md#ticdc-处理数据变更的实现原理)。

3. TiCDC 提供事务最终一致性的保证，开启 [redo log](/ticdc/ticdc-sink-to-mysql.md#灾难场景的最终一致性复制) 后提供容灾场景下的最终一致性保证，开启 [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md#启用-syncpoint) 后提供一致性快照读和数据一致性校验。

4. TiCDC 支持同步数据到多类下游，包括 [TiDB 及兼容Mysql 协议的数据库](/ticdc/ticdc-sink-to-mysql.md)，[Kafka](/ticdc/ticdc-sink-to-kafka.md)，[Pulsar](/ticdc/ticdc-sink-to-pulsar), [存储服务（Amazon S3、GCS、Azure Blob Storage 和 NFS](/ticdc/ticdc-sink-to-cloud-storage.md)。

## TiCDC 的数据同步能力

1. TiCDC 支持同步上游执行的 DDL 和 DML 语句，但不同步上游系统表执行的 DDL 和 DML（包括 `mysql.*` 和 `information_schema.*`) ，也不同步上游中创建的临时表。

2. TiCDC 不支持同步 DQL (Data Query Language) 语句，也不支持同步 DCL (Data Control Language) 语句。

3. TiCDC 支持通过 DDL 同步上游表中 Index 的设置 (`add index`， `create index`), 并且为了减小对 Changefeed 同步延迟的影响，如果下游是 TiDB，TiCDC 会[异步执行创建和添加索引的 DDL 操作](/ticdc/ticdc-ddl.md#创建和添加索引-ddl-的异步执行)。

4. 对于表中设定的外键约束，TiCDC 会同步对应的 DDL (`add foreign key`) 语句，但 TiCDC 不负责同步上游系统变量的设置，如 [foreign_key_checks](/system-variables.md#foreign_key_checks) 。因此客户需要自行在下游设置合适的系统变量，以决定下游外键约束检查是否开启。

5. TiCDC 内部只检查收到的上游变更的完整性，不参与检查数据变更是否符合下游各类约束。如遇到不满足下游约束的数据变更，TiCDC 会在写下游时进行报错返回。