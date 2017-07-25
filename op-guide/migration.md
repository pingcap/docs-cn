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
|MySQL|127.0.0.1|3306|root|* |
|TiDB|127.0.0.1|4000|root|* |


## Scenarios

 + To import all the history data. This needs the following tools:
	 - `Checker`: to check if the shema is compatible with TiDB.
	 - `Mydumper`: to export data from MySQL.
	 - `Loader`: to import data to TiDB.

 + To incrementally synchronise data after all the history data is imported. This needs the following tools:
	 - `Checker`: to check if the shema is compatible with TiDB.
	 - `Mydumper`: to export data from MySQL.
	 - `Loader`: to import data to TiDB.
	 - `Syncer`: to incrementally synchronise data from MySQL to TiDB.

	 **Note:** To incrementally synchronise data from MySQL to TiDB, the binary logging (binlog) must be enabled and must use the `row` format in MySQL.
	
### Enabling binary logging (binlog) in MySQL

Before using the `syncer` tool, make sure:
+ Binlog is enabled in MySQL. See [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

+ Binlog must use the `row` format which is the recommended binlog format in MySQL 5.7. It can be configured using the following statement:

    ```bash
    SET GLOBAL binlog_format = ROW;
    ``` 


## Step 1. Using the `checker` tool to check the Schema

Before migrating, you can use the `checker` tool in TiDB to check if TiDB supports the table schema of the data to be migrated. If the `checker` fails to check a certain table schema, it means that the table is not currently supported by TiDB and therefore the data in the table cannot be migrated.
 
See [Downloading the TiDB Toolset](#downloading-the-tidb-toolset) to download the `checker` tool.

### Downloading the TiDB Toolset (Linux)

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


## Step 2. Using the `mydumper` / `loader` tool to export and import all the data

You can use `mydumper` to export data from MySQL and `loader` to import the data into TiDB.

**Note:** Although TiDB also supports the official `mysqldump` tool from MySQL for data migration, it is not recommended to use the `mysqldump` tool. Its performance is much lower than `mydumper` / `loader` and it costs a lot of time to migrate large amounts of data. `mydumper`/`loader` is a more powerful tool to migrate data. For more information, see [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper).


### 1. Exporting data from MySQL 

Use the `mydumper` tool to export data from MySQL by using the following command:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```
In this command, 
+ `-B test`: means the data is exported from the `test` database.
+ `-T t1,t2`: means only the `t1` and `t2` tables are exported.
+ `-t 16`: means 16 threads are used to export the data.
+ `-F 64`: means a table is partitioned into chunks and one chunk is 64MB.
+ `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

**Note:**
On the Cloud platforms which require the `super privilege`, such as on the Aliyun platform, add the `--no-locks` parameter to the command. If not, you might get the error message that you don't have the privilege.

### 2. Importing data to TiDB


Use the `loader` tool to import the data from MySQL to TiDB. See [Loader instructions](./tools/loader.md) for more information.

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is imported, you can view the data in TiDB using the MySQL client:

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

### 3. Best practice
To migrate data quickly, especially for huge amount of data, you can refer to the following recommendations.

- Make the exported data file as small as possible and it is recommended not to exceed 64M. You can use the -F parameter to set the value.
- The -t parameter can be evaluated according to the number and the load of TiKV instances. For example, if there are three TiKV instances, -t can be set to 3 * (1 ~ n). If the load of TiKV is too high and the log `backoffer.maxSleep 15000ms is exceeded` appears many times, it's better to decrease -t; otherwise increase it.

### A sample, and the configuration

 - The total size of the exported files is 214G. A single table has 8 columns and 2 billion rows.
 - The cluster topology:
    - 12 TiKV instances: 4 nodes, 3 TiKV instances per node
    - 4 TiDB instances
    - 3 PD instances
 - The configuration of each node:
    - CPU: Intel Xeon E5-2670 v3 @ 2.30GHz
    - 48 vCPU [2 x 12 physical cores]
    - Memory: 128G
    - Disk: sda [raid 10, 300G] sdb[RAID 5, 2T]
    - OS: CentOS 7.2
 - the F parameter of mydumper is set to 16 and the -t parameter of loader is set to 64.

**Results**: It takes 11 hours to import all the data, which is 19.4G per hour.

## Step 3. (Optional) Using the `syncer` tool to import data incrementally

The previous section introduces how to import all the history data from MySQL to TiDB using `mydumper`/`loader`. But this is not applicable if the data in MySQL is updated after the migration and it is expected to import the updated data quickly.

Therefore, TiDB provides the `syncer` tool for an incremental data import from MySQL to TiDB.

See [Downloading the TiDB Enterprise Toolset](#downloading-the-tidb-enterprise-toolset) to download the `syncer` tool.

### Downloading the TiDB Enterprise Toolset (Linux)

```bash
# Download the enterprise tool package.
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256

# Extract the package.
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```

Assuming the data from `t1` and `t2` is already imported to TiDB using `mydumper`/`loader`. Now we hope that any updates to these two tables are synchronised to TiDB in real time.

### 1. Obtaining the position to synchronise

The data exported from MySQL contains a metadata file which includes the position information. Take the following metadata information as an example:
```
Started dump at: 2017-04-28 10:48:10
SHOW MASTER STATUS:
	Log: mysql-bin.000003
	Pos: 930143241
	GTID:

Finished dump at: 2017-04-28 10:48:11

```
The position information (`Pos: 930143241`) needs to be stored in the `syncer.meta` file for `syncer` to synchronize:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 930143241
```
**Note:** The `syncer.meta` file only needs to be configured once when it is first used. The position will be automatically updated when binlog is synchronised. 

### 2. Start `syncer`

The `config.toml` file for `syncer`:

```toml
log-level = "info"

server-id = 101

# The file path for meta:
meta = "./syncer.meta"
worker-count = 16
batch = 10

# The testing address for pprof. It can also be used by Prometheus to pull the syncer metrics.
status-addr = ":10081"

skip-sqls = ["ALTER USER", "CREATE USER"]

# Support whitelist filter. You can specify the database and table to be synchronised. For example:
# Synchronise all the tables of db1 and db2:
replicate-do-db = ["db1","db2"]

# Synchronise db1.table1.
[[replicate-do-table]]
db-name ="db1"
tbl-name = "table1"

# Synchronise db3.table2.
[[replicate-do-table]]
db-name ="db3"
tbl-name = "table2"

# Support regular expressions. Start with '~'  to use regular expressions.
# To synchronise all the databases that start with `test`:
replicate-do-db = ["~^test.*"]

# The sharding synchronising rules support wildcharacter.
# 1. The asterisk character (*, also called "star") matches zero or more characters,
#    for example, "doc*" matches "doc" and "document" but not "dodo";
#    asterisk character must be in the end of the wildcard word,
#    and there is only one asterisk in one wildcard word.
# 2. The question mark ? matches exactly one character.
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

### 3. Inserting data into MySQL

```bash
INSERT INTO t1 VALUES (4, 4), (5, 5);
```

### 4. Logging in TiDB and viewing the data:

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

`syncer` outputs the current synchronised data statistics every 30 seconds:

```bash
2017/06/08 01:18:51 syncer.go:934: [info] [syncer]total events = 15, total tps = 130, recent tps = 4,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-17
2017/06/08 01:19:21 syncer.go:934: [info] [syncer]total events = 15, total tps = 191, recent tps = 2,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-35
```

You can see that by using `syncer`, the updates in MySQL are automatically synchronised in TiDB.
