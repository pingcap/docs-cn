---
title: TiDB Binlog 术语表
summary: 学习 TiDB Binlog 相关术语
aliases: ['/docs-cn/v3.0/tidb-binlog/tidb-binlog-glossary/','/docs-cn/v3.0/reference/tidb-binlog/glossary/']
---

# TiDB Binlog 术语表

本文档介绍 TiDB Binlog 相关术语。

## Binlog

在 TiDB Binlog 中，Binlog 通常 TiDB 写的 Binlog 数据，注意 TiDB Binlog 的格式跟 MySQL 不同，也指 Drainer 写到 Kafka 或者文件的 Binlog 数据，但他们的格式不一样。

## Binlog event

TiDB 写的 DML Binlog 有 3 种 event, 分别是 Insert, Update, Delete, Drainer 监控面板 可以看到对应同步数据不同 event 的个数。

## Checkpoint

Checkpoint 指保存的断点信息，记录了 Drainer 同步到下游的 commit-ts，Drainer 重启时可以读取 checkpoint 接着从对应 commit-ts 同步数据到下游。

## Safe mode

指增量复制过程中，用于支持在表结构中存在主键或唯一索引的条件下可重复导入 DML 的模式。

该模式的主要特点为将来自上游的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE` 后再向下游执行。在 Drainer 启动的前 5 分钟会自动启动 Safe mode，另外也可以配置文件中通过 `safe-mode` 参数手动开启。

该配置仅对下游是 MySQL/TiDB 有效。
