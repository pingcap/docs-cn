---
title: Scale the TiDB Cluster Using TiUP
summary: Learn how to scale the TiDB cluster using TiUP.
aliases: ['/docs/dev/scale-tidb-using-tiup/','/docs/dev/how-to/scale/with-tiup/']
---

# Scale the TiDB Cluster Using TiUP

The capacity of a TiDB cluster can be increased or decreased without interrupting the online services.

This document describes how to scale the TiDB, TiKV, PD, TiCDC, or TiFlash cluster using TiUP. If you have not installed TiUP, refer to the steps in [Install TiUP on the control machine](/production-deployment-using-tiup.md#step-2-install-tiup-on-the-control-machine).

To view the current cluster name list, run `tiup cluster list`.

For example, if the original topology of the cluster is as follows:

| Host IP | Service |
|:---|:----|
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD |
| 10.0.1.5 | TiKV + Monitor |
| 10.0.1.1 | TiKV |
| 10.0.1.2 | TiKV |

## Scale out a TiDB/PD/TiKV cluster

If you want to add a TiDB node to the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to add the PD node. Before you add the TiKV node, it is recommended that you adjust the PD scheduling parameters in advance according to the cluster load.

1. Configure the scale-out topology:

    > **Note:**
    >
    > * The port and directory information is not required by default.
    > * If multiple instances are deployed on a single machine, you need to allocate different ports and directories for them. If the ports or directories have conflicts, you will receive a notification during deployment or scaling.
    > * Since TiUP v1.0.0, the scale-out configuration will inherit the global configuration of the original cluster.

    Add the scale-out topology configuration in the `scale-out.yaml` file:

    {{< copyable "shell-regular" >}}

    ```shell
    vi scale-out.yaml
    ```

    {{< copyable "" >}}

    ```ini
    tidb_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 4000
      status_port: 10080
      deploy_dir: /data/deploy/install/deploy/tidb-4000
      log_dir: /data/deploy/install/log/tidb-4000
    ```

    Here is a TiKV configuration file template:

    {{< copyable "" >}}

    ```ini
    tikv_servers:
    - host: 10.0.1.5
        ssh_port: 22
        port: 20160
        status_port: 20180
        deploy_dir: /data/deploy/install/deploy/tikv-20160
        data_dir: /data/deploy/install/data/tikv-20160
        log_dir: /data/deploy/install/log/tikv-20160
    ```

    Here is a PD configuration file template:

    {{< copyable "" >}}

    ```ini
    pd_servers:
    - host: 10.0.1.5
        ssh_port: 22
        name: pd-1
        client_port: 2379
        peer_port: 2380
        deploy_dir: /data/deploy/install/deploy/pd-2379
        data_dir: /data/deploy/install/data/pd-2379
        log_dir: /data/deploy/install/log/pd-2379
    ```

    To view the configuration of the current cluster, run `tiup cluster edit-config <cluster-name>`. Because the parameter configuration of `global` and `server_configs` is inherited by `scale-out.yaml` and thus also takes effect in `scale-out.yaml`.

    After the configuration, the current topology of the cluster is as follows:

    | Host IP | Service |
    |:---|:----|
    | 10.0.1.3   | TiDB + TiFlash   |
    | 10.0.1.4   | TiDB + PD   |
    | 10.0.1.5   | **TiDB** + TiKV + Monitor   |
    | 10.0.1.1   | TiKV    |
    | 10.0.1.2   | TiKV    |

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **Note:**
    >
    > The command above is based on the assumption that the mutual trust has been configured for the user to execute the command and the new machine. If the mutual trust cannot be configured, use the `-p` option to enter the password of the new machine, or use the `-i` option to specify the private key file.

    If you see the `Scaled cluster <cluster-name> out successfully`, the scale-out operation is successfully completed.

3. Check the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser to monitor the status of the cluster and the new node.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | **TiDB** + TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale out a TiFlash cluster

If you want to add a TiFlash node to the `10.0.1.4` host, take the following steps.

> **Note:**
>
> When adding a TiFlash node to an existing TiDB cluster, you need to note the following things:
>
> 1. Confirm that the current TiDB version supports using TiFlash. Otherwise, upgrade your TiDB cluster to v5.0 or later versions.
> 2. Execute the `tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true` command to enable the Placement Rules feature. Or execute the corresponding command in [pd-ctl](/pd-control.md).

1. Add the node information to the `scale-out.yaml` file:

    Create the `scale-out.yaml` file to add the TiFlash node information.

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 10.0.1.4
    ```

    Currently, you can only add IP but not domain name.

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **Note:**
    >
    > The command above is based on the assumption that the mutual trust has been configured for the user to execute the command and the new machine. If the mutual trust cannot be configured, use the `-p` option to enter the password of the new machine, or use the `-i` option to specify the private key file.

3. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster and the new node.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + **TiFlash**    |
| 10.0.1.5   | TiDB+ TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale out a TiCDC cluster

If you want to add two TiCDC nodes to the `10.0.1.3` and `10.0.1.4` hosts, take the following steps.

1. Add the node information to the `scale-out.yaml` file:

    Create the `scale-out.yaml` file to add the TiCDC node information.

    {{< copyable "" >}}

    ```ini
    cdc_servers:
      - host: 10.0.1.3
      - host: 10.0.1.4
    ```

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **Note:**
    >
    > The command above is based on the assumption that the mutual trust has been configured for the user to execute the command and the new machine. If the mutual trust cannot be configured, use the `-p` option to enter the password of the new machine, or use the `-i` option to specify the private key file.

3. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster and the new nodes.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + **TiCDC**  |
| 10.0.1.4   | TiDB + PD + TiFlash + **TiCDC**  |
| 10.0.1.5   | TiDB+ TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale in a TiDB/PD/TiKV cluster

If you want to remove a TiKV node from the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to remove the TiDB and PD node.

1. View the node ID information:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ```
    Starting /root/.tiup/components/cluster/v1.5.0/cluster display <cluster-name>
    TiDB Cluster: <cluster-name>
    TiDB Version: v5.1.0
    ID              Role         Host        Ports                            Status  Data Dir                Deploy Dir
    --              ----         ----        -----                            ------  --------                ----------
    10.0.1.3:8300   cdc          10.0.1.3    8300                             Up      -                       deploy/cdc-8300
    10.0.1.4:8300   cdc          10.0.1.4    8300                             Up      -                       deploy/cdc-8300
    10.0.1.4:2379   pd           10.0.1.4    2379/2380                        Healthy data/pd-2379            deploy/pd-2379
    10.0.1.1:20160  tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.2:20160  tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.5:20160  tikv         10.0.1.5    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.3:4000   tidb         10.0.1.3    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.4:4000   tidb         10.0.1.4    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.5:4000   tidb         10.0.1.5    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.3:9000   tiflash      10.0.1.3    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.4:9000   tiflash      10.0.1.4    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.5:9090   prometheus   10.0.1.5    9090                             Up      data/prometheus-9090    deploy/prometheus-9090
    10.0.1.5:3000   grafana      10.0.1.5    3000                             Up      -                       deploy/grafana-3000
    10.0.1.5:9093   alertmanager 10.0.1.5    9093/9294                        Up      data/alertmanager-9093  deploy/alertmanager-9093
    ```

2. Run the scale-in command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
    ```

    The `--node` parameter is the ID of the node to be taken offline.

    If you see the `Scaled cluster <cluster-name> in successfully`, the scale-in operation is successfully completed.

3. Check the cluster status:

    The scale-in process takes some time. If the status of the node to be scaled in becomes `Tombstone`, that means the scale-in operation is successful.

    To check the scale-in status, run the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster.

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + TiFlash + TiCDC |
| 10.0.1.5   | TiDB + Monitor **(TiKV is deleted)**   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale in a TiFlash cluster

If you want to remove a TiFlash node from the `10.0.1.4` host, take the following steps.

### 1. Adjust the number of replicas of the tables according to the number of remaining TiFlash nodes

Before the node goes down, make sure that the number of remaining nodes in the TiFlash cluster is no smaller than the maximum number of replicas of all tables. Otherwise, modify the number of TiFlash replicas of the related tables.

1. For all tables whose replicas are greater than the number of remaining TiFlash nodes in the cluster, execute the following command in the TiDB client:

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. Wait for the TiFlash replicas of the related tables to be deleted. [Check the table replication progress](/tiflash/use-tiflash.md#check-the-replication-progress) and the replicas are deleted if the replication information of the related tables is not found.

### 2. Perform the scale-in operation

Next, perform the scale-in operation with one of the following solutions.

#### Solution 1: Use TiUP to remove a TiFlash node

1. First, confirm the name of the node to be taken down:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

2. Remove the TiFlash node (assume that the node name is `10.0.1.4:9000` from Step 1):

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

#### Solution 2: Manually remove a TiFlash node

In special cases (such as when a node needs to be forcibly taken down), or if the TiUP scale-in operation fails, you can manually remove a TiFlash node with the following steps.

1. Use the store command of pd-ctl to view the store ID corresponding to this TiFlash node.

    * Enter the store command in [pd-ctl](/pd-control.md) (the binary file is under `resources/bin` in the tidb-ansible directory).

    * If you use TiUP deployment, replace `pd-ctl` with `tiup ctl pd`:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store
        ```

        > **Note:**
        >
        > If multiple PD instances exist in the cluster, you only need to specify the IP address:port of an active PD instance in the above command.

2. Remove the TiFlash node in pd-ctl:

    * Enter `store delete <store_id>` in pd-ctl (`<store_id>` is the store ID of the TiFlash node found in the previous step.

    * If you use TiUP deployment, replace `pd-ctl` with `tiup ctl pd`:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

        > **Note:**
        >
        > If multiple PD instances exist in the cluster, you only need to specify the IP address:port of an active PD instance in the above command.
        
3. Wait for the store of the TiFlash node to disappear or for the `state_name` to become `Tombstone` before you stop the TiFlash process.

    If, after waiting for a long time, the node still fails to disappear or the `state_name` fails to become `Tombstone`, consider using the following command to force the node out of the cluster.

    **Note that the command will directly discard the replicas on the TiFlash node, which might cause the query to fail.**

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST 'http://<pd-address>/pd/api/v1/store/<store_id>/state?state=Tombstone'
    ```

4. Manually delete TiFlash data files (whose location can be found in the `data_dir` directory under the TiFlash configuration of the cluster topology file).

5. Manually update TiUP's cluster configuration file (delete the information of the TiFlash node that goes down in edit mode).

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

> **Note:**
>
> Before all TiFlash nodes in the cluster stop running, if not all tables replicated to TiFlash are canceled, you need to manually clean up the replication rules in PD, or the TiFlash node cannot be taken down successfully.

The steps to manually clean up the replication rules in PD are below:

1. View all data replication rules related to TiFlash in the current PD instance:

    {{< copyable "shell-regular" >}}

    ```shell
    curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
    ```

    ```
    [
      {
        "group_id": "tiflash",
        "id": "table-45-r",
        "override": true,
        "start_key": "7480000000000000FF2D5F720000000000FA",
        "end_key": "7480000000000000FF2E00000000000000F8",
        "role": "learner",
        "count": 1,
        "label_constraints": [
          {
            "key": "engine",
            "op": "in",
            "values": [
              "tiflash"
            ]
          }
        ]
      }
    ]
    ```

2. Remove all data replication rules related to TiFlash. Take the rule whose `id` is `table-45-r` as an example. Delete it by the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

## Scale in a TiCDC cluster

If you want to remove the TiCDC node from the `10.0.1.4` host, take the following steps:

1. Take the node offline:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
    ```

2. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster.

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + **(TiCDC is deleted）**  |
| 10.0.1.5   | TiDB + Monitor  |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |
