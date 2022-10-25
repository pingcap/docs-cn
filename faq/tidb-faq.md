---
title: TiDB 产品常见问题
aliases: ['/docs-cn/dev/faq/tidb-faq/','/docs-cn/dev/faq/tidb/']
---

# TiDB 产品常见问题

## 1.1 TiDB 介绍及整体架构

### 1.1.1 TiDB 是什么？

[TiDB](https://github.com/pingcap/tidb) 是 [PingCAP](https://pingcap.com/about-cn/) 公司自主设计、研发的开源分布式关系型数据库，是一款同时支持在线事务处理与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 的融合型分布式数据库产品，具备水平扩容或者缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 5.7 协议和 MySQL 生态等重要特性。目标是为用户提供一站式 OLTP (Online Transactional Processing)、OLAP (Online Analytical Processing)、HTAP 解决方案。TiDB 适合高可用、强一致要求较高、数据规模较大等各种应用场景。更多详细信息，请参阅 [TiDB 简介](/overview.md)。

### 1.1.2 TiDB 整体架构

参见 [TiDB 整体架构](/tidb-architecture.md)，以及 TiDB 数据库的[存储](/tidb-storage.md)、[计算](/tidb-computing.md)与[调度](/tidb-scheduling.md)。

### 1.1.3 TiDB 是基于 MySQL 开发的吗？

不是。虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

### 1.1.4 TiDB、TiKV、Placement Driver (PD) 主要作用？

- TiDB 是 Server 计算层，主要负责 SQL 的解析、制定查询计划、生成执行器。
- TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据，简而言之，TiKV 是 TiDB 的存储引擎。
- PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

### 1.1.5 TiDB 易用性如何？

TiDB 使用起来很简单，可以将 TiDB 集群当成 MySQL 来用。你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码，同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

### 1.1.6 TiDB 和 MySQL 兼容性如何？

TiDB 支持绝大部分 MySQL 5.7 的语法，但目前还不支持触发器、存储过程、自定义函数、外键约束等。详情参见[与 MySQL 兼容性对比](/mysql-compatibility.md)。

### 1.1.7 TiDB 支持分布式事务吗？

支持。无论是一个地方的几个节点，还是[跨多个数据中心的多个节点](/multi-data-centers-in-one-city-deployment.md)，TiDB 均支持 ACID 分布式事务。

TiDB 事务模型灵感源自 Google Percolator 模型，主体是一个两阶段提交协议，并进行了一些实用的优化。该模型依赖于一个时间戳分配器，为每个事务分配单调递增的时间戳，这样就检测到事务冲突。在 TiDB 集群中，[PD](/tidb-scheduling.md) 承担时间戳分配器的角色。

### 1.1.8 TiDB 支持哪些编程语言？

只要支持 MySQL Client/Driver 的编程语言，都可以直接使用 TiDB。

### 1.1.9 TiDB 是否支持其他存储引擎？

是的，除了 TiKV 之外，TiDB 还支持一些单机存储引擎，比如 UniStore 和 MockTiKV。注意，TiDB 后续版本可能不再支持 MockTiKV。

要查看 TiDB 支持的存储引擎，可使用以下命令：

{{< copyable "shell-regular" >}}

```shell
./bin/tidb-server -h
```

返回结果如下：

```shell
Usage of ./bin/tidb-server:
  -L string
        log level: info, debug, warn, error, fatal (default "info")
  -P string
        tidb server port (default "4000")
  -V    print version information and exit (default false)
.........
  -store string
        registered store name, [tikv, mocktikv, unistore] (default "unistore")
  ......
```

### 1.1.10 除了官方文档，有没有其他 TiDB 知识获取途径？

- [官方文档](https://docs.pingcap.com/zh/)：获取 TiDB 相关知识最主要、最及时的途径。
- [官方博客](https://cn.pingcap.com/blog/)：了解产品技术解读、观点洞察、案例实践。
- [AskTUG 社区论坛](https://asktug.com)：与社区用户、技术专家互动交流。
- [PingCAP Education](https://cn.pingcap.com/education/)：学习线上课程，获得数据库能力认证。

### 1.1.11 TiDB 用户名长度限制？

在 TiDB 中，用户名最长为 32 个字符。

### 1.1.12 TiDB 是否支持 XA？

虽然 TiDB 的 JDBC 驱动用的就是 MySQL JDBC (Connector/J)，但是当使用 Atomikos 的时候，数据源要配置成类似这样的配置：`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`。MySQL JDBC XADataSource 连接 TiDB 的模式目前是不支持的。MySQL JDBC 中配置好的 XADataSource 模式，只对 MySQL 数据库起作用（DML 去修改 redo 等）。

Atomikos 配好两个数据源后，JDBC 驱动都要设置成 XA 模式，然后 Atomikos 在操作 TM 和 RM (DB) 的时候，会通过数据源的配置，发起带有 XA 指令到 JDBC 层。JDBC 层 XA 模式启用的情况下，会对 InnoDB（如果是 MySQL 的话）下发操作一连串 XA 逻辑的动作，包括 DML 去变更 redo log 等，就是两阶段递交的那些操作。TiDB 目前的引擎版本中，没有对上层应用层 JTA/XA 的支持，不解析这些 Atomikos 发过来的 XA 类型的操作。

MySQL 是单机数据库，只能通过 XA 来满足跨数据库事务，而 TiDB 本身就通过 Google 的 Percolator 事务模型支持分布式事务，性能稳定性比 XA 要高出很多，所以不会也不需要支持 XA。

## 1.2 TiDB 原理

### 1.2.1 存储 TiKV 详细解读

[三篇文章了解 TiDB 技术内幕 - 说存储](https://cn.pingcap.com/blog/tidb-internal-1)

### 1.2.2 计算 TiDB 详细解读

[三篇文章了解 TiDB 技术内幕 - 说计算](https://cn.pingcap.com/blog/tidb-internal-2)

### 1.2.3 调度 PD 详细解读

[三篇文章了解 TiDB 技术内幕 - 谈调度](https://cn.pingcap.com/blog/tidb-internal-3)
