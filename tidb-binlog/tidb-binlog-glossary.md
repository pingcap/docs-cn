---
title: TiDB Binlog 术语表
summary: 学习 TiDB Binlog 相关术语
---

# TiDB Binlog 术语表

本文档介绍 TiDB Binlog 相关术语。

## Binlog

在 TiDB Binlog 中，Binlog 通常指 TiDB 写的二进制日志数据，也指 Drainer 写到 Kafka 或者文件的二进制日志数据，前者与后者的格式不同。此外，TiDB 的 binlog 格式与 MySQL 的 binlog 格式也不同。

## Binlog event

TiDB 写的 DML Binlog 有 3 种 event，分别为：`INSERT`、`UPDATE` 和 `DELETE`。在 Drainer 监控面板上可以看到同步数据对应的不同 event 的个数。

## Checkpoint

Checkpoint 指保存的断点信息，记录了 Drainer 同步到下游的 commit-ts。Drainer 重启时可以读取 checkpoint，并从对应的 commit-ts 开始同步数据到下游。

## Safe mode

Safe mode 指增量复制过程中，当表结构中存在主键或唯一索引时，用于支持幂等导入 DML 的模式。

该模式将来自上游的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE`，然后再向下游执行。在 Drainer 启动的前 5 分钟，会自动启动 Safe mode；另外也可以在配置文件中通过 `safe-mode` 参数手动开启，但该配置仅在下游是 MySQL 或 TiDB 时有效。
