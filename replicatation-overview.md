---
title: 数据同步场景综述
summary: 了解使用 TiCDC 进行数据同步的具体场景。
---

# 数据同步场景综述

本文档总体介绍可用于 TiDB 的数据同步方案。

## 从 TiDB 同步数据至 Confluent Cloud

你可以使用 TiCDC 将 TiDB 的增量数据同步到 Confluent Cloud，并借助 Confluent Cloud 的能力最终将数据分别同步到 ksqlDB、Snowflake、SQL Server。

[从 TiDB 同步数据至 Confluent Cloud](/replicate-from-tidb-to-confluent.md)

## 从 TiDB 同步数据至 Apache Kafka 和 Apache Flink

[从 TiDB 同步数据至 Apache Kafka 和 Apache Flink](/replicate-from-tidb-to-kafka-flink.md)

## 从 TiDB 同步数据至与 MySQL 兼容的数据库
