---
title: Software and Hardware Recommendations
summary: Learn the software and hardware recommendations for deploying and running TiDB.
aliases: ['/docs/dev/hardware-and-software-requirements/','/docs/dev/how-to/deploy/hardware-recommendations/']
---

# Software and Hardware Recommendations

As an open source distributed NewSQL database with high performance, TiDB can be deployed in the Intel architecture server, ARM architecture server, and major virtualization environments and runs well. TiDB supports most of the major hardware networks and Linux operating systems.

## Linux OS version requirements

| Linux OS Platform        | Version      |
| :-----------------------:| :----------: |
| Red Hat Enterprise Linux | 7.3 or later 7.x releases |
| CentOS                   | 7.3 or later 7.x releases |
| Oracle Enterprise Linux  | 7.3 or later 7.x releases |
| Ubuntu LTS               | 16.04 or later |

> **Note:**
>
> - For Oracle Enterprise Linux, TiDB supports the Red Hat Compatible Kernel (RHCK) and does not support the Unbreakable Enterprise Kernel provided by Oracle Enterprise Linux.
> - A large number of TiDB tests have been run on the CentOS 7.3 system, and in our community there are a lot of best practices in which TiDB is deployed on the Linux operating system. Therefore, it is recommended to deploy TiDB on CentOS 7.3 or later.
> - The support for the Linux operating systems above includes the deployment and operation in physical servers as well as in major virtualized environments like VMware, KVM and XEN.
> - Red Hat Enterprise Linux 8.0, CentOS 8 Stream, and Oracle Enterprise Linux 8.0 are not supported yet as the testing of these platforms is in progress.
> - Support for CentOS 8 Linux is not planned because its upstream support ends on December 31, 2021.
> - Support for Ubuntu 16.04 will be removed in future versions of TiDB. Upgrading to Ubuntu 18.04 or later is strongly recommended.

Other Linux OS versions such as Debian Linux and Fedora Linux might work but are not officially supported.

## Software recommendations

### Control machine

| Software | Version |
| :--- | :--- |
| sshpass | 1.06 or later |
| TiUP | 0.6.2 or later |

> **Note:**
>
> It is required that you [deploy TiUP on the control machine](/production-deployment-using-tiup.md#step-2-install-tiup-on-the-control-machine) to operate and manage TiDB clusters.

### Target machines

| Software | Version |
| :--- | :--- |
| sshpass | 1.06 or later |
| numa | 2.0.12 or later |
| tar | any |

## Server recommendations

You can deploy and run TiDB on the 64-bit generic hardware server platform in the Intel x86-64 architecture or on the hardware server platform in the ARM architecture. The requirements and recommendations about server hardware configuration (ignoring the resources occupied by the operating system itself) for development, test, and production environments are as follows:

### Development and test environments

| Component | CPU     | Memory | Local Storage  | Network  | Instance Number (Minimum Requirement) |
| :------: | :-----: | :-----: | :----------: | :------: | :----------------: |
| TiDB    | 8 core+   | 16 GB+  | No special requirements | Gigabit network card | 1 (can be deployed on the same machine with PD)      |
| PD      | 4 core+   | 8 GB+  | SAS, 200 GB+ | Gigabit network card | 1 (can be deployed on the same machine with TiDB)       |
| TiKV    | 8 core+   | 32 GB+  | SAS, 200 GB+ | Gigabit network card | 3       |
| TiFlash | 32 core+  | 64 GB+  | SSD, 200 GB+ | Gigabit network card | 1     |
| TiCDC | 8 core+ | 16 GB+ | SAS, 200 GB+ | Gigabit network card | 1 |

> **Note:**
>
> - In the test environment, the TiDB and PD instances can be deployed on the same server.
> - For performance-related test, do not use low-performance storage and network hardware configuration, in order to guarantee the correctness of the test result.
> - For the TiKV server, it is recommended to use NVMe SSDs to ensure faster reads and writes.
> - If you only want to test and verify the features, follow [Quick Start Guide for TiDB](/quick-start-with-tidb.md) to deploy TiDB on a single machine.
> - The TiDB server uses the disk to store server logs, so there are no special requirements for the disk type and capacity in the test environment.

### Production environment

| Component | CPU | Memory | Hard Disk Type | Network | Instance Number (Minimum Requirement) |
| :-----: | :------: | :------: | :------: | :------: | :-----: |
|  TiDB  | 16 core+ | 32 GB+ | SAS | 10 Gigabit network card (2 preferred) | 2 |
| PD | 4 core+ | 8 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| TiKV | 16 core+ | 32 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| TiFlash | 48 core+ | 128 GB+ | 1 or more SSDs | 10 Gigabit network card (2 preferred) | 2 |
| TiCDC | 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred) | 2 |
| Monitor | 8 core+ | 16 GB+ | SAS | Gigabit network card | 1 |

> **Note:**
>
> - In the production environment, the TiDB and PD instances can be deployed on the same server. If you have a higher requirement for performance and reliability, try to deploy them separately.
> - It is strongly recommended to use higher configuration in the production environment.
> - It is recommended to keep the size of TiKV hard disk within 2 TB if you are using PCIe SSDs or within 1.5 TB if you are using regular SSDs.

Before you deploy TiFlash, note the following items:

- TiFlash can be [deployed on multiple disks](/tiflash/tiflash-configuration.md#multi-disk-deployment).
- It is recommended to use a high-performance SSD as the first disk of the TiFlash data directory to buffer the real-time replication of TiKV data. The performance of this disk should not be lower than that of TiKV, such as PCI-E SSD. The disk capacity should be no less than 10% of the total capacity; otherwise, it might become the bottleneck of this node. You can deploy ordinary SSDs for other disks, but note that a better PCI-E SSD brings better performance. 
- It is recommended to deploy TiFlash on different nodes from TiKV. If you must deploy TiFlash and TiKV on the same node, increase the number of CPU cores and memory, and try to deploy TiFlash and TiKV on different disks to avoid interfering each other.
- The total capacity of the TiFlash disks is calculated in this way: `the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas`. For example, if the overall planned capacity of TiKV is 1 TB, the number of TiKV replicas is 3, and the number of TiFlash replicas is 2, then the recommended total capacity of TiFlash is `1024 GB / 3 * 2`. You can replicate only the data of some tables. In such case, determine the TiFlash capacity according to the data volume of the tables to be replicated.

Before you deploy TiCDC, note that it is recommended to deploy TiCDC on PCIe-SSD disks larger than 200 GB.

## Network requirements

As an open source distributed NewSQL database, TiDB requires the following network port configuration to run. Based on the TiDB deployment in actual environments, the administrator can open relevant ports in the network side and host side.

| Component | Default Port | Description |
| :--:| :--: | :-- |
| TiDB |  4000  | the communication port for the application and DBA tools |
| TiDB | 10080  | the communication port to report TiDB status |
| TiKV | 20160 | the TiKV communication port |
| TiKV |  20180 | the communication port to report TiKV status |
| PD | 2379 | the communication port between TiDB and PD |
| PD | 2380 | the inter-node communication port within the PD cluster |
| TiFlash | 9000 | the TiFlash TCP service port |
| TiFlash | 8123 | the TiFlash HTTP service port |
| TiFlash | 3930 | the TiFlash RAFT and Coprocessor service port |
| TiFlash | 20170 |the TiFlash Proxy service port |
| TiFlash | 20292 | the port for Prometheus to pull TiFlash Proxy metrics |
| TiFlash | 8234 | the port for Prometheus to pull TiFlash metrics |
| Pump | 8250 | the Pump communication port |
| Drainer | 8249 | the Drainer communication port |
| TiCDC | 8300 | the TiCDC communication port |
| Prometheus | 9090 | the communication port for the Prometheus service|
| Node_exporter | 9100 | the communication port to report the system information of every TiDB cluster node |
| Blackbox_exporter | 9115 | the Blackbox_exporter communication port, used to monitor the ports in the TiDB cluster |
| Grafana | 3000 | the port for the external Web monitoring service and client (Browser) access|
| Alertmanager | 9093 | the port for the alert web service |
| Alertmanager | 9094 | the alert communication port |

## Web browser requirements

TiDB relies on [Grafana](https://grafana.com/) to provide visualization of database metrics. A recent version of Internet Explorer, Chrome or Firefox with Javascript enabled is sufficient.
