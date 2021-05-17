---
title: Deploy TiCDC
summary: Learn how to deploy TiCDC and the hardware and software recommendations for deploying and running it.
---

# Deploy TiCDC

This document describes how to deploy a TiCDC cluster and the hardware and software recommendations for deploying and running it. You can either deploy TiCDC along with a new TiDB cluster or add the TiCDC component to an existing TiDB cluster. Generally, it is recommended that you deploy TiCDC using TiUP. In addition, you can also deploy it using binary as needed.

## Software and hardware recommendations

In production environments, the recommendations of software and hardware for TiCDC are as follows:

| Linux OS       | Version         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 or later versions   |
| CentOS                   | 7.3 or later versions   |

| CPU | Memory | Disk type | Network | Number of TiCDC cluster instances (minimum requirements for production environment) |
| :--- | :--- | :--- | :--- | :--- |
| 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred） | 2 |

For more information, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

## Deploy a new TiDB cluster that includes TiCDC using TiUP

When you deploy a new TiDB cluster using TiUP, you can also deploy TiCDC at the same time. You only need to add the `cdc_servers` section in the initialization configuration file that TiUP uses to start the TiDB cluster. For detailed operations, see [Edit the initialization configuration file](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file). For detailed configurable fields, see [Configure `cdc_servers` using TiUP](/tiup/tiup-cluster-topology-reference.md#cdc_servers).

## Add TiCDC to an existing TiDB cluster using TiUP

You can also use TiUP to add the TiCDC component to an existing TiDB cluster. Take the following procedures:

1. Make sure that the current TiDB version supports TiCDC; otherwise, you need to upgrade the TiDB cluster to `v4.0.0-rc.1` or later versions. Since v4.0.6, TiCDC has become a feature for general availability (GA). It is recommended that you use v4.0.6 or later versions.

2. To deploy TiCDC, refer to [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster).

## Add TiCDC to an existing TiDB cluster using binary (not recommended)

Suppose that the PD cluster has a PD node (the client URL is `10.0.10.25:2379`) that can provide services. If you want to deploy three TiCDC nodes, start the TiCDC cluster by executing the following commands. You only need to specify the same PD address, and the newly started nodes automatically join the TiCDC cluster.

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

The following are descriptions of options available in the `cdc server` command:

- `gc-ttl`: The TTL (Time To Live) of the service level `GC safepoint` in PD set by TiCDC, in seconds. The default value is `86400`, which means 24 hours.
- `pd`: The URL of the PD client.
- `addr`: The listening address of TiCDC, the HTTP API address, and the Prometheus address of the service.
- `advertise-addr`: The access address of TiCDC to the outside world.
- `tz`: Time zone used by the TiCDC service. TiCDC uses this time zone when it internally converts time data types such as `TIMESTAMP` or when it replicates data to the downstream. The default is the local time zone in which the process runs. If you specify `time-zone` (in `sink-uri`) and `tz` at the time, the internal TiCDC processes use the time zone specified by `tz`, and the sink uses the time zone specified by `time-zone` for replicating data to the downstream.
- `log-file`: The address of the running log of the TiCDC process. The default is `cdc.log`.
- `log-level`: The log level when the TiCDC process is running. The default is `info`.
- `ca`: The path of the CA certificate file used by TiCDC, in the PEM format (optional).
- `cert`: The path of the certificate file used by TiCDC, in the PEM format (optional).
- `key`: The path of the certificate key file used by TiCDC, in the PEM format (optional).
- `config`: The address of the configuration file that TiCDC uses (optional). This option is supported since TiCDC v5.0.0. This option can be used in the TiCDC deployment since TiUP v1.4.0.
