---
title: 数据集成场景综述
summary: 了解使用 TiCDC 进行数据集成的具体场景。
---

# 数据集成场景综述

本文档总体介绍可用于 TiDB 的数据集成方案。

## 与 Confluent Cloud 进行数据集成

您可以使用 TiCDC 将 TiDB 的增量数据同步到 Confluent Cloud，并借助 Confluent Cloud 的能力最终将数据分别同步到 ksqlDB、Snowflake、SQL Server。

[与 Confluent Cloud 进行数据集成](/replicate-from-tidb-to-confluent.md)

## 与 Apache Kafka 和 Apache Flink 进行数据集成

您可以使用 TiCDC 将 TiDB 的增量数据同步到 Apache Kafka，并使用 Apache Flink 消费 Kafka 中的数据。

[与 Apache Kafka 和 Apache Flink 进行数据集成](/replicate-from-tidb-to-kafka-flink.md)

