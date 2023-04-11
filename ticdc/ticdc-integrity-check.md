---
title: TiCDC 数据正确性校验
summary: 了解 TiCDC 数据正确性校验功能
---

# 基于 Checksum 的单行数据正确性校验

从 v7.1.0 版本开始，TiCDC 新增了单行数据正确性校验功能，该功能基于 Checksum 算法对单行数据的正确性进行校验。通过该功能可以校验一行数据从 TiDB 写入、经由 TiCDC 流出，再写入到 Kafka 集群的过程中是否发生了数据错误。该功能仅支持下游是 Kafka Sink 的 Changefeed，支持 Canal-JSON / Avro / Open-Protocol 等协议。

本文档介绍了如何在 TiCDC 中启用或关闭单行数据校验功能，并提供该功能的基本原理。

## 启用功能


* 首先用户需要在上游 TiDB 开启行数据 Checksum 功能，执行如下 SQL 语句：

```sql
SET GLOBAL enable_row_level_checksum = true; 
```

上述配置仅对新创建的会话生效，因此需要重新链接 TiDB。


* 在创建 Changefeed 的 `--config` 参数所指定的配置文件中，添加如下配置:

```toml
[Integrity]
integrity-check-level="correctness"
corruption-handle-level="warn"
```

* 当使用 Canal-JSON 或 Avro 作为数据编码格式的时候，需要在 `sink-uri` 中设置 `enable-tidb-extension` 为 true。除此之外，使用 Avro 时，还需要设置 `avro-decimal-handling-mode` 为 `string`, `avro-bigint-unsigned-handling-mode` 为 `string`

经由上述配置的 Changefeed，会在每一条写入到 Kafka 的消息中，携带有该条消息对应数据的 Checksum，用户可以根据该 Checksum 的值做数据一致性校验工作。

## 关闭功能

* 首先按照 [TiCDC 更新同步任务配置](/ticdc/ticdc-manage-changefeed.md#更新同步任务配置) 的说明，通过`暂停任务 -> 修改配置 -> 恢复任务` 的流程，在 Changefeed 的 `--config` 参数所指定的配置文件中移除 `Integrity` 表的所有配置。

* 用户在上游 TiDB 关闭行数据 Checksum 功能，执行如下 SQL 语句
    ```sql
    SET GLOBAL enable_row_level_checksum = false; 
    ```

请注意，上述配置仅对新创建的会话生效。当所有写入 TiDB 的客户端都完成数据库连接重建后，Changefeed 写入 Kafka 的消息中就不再携带有该条消息对应数据的 Checksum 值。

## 实现原理

TiDB 在启用了 Row Checksum 功能后，使用 CRC32 算法，对该行数据计算一个 Checksum 值，一并写入到 TiKV。TiCDC 从 TiKV 中读取出数据，根据相同的算法，重新计算一遍 Checksum，如果该值和 TiDB 写入的值相同，那么可以说明数据在 TiDB 到 TiCDC 的链路上是正确的。TiCDC 将数据编码成特定的格式，发送到 Kafka，Kafka Consumer 读取出数据之后，可以使用和 TiDB 相同的算法，计算得到一个新的 Checksum，将该值和数据中携带的 Checksum 值进行对比，二者一致则可说明从 TiCDC 到 Kafka Consumer 的链路上数据是正确的。
