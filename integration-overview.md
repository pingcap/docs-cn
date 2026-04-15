---
title: 数据集成概述
summary: 了解使用 TiCDC 进行数据集成的具体场景。
---

# 数据集成概述

数据集成一般是指数据在各个独立的数据源之间流动、转换和汇集。随着数据量的爆炸式增长和数据价值被深度挖掘，对数据集成的需求越来越普遍和迫切。为了避免 TiDB 成为数据孤岛，顺利与各个数据系统进行集成，TiCDC 提供将 TiDB 增量数据变更日志实时同步到其他数据系统的能力。本文介绍一些常用的数据集成场景，你可以依据这些场景选择最适合自己的数据集成方案。

## 与 Confluent Cloud 和 Snowflake、ksqlDB、SQL Server 进行数据集成

你可以使用 TiCDC 将 TiDB 的增量数据同步到 Confluent Cloud，并借助 Confluent Cloud 的能力最终将数据分别同步到 Snowflake、ksqlDB、SQL Server。参见[与 Confluent Cloud 和 Snowflake、ksqlDB、SQL Server 进行数据集成](/ticdc/integrate-confluent-using-ticdc.md)。

## 与 Apache Kafka 和 Apache Flink 进行数据集成

你可以使用 TiCDC 将 TiDB 的增量数据同步到 Apache Kafka，并使用 Apache Flink 消费 Kafka 中的数据。参见[与 Apache Kafka 和 Apache Flink 进行数据集成](/replicate-data-to-kafka.md)。
