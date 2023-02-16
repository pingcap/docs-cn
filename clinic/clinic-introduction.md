---
title: PingCAP Clinic Overview
summary: Learn about the PingCAP Clinic Diagnostic Service (PingCAP Clinic), including tool components, user scenarios, and implementation principles.
---

# PingCAP Clinic Overview

PingCAP Clinic Diagnostic Service (PingCAP Clinic) is a diagnostic service provided by PingCAP for TiDB clusters that are deployed using either TiUP or TiDB Operator. This service helps to troubleshoot cluster problems remotely and provides a quick check of cluster status locally. With PingCAP Clinic, you can ensure the stable operation of your TiDB cluster for its full life-cycle, predict potential problems, reduce the probability of problems, troubleshoot cluster problems quickly, and fix cluster problems.

PingCAP Clinic provides the following two components to diagnose cluster problems:

- Diag client:

    Diag client (Diag) is a diagnostic tool deployed on the cluster side. Diag is used to collect cluster diagnostic data, upload diagnostic data to the Clinic Server, and perform a quick health check locally on your cluster. For a full list of diagnostic data that can be collected by Diag, see [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md).

    > **Note:**
    >
    > Diag supports TiDB v4.0 and later versions, but **does not support** collecting data from clusters deployed using TiDB Ansible.

- Clinic Server:

    Clinic Server is a cloud service deployed in the cloud. By providing diagnostic services in the SaaS model, the Clinic Server can not only receive uploaded diagnostic data but also work as an online diagnostic environment to store data, view data, and provide cluster diagnostic reports. Clinic Server provides two independent services depending on the storage location:

    - [Clinic Server for international users](https://clinic.pingcap.com): Data is stored in AWS in US.
    - [Clinic Server for users in the Chinese mainland](https://clinic.pingcap.com.cn): Data is stored in AWS in China (Beijing) regions.

## User scenarios

- Troubleshoot cluster problems remotely

    When your cluster has some problems that cannot be fixed quickly, you can [get support](/support.md) from PingCAP or the community. When contacting technical support for remote assistance, you need to save various diagnostic data from the cluster and forward the data to the support staff. In this case, you can use Diag to collect diagnostic data with one click. Diag helps you to collect complete diagnostic data quickly, which can avoid complex manual data collection operations. After collecting data, you can upload the data to the Clinic Server for PingCAP technical support staff to troubleshoot cluster problems. The Clinic Server provides secure storage for uploaded diagnostic data and supports the online diagnosis, which greatly improves the troubleshooting efficiency.

- Quickly check cluster status

    Even if your cluster is running stably for now, it is necessary to periodically check the cluster to detect potential stability risks. You can identify potential health risks of a cluster using the local and server-side quick check feature provided by PingCAP Clinic.

## Implementation principles

This section introduces the implementation principles about how Diag collects diagnostic data from a cluster.

First, Diag gets cluster topology information from the deployment tool TiUP (tiup-cluster) or TiDB Operator (tidb-operator). Then, Diag collects different types of diagnostic data through various data collection methods as follows:

- Transfer server files through SCP

    For clusters deployed using TiUP, Diag can collect log files and configuration files directly from the nodes of the target component through the Secure copy protocol (SCP).

- Collect data by running commands remotely through SSH

    For clusters deployed using TiUP, Diag can connect to the target component system through SSH (Secure Shell) and run commands (such as Insight) to obtain system information, including kernel logs, kernel parameters, and basic information of the system and hardware.

- Collect data through HTTP call

    - By calling the HTTP interface of TiDB components, Diag can get the real-time configuration sampling information and the real-time performance sampling information of TiDB, TiKV, PD, and other components.
    - By calling the HTTP interface of Prometheus, Diag can get alert information and monitoring metrics data.

- Query database parameters through SQL statements

    Using SQL statements, Diag can query system variables and other information of TiDB. To use this method, you need to **additionally provide** the username and password to access TiDB when collecting data.

## The limitations of Clinic Server

> **Note:**
>
> - Clinic Server is free from July 15, 2022 to July 14, 2023. You will be notified through email before July 14, 2023 if the service starts charging fee afterwards.
> - If you want to adjust the usage limitations, [get support](/support.md) from PingCAP.

| Service Type| Limitation |
| :------ | :------ |
| Number of clusters | 10/organization |
| Storage capacity | 50 GB/cluster |
| Storage duration | 180 days |
| Data size | 3 GB/package |
| Saving duration of the data rebuild environment | 3 days |

## Next step

- Use PingCAP Clinic in an on-premise environment
    - [Quick Start with PingCAP Clinic](/clinic/quick-start-with-clinic.md)
    - [Troubleshoot Clusters using PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
    - [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md)

- Use PingCAP Clinic on Kubernetes
    - [Troubleshoot TiDB Cluster using PingCAP Clinic](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)
    - [PingCAP Clinic Diagnostic Data](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-data-collection)
