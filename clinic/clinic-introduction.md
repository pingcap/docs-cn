---
title: PingCAP Clinic Overview
summary: Learn about the PingCAP Clinic Diagnostic Service (PingCAP Clinic), including tool components, user scenarios, and implementation principles.
---

# PingCAP Clinic Overview

PingCAP Clinic Diagnostic Service (PingCAP Clinic) is a diagnostic service provided by PingCAP for TiDB clusters that are deployed using either TiUP or TiDB Operator. This service helps to troubleshoot cluster problems remotely and provides a quick check of cluster status locally. With PingCAP Clinic, you can ensure the stable operation of your TiDB cluster for its full life-cycle, predict potential problems, reduce the probability of problems, troubleshoot cluster problems quickly, and fix cluster problems.

PingCAP Clinic is currently in the Technical Preview stage. This service provides the following two components to diagnose cluster problems:

- Diag client:

    Diag client (Diag) is a diagnostic tool deployed on the cluster side. Diag is used to collect cluster diagnostic data, upload diagnostic data to the Clinic Server, and perform a quick health check locally on your cluster. For a full list of diagnostic data that can be collected by Diag, see [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md).

    > **Note:**
    >
    > Diag temporarily **does not support** collecting data from the clusters deployed using TiDB Ansible.

- Clinic Server:

    Clinic Server is a cloud service deployed in the cloud. By providing diagnostic services in the SaaS model, the Clinic Server can not only receive uploaded diagnostic data but also work as an online diagnostic environment to store data, view data, and provide cluster diagnostic reports.

    Currently, you can upload the collected diagnostic data to [Clinic Server China](https://clinic.pingcap.com.cn) only. The uploaded data is stored in the AWS S3 China (Beijing) region server set up by PingCAP. Clinic Server Global will be provided soon with a new URL and data storage location in one of the AWS S3 regions in North America.

## User scenarios

- Troubleshoot cluster problems remotely

    When your cluster has some problems that cannot be fixed quickly, you can ask for help at [TiDB Community slack channel](https://tidbcommunity.slack.com/archives/CH7TTLL7P) or contact PingCAP technical support. When contacting technical support for remote assistance, you need to save various diagnostic data from the cluster and forward the data to the support staff. In this case, you can use Diag to collect diagnostic data with one click. Diag helps you to collect complete diagnostic data quickly, which can avoid complex manual data collection operations. After collecting data, you can upload the data to the Clinic Server for PingCAP technical support staff to troubleshoot cluster problems. The Clinic Server provides secure storage for uploaded diagnostic data and supports the online diagnosis, which greatly improves the troubleshooting efficiency.

- Perform a quick check on the cluster status locally

    Even if your cluster runs stably now, it is necessary to periodically check the cluster to avoid potential stability risks. You can check the potential health risks of a cluster using the local quick check feature provided by PingCAP Clinic. The PingCAP Clinic Technical Preview version provides a rationality check on cluster configuration items to discover unreasonable configurations and provide modification suggestions.

## Implementation principles

This section introduces the implementation principles about how Diag collects diagnostic data from a cluster.

First, Diag gets cluster topology information from the deployment tool TiUP (tiup-cluster) or TiDB Operator (tidb-operator). Then, Diag collects different types of diagnostic data through various data collection methods as follows:

- Transfer server files through SCP

    For the clusters deployed using TiUP, Diag can collect log files and configuration files directly from the nodes of the target component through the Secure copy protocol (SCP).

- Collect data by running commands remotely through SSH

    For the clusters deployed using TiUP, Diag can connect to the target component system through SSH (Secure Shell) and run commands (such as Insight) to obtain system information, including kernel logs, kernel parameters, and basic information of the system and hardware.

- Collect data through HTTP call

    - By calling the HTTP interface of TiDB components, Diag can get the real-time configuration sampling information and the real-time performance sampling information of TiDB, TiKV, PD, and other components.
    - By calling the HTTP interface of Prometheus, Diag can get alert information and monitoring metrics data.

- Query database parameters through SQL statements

    Using SQL statements, Diag can query system variables and other information of TiDB. To use this method, you need to **additionally provide** the username and password to access TiDB when collecting data.

## Next step

- [Troubleshoot TiDB Cluster Using PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
- [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md)
