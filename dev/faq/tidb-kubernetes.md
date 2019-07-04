---
title: Kubernetes 上的 TiDB 集群常见问题
category: FAQ
---

# Kubernetes 上的 TiDB 集群常见问题

## 时区设置

默认情况下，在 Kubernetes 集群上部署的 TiDB 集群各组件容器中的时区为 UTC，如果要修改时区配置，有下面两种情况：

* 第一次部署集群

    在 TiDB 集群的 `values.yaml` 文件中，修改 `timezone` 配置，例如：`timezone: Asia/Shanghai`，然后部署 TiDB 集群。
* 集群已经在运行

    如果 TiDB 集群已经在运行，需要做如下修改：
    * 在 TiDB 集群 values.yaml 中，修改 timezone 配置，例如：timezone: Asia/Shanghai，然后升级 TiDB 集群。
    * 参考[时区支持](/how-to/configure/time-zone.md)，修改 TiDB 服务时区配置。
