---
title: Deploy a DM Cluster Offline Using TiUP
summary: Introduce how to deploy a DM cluster offline using TiUP.
---

# Deploy a DM Cluster Offline Using TiUP

This document describes how to deploy a DM cluster offline using TiUP.

## Step 1: Prepare the TiUP offline component package

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

        ```bash
        # You can modify ${version} to the needed version.
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --tiup=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}') --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        The command above creates a directory named `tidb-dm-${version}-linux-amd64` in the current directory, which contains the component package managed by TiUP.

    2. Pack the component package by using the `tar` command and send the package to the control machine in the isolated environment:

        {{< copyable "shell-regular" >}}

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        `tidb-dm-${version}-linux-amd64.tar.gz` is an independent offline environment package.

## Step 2: Deploy the offline TiUP component

After sending the package to the control machine of the target cluster, install the TiUP component by running the following command:

{{< copyable "shell-regular" >}}

```bash
# You can modify ${version} to the needed version.
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

The `local_install.sh` script automatically executes the `tiup mirror set tidb-dm-${version}-linux-amd64` command to set the current mirror address to `tidb-dm-${version}-linux-amd64`.

To switch the mirror to another directory, manually execute the `tiup mirror set <mirror-dir>` command. If you want to switch back to the official mirror, execute `tiup mirror set https://tiup-mirrors.pingcap.com`.

## Step 3: Edit the initialization configuration file

You need to edit the cluster initialization configuration file according to different cluster topologies.

For the full configuration template, refer to the [TiUP configuration parameter template](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml). Create a configuration file `topology.yaml`. In other combined scenarios, edit the configuration file as needed according to the templates.

The configuration of deploying three DM-masters, three DM-workers, and one monitoring component instance is as follows:

```yaml
---
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/home/tidb/dm/deploy"
  data_dir: "/home/tidb/dm/data"
  # arch: "amd64"

master_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

worker_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

monitoring_servers:
  - host: 172.19.0.101

grafana_servers:
  - host: 172.19.0.101

alertmanager_servers:
  - host: 172.19.0.101
```

> **Note:**
>
> - If you do not need to ensure high availability of the DM cluster, deploy only one DM-master node, and the number of deployed DM-worker nodes must be no less than the number of upstream MySQL/MariaDB instances to be migrated.
>
> - To ensure high availability of the DM cluster, it is recommended to deploy three DM-master nodes, and the number of deployed DM-worker nodes must be greater than the number of upstream MySQL/MariaDB instances to be migrated (for example, the number of DM-worker nodes is two more than the number of upstream instances).
>
> - For parameters that should be globally effective, configure these parameters of corresponding components in the `server_configs` section of the configuration file.
>
> - For parameters that should be effective on a specific node, configure these parameters in `config` of this node.
>
> - Use `.` to indicate the subcategory of the configuration, such as `log.slow-threshold`. For more formats, see [TiUP configuration template](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml).
>
> - For more parameter description, see [master `config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml) and [worker `config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml).
>
> - Make sure that the ports among the following components are interconnected:
>     - The `peer_port` (`8291` by default) among the DM-master nodes are interconnected.
>     - Each DM-master node can connect to the `port` of all DM-worker nodes (`8262` by default).
>     - Each DM-worker node can connect to the `port` of all DM-master nodes (`8261` by default).
>     - The TiUP nodes can connect to the `port` of all DM-master nodes (`8261` by default).
>     - The TiUP nodes can connect to the `port` of all DM-worker nodes (`8262` by default).

## Step 4: Execute the deployment command

> **Note:**
>
> You can use secret keys or interactive passwords for security authentication when you deploy DM using TiUP:
>
> - If you use secret keys, you can specify the path of the keys through `-i` or `--identity_file`;
> - If you use passwords, add the `-p` flag to enter the password interaction window;
> - If password-free login to the target machine has been configured, no authentication is required.

{{< copyable "shell-regular" >}}

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

In the above command:

- The name of the deployed DM cluster is `dm-test`.
- The version of the DM cluster is `${version}`. You can view the latest versions supported by TiUP by running `tiup list dm-master`.
- The initialization configuration file is `topology.yaml`.
- `--user root`: Log in to the target machine through the `root` key to complete the cluster deployment, or you can use other users with `ssh` and `sudo` privileges to complete the deployment.
- `[-i]` and `[-p]`: optional. If you have configured login to the target machine without password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the `root` user (or other users specified by `--user`) that has access to the target machine. `[-p]` is used to input the user password interactively.
- TiUP DM uses the embedded SSH client. If you want to use the SSH client native to the control machine system, edit the configuration according to [using the system's native SSH client to connect to the cluster](/dm/maintain-dm-using-tiup.md#use-the-systems-native-ssh-client-to-connect-to-cluster).

At the end of the output log, you will see ```Deployed cluster `dm-test` successfully```. This indicates that the deployment is successful.

## Step 5: Check the clusters managed by TiUP

{{< copyable "shell-regular" >}}

```shell
tiup dm list
```

TiUP supports managing multiple DM clusters. The command above outputs information of all the clusters currently managed by TiUP, including the name, deployment user, version, and secret key information:

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## Step 6: Check the status of the deployed DM cluster

To check the status of the `dm-test` cluster, execute the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dm display dm-test
```

Expected output includes the instance ID, role, host, listening port, and status (because the cluster is not started yet, so the status is `Down`/`inactive`), and directory information of the `dm-test` cluster.

## Step 7: Start the cluster

{{< copyable "shell-regular" >}}

```shell
tiup dm start dm-test
```

If the output log includes ```Started cluster `dm-test` successfully```, the start is successful.

## Step 8: Verify the running status of the cluster

Check the DM cluster status using TiUP:

{{< copyable "shell-regular" >}}

```shell
tiup dm display dm-test
```

If the `Status` is `Up` in the output, the cluster status is normal.
