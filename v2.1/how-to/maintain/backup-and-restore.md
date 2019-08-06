---
title: Backup and Restore
summary: Learn how to back up and restore the data of TiDB.
category: how-to
---

# Backup and Restore

This document describes how to back up and restore the data of TiDB. Currently, this document only covers full backup and restoration.

Here we assume that the TiDB service information is as follows:

|Name|Address|Port|User|Password|
|:----:|:-------:|:----:|:----:|:------:|
|TiDB|127.0.0.1|4000|root|*|

Use the following tools for data backup and restoration:

- `mydumper`: to export data from TiDB
- `loader`: to import data into TiDB

## Download TiDB toolset (Linux)

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

## Full backup and restoration using `mydumper`/`loader`

You can use [`mydumper`](/reference/tools/mydumper.md) to export data from TiDB and [`loader`](/reference/tools/loader.md) to import the data into TiDB.

> **Important**: You must use the `mydumper` from the Enterprise Tools package, and not the `mydumper` provided by your operating system's package manager. The upstream version of `mydumper` does not yet handle TiDB correctly ([#155](https://github.com/maxbube/mydumper/pull/155)). Using `mysqldump` is also not recommended, as it is much slower for both backup and restoration.

### Best practices of full backup and restoration using `mydumper`/`loader`

To quickly backup and restore data (especially large amounts of data), refer to the following recommendations:

- Keep the exported data file as small as possible and it is recommended keep it within 64M. You can use the `-F` parameter to set the value.
- You can adjust the `-t` parameter of `loader` based on the number and the load of TiKV instances. For example, if there are three TiKV instances, `-t` can be set to around 3 * (1 ~ n). If the load of TiKV is too high and the log `backoffer.maxSleep 15000ms is exceeded` is displayed many times, decrease the value of `-t`; otherwise, increase it.

#### An example of restoring data and related configuration

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
    - Operating System: CentOS 7.3
- The `-F` parameter of `mydumper` is set to 16 and the `-t` parameter of `loader` is set to 64.

**Results**: It takes 11 hours to import all the data, which is 19.4G/hour.

### Backup data from TiDB

Use `mydumper` to backup data from TiDB.

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

In this command,

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 64`: means a table is partitioned into chunks and one chunk is 64MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

If `mydumper` emits error like:

```
** (mydumper:27528): CRITICAL **: 13:25:09.081: Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

Then execute two more commands:

- Step 1: before executing the `mydumper` command, query the GC values of the TiDB cluster and adjust it to a suitable value using the MySQL client.

    ```sql
    mysql> SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time'
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)

    mysql> update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

- Step 2: after you finish running the `mydumper` command, restore the GC value of the TiDB cluster to its original value in step 1.

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### Restore data into TiDB

To restore data into TiDB, use `loader` to import the previously exported data. See [Loader instructions](/reference/tools/loader.md) for more information.

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is imported, you can view the data in TiDB using the MySQL client:

```sql
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
