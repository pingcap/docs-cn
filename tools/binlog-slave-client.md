---
title: binlog slave client 用户文档
category: tools
---

## binlog slave client 用户文档

目前 Drainer 提供了多种输出方式，包括 MySQL、TiDB、TheFlash、pb 格式文件等。但是用户往往有一些自定义的需求，比如输出到 Elasticsearch、Hive 等，这些需求 Drainer 现在还没有实现，因此 Drainer 增加了输出到 kafka 的功能，将 binlog 数据解析后按一定的格式再输出到 kafka 中，用户再编写代码从 Kafka 中读出数据进行处理。

### 配置 Drainer

修改 Drainer 的配置文件，设置输出为 Kafka，相关配置如下：

```
[syncer]
db-type = "kafka"

[syncer.to]
# Kafka 地址
kafka-addrs = "127.0.0.1:9092"
# Kafka 版本号
kafka-version = "0.8.2.0"
```

### 自定义开发
#### 数据格式
首先需要了解 Drainer 写入到 Kafka 中的数据格式。数据格式的具体定义在 [binlog.proto](https://github.com/pingcap/tidb-tools/blob/master/tidb_binlog/slave_binlog_proto/proto/binlog.proto)

