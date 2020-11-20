---
title: Synchronous Replication for Dual Data Centers
summary: Learn how to configure synchronous replication for dual data centers.
---

# Synchronous Replication for Dual Data Centers

This document introduces how to configure synchronous replication for dual data centers.

> **Warning:**
>
> Synchronous replication is still an experimental feature. Do not use it in a production environment.

In the scenario of dual data centers, one is the primary center and the other is the DR (data recovery) center. When a Region has an odd number of replicas, more replicas are placed in the primary center. When the DR center is down for more than a specified period of time, the asynchronous mode is used by default for the replication between two centers.

To use the synchronous mode, you can configure it in the PD configuration file or change the replication mode manually using pd-ctl.

## Enable synchronous replication in the PD configuration file

The replication mode is controlled by PD. You can configure it in the PD configuration file when deploying a cluster. See the following example:

{{< copyable "" >}}

```toml
[replication-mode]
replication-mode = "dr-auto-sync"
[replication-mode.dr-auto-sync]
label-key = "zone"
primary = "z1"
dr = "z2"
primary-replicas = 2
dr-replicas = 1
wait-store-timeout = "1m"
wait-sync-timeout = "1m"
```

In the configuration above:

+ `dr-auto-sync` is the mode to enable synchronous replication.
+ The label key `zone` is used to distinguish different data centers.
+ TiKV instances with the `"z1"` value are considered in the primary data center, and TiKV instances with `"z2"` are in the DR data center.
+ `primary-replicas` is the number of replicas that should be placed in the primary data center.
+ `dr-replicas` is the number of replicas that should be placed in the DR data center.
+ `wait-store-timeout` is the time to wait before falling back to asynchronous replication.

To check the current replication state of the cluster, use the following URL:

{{< copyable "shell-regular" >}}

```bash
% curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

```bash
{
  "mode": "dr-auto-sync",
  "dr-auto-sync": {
    "label-key": "zone",
    "state": "sync"
  }
}
```

> **Note:**
>
> The replication state of the cluster indicates how all Regions are replicated, with the options of `async`, `sync-recover`, and `sync`.

After the cluster state becomes `sync`, it will not become `async` unless the number of down instances is larger than the specified number of replicas in either data center. Once the cluster state becomes `async`, PD requests TiKV to change the replication mode to `asynchronous` and checks whether TiKV instances are recovered from time to time. When the number of down instances is smaller than the number of replicas in both data centers, the cluster enters the `sync-recover` state, and then requests TiKV to change the replication mode to `synchronous`. After all Regions become `synchronous`, the cluster becomes `sync` again.

## Change the replication mode manually

You can use [`pd-ctl`](/pd-control.md) to change a cluster from `asynchronous` to `synchronous`.

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode dr-auto-sync
```

Or change back to `asynchronous`:

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode majority
```

You can also update the label key:

{{< copyable "shell-regular" >}}

```bash
>> config set replication-mode dr-auto-sync label-key dc
```
