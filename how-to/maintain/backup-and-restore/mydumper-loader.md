---
title: Use `mydumper`and `loader` to Back up and Restore Data
summary: Learn how to back up and restore the data of TiDB using `mydumper` and `loader`.
category: how-to
aliases: ['/docs/dev/how-to/maintain/backup-and-restore/']
---

# Use `mydumper` and `loader` to Back up and Restore Data

This document describes how to back up and restore the data of TiDB using `mydumper` and `loader`. Currently, this document only covers full backup and restoration.

Suppose that the TiDB service information is as follows:

|Name|Address|Port|User|Password|
|:----:|:-------:|:----:|:----:|:------:|
|TiDB|127.0.0.1|4000|root|*|

Use the following tools for data backup and restoration:

- `mydumper`: to export data from TiDB
- `loader`: to import data into TiDB

## Download TiDB toolset (Linux)

1. Download the tool package:

    {{< copyable "shell-regular" >}}

    ```bash
    wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz && \
    wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256
    ```

2. Check the file integrity. If the result is fine, the file is correct.

    {{< copyable "shell-regular" >}}

    ```bash
    sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
    ```

3. Extract the package:

    {{< copyable "shell-regular" >}}

    ```bash
    tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz && \
    cd tidb-enterprise-tools-latest-linux-amd64
    ```

## Full backup and restoration using `mydumper`/`loader`

Use [`mydumper`](/reference/tools/mydumper.md) to export data from TiDB and [`loader`](/reference/tools/loader.md) to import data into TiDB.

> **Note:**
>
> Use `mydumper` from the Enterprise Tools package, and not the `mydumper` provided by your operating system's package manager. The upstream version of `mydumper` does not yet handle TiDB correctly ([#155](https://github.com/maxbube/mydumper/pull/155)). It is also not recommended to use `mysqldump` which is much slower for both backup and restoration.

### Best practices for full backup and restoration using `mydumper`/`loader`

To quickly backup and restore data (especially large amounts of data), refer to the following recommendations:

- Keep the exported data file as small as possible and it is recommended to keep it smaller than 64M. Use the `-F` parameter to set the value.
- Adjust the `-t` parameter of `loader` based on the number and the load of TiKV instances. It is recommended that you set the value of `-t` to `32`. If the load of TiKV is too high and the `backoffer.maxSleep 15000ms is exceeded` log is displayed many times, decrease the value of `-t`; otherwise, increase the value.

### Backup data from TiDB

Use `mydumper` to backup data from TiDB.

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 32 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

In this command,

- `-B test` means that the data is exported from the `test` database.
- `-T t1,t2` means that only the `t1` and `t2` tables are exported.
- `-t 32` means that 32 threads are used to export the data.
- `-F 64` means that a table is partitioned into chunks and one chunk is 64MB.
- `--skip-tz-utc` means to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

If `mydumper` returns the following error:

```
** (mydumper:27528): CRITICAL **: 13:25:09.081: Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

Then execute two more commands:

1. Before executing the `mydumper` command, query the GC values of the TiDB cluster and adjust it to a suitable value using the MySQL client:

    ```sql
    mysql> SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)

    mysql> update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. After finishing running the `mydumper` command, restore the adjusted GC value (`720h`) of the TiDB cluster to its original value (`10m0s`) in step 1.

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### Restore data into TiDB

To restore data into TiDB, use `loader` to import the previously exported data. See [Loader instructions](/reference/tools/loader.md) for more information.

{{< copyable "shell-regular" >}}

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is imported, you can view the data in TiDB using the MySQL client:

{{< copyable "shell-regular" >}}

```shell
mysql -h127.0.0.1 -P4000 -uroot
```

{{< copyable "sql" >}}

```sql
mysql> show tables;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+
```

{{< copyable "sql" >}}

```sql
mysql> select * from t1;
```

```
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+
```

{{< copyable "sql" >}}

```sql
mysql> select * from t2;
```

```
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```
