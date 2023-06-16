---
title: Handle Failed DDL Statements in TiDB Data Migration
summary: Learn how to handle failed DDL statements when you're using the TiDB Data Migration tool to migrate data.
aliases: ['/docs/tidb-data-migration/dev/skip-or-replace-abnormal-sql-statements/']
---

# Handle Failed DDL Statements in TiDB Data Migration

This document introduces how to handle failed DDL statements when you're using the TiDB Data Migration (DM) tool to migrate data.

Currently, TiDB is not completely compatible with all MySQL syntax (see [the DDL statements supported by TiDB](/mysql-compatibility.md#ddl-operations)). Therefore, when DM is migrating data from MySQL to TiDB and TiDB does not support the corresponding DDL statement, an error might occur and break the migration process. In this case, you can use the `binlog` command of DM to resume the migration.

## Restrictions

Do not use this command in the following situations:

* It is unacceptable in the actual production environment that the failed DDL statement is skipped in the downstream TiDB.
* The failed DDL statement cannot be replaced with other DDL statements.
* Other DDL statements must not be injected into the downstream TiDB.

For example, `DROP PRIMARY KEY`. In this scenario, you can only create a new table in the downstream with the new table schema (after executing the DDL statement), and re-import all the data into this new table.

## Supported scenarios

During the migration, the DDL statement unsupported by TiDB is executed in the upstream and migrated to the downstream, and as a result, the migration task gets interrupted.

- If it is acceptable that this DDL statement is skipped in the downstream TiDB, then you can use `binlog skip <task-name>` to skip migrating this DDL statement and resume the migration.
- If it is acceptable that this DDL statement is replaced with other DDL statements, then you can use `binlog replace <task-name>` to replace this DDL statement and resume the migration.
- If it is acceptable that other DDL statements are injected to the downstream TiDB, then you can use `binlog inject <task-name>` to inject other DDL statements and resume the migration.

## Commands

When you use dmctl to manually handle the failed DDL statements, the commonly used commands include `query-status` and `binlog`.

### query-status

The `query-status` command is used to query the current status of items such as the subtask and the relay unit in each MySQL instance. For details, see [query status](/dm/dm-query-status.md).

### binlog

The `binlog` command is used to manage and show binlog operations. This command is only supported in DM v6.0 and later versions. For earlier versions, use the `handle-error` command.

The usage of `binlog` is as follows:

```bash
binlog -h
```

```
manage or show binlog operations

Usage:
  dmctl binlog [command]

Available Commands:
  inject      inject the current error event or a specific binlog position (binlog-pos) with some ddls
  list        list error handle command at binlog position (binlog-pos) or after binlog position (binlog-pos)
  replace     replace the current error event or a specific binlog position (binlog-pos) with some ddls
  revert      revert the current binlog operation or a specific binlog position (binlog-pos) operation
  skip        skip the current error event or a specific binlog position (binlog-pos) event

Flags:
  -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
  -h, --help                help for binlog

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl binlog [command] --help" for more information about a command.
```

`binlog` supports the following sub-commands:

* `inject`: injects DDL statements into the current error event or a specific binlog position. To specify the binlog position, refer to `-b, --binlog-pos`.
* `list`: lists all valid `inject`, `skip`, and `replace` operations at the current binlog position or after the current binlog position. To specify the binlog position, refer to `-b, --binlog-pos`.
* `replace`: replaces the DDL statement at a specific binlog position with another DDL statement. To specify the binlog position, refer to `-b, --binlog-pos`.
* `revert`: reverts the `inject`, `skip` or `replace` operation at a specified binlog operation, only if the previous operation does not take effect. To specify the binlog position, refer to `-b, --binlog-pos`.
* `skip`: skips the DDL statement at a specific binlog position. To specify the binlog position, refer to `-b, --binlog-pos`.

`binlog` supports the following flags:

+ `-b, --binlog-pos`:
    - Type: string.
    - Specifies a binlog position. When the position of the binlog event matches `binlog-pos`, the operation is executed. If it is not specified, DM automatically sets `binlog-pos` to the currently failed DDL statement.
    - Format: `binlog-filename:binlog-pos`, for example, `mysql-bin|000001.000003:3270`.
    - After the migration returns an error, the binlog position can be obtained from `position` in `startLocation` returned by `query-status`. Before the migration returns an error, the binlog position can be obtained by using [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html) in the upstream MySQL instance.

+ `-s, --source`:
    - Type: string.
    - Specifies the MySQL instance in which the preset operation is to be executed.

## Usage examples

### Skip DDL if the migration gets interrupted

If you need to skip the DDL statement when the migration gets interrupted, run the `binlog skip` command:

```bash
binlog skip -h
```

```
skip the current error event or a specific binlog position (binlog-pos) event

Usage:
  dmctl binlog skip <task-name> [flags]

Flags:
  -h, --help   help for skip

Global Flags:
  -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
  -s, --source strings      MySQL Source ID.
```

#### Non-shard-merge scenario

Assume that you need to migrate the upstream table `db1.tbl1` to the downstream TiDB. The initial table schema is:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE db1.tbl1;
```

```sql
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl1  | CREATE TABLE `tbl1` (
  `c1` int(11) NOT NULL,
  `c2` decimal(11,3) DEFAULT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

Now, the following DDL statement is executed in the upstream to alter the table schema (namely, alter DECIMAL(11, 3) of c2 into DECIMAL(10, 3)):

{{< copyable "sql" >}}

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

Because this DDL statement is not supported by TiDB, the migration task of DM gets interrupted. Execute the `query-status <task-name>` command, and you can see the following error:

```
ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision
```

Assume that it is acceptable in the actual production environment that this DDL statement is not executed in the downstream TiDB (namely, the original table schema is retained). Then you can use `binlog skip <task-name>` to skip this DDL statement to resume the migration. The procedures are as follows:

1. Execute `binlog skip <task-name>` to skip the currently failed DDL statement:

    {{< copyable "" >}}

    ```bash
    » binlog skip test
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

2. Execute `query-status <task-name>` to view the task status:

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary> See the execution result.</summary>

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-01",
                    "worker": "worker1",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    You can see that the task runs normally and the wrong DDL is skipped.

#### Shard merge scenario

Assume that you need to merge and migrate the following four tables in the upstream to one same table ``` `shard_db`.`shard_table` ``` in the downstream. The task mode is "pessimistic".

- MySQL instance 1 contains the `shard_db_1` schema, which includes the `shard_table_1` and `shard_table_2` tables.
- MySQL instance 2 contains the `shard_db_2` schema, which includes the `shard_table_1` and `shard_table_2` tables.

The initial table schema is:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

Now, execute the following DDL statement to all upstream sharded tables to alter their character set:

{{< copyable "sql" >}}

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` CHARACTER SET LATIN1 COLLATE LATIN1_DANISH_CI;
```

Because this DDL statement is not supported by TiDB, the migration task of DM gets interrupted. Execute the `query-status` command, and you can see the following errors reported by the `shard_db_1`.`shard_table_1` table in MySQL instance 1 and the `shard_db_2`.`shard_table_1` table in MySQL instance 2:

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
    "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
}
```

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
    "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
}
```

Assume that it is acceptable in the actual production environment that this DDL statement is not executed in the downstream TiDB (namely, the original table schema is retained). Then you can use `binlog skip <task-name>` to skip this DDL statement to resume the migration. The procedures are as follows:

1. Execute `binlog skip <task-name>` to skip the currently failed DDL statements in MySQL instance 1 and 2:

    {{< copyable "" >}}

    ```bash
    » binlog skip test
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

2. Execute the `query-status` command, and you can see the errors reported by the `shard_db_1`.`shard_table_2` table in MySQL instance 1 and the `shard_db_2`.`shard_table_2` table in MySQL instance 2:

    ```
    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }
    ```

    ```
    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }
    ```

3. Execute `binlog skip <task-name>` again to skip the currently failed DDL statements in MySQL instance 1 and 2:

    {{< copyable "" >}}

    ```bash
    » handle-error test skip
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

4. Use `query-status <task-name>` to view the task status:

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary> See the execution result.</summary>

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-01",
                    "worker": "worker1",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            },
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-02",
                    "worker": "worker2",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    You can see that the task runs normally with no error and all four wrong DDL statements are skipped.

### Replace DDL if the migration gets interrupted

If you need to replace the DDL statement when the migration gets interrupted, run the `binlog replace` command:

```bash
binlog replace -h
```

```
replace the current error event or a specific binlog position (binlog-pos) with some ddls

Usage:
  dmctl binlog replace <task-name> <replace-sql1> <replace-sql2>... [flags]

Flags:
  -h, --help   help for replace

Global Flags:
  -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
  -s, --source strings      MySQL Source ID.
```

#### Non-shard-merge scenario

Assume that you need to migrate the upstream table `db1.tbl1` to the downstream TiDB. The initial table schema is:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE db1.tbl1;
```

```SQL
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `tbl1` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

Now, perform the following DDL operation in the upstream to add a new column with the UNIQUE constraint:

{{< copyable "sql" >}}

```sql
ALTER TABLE `db1`.`tbl1` ADD COLUMN new_col INT UNIQUE;
```

Because this DDL statement is not supported by TiDB, the migration task gets interrupted. Execute the `query-status` command, and you can see the following error:

```
{
    "Message": "cannot track DDL: ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'db1.tbl1'",
}
```

You can replace this DDL statement with two equivalent DDL statements. The steps are as follows:

1. Replace the wrong DDL statement by the following command:

    {{< copyable "" >}}

    ```bash
    » binlog replace test "ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT;ALTER TABLE `db1`.`tbl1` ADD UNIQUE(`new_col`)";
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

2. Use `query-status <task-name>` to view the task status:

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary> See the execution result.</summary>

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-01",
                    "worker": "worker1",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    You can see that the task runs normally and the wrong DDL statement is replaced by new DDL statements that execute successfully.

#### Shard merge scenario

Assume that you need to merge and migrate the following four tables in the upstream to one same table ``` `shard_db`.`shard_table` ``` in the downstream. The task mode is "pessimistic".

- In the MySQL instance 1, there is a schema `shard_db_1`, which has two tables `shard_table_1` and `shard_table_2`.
- In the MySQL instance 2, there is a schema `shard_db_2`, which has two tables `shard_table_1` and `shard_table_2`.

The initial table schema is:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

Now, perform the following DDL operation to all upstream sharded tables to add a new column with the UNIQUE constraint:

{{< copyable "sql" >}}

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` ADD COLUMN new_col INT UNIQUE;
```

Because this DDL statement is not supported by TiDB, the migration task gets interrupted. Execute the `query-status` command, and you can see the following errors reported by the `shard_db_1`.`shard_table_1` table in MySQL instance 1 and the `shard_db_2`.`shard_table_1` table in MySQL instance 2:

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_1.shard_table_1'",
}
```

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_2.shard_table_1'",
}
```

You can replace this DDL statement with two equivalent DDL statements. The steps are as follows:

1. Replace the wrong DDL statements respectively in MySQL instance 1 and MySQL instance 2 by the following commands:

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_1` ADD UNIQUE(`new_col`)";
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_1` ADD UNIQUE(`new_col`)";
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

2. Use `query-status <task-name>` to view the task status, and you can see the following errors reported by the `shard_db_1`.`shard_table_2` table in MySQL instance 1 and the `shard_db_2`.`shard_table_2` table in MySQL instance 2:

    ```
    {
        "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_1`.`shard_table_2`], right DDL sequence should be ..."
    }
    ```

    ```
    {
        "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_2`.`shard_table_2`], right DDL sequence should be ..."
    }
    ```

3. Execute `handle-error <task-name> replace` again to replace the wrong DDL statements in MySQL instance 1 and 2:

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_2` ADD UNIQUE(`new_col`)";
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_2` ADD UNIQUE(`new_col`)";
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

4. Use `query-status <task-name>` to view the task status:

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary> See the execution result.</summary>

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-01",
                    "worker": "worker1",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            },
            {
                "result": true,
                "msg": "",
                "sourceStatus": {
                    "source": "mysql-replica-02",
                    "worker": "worker2",
                    "result": null,
                    "relayStatus": null
                },
                "subTaskStatus": [
                    {
                        "name": "test",
                        "stage": "Running",
                        "unit": "Sync",
                        "result": null,
                        "unresolvedDDLLockID": "",
                        "sync": {
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": try,
                            "binlogType": "remote",
                            "totalRows": "4",
                            "totalRps": "0",
                            "recentRps": "0"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    You can see that the task runs normally with no error and all four wrong DDL statements are replaced.

### Other commands

For the usage of other commands of `binlog`, refer to the `binlog skip` and `binlog replace` examples above.
