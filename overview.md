---
title: TiDB Introduction
summary: Learn how to quickly start a TiDB cluster.
category: introduction
aliases: ['/docs/dev/overview/']
---

# TiDB Introduction

[TiDB](https://github.com/pingcap/tidb) ("Ti" stands for Titanium) is an open-source NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability.

TiDB can be deployed on-premise or in-cloud. The following deployment options are officially supported by PingCAP:

- [TiUP Deployment](/production-deployment-using-tiup.md): This guide describes how to deploy TiDB using [TiUP](https://github.com/pingcap-incubator/tiup). It is strongly recommended for production deployment.
- [Docker Deployment](/test-deployment-using-docker.md): This guide describes how to deploy TiDB using Docker.
- [Docker Compose Deployment](/deploy-test-cluster-using-docker-compose.md): This guide describes how to deploy TiDB using Docker compose. You can follow this guide to quickly deploy a TiDB cluster for testing and development on your local drive.
- Kubernetes Deployment:

    You can use [TiDB Operator](https://github.com/pingcap/tidb-operator) to deploy TiDB on:

    - [AWS EKS (Elastic Kubernetes Service)](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/deploy-on-aws-eks)
    - [GKE (Google Kubernetes Engine)](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/deploy-on-gcp-gke)
    - [Google Cloud Shell](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/deploy-tidb-from-kubernetes-gke)
    - [Alibaba Cloud ACK (Container Service for Kubernetes)](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/deploy-on-alibaba-cloud)

    Or deploy TiDB locally using:

    - [kind](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/get-started#create-a-kubernetes-cluster-using-kind)
    - [Minikube](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/get-started#create-a-kubernetes-cluster-using-minikube)

- [Binary Tarball Deployment](/production-deployment-from-binary-tarball.md): This guide describes how to deploy TiDB from a binary tarball in production. Guides for [development](/deploy-tidb-from-binary.md) and [testing](/test-deployment-from-binary-tarball.md) environments are also available.

## Community provided blog posts & tutorials

The following list collects deployment guides and tutorials from the community. The content is subject to change by the contributors.

- [How To Spin Up an HTAP Database in 5 Minutes with TiDB + TiSpark](https://pingcap.com/blog/how_to_spin_up_an_htap_database_in_5_minutes_with_tidb_tispark/)
- [Developer install guide (single machine)](http://www.tocker.ca/this-blog-now-powered-by-wordpress-tidb.html)
- [TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/)

_Your contribution is also welcome! Feel free to open a [pull request](https://github.com/pingcap/docs/blob/master/overview.md) to add additional links._

## Source code

Source code for [all components of the TiDB platform](https://github.com/pingcap) is available on GitHub.

- [TiDB](https://github.com/pingcap/tidb)
- [TiKV](https://github.com/tikv/tikv)
- [PD](https://github.com/pingcap/pd)
- [TiSpark](https://github.com/pingcap/tispark)
- [TiDB Operator](https://github.com/pingcap/tidb-operator)
