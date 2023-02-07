---
title: Software and Hardware Recommendations
summary: Learn the software and hardware recommendations for deploying and running TiDB.
aliases: ['/docs/dev/hardware-and-software-requirements/','/docs/dev/how-to/deploy/hardware-recommendations/']
---

# Software and Hardware Recommendations

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

As an open-source distributed SQL database with high performance, TiDB can be deployed in the Intel architecture server, ARM architecture server, and major virtualization environments and runs well. TiDB supports most of the major hardware networks and Linux operating systems.

## OS and platform requirements

|  Operating systems   |   Supported CPU architectures   |
|   :---   |   :---   |
| Red Hat Enterprise Linux 8.4 or a later 8.x version  |  <ul><li>x86_64</li><li>ARM 64</li></ul>  |
| <ul><li>Red Hat Enterprise Linux 7.3 or a later 7.x version</li><li>CentOS 7.3 or a later 7.x version</li></ul>  |  <ul><li>x86_64</li><li>ARM 64</li></ul>   |
| Amazon Linux 2 | <ul><li>x86_64</li><li>ARM 64</li></ul> |
| Kylin Euler V10 SP1/SP2   |   <ul><li>x86_64</li><li>ARM 64</li></ul>   |
| UOS V20                 |   <ul><li>x86_64</li><li>ARM 64</li></ul>   |
|   macOS Catalina or later   |  <ul><li>x86_64</li><li>ARM 64</li></ul>  |
|  Oracle Enterprise Linux 7.3 or a later 7.x version  |  x86_64           |
|   Ubuntu LTS 18.04 or later   |  x86_64           |
| CentOS 8 Stream | <ul><li>x86_64</li><li>ARM 64</li></ul> |
|  Debian 9 (Stretch) or later |  x86_64           |
|  Fedora 35 or later   |  x86_64           |
|  openSUSE Leap later than v15.3 (not including Tumbleweed) |  x86_64           |
|  SUSE Linux Enterprise Server 15  |  x86_64                        |

> **Note:**
>
> - For Oracle Enterprise Linux, TiDB supports the Red Hat Compatible Kernel (RHCK) and does not support the Unbreakable Enterprise Kernel provided by Oracle Enterprise Linux.
> - According to [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/), the upstream support for CentOS Linux 8 ended on December 31, 2021. CentOS Stream 8 continues to be supported by the CentOS organization.
> - Support for Ubuntu 16.04 will be removed in future versions of TiDB. Upgrading to Ubuntu 18.04 or later is strongly recommended.
> - If you are using the 32-bit version of an operating system listed in the preceding table, TiDB **is not guaranteed** to be compilable, buildable or deployable on the 32-bit operating system and the corresponding CPU architecture, or TiDB does not actively adapt to the 32-bit operating system.
> - Other operating system versions not mentioned above might work but are not officially supported.

## Software recommendations

### Control machine

| Software | Version |
| :--- | :--- |
| sshpass | 1.06 or later |
| TiUP | 1.5.0 or later |

> **Note:**
>
> It is required that you [deploy TiUP on the control machine](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine) to operate and manage TiDB clusters.

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
> - Starting from v6.3.0, to deploy TiFlash under the Linux AMD64 architecture, the CPU must support the AVX2 instruction set. Ensure that `cat /proc/cpuinfo | grep avx2` has output. To deploy TiFlash under the Linux ARM64 architecture, the CPU must support the ARMv8 instruction set architecture. Ensure that `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'` has output. By using the instruction set extensions, TiFlash's vectorization engine can deliver better performance.

### Production environment

| Component | CPU | Memory | Hard Disk Type | Network | Instance Number (Minimum Requirement) |
| :-----: | :------: | :------: | :------: | :------: | :-----: |
|  TiDB  | 16 core+ | 48 GB+ | SAS | 10 Gigabit network card (2 preferred) | 2 |
| PD | 8 core+ | 16 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
| TiKV | 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred) | 3 |
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

Before you deploy TiCDC, note that it is recommended to deploy TiCDC on PCIe-SSD disks larger than 1 TB.

## Network requirements

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

As an open-source distributed SQL database, TiDB requires the following network port configuration to run. Based on the TiDB deployment in actual environments, the administrator can open relevant ports in the network side and host side.

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
| Monitoring | 9090 | the communication port for the Prometheus service|
| Monitoring | 12020 | the communication port for the NgMonitoring service|
| Node_exporter | 9100 | the communication port to report the system information of every TiDB cluster node |
| Blackbox_exporter | 9115 | the Blackbox_exporter communication port, used to monitor the ports in the TiDB cluster |
| Grafana | 3000 | the port for the external Web monitoring service and client (Browser) access|
| Alertmanager | 9093 | the port for the alert web service |
| Alertmanager | 9094 | the alert communication port |

## Disk space requirements

| Component | Disk space requirement | Healthy disk usage |
| :-- | :-- | :-- |
| TiDB | At least 30 GB for the log disk | Lower than 90% |
| PD | At least 20 GB for the data disk and for the log disk, respectively | Lower than 90% |
| TiKV | At least 100 GB for the data disk and for the log disk, respectively | Lower than 80% |
| TiFlash | At least 100 GB for the data disk and at least 30 GB for the log disk, respectively | Lower than 80% |
| TiUP | <ul><li>Control machine: No more than 1 GB space is required for deploying a TiDB cluster of a single version. The space required increases if TiDB clusters of multiple versions are deployed. </li> <li> Deployment servers (machines where the TiDB components run): TiFlash occupies about 700 MB space and other components (such as PD, TiDB, and TiKV) occupy about 200 MB space respectively. During the cluster deployment process, the TiUP cluster requires less than 1 MB of temporary space (`/tmp` directory) to store temporary files.</li></ul>| N/A |
| Ngmonitoring | <ul><li>Conprof: 3 x 1 GB x Number of components (each component occupies about 1 GB per day, 3 days in total) + 20 GB reserved space </li><li> Top SQL: 30 x 50 MB x Number of components (each component occupies about 50 MB per day, 30 days in total) </li><li> Conprof and Top SQL share the reserved space</li></ul> | N/A |

## Web browser requirements

TiDB relies on [Grafana](https://grafana.com/) to provide visualization of database metrics. A recent version of Internet Explorer, Chrome or Firefox with Javascript enabled is sufficient.
