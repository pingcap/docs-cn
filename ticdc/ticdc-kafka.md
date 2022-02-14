# 从 TiDB 输出数据变更流到 Kafka

* kafka producer 说明，以及相关配置项
* changefeed 创建过程说明，sink-uri 示例
* 介绍常用配置 filter / dispatcher

open protocol 问题


# Protocol

* 引导用户使用 canal-json 协议，其他协议不必体现

# 运维操作

* 修改 topic 的 partitions 数量

# Kafka 集群配置推荐

# FAQ

频繁遇到 kafka message size too large 问题
