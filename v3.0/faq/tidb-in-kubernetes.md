---
title: TiDB FAQs in Kubernetes
summary: Learn about TiDB FAQs in Kubernetes.
category: FAQ
---

# TiDB FAQs in Kubernetes

This document collects frequently asked questions (FAQs) about the TiDB cluster in Kubernetes.

## How to modify time zone settings？

The default time zone setting for each component container of a TiDB cluster in Kubernetes is UTC. To modify this setting, take the steps below based on your cluster status:

* If it is the first time you deploy the cluster:

    In the `values.yaml` file of the TiDB cluster, modify the `timezone` setting. For example, you can set it to `timezone: Asia/Shanghai` before you deploy the TiDB cluster.

* If the cluster is running:

    * In the `values.yaml` file of the TiDB cluster, modify `timezone` settings in the `values.yaml` file of the TiDB cluster. For example, you can set it to `timezone: Asia/Shanghai` and then upgrade the TiDB cluster.
    * Refer to [Time Zone Support](/v3.0/how-to/configure/time-zone.md) to modify TiDB service time zone settings.
