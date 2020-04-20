---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
category: how-to
---

# Deploy a TiDB Cluster Using TiUP

[TiUP](https://github.com/pingcap-incubator/tiup) is a cluster operation and maintenance tool introduced in TiDB 4.0. TiUP provides [TiUP cluster](https://github.com/pingcap-incubator/tiup-cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster; managing TiDB cluster parameters; deploying TiDB Binlog; deploying TiFlash; etc.

This document introduces how to use TiUP to deploy a TiDB cluster. The steps are as follows:

1. [Prepare the deployment environment](#1-prepare-the-deployment-environment)
2. [Configure the initialization parameter file `topology.yaml`](#2-configure-the-initialization-parameter-file-topologyyaml)
3. [Execute the deployment command](#3-execute-the-deployment-command)
4. [Verify the deployment status of the cluster](#4-verify-the-deployment-status-of-the-cluster)
5. [Start the cluster](#5-start-the-cluster)
6. [Verify the running status of the cluster](#6-verify-the-running-status-of-the-cluster)

This document also provides commands to stop and destroy a TiDB cluster using TiUP, as well as FAQs of the TiUP deployment method. See the following sections for details:

- [Stop a TiDB cluster using TiUP](#stop-a-tidb-cluster-using-tiup)
- [Destroy a TiDB cluster using TiUP](#destroy-a-tidb-cluster-using-tiup)
- [TiUP Deployment FAQs](#tiup-deployment-faqs)

## 1. Prepare the deployment environment

Here are the steps of preparing your deployment environment:

- [Step 1: Prepare the right machines for deployment](#step-1-prepare-the-right-machines-for-deployment)
- [Step 2: Install TiUP on the Control Machine](#step-2-install-tiup-on-the-control-machine)
- [Step 3: Mount the data disk ext4 filesystem with options on the target machines that deploy TiKV](#step-3-mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines-that-deploy-tikv)

### Step 1: Prepare the right machines for deployment

The software and hardware recommendations for the **Control Machine** are as follows:

- The Control Machine can be one of the target machines.
- For the Control Machine' operating system, it is recommended to install CentOS 7.3 or above.
- The Control Machine needs to access the external Internet to download TiDB and related software installation packages.
- You need to install TiUP on the Control Machine. Refer to [Step 2](#step-2-install-tiup-on-the-control-machine) for installation steps.

The software and hardware recommendations for the **target machines** are as follows:

- It is recommended that you deploy four or more target machines with at least three TiKV instances, and that the TiKV instances are not deployed on the same machine as TiDB and PD instances.
- Currently TiUP only supports deploying the TiDB cluster on x86_64 (AMD64) architecture (TiUP will support deploying TiDB on ARM architecture at 4.0 GA)
    - Under AMD64 architecture, it is recommended to use CentOS 7.3 or above as the operating system.
    - Under ARM architecture, it is recommended to use CentOS 7.6 1810 as the operating system.
- For the file system of TiKV data files, it is recommended to use EXT4 format. (refer to [Step 3](#step-3-mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines-that-deploy-tikv)) You can also use CentOS default XFS format.
- The target machines can communicate with each other on the Intranet. (It is recommended to [disable the firewall `firewalld`](#how-to-stop-the-firewall-service-of-deployment-machines), or enable the required ports between the nodes of the TiDB cluster.)
- If you need to bind CPU cores, [install the `numactl` tool](#how-to-install-the-numactl-tool).
- If you need to bind CPU cores, install the `numactl` tool.

For other software and hardware recommendations, refer to [TiDB Software and Hardware Recommendations](/how-to/deploy/hardware-recommendations.md).

### Step 2: Install TiUP on the Control Machine

Log in to the Control Machine using a regular user account (take the `tidb` user as an example). All the following TiUP installation and cluster management operations can be performed by the `tidb` user.

1. Install TiUP by executing the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    Expected output:

    ```log
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100 6029k  100 6029k    0     0  2384k      0  0:00:02  0:00:02 --:--:-- 2385k
    Detected shell: /bin/bash
    Shell profile:  /home/tidb/.bash_profile
    /home/tidb/.bash_profile has been modified to to add tiup to PATH
    open a new terminal or source /home/tidb/.bash_profile to use it
    Installed path: /home/tidb/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

2. Set the TiUP environment variables:

    Redeclare the global environment variables:

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

    Confirm whether TiUP is installed:

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

3. Install the TiUP cluster component (take `cluster-v0.4.3` as an example)

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

    Expected output:

    ```log
    The component `cluster` is not installed; downloading from repository.
    download https://tiup-mirrors.pingcap.com/cluster-v0.4.3-linux-amd64.tar.gz:
    17400435 / 17400435 [---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------] 100.00% ? p/s
    Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster
    Deploy a TiDB cluster for production

    Usage:
    cluster [flags]
    cluster [command]

    Available Commands:
    deploy      Deploy a cluster for production
    start       Start a TiDB cluster
    stop        Stop a TiDB cluster
    restart     Restart a TiDB cluster
    scale-in    Scale in a TiDB cluster
    scale-out   Scale out a TiDB cluster
    destroy     Destroy a specified cluster
    upgrade     Upgrade a specified TiDB cluster
    exec        Run shell command on host in the tidb cluster
    display     Display information of a TiDB cluster
    list        List all clusters
    audit       Show audit log of cluster operation
    import      Import an exist TiDB cluster from TiDB-Ansible
    edit-config Edit TiDB cluster config
    reload      Reload a TiDB cluster's config and restart if needed
    help        Help about any command

    Flags:
    -h, --help      help for cluster
        --version   version for cluster

    Use "cluster [command] --help" for more information about a command.
    ```

4. If it is already installed, update the TiUP cluster component to the latest version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update cluster
    ```

    Expected output will include `“Update successfully!”`:

    ```log
    The `cluster:v0.4.3` has been installed
    Update successfully!
    ```

5. Verify the current version of your TiUP cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --binary cluster
    ```

    Expected output (in the example, the current version is `v0.4.3`):

    ```log
    /home/tidb/.tiup/components/cluster/v0.4.3/cluster
    ```

### Step 3: Mount the data disk ext4 filesystem with options on the target machines that deploy TiKV

> **Note:**
>
> It is recommended to use the EXT4 file system format for the data directory of the target machines that deploy TiKV. Compared with the XFS file system format, we support more deployment cases that use the EXT4 file system format.
> 
> **For the production environment, use the EXT4 file system format.**

Log in to the target machines using the `root` user account.

Format your data disks to the ext4 filesystem and add the `nodelalloc` and `noatime` mount options to the filesystem. It is required to add the `nodelalloc` option, or else the TiUP deployment cannot pass the test. The `noatime` option is optional.

> **Note:**
>
> If your data disks have been formatted to ext4 and have added the mount options, you can uninstall it by running the `umount /dev/nvme0n1p1` command, follow the steps starting from editing the `/etc/fstab` file, and add the options again to the filesystem.

Take the `/dev/nvme0n1` data disk as an example:

1. View the data disk.

    {{< copyable "shell-root" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. Create the partition table.

    {{< copyable "shell-root" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **Note:**
    >
    > Use the `lsblk` command to view the device number of the partition: for a nvme disk, the generated device number is usually `nvme0n1p1`; for a regular disk (for example, `/dev/sdb`), the generated device number is usually `sdb1`.

3. Format the data disk to the ext4 filesystem.

    {{< copyable "shell-root" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. View the partition UUID of the data disk.

    In this example, the UUID of `nvme0n1p1` is `c51eb23b-195c-4061-92a9-3fad812cc12f`.

    {{< copyable "shell-root" >}}

    ```bash
    lsblk -f
    ```

    ```
    NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
    sda
    ├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
    ├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
    └─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
    sr0
    nvme0n1
    └─nvme0n1p1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f
    ```

5. Edit the `/etc/fstab` file and add the mount options.

    {{< copyable "shell-root" >}}

    ```shell
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. Mount the data disk.

    {{< copyable "shell-root" >}}

    ```shell
    mkdir /data1 && \
    mount -a
    ```

7. Check using the following command.

    {{< copyable "shell-root" >}}

    ```shell
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

    If the filesystem is ext4 and `nodelalloc` is included in the mount options, you have successfully mount the data disk ext4 filesystem with options on the target machines.

## 2. Configure the initialization parameter file `topology.yaml`

You need to manually write the cluster initialization configuration file. For the full configuration parameter template, refer to [Github TiUP Project](https://github.com/pingcap-incubator/tiops/blob/master/topology.example.yaml).

You need to create a YAML configuration file on the Control Machine, such as `topology.yaml`.

The following sections provide a cluster configuration template for each of the following common scenarios:

- [Scenario 1: Single machine with single instance](#scenario-1-single-machine-with-single-instance)
- [Scenario 2: Single machine with multiple instances](#scenario-2-single-machine-with-multiple-instances)
- [Scenario 3: Use TiDB Binlog deployment template](#scenario-3-use-tidb-binlog-deployment-template)

### Scenario 1: Single machine with single instance

#### Deployment requirements

- Use the `tidb` user for cluster management
- Use the default `22` port
- Use `/tidb-deploy` as the deployment directory is
- Use `/tidb-data` as the data directory

#### Topology

| Instance | Count | Physical Machine Configuration | IP | Other Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiKV | 3 | 16 Vcore 32GB * 1 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | Default port configuration; <br> Global directory configuration |
| TiDB |3 | 16 Vcore 32GB * 1 | 10.0.1.7 <br> 10.0.1.8 <br> 10.0.1.9 | Default port configuration; <br>  Global directory configuration |
| PD | 3 |4 Vcore 8GB * 1 |10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | Default port configuration; <br> Global directory configuration |
| TiFlash | 1 | 32 VCore 64 GB * 1 | 10.0.1.10 | Default port configuration; <br> Global directory configuration |

#### Step 4: Edit the configuration file template topology.yaml

> **Note:**
>
> You do not need to manually create the `tidb` user, because the TiUP cluster component will automatically create the `tidb` user on the target machines. You can customize the user or keep it the same as the user of the Control Machine.

> **Note:**
>
> - If you need to [deploy TiFlash](/reference/tiflash/deploy.md), set `replication.enable-placement-rules` to `true` in the `topology.yaml` configuration file to enable PD’s [Placement Rules](/how-to/configure/placement-rules.md) feature.
>
> - Currently, the instance-level configuration `"-host"` under `tiflash_servers` only supports IP, not domain name.
> 
> - For the detailed parameter configuration of TiFlash, refer to [TiFlash Parameter Configuration](#tiflash-parameter).

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and as the default value of
# # them if the specific deployment value missing.

global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

# # Monitored variables are used to all the machine
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  # deploy_dir: "/tidb-deploy/monitored-9100"
  # data_dir: "/tidb-data/monitored-9100"
  # log_dir: "/tidb-deploy/monitored-9100/log"
# # Server configs are used to specify the runtime configuration of TiDB components
# # All configuration items can be found in TiDB docs:
# # - TiDB: https://pingcap.com/docs/stable/reference/configuration/tidb-server/configuration-file/
# # - TiKV: https://pingcap.com/docs/stable/reference/configuration/tikv-server/configuration-file/
# # - PD: https://pingcap.com/docs/stable/reference/configuration/pd-server/configuration-file/
# # All configuration items use points to represent the hierarchy, e.g:
# #   readpool.storage.use-unified-pool
# #           ^       ^
# # You can overwrite this configuration via instance-level `config` field

server_configs:
  tidb:
    log.slow-threshold: 300
    binlog.enable: false
    binlog.ignore-error: false
  tikv:
    # server.grpc-concurrency: 4
    # raftstore.apply-pool-size: 2
    # raftstore.store-pool-size: 2
    # rocksdb.max-sub-compactions: 1
    # storage.block-cache.capacity: "16GB"
    # readpool.unified.max-thread-count: 12
    readpool.storage.use-unified-pool: true
    readpool.coprocessor.use-unified-pool: true
  pd:
    schedule.leader-schedule-limit: 4
    schedule.region-schedule-limit: 2048
    schedule.replica-schedule-limit: 64
    replication.enable-placement-rules: true
  tiflash:
    logger.level: "info"
  # pump:
  #   gc: 7

pd_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # name: "pd-1"
    # client_port: 2379
    # peer_port: 2380
    # deploy_dir: "/tidb-deploy/pd-2379"
    # data_dir: "/tidb-data/pd-2379"
    # log_dir: "/tidb-deploy/pd-2379/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.pd` values
    # config:
    #   schedule.max-merge-region-size: 20
    #   schedule.max-merge-region-keys: 200000
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.7
    # ssh_port: 22
    # port: 4000
    # status_port: 10080
    # deploy_dir: "/tidb-deploy/tidb-4000"
    # log_dir: "/tidb-deploy/tidb-4000/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.tidb` values
    # config:
    #   log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.8
  - host: 10.0.1.9

tikv_servers:
  - host: 10.0.1.1
    # ssh_port: 22
    # port: 20160
    # status_port: 20180
    # deploy_dir: "/tidb-deploy/tikv-20160"
    # data_dir: "/tidb-data/tikv-20160"
    # log_dir: "/tidb-deploy/tikv-20160/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.tikv` values
    # config:
    #   server.grpc-concurrency: 4
    #   server.labels: { zone: "zone1", dc: "dc1", host: "host1" }
  - host: 10.0.1.2
  - host: 10.0.1.3

tiflash_servers:
  - host: 10.0.1.10
  # ssh_port: 22
  # tcp_port: 9000
  # http_port: 8123
  # flash_service_port: 3930
  # flash_proxy_port: 20170
  # flash_proxy_status_port: 20292
  # metrics_port: 8234
  # deploy_dir: /tidb-deploy/tiflash-9000
  # data_dir: /tidb-data/tiflash-9000
  # log_dir: /tidb-deploy/tiflash-9000/log
  # numa_node: "0,1"
  # # Config is used to overwrite the `server_configs.tiflash` values
  # config:
  #   logger.level: "info"
  # learner_config:
  #   log-level: "info"
  #  - host: 10.0.1.15
  #  - host: 10.0.1.16

# pump_servers:
#   - host: 10.0.1.17
#     ssh_port: 22
#     port: 8250
#     deploy_dir: "/tidb-deploy/pump-8249"
#     data_dir: "/tidb-data/pump-8249"
#     log_dir: "/tidb-deploy/pump-8249/log"
#     numa_node: "0,1"
#     # Config is used to overwrite the `server_configs.drainer` values
#     config:
#       gc: 7
#   - host: 10.0.1.18
#   - host: 10.0.1.19
# drainer_servers:
#   - host: 10.0.1.17
#     port: 8249
#     data_dir: "/tidb-data/drainer-8249"
#     # if drainer doesn't have checkpoint, use initial commitTS to initial checkpoint
#     # will get a latest timestamp from pd if setting to be -1 (default -1)
#     commit_ts: -1
#     deploy_dir: "/tidb-deploy/drainer-8249"
#     log_dir: "/tidb-deploy/drainer-8249/log"
#     numa_node: "0,1"
#     # Config is used to overwrite the `server_configs.drainer` values
#     config:
#       syncer.db-type: "mysql"
#       syncer.to.host: "127.0.0.1"
#       syncer.to.user: "root"
#       syncer.to.password: ""
#       syncer.to.port: 3306
#   - host: 10.0.1.19

monitoring_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # port: 9090
    # deploy_dir: "/tidb-deploy/prometheus-8249"
    # data_dir: "/tidb-data/prometheus-8249"
    # log_dir: "/tidb-deploy/prometheus-8249/log"

grafana_servers:
  - host: 10.0.1.4
    # port: 3000
    # deploy_dir: /tidb-deploy/grafana-3000

alertmanager_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # web_port: 9093
    # cluster_port: 9094
    # deploy_dir: "/tidb-deploy/alertmanager-9093"
    # data_dir: "/tidb-data/alertmanager-9093"
    # log_dir: "/tidb-deploy/alertmanager-9093/log"

```

### Scenario 2: Single machine with multiple instances

#### Deployment requirements

The physical machines on which TiDB and TiKV components are deployed have a 2-way processor with 16 Vcores per way, and the memory also meets the standard.

In order to improve the resource utilization, you can deploy multiple instances on a single machine, that is, you can bind the cores through numa to isolate CPU resources used by TiDB and TiKV instances.

You can also deploy PD and Prometheus in a mixed manner, but the data directories of the two require two independent file systems.

#### Key parameter configuration

This section introduces the key parameters of the single-machine multi-instance deployment method, which is mainly used in the single-machine multi-instance deployment scenario of TiDB and TiKV.

You need to fill in the result in the configuration file (as described in the Step 4) according to the calculation formula provided.

- Configuration optimization for TiKV

    - Make `readpool` thread pool self-adaptive. Configure the `readpool.unified.max-thread-count` parameter to make `readpool.storage` and `readpool.coprocessor` share a unified thread pool, and also enable self-adaptive switches for them.

        - Enable `readpool.storage` and `readpool.coprocessor`:

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        - The calculation formula is as follows:

        ```
        readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances
        ```

    - Make storage CF (all RocksDB column families) memory self-adaptive. Configure the `storage.block-cache.capacity` parameter to automatically balance memory usage among CFs.

        - The default setting of the `storage.block-cache` parameter is CF self-adaptive. You do not need to modify this configuration:

            ```yaml
            storage.block-cache.shared: true
            ```

        - The calculation formula is as follows:

            ```
            storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)
            ```

    - If multiple TiKV instances are deployed on the same physical disk, you need to add the `capacity` parameter in the TiKV configuration:

        ```
        raftstore.capacity = the total disk capacity / the number of TiKV instances
        ```

- Label scheduling configuration

    Because multiple TiKV instances are deployed on a single machine, in order to avoid losing 2 replicas of the default 3 replicas in the Region Group during machine downtime which causes cluster unavailability, you can use labels to implement intelligent scheduling of PD.

    - TiKV configuration

        Configure the same host-level label information on the same physical machines:

        ```yml
        config:
          server.labels:
            host: tikv1
        ```

    - PD configuration

        Configure labels type for PD to identify and schedule Regions:

        ```yml
        pd:
          replication.location-labels: ["host"]
        ```

- Bind cores by configuring `numa_node`

    - Configure the `numa_node` parameter in the corresponding instance parameter module and add the number of CPU cores;

    - Before you use numa to bind the cores, make sure you have installed the numactl tool. After you confirm the CPU information of the corresponding physical machines, then you can configure the parameters.

    - The `numa_node` parameter corresponds to the `numactl --membind` configuration.

#### Topology

| Instance | Count | Physical Machine Configuration | IP | Other Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiKV | 6 | 32 Vcore 64GB * 3 | 10.0.1.1<br> 10.0.1.2<br> 10.0.1.3 | 1. Distinguish between instance-level port and status_port; <br> 2. Configure `readpool` and `storage` global parameters and the `raftstore` parameter; <br> 3. Configure instance-level host-dimension labels; <br> 4. Configure numa to bind cores|
| TiDB | 6 | 32 Vcore 64GB * 3 | 10.0.1.7<br> 10.0.1.8<br> 10.0.1.9 | Configure numa to bind cores |
| PD | 3 | 16 Vcore 32 GB | 10.0.1.4<br> 10.0.1.5<br> 10.0.1.6 | Configure `location_lables` parameter |
| TiFlash | 1 | 32 VCore 64 GB | 10.0.1.10 | Default port; <br> Customized deployment directory - the `data_dir` parameter is set to `/data1/tiflash/data` |

#### Step 4: Edit the configuration file template topology.yaml

> **Note:**
>
> - You do not need to manually create the `tidb` user, because the TiUP cluster component will automatically create the `tidb` user on the target machines. You can customize the user or keep it the same as the user of the Control Machine.
> - By default, `deploy_dir` of each component uses `<deploy_dir>/<components_name>-<port>` of the global configuration. For example, if you specify the `tidb` port as `4001`, then the TiDB component's default `deploy_dir` is `tidb-deploy/tidb-4001`. Therefore, when you specify non-default ports in multi-instance scenarios, you do not need to specify `deploy_dir` again.

> **Note:**
>
> - If you need to [deploy TiFlash](/reference/tiflash/deploy.md), set `replication.enable-placement-rules` to `true` in the `topology.yaml` configuration file to enable PD’s [Placement Rules](/how-to/configure/placement-rules.md) feature.
>
> - Currently, the instance-level configuration `"-host"` under `tiflash_servers` only supports IP, not domain name.
> 
> - For the detailed parameter configuration of TiFlash, refer to [TiFlash Parameter Configuration](#tiflash-parameter).

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and as the default value of
# # them if the specific deployment value missing.

global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  deploy_dir: "/tidb-deploy/monitored-9100"
  data_dir: "/tidb-data-monitored-9100"
  log_dir: "/tidb-deploy/monitored-9100/log"

server_configs:
  tikv:
    readpool.unified.max-thread-count: <fill in the calculated result from the calculation formula provided before>
    readpool.storage.use-unified-pool: true
    readpool.coprocessor.use-unified-pool: true
    storage.block-cache.capacity: "<fill in the calculated result from the calculation formula provided before>"
    raftstore.capacity: "<fill in the calculated result from the calculation formula provided before>"
  pd:
    replication.location-labels: ["host"]
    replication.enable-placement-rules: true

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.7
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.7
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"
  - host: 10.0.1.8
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.8
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"
  - host: 10.0.1.9
    port: 4000
    status_port: 10080
    deploy_dir: "/tidb-deploy/tidb-4000"
    log_dir: "/tidb-deploy/tidb-4000/log"
    numa_node: "0"
  - host: 10.0.1.9
    port: 4001
    status_port: 10081
    deploy_dir: "/tidb-deploy/tidb-4001"
    log_dir: "/tidb-deploy/tidb-4001/log"
    numa_node: "1"

tikv_servers:
  - host: 10.0.1.1
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.1
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv1" }
  - host: 10.0.1.2
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.2
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv2" }
  - host: 10.0.1.3
    port: 20160
    status_port: 20180
    deploy_dir: "/tidb-deploy/tikv-20160"
    data_dir: "/tidb-data/tikv-20160"
    log_dir: "/tidb-deploy/tikv-20160/log"
    numa_node: "0"
    config:
      server.labels: { host: "tikv3" }
  - host: 10.0.1.3
    port: 20161
    status_port: 20181
    deploy_dir: "/tidb-deploy/tikv-20161"
    data_dir: "/tidb-data/tikv-20161"
    log_dir: "/tidb-deploy/tikv-20161/log"
    numa_node: "1"
    config:
      server.labels: { host: "tikv3" }
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data
monitoring_servers:
  - host: 10.0.1.7
grafana_servers:
  - host: 10.0.1.7
alertmanager_servers:
  - host: 10.0.1.7
```

### Scenario 3: Use TiDB Binlog deployment template

#### Deployment requirements

- Use `/tidb-deploy` as the default deployment directory 
- Use `/tidb-data` as the data directory
- Use TiDB Binlog to replicate data to the downstream machine `10.0.1.9:4000`

#### Key parameter configuration

Key parameters of TiDB:

- `binlog.enable: true` 

    This enables the binlog service. The default value of this parameter is `false`.

- `binlog.ignore-error: true` 

    It is recommended to enable this parameter in scenarios that require high availability. If it is set to `true`, TiDB stops writing to the binlog when an error occurs, and add 1 to the count on the monitoring item `tidb_server_critical_error_total`; if it is set to `false`, once writing to binlog fails, the entire TiDB service is stopped.

#### Topology

| Instance | Physical Machine Configuration | IP | Other Configuration |
| :-- | :-- | :-- | :-- |
| TiKV | 16 Vcore 32 GB * 3 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | Default port configuration |
|TiDB | 16 Vcore 32 GB * 3 | 10.0.1.7 <br> 10.0.1.8 <br> 10.0.1.9 | Default port configuration;<br>`enable_binlog` enabled; <br> `ignore-error` enabled |
| PD | 4 Vcore 8 GB * 3| 10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | Default port configuration |
| TiFlash | 1 | 32 VCore 64 GB  | 10.0.1.10 | Default port configuration; <br> Customized deployment directory - the `data_dir` parameter is set to `/data1/tiflash/data,/data2/tiflash/data` for multi-disk deployment |
| Pump|8 Vcore 16GB * 3|10.0.1.6<br>10.0.1.7<br>10.0.1.8 | Default port configuration; <br> The GC time is set to 7 days |
| Drainer | 8 Vcore 16GB | 10.0.1.9 | Default port configuration; <br>Set default initialization commitTS |

#### Step 4: Edit the configuration file template topology.yaml

> **Note:**
>
> You do not need to manually create the `tidb` user, because the TiUP cluster component will automatically create the `tidb` user on the target machines. You can customize the user or keep it the same as the user of the Control Machine.

> **Note:**
>
> - If you need to [deploy TiFlash](/reference/tiflash/deploy.md), set `replication.enable-placement-rules` to `true` in the `topology.yaml` configuration file to enable PD’s [Placement Rules](/how-to/configure/placement-rules.md) feature.
>
> - Currently, the instance-level configuration `"-host"` under `tiflash_servers` only supports IP, not domain name.
> 
> - For the detailed parameter configuration of TiFlash, refer to [TiFlash Parameter Configuration](#tiflash-parameter).

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and as the default value of
# # them if the specific deployment value missing.

global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
monitored:
  node_exporter_port: 9122
  blackbox_exporter_port: 9137
  deploy_dir: "/tidb-deploy/monitored-9100"
  data_dir: "/tidb-data/monitored-9100"
  log_dir: "/tidb-deploy/monitored-9100/log"

server_configs:
  tidb:
    binlog.enable: true
    binlog.ignore-error: true
  pd:
    replication.enable-placement-rules: true

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6
tidb_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9
tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3

pump_servers:
  - host: 10.0.1.6
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8249"
    data_dir: "/tidb-data/pump-8249"
    # Config is used to overwrite the `server_configs.drainer` values
    config:
      gc: 7
  - host: 10.0.1.7
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8249"
    data_dir: "/tidb-data/pump-8249"
    # Config is used to overwrite the `server_configs.drainer` values
    config:
      gc: 7
  - host: 10.0.1.8
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8249"
    data_dir: "/tidb-data/pump-8249"
    # Config is used to overwrite the `server_configs.drainer` values
    config:
      gc: 7
drainer_servers:
  - host: 10.0.1.9
    port: 8249
    data_dir: "/tidb-data/drainer-8249"
    # if drainer doesn't have checkpoint, use initial commitTS to initial checkpoint
    # will get a latest timestamp from pd if setting to be -1 (default -1)
    commit_ts: -1
    deploy_dir: "/tidb-deploy/drainer-8249"
    # Config is used to overwrite the `server_configs.drainer` values
    config:
      syncer.db-type: "tidb"
      syncer.to.host: "10.0.1.9"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 4000
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data,/data2/tiflash/data 
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

## 3. Execute the deployment command

### Deployment command introduction

Use `--help` to query specific parameter descriptions:

{{< copyable "shell-regular" >}}

```shell
tiup cluster  deploy --help
```

Expected output:

```log
Deploy a cluster for production. SSH connection will be used to deploy files, as well as creating system users for running the service.

Usage:
  cluster deploy <cluster-name> <version> <topology.yaml> [flags]

Flags:
  -h, --help                   help for deploy
  -i, --identity_file string   The path of the SSH identity file. If specified, public key authentication will be used.
      --user string            The user name to login via SSH. The user must have root (or sudo) privilege. (default "root")
  -y, --yes                    Skip confirming the topology
```

> **Note:**
>
> You can use secret keys or interactive passwords for security authentication when you deploy TiDB using TiUP:
>
> - If you use secret keys, you can specify the path of the keys through `-i` or `--identity_file`;
> - If you use passwords, you do not need to add other parameters, tap `Enter` and you can enter the password interaction window.

### Step 5: Execute the deployment command

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v4.0.0-rc ./topology.yaml --user root -i /home/root/.ssh/gcp_rsa
```

In the above command:

- The name of the TiDB cluster deployed through TiUP cluster is `tidb-test`.
- The deployment version is `v4.0.0-rc`. For other supported versions, see [How to view the TiDB versions supported by TiUP](#how-to-view-the-tidb-versions-supported-by-tiup).
- The initialization configuration file is `topology.yaml`.
- Log in to the target machine through the `root` key to complete the cluster deployment, or you can use other users with `ssh` and `sudo` privileges to complete the deployment.

At the end of the output log, you will see ```Deployed cluster `tidb-test` successfully```. This indicates that the deployment is successful.

## 4. Verify the deployment status of the cluster

### Verification command introduction

{{< copyable "shell-regular" >}}

```shell
tiup cluster list --help
```

```log
List all clusters

Usage:
  cluster list [flags]

Flags:
  -h, --help   help for list

# Usage shows the execution command, which shows the list of all the managed TiDB clusters.
```

### Step 6: Check the cluster managed by TiUP

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

Expected output will include the name, deployment user, version, and secret key information of the TiDB cluster managed by TiUP cluster:

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v4.0.0-rc  /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

### Step 7: Check the status of `tidb-test`

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

Expected output will include the instance ID, role, host, listening port, and status (because the cluster is not started yet, so the status is `Down`/`inactive`), and directory information:

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster display tidb-test
TiDB Cluster: tidb-test
TiDB Version: v4.0.0-rc
ID                  Role          Host          Ports                            Status    Data Dir                        Deploy Dir
--                  ----          ----          -----                            ------    --------                        ----------
10.0.1.4:9104       alertmanager  10.0.1.4      9104/9105                        inactive  /tidb-data/alertmanager-9104    /tidb-deploy/alertmanager-9104
10.0.1.4:3000       grafana       10.0.1.4      3000                             inactive  -                               /tidb-deploy/grafana-3000
10.0.1.4:2379       pd            10.0.1.4      2379/2380                        Down      /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.5:2379       pd            10.0.1.5      2379/2380                        Down      /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.6:2379       pd            10.0.1.6      2379/2380                        Down      /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.4:9090       prometheus    10.0.1.4      9090                             inactive  /tidb-data/prometheus-9090      /tidb-deploy/prometheus-9090
10.0.1.7:4000       tidb          10.0.1.7      4000/10080                       Down      -                               /tidb-deploy/tidb-4000
10.0.1.8:4000       tidb          10.0.1.8      4000/10080                       Down      -                               /tidb-deploy/tidb-4000
10.0.1.9:4000       tidb          10.0.1.9      4000/10080                       Down      -                               /tidb-deploy/tidb-4000
10.0.1.10:9000      tiflash       10.0.1.4      9000/8123/3930/20170/20292/8234  Down      /tidb-data-lzs/tiflash-10000    /tidb-deploy-lzs/tiflash-10000
10.0.1.1:20160      tikv          10.0.1.1      20160/20180                      Down      /tidb-data/tikv-20160           /tidb-deploy/tikv-2060
10.0.1.2:20160      tikv          10.0.1.2      20160/20180                      Down      /tidb-data/tikv-20160           /tidb-deploy/tikv-2060
10.0.1.3:20160      tikv          10.0.1.4      20160/20180                      Down      /tidb-data/tikv-20160           /tidb-deploy/tikv-2060
```

## 5. Start the cluster

### Step 8: Start the `tidb-test` cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

If the output log includes ```Started cluster `tidb-test` successfully```, it means that the startup is successful.

## 6. Verify the running status of the cluster

### Step 9: Check the `tidb-test` cluster status using TiUP

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

Expected output (if the `Status` is `Up`, the cluster status is normal):

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster display tidb-test
TiDB Cluster: tidb-test
TiDB Version: v4.0.0-rc
ID              Role          Host      Ports                            Status     Data Dir                        Deploy Dir
--              ----          ----      -----                            ------     --------                        ----------
10.0.1.4:9104   alertmanager  10.0.1.4  9104/9105                        Up         /tidb-data/alertmanager-9104    /tidb-deploy/alertmanager-9104
10.0.1.4:3000   grafana       10.0.1.4  3000                             Up         -                               /tidb-deploy/grafana-3000
10.0.1.4:2379   pd            10.0.1.4  2379/2380                        Healthy|L  /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.5:2379   pd            10.0.1.5  2379/2380                        Healthy    /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.6:2379   pd            10.0.1.6  2379/2380                        Healthy    /tidb-data/pd-2379              /tidb-deploy/pd-2379
10.0.1.4:9090   prometheus    10.0.1.4  9090                             Up         /tidb-data/prometheus-9090      /tidb-deploy/prometheus-9090
10.0.1.7:4000   tidb          10.0.1.7  4000/10080                       Up         -                               /tidb-deploy/tidb-4000
10.0.1.8:4000   tidb          10.0.1.8  4000/10080                       Up         -                               /tidb-deploy/tidb-4000
10.0.1.9:4000   tidb          10.0.1.9  4000/10080                       Up         -                               /tidb-deploy/tidb-4000
10.0.1.10:9000  tiflash       10.0.1.4  9000/8123/3930/20170/20292/8234  Up         /tidb-data-lzs/tiflash-9000     /tidb-deploy-lzs/tiflash-9000
10.0.1.1:2060   tikv          10.0.1.1  2060/20080                       Up         /tidb-data/tikv-2060            /tidb-deploy/tikv-2060
10.0.1.2:2060   tikv          10.0.1.2  2060/20080                       Up         /tidb-data/tikv-2060            /tidb-deploy/tikv-2060
10.0.1.3:2060   tikv          10.0.1.4  2060/20080                       Up         /tidb-data/tikv-2060            /tidb-deploy/tikv-2060
```

### Step 10: Check TiDB cluster status through TiDB Dashboard and Grafana

#### Check TiDB cluster status through TiDB Dashboard

Log in to TiDB Dashboard via `{pd-leader-ip}:2379/dashboard` with the `root` user and password (empty by default) of the TiDB database. If you have modified the password of the `root` user, then enter the modified password.

![TiDB-Dashboard](/media/tiup/tidb-dashboard.png)

The main page displays the node information of the TiDB cluster:

![TiDB-Dashboard-status](/media/tiup/tidb-dashboard-status.png)

#### Check TiDB cluster status through Grafana Overview page

Log in to Grafana monitoring via `{Grafana-ip}:3000` (the default username and password is `admin` and `admin`).

![Grafana-login](/media/tiup/grafana-login.png)

Click Overview monitoring page to check TiDB port and load information:

![Grafana-overview](/media/tiup/grafana-overview.png)

### Step 11: Log in to the database to execute simple SQL statements

> **Note:**
>
> Before logging into the database, you need to install the MySQL client.

Log in to the database by executing the following command:

{{< copyable "shell-regular" >}}

```shell
mysql -u root -h 10.0.1.4 -P 4000
```

Execute simple SQL statements:

```sql
--
-- Successfully logged in
--
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.7.25-TiDB-v4.0.0-beta-446-g5268094af TiDB Server (Apache License 2.0), MySQL 5.7 compatible

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

--
-- Check TiDB version
--
MySQL [(none)]> select tidb_version()\G
*************************** 1. row ***************************
tidb_version(): Release Version: v4.0.0-beta-446-g5268094af
Git Commit Hash: 5268094afe05c7efef0d91d2deeec428cc85abe6
Git Branch: master
UTC Build Time: 2020-03-17 02:22:07
GoVersion: go1.13
Race Enabled: false
TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
Check Table Before Drop: false
1 row in set (0.00 sec)
MySQL [tidb]> create database pingcap;
Query OK, 0 rows affected (0.10 sec)

--
-- Create PingCAP database
--
MySQL [(none)]> create database pingcap;
Query OK, 0 rows affected (0.10 sec)

MySQL [(none)]> use pingcap;
Database changed
--
-- Create tab_tidb table
--
MySQL [pingcap]> CREATE TABLE `tab_tidb` (
    ->         `id` int(11) NOT NULL AUTO_INCREMENT,
    ->          `name` varchar(20) NOT NULL DEFAULT '',
    ->          `age` int(11) NOT NULL DEFAULT 0,
    ->          `version` varchar(20) NOT NULL DEFAULT '',
    ->           PRIMARY KEY (`id`),
    ->           KEY `idx_age` (`age`));
Query OK, 0 rows affected (0.11 sec)
--
-- Insert data
--
MySQL [pingcap]> insert into `tab_tidb` values (1,'TiDB',5,'TiDB-v4.0.0');
Query OK, 1 row affected (0.03 sec)
--
-- Check tab_tidb table
--
MySQL [pingcap]> select * from tab_tidb;
+----+------+-----+-------------+
| id | name | age | version     |
+----+------+-----+-------------+
|  1 | TiDB |   5 | TiDB-v4.0.0 |
+----+------+-----+-------------+
1 row in set (0.00 sec)
--
-- Check TiKV store status, store_id, storage status, and the starting time
--
MySQL [pingcap]> select STORE_ID,ADDRESS,STORE_STATE,STORE_STATE_NAME,CAPACITY,AVAILABLE,UPTIME from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+--------------------+-------------+------------------+----------+-----------+--------------------+
| STORE_ID | ADDRESS            | STORE_STATE | STORE_STATE_NAME | CAPACITY | AVAILABLE | UPTIME             |
+----------+--------------------+-------------+------------------+----------+-----------+--------------------+
|        1 | 10.0.1.1:20160 |           0 | Up               | 49.98GiB | 46.3GiB   | 5h21m52.474864026s |
|        4 | 10.0.1.2:20160 |           0 | Up               | 49.98GiB | 46.32GiB  | 5h21m52.522669177s |
|        5 | 10.0.1.3:20160 |           0 | Up               | 49.98GiB | 45.44GiB  | 5h21m52.713660541s |
+----------+--------------------+-------------+------------------+----------+-----------+--------------------+
3 rows in set (0.00 sec)

MySQL [pingcap]> exit
Bye
```

## Stop a TiDB cluster using TiUP

To stop the `tidb-test` cluster, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster stop tidb-test
```

If the output log includes ```Stopped cluster `tidb-test` successfully```, then the cluster is successfully stopped.

## Destroy a TiDB cluster using TiUP

> **Warning:**
>
> Perform this operation carefully in a production environment. The cleanup task cannot be rolled back after this operation is confirmed.

To destroy the `tidb-test` cluster, including data and services, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster destroy tidb-test
```

If the output log includes ```Destroy cluster `tidb-test` successfully```, then the cluster is successfully destroyed.

## TiUP Deployment FAQs

This section describes common problems and solutions when you deploy TiDB clusters using TiUP.

### Default port

| Component | Port variable | Default port | Description |
| :-- | :-- | :-- | :-- |
| TiDB | port | 4000  | the communication port for the application and DBA tools |
| TiDB | status_port | 10080  | the communication port to report TiDB status |
| TiKV | port | 20160 | the TiKV communication port |
| TiKV | status_port   | 20180   | the communication port to report the TiKV status |
| PD | client_port | 2379 | the communication port between TiDB and PD |
| PD | peer_port | 2380 | the inter-node communication port within the PD cluster |
| Pump | port | 8250  | the Pump communication port |
| Drainer | port | 8249 | the Drainer communication port |
| Prometheus | port | 9090 | the communication port for the Prometheus service |
| Node_exporter | node_exporter_port | 9100 | the communication port to report the system information of every TiDB cluster node |
| Blackbox_exporter | blackbox_exporter_port | 9115 | the Blackbox_exporter communication port，used to monitor ports in a TiDB cluster |
| Grafana | grafana_port |  3000 | the port for the external web monitoring service and client (Browser) access |
| Alertmanager | web_port | 9093 | the port for the web monitoring service |
| Alertmanager | cluster_port | 9094 | the monitoring communication port |

### Default directory

| Module | Directory variable | Default directory | Description |
| :-- | :-- | :-- | :-- |
| Global | `deploy_dir` | `/home/tidb/deploy` | deployment directory |
| Global | `data_dir` | `/home/tidb/data` | data directory |
| Global | `log_dir` | `/home/tidb/deploy/log` | log directory |
| Monitored | `deploy_dir` | `/home/tidb/data` | deployment directory |
| Monitored | `data_dir` | `/home/tidb/deploy` | data directory |
| Monitored | `log_dir` | `/home/tidb/deploy` | log directory |
| Instance | `deploy_dir` | inherit global configuration | deployment directory |
| Instance | `data_dir` | inherit global configuration | data directory |
| Instance | `log_dir` | inherit global configuration | log directory |

### TiFlash parameter

| Parameter | Default configuration | Description |
| :-- | :-- | :-- |
| ssh_port | 22 | SSH default port |
| tcp_port | 9000 | TiFlash TCP service port |
| http_port | 8123 | TiFlash HTTP service port |
| flash_service_port | 3930 | TiFlash RAFT service port and Coprocessor service port |
| flash_proxy_port | 20170 | TiFlash Proxy service port |
| flash_proxy_status_port | 20292 | Prometheus pulling TiFlash Proxy metrics port |
| metrics_port | 8234 | Prometheus pulling TiFlash metrics port |
| deploy_dir | /home/tidb/deploy/tiflash-9000 | TiFlash deployment directory |
| data_dir | /home/tidb/deploy/tiflash-9000/data | TiFlash data storage directory |
| log_dir | /home/tidb/deploy/tiflash-9000/log | TiFlash log storage directory |

### Parameter module configuration

This section describes the parameter module configuration in descending order.

#### 1. Instance parameter module

Taking the TiDB server as an example, the configuration of the instance parameter module (instances split by `- host`) is applied to the target node with the highest priority.

- The `config` configuration in the instance takes precedence over the `server_configs` parameter module configuration.
- The `ssh_port`, `deploy_dir`, `log_dir` configurations in the instance take precedence over the `global` parameter module configuration.

```yaml
tidb_servers:
  - host: 10.0.1.11
    ssh_port: 22
    port: 4000
    status_port: 10080
    deploy_dir: "deploy/tidb-4000"
    log_dir: "deploy/tidb-4000/log"
    numa_node: "0,1"
    # Config is used to overwrite the `server_configs.tidb` values
    config:
      log.slow-query-file: tidb-slow-overwritten.log
```

#### 2. `global`, `server_configs`, `monitored` parameter modules

- The configuration in the `global` parameter module is global configuration and its priority is lower than that of the instance parameter module.

    ```yaml
    global:
    user: "tidb"
    ssh_port: 22
    deploy_dir: "deploy"
    data_dir: "data"
    ```

- The configuration of the `server_configs` parameter module applies to global monitoring and its priority is lower than that of the instance parameter module.

    ```yaml
    server_configs:
    tidb:
      log.slow-threshold: 300
      binlog.enable: false
      binlog.ignore-error: false
    tikv:
      # server.grpc-concurrency: 4
      # raftstore.apply-pool-size: 2
      # raftstore.store-pool-size: 2
      # rocksdb.max-sub-compactions: 1
      # storage.block-cache.capacity: "16GB"
      # readpool.unified.max-thread-count: 12
      readpool.storage.use-unified-pool: true
      readpool.coprocessor.use-unified-pool: true
    pd:
      schedule.leader-schedule-limit: 4
      schedule.region-schedule-limit: 2048
      schedule.replica-schedule-limit: 64
      replication.enable-placement-rules: true
    pump:
        gc: 7
    ```

- The configuration of the `monitored` parameter module applies to the monitored host. The default ports are `9100` and `9115`. If the directory is configured, it will be deployed to the user's `/home` directory by default. For example, if the `user` in the `global` parameter module is `"tidb"`, then it will be deployed to the `/home/tidb` directory.

    ```yaml
    # Monitored variables are used to
    monitored:
    node_exporter_port: 9100
    blackbox_exporter_port: 9115
    deploy_dir: "deploy/monitored-9100"
    data_dir: "data/monitored-9100"
    log_dir: "deploy/monitored-9100/log"
    ```

### How to view the TiDB versions supported by TiUP

Execute the following command to view the TiDB versions that TiUP supports:

```shell
tiup list tidb --refresh
```

In the following output:

- `Version` is the supported TiDB version
- `Installed` is the currently installed version
- `Release` is the release time
- `Platforms` is the supported platform

```log
Available versions for tidb (Last Modified: 2020-02-26T15:20:35+08:00):
Version        Installed  Release:                             Platforms
-------        ---------  --------                             ---------
master                    2020-03-18T08:39:11.753360611+08:00  linux/amd64,darwin/amd64
v3.0.1                    2020-04-07T17:53:00+08:00            linux/amd64,darwin/amd64
v3.0.2                    2020-04-08T23:38:37+08:00            linux/amd64,darwin/amd64
v3.0.3                    2020-03-27T22:41:16.279411145+08:00  linux/amd64,darwin/amd64
v3.0.4                    2020-03-27T22:43:35.362550386+08:00  linux/amd64,darwin/amd64
v3.0.5                    2020-03-27T22:46:01.016467032+08:00  linux/amd64,darwin/amd64
v3.0.6                    2020-03-13T11:55:17.941641963+08:00  linux/amd64,darwin/amd64
v3.0.7                    2020-03-13T12:02:22.538128662+08:00  linux/amd64,darwin/amd64
v3.0.8                    2020-03-17T14:03:29.575448277+08:00  linux/amd64,darwin/amd64
v3.0.9                    2020-03-13T13:02:15.947260351+08:00  linux/amd64,darwin/amd64
v3.0.10                   2020-03-13T14:11:53.774527401+08:00  linux/amd64,darwin/amd64
v3.0.11                   2020-03-13T15:31:06.94547891+08:00   linux/amd64,darwin/amd64
v3.0.12                   2020-03-20T11:36:28.18950808+08:00   linux/amd64,darwin/amd64
v3.1.0-beta.2             2020-03-19T00:48:48.266468238+08:00  linux/amd64,darwin/amd64
v3.1.0-rc                 2020-04-02T23:43:17.456327834+08:00  linux/amd64,darwin/amd64
v4.0.0-beta               2020-03-13T12:43:55.508190493+08:00  linux/amd64,darwin/amd64
v4.0.0-beta.1             2020-03-13T12:30:08.913759828+08:00  linux/amd64,darwin/amd64
v4.0.0-beta.2             2020-03-18T22:52:00.830626492+08:00  linux/amd64,darwin/amd64
v4.0.0-rc      YES        2020-04-09T00:10:32+08:00            linux/amd64,darwin/amd64
nightly                   2020-04-10T08:42:23+08:00            darwin/amd64,linux/amd64
```

### How to view the TiDB components supported by TiUP 

Execute the following command to view the TiDB components that TiUP supports:

```shell
tiup list
```

In the following output:

- `Name` is the supported component name
- `Installed` is whether or not the component is installed
- `Platforms` is the supported platform
- `Description` is the component description

```log
Available components (Last Modified: 2020-02-27T15:20:35+08:00):
Name               Installed                                                                                                             Platforms                 Description
----               ---------                                                                                                             ---------                 -----------
tidb               YES(v4.0.0-rc)                                                                                                    darwin/amd64,linux/amd64  TiDB is an open source distributed HTAP database compatible with the MySQL protocol
tikv               YES(v4.0.0-rc)                                                                                                    darwin/amd64,linux/amd64  Distributed transactional key-value database, originally created to complement TiDB
pd                 YES(v4.0.0-rc)                                                                                                    darwin/amd64,linux/amd64  PD is the abbreviation for Placement Driver. It is used to manage and schedule the TiKV cluster
playground         YES(v0.0.5)                                                                                                           darwin/amd64,linux/amd64  Bootstrap a local TiDB cluster
client                                                                                                                                   darwin/amd64,linux/amd64  A simple mysql client to connect TiDB
prometheus                                                                                                                               darwin/amd64,linux/amd64  The Prometheus monitoring system and time series database.
tpc                                                                                                                                      darwin/amd64,linux/amd64  A toolbox to benchmark workloads in TPC
package                                                                                                                                  darwin/amd64,linux/amd64  A toolbox to package tiup component
grafana                                                                                                                                  linux/amd64,darwin/amd64  Grafana is the open source analytics & monitoring solution for every database
alertmanager                                                                                                                             darwin/amd64,linux/amd64  Prometheus alertmanager
blackbox_exporter                                                                                                                        darwin/amd64,linux/amd64  Blackbox prober exporter
node_exporter                                                                                                                            darwin/amd64,linux/amd64  Exporter for machine metrics
pushgateway                                                                                                                              darwin/amd64,linux/amd64  Push acceptor for ephemeral and batch jobs
tiflash                                                                                                                                  linux/amd64               The TiFlash Columnar Storage Engine
drainer                                                                                                                                  linux/amd64               The drainer componet of TiDB binlog service
pump                                                                                                                                     linux/amd64               The pump componet of TiDB binlog service
cluster            YES(v0.4.6)  linux/amd64,darwin/amd64  Deploy a TiDB cluster for production
```

### How to check whether the NTP service is normal

1. Run the following command. If it returns `running`, then the NTP service is running.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

2. Run the `ntpstat` command. If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    synchronised to NTP server (85.199.214.101) at stratum 2
    time correct to within 91 ms
    polling server every 1024 s
    ```

    > **Note:**
    >
    > For the Ubuntu system, you need to install the `ntpstat` package.

- The following condition indicates the NTP service is not synchronizing normally:

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    unsynchronised
    ```

- The following condition indicates the NTP service is not running normally:

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    Unable to talk to NTP daemon. Is it running?
    ```

- To make the NTP service start synchronizing as soon as possible, run the following command. Replace `pool.ntp.org` with your NTP server.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop ntpd.service && \
    sudo ntpdate pool.ntp.org && \
    sudo systemctl start ntpd.service
    ```

- To install the NTP service manually on the CentOS 7 system, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum install ntp ntpdate && \
    sudo systemctl start ntpd.service && \
    sudo systemctl enable ntpd.service
    ```

### How to manually configure the SSH mutual trust and sudo without password

1. Log in to the deployment target machine respectively using the `root` user account, create the `tidb` user and set the login password.

    {{< copyable "shell-root" >}}

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2. To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

    {{< copyable "shell-root" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. Use the `tidb` user to log in to the Control Machine, and run the following command. Replace `10.0.1.1` with the IP of your deployment target machine, and enter the `tidb` user password of the deployment target machine as prompted. Successful execution indicates that SSH mutual trust is already created. This applies to other machines as well.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. Log in to the Control Machine using the `tidb` user account, and log in to the IP of the target machine using `ssh`. If you do not need to enter the password and can successfully log in, then the SSH mutual trust is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. After you login to the deployment target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

### How to stop the firewall service of deployment machines

1. Check the firewall status. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. Stop the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. Disable automatic start of the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. Check the firewall status.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status firewalld.service
    ```

### How to install the `numactl` tool

> **Note:**
>
> - Binding cores using NUMA is a method to isolate CPU resources and is suitable for deploying multiple instances on highly configured physical machines.
> - After completing deployment using `tiup cluster deploy`, you can use the `exec` command to perform cluster level management operations.

1. Log in to the target node to install. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum -y install numactl
    ```

2. Run the `exec` command using `tiup cluster` to install in batches.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec --help
    ```

    ```
    Run shell command on host in the tidb cluster

    Usage:
    cluster exec <cluster-name> [flags]

    Flags:
        --command string   the command run on cluster host (default "ls")
    -h, --help             help for exec
        --sudo             use root permissions (default false)
    ```

    To use the sudo privilege to execute the installation command for all the target machines in the `tidb-test` cluster, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```
