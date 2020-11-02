---
title: Use Dumpling and TiDB Lightning for Data Backup and Restoration
summary: Introduce how to use Dumpling and TiDB Lightning to backup and restore full data of TiDB.
aliases: ['/docs/dev/export-or-backup-using-dumpling/','/tidb/dev/export-or-backup-using-dumpling']
---

# Use Dumpling and TiDB Lightning for Data Backup and Restoration

This document introduces in detail how to use Dumpling and TiDB Lightning to backup and restore full data of TiDB. For incremental backup and replication to downstream, refer to [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

Suppose that the TiDB server information is as follows:

|Server Name|Server Address|Port|User|Password|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|

Use the following tools for data backup and restoration:

- [Dumpling](/dumpling-overview.md): to export data from TiDB
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md): to import data into TiDB

## Best practices for full backup and restoration using Dumpling/TiDB Lightning

To quickly backup and restore data (especially large amounts of data), refer to the following recommendations:

* Keep the exported data file as small as possible. It is recommended to use the `-F` option of Dumpling to set the file size. If you use TiDB Lightning to restore data, it is recommended that you set the value of `-F` to `256m`.
* If some of the exported tables have many rows, you can enable concurrency in the table by setting the `-r` option.

## Backup data from TiDB

Use the following `dumpling` command to backup data from TiDB.

{{< copyable "shell-regular" >}}

```bash
./bin/dumpling -h 127.0.0.1 -P 4000 -u root -t 32 -F 256m -T test.t1 -T test.t2 -o ./var/test
```

In this command:

- `-T test.t1 -T test.t2` means that only the two tables `test`.`t1` and `test`.`t2` are exported. For more methods to filter exported data, refer to [Filter exported data](/dumpling-overview.md#filter-the-exported-data).
- `-t 32` means that 32 threads are used to export the data.
- `-F 256m` means that a table is partitioned into chunks, and one chunk is 256MB.

Starting from v4.0.0, Dumpling can automatically extends the GC time if it can access the PD address of the TiDB cluster. But for TiDB earlier than v4.0.0, you need to manually modify the GC time. Otherwise, you might bump into the following error:

```log
Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

The steps to manually modify the GC time are as follows:

1. Before executing the `dumpling` command, query the [GC](/garbage-collection-overview.md) value of the TiDB cluster and execute the following statement in the MySQL client to adjust it to a suitable value:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```sql
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. After executing the `dumpling` command, restore the GC value of the TiDB cluster to the initial value in step 1:

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '10m' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## Restore data into TiDB

To restore data into TiDB, use TiDB Lightning to import the exported data. See [TiDB Lightning Tutorial](/tidb-lightning/tidb-lightning-backends.md).
