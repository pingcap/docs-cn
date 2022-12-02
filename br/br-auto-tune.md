---
title: Backup Auto-Tune
summary: Learn about the auto-tune feature of TiDB backup and restore, which automatically limits the resources used by backups to reduce the impact on the cluster in case of high cluster resource usage.
---

# Backup Auto-Tune <span class="version-mark">New in v5.4.0</span>

Before TiDB v5.4.0, when you back up data using Backup & Restore (BR), the number of threads used for backup makes up 75% of the logical CPU cores. Without a speed limit, the backup process can consume a lot of cluster resources, which has a considerable impact on the performance of the online cluster. Although you can reduce the impact of backup by adjusting the size of the thread pool, it is a tedious task to observe the CPU load and manually adjust the thread pool size.

To reduce the impact of backup tasks on the cluster, TiDB v5.4.0 introduces the auto-tune feature, which is enabled by default. When the cluster resource utilization is high, BR automatically limits the resources used by backup tasks and thereby reduces their impact on the cluster. The auto-tune feature is enabled by default.

## Usage scenario

If you want to reduce the impact of backup tasks on the cluster, you can enable the auto-tune feature. With this feature enabled, TiDB performs backup tasks as fast as possible without excessively affecting the cluster.

Alternatively, you can limit the backup speed by using the TiKV configuration item [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) or using the parameter `--ratelimit`.

## Use auto-tune

The auto-tune feature is enabled by default, without additional configuration.

> **Note:**
>
> For clusters that upgrade from v5.3.x to v5.4.0 or later versions, the auto-tune feature is disabled by default. You need to manually enable it.

To manually enable the auto-tune feature, you need to set the TiKV configuration item [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) to `true`.

TiKV supports dynamically configuring the auto-tune feature. You can enable or disable the feature without restarting your cluster. To dynamically enable or disable the auto-tune feature, run the following command:

{{< copyable "shell-regular" >}}

```shell
tikv-ctl modify-tikv-config -n backup.enable-auto-tune -v <true|false>
```

When you perform backup tasks on an offline cluster, to speed up the backup, you can modify the value of `backup.num-threads` to a larger number using `tikv-ctl`.

## Limitations

Auto-tune is a coarse-grained solution for limiting backup speed. It reduces the need for manual tuning. However, because of the lack of fine-grained control, auto-tune might not be able to completely remove the impact of backup on the cluster.

The auto-tune feature has the following issues and corresponding solutions:

- Issue 1: For **write-heavy clusters**, auto-tune might put the workload and backup tasks into a "positive feedback loop": the backup tasks take up too many resources, which causes the cluster to use fewer resources; at this point, auto-tune might mistakenly assume that the cluster is not under heavy workload and thus allowing backup to run faster. In such cases, auto-tune is ineffective.

    - Solution: Manually adjust `backup.num-threads` to a smaller number to limit the number of threads used by backup tasks. The working principle is as follows:

        The backup process includes lots of SST decoding, encoding, compression, and decompression, which consume CPU resources. In addition, previous test cases have shown that during the backup process, the CPU utilization of the thread pool used for backup is close to 100%. This means that the backup tasks take up a lot of CPU resources. By adjusting the number of threads used by the backup tasks, TiKV can limit the CPU cores used by backup tasks, thus reducing the impact of backup tasks on the cluster performance.

- Issue 2: For **clusters with hotspots**, backup tasks on the TiKV node that has hotspots might be excessively limited, which slows down the overall backup process.

    - Solution: Eliminate the hotspot node, or disable auto-tune on the hotspot node (this might reduce the cluster performance).

- Issue 3: For scenarios with **high traffic jitter**, because auto-tune adjusts the speed limit on a fixed interval (1 minute by default), it might not be able to handle high traffic jitter. For details, see [`auto-tune-refresh-interval`](#implementation).

    - Solution: Disable auto-tune.

## Implementation

Auto-tune adjusts the size of the thread pool used by backup tasks to ensure that the overall CPU utilization of the cluster does not exceed a specific threshold.

This feature has two related configuration items not listed in the TiKV configuration file. These two configuration items are only for internal tuning. You do **not** need to configure these two configuration items when you perform backup tasks.

- `backup.auto-tune-remain-threads`:

    - Auto-tune controls the resources used by the backup tasks and ensures that at least `backup.auto-tune-remain-threads` cores are available for other tasks on the same node.
    - Default value: `round(0.2 * vCPU)`

- `backup.auto-tune-refresh-interval`:

    - Every `backup.auto-tune-refresh-interval` minute(s), auto-tune refreshes the statistics and recalculates the maximum number of CPU cores that backup tasks can use.
    - Default value: `1m`

The following is an example of how auto-tune works. `*` denotes a CPU core used by backup tasks. `^` denotes a CPU core used by other tasks. `-` denotes an idle CPU core.

```
|--------| The server has 8 logical CPU cores.
|****----| By default, `backup.num-threads` is `4`. Note that auto-tune makes sure that the thread pool size is never larger than `backup.num-threads`.
|^^****--| By default, `auto-tune-remain-threads` = round(8 * 0.2) = 2. Auto-tune adjusts the size of the thread pool to `4`.
|^^^^**--| Because the cluster workload gets higher, auto-tune adjusts the size of the thread pool to `2`. After that, the cluster still has 2 idle CPU cores.
```

In the **Backup CPU Utilization** panel, you can see the size of the thread pool adjusted by auto-tune:

![Grafana dashboard example of backup auto-tune metrics](/media/br/br-auto-throttle.png)

In the image above, the yellow semi-transparent area represents the threads available for backup tasks. You can see the CPU utilization of backup tasks does not go beyond the yellow area.
