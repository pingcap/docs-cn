---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
aliases: ['/docs/dev/tiflash/troubleshoot-tiflash/']
---

# Troubleshoot a TiFlash Cluster

This section describes some commonly encountered issues when using TiFlash, the reasons, and the solutions.

## TiFlash fails to start

The issue might occur due to different reasons. It is recommended that you troubleshoot it following the steps below:

1. Check whether your system is RedHat Enterprise Linux 8.

     RedHat Enterprise Linux 8 does not have the `libnsl.so` system library. You can manually install it via the following command:

     {{< copyable "shell-regular" >}}

     ```shell
     dnf install libnsl
     ```

2. Check your system's `ulimit` parameter setting.

     {{< copyable "shell-regular" >}}

     ```shell
     ulimit -n 1000000
     ```

3. Use the PD Control tool to check whether there is any TiFlash instance that failed to go offline on the node (same IP and Port) and force the instance(s) to go offline. For detailed steps, refer to [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

If the above methods cannot resolve your issue, save the TiFlash log files and [get support](/support.md) from PingCAP or the community.

## TiFlash replica is always unavailable

This is because TiFlash is in an abnormal state caused by configuration errors or environment issues. Take the following steps to identify the faulty component:

1. Check whether PD enables the `Placement Rules` feature:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    - If `true` is returned, go to the next step.
    - If `false` is returned, [enable the Placement Rules feature](/configure-placement-rules.md#enable-placement-rules) and go to the next step.

2. Check whether the TiFlash process is working correctly by viewing `UpTime` on the TiFlash-Summary monitoring panel.

3. Check whether the TiFlash proxy status is normal through `pd-ctl`.

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    The TiFlash proxy's `store.labels` includes information such as `{"key": "engine", "value": "tiflash"}`. You can check this information to confirm a TiFlash proxy.

4. Check whether `pd buddy` can correctly print the logs (the log path is the value of `log` in the [flash.flash_cluster] configuration item; the default log path is under the `tmp` directory configured in the TiFlash configuration file).

5. Check whether the number of configured replicas is less than or equal to the number of TiKV nodes in the cluster. If not, PD cannot replicate data to TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    Reconfirm the value of `default: count`.

    > **Note:**
    >
    > After the [placement rules](/configure-placement-rules.md) feature is enabled, the previously configured `max-replicas` and `location-labels` no longer take effect. To adjust the replica policy, use the interface related to placement rules.

6. Check whether the remaining disk space of the machine (where `store` of the TiFlash node is) is sufficient. By default, when the remaining disk space is less than 20% of the `store` capacity (which is controlled by the `low-space-ratio` parameter), PD cannot schedule data to this TiFlash node.

## Some queries return the `Region Unavailable` error

If the load pressure on TiFlash is too heavy and it causes that TiFlash data replication falls behind, some queries might return the `Region Unavailable` error.

In this case, you can balance the load pressure by adding more TiFlash nodes.

## Data file corruption

Take the following steps to handle the data file corruption:

1. Refer to [Take a TiFlash node down](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster) to take the corresponding TiFlash node down.
2. Delete the related data of the TiFlash node.
3. Redeploy the TiFlash node in the cluster.

## TiFlash analysis is slow

If a statement contains operators or functions not supported in the MPP mode, TiDB does not select the MPP mode. Therefore, the analysis of the statement is slow. In this case, you can execute the `EXPLAIN` statement to check for operators or functions not supported in the MPP mode.

{{< copyable "sql" >}}

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

In this example, the warning message shows that TiDB does not select the MPP mode because TiDB 5.4 and earlier versions do not support the `subtime` function.

```
+---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## Data is not replicated to TiFlash

After deploying a TiFlash node and starting replication (by performing the ALTER operation), no data is replicated to it. In this case, you can identify and address the problem by following the steps below:

1. Check whether the replication is successful by running the `ALTER table <tbl_name> set tiflash replica <num>` command and check the output.

    - If there is output, go to the next step.
    - If there is no output, run the `SELECT * FROM information_schema.tiflash_replica` command to check whether TiFlash replicas have been created. If not, run the `ALTER table ${tbl_name} set tiflash replica ${num}` command again, check whether other statements (for example, `add index`) have been executed, or check whether DDL executions are successful.

2. Check whether the TiFlash process runs correctly.

   Check whether there is any change in `progress`, the `flash_region_count` parameter in the `tiflash_cluster_manager.log` file, and the Grafana monitoring item `Uptime`:

   - If yes, the TiFlash process runs correctly.
   - If no, the TiFlash process is abnormal. Check the `tiflash` log for further information.

3. Check whether the [Placement Rules](/configure-placement-rules.md) function has been enabled by using pd-ctl:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    - If `true` is returned, go to the next step.
    - If `false` is returned, [enable the Placement Rules feature](/configure-placement-rules.md#enable-placement-rules) and go to the next step.

4. Check whether the `max-replicas` configuration is correct:

    - If the value of `max-replicas` does not exceed the number of TiKV nodes in the cluster, go to the next step.
    - If the value of `max-replicas` is greater than the number of TiKV nodes in the cluster, the PD does not replicate data to the TiFlash node. To address this issue, change `max-replicas` to an integer fewer than or equal to the number of TiKV nodes in the cluster.

    > **Note:**
    >
    > `max-replicas` is defaulted to 3. In production environments, the value is usually fewer than the number of TiKV nodes. In test environments, the value can be 1.

    {{< copyable "shell-regular" >}}

    ```shell
        curl -X POST -d '{
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3,
            "location_labels": [
            "host"
            ]
        }' <http://172.16.x.xxx:2379/pd/api/v1/config/rule>
    ```

5. Check whether the connection between TiDB or PD and TiFlash is normal.

    Search the `flash_cluster_manager.log` file for the `ERROR` keyword.

    - If no `ERROR` is found, the connection is normal. Go to the next step.
    - If `ERROR` is found, the connection is abnormal. Perform the following check.

      - Check whether the log records PD keywords.

          If PD keywords are found, check whether `raft.pd_addr` in the TiFlash configuration file is valid. Specifically, run the `curl '{pd-addr}/pd/api/v1/config/rules'` command and check whether there is any output in 5s.

      - Check whether the log records TiDB-related keywords.

          If TiDB keywords are found, check whether `flash.tidb_status_addr` in the TiFlash configuration file is valid. Specifically, run the `curl '{tidb-status-addr}/tiflash/replica'` command and check whether there is any output in 5s.

      - Check whether the nodes can ping through each other.

    > **Note:**
    >
    >  If the problem persists, collect logs of the corresponding component for troubleshooting.

6. Check whether `placement-rule` is created for tables.

    Search the `flash_cluster_manager.log` file for the `Set placement rule … table-<table_id>-r` keyword.

    - If the keyword is found, go to the next step.
    - If not, collect logs of the corresponding component for troubleshooting.

7. Check whether the PD schedules properly.

    Search the `pd.log` file for the `table-<table_id>-r` keyword and scheduling behaviors like `add operator`.

    - If the keyword is found, the PD schedules properly.
    - If not, the PD does not schedule properly. You can [get support](/support.md) from PingCAP or the community.

## Data replication gets stuck

If data replication on TiFlash starts normally but then all or some data fails to be replicated after a period of time, you can confirm or resolve the issue by performing the following steps:

1. Check the disk space.

    Check whether the disk space ratio is higher than the value of `low-space-ratio` (defaulted to 0.8. When the space usage of a node exceeds 80%, the PD stops migrating data to this node to avoid exhaustion of disk space).

    - If the disk usage ratio is greater than or equal to the value of `low-space-ratio`, the disk space is insufficient. To relieve the disk space, remove unnecessary files, such as `space_placeholder_file` (if necessary, set `reserve-space` to 0MB after removing the file) under the `${data}/flash/` folder.
    - If the disk usage ratio is less than the value of `low-space-ratio`, the disk space is sufficient. Go to the next step.

2. Check the network connectivity between TiKV, TiFlash, and PD.

    In `flash_cluster_manager.log`, check whether there are any new updates to `flash_region_count` corresponding to the table that gets stuck.

    - If no, go to the next step.
    - If yes, search for `down peer` (replication gets stuck if there is a peer that is down).

        - Run `pd-ctl region check-down-peer` to search for `down peer`.
        - If `down peer` is found, run `pd-ctl operator add remove-peer\<region-id> \<tiflash-store-id>` to remove it.

3. Check CPU usage.

    On Grafana, choose **TiFlash-Proxy-Details** > **Thread CPU** > **Region task worker pre-handle/generate snapshot CPU**. Check the CPU usage of `<instance-ip>:<instance-port>-region-worker`.

    If the curve is a straight line, the TiFlash node is stuck. Terminate the TiFlash process and restart it, or [get support](/support.md) from PingCAP or the community.

## Data replication is slow

The causes may vary. You can address the problem by performing the following steps.

1. Adjust the value of the scheduling parameters.

    - Increase [`store limit`](/configure-store-limit.md#usage) to accelerate replication.
    - Decrease [`config set patrol-region-interval 10ms`](/pd-control.md#command) to make checker scan on Regions more frequent in TiKV.
    - Increase [`region merge`](/pd-control.md#command) to reduce the number of Regions, which means fewer scans and higher check frequencies.

2. Adjust the load on TiFlsh.

    Excessively high load on TiFlash can also result in slow replication. You can check the load of TiFlash indicators on the **TiFlash-Summary** panel on Grafana:

    - `Applying snapshots Count`: `TiFlash-summary` > `raft` > `Applying snapshots Count`
    - `Snapshot Predecode Duration`: `TiFlash-summary` > `raft` > `Snapshot Predecode Duration`
    - `Snapshot Flush Duration`: `TiFlash-summary` > `raft` > `Snapshot Flush Duration`
    - `Write Stall Duration`: `TiFlash-summary` > `Storage Write Stall` > `Write Stall Duration`
    - `generate snapshot CPU`: `TiFlash-Proxy-Details` > `Thread CPU` > `Region task worker pre-handle/generate snapshot CPU`

    Based on your service priorities, adjust the load accordingly to achieve optimal performance.
