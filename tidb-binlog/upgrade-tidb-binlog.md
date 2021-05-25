---
title: Upgrade TiDB Binlog
summary: Learn how to upgrade TiDB Binlog to the latest cluster version.
aliases: ['/docs/dev/tidb-binlog/upgrade-tidb-binlog/','/docs/dev/reference/tidb-binlog/upgrade/','/docs/dev/how-to/upgrade/tidb-binlog/']
---

# Upgrade TiDB Binlog

This document introduces how to upgrade TiDB Binlog that is deployed manually to the latest [cluster](/tidb-binlog/tidb-binlog-overview.md) version. There is also a section on how to upgrade TiDB Binlog from an earlier incompatible version (Kafka/Local version) to the latest version.

## Upgrade TiDB Binlog deployed manually

Follow the steps in this section if you deploy TiDB Binlog manually.

### Upgrade Pump

First, upgrade each Pump instance in the cluster one by one. This ensures that there are always Pump instances in the cluster that can receive binlogs from TiDB. The steps are as below:

1. Replace the original file with the new version of `pump`.
2. Restart the Pump process.

### Upgrade Drainer

Second, upgrade the Drainer component:

1. Replace the original file with the new version of `drainer`.
2. Restart the Drainer process.

## Upgrade TiDB Binlog from Kafka/Local version to the cluster version

The new TiDB versions (v2.0.8-binlog, v2.1.0-rc.5 or later) are not compatible with the Kafka version or Local version of TiDB Binlog. If TiDB is upgraded to one of the new versions, it is required to use the cluster version of TiDB Binlog. If the Kafka or local version of TiDB Binlog is used before upgrading, you need to upgrade your TiDB Binlog to the cluster version.

The corresponding relationship between TiDB Binlog versions and TiDB versions is shown in the following table:

| TiDB Binlog version | TiDB version                              | Note                                                                                       |
|---------------------|-------------------------------------------|--------------------------------------------------------------------------------------------|
| Local               | TiDB 1.0 or earlier                       |                                                                                            |
| Kafka               | TiDB 1.0 ~ TiDB 2.1 RC5                   | TiDB 1.0 supports both the local and Kafka versions of TiDB Binlog.                        |
| Cluster             | TiDB v2.0.8-binlog, TiDB 2.1 RC5 or later | TiDB v2.0.8-binlog is a special 2.0 version supporting the cluster version of TiDB Binlog. |

### Upgrade process

> **Note:**
>
> If importing the full data is acceptable, you can abandon the old version and deploy TiDB Binlog following [TiDB Binlog Cluster Deployment](/tidb-binlog/deploy-tidb-binlog.md).

If you want to resume replication from the original checkpoint, perform the following steps to upgrade TiDB Binlog:

1. Deploy the new version of Pump.
2. Stop the TiDB cluster service.
3. Upgrade TiDB and the configuration, and write the binlog data to the new Pump cluster.
4. Reconnect the TiDB cluster to the service.
5. Make sure that the old version of Drainer has replicated the data in the old version of Pump to the downstream completely;

    Query the `status` interface of Drainer，command as below：

    {{< copyable "shell-regular" >}}

    ```bash
    curl 'http://172.16.10.49:8249/status'
    ```

    ```
    {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}
    ```

    If the return value of `Synced` is True, it means Drainer has replicated the data in the old version of Pump to the downstream completely.

6. Start the new version of Drainer.
7. Close the Pump and Drainer of the old versions and the dependent Kafka and ZooKeeper.
