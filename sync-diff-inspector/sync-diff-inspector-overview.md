---
title: sync-diff-inspector User Guide
summary: Use sync-diff-inspector to compare data and repair inconsistent data.
aliases: ['/docs/dev/sync-diff-inspector/sync-diff-inspector-overview/','/docs/dev/reference/tools/sync-diff-inspector/overview/']
---

# sync-diff-inspector User Guide

[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector) is a tool used to compare data stored in the databases with the MySQL protocol. For example, it can compare the data in MySQL with that in TiDB, the data in MySQL with that in MySQL, or the data in TiDB with that in TiDB. In addition, you can also use this tool to repair data in the scenario where a small amount of data is inconsistent.

This guide introduces the key features of sync-diff-inspector and describes how to configure and use this tool. To download sync-diff-inspector, use one of the following methods:

+ Binary package. The sync-diff-inspector binary package is included in the TiDB Toolkit. To download the TiDB Toolkit, see [Download TiDB Tools](/download-ecosystem-tools.md).
+ Docker image. Execute the following command to download:

    {{< copyable "shell-regular" >}}

    ```shell
    docker pull pingcap/tidb-enterprise-tools:nightly
    ```

## Key features

* Compare the table schema and data
* Generate the SQL statements used to repair data if the data inconsistency exists
* Support [data check for tables with different schema or table names](/sync-diff-inspector/route-diff.md)
* Support [data check in the sharding scenario](/sync-diff-inspector/shard-diff.md)
* Support [data check for TiDB upstream-downstream clusters](/sync-diff-inspector/upstream-downstream-diff.md)
* Support [data check in the DM replication scenario](/sync-diff-inspector/dm-diff.md)

## Restrictions of sync-diff-inspector

* Online check is not supported for data migration between MySQL and TiDB. Ensure that no data is written into the upstream-downstream checklist, and that data in a certain range is not changed. You can check data in this range by setting `range`.

* In TiDB and MySQL, `FLOAT`, `DOUBLE` and other floating-point types are implemented differently. `FLOAT` and `DOUBLE` respectively take 6 and 15 significant digits for calculating checksum. If you do not want to use this feature, set `ignore-columns` to skip checking these columns.

* Support checking tables that do not contain the primary key or the unique index. However, if data is inconsistent, the generated SQL statements might not be able to repair the data correctly.

## Database privileges for sync-diff-inspector

sync-diff-inspector needs to obtain the information of table schema and to query data. The required database privileges are as follows:

* Upstream database
    - `SELECT` (checks data for comparison)
    - `SHOW_DATABASES` (views database name)
    - `RELOAD` (views table schema)
* Downstream database
    - `SELECT` (checks data for comparison)
    - `SHOW_DATABASES` (views database name)
    - `RELOAD` (views table schema)

## Configuration file description

The configuration of sync-diff-inspector consists of the following parts:

- `Global config`: General configurations, such as number of threads to check, whether to export SQL statement to fix inconsistent tables, whether to compare the data, and whether to skip checking tables that do not exist in the upstream or downstream.
- `Databases config`: Configures the instances of the upstream and downstream databases.
- `Routes`: Rules for upstream multiple schema names to match downstream single schema names **(optional)**.
- `Task config`: Configures the tables for checking. If some tables have a certain mapping relationship between the upstream and downstream databases or have some special requirements, you must configure these tables.
- `Table config`: Special configurations for specific tables, such as specified ranges and columns to be ignored **(optional)**.

Below is the description of a complete configuration file:

- Note: configurations with `s` after their name can have multiple values, so you need to use square brackets `[]` to contain the configuration values.

``` toml
# Diff Configuration.

######################### Global config #########################
# The number of goroutines created to check data. The number of connections between sync-diff-inspector and upstream/downstream databases is slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

# If enabled, sync-diff-inspector skips checking tables that do not exist in the upstream or downstream.
skip-non-existing-table = false

######################### Datasource config #########################
[data-sources]
[data-sources.mysql1] # mysql1 is the only custom ID for the database instance. It is used for the following `task.source-instances/task.target-instance` configuration.
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""  # The password for connecting to the upstream database. It can be plain text or Base64-encoded.

    # (optional) Use mapping rules to match multiple upstream sharded tables. Rule1 and rule2 are configured in the following Routes section.
    route-rules = ["rule1", "rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""  # The password for connecting to the downstream database. It can be plain text or Base64-encoded.

    # (optional) Use TLS to connect TiDB.
    # security.ca-path = ".../ca.crt"
    # security.cert-path = ".../cert.crt"
    # security.key-path = ".../key.crt"

    # (optional) Use the snapshot feature. If enabled, historical data is used for comparison.
    # snapshot = "386902609362944000"
    # When "snapshot" is set to "auto", the last syncpoints generated by TiCDC in the upstream and downstream are used for comparison. For details, see <https://github.com/pingcap/tidb-tools/issues/663>.
    # snapshot = "auto"

########################### Routes ##############################
# To compare the data of a large number of tables with different schema names or table names, or check the data of multiple upstream sharded tables and downstream table family, use the table-rule to configure the mapping relationship. You can configure the mapping rule only for the schema or table. Also, you can configure the mapping rules for both the schema and the table.
[routes]
[routes.rule1] # rule1 is the only custom ID for the configuration. It is used for the above `data-sources.route-rules` configuration.
schema-pattern = "test_*"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t_*"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"         # The name of the schema in the target database
target-table = "t"             # The name of the target table
[routes.rule2]
schema-pattern = "test2_*"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t2_*"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test2"         # The name of the schema in the target database
target-table = "t2"             # The name of the target table

######################### task config #########################
# Configures the tables of the target database that need to be compared.
[task]
    # output-dir saves the following information:
    # 1 sql: The SQL file to fix tables that is generated after error is detected. One chunk corresponds to one SQL file.
    # 2 log: sync-diff.log
    # 3 summary: summary.txt
    # 4 checkpoint: a dir
    output-dir = "./output"
    # The upstream database. The value is the unique ID declared by data-sources.
    source-instances = ["mysql1"]
    # The downstream database. The value is the unique ID declared by data-sources.
    target-instance = "tidb0"
    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    # Use "?" to match any character and "*" to match characters of any length.
    # For detailed match rules, refer to golang regexp pkg: https://github.com/google/re2/wiki/Syntax.
    target-check-tables = ["schema*.table*", "!c.*", "test2.t2"]
    # (optional) Extra configurations for some tables, Config1 is defined in the following table config example.
    target-configs = ["config1"]

######################### Table config #########################
# Special configurations for specific tables. The tables to be configured must be in `task.target-check-tables`.
[table-configs.config1] # config1  is the only custom ID for this configuration. It is used for the above `task.target-configs` configuration.
# The name of the target table, you can use regular expressions to match multiple tables, but one table is not allowed to be matched by multiple special configurations at the same time.
target-tables = ["schema*.test*", "test2.t2"]
# (optional) Specifies the range of the data to be checked
# It needs to comply with the syntax of the WHERE clause in SQL.
range = "age > 10 AND age < 20"
# (optional) Specifies the column used to divide data into chunks. If you do not configure it,
# sync-diff-inspector chooses an appropriate column (primary key, unique key, or a field with index).
index-fields = ["col1","col2"]
# (optional) Ignores checking some columns such as some types (json, bit, blob, etc.)
# that sync-diff-inspector does not currently support.
# The floating-point data type behaves differently in TiDB and MySQL. You can use
# `ignore-columns` to skip checking these columns.
ignore-columns = ["",""]
# (optional) Specifies the size of the chunk for dividing the table. If not specified, this configuration can be deleted or be set as 0.
chunk-size = 0
# (optional) Specifies the "collation" for the table. If not specified, this configuration can be deleted or be set as an empty string.
collation = ""
```

## Run sync-diff-inspector

Run the following command:

{{< copyable "shell-regular" >}}

```bash
./sync_diff_inspector --config=./config.toml
```

This command outputs a check report `summary.txt` in the `output-dir` of `config.toml` and the log `sync_diff.log`. In the `output-dir`, a folder named by the hash value of the `config. toml` file is also generated. This folder includes the checkpoint node information of breakpoints and the SQL file generated when the data is inconsistent.

### Progress information

sync-diff-inspector sends progress information to `stdout` when running. Progress information includes the comparison results of table structures, comparison results of table data and the progress bar.

> **Note:**
>
> To ensure the display effect, keep the display window width above 80 characters.

```progress
A total of 2 tables need to be compared

Comparing the table structure of ``sbtest`.`sbtest96`` ... equivalent
Comparing the table structure of ``sbtest`.`sbtest99`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest96`` ... failure
Comparing the table data of ``sbtest`.`sbtest99`` ...
_____________________________________________________________________________
Progress [==========================================================>--] 98% 193/200
```

```progress
A total of 2 tables need to be compared

Comparing the table structure of ``sbtest`.`sbtest96`` ... equivalent
Comparing the table structure of ``sbtest`.`sbtest99`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest96`` ... failure
Comparing the table data of ``sbtest`.`sbtest99`` ... failure
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
The data of `sbtest`.`sbtest99` is not equal
The data of `sbtest`.`sbtest96` is not equal

The rest of tables are all equal.

A total of 2 tables have been compared, 0 tables finished, 2 tables failed, 0 tables skipped.
The patch file has been generated in
        'output/fix-on-tidb2/'
You can view the comparison details through 'output/sync_diff.log'
```

### Output file

The directory structure of the output file is as follows:

```
output/
|-- checkpoint # Saves the breakpoint information
| |-- bbfec8cc8d1f58a5800e63aa73e5 # Config hash. The placeholder file which identifies the configuration file corresponding to the output directory (output/)
│ |-- DO_NOT_EDIT_THIS_DIR
│ └-- sync_diff_checkpoints.pb # The breakpoint information
|
|-- fix-on-target # Saves SQL files to fix data inconsistency
| |-- xxx.sql
| |-- xxx.sql
| └-- xxx.sql
|
|-- summary.txt # Saves the summary of the check results
└-- sync_diff.log # Saves the output log information when sync-diff-inspector is running
```

### Log

The log of sync-diff-inspector is saved in `${output}/sync_diff.log`, among which `${output}` is the value of `output-dir` in the `config.toml` file.

### Progress

The running sync-diff-inspector periodically (every 10 seconds) prints the progress in checkpoint, which is located at `${output}/checkpoint/sync_diff_checkpoints.pb`, among which `${output}` is the value of `output-dir` in the `config.toml` file.

### Result

After the check is finished, sync-diff-inspector outputs a report. It is located at `${output}/summary.txt`, and `${output}` is the value of `output-dir` in the `config.toml` file.

```summary
+---------------------+---------+--------------------+----------------+---------+-----------+
|        TABLE        | RESULT  | STRUCTURE EQUALITY | DATA DIFF ROWS | UPCOUNT | DOWNCOUNT |
+---------------------+---------+--------------------+----------------+---------+-----------+
| `sbtest`.`sbtest99` | succeed | true               | +97/-97        |  999999 |    999999 |
| `sbtest`.`sbtest96` | succeed | true               | +0/-101        |  999999 |   1000100 |
| `sbtest`.`sbtest97` | skipped | false              | +999999/-0     |  999999 |         0 |
+---------------------+---------+--------------------+----------------+---------+-----------+
Time Cost: 16.75370462s
Average Speed: 113.277149MB/s
```

- `TABLE`: The corresponding database and table names
- `RESULT`: Whether the check is completed. If you have configured `skip-non-existing-table = true`, the value of this column is `skipped` for tables that do not exist in the upstream or downstream
- `STRUCTURE EQUALITY`: Checks whether the table structure is the same
- `DATA DIFF ROWS`: `rowAdd`/`rowDelete`. Indicates the number of rows that need to be added/deleted to fix the table

### SQL statements to fix inconsistent data

If different rows exist during the data checking process, the SQL statements will be generated to fix them. If the data inconsistency exists in a chunk, a SQL file named by `chunk.Index` will be generated. The SQL file is located at `${output}/fix-on-${instance}`, and `${instance}` is the value of `task.target-instance` in the `config.toml` file.

A SQL file contains the tale to which the chunk belong and the range information. For the SQL files, you should consider the following three situations:

- If the rows in the downstream database are missing, REPLACE statements will be applied
- If the rows in the downstream database are redundant, DELETE statements will be applied
- If some data of the rows in the downstream database is inconsistent, REPLACE statements will be applied and inconsistent columns will be marked with annotation in the SQL file

```sql
-- table: sbtest.sbtest99
-- range in sequence: (3690708) < (id) <= (3720581)
/*
  DIFF COLUMNS ╏   `K`   ╏                `C`                 ╏               `PAD`
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  source data  ╏ 2501808 ╏ 'hello'                            ╏ 'world'
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  target data  ╏ 5003616 ╏ '0709824117-9809973320-4456050422' ╏ '1714066100-7057807621-1425865505'
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
*/
REPLACE INTO `sbtest`.`sbtest99`(`id`,`k`,`c`,`pad`) VALUES (3700000,2501808,'hello','world');
```

## Note

- sync-diff-inspector consumes a certain amount of server resources when checking data. Avoid using sync-diff-inspector to check data during peak business hours.
- Before comparing the data in MySQL with that in TiDB, pay attention to the collation configuration of the tables. If the primary key or unique key is the `varchar` type and the collation configuration in MySQL differs from that in TiDB, the final check result might be incorrect because of the collation issue. You need to add collation to the sync-diff-inspector configuration file.
- sync-diff-inspector divides data into chunks first according to TiDB statistics and you need to guarantee the accuracy of the statistics. You can manually run the `analyze table {table_name}` command when the TiDB server's *workload is light*.
- Pay special attention to `table-rules`. If you configure `schema-pattern="test1"`, `table-pattern = "t_1"`, `target-schema="test2"` and `target-table = "t_2"`, the `test1`.`t_1` schema in the source database and the `test2`.`t_2` schema in the target database are compared. Sharding is enabled by default in sync-diff-inspector, so if the source database has a `test2`.`t_2` table, the `test1`.`t_1` table and `test2`.`t_2` table in the source database serving as sharding are compared with the `test2`.`t_2` table in the target database.
- The generated SQL file is only used as a reference for repairing data, and you need to confirm it before executing these SQL statements to repair data.
