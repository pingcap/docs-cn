---
title: sink uri 配置规则
category: reference
---

# Sink URI

Sink URI 需要按照以下格式进行配置，目前 scheme 支持 mysql/tidb/kafka

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

## sink uri 配置 mysql/tidb

配置样例

```
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

参数解析

| 参数         | 解析                                             |
| ------------ | ------------------------------------------------ |
| mysql        | 下游数据库连接用户名                             |
| 123456       | 下游数据密码                                     |
| 127.0.0.1    | 下游数据库连接 IP                                |
| 3306         | 下游数据连接端口                                 |
| worker-count | 向下游执行 SQL 的并发度（可选，默认值 16）       |
| max-txn-row  | 向下游执行 SQL 的 batch 大小（可选，默认值 256） |

## sink uri 配置 kakfa

配置样例

```
--sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

参数解析

| 参数               | 解析                                                         |
| ------------------ | ------------------------------------------------------------ |
| 127.0.0.1          | 下游 kafka 对外提供服务的 IP                                 |
| 9092               | 下游数据密码                                                 |
| cdc-test           | 数据同步到 kafka topic 的名字                                |
| kafka-version      | 下游 kafka 版本号（可选，默认值 2.4.0）                      |
| partition-num      | 下游 kafka partition 数量（可选，不能大于实际 partition 数量。如果不填会自动获取 partition 数量） |
| max-message-bytes  | 每次向 kafka broker 发送消息的最大数据量（可选，默认值 64MB） |
| replication-factor | kafka 消息保存副本数（可选，默认值 1）                       |
