---
title: sync-diff-inspector User Guide
summary: Use sync-diff-inspector to compare data and repair inconsistent data.
category: reference
aliases: ['/docs/tools/sync-diff-inspector/']
---

# sync-diff-inspector User Guide

[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector) is a tool used to compare the data that is stored in databases with the MySQL protocol. For example, it can compare the data in MySQL with that in TiDB, the data in MySQL with that in MySQL, or the data in TiDB with that in TiDB. In addition, you can also use this tool to repair data in the scenario where a small amount of data is inconsistent.

This guide introduces the key features of sync-diff-inspector and describes how to configure and use this tool. You can download it at [tidb-enterprise-tools-latest-linux-amd64](https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz).

> **Note:**
>
> - TiDB uses the `utf8_bin` collation. If you need to compare the data in MySQL with that in TiDB, pay attention to the collation configuration of MySQL tables. If the primary key or unique key is the `varchar` type and the collation configuration in MySQL differs from that in TiDB, then the final check result might be incorrect because of the collation issue. You need to add collation to the sync-diff-inspector configuration file.
> - If you configure the `tidb-instance-id` to divide data into chunks according to TiDB statistics, try to guarantee the accuracy of statistics. You can manually run the `analyze table {table_name}` command when the TiDB server *workload is light*.
> - Pay special attention to `table-rules`. If you configure `schema-pattern="test1"` and `target-schema="test2"`, the `test1` schema in the source database and the `test2` schema in the target database are compared. If the source database has a `test2` schema, this `test2` schema is also compared with the `test2` schema in the target database.

## Key features

- Compare the table schema and data
- Generate the SQL statements used to repair data if the data inconsistency exists
- Support comparing the data of multiple tables with the data of a single table (for the scenario of synchronizing data from sharded tables into the combined table)
- Support comparing the data of different schemas or tables with different names

## Description of common configuration

```toml
# Diff configuration

# The log level. You can set it to "info" or "debug".
log-level = "info"

# sync-diff-inspector divides the data into multiple chunks based on the primary key,
# unique key, or the index, and then compares the data of each chunk.
# Use "chunk-size" to set the size of a chunk.
chunk-size = 1000

# The number of goroutines created to check data
check-thread-count = 4

# The proportion of sampling check. If you set it to 100, all the data is checked.
sample-percent = 100

# If enabled, the chunk's checksum is calculated and data is compared by checksum.
# If disabled, data is compared line by line.
use-checksum = true

# If set to true, data check is ignored. If set false, data is checked.
ignore-data-check = false

# If set to true, the table struct comparison is ignored.
# If set to false, the table struct is compared.
ignore-struct-check = false

# The name of the file which saves the SQL statements used to repair data
fix-sql-file = "fix.sql"

# If you need to divide data into chunks according to TiDB statistics, configure tidb-instance-id. The value of tidb-instance-id is the instance-id configured in source-db or target-db.
# tidb-instance-id = "target-1"

# If you need to compare the data of a large number of tables with different schema names or table names, use the table-rule to configure the mapping relationship. You can configure the mapping rule of only schema or only table, or you can also configure the mapping rules of both the schema and table.
#[[table-rules]]
# schema-pattern and table-pattern support regular expressions.
# schema-pattern = "test_*"
# table-pattern = "t_*"
# target-schema = "test"
# target-table = "t"

# Configure the tables of the target databases that need to be checked.
[[check-tables]]
# The name of the schema in the target database
schema = "test"

# The list of tables that need to be checked in the target database
tables = ["test1", "test2", "test3"]

# Supports using regular expressions to configure tables to be checked
# You need to start with '~'. For example, the following configuration checks
# all the tables with the prefix 'test' in the table name.
# tables = ["~^test.*"]
# The following configuration checks all the tables in the database.
# tables = ["~^"]

# Special configuration for some tables
# The configured table must be included in "check-tables'.
[[table-config]]
# The name of the schema in the target database
schema = "test"

# The table name
table = "test3"

# Specifies the column used to divide data into chunks. If you do not configure it,
# sync-diff-inspector chooses an appropriate column (primary key, unique key, or a field with index).
index-field = "id"

# Specifies the range of the data to be checked
# It needs to comply with the syntax of the WHERE clause in SQL.
range = "age > 10 AND age < 20"

# Set it to "true" when comparing the data of multiple sharded tables
# with the data of the combined table.
is-sharding = false

# The collation of the string type of data might be inconsistent in some conditions.
# You can specify "collation" to guarantee the order consistency.
# You need to keep it corresponding to the "charset" setting in the database.
# collation = "latin1_bin"

# Ignores checking some columns. But these columns can still be used to
# divide chunks and sort the checked data.
# ignore-columns = ["name"]

# Removes some columns. During checking, these columns are removed from the table struct.
# These columns are neither checked nor used to divide chunks or sort data.
# remove-columns = ["name"]

# Configuration example of comparing two tables with different database names and table names.
[[table-config]]
# The name of the target schema
schema = "test"

# The name of the target table
table = "test2"

# Set it to "false" in non-sharding scenarios.
is-sharding = false

# Configuration of the source data
[[table-config.source-tables]]
# The instance ID of the source schema
instance-id = "source-1"
# The name of the source schema
schema = "test"
# The name of the source table
table  = "test1"

# Configuration of the instance in the source database
[[source-db]]
host = "127.0.0.1"
port = 3306
user = "root"
password = ""
# The ID of the instance in the source database, the unique identifier of a database instance
instance-id = "source-1"
# Use the snapshot function of TiDB.
# If enabled, the history data is used for comparison.
# snapshot = "2016-10-08 16:45:26"

# Configuration of the instance in the target database
[target-db]
host = "127.0.0.1"
port = 4000
user = "root"
password = ""
# Use the snapshot function of TiDB.
# If enabled, the history data is used for comparison.
# snapshot = "2016-10-08 16:45:26"
```

## Configuration of data comparison in the sharding scenario

Assuming that you have two MySQL instances, use a synchronization tool to synchronize the data into TiDB as shown below:

![shard-table-sync](/media/shard-table-sync.png)

If you need to check the data consistency after synchronization, you can use the following configuration to compare data:

```toml
# Diff Configuration

# Configure the tables in the target databases to be compared.
[[check-tables]]
# The name of the schema
schema = "test"

# The list of tables which need check in the target database
# In the sharding mode, you must set config for each table in "table-config", otherwise the table is not checked.
# The name of the table to be checked
tables = ["test"]

# Configure the sharded tables corresponding to this table.
[[table-config]]
# The name of the target schema
schema = "test"

# The name of the table in the target schema
table = "test"

# Set it to "true" in the sharding scenario.
is-sharding = true

# Configuration of the source tables
[[table-config.source-tables]]
# The ID of the instance in the source database
instance-id = "source-1"
schema = "test"
table  = "test1"

[[table-config.source-tables]]
# The ID of the instance in the source database
instance-id = "source-1"
schema = "test"
table  = "test2"

[[table-config.source-tables]]
# The ID of the instance in the source database
instance-id = "source-2"
schema = "test"
table  = "test3"

# Configuration of the instance in the source database
[[source-db]]
host = "127.0.0.1"
port = 3306
user = "root"
password = ""
instance-id = "source-1"

# Configuration of the instance in the source database
[[source-db]]
host = "127.0.0.2"
port = 3306
user = "root"
password = ""
instance-id = "source-2"

# Configuration of the instance in the source database
[target-db]
host = "127.0.0.3"
port = 4000
user = "root"
password = ""
instance-id = "target-1"
```

## Run sync-diff-inspector

Run the following command:

``` bash
./bin/sync_diff_inspector --config=./config.toml
```

The above command outputs a check report to the log and describes the check result of each table. If data inconsistency exists, the SQL statements used to fix inconsistency are stored to the `fix.sql` file.
