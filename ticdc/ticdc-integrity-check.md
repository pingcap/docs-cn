---
title: TiCDC 单行数据正确性校验
summary: 介绍 TiCDC 数据正确性校验功能的实现原理和使用方法。
---

# TiCDC 单行数据正确性校验

从 v7.1.0 开始，TiCDC 引入了单行数据正确性校验功能。该功能基于 [Checksum 算法](#checksum-算法)，校验一行数据从 TiDB 写入、通过 TiCDC 同步，到写入 Kafka 集群的过程中数据内容是否发生错误。目前，仅下游为 Kafka 且协议为 Simple 或 Avro 的 Changefeed 支持该功能。关于 Checksum 值的计算规则，请参考 [Checksum 计算规则](#checksum-计算规则)。

## 启用功能

TiCDC 数据正确性校验功能默认关闭，要使用该功能，请执行以下步骤：

1. 首先，你需要在上游 TiDB 中开启行数据 Checksum 功能 ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入))：

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    上述配置仅对新创建的会话生效，因此需要重新连接 TiDB。

2. 在创建 Changefeed 的 `--config` 参数所指定的[配置文件中](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明)，添加如下配置：

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3. 当使用 Avro 作为数据编码格式时，你需要在 [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 中设置 [`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)。同时，为了防止数值类型在网络传输过程中发生精度丢失，导致 Checksum 校验失败，还需要设置 [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka) 和 [`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)。下面是一个配置示例：

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-checksum" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    通过上述配置，Changefeed 会在每条写入 Kafka 的消息中携带该消息对应数据的 Checksum，你可以根据此 Checksum 的值进行数据一致性校验。

    > **注意：**
    >
    > 对于已有 Changefeed，如果未设置 `avro-decimal-handling-mode` 和 `avro-bigint-unsigned-handling-mode`，开启 Checksum 校验功能时会引起 Schema 不兼容问题。可以通过修改 Schema Registry 的兼容性为 `NONE` 解决该问题。详情可参考 [Schema 兼容性](https://docs.confluent.io/platform/current/schema-registry/fundamentals/avro.html#no-compatibility-checking)。

## 关闭功能

TiCDC 默认关闭单行数据的 Checksum 校验功能。若要在开启此功能后将其关闭，请执行以下步骤：

1. 首先，按照 [TiCDC 更新同步任务配置](/ticdc/ticdc-manage-changefeed.md#更新同步任务配置)的说明，按照 `暂停任务 -> 修改配置 -> 恢复任务` 的流程更新 Changefeed 的配置内容。在 Changefeed 的 `--config` 参数所指定的配置文件中调整 `[integrity]` 的配置内容为：

    ```toml
    [integrity]
    integrity-check-level = "none"
    corruption-handle-level = "warn"
    ```

2. 在上游 TiDB 中关闭行数据 Checksum 功能 ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-从-v710-版本开始引入))，执行如下 SQL 语句：

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    上述配置仅对新创建的会话生效。在所有写入 TiDB 的客户端都完成数据库连接重建后，Changefeed 写入 Kafka 的消息中将不再携带该条消息对应数据的 Checksum 值。

## Checksum 算法

### Checksum V1

在 v8.4.0 之前，TiDB 和 TiCDC 采用 Checksum v1 算法进行 Checksum 计算和校验。

在启用单行数据 Checksum 正确性校验功能后，TiDB 会使用 CRC32 算法计算每行数据的 Checksum 值，并将这个值与该行数据一并存储在 TiKV 中。随后，TiCDC 从 TiKV 读取这些数据，并使用相同的算法重新计算 Checksum，如果得到的 Checksum 值与 TiDB 写入的 Checksum 值相同，则表明数据在从 TiDB 到 TiCDC 的传输过程中是正确的。

TiCDC 将数据编码成特定格式并发送至 Kafka。Kafka Consumer 读取数据后，可以使用与 TiDB 相同的 CRC32 算法计算得到新的 Checksum，将此值与数据中携带的 Checksum 值进行比较，若二者一致，则表明从 TiCDC 到 Kafka Consumer 的传输链路上的数据是正确的。

### Checksum V2

从 v8.4.0 开始，TiDB 和 TiCDC 引入 Checksum V2 算法，解决了 Checksum V1 在执行 `ADD COLUMN` 或 `DROP COLUMN` 后无法正确校验 Update 或 Delete 事件中 Old Value 数据的问题。

对于 v8.4.0 及之后新创建的集群，或从之前版本升级到 v8.4.0 的集群，启用单行数据 Checksum 正确性校验功能后，TiDB 默认使用 Checksum V2 算法进行 Checksum 计算和校验。TiCDC 支持同时处理 V1 和 V2 两种 Checksum。该变更仅影响 TiDB 和 TiCDC 内部实现，不影响下游 Kafka consumer 的 Checksum 计算校验方法。

## Checksum 计算规则

Checksum 计算算法的伪代码如下：

```
fn checksum(columns) {
    let result = 0
    for column in sort_by_schema_order(columns) {
        result = crc32.update(result, encode(column))
    }
    return result
}
```

* `columns` 应该按照 column ID 排序。在 Avro schema 中，各个字段已经按照 column ID 的顺序排序，因此可以直接按照此顺序排序 `columns`。

* `encode(column)` 函数将 column 的值编码为字节，编码规则取决于该 column 的数据类型。具体规则如下：

    * TINYINT、SMALLINT、INT、BIGINT、MEDIUMINT 和 YEAR 类型会被转换为 UINT64 类型，并按照小端序编码。例如，数字 `0x0123456789abcdef` 会被编码为 `hex'0x0123456789abcdef'`。
    * FLOAT 和 DOUBLE 类型会被转换为 DOUBLE 类型，然后转换为 IEEE754 格式的 UINT64 类型。
    * BIT、ENUM 和 SET 类型会被转换为 UINT64 类型。

        * BIT 类型按照二进制转换为 UINT64 类型。
        * ENUM 和 SET 类型按照其对应的 INT 值转换为 UINT64 类型。例如，`SET('a','b','c')` 类型 column 的数据值为 `'a,c'`，则该值将被编码为 `0b101`，即 `5`。

    * TIMESTAMP、DATE、DURATION、DATETIME、JSON 和 DECIMAL 类型会被转换为 STRING 类型，然后转换为字节。
    * CHAR、VARCHAR、VARSTRING、STRING、TEXT、BLOB（包括 TINY、MEDIUM 和 LONG）等字符类型，会直接使用字节。
    * NULL 和 GEOMETRY 类型不会被纳入到 Checksum 计算中，返回空字节。

基于 Golang 的 Avro 数据消费和 Checksum 校验，可以参考 [TiCDC 行数据 Checksum 校验](/ticdc/ticdc-avro-checksum-verification.md)。

> **注意：**
>
> - 开启 Checksum 校验功能后，DECIMAL 和 UNSIGNED BIGINT 类型的数据会被转换为字符串类型。因此在下游消费者代码中需要将其转换为对应的数值类型，然后进行 Checksum 相关计算。
> - Delete 事件只含有 Handle Key 列的内容，而 Checksum 是基于所有列计算的，所以 Delete 事件不参与到 Checksum 的校验中。