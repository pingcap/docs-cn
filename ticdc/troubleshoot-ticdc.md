---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
aliases: ['/docs/dev/ticdc/troubleshoot-ticdc/']
---

# Troubleshoot TiCDC

This document introduces the common issues and errors that you might encounter when using TiCDC, and the corresponding maintenance and troubleshooting methods.

## How to choose `start-ts` when starting a task

The `start-ts` of a replication task corresponds to a Timestamp Oracle (TSO) in the upstream TiDB cluster. TiCDC requests data from this TSO in a replication task. Therefore, the `start-ts` of the replication task must meet the following requirements:

- The value of `start-ts` is larger than the `tikv_gc_safe_point` value of the current TiDB cluster. Otherwise, an error occurs when you create a task.
- Before starting a task, ensure that the downstream has all data before `start-ts`. For scenarios such as replicating data to message queues, if the data consistency between upstream and downstream is not required, you can relax this requirement according to your application need.

If you do not specify `start-ts`, or specify `start-ts` as `0`, when a replication task is started, TiCDC gets a current TSO and starts the task from this TSO.

## Some tables cannot be replicated when you start a task

When you execute `cdc cli changefeed create` to create a replication task, TiCDC checks whether the upstream tables meet the [replication restrictions](/ticdc/ticdc-overview.md#restrictions). If some tables do not meet the restrictions, `some tables are not eligible to replicate` is returned with a list of ineligible tables. You can choose `Y` or `y` to continue creating the task, and all updates on these tables are automatically ignored during the replication. If you choose an input other than `Y` or `y`, the replication task is not created.

## How to handle replication interruption

A replication task might be interrupted in the following known scenarios:

- The downstream continues to be abnormal, and TiCDC still fails after many retries.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling method: You can resume the replication task via the HTTP interface after the downstream is back to normal.

- Replication cannot continue because of incompatible SQL statement(s) in the downstream.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling procedures:
        1. Query the status information of the replication task using the `cdc cli changefeed query` command and record the value of `checkpoint-ts`.
        2. Use the new task configuration file and add the `ignore-txn-start-ts` parameter to skip the transaction corresponding to the specified `start-ts`.
        3. Stop the old replication task via HTTP API. Execute `cdc cli changefeed create` to create a new task and specify the new task configuration file. Specify `checkpoint-ts` recorded in step 1 as the `start-ts` and start a new task to resume the replication.

## `gc-ttl` and file sorting

Since v4.0.0-rc.1, PD supports external services in setting the service-level GC safepoint. Any service can register and update its GC safepoint. PD ensures that the key-value data smaller than this GC safepoint is not cleaned by GC. Enabling this feature in TiCDC ensures that the data to be consumed by TiCDC is retained in TiKV without being cleaned by GC when the replication task is unavailable or interrupted.

When starting the TiCDC server, you can specify the Time To Live (TTL) duration of GC safepoint through `gc-ttl`, which means the longest time that data is retained within the GC safepoint. This value is set by TiCDC in PD, which is 86,400 seconds by default.

If the replication task is interrupted for a long time and a large volume of unconsumed data is accumulated, Out of Memory (OOM) might occur when TiCDC is started. In this situation, you can enable the file sorting feature of TiCDC that uses system files for sorting. To enable this feature, pass `--sort-engine=file` and `--sort-dir=/path/to/sort_dir` to the `cdc cli` command when creating a replication task. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --sort-engine="file" --sort-dir="/data/cdc/sort"
```

> **Note:**
>
> TiCDC (the 4.0 version) does not support dynamically modifying the file sorting and memory sorting yet.
