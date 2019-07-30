---
title: TiDB 简介
category: introduction
---

# TiDB 简介

TiDB 是 PingCAP 公司设计的开源分布式 HTAP (Hybrid Transactional and Analytical Processing) 数据库，结合了传统的 RDBMS 和 NoSQL 的最佳特性。TiDB 兼容 MySQL，支持无限的水平扩展，具备强一致性和高可用性。TiDB 的目标是为 OLTP (Online Transactional Processing) 和 OLAP (Online Analytical Processing) 场景提供一站式的解决方案。

TiDB 具备如下特性：

- 高度兼容 MySQL

    [大多数情况下](/reference/mysql-compatibility.md)，无需修改代码即可从 MySQL 轻松迁移至 TiDB，分库分表后的 MySQL 集群亦可通过 TiDB 工具进行实时迁移。

- 水平弹性扩展

    通过简单地增加新节点即可实现 TiDB 的水平扩展，按需扩展吞吐或存储，轻松应对高并发、海量数据场景。

- 分布式事务

    TiDB 100% 支持标准的 ACID 事务。

- 真正金融级高可用

    相比于传统主从 (M-S) 复制方案，基于 Raft 的多数派选举协议可以提供金融级的 100% 数据强一致性保证，且在不丢失大多数副本的前提下，可以实现故障的自动恢复 (auto-failover)，无需人工介入。

- 一站式 HTAP 解决方案

    TiDB 作为典型的 OLTP 行存数据库，同时兼具强大的 OLAP 性能，配合 TiSpark，可提供一站式 HTAP 解决方案，一份存储同时处理 OLTP & OLAP，无需传统繁琐的 ETL 过程。

- 云原生 SQL 数据库

    TiDB 是为云而设计的数据库，支持公有云、私有云和混合云，配合 [TiDB Operator 项目](/reference/tidb-operator-overview.md) 可实现自动化运维，使部署、配置和维护变得十分简单。

TiDB 的设计目标是 100% 的 OLTP 场景和 80% 的 OLAP 场景，更复杂的 OLAP 分析可以通过 [TiSpark 项目](/reference/tispark.md)来完成。

TiDB 对业务没有任何侵入性，能优雅的替换传统的数据库中间件、数据库分库分表等 Sharding 方案。同时它也让开发运维人员不用关注数据库 Scale 的细节问题，专注于业务开发，极大的提升研发的生产力。

三篇文章了解 TiDB 技术内幕：

- [说存储](https://pingcap.com/blog-cn/tidb-internal-1/)
- [说计算](https://pingcap.com/blog-cn/tidb-internal-2/)
- [谈调度](https://pingcap.com/blog-cn/tidb-internal-3/)

## 部署方式

TiDB 可以部署在本地和云平台上，支持公有云、私有云和混合云。你可以根据实际场景或需求，选择相应的方式来部署 TiDB 集群：

- [使用 Ansible 部署](/how-to/deploy/orchestrated/ansible.md)：如果用于生产环境，推荐使用 Ansible 部署 TiDB 集群。
- [使用 Ansible 离线部署](/how-to/deploy/orchestrated/offline-ansible.md)：如果部署环境无法访问网络，可使用 Ansible 进行离线部署。
- [使用 TiDB Operator 部署](/how-to/deploy/tidb-operator.md)：使用 TiDB Operator 在 Kubernetes 集群上部署生产就绪的 TiDB 集群，支持[部署到 AWS EKS](/how-to/deploy/orchestrated/tidb-in-kubernetes/aws-eks.md)、[部署到阿里云 ACK](dev/how-to/deploy/orchestrated/tidb-in-kubernetes/alibaba-cloud.md) 等。
- [使用 Docker Compose 部署](/how-to/get-started/deploy-tidb-from-docker-compose.md)：如果你只是想测试 TiDB、体验 TiDB 的特性，或者用于开发环境，可以使用 Docker Compose 在本地快速部署 TiDB 集群。该部署方式不适用于生产环境。
- [使用 Docker 部署](/how-to/deploy/orchestrated/docker.md)：你可以使用 Docker 部署 TiDB 集群，但该部署方式不适用于生产环境。
- [使用 TiDB Operator 部署到 Minikube](/how-to/get-started/deploy-tidb-from-kubernetes-minikube.md)：你可以使用 TiDB Opeartor 将 TiDB 集群部署到本地 Minikube 启动的 Kubernetes 集群中。该部署方式不适用于生产环境。
- [使用 TiDB Operator 部署到 DinD](/how-to/get-started/deploy-tidb-from-kubernetes-dind.md)：你可以使用 TiDB Operator 将 TiDB 集群部署到本地以 DinD 方式启动的 Kubernetes 集群中。该部署方式不适用于生产环境。

## 项目源码

TiDB 集群所有组件的源码均可从 GitHub 上直接访问：

- [TiDB](https://github.com/pingcap/tidb)
- [TiKV](https://github.com/tikv/tikv)
- [PD](https://github.com/pingcap/pd)
- [TiSpark](https://github.com/pingcap/tispark)
- [TiDB Operator](https://github.com/pingcap/tidb-operator)
