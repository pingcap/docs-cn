---
title: Software and Hardware Requirements
summary: Learn the software and hardware requirements for DM cluster.
aliases: ['/docs/tidb-data-migration/dev/hardware-and-software-requirements/']
---

# Software and Hardware Requirements

TiDB Data Migration (DM) supports mainstream Linux operating systems. See the following table for specific version requirements:

| Linux OS Platform       | Version         |
| :----------------------- | :----------:   |
| Red Hat Enterprise Linux | 7.3 or later   |
| CentOS                   | 7.3 or later   |
| Oracle Enterprise Linux  | 7.3 or later   |
| Ubuntu LTS               | 16.04 or later |

DM can be deployed and run on Intel architecture servers and mainstream virtualization environments.

## Recommended server requirements

DM can be deployed and run on a 64-bit generic hardware server platform (Intel x86-64 architecture). For servers used in the development, testing, and production environments, this section illustrates recommended hardware configurations (these do not include the resources used by the operating system).

### Development and test environments

| Component | CPU | Memory | Local Storage | Network | Number of Instances (Minimum Requirement) |
| --- | --- | --- | --- | --- | --- |
| DM-master | 4 core+ | 8 GB+ | SAS, 200 GB+ | Gigabit network card | 1 |
| DM-worker | 8 core+ | 16 GB+ | SAS, 200 GB+ (Greater than the size of the migrated data) | Gigabit network card | The number of upstream MySQL instances |

> **Note:**
>
> - In the test environment, DM-master and DM-worker used for functional verification can be deployed on the same server.
> - To prevent interference with the accuracy of the performance test results, it is **not recommended** to use low-performance storage and network hardware configurations.
> - If you need to verify the function only, you can deploy a DM-master on a single machine. The number of DM-worker deployed must be greater than or equal to the number of upstream MySQL instances. To ensure high availability, it is recommended to deploy more DM-workers.
> - DM-worker stores full data in the `dump` and `load` phases. Therefore, the disk space for DM-worker needs to be greater than the total amount of data to be migrated. If the relay log is enabled for the migration task, DM-worker needs additional disk space to store upstream binlog data.

### Production environment

| Component | CPU | Memory | Hard Disk Type | Network | Number of Instances (Minimum Requirement) |
| --- | --- | --- | --- | --- | --- |
| DM-master | 4 core+ | 8 GB+ | SAS, 200 GB+ | Gigabit network card | 3 |
| DM-worker | 16 core+ | 32 GB+ | SSD, 200 GB+ (Greater than the size of the migrated data) | 10 Gigabit network card | Greater than the number of upstream MySQL instances |
| Monitor | 8 core+ | 16 GB+ | SAS, 200 GB+ | Gigabit network card | 1 |

> **Note:**
>
> - In the production environment, it is not recommended to deploy and run DM-master and DM-worker on the same server, because when DM-worker writes data to disks, it might interfere with the use of disks by DM-master's high availability component.
> - If a performance issue occurs, you are recommended to modify the task configuration file according to the [Optimize Configuration of DM](/dm/dm-tune-configuration.md) document. If the performance is not effectively optimized by tuning the configuration file, you can try to upgrade the hardware of your server.
