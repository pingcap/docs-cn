---
title: TiCDC 数据正确性校验
summary: 了解 TiCDC 数据正确性校验功能
---

# 基于 Checksum 的单行数据正确性校验

从 v7.1.0 版本开始，TiCDC 支持单行数据正确性校验，该功能基于单行数据的 Checksum 实现，可以被用于佐证一行数据变更从 TiDB 写入，经由 TiCDC 流出，写入到 Kafka 集群的过程中，该行数据是正确的。

本文档介绍如何启用该功能。

## 启用单行数据 Checksum 功能

该功能仅支持下游是 Kafka Sink 的 Changefeed，支持 Canal-JSON / Avro / Open-Protocol 等协议。

1. 首先用户需要在 TiDB 开启行数据 Checksum 功能，执行如下 SQL 语句：

```sql
```

2. 在创建 Changefeed 的 `--config` 参数所指定的配置文件中，添加如下配置:

```toml
[Integrity]
integrity-check-level="correctness"
corruption-handle-level="warn"
```

3. 当使用 Canal-JSON 或 Avro 作为数据编码格式的时候，需要在 `sink-uri` 中设置 `enable-tidb-extension` 为 true。除此之外，使用 Avro 时，还需要设置 `avro-decimal-handling-mode` 为 `string`, `avro-bigint-unsigned-handling-mode` 为 `string`

经由上述配置的 Changefeed，会在每一条写入到 Kafka 的消息中，携带有该条消息对应数据的 Checksum，用户可以根据该 Checksum 的值做数据一致性校验工作。

## 基于 Checksum 的数据校验