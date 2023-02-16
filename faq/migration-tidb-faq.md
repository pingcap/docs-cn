---
title: Migration FAQs
summary: Learn about the FAQs related to data migration.
---

# Migration FAQs

This document summarizes the frequently asked questions (FAQs) related to TiDB data migration.

For the frequently asked questions about migration-related tools, click the corresponding links in the list below:

- [Backup & Restore FAQs](/faq/backup-and-restore-faq.md)
- [TiDB Binlog FAQ](/tidb-binlog/tidb-binlog-faq.md)
- [TiDB Lightning FAQs](/tidb-lightning/tidb-lightning-faq.md)
- [TiDB Data Migration (DM) FAQs](/dm/dm-faq.md)
- [TiCDC FAQs](/ticdc/ticdc-faq.md)

## Full data export and import

### How to migrate an application running on MySQL to TiDB?

Because TiDB supports most MySQL syntax, generally you can migrate your applications to TiDB without changing a single line of code in most cases.

### Data import and export is slow, and many retries and EOF errors appear in the log of each component without other errors

If no other logical errors occur, retries and EOF errors might be caused by network issues. It is recommended to first use tools to check the network connectivity. In the following example, [iperf](https://iperf.fr/) is used for troubleshooting:

+ Execute the following command on the server-side node where the retries and EOF errors occur:

    {{< copyable "shell-regular" >}}

    ```shell
    iperf3 -s
    ```

+ Execute the following command on the client-side node where the retries and EOF errors occur:

    {{< copyable "shell-regular" >}}

    ```shell
    iperf3 -c <server-IP>
    ```

The following example is the output of a client node with a good network connection:

```shell
$ iperf3 -c 192.168.196.58
Connecting to host 192.168.196.58, port 5201
[  5] local 192.168.196.150 port 55397 connected to 192.168.196.58 port 5201
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  18.0 MBytes   150 Mbits/sec
[  5]   1.00-2.00   sec  20.8 MBytes   175 Mbits/sec
[  5]   2.00-3.00   sec  18.2 MBytes   153 Mbits/sec
[  5]   3.00-4.00   sec  22.5 MBytes   188 Mbits/sec
[  5]   4.00-5.00   sec  22.4 MBytes   188 Mbits/sec
[  5]   5.00-6.00   sec  22.8 MBytes   191 Mbits/sec
[  5]   6.00-7.00   sec  20.8 MBytes   174 Mbits/sec
[  5]   7.00-8.00   sec  20.1 MBytes   168 Mbits/sec
[  5]   8.00-9.00   sec  20.8 MBytes   175 Mbits/sec
[  5]   9.00-10.00  sec  21.8 MBytes   183 Mbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-10.00  sec   208 MBytes   175 Mbits/sec                  sender
[  5]   0.00-10.00  sec   208 MBytes   174 Mbits/sec                  receiver

iperf Done.
```

If the output shows low network bandwidth and high bandwidth fluctuations, a large number of retries and EOF errors might appear in each component log. In this case, you need to consult your network service provider to improve the network quality.

If the output of each metric looks good, try to update each component. If the problem persists after the updating, [get support](/support.md) from PingCAP or the community.

### If I accidentally import the MySQL user table into TiDB, or forget the password and cannot log in, how to deal with it?

Restart the TiDB service, add the `-skip-grant-table=true` parameter in the configuration file. Log into the cluster without password and recreate the user, or recreate the `mysql.user` table. For the specific table schema, search the official documentation.

### How to export the data in TiDB?

You can use the following methods to export the data in TiDB:

- Export data using mysqldump and the `WHERE` clause.
- Use the MySQL client to export the results of `select` to a file.

### How to migrate from DB2 or Oracle to TiDB?

To migrate all the data or migrate incrementally from DB2 or Oracle to TiDB, see the following solution:

- Use the official migration tool of Oracle, such as OGG, Gateway, CDC (Change Data Capture).
- Develop a program for importing and exporting data.
- Export Spool as text file, and import data using Load infile.
- Use a third-party data migration tool.

Currently, it is recommended to use OGG.

### Error: `java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation` while using Sqoop to write data into TiDB in `batches`

In Sqoop, `--batch` means committing 100 `statement`s in each batch, but by default each `statement` contains 100 SQL statements. So, 100 * 100 = 10000 SQL statements, which exceeds 5000, the maximum number of statements allowed in a single TiDB transaction.

Two solutions:

- Add the `-Dsqoop.export.records.per.statement=10` option as follows:

    {{< copyable "shell-regular" >}}

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

- You can also increase the limited number of statements in a single TiDB transaction, but this will consume more memory.

### Why does Dumpling return `The local disk space is insufficient` error or cause the upstream database to run out of memory when exporting a table?

This issue might have the following causes:

+ The database's primary keys are not evenly distributed (for example, when you enable [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)).
+ The upstream database is TiDB and the exported table is a partitioned table.

For the above cases, Dumpling splits excessively large data chunk for the export and sends queries with excessively large results. To address the issue, you can get the latest version of Dumpling.

### Does TiDB have a function like the Flashback Query in Oracle? Does it support DDL?

 Yes, it does. And it supports DDL as well. For details, see [how TiDB reads data from history versions](/read-historical-data.md).

## Migrate the data online

### Is there a current solution to replicating data from TiDB to other databases like HBase and Elasticsearch?

No. Currently, the data replication depends on the application itself.

## Migrate the traffic

### How to migrate the traffic quickly?

It is recommended to migrate application data from MySQL to TiDB using [TiDB Data Migration](/dm/dm-overview.md) tool. You can migrate the read and write traffic in batches by editing the network configuration as needed. Deploy a stable network LB (such as HAproxy, LVS, F5, and DNS) on the upper layer, in order to implement seamless migration by directly editing the network configuration.

### Is there a limit for the total write and read capacity in TiDB?

The total read capacity has no limit. You can increase the read capacity by adding more TiDB servers. Generally the write capacity has no limit as well. You can increase the write capacity by adding more TiKV nodes.

### The error message `transaction too large` is displayed

Due to the limitation of the underlying storage engine, each key-value entry (one row) in TiDB should be no more than 6MB. You can adjust the [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration value up to 120MB.

Distributed transactions need two-phase commit and the bottom layer performs the Raft replication. If a transaction is very large, the commit process would be quite slow and the write conflict is more likely to occur. Moreover, the rollback of a failed transaction leads to an unnecessary performance penalty. To avoid these problems, we limit the total size of key-value entries to no more than 100MB in a transaction by default. If you need larger transactions, modify the value of `txn-total-size-limit` in the TiDB configuration file. The maximum value of this configuration item is up to 10G. The actual limitation is also affected by the physical memory of the machine.

There are [similar limits](https://cloud.google.com/spanner/docs/limits) on Google Cloud Spanner.

### How to import data in batches?

When you import data, insert in batches and keep the number of rows within 10,000 for each batch.

### Does TiDB release space immediately after deleting data?

None of the `DELETE`, `TRUNCATE` and `DROP` operations release data immediately. For the `TRUNCATE` and `DROP` operations, after the TiDB GC (Garbage Collection) time (10 minutes by default), the data is deleted and the space is released. For the `DELETE` operation, the data is deleted but the space is not released according to TiDB GC. When subsequent data is written into RocksDB and executes `COMPACT`, the space is reused.

### Can I execute DDL operations on the target table when loading data?

No. None of the DDL operations can be executed on the target table when you load data, otherwise the data fails to be loaded.

### Does TiDB support the `replace into` syntax?

Yes.

### Why does the query speed getting slow after deleting data?

Deleting a large amount of data leaves a lot of useless keys, affecting the query efficiency. Currently the Region Merge feature is in development, which is expected to solve this problem. For details, see the [deleting data section in TiDB Best Practices](https://en.pingcap.com/blog/tidb-best-practice/#write).

### What is the most efficient way of deleting data?

When deleting a large amount of data, it is recommended to use `Delete from t where xx limit 5000;`. It deletes through the loop and uses `Affected Rows == 0` as a condition to end the loop, so as not to exceed the limit of transaction size. With the prerequisite of meeting business filtering logic, it is recommended to add a strong filter index column or directly use the primary key to select the range, such as `id >= 5000*n+m and id < 5000*(n+1)+m`.

If the amount of data that needs to be deleted at a time is very large, this loop method will get slower and slower because each deletion traverses backward. After deleting the previous data, lots of deleted flags remain for a short period (then all will be processed by Garbage Collection) and influence the following Delete statement. If possible, it is recommended to refine the Where condition. See [details in TiDB Best Practices](https://en.pingcap.com/blog/tidb-best-practice/#write).

### How to improve the data loading speed in TiDB?

- The [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) tool is developed for distributed data import. It should be noted that the data import process does not perform a complete transaction process for performance reasons. Therefore, the ACID constraint of the data being imported during the import process cannot be guaranteed. The ACID constraint of the imported data can only be guaranteed after the entire import process ends. Therefore, the applicable scenarios mainly include importing new data (such as a new table or a new index) or the full backup and restoring (truncate the original table and then import data).
- Data loading in TiDB is related to the status of disks and the whole cluster. When loading data, pay attention to metrics like the disk usage rate of the host, TiClient Error, Backoff, Thread CPU and so on. You can analyze the bottlenecks using these metrics.
