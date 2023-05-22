---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
aliases: ['/docs/dev/pd-recover/','/docs/dev/reference/tools/pd-recover/']
---

# PD Recover User Guide

PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally.

## Compile from source code

+ [Go](https://golang.org/) 1.20 or later is required because the Go modules are used.
+ In the root directory of the [PD project](https://github.com/pingcap/pd), use the `make pd-recover` command to compile and generate `bin/pd-recover`.

> **Note:**
>
> Generally, you do not need to compile source code because the PD Control tool already exists in the released binary or Docker. However, developer users can refer to the instructions above for compiling source code.

## Download TiDB Toolkit

The PD Recover installation package is included in the TiDB Toolkit. To download the TiDB Toolkit, see [Download TiDB Tools](/download-ecosystem-tools.md).

The following sections introduce two methods to recover a PD cluster: recover from a surviving PD node and rebuild a PD cluster entirely.

## Method 1: Recover a PD cluster using a surviving PD node

When a majority of PD nodes in a cluster experience an unrecoverable error, the cluster becomes unable to provide services. If there are any surviving PD nodes, you can recover the service by selecting a surviving PD node and forcibly modifying the members of the Raft Group. The steps are as follows:

### Step 1: Stop all nodes

To prevent data corruption or other unrecoverable errors caused by interactions with PD parameters during the recovery process, stop the TiDB, TiKV, and TiFlash processes in the cluster.

### Step 2: Start the surviving PD node

Start the surviving PD node using the `--force-new-cluster` startup parameter. The following is an example:

```shell
./bin/pd-server --force-new-cluster --name=pd-127.0.0.10-2379 --client-urls=http://0.0.0.0:2379 --advertise-client-urls=http://127.0.0.1:2379 --peer-urls=http://0.0.0.0:2380 --advertise-peer-urls=http://127.0.0.1:2380 --config=conf/pd.toml
```

### Step 3: Repair metadata using `pd-recover`

Since this method relies on a minority PD node to recover the service, the node might contain outdated data. If the `alloc_id` and `tso` data roll back, the cluster data might be corrupted or unavailable. To prevent this, you need to use `pd-recover` to modify the metadata to ensure that the node can provide correct allocation IDs and TSO services. The following is an example:

```shell
./bin/pd-recover --from-old-member --endpoints=http://127.0.0.1:2379 # Specify the corresponding PD address
```

> **Note:**
>
> In this step, the `alloc_id` in the storage automatically increases by a safe value of `100000000`. As a result, the subsequent cluster will allocate larger IDs.
>
> Additionally, `pd-recover` does not modify the TSO. Therefore, before performing this step, make sure that the local time is later than the time when the failure occurs, and verify that the NTP clock synchronization service is enabled between the PD components before the failure. If it is not enabled, you need to adjust the local clock to a future time to prevent the TSO from rolling back.

### Step 4: Restart the PD node

Once you see the prompt message `recovery is successful`, restart the PD node.

### Step 5: Scale out PD and start the cluster

Scale out the PD cluster using the deployment tool and start the other components in the cluster. At this point, the PD service is available.

## Method 2: Entirely rebuild a PD cluster

This method is applicable to scenarios in which all PD data is lost, but the data of other components, such as TiDB, TiKV, and TiFlash, still exists.

### Step 1: Get cluster ID

The cluster ID can be obtained from the log of PD, TiKV, or TiDB. To get the cluster ID, you can view the log directly on the server.

#### Get cluster ID from PD log (recommended)

To get the cluster ID from the PD log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### Get cluster ID from TiDB log

To get the cluster ID from the TiDB log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### Get cluster ID from TiKV log

To get the cluster ID from the TiKV log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### Step 2: Get allocated ID

The allocated ID value you specify must be larger than the currently largest allocated ID value. To get allocated ID, you can either get it from the monitor, or view the log directly on the server.

#### Get allocated ID from the monitor (recommended)

To get allocated ID from the monitor, you need to make sure that the metrics you are viewing are the metrics of **the last PD leader**, and you can get the largest allocated ID from the **Current ID allocation** panel in PD dashboard.

#### Get allocated ID from PD log

To get the allocated ID from the PD log, you need to make sure that the log you are viewing is the log of **the last PD leader**, and you can get the maximum allocated ID by running the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

Or you can simply run the above command in all PD servers to find the largest one.

### Step 3: Deploy a new PD cluster

Before deploying a new PD cluster, you need to stop the existing PD cluster and then delete the previous data directory or specify a new data directory using `--data-dir`.

### Step 4: Use pd-recover

You only need to run `pd-recover` on one PD node.

{{< copyable "shell-regular" >}}

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### Step 5: Restart the whole cluster

When you see the prompted information that the recovery is successful, restart the whole cluster.

## FAQ

### Multiple cluster IDs are found when getting the cluster ID

When a PD cluster is created, a new cluster ID is generated. You can determine the cluster ID of the old cluster by viewing the log.

### The error `dial tcp 10.0.1.13:2379: connect: connection refused` is returned when executing `pd-recover`

The PD service is required when you execute `pd-recover`. Deploy and start the PD cluster before you use PD Recover.
