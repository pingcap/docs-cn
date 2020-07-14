---
title: TiDB Dashboard Cluster Information Page
summary: View the running status of TiDB, TiKV, PD, TiFlash components in the entire cluster and the running status of the host on which these components are located.
aliases: ['/docs/dev/dashboard/dashboard-cluster-info/']
---

# TiDB Dashboard Cluster Information Page

On the cluster information page, you can view the running status of TiDB, TiKV, PD, TiFlash components in the entire cluster and the running status of the host on which these components are located.

## Access the page

You can use one of the following two methods to access the cluster information page:

- After logging into TiDB Dashboard, click **Cluster Info** on the left navigation menu:

  ![Access cluster information page](/media/dashboard/dashboard-cluster-info-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/cluster_info/instance> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Instance list

Click **Instances** to view the list of instances:

![Instance list](/media/dashboard/dashboard-cluster-info-instances.png)

This instance list shows the overview information of all instances of TiDB, TiKV, PD, and TiFlash components in the cluster.

The list includes the following information:

- Address: The instance address.
- Status: The running status of the instance.
- Up Time: The start time of the instance.
- Version: The instance version number.
- Deployment directory: The directory in which the instance binary file is located.
- Git Hash: The Git Hash value corresponding to the instance binary file.

An instance has the following running status:

- Up: The instance is running properly.
- Down or Unreachable: The instance is not started or a network problem exists on the corresponding host.
- Tombstone: The data on the instance has been completely migrated out and the scaling-in is complete. This status exists only on TiKV or TiFlash instances.
- Leaving: The data on the instance is being migrated out and the scaling-in is in process. This status exists only on TiKV or TiFlash instances.
- Unknown: The running state of the instance is unknown.

> **Note:**
>
> Some columns in the table can be displayed only when the instance is up.

## Host list

Click **Hosts** to view the list of hosts:

![Host list](/media/dashboard/dashboard-cluster-info-hosts.png)

This host list shows the running status of hosts that correspond to all instances of TiDB, TiKV, PD, and TiFlash components in the cluster.

The list includes the following information:

- Address: The Host IP address.
- CPU: The number of logical cores of the host CPU.
- CPU Usage: The user-mode and kernel-mode CPU usage in the current 1 second.
- Memory: The total physical memory size of the host.
- Memory Usage: The current memory usage of the host.
- Disk: The file system of the disk on the host on which the instance is running and the mounting path of this disk.
- Disk Usage: The space usage of the disk on the host on which the instance is running.

> **Note:**
>
> The host list information is provided by each instance process, so when all instances on the host are down, the host information is not displayed.
