---
title: Software and Hardware Recommendations
summary: Learn the software and hardware recommendations for deploying and running TiDB.
category: how-to
aliases: ['/docs/op-guide/recommendation/']
---

# Software and Hardware Recommendations

## About

As an open source distributed NewSQL database with high performance, TiDB can be deployed in the Intel architecture server and major virtualization environments and runs well. TiDB supports most of the major hardware networks and Linux operating systems.

## Linux OS version requirements

| Linux OS Platform        | Version      |
| :-----------------------:| :----------: |
| Red Hat Enterprise Linux | 7.3 or later |
| CentOS                   | 7.3 or later |
| Oracle Enterprise Linux  | 7.3 or later |
| Ubuntu LTS               | 16.04 or later |

> **Note:**
>
> - For Oracle Enterprise Linux, TiDB supports the Red Hat Compatible Kernel (RHCK) and does not support the Unbreakable Enterprise Kernel provided by Oracle Enterprise Linux.
> - A large number of TiDB tests have been run on the CentOS 7.3 system, and in our community there are a lot of best practices in which TiDB is deployed on the Linux operating system. Therefore, it is recommended to deploy TiDB on CentOS 7.3 or later.
> - The support for the Linux operating systems above includes the deployment and operation in physical servers as well as in major virtualized environments like VMware, KVM and XEN.

## Server recommendations

You can deploy and run TiDB on the 64-bit generic hardware server platform in the Intel x86-64 architecture. The requirements and recommendations about server hardware configuration for development, test and production environments are as follows:

### Development and test environments

| Component | CPU     | Memory | Local Storage  | Network  | Instance Number (Minimum Requirement) |
| :------: | :-----: | :-----: | :----------: | :------: | :----------------: |
| TiDB    | 8 core+   | 16 GB+  | No special requirements | Gigabit network card | 1 (can be deployed on the same machine with PD)      |
| PD      | 4 core+   | 8 GB+  | SAS, 200 GB+ | Gigabit network card | 1 (can be deployed on the same machine with TiDB)       |
| TiKV    | 8 core+   | 32 GB+  | SAS, 200 GB+ | Gigabit network card | 3       |
|         |         |         |              | Total Server Number |  4      |

> **Note**:
>
> - In the test environment, the TiDB and PD instances can be deployed on the same server.
> - For performance-related test, do not use low-performance storage and network hardware configuration, in order to guarantee the correctness of the test result.
> - For the TiKV server, it is recommended to use NVMe SSDs to ensure faster reads and writes.
> - The TiDB server uses the disk to store server logs, so there are no special requirements for the disk type and capacity in the test environment.

### Production environment

| Component | CPU | Memory | Hard Disk Type | Network | Instance Number (Minimum Requirement) |
| :-----: | :------: | :------: | :------: | :------: | :-----: |
|  TiDB  | 16 core+ | 32 GB+ | SAS | 10 Gigabit network card (2 preferred) | 2 |
| PD | 4 core+ | 8 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| TiKV | 16 core+ | 32 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| Monitor | 8 core+ | 16 GB+ | SAS | Gigabit network card | 1 |
|     |     |     |      |  Total Server Number   |    9   |

> **Note**:
>
> - In the production environment, the TiDB and PD instances can be deployed on the same server. If you have a higher requirement for performance and reliability, try to deploy them separately.
> - It is strongly recommended to use higher configuration in the production environment.
> - It is recommended to keep the size of TiKV hard disk within 2 TB if you are using PCIe SSDs or within 1.5 TB if you are using regular SSDs.

## Network requirements

As an open source distributed NewSQL database, TiDB requires the following network port configuration to run. Based on the TiDB deployment in actual environments, the administrator can open relevant ports in the network side and host side.

| Component | Default Port | Description |
| :--:| :--: | :-- |
| TiDB |  4000  | the communication port for the application and DBA tools |
| TiDB | 10080  | the communication port to report TiDB status |
| TiKV | 20160 | the TiKV communication port |
| PD | 2379 | the communication port between TiDB and PD |
| PD | 2380 | the inter-node communication port within the PD cluster |
| Pump | 8250 | the Pump communication port |
| Drainer | 8249 | the Drainer communication port |
| Prometheus | 9090 | the communication port for the Prometheus service|
| Pushgateway | 9091 | the aggregation and report port for TiDB, TiKV, and PD monitor |
| Node_exporter | 9100 | the communication port to report the system information of every TiDB cluster node |
| Blackbox_exporter | 9115 | the Blackbox_exporter communication port, used to monitor the ports in the TiDB cluster |
| Grafana | 3000 | the port for the external Web monitoring service and client (Browser) access|
| Grafana | 8686 | the grafana_collector communication port, used to export the Dashboard as the PDF format |
| Kafka_exporter | 9308 | the Kafka_exporter communication port, used to monitor the binlog Kafka cluster |

## Web browser requirements

TiDB relies on [Grafana](https://grafana.com/) to provide visualization of database metrics. A recent version of Internet Explorer, Chrome or Firefox with Javascript enabled is sufficient.
