---
title: Replicate Data to MySQL-compatible Databases
summary: Learn how to replicate data to TiDB or MySQL using TiCDC.
---

# Replicate Data to MySQL-compatible Databases

This document describes how to replicate incremental data to the downstream TiDB database or other MySQL-compatible databases using TiCDC. It also introduces how to use the eventually consistent replication feature in disaster scenarios.

## Create a replication task

Create a replication task by running the following command:

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="mysql://root:123456@127.0.0.1:3306/" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--changefeed-id`: The ID of the replication task. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the replication task. For details, see [Configure sink URI with `mysql`/`tidb`](#configure-sink-uri-for-mysql-or-tidb).
- `--start-ts`: Specifies the starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: Specifies the ending TSO of the changefeed. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: Specifies the changefeed configuration file. For details, see [TiCDC Changefeed Configuration Parameters](/ticdc/ticdc-changefeed-config.md).

## Configure sink URI for MySQL or TiDB

Sink URI is used to specify the connection information of the TiCDC target system. The format is as follows:

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

> **Note:**
>
> `/path` is not used for the MySQL sink.

Sample configuration for MySQL:

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306"
```

The following are descriptions of sink URI parameters and parameter values that can be configured for MySQL or TiDB:

| Parameter/Parameter value    | Description                                             |
| :------------ | :------------------------------------------------ |
| `root`        | The username of the downstream database.                              |
| `123456`       | The password of the downstream database (can be encoded using Base64).                                      |
| `127.0.0.1`    | The IP address of the downstream database.                               |
| `3306`         | The port for the downstream data.                                 |
| `worker-count` | The number of SQL statements that can be concurrently executed to the downstream (optional, `16` by default).       |
| `max-txn-row`  | The size of a transaction batch that can be executed to the downstream (optional, `256` by default). |
| `ssl-ca` | The path of the CA certificate file needed to connect to the downstream MySQL instance (optional).  |
| `ssl-cert` | The path of the certificate file needed to connect to the downstream MySQL instance (optional). |
| `ssl-key` | The path of the certificate key file needed to connect to the downstream MySQL instance (optional). |
| `time-zone` | The time zone used when connecting to the downstream MySQL instance, which is effective since v4.0.8. This is an optional parameter. If this parameter is not specified, the time zone of TiCDC service processes is used. If this parameter is set to an empty value, no time zone is specified when TiCDC connects to the downstream MySQL instance and the default time zone of the downstream is used. |
| `transaction-atomicity`  |  The atomicity level of a transaction. This is an optional parameter, with the default value of `none`. When the value is `table`, TiCDC ensures the atomicity of a single-table transaction. When the value is `none`, TiCDC splits the single-table transaction.  |

To encode the database password in the sink URI using Base64, use the following command:

```shell
echo -n '123456' | base64   # '123456' is the password to be encoded.
```

The encoded password is `MTIzNDU2`:

```shell
MTIzNDU2
```

> **Note:**
>
> When the sink URI contains special characters such as `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`, you need to escape the special characters, for example, in [URI Encoder](https://meyerweb.com/eric/tools/dencoder/).

## Eventually consistent replication in disaster scenarios

Starting from v6.1.1, this feature becomes GA. Starting from v5.3.0, TiCDC supports backing up incremental data from an upstream TiDB cluster to an object storage or an NFS of the downstream cluster. When the upstream cluster encounters a disaster and becomes unavailable, TiCDC can restore the downstream data to the recent eventually consistent state. This is the eventually consistent replication capability provided by TiCDC. With this capability, you can switch applications to the downstream cluster quickly, avoiding long-time downtime and improving service continuity.

Currently, TiCDC can replicate incremental data from a TiDB cluster to another TiDB cluster or a MySQL-compatible database system (including Aurora, MySQL, and MariaDB). In case the upstream cluster crashes, TiCDC can restore data in the downstream cluster within 5 minutes, given the conditions that TiCDC replicates data normally before the crash, and the replication lag is small. It allows data loss of 10s at most, that is, RTO <= 5 min, and P95 RPO <= 10s.

TiCDC replication lag increases in the following scenarios:

- The TPS increases significantly in a short time.
- Large or long transactions occur in the upstream.
- The TiKV or TiCDC cluster in the upstream is reloaded or upgraded.
- Time-consuming DDL statements, such as `add index`, are executed in the upstream.
- The PD is configured with aggressive scheduling strategies, resulting in frequent transfer of Region leaders, or frequent Region merge or Region split.

> **Note:**
>
> Starting from v6.1.1, the eventually consistent replication feature of TiCDC supports Amazon S3-compatible object storage. Starting from v6.1.4, this feature supports GCS- and Azure-compatible object storage.

### Prerequisites

- Prepare a highly available object storage or NFS for storing TiCDC's real-time incremental data backup files. These files can be accessed in case of a disaster in the upstream.
- Enable this feature for changefeeds that need to have eventual consistency in disaster scenarios. To enable it, you can add the following configuration to the changefeed configuration file.

```toml
[consistent]
# Consistency level. Options include:
# - none: the default value. In a non-disaster scenario, eventual consistency is only guaranteed if and only if finished-ts is specified.
# - eventual: Uses redo log to guarantee eventual consistency in case of the primary cluster disasters.
level = "eventual"

# Individual redo log file size, in MiB. By default, it's 64. It is recommended to be no more than 128.
max-log-size = 64

# The interval for flushing or uploading redo logs to Amazon S3, in milliseconds. It is recommended that this configuration be equal to or greater than 2000.
flush-interval = 2000

# The path under which redo log backup is stored. The scheme can be nfs (NFS directory), or Amazon S3, GCS, and Azure (uploaded to object storage).
storage = "$SCHEME://logbucket/test-changefeed?endpoint=http://$ENDPOINT/"
```

### Disaster recovery

When a disaster happens in the primary cluster, you need to recover manually in the secondary cluster by running the `cdc redo` command. The recovery process is as follows.

1. Ensure that all the TiCDC processes have exited. This is to prevent the primary cluster from resuming service during data recovery and prevent TiCDC from restarting data synchronization.
2. Use cdc binary for data recovery. Run the following command:

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

In this command:

- `tmp-dir`: Specifies the temporary directory for downloading TiCDC incremental data backup files.
- `storage`: Specifies the address for storing the TiCDC incremental data backup files, either an URI of object storage or an NFS directory.
- `sink-uri`: Specifies the secondary cluster address to restore the data to. Scheme can only be `mysql`.
