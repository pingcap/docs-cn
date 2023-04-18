---
title: TiCDC 数据正确性校验
summary: 介绍 TiCDC 数据正确性校验功能的实现原理和使用方法。
---

# TiCDC 数据正确性校验

从 v7.1.0 开始，TiCDC 引入了单行数据正确性校验功能，该功能基于 Checksum 算法对单行数据的正确性进行校验。该功能可以校验一行数据从 TiDB 写入、通过 TiCDC 同步，到写入 Kafka 集群的过程中是否出现错误。TiCDC 数据正确性校验功能仅支持下游是 Kafka 的 Changefeed，目前支持 Avro 协议。

## 实现原理

在启用单行数据 Checksum 正确性校验功能后，TiDB 使用 CRC32 算法计算该行数据的 Checksum 值，并将其一并写入 TiKV。TiCDC 从 TiKV 读取数据，根据相同的算法重新计算 Checksum。如果该值与 TiDB 写入的值相同，则可以证明数据在 TiDB 至 TiCDC 的传输过程中是正确的。

TiCDC 将数据编码成特定格式并发送至 Kafka。Kafka Consumer 读取数据后，可以使用与 TiDB 相同的算法计算得到新的 Checksum。将此值与数据中携带的 Checksum 值进行比较，若二者一致，则可证明从 TiCDC 至 Kafka Consumer 的传输链路上的数据是正确的。

## 启用功能

TiCDC 数据正确性校验功能默认关闭，要使用该功能，请执行以下步骤：

1. 首先，你需要在上游 TiDB 中开启行数据 Checksum 功能 ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入))：

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    上述配置仅对新创建的会话生效，因此需要重新连接 TiDB。

2. 在创建 Changefeed 的 `--config` 参数所指定的配置文件中，添加如下配置：

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3. 当使用 Avro 作为数据编码格式时，你需要在 [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 中设置 [`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)，同时还需设置 [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 和 [`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)。下面是一个配置示例：

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    通过上述配置，Changefeed 会在每条写入 Kafka 的消息中携带该消息对应数据的 Checksum，你可以根据此 Checksum 的值进行数据一致性校验。

## 关闭功能

TiCDC 默认关闭单行数据的 Checksum 校验功能。若要在开启此功能后将其关闭，请执行以下步骤：

1. 首先，按照 [TiCDC 更新同步任务配置](/ticdc/ticdc-manage-changefeed.md#更新同步任务配置)的说明，按照 `暂停任务 -> 修改配置 -> 恢复任务` 的流程，在 Changefeed 的 `--config` 参数所指定的配置文件中移除 `[Integrity]` 的所有配置。

2. 在上游 TiDB 中关闭行数据 Checksum 功能 ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入))，执行如下 SQL 语句：

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    上述配置仅对新创建的会话生效。在所有写入 TiDB 的客户端都完成数据库连接重建后，Changefeed 写入 Kafka 的消息中将不再携带该条消息对应数据的 Checksum 值。
