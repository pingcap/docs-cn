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
    - `Checker`: to check if the shema is compatible with TiDB.
    - `Mydumper`: to export data from MySQL.
    - `Loader`: to import data to TiDB.

+ To incrementally replicate data after all the history data is imported. This needs the following tools:
    - `Checker`: to check if the shema is compatible with TiDB.
    - `Mydumper`: to export data from MySQL.
    - `Loader`: to import data to TiDB.
    - `Syncer`: to incrementally replicate data from MySQL to TiDB.

        > **Note:**
        >
        > To incrementally replicate data from MySQL to TiDB, the binary logging (binlog) must be enabled and must use the `row` format in MySQL.

### Enable binary logging (binlog) in MySQL

Before using the `syncer` tool, make sure:
+ Binlog is enabled in MySQL. See [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

+ Binlog must use the `row` format which is the recommended binlog format in MySQL 5.7. It can be configured using the following statement:

    ```bash
    SET GLOBAL binlog_format = ROW;
    ```

## Use the `checker` tool to check the schema

Before migrating, you can use the `checker` tool in TiDB to check if TiDB supports the table schema of the data to be migrated. If the `checker` fails to check a certain table schema, it means that the table is not currently supported by TiDB and therefore the data in the table cannot be migrated.

See [Download the TiDB toolset](#download-the-tidb-toolset-linux) to download the `checker` tool.

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

### A sample to use the `checker` tool

1. Create several tables in the `test` database in MySQL and insert data.

    ```sql
    USE test;
    CREATE TABLE t1 (id INT, age INT, PRIMARY KEY(id)) ENGINE=InnoDB;
    CREATE TABLE t2 (id INT, name VARCHAR(256), PRIMARY KEY(id)) ENGINE=InnoDB;

    INSERT INTO t1 VALUES (1, 1), (2, 2), (3, 3);
    INSERT INTO t2 VALUES (1, "a"), (2, "b"), (3, "c");
    ```

2. Use the `checker` tool to check all the tables in the `test` database.

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test
    2016/10/27 13:11:49 checker.go:48: [info] Checking database test
    2016/10/27 13:11:49 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t1
    2016/10/27 13:11:49 checker.go:69: [info] Check table t1 succ
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t2
    2016/10/27 13:11:49 checker.go:69: [info] Check table t2 succ
    ```

3. Use the `checker` tool to check one of the tables in the `test` database.

    > **Note:**
    >
    > Assuming you need to migrate the `t1` table only in this sample.

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test t1
    2016/10/27 13:13:56 checker.go:48: [info] Checking database test
    2016/10/27 13:13:56 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:13:56 checker.go:63: [info] Checking table t1
    2016/10/27 13:13:56 checker.go:69: [info] Check table t1 succ
    Check database succ!
    ```

### A sample of a table that cannot be migrated

1. Create the following `t_error` table in MySQL:

    ```sql
    CREATE TABLE t_error ( a INT NOT NULL, PRIMARY KEY (a))
    ENGINE=InnoDB TABLESPACE ts1
    PARTITION BY RANGE (a) PARTITIONS 3 (
    PARTITION P1 VALUES LESS THAN (2),
    PARTITION P2 VALUES LESS THAN (4) TABLESPACE ts2,
    PARTITION P3 VALUES LESS THAN (6) TABLESPACE ts3);
    ```
2. Use the `checker` tool to check the table. If the following error is displayed, the `t_error` table cannot be migrated.

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test t_error
    2017/08/04 11:14:35 checker.go:48: [info] Checking database test
    2017/08/04 11:14:35 main.go:39: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2017/08/04 11:14:35 checker.go:63: [info] Checking table t1
    2017/08/04 11:14:35 checker.go:67: [error] Check table t1 failed with err: line 3 column 29 near " ENGINE=InnoDB DEFAULT CHARSET=latin1
    /*!50100 PARTITION BY RANGE (a)
    (PARTITION P1 VALUES LESS THAN (2) ENGINE = InnoDB,
     PARTITION P2 VALUES LESS THAN (4) TABLESPACE = ts2 ENGINE = InnoDB,
     PARTITION P3 VALUES LESS THAN (6) TABLESPACE = ts3 ENGINE = InnoDB) */" (total length 354)
    github.com/pingcap/tidb/parser/yy_parser.go:96:
    github.com/pingcap/tidb/parser/yy_parser.go:109:
    /home/jenkins/workspace/build_tidb_tools_master/go/src/github.com/pingcap/tidb-tools/checker/checker.go:122:  parse CREATE TABLE `t1` (
      `a` int(11) NOT NULL,
      PRIMARY KEY (`a`)
    ) /*!50100 TABLESPACE ts1 */ ENGINE=InnoDB DEFAULT CHARSET=latin1
    /*!50100 PARTITION BY RANGE (a)
    (PARTITION P1 VALUES LESS THAN (2) ENGINE = InnoDB,
     PARTITION P2 VALUES LESS THAN (4) TABLESPACE = ts2 ENGINE = InnoDB,
     PARTITION P3 VALUES LESS THAN (6) TABLESPACE = ts3 ENGINE = InnoDB) */ error
    /home/jenkins/workspace/build_tidb_tools_master/go/src/github.com/pingcap/tidb-tools/checker/checker.go:114:
    2017/08/04 11:14:35 main.go:83: [error] Check database test with 1 errors and 0 warnings.
    ```
