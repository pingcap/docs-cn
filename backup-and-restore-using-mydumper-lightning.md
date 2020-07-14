---
title: Use Mydumper and TiDB Lightning for Backup and Restoration
aliases: ['/docs/dev/backup-and-restore-using-mydumper-lightning/','/docs/dev/how-to/maintain/backup-and-restore/mydumper-lightning/','/docs/dev/how-to/maintain/backup-and-restore/']
---

# Use Mydumper and TiDB Lightning for Data Backup and Restoration

This document describes how to perform full backup and restoration of the TiDB data using Mydumper and TiDB Lightning. For incremental backup and restoration, refer to [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

Suppose that the TiDB service information is as follows:

|Name|Address|Port|User|Password|
|:----|:-------|:----|:----|:--------|
|TiDB|127.0.0.1|4000|root|*|

Use the following tools for data backup and restoration:

- [Mydumper](/mydumper-overview.md): to export data from TiDB
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md): to import data into TiDB

## Full backup and restoration using Mydumper/TiDB Lightning

`mydumper` is a powerful data backup tool. For more information, refer to [`maxbube/mydumper`](https://github.com/maxbube/mydumper).

Use [Mydumper](/mydumper-overview.md) to export data from TiDB and use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data into TiDB.

> **Note:**
>
> It is recommended to download [Mydumper](/mydumper-overview.md) from the PingCAP website, because the R&D team has adapted `mydumper` for TiDB. It is not recommended to use `mysqldump` which is much slower for both backup and restoration.

### Best practices for full backup and restoration using Mydumper/TiDB Lightning

To quickly backup and restore data (especially large amounts of data), refer to the following recommendations:

* Keep the exported data file as small as possible. It is recommended to use the `-F` parameter to set the file size. If you use TiDB Lightning to restore data, it is recommended that you set the value of `-F` to `256` (MB). If you use `loader` for restoration, it is recommended to set the value to `64` (MB).

## Backup data from TiDB

Use `mydumper` to backup data from TiDB.

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 32 -F 256 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

In this command,

`-B test` means that the data is exported from the `test` database.
`-T t1,t2` means that only the `t1` and `t2` tables are exported.
`-t 32` means that 32 threads are used to export the data.
`-F 256` means that a table is partitioned into chunks, and one chunk is 256MB.
`--skip-tz-utc` means to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

If `mydumper` returns the following error:

```
** (mydumper:27528): CRITICAL **: 13:25:09.081: Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

Then execute two more commands:

1. Before executing the `mydumper` command, query the [GC](/garbage-collection-overview.md) values of the TiDB cluster and adjust it to a suitable value using the MySQL client:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. After running the `mydumper` command, adjust GC value of the TiDB cluster to its original value in step 1.

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## Restore data into TiDB

To restore data into TiDB, use TiDB Lightning to import the exported data. See [TiDB Lightning Tutorial](/tidb-lightning/tidb-lightning-tidb-backend.md).
