---
title: TiDB 快速入门指南
category: deployment
---

# TiDB 快速入门指南

作为开源分布式 HTAP (Hybrid Transactional and Analytical Processing) 数据库，TiDB 可以部署在本地和云平台上，支持公有云、私有云和混合云。

## TiDB 部署方式

你可以根据实际场景或需求，选择相应的方式来部署 TiDB 集群：

- [使用 Ansible 部署](op-guide/ansible-deployment.md)：如果用于生产环境，须使用 Ansible 部署 TiDB 集群。
- [使用 Ansible 离线部署](op-guide/offline-ansible-deployment.md)：如果部署环境无法访问网络，可使用 Ansible 进行离线部署。
- [使用 Docker Compose 部署](op-guide/docker-compose.md)：如果你只是想测试 TiDB、体验 TiDB 的特性，或者用于开发环境，可以使用 Docker Compose 在本地快速部署 TiDB 集群。该部署方式不适用于生产环境。
- [使用 Docker 部署](op-guide/docker-deployment.md)：你可以使用 Docker 部署 TiDB 集群，但该部署方式不适用于生产环境。

## 项目源码

TiDB 集群所有组件的源码均可从 GitHub 上直接访问：

- [TiDB](https://github.com/pingcap/tidb)
- [TiKV](https://github.com/tikv/tikv)
- [PD](https://github.com/pingcap/pd)
- [TiSpark](https://github.com/pingcap/tispark)
- [TiDB Operator](https://github.com/pingcap/tidb-operator)