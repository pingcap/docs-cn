---
title: Deploy a TiDB Cluster Offline Using TiUP
summary: Introduce how to deploy a TiDB cluster offline using TiUP.
aliases: ['/docs/dev/production-offline-deployment-using-tiup/']
---

# Deploy a TiDB Cluster Offline Using TiUP

This document describes how to deploy a TiDB cluster offline using TiUP.

## Step 1: Prepare the TiUP offline component package

### Option 1: Download the official TiUP offline component package

Download the offline mirror package of the TiDB server (including the TiUP offline component package) from the [Download TiDB](https://pingcap.com/download/) page.

### Option 2: Manually pack an offline component package using `tiup mirror clone`

The steps are below.

- Install the TiUP package manager online.

    1. Install the TiUP tool:

        {{< copyable "shell-regular" >}}

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2. Redeclare the global environment variables:

        {{< copyable "shell-regular" >}}

        ```shell
        source .bash_profile
        ```

    3. Confirm whether TiUP is installed:

        {{< copyable "shell-regular" >}}

        ```shell
        which tiup
        ```

- Pull the mirror using TiUP

    1. Pull the needed components on a machine that has access to the Internet:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        The command above creates a directory named `tidb-community-server-${version}-linux-amd64` in the current directory, which contains the component package necessary for starting a cluster.

    2. Pack the component package by using the `tar` command and send the package to the control machine in the isolated environment:

        {{< copyable "shell-regular" >}}

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz` is an independent offline environment package.

## Step 2: Deploy the offline TiUP component

After sending the package to the control machine of the target cluster, install the TiUP component by running the following command:

{{< copyable "shell-regular" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

The `local_install.sh` script automatically executes the `tiup mirror set tidb-community-server-${version}-linux-amd64` command to set the current mirror address to `tidb-community-server-${version}-linux-amd64`.

To switch the mirror to another directory, you can manually execute the `tiup mirror set <mirror-dir>` command. To switch the mirror to the online environment, you can execute the `tiup mirror set https://tiup-mirrors.pingcap.com` command.

## Step 3: Mount the TiKV data disk

> **Note:**
>
> It is recommended to use the EXT4 file system format for the data directory of the target machines that deploy TiKV. Compared with the XFS file system format, the EXT4 file system format has more deployment cases of TiDB clusters. For the production environment, use the EXT4 file system format.

Log in to the target machines using the `root` user account.

Format your data disks to the ext4 filesystem and add the `nodelalloc` and `noatime` mount options to the filesystem. It is required to add the `nodelalloc` option, or else the TiUP deployment cannot pass the test. The `noatime` option is optional.

> **Note:**
>
> If your data disks have been formatted to ext4 and have added the mount options, you can uninstall it by running the `umount /dev/nvme0n1p1` command, follow the steps starting from editing the `/etc/fstab` file, and add the options again to the filesystem.

Take the `/dev/nvme0n1` data disk as an example:

1. View the data disk:

    {{< copyable "shell-root" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. Create the partition table:

    {{< copyable "shell-root" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **Note:**
    >
    > Use the `lsblk` command to view the device number of the partition: for a `nvme` disk, the generated device number is usually `nvme0n1p1`; for a regular disk (for example, `/dev/sdb`), the generated device number is usually `sdb1`.

3. Format the data disk to the ext4 filesystem:

    {{< copyable "shell-root" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. View the partition UUID of the data disk:

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

5. Edit the `/etc/fstab` file and add the mount options:

    {{< copyable "shell-root" >}}

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. Mount the data disk:

    {{< copyable "shell-root" >}}

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7. Check whether the steps above take effect by using the following command:

    {{< copyable "shell-root" >}}

    ```bash
    mount -t ext4
    ```

    If the filesystem is ext4 and `nodelalloc` is included in the mount options, you have successfully mount the data disk ext4 filesystem with options on the target machines.

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

## Step 4: Edit the initialization configuration file `topology.yaml`

You need to manually create and edit the cluster initialization configuration file. For the full configuration template, refer to the [TiUP configuration parameter template](https://github.com/pingcap/tiup/blob/master/examples/topology.example.yaml).

Create a YAML configuration file on the control machine, such as `topology.yaml`:

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

server_configs:
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
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data,/data2/tiflash/data
cdc_servers:
  - host: 10.0.1.6
  - host: 10.0.1.7
  - host: 10.0.1.8
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

## Step 5: Deploy the TiDB cluster

Execute the following command to deploy the TiDB cluster:

{{< copyable "shell-regular" >}}

```bash
tiup cluster deploy tidb-test v4.0.0 topology.yaml --user tidb [-p] [-i /home/root/.ssh/gcp_rsa]
tiup cluster start tidb-test
```

> **Parameter description:**
>
> - The name of the cluster deployed by the TiUP cluster is `tidb-test`.
> - The deployment version is `v4.0.0`. To obtain other supported versions, run `tiup list tidb`.
> - The initialization configuration file is `topology.yaml`.
> - `–user tidb`: log in to the target machine using the `tidb` user account to complete the cluster deployment. The `tidb` user needs to have `ssh` and `sudo` privileges of the target machine. You can use other users with `ssh` and `sudo` privileges to complete the deployment.
> - `[-i]` and `[-p]`: optional. If you have configured login to the target machine without password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the `root` user (or other users specified by `-user`) that has access to the target machine. `[-p]` is used to input the user password interactively.

If you see the ``Deployed cluster `tidb-test` successfully`` output at the end of the log, the deployment is successful.

After the deployment, see [Deploy and Maintain TiDB Using TiUP](/tiup/tiup-cluster.md) for the cluster operations.

> **Note:**
>
> By default, TiDB and TiUP share usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
