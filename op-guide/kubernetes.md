---
title: TiDB Deployment on Kubernetes
summary: Use TiDB Operator to quickly deploy a TiDB cluster on Kubernetes
category: operations
---

# TiDB Deployment on Kubernetes

[TiDB Operator](https://github.com/pingcap/tidb-operator) manages TiDB clusters on [Kubernetes](https://kubernetes.io) 
and automates tasks related to operating a TiDB cluster. It makes TiDB a truly cloud-native database.

> **Warning:** Currently, TiDB Operator is work in progress [WIP] and is NOT ready for production. Use at your own risk.

## Google Kubernetes Engine (GKE)

The TiDB Operator tutorial for GKE runs directly in the Google Cloud Shell.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/pingcap/tidb-operator&tutorial=docs/google-kubernetes-tutorial.md)

## Local install using Docker in Docker

Docker in Docker (DinD) runs Docker containers as virtual machines and runs another layer of Docker containers inside the first layer of Docker containers. `kubeadm-dind-cluster` uses this technology to run the Kubernetes cluster in Docker containers. TiDB Operator uses a modified DinD script to manage the DinD Kubernetes cluster.

[Continue reading tutorial on GitHub &rarr;](https://github.com/pingcap/tidb-operator/blob/master/docs/local-dind-tutorial.md)
