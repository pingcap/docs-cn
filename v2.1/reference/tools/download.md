---
title: Download
summary: Download the most officially maintained versions of TiDB enterprise tools.
category: reference
---

# Download

This document collects the available downloads for most officially maintained versions of TiDB enterprise tools.

## TiDB Binlog and TiDB Lightning

If you want to download the 2.1 version of [TiDB Binlog](/v2.1/reference/tidb-binlog-overview.md) or [TiDB Lightning](/v2.1/reference/tools/tidb-lightning/overview.md), directly download the TiDB package, because both TiDB Binlog and TiDB Lightning are included in the TiDB package.

In addition, the Kafka version of TiDB Binlog is also provided.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-v2.1.16-linux-amd64.tar.gz](http://download.pingcap.org/tidb-v2.1.16-linux-amd64.tar.gz) (TiDB Binlog, TiDB Lightning) | Linux | amd64 |[tidb-v2.1.16-linux-amd64.sha256](http://download.pingcap.org/tidb-v2.1.16-linux-amd64.sha256)|
| [tidb-binlog-kafka-linux-amd64.tar.gz](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz) (the Kafka version of TiDB Binlog) | Linux | amd64 |[tidb-binlog-kafka-linux-amd64.sha256](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256)|

## DM (Data Migration)

If you want to download the 1.0 GA version of [DM](/v2.1/reference/tools/data-migration/overview.md), click the download link in the following table.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [dm-v1.0.1-linux-amd64.tar.gz](http://download.pingcap.org/dm-v1.0.1-linux-amd64.tar.gz) | Linux | amd64 | [dm-v1.0.1-linux-amd64.sha256](http://download.pingcap.org/dm-v1.0.1-linux-amd64.sha256) |

If you want to download the latest version of [DM](/v2.1/reference/tools/data-migration/overview.md), click the download link in the following table. You can also check the [DM Release](https://github.com/pingcap/dm/releases) page.

| Package name | OS | Architecture |  SHA256 checksum |
|:---|:---|:---|:---|
| [dm-latest-linux-amd64.tar.gz](http://download.pingcap.org/dm-latest-linux-amd64.tar.gz) | Linux | amd64 | [dm-latest-linux-amd64.sha256](http://download.pingcap.org/dm-latest-linux-amd64.sha256) |

## Syncer, Loader, and Mydumper

If you want to download the latest version of [Syncer](/v2.1/reference/tools/syncer.md), [Loader](/v2.1/reference/tools/loader.md), or [Mydumper](/v2.1/reference/tools/mydumper.md), directly download the tidb-enterprise-tools package, because all these tools are included in this package.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-latest-linux-amd64.sha256](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256) |

This enterprise tools package includes all the following tools:

- Syncer
- Loader
- Mydumper
- [binlogctl](/v2.1/reference/tidb-binlog-overview.md#binlogctl-guide)
- ddl_checker
- [sync_diff_inspector](/v2.1/reference/tools/sync-diff-inspector/overview.md)
