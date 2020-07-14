---
title: Export or Backup Data Using Dumpling
summary: Use the Dumpling tool to export or backup data in TiDB.
aliases: ['/docs/dev/export-or-backup-using-dumpling/']
---

# Export or Backup Data Using Dumpling

This document introduces how to use the [Dumpling](https://github.com/pingcap/dumpling) tool to export or backup data in TiDB. Dumpling exports data stored in TiDB as SQL or CSV data files and can be used to make a logical full backup or export.

For backups of SST files (KV pairs) or backups of incremental data that are not sensitive to latency, refer to [BR](/br/backup-and-restore-tool.md). For real-time backups of incremental data, refer to [TiCDC](/ticdc/ticdc-overview.md).

When using Dumpling, you need to execute the export command on a running cluster. This document assumes that there is a TiDB instance on the `127.0.0.1:4000` host and that this TiDB instance has a root user without a password.

## Export data from TiDB

Export data using the following command:

{{< copyable "shell-regular" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  --filetype sql \
  --threads 32 \
  -o /tmp/test \
  -F $(( 1024 * 1024 * 256 ))
```

In the above command, `-H`, `-P` and `-u` mean address, port and user, respectively. If password authentication is required, you can pass it to Dumpling with `-p $YOUR_SECRET_PASSWORD`.

Dumpling exports all tables (except for system tables) in the entire database by default. You can use `--where <SQL where expression>` to select the records to be exported. If the exported data is in CSV format (CSV files can be exported using `--filetype csv`), you can also use `--sql <SQL>` to export records selected by the specified SQL statement. 

For example, you can export all records that match `id < 100` in `test.sbtest1` using the following command:

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql "select * from `test`.`sbtest1` where id < 100"
```

Note that the `--sql` option can be used only for exporting CSV files for now. However, you can use `--where` to filter the rows to be exported, and use the following command to export all rows with `id < 100`:

> **Note:**
>
> You need to execute the `select * from <table-name> where id < 100` statement on all tables to be exported. If any table does not have the specified field, then the export fails.

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

> **Note:**
> 
> Currently, Dumpling does not support exporting only certain tables specified by users (i.e. `-T` flag, see [this issue](https://github.com/pingcap/dumpling/issues/76)). If you do need this feature, you can use [MyDumper](/backup-and-restore-using-mydumper-lightning.md) instead.

The exported file is stored in the `./export-<current local time>` directory by default. Commonly used parameters are as follows:

- `-o` is used to select the directory where the exported files are stored.
- `-F` option is used to specify the maximum size of a single file (the unit here is byte, different from MyDumper).
- `-r` option is used to specify the maximum number of records (or the number of rows in the database) for a single file.

You can use the above parameters to provide Dumpling with a higher degree of parallelism.

Another flag that is not mentioned above is `--consistency <consistency level>`, which controls the way in which data is exported for "consistency assurance". For TiDB, consistency is ensured by getting a snapshot of a certain timestamp by default (i.e. `--consistency snapshot`). When using snapshot for consistency, you can use the `--snapshot` parameter to specify the timestamp to be backed up. You can also use the following levels of consistency:

- `flush`: Use [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) to ensure consistency.
- `snapshot`: Get a consistent snapshot of the specified timestamp and export it.
- `lock`: Add read locks on all tables to be exported.
- `none`: No guarantee for consistency.
- `auto`: Use `flush` for MySQL and `snapshot` for TiDB.

After everything is done, you can see the exported file in `/tmp/test`:

{{< copyable "shell-regular" >}}

```shell
ls -lh /tmp/test | awk '{print $5 "\t" $9}'
```

```
140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

In addition, if the data volume is very large, to avoid export failure due to GC during the export process, you can extend the GC time in advance:

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

After your operation is completed, set the GC time back (the default value is `10m`):

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
```

Finally, all the exported data can be imported back to TiDB using [Lightning](/tidb-lightning/tidb-lightning-tidb-backend.md).
