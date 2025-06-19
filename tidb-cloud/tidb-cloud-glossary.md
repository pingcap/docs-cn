---
title: TiDB Cloud 术语表
summary: 了解 TiDB Cloud 中使用的术语。
category: glossary
aliases: ['/tidbcloud/glossary']
---

# TiDB Cloud 术语表

## A

### ACID

ACID 指事务的四个关键属性：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability）。每个属性描述如下：

- **原子性**意味着操作的所有更改要么全部执行，要么全部不执行。TiDB 通过确保存储主键的 [TiDB Region](#region) 的原子性来实现事务的原子性。

- **一致性**意味着事务始终将数据库从一个一致的状态转换到另一个一致的状态。在 TiDB 中，在将数据写入内存之前会确保数据一致性。

- **隔离性**意味着正在进行的事务在完成之前对其他事务是不可见的。这允许并发事务在不牺牲一致性的情况下读写数据。TiDB 目前支持 `REPEATABLE READ` 隔离级别。

- **持久性**意味着一旦事务提交，即使在系统故障的情况下也保持提交状态。TiKV 使用持久存储来确保持久性。

## C

### Chat2Query

Chat2Query 是集成在 SQL Editor 中的 AI 驱动功能，可以帮助用户使用自然语言指令生成、调试或重写 SQL 查询。更多信息，请参见[使用 AI 辅助的 SQL Editor 探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

此外，TiDB Cloud 为 TiDB Cloud Serverless 集群提供 Chat2Query API。启用后，TiDB Cloud 将自动创建一个名为 **Chat2Query** 的系统 Data App 和 Data Service 中的 Chat2Data 端点。你可以调用此端点，通过提供指令让 AI 生成和执行 SQL 语句。更多信息，请参见[开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

### Credit（积分）

TiDB Cloud 为概念验证（PoC）用户提供一定数量的积分。一个积分等于一美元。你可以在积分过期前使用积分支付 TiDB 集群费用。

## D

### Data App（数据应用）

[Data Service (beta)](#data-service) 中的 Data App 是可用于访问特定应用程序数据的端点集合。你可以使用 API 密钥配置授权设置，以限制对 Data App 中端点的访问。

更多信息，请参见[管理 Data App](/tidb-cloud/data-service-manage-data-app.md)。

### Data Service（数据服务）

Data Service (beta) 使你能够通过使用自定义 API [端点](#endpoint)通过 HTTPS 请求访问 TiDB Cloud 数据。此功能使用无服务器架构来处理计算资源和弹性扩展，因此你可以专注于端点中的查询逻辑，而无需担心基础设施或维护成本。

更多信息，请参见[Data Service 概述](/tidb-cloud/data-service-overview.md)。

### Direct Customer（直接客户）

直接客户是直接从 PingCAP 购买 TiDB Cloud 并支付账单的最终客户。这与 [MSP 客户](#msp-customer)不同。

## E

### Endpoint（端点）

Data Service 中的端点是可以自定义以执行 SQL 语句的 Web API。你可以为 SQL 语句指定参数，例如在 `WHERE` 子句中使用的值。当客户端调用端点并在请求 URL 中为参数提供值时，端点会使用提供的参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

更多信息，请参见[管理端点](/tidb-cloud/data-service-manage-endpoint.md)。

## F

### Full-text search（全文搜索）

与专注于语义相似性的[向量搜索](/tidb-cloud/vector-search-overview.md)不同，全文搜索让你可以检索精确关键词的文档。在检索增强生成（RAG）场景中，你可以将全文搜索与向量搜索结合使用，以提高检索质量。

更多信息，请参见[使用 SQL 进行全文搜索](/tidb-cloud/vector-search-full-text-search-sql.md)和[使用 Python 进行全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)。

## M

### member（成员）

已被邀请加入组织的用户，可以访问该组织及其集群。

### MPP

从 v5.0 开始，TiDB 通过 TiFlash 节点引入了大规模并行处理（MPP）架构，在 TiFlash 节点之间共享大型连接查询的执行工作负载。当启用 MPP 模式时，TiDB 会根据成本决定是否使用 MPP 框架执行计算。在 MPP 模式下，连接键通过 Exchange 操作在计算时重新分配，这将计算压力分配到每个 TiFlash 节点并加快计算速度。更多信息，请参见[使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### MSP Customer（MSP 客户）

托管服务提供商（MSP）客户是通过 MSP 渠道购买 TiDB Cloud 并支付账单的最终客户。这与[直接客户](#direct-customer)不同。

### Managed Service Provider（托管服务提供商，MSP）

托管服务提供商（MSP）是转售 TiDB Cloud 并提供增值服务的合作伙伴，包括但不限于 TiDB Cloud 组织管理、计费服务和技术支持。

## N

### node（节点）

指数据实例（TiKV）、计算实例（TiDB）或分析实例（TiFlash）。

## O

### organization（组织）

用于管理 TiDB Cloud 账户的实体，包括一个管理账户和任意数量的多个成员账户。

### organization members（组织成员）

组织成员是由组织所有者或项目所有者邀请加入组织的用户。组织成员可以查看组织的成员，并可以被邀请加入组织内的项目。

## P

### policy（策略）

定义应用于角色、用户或组织的权限的文档，例如对特定操作或资源的访问权限。

### project（项目）

基于组织创建的项目，可以根据项目分别管理人员、实例和网络等资源，项目之间的资源不会相互干扰。

### project members（项目成员）

项目成员是被邀请加入组织的一个或多个项目的用户。项目成员可以管理集群、网络访问、备份和其他资源。

## R

### Recycle Bin（回收站）

存储具有有效备份的已删除集群数据的位置。一旦备份的 TiDB Cloud Dedicated 集群被删除，该集群的现有备份文件将被移至回收站。对于自动备份的备份文件，回收站将保留指定时间。你可以在**备份设置**中配置备份保留时间，默认为 7 天。对于手动备份的备份文件，没有过期日期。为避免数据丢失，请及时将数据恢复到新集群。请注意，如果集群**没有备份**，已删除的集群将不会显示在此处。

### region（区域）

- TiDB Cloud region（TiDB Cloud 区域）

    部署 TiDB Cloud 集群的地理区域。TiDB Cloud 区域包含至少 3 个可用区，集群跨这些区域部署。

- TiDB Region

    TiDB 中的基本数据单位。TiKV 将键值空间划分为一系列连续的键段，每个段称为一个 Region。每个 Region 的默认大小限制为 96 MB，可以配置。

### replica（副本）

可以位于相同或不同区域并包含相同数据的单独数据库。副本通常用于灾难恢复或提高性能。

### Replication Capacity Unit（复制容量单位）

changefeed 的复制根据计算资源收费，即 TiCDC 复制容量单位。

### Request Unit（请求单位）

请求单位（RU）是用于表示单个数据库请求消耗的资源量的度量单位。请求消耗的 RU 数量取决于各种因素，例如操作类型或检索或修改的数据量。更多信息，请参见 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

## S

### Spending limit（消费限额）

消费限额指你愿意在特定工作负载上每月花费的最大金额。这是一种成本控制机制，使你能够为 TiDB Cloud Serverless 集群设置预算。对于[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)，消费限额必须设置为最低 0.01 美元。此外，如果符合条件，可扩展集群可以获得免费配额。具有免费配额的可扩展集群将首先使用免费配额。

## T

### TiDB cluster（TiDB 集群）

由 [TiDB](https://docs.pingcap.com/tidb/stable/tidb-computing)、[TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage)、[Placement Driver](https://docs.pingcap.com/tidb/stable/tidb-scheduling)（PD）和 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 节点组成的功能性工作数据库集合。

### TiDB node（TiDB 节点）

从事务或分析存储返回的查询数据进行聚合的计算节点。增加 TiDB 节点数量将增加集群可以处理的并发查询数量。

### TiFlash node（TiFlash 节点）

实时从 TiKV 复制数据并支持实时分析工作负载的分析存储节点。

### TiKV node（TiKV 节点）

存储在线事务处理（OLTP）数据的存储节点。为了实现高可用性，它以 3 个节点的倍数（例如 3、6、9）进行扩展，其中两个节点作为副本。增加 TiKV 节点数量将增加总吞吐量。

### traffic filter（流量过滤器）

允许通过 SQL 客户端访问 TiDB Cloud 集群的 IP 地址和无类域间路由（CIDR）地址列表。流量过滤器默认为空。

## V

### Vector search（向量搜索）

[向量搜索](/tidb-cloud/vector-search-overview.md)是一种优先考虑数据含义以提供相关结果的搜索方法。与依赖精确关键词匹配和词频的传统全文搜索不同，向量搜索将各种数据类型（如文本、图像或音频）转换为高维向量，并基于这些向量之间的相似性进行查询。这种搜索方法捕获数据的语义含义和上下文信息，从而更准确地理解用户意图。即使搜索词与数据库中的内容不完全匹配，向量搜索仍然可以通过分析数据的语义提供符合用户意图的结果。

### Virtual Private Cloud（虚拟私有云）

为你的资源提供托管网络服务的逻辑隔离虚拟网络分区。

### VPC

Virtual Private Cloud（虚拟私有云）的缩写。

### VPC peering（VPC 对等连接）

使你能够连接虚拟私有云（[VPC](#vpc)）网络，以便不同 VPC 网络中的工作负载可以私密通信。

### VPC peering connection（VPC 对等连接）

两个虚拟私有云（VPC）之间的网络连接，使你能够使用私有 IP 地址在它们之间路由流量，并帮助你促进数据传输。
