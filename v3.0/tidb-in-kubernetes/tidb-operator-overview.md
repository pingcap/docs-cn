---
title: Overview of TiDB Operator
summary: Learn the overview of TiDB Operator.
category: reference
---

# Overview of TiDB Operator

TiDB Operator is an automatic operation system for TiDB clusters in Kubernetes. It provides a full management life-cycle for TiDB including deployment, upgrades, scaling, backup, fail-over, and configuration changes. With TiDB Operator, TiDB can run seamlessly in the Kubernetes clusters deployed on a public or private cloud.

## Architecture of TiDB Operator

![TiDB Operator Overview](/media/tidb-operator-overview.png)

TiDB Operator consists of the following components:

* `TidbCluster` is a custom resource defined using CRD (`CustomResourceDefinition`) to describe the desired state of the TiDB cluster;
* `tidb-controller-manager` is a set of custom controllers in Kubernetes. These controllers constantly compare the desired state recorded in the `TidbCluster` object with the actual state of the TiDB cluster. They adjust the resources in Kubernetes to drive the TiDB cluster to meet the desired state;
* `tidb-scheduler` is a Kubernetes scheduler extension that injects the TiDB specific scheduling policies to the Kubernetes scheduler;
* `tkctl` is the command-line interface for TiDB clusters in Kubernetes. It is used for cluster operations and troubleshooting cluster issues.

![TiDB Operator Control Flow](/media/tidb-operator-control-flow.png)

The diagram above is the analysis of the control flow of TiDB Operator. Because TiDB clusters also need components such as monitoring, initialization, scheduled backup, Binlog and so on, TiDB Operator encapsulates the definition of these components in the Helm chart. The overall control process is as follows:

1. The user creates a `TidbCluster` object and a corresponding series of Kubernetes-native objects through Helm, such as a `CronJob` that performs scheduled backups;
2. TiDB Operator watches `TidbCluster` and other related objects, and constantly adjust the `StatefulSet` and `Service` objects of PD, TiKV, and TiDB based on the actual state of the cluster;
3. Kubernetes' native controller creates, updates, and deletes the corresponding `Pod` based on objects such as `StatefulSet`, `Deployment`, and `CronJob`;
4. In the `Pod` declaration of PD, TiKV, and TiDB, the `tidb-scheduler` scheduler is specified. `tidb-scheduler` applies the specific scheduling logic of TiDB when scheduling the corresponding `Pod`.

Based on the above declarative control flow, TiDB Operator automatically performs health check and fault recovery for the cluster nodes. You can easily modify the `TidbCluster` object declaration to perform operations such as deployment, upgrade and scaling.

## Manage TiDB clusters using TiDB Operator

TiDB Operator provides several ways to deploy TiDB clusters in Kubernetes:

+ For test environment:
    - [DinD](tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind.md): Deploy TiDB clusters in a local DinD environment using TiDB Operator
    - [Minikube](tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-minikube.md): Deploy TiDB clusters in a local Minikube environment using TiDB Operator
    - [GKE](tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-gke.md): Deploy TiDB clusters on GKE using TiDB Operator

+ For production environment:
    - On public cloud: see [Deploy TiDB on AWS EKS](tidb-in-kubernetes/deploy/aws-eks.md), [Deploy TiDB on GCP GKE](tidb-in-kubernetes/deploy/gcp-gke.md), or [Deploy TiDB on Alibaba Cloud Kubernetes](tidb-in-kubernetes/deploy/alibaba-cloud.md) to deploy TiDB clusters for a production environment on a specific public cloud and perform subsequent operation tasks;
    - In an existing Kubernetes cluster: first install TiDB Operator in a Kubernetes cluster according to [Deploy TiDB Operator in Kubernetes](tidb-in-kubernetes/deploy/tidb-operator.md), then deploy your TiDB clusters according to [TiDB in General Kubernetes](tidb-in-kubernetes/deploy/general-kubernetes.md). You also need to adjust the configuration of the Kubernetes cluster based on [Prerequisites for TiDB in Kubernetes](tidb-in-kubernetes/deploy/prerequisites.md) and configure the local PV for your Kubernetes cluster to achieve low latency of local storage for TiKV according to [Local PV Configuration](tidb-in-kubernetes/reference/configuration/local-pv.md).

Before deploying TiDB on any of the above two environments, you can always refer to [TiDB Cluster Configuration Document](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md) to customize TiDB configurations.

After the deployment is complete, see the following documents to use, operate, and maintain TiDB clusters in Kubernetes:

+ [Manage the TiDB Cluster](tidb-in-kubernetes/maintain/tidb-cluster.md)
+ [Access the TiDB Cluster](tidb-in-kubernetes/deploy/access-tidb.md)
+ [Scale TiDB Cluster](tidb-in-kubernetes/scale-in-kubernetes.md)
+ [Upgrade TiDB Cluster](tidb-in-kubernetes/upgrade/tidb-cluster.md#upgrade-the-version-of-tidb-cluster)
+ [Change the Configuration of TiDB Cluster](tidb-in-kubernetes/upgrade/tidb-cluster.md#change-the-configuration-of-tidb-cluster)
+ [Backup and Restore](tidb-in-kubernetes/maintain/backup-and-restore.md)
+ [Automatic Failover](tidb-in-kubernetes/maintain/auto-failover.md)
+ [Monitor a TiDB Cluster in Kubernetes](tidb-in-kubernetes/monitor/tidb-in-kubernetes.md)
+ [Collect TiDB Logs in Kubernetes](tidb-in-kubernetes/maintain/log-collecting.md)

When a problem occurs and the cluster needs diagnosis, you can:

+ See [TiDB FAQs in Kubernetes](tidb-in-kubernetes/faq.md) for any available solution;
+ See [Troubleshoot TiDB in Kubernetes](tidb-in-kubernetes/troubleshoot.md) to shoot troubles.

TiDB in Kubernetes provides a dedicated command-line tool `tkctl` for cluster management and auxiliary diagnostics. Meanwhile, some of TiDB's tools are used differently in Kubernetes. You can:

+ Use `tkctl` according to [`tkctl` Guide](tidb-in-kubernetes/reference/tools/tkctl.md );
+ See [Tools in Kubernetes](tidb-in-kubernetes/reference/tools/in-kubernetes.md) to understand how TiDB tools are used in Kubernetes.

Finally, when a new version of TiDB Operator is released, you can refer to [Upgrade TiDB Operator](tidb-in-kubernetes/upgrade/tidb-operator.md) to upgrade to the latest version.
