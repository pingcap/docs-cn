---
title: 通用
category: faq-product
---

# 通用

## TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。支持水平扩展、高可用、ACID 事务、SQL 等特性。同时 TiDB 还支持 MySQL 语法和 MySQL 协议。

## TiDB 是基于 MySQL 开发的吗？

不是。虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

## TiDB 和 TiKV 是如何配合使用？ 他们之间的关系是？

TiDB 是 SQL 层，主要负责 SQL 的解析、制定查询计划、生成执行器；TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据。简而言之，TiKV 是 TiDB 的存储引擎。

## Placement Driver (PD) 是做什么的？

PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

## TiDB 用起来简单吗？

是的，TiDB 用起来很简单。启动整套服务后，就可以将 TiDB 当做一个普通的 MySQL Server 来用，你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码。同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

## TiDB 适用的场景是？

原业务的 MySQL 的业务遇到单机容量或者性能瓶颈时，可以考虑使用 TiDB 无缝替换 MySQL。TiDB 可以提供如下特性：

+ 吞吐、存储和计算能力的水平扩展
+ 水平伸缩时不停服务
+ 强一致性
+ 分布式 ACID 事务

## TiDB 不适用于哪些场景？

如果你的应用数据量小 (所有数据千万级别行以下)，且没有高可用、强一致性或者多数据中心复制等要求，那么就不适合使用 TiDB。

## TiDB 的强一致特性是什么样的？

TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致。单个副本失效时，不影响数据的可靠性。

## TiDB 支持分布式事务吗？

TiDB 支持 ACID 分布式事务。事务模型是以 Google 的 Percolator 模型为基础，并做了一些优化。这个模型需要一个时间戳分配器，分配唯一且递增的时间戳。在 TiDB 集群中，PD 承担时间戳分配器的角色。

## 在使用 TiDB 时，我需要用什么编程语言？

可以用任何你喜欢的编程语言，只要该语言有 MySQL Client/Driver。

## 和 MySQL/Oracle 等传统关系型数据库相比，TiDB 有什么优势？

和这些数据库相比，TiDB 最大的特点是可以无限水平扩展，在此过程中不损失事务特性。

## 和 Cassandra/Hbase/MongoDB 等 NoSQL 数据库相比，TiDB 有什么优势？

TiDB 在提供水平扩展特性的同时，还能提供 SQL 以及分布式事务。


## 使用 go get 方式安装 TiDB 为什么报错了？

请手动将TiDB克隆到GOPATH目录，然后运行 `make` 命令。TiDB是一个项目而不是一个库，它的依赖比较复杂，并且parser也是根据 `parser.y` 生成的，我们不支持 `go get` 方式，而是使用 Makefile 来管理。

如果你是开发者并且熟悉Go语言，你可以尝试在TiDB项目的根目录运行 `make parser; ln -s _vendor/src vendor` ，之后就可以使用 `go run`, `go test` `go install` 等命令，但是并不推荐这种做法。




