---
title: TiDB FAQs in Kubernetes
summary: Learn about TiDB FAQs in Kubernetes.
category: FAQ
aliases: ['/docs/v3.0/faq/tidb-in-kubernetes/']
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

## Can HPA or VPA be configured on TiDB components?

Currently, the TiDB cluster does not support HPA (Horizontal Pod Autoscaling) or VPA (Vertical Pod Autoscaling), because it is difficult to achieve autoscaling on stateful applications such as a database. Autoscaling can not be achieved merely by the monitoring data of CPU and memory.

## What scenarios require manual intervention when I use TiDB Operator to orchestrate a TiDB cluster?

Besides the operation of the Kubernetes cluster itself, there are the following two scenarios that might require manual intervention when using TiDB Operator:

* Adjusting the cluster after the auto-failover of TiKV. See [Auto-Failover](/v3.0/tidb-in-kubernetes/maintain/auto-failover.md) for details;
* Maintaining or dropping the specified Kubernetes nodes. See [Maintaining Nodes](/v3.0/tidb-in-kubernetes/maintain/kubernetes-node.md) for details.

## What is the recommended deployment topology when I use TiDB Operator to orchestrate a TiDB cluster on a public cloud?

To achieve high availability and data security, it is recommended that you deploy the TiDB cluster in at least three availability zones in a production environment.

In terms of the deployment topology relationship between the TiDB cluster and TiDB services, TiDB Operator supports the following three deployment modes. Each mode has its own merits and demerits, so your choice must be based on actual application needs.

* Deploy the TiDB cluster and TiDB services in the same Kubernetes cluster of the same VPC;
* Deploy the TiDB cluster and TiDB services in different Kubernetes clusters of the same VPC;
* Deploy the TiDB cluster and TiDB services in different Kubernetes clusters of different VPCs.

## Does TiDB Operator support TiSpark?

TiDB Operator does not yet support automatically orchestrating TiSpark.

If you want to add the TiSpark component to TiDB in Kubernetes, you must maintain Spark on your own in **the same** Kubernetes cluster. You must ensure that Spark can access the IPs and ports of PD and TiKV instances, and install the TiSpark plugin for Spark. [TiSpark](/v3.0/reference/tispark.md#deploy-tiSpark-on-the-existing-spark-cluster) offers a detailed guide for you to install the TiSpark plugin.

To maintain Spark in Kubernetes, refer to [Spark on Kubernetes](http://spark.apache.org/docs/latest/running-on-kubernetes.html).

## How to check the configuration of the TiDB cluster?

To check the configuration of the PD, TiKV, and TiDB components of the current cluster, run the following command:

* Check the PD configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <pd-pod-name> -n <namespace> -- cat /etc/pd/pd.toml
    ```

* Check the TiKV configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tikv-pod-name> -n <namespace> -- cat /etc/tikv/tikv.toml
    ```

* Check the TiDB configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tidb-pod-name> -c tidb -n <namespace> -- cat /etc/tidb/tidb.toml
    ```
