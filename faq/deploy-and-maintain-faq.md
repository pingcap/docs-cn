---
title: TiDB Deployment FAQs
summary: Learn about the FAQs related to TiDB deployment.
---

# TiDB Deployment FAQs

This document summarizes the FAQs related to TiDB deployment.

## Software and hardware requirements

### What operating systems does TiDB support?

For the TiDB-supported operating systems, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

### What is the recommended hardware configuration for a TiDB cluster in the development, test, or production environment?

You can deploy and run TiDB on the 64-bit generic hardware server platform in the Intel x86-64 architecture or on the hardware server platform in the ARM architecture. For the requirements and recommendations about server hardware configuration for development, test, and production environments, see [Software and Hardware Recommendations - Server recommendations](/hardware-and-software-requirements.md#server-recommendations).

### What's the purposes of 2 network cards of 10 gigabit?

As a distributed cluster, TiDB has a high demand on time, especially for PD, because PD needs to distribute unique timestamps. If the time in the PD servers is not consistent, it takes longer waiting time when switching the PD server. The bond of two network cards guarantees the stability of data transmission, and 10 gigabit guarantees the transmission speed. Gigabit network cards are prone to meet bottlenecks, therefore it is strongly recommended to use 10 gigabit network cards.

### Is it feasible if we don't use RAID for SSD?

If the resources are adequate, it is recommended to use RAID 10 for SSD. If the resources are inadequate, it is acceptable not to use RAID for SSD.

### What's the recommended configuration of TiDB components?

- TiDB has a high requirement on CPU and memory. If you need to enable TiDB Binlog, the local disk space should be increased based on the service volume estimation and the time requirement for the GC operation. But the SSD disk is not a must.
- PD stores the cluster metadata and has frequent Read and Write requests. It demands a high I/O disk. A disk of low performance will affect the performance of the whole cluster. It is recommended to use SSD disks. In addition, a larger number of Regions has a higher requirement on CPU and memory.
- TiKV has a high requirement on CPU, memory and disk. It is required to use SSD.

For details, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

## Installation and deployment

For the production environment, it is recommended to use [TiUP](/tiup/tiup-overview.md) to deploy your TiDB cluster. See [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

### Why the modified `toml` configuration for TiKV/PD does not take effect?

You need to set the `--config` parameter in TiKV/PD to make the `toml` configuration effective. TiKV/PD does not read the configuration by default. Currently, this issue only occurs when deploying using Binary. For TiKV, edit the configuration and restart the service. For PD, the configuration file is only read when PD is started for the first time, after which you can modify the configuration using pd-ctl. For details, see [PD Control User Guide](/pd-control.md).

### Should I deploy the TiDB monitoring framework (Prometheus + Grafana) on a standalone machine or on multiple machines? What is the recommended CPU and memory?

The monitoring machine is recommended to use standalone deployment. It is recommended to use an 8 core CPU with 16 GB+ memory and a 500 GB+ hard disk.

### Why the monitor cannot display all metrics?

Check the time difference between the machine time of the monitor and the time within the cluster. If it is large, you can correct the time and the monitor will display all the metrics.

### What is the function of supervise/svc/svstat service?

- supervise: the daemon process, to manage the processes
- svc: to start and stop the service
- svstat: to check the process status

### Description of inventory.ini variables

| Variable        | Description                                                |
| ---- | ------- |
| `cluster_name` | the name of a cluster, adjustable |
| `tidb_version` | the version of TiDB |
| `deployment_method` | the method of deployment, binary by default, Docker optional |
| `process_supervision` | the supervision way of processes, systemd by default, supervise optional |
| `timezone` | the timezone of the managed node, adjustable, `Asia/Shanghai` by default, used with the `set_timezone` variable |
| `set_timezone` | to edit the timezone of the managed node, True by default; False means closing |
| `enable_elk` | currently not supported |
| `enable_firewalld` | to enable the firewall, closed by default |
| `enable_ntpd` | to monitor the NTP service of the managed node, True by default; do not close it |
| `machine_benchmark` | to monitor the disk IOPS of the managed node, True by default; do not close it |
| `set_hostname` | to edit the hostname of the managed node based on the IP, False by default |
| `enable_binlog` | whether to deploy Pump and enable the binlog, False by default, dependent on the Kafka cluster; see the `zookeeper_addrs` variable |
| `zookeeper_addrs` | the ZooKeeper address of the binlog Kafka cluster |
| `enable_slow_query_log` | to record the slow query log of TiDB into a single file: ({{ deploy_dir }}/log/tidb_slow_query.log). False by default, to record it into the TiDB log |
| `deploy_without_tidb` | the Key-Value mode, deploy only PD, TiKV and the monitoring service, not TiDB; set the IP of the tidb_servers host group to null in the `inventory.ini` file |

### How to separately record the slow query log in TiDB? How to locate the slow query SQL statement?

1. The slow query definition for TiDB is in the TiDB configuration file. The `tidb_slow_log_threshold: 300` parameter is used to configure the threshold value of the slow query (unit: millisecond).

2. If a slow query occurs, you can locate the `tidb-server` instance where the slow query is and the slow query time point using Grafana and find the SQL statement information recorded in the log on the corresponding node.

3. In addition to the log, you can also view the slow query using the `ADMIN SHOW SLOW` command. For details, see [`ADMIN SHOW SLOW` command](/identify-slow-queries.md#admin-show-slow-command).

### How to add the `label` configuration if `label` of TiKV was not configured when I deployed the TiDB cluster for the first time?

The configuration of TiDB `label` is related to the cluster deployment architecture. It is important and is the basis for PD to execute global management and scheduling. If you did not configure `label` when deploying the cluster previously, you should adjust the deployment structure by manually adding the `location-labels` information using the PD management tool `pd-ctl`, for example, `config set location-labels "zone,rack,host"` (you should configure it based on the practical `label` level name).

For the usage of `pd-ctl`, see [PD Control User Guide](/pd-control.md).

### Why does the `dd` command for the disk test use the `oflag=direct` option?

The Direct mode wraps the Write request into the I/O command and sends this command to the disk to bypass the file system cache and directly test the real I/O Read/Write performance of the disk.

### How to use the `fio` command to test the disk performance of the TiKV instance?

- Random Read test:

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

- The mix test of sequential Write and random Read:

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

## What public cloud vendors are currently supported by TiDB?

TiDB supports deployment on [Google Cloud GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke), [AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks), and [Alibaba Cloud ACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud).

In addition, TiDB is currently available on JD Cloud and UCloud.
