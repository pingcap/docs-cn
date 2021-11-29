---
title: Use TiDB Lightning to Import Data in Parallel
summary: Learn the concept, user scenarios, usages, and limitations of importing Data in parallel when using TiDB Lightning.
---

# Use TiDB Lightning to Import Data in Parallel

Since v5.3.0, the [Local-backend mode](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-local-backend) of TiDB Lightning supports the parallel import of a single table or multiple tables. By simultaneously running multiple TiDB Lightning instances, you can import data in parallel from different single tables or multiple tables. In this way, TiDB Lightning provides the ability to scale horizontally, which can greatly reduce the time required to import large amounts of data.

In technical implementation, TiDB Lightning records the meta data of each instance and the data of each imported table in the target TiDB, and coordinates the Row ID allocation range of different instances, the record of global Checksum, and the configuration changes and recovery of TiKV and PD.

You can use TiDB Lightning to import data in parallel in the following scenarios:

- Import sharded schemas and sharded tables. In this scenario, multiple tables from multiple upstream database instances are imported into the downstream TiDB database by different TiDB Lightning instances in parallel.
- Import single tables in parallel. In this scenario, single tables stored in a certain directory or cloud storage (such as Amazon S3) are imported into the downstream TiDB cluster by different TiDB Lightning instances in parallel. This is a new feature introduced in TiDB 5.3.0.

> **Note:**
>
> Parallel import only supports the initialized empty tables in TiDB. It does not support migrating data to tables with data written by existing services. Otherwise, data inconsistencies may occur.

The following diagram shows how importing sharded schemas and sharded tables works. In this scenario, you can use multiple TiDB Lightning instances to import MySQL sharded tables to a downstream TiDB cluster.

![Import sharded schemas and sharded tables](/media/parallel-import-shard-tables-en.png)

The following diagram shows how importing single tables works. In this scenario, you can use multiple TiDB Lightning instances to split data from a single table and import it in parallel to a downstream TiDB cluster.

![Import single tables](/media/parallel-import-single-tables-en.png)

## Considerations

No additional configuration is required for parallel import using TiDB Lightning. When TiDB Lightning is started, it registers meta data in the downstream TiDB cluster and automatically detects whether there are other instances migrating data to the target cluster at the same time. If there is, it automatically enters the parallel import mode.

But when migrating data in parallel, you need to take the following into consideration:

- Handle conflicts between primary keys or unique indexes across multiple sharded tables
- Optimize import performance

### Handle conflicts between primary keys or unique indexes

When using [Local-backend mode](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-local-backend) to import in parallel, you need to ensure that there are no primary key or unique index conflicts between data sources, and between the tables in the target TiDB cluster. Ensure that there are no data writes in the target table during import. Otherwise, TiDB Lightning will not be able to guarantee the correctness of the imported data, and the target table will contain inconsistent indexes after the import is completed.

### Optimize import performance

Because TiDB Lightning needs to upload the generated Key-Value data to the TiKV node where each copy of the corresponding Region is located, the import speed is limited by the size of the target cluster. It is recommended to ensure that the number of TiKV instances in the target TiDB cluster and the number of TiDB Lightning instances are greater than n:1 (n is the number of copies of the Region). At the same time, you need to meet the following requirements to achieve the optimal import performance:

- The total size of source files for each TiDB Lightning instances performing parallel import should be smaller than 5 TiB
- The total number of TiDB Ligntning instances should be smaller than 10

When using TiDB Lightning to import shared databases and tables in parallel, choose an appropriate number of TiDB Lightning instances according to the amount of data.

- If the MySQL data volume is less than 2 TiB, you can use one TiDB Lightning instance for parallel import.
- If the MySQL data volume exceeds 2 TiB and the total number of MySQL instance is smaller than 10, it is recommended that you use one TiDB Lightning instance for each MySQL instance, and the number of parallel TiDB Lightning instances should not exceed 10.
- If the MySQL data volume exceeds 2 TiB and the total number of MySQL instance exceeds 10, it is recommended that you allocate 5 to 10 TiDB Lightning instances for importing the data exported by these MySQL instances.

Next, this document uses two examples to detail the operation steps of parallel import in different scenarios:

- Example 1: Use Dumpling + TiDB Lightning to import sharded databases and tables into TiDB in parallel
- Example 2: Import single tables in parallel

## Example 1: Use Dumpling + TiDB Lightning to Import Sharded Databases and Tables into TiDB in Parallel

In this example, assume that the upstream is a MySQL cluster with 10 sharded tables, with a total size of 10 TiB. You can Use 5 TiDB Lightning instances to perform parallel import, and each instance imports 2 TiB. It is estimated that the total import time (excluding the time required for Dumpling export) can be reduced from about 40 hours to about 10 hours.

Assume that the upstream library is named `my_db`, and the name of each sharded table is `my_table_01` ~ `my_table_10`. You want to merge and import them into the downstream `my_db.my_table` table. The specific steps are described in the following sections.

### Step 1: Use Dumpling to export data

Export two sharded tables on the 5 nodes where TiDB Lightning is deployed:

- If the two sharded tables are in the same MySQL instance, you can use the `-f` parameter of Dumpling to directly export them. When using TiDB Lightning to import, you can specify `data-source-dir` as the directory where Dumpling exports data to;
- If the data of the two sharded tables are distributed on different MySQL nodes, you need to use Dumpling to separately export them. The exported data needs to be placed in the same parent directory <b>but in different sub-directories</b>. When using TiDB Lightning to perform parallel import, you need to specify `data-source-dir` as the parent directory.

For more information on how to use Dumpling to export data, see [Dumpling](/dumpling-overview.md).

### Step 2: Configure TiDB Lightning data sources

Create a configuration file `tidb-lightning.toml`, and then add the following content:

```
[lightning]
status-addr = ":8289"

[mydumper]
# Specify the path for Dumpling to export data. If Dumpling performs several times and the data belongs to different directories, you can place all the exported data in the same parent directory and specify this parent directory here.
data-source-dir = "/path/to/source-dir"

[tikv-importer]
# Use the Local backend mode.
backend = "local"

# Specify the path for local sorting data.
sorted-kv-dir = "/path/to/sorted-dir"

# Specify the routes for shard schemas and tables.
[[routes]]
schema-pattern = "my_db"
table-pattern = "my_table_*"
target-schema = "my_db"
target-table = "my_table"
```

If the data source is stored in a distributed storage cache such as Amazon S3 or GCS, see [External Storages](/br/backup-and-restore-storages.md).

### Step 3: Start TiDB Lightning to import data

During parallel import, the server configuration requirements for each TiDB Lightning node are the same as the non-parallel import mode. Each TiDB Lightning node needs to consume the same resources. It is recommended to deploy them on different servers. For detailed deployment steps, see [Deploy TiDB Lightning](/tidb-lightning/deploy-tidb-lightning.md).

Start TiDB Lightning on each server in turn. If you use `nohup` to directly start it from the command line, it might exit due to the SIGHUP signal. So it is recommended to put `nohup` in the script, for example:

```shell
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

During parallel import, TiDB Lightning automatically performs the following checks after starting the task.

- Check whether there is enough space on the local disk and on the TiKV cluster for importing data. TiDB Lightning samples the data sources and estimates the percentage of the index size from the sample result. Because indexes are included in the estimation, there may be cases where the size of the source data is less than the available space on the local disk, but still the check fails.
- Check whether the regions in the TiKV cluster are distributed evenly and whether there are too many empty regions. If the number of empty regions exceeds max(1000, number of tables * 3), i.e. greater than the bigger one of "1000" or "3 times the number of tables ", then the import cannot be executed.
- Check whether the data is imported in order from the data sources. The size of `mydumper.batch-size` is automatically adjusted based on the result of the check. Therefore, the `mydumper.batch-size` configuration is no longer available.

You can also turn off the check and perform a forced import with the `lightning.check-requirements` configuration. For more detailed checks, see [TiDB Lightning prechecks](/tidb-lightning/tidb-lightning-prechecks.md)

### Step 4: Check the import progress

After starting the import, you can check the progress in either of the following ways:

- Check the progress through the `grep` log keyword `progress`. It is updated every 5 minutes by default.
- Check the progress through the monitoring console. For details, see [TiDB Lightning Monitoring](/tidb-lightning/monitor-tidb-lightning.md).

Wait for all TiDB Lightning instances to finish, then the entire import is completed.

## Example 2: Import single tables in parallel

TiDB Lightning also supports parallel import of single tables. For example, import multiple single tables stored in Amazon S3 by different TiDB Lightning instances into the downstream TiDB cluster in parallel. This method can speed up the overall import speed. For more information on external storages, see [External Storages](/br/backup-and-restore-storages.md)).

> **Note:**
>
>In the local environment, you can use the --where parameter of Dumpling to divide the data of a single table into different parts and export it to the local disks of multiple servers in advance. This way, you can still perform parallel import. The configuration is the same as Example 1.

Assuming that the source files are stored in Amazon S3, the table files are `my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql`, a total of 10,000 SQL files. If you want to use 2 TiDB Lightning instances to speed up the import, you need to add the following settings in the configuration file:

```
[[mydumper.files]]
# the db schema file
pattern = '(?i)^(?:[^/]*/)*my_db-schema-create\.sql'
schema = "my_db"
type = "schema-schema"

[[mydumper.files]]
# the table schema file
pattern = '(?i)^(?:[^/]*/)*my_db\.my_table-schema\.sql'
schema = "my_db"
table = "my_table"
type = "table-schema"

[[mydumper.files]]
# Only import 00001~05000 and ignore other files
pattern = '(?i)^(?:[^/]*/)*my_db\.my_table\.(0[0-4][0-9][0-9][0-9]|05000)\.sql'
schema = "my_db"
table = "my_table"
type = "sql"
```

You can modify the configuration of the other instance to only import the `05001 ~ 10000` data files.

For other steps, see the relevant steps in Example 1.
