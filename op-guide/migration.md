---
title: Migrating Data from MySQL to TiDB
category: advanced
---

# Migrating Data from MySQL to TiDB

## Overview

This document describes how to migrate data from MySQL to TiDB in detail.

See the following for the assumed MySQL and TiDB server information:


|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|MySQL|127.0.0.1|3306|root||
|TiDB|127.0.0.1|4000|root||

## Step 1. Using the `checker` tool to check the Schema

Before migrating, you can use the `checker` tool in TiDB to check if TiDB supports the table schema of the data to be migrated in advance. If the `checker` fails to check a certain table schema, it means that the table is not currently supported by TiDB and therefore the data in the table cannot be migrated. 
See [Downloading the TiDB Toolset](#downloading-the-tidb-toolset) to download the `checker` tool.

### Downloading the TiDB Toolset

#### Linux

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

1\. Create several tables in the `test` database in MySQL and insert data.

```bash
USE test;
CREATE TABLE t1 (id INT, age INT, PRIMARY KEY(id)) ENGINE=InnoDB;
CREATE TABLE t2 (id INT, name VARCHAR(256), PRIMARY KEY(id)) ENGINE=InnoDB;

INSERT INTO t1 VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t2 VALUES (1, "a"), (2, "b"), (3, "c");
```

2\. Use the `checker` tool to check all the tables in the `test` database.

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test
2016/10/27 13:11:49 checker.go:48: [info] Checking database test
2016/10/27 13:11:49 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2016/10/27 13:11:49 checker.go:63: [info] Checking table t1
2016/10/27 13:11:49 checker.go:69: [info] Check table t1 succ
2016/10/27 13:11:49 checker.go:63: [info] Checking table t2
2016/10/27 13:11:49 checker.go:69: [info] Check table t2 succ
```

3\. Use the `checker` tool to check one of the tables in the `test` database.

**Note:** Assuming you need to migrate the `t1` table only in this sample.

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test t1
2016/10/27 13:13:56 checker.go:48: [info] Checking database test
2016/10/27 13:13:56 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2016/10/27 13:13:56 checker.go:63: [info] Checking table t1
2016/10/27 13:13:56 checker.go:69: [info] Check table t1 succ
Check database succ!
```

### A sample of a table that cannot be migrated

1\. Create the following `t_error` table in MySQL:
```bash
CREATE TABLE t_error (
  c timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```


2\. Use the `checker` tool to check the table. If the following error is displayed, the `t_error` table cannot be migrated.

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test t_error
2016/10/27 13:19:28 checker.go:48: [info] Checking database test
2016/10/27 13:19:28 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2016/10/27 13:19:28 checker.go:63: [info] Checking table t_error
2016/10/27 13:19:28 checker.go:67: [error] Check table t_error failed with err: line 1 column 56 near ") ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1"
github.com/pingcap/tidb/parser/yy_parser.go:111:
github.com/pingcap/tidb/parser/yy_parser.go:124:
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/github.com/pingcap/tidb-tools/checker/checker.go:122:  parse CREATE TABLE `t_error` (
  `c` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 error
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/github.com/pingcap/tidb-tools/checker/checker.go:114:
2016/10/27 13:19:28 main.go:68: [error] Check database test with 1 errors and 0 warnings.
```


## Step 2. Using the `mydumper` / `loader` tool to export and import data in full volume

You can use `mydumper` to export data from MySQL and `loader` to import the data into TiDB.

**Note:** Although TiDB also supports the official `mysqldump` tool from MySQL for data migration, it is not recommended to use the `mysqldump` tool. Its performance is much slower than `mydumper` / `loader` and it costs a lot of time to migrate large amounts of data.

`mydumper`/`loader` is a more powerful tool to migrate data. For more information, see [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper).

###1. Downloading the Binary

#### Linux

```bash
# Download the mydumper package.
wget http://download.pingcap.org/mydumper-linux-amd64.tar.gz
wget http://download.pingcap.org/mydumper-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct. 
sha256sum -c mydumper-linux-amd64.sha256 
# Extract the package.
tar -xzf mydumper-linux-amd64.tar.gz
cd mydumper-linux-amd64
```

###2. Exporting data from MySQL 

Use the `mydumper` tool to export data from MySQL by typing the following command:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 128 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```
In this command, 
+ `-B test`: means the data is exported from the `test` database.
+ `-T t1,t2`: means only the `t1` and `t2` tables are exported.
+ `-t 16`: means 16 threads are used to export the data.
+ `-F 128`: means a table is partitioned into chunks and one chunk is 128MB.
+ `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

**Note:**
On the Cloud platforms which require the `super privilege`, such as on the Aliyun platform, add the `--no-locks` parameter to the command. If not, you might get the error message that you don't have the privilege.

###3. Importing data to TiDB

Use the `loader` tool to import the data from MySQL to TiDB

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 4 -d ./var/test
```
In this command, 
+ `-q 1` means how many queries are included in this transaction. The default value is 1000. In this example, we use `1`.

After the data is imported, you can view the data in TiDB using the official MySQL client:

```bash
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```

## Step 3. Using the `syncer` tool to import data incrementally

The previous section introduces how to import data from MySQL to TiDB in full volume using `mydumper`/`loader`. But this is not applicable if the data in MySQL is updated after the migration and it is expected to import the updated data quickly.

Therefore, TiDB provides the `syncer` tool for an incremental data import from MySQL to TiDB easily.

See [Downloading the TiDB Enterprise Toolset](#downloading-the-tidb-enterprise-toolset) to download the `syncer` tool.

### Downloading the TiDB Enterprise Toolset

#### Linux

```bash
# Download the enterpise tool package.
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
# Extract the package.
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```

Assuming the data from `t1` and `t2` is already imported to TiDB using `mydumper`/`loader`. Now we hope that any updates to these two tables are synchronized to the TiDB in real time.

###1. Enabling binary logging (binlog) in MySQL

Before using the `syncer` tool, make sure:
+ Binlog is enabled in MySQL. See [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

+ Binlog must use the `row` format which is the recommended binlog format in MySQL 5.7. It can be configured using the following statement:

    ```bash
    SET GLOBAL binlog_format = ROW;
    ``` 

###2. Obtaining the position to synchronize

Use the `show master status` statement to get the position of the current binlog, which is the  initial synchronizing position for `syncer`. 

```bash
show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |     1280 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
```

The information about the position is stored in the `syncer.meta` file for `syncer`:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 1280
```
**Note:** The `syncer.meta` file only needs to be configured once when it is first used. The position will be automatically updated when binlog is synchronized. 

###3. Start `syncer`

The `config.toml` file for `syncer`:

```toml
log-level = "info"

server-id = 101

meta = "./syncer.meta"
worker-count = 16
batch = 10

status-addr = ":10081"

skip-sqls = ["ALTER USER", "CREATE USER"]

##replicate-do-db priority over replicate-do-table if have same db name
##and we support regex expression , start with '~' declare use regex expression.
#
#replicate-do-db = ["~^b.*","s1"]
#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "log"

#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "~^a.*"

# skip prefix mathched sqls
# skip-sqls = ["^ALTER\\s+USER", "^CREATE\\s+USER"]

# 1. asterisk character (*, also called "star") matches zero or more characters,
#    for example, doc* matches doc and document but not dodo;
#    asterisk character must be in the end of wildcard word,
#    and there is only one asterisk in one wildcard word
# 2. the question mark ? matches exactly one character
#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "abc_*"
#target-schema = "route"
#target-table = "abc"

#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "xyz_*"
#target-schema = "route"
#target-table = "xyz"

[from]
host = "127.0.0.1"
user = "root"
password = ""
port = 3306

[to]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000
```

Start `syncer`:

```bash
./bin/syncer -config config.toml

2016/10/27 15:22:01 binlogsyncer.go:226: [info] begin to sync binlog from position (mysql-bin.000003, 1280)
2016/10/27 15:22:01 binlogsyncer.go:130: [info] register slave for master server 127.0.0.1:3306
2016/10/27 15:22:01 binlogsyncer.go:552: [info] rotate to (mysql-bin.000003, 1280)
2016/10/27 15:22:01 syncer.go:549: [info] rotate binlog to (mysql-bin.000003, 1280)
```

###4. Inserting data into MySQL

```bash
INSERT INTO t1 VALUES (4, 4), (5, 5);
```

###5. Login TiDB and view the data:

```bash
mysql -h127.0.0.1 -P4000 -uroot -p
mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
```

`syncer` outputs the current synchronized data statistics every 30 seconds:

```bash
2017/06/08 01:18:51 syncer.go:934: [info] [syncer]total events = 15, total tps = 130, recent tps = 4,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-17
2017/06/08 01:19:21 syncer.go:934: [info] [syncer]total events = 15, total tps = 191, recent tps = 2,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-35
```

You can see that by using `syncer`, the updates in MySQL can be automatically synchronized in TiDB.
