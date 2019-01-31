---
title: Migration Overview
summary: Learn how to migrate data from MySQL to TiDB.
category: operations
---

# Migration Overview

## Overview

This document describes how to migrate data from MySQL to TiDB in detail.

See the following for the assumed MySQL and TiDB server information:

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|MySQL|127.0.0.1|3306|root|* |
|TiDB|127.0.0.1|4000|root|* |

## Scenarios

+ To import all the history data. This needs the following tools:
    - `mydumper`: to export data from MySQL.
    - `Loader`: to import data to TiDB.

+ To incrementally synchronize data after all the history data is imported. This needs the following tools:
    - `mydumper`: to export data from MySQL.
    - `Loader`: to import data to TiDB.
    - `Syncer`: to incrementally synchronize data from MySQL to TiDB.

        > **Note:** To incrementally synchronize data from MySQL to TiDB, the binary logging (binlog) must be enabled and must use the `row` format in MySQL.

### Enable binary logging (binlog) in MySQL

Before using the `syncer` tool, make sure:

+ Binlog is enabled in MySQL. See [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

+ Binlog must use the `row` format which is the recommended binlog format in MySQL 5.7. It can be configured using the following statement:

    ```bash
    SET GLOBAL binlog_format = ROW;
    ```

### Download the TiDB toolset (Linux)

```bash
# Download the tool package.
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256

# Extract the package.
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```
