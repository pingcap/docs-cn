---
title: Skip or Replace Abnormal SQL Statements
summary: Learn how to skip or replace abnormal SQL statements when you use Data Migration.
category: reference
aliases: ['/docs/tools/dm/skip-replace-sqls/'] 
---

# Skip or Replace Abnormal SQL Statements

This document introduces how to handle abnormal SQL statements using Data Migration (DM). 

Currently, TiDB is not completely compatible with all MySQL syntax (see [the DDL statements supported by TiDB](/reference/mysql-compatibility.md#ddl)). Therefore, when DM is replicating data from MySQL to TiDB and TiDB does not support the corresponding SQL statement, an error might occur and break the replication process. In this case, there are two ways to resume the replication:

- Use dmctl to manually skip the binlog event to which this SQL statement corresponds

- Use dmctl to manually replace the corresponding binlog event with other specified SQL statements that should be executed to the downstream later

If you know in advance that an unsupported SQL statement is going to be replicated, you can also use dmctl to manually preset the skip or replace operation, which is automatically executed when DM replicates the corresponding binlog event into the downstream and thus avoid breaking the replication.

#### Restrictions

- The skip or replace operation is a one-time operation that is only used to skip or replace the SQL statement unsupported by the downstream TiDB. Do not handle other replication errors with this approach.
    - For other replication errors, try to handle them using [Black and white table lists](/reference/tools/data-migration/features/overview.md#black-and-white-table-lists) or [Binlog event filtering](/reference/tools/data-migration/features/overview.md#binlog-event-filter).

- If it is unacceptable in the actual production environment that the abnormal DDL statement is skipped in the downstream TiDB and it cannot be replaced with other DDL statements, then do not use this approach.
    - For example: `DROP PRIMARY KEY`
    - In this scenario, you can only create a new table in the downstream with the new table schema (after executing the DDL statement), and re-import all the data into this new table. 

- A single skip or replace operation targets at a single binlog event.

- `--sharding` is only used to preset the operation to the sharding group. You must preset it before executing the DDL statement and presetting it after executing the DDL is not allowed.
    - `--sharding` only supports presetting operations, and in this mode, you can only use `--sql-pattern` to match the binlog event.
    - For the principles of replicating sharding DDL statements using DM, see [Merge and replicate data from sharded tables](/reference/tools/data-migration/features/shard-merge.md#principles)

#### Match the binlog event

When the replication task gets interrupted because of the SQL execution error, you can obtain the position of the corresponding binlog event by using `query-error`. When you execute `sql-skip` or `sql-replace`, you can specify the position to match the binlog event.

However, when you try to avoid breaking the replication by actively handling unsupported SQL statements, you cannot know in advance the position of the binlog event, so you need another approach to match the subsequent binlog events.

In DM, two modes of matching the binlog event are supported (you can only choose one mode from below):

1. binlog position: the position information of the binlog event 

    - The binlog position is given by `--binlog-pos` in the command, and the format is `binlog-filename:binlog-pos`, for example, `mysql-bin|000001.000003:3270`.
    - The format of the binlog filename in DM is not completely consistent with that in the upstream MySQL.
    - When the replication error occurs, the position can be directly obtained from `failedBinlogPosition` returned by `query-error`.

2. DDL pattern: the regular expression (only for the DDL statement) matching mode

    - The DDL pattern is given by `--sql-pattern` in the command, for example, to match ``` ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2` ```, the corresponding regular expression should be ``` ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` ```.
    - The regular expression must be prefixed with `~` and cannot contain any common space (you can replace the space with `\s` or `\s+` in the string).

In the scenario of merging and replicating data from sharded tables, if you need DM to automatically select a DDL lock owner to execute the skip or replace operation, then you must use the DDL pattern matching mode because the binlog positions corresponding to the DDL statements on different DM-workers have no logical connection and are hard to confirm.

> **Note:**
>
> - You can only register one operator (specified by `--binlog-pos`) for one binlog event. The previous one can be overwritten by the newly registered operator.
> - Do not specify an operator for one binlog event by using `--binlog-pos` and `--sql-pattern` at the same time.
> - The operator is deleted once it successfully matches the binlog event (not after the execution succeeds). If you need to match again (using `--sql-pattern`) later, you have to register a new operator.

### Supported scenarios

- Scenario 1: during the replication, the DDL statement unsupported by TiDB is executed in the upstream and replicated to the downstream, and as a result, the replication task gets interrupted.

    - If it is acceptable that this DDL statement is skipped in the downstream TiDB, then you can use `sql-skip` to resume the replication.
    - If it is acceptable that this DDL statement is replaced with other DDL statements, then you can use `sql-replace` to resume the replication.

- Scenario 2: during the replication, you know in advance that an unsupported SQL statement is going to be replicated, so you can handle it beforehand to avoid breaking the replication.

    - If it is acceptable that this DDL statement is skipped in the downstream TiDB, then you can use `sql-skip` to preset an operation to automatically skip this DDL statement when it needs to be executed.
    - If it is acceptable that this DDL statement is replaced with other DDL statements, then you can use `sql-replace` to preset an operation to automatically replace this DDL statement when it needs to be executed.

### Implementation principles

In DM, simplified procedures of incremental data replication can be described as follows:

1. The relay unit is used as a slave of the upstream MySQL to fetch the binlog that is persisted in the local storage as the relay log. 

2. The binlog replication unit (sync) reads the local relay log to obtain the binlog event. 

3. The binlog replication unit parses the binlog event and builds the DDL/DML statements, and then replicates these statements to the downstream TiDB.

When the binlog replication unit is parsing the binlog event and replicating data to the downstream, the replication process might get interrupted because the corresponding SQL statement is not supported by TiDB.

In DM, you can register some skip or replace operators for the binlog event. Before replicating the SQL statements to the downstream, DM compares the current binlog event information(position, DDL statement) with registered operators. If the position or the DDL matches with a registered operator, it executes the operation corresponding to the operator and then remove this operator. 

**Use `sql-skip` / `sql-replace` to resume the replication**

1. Use `sql-skip` or `sql-replace` to register an operator for the specified binlog position or DDL pattern.

2. Use `resume-task` to resume the replication task.

3. Regain and re-parse the binlog event that causes the replication error.

4. The binlog event successfully matches with the registered operator in step 1.

5. Execute the skip or replace operation corresponding to the operator and then the replication task continues.

**Use `sql-skip` / `sql-replace` to preset operations to avoid breaking the replication**

1. Use `sql-skip` or `sql-replace` to register an operator for the specified DDL pattern.

2. Parse the relay log to obtain the binlog event.

3. The binlog event (including the SQL statements unsupported by TiDB) successfully matches with the registered operator in step 1.

4. Execute the skip or replace operation corresponding to the operator and then the replication task continues and does not get interrupted.

**Use `sql-skip` / `sql-replace` to preset operations to avoid breaking the replication in the scenario of merging and replicating data from sharded tables**

1. Use `sql-skip` or `sql-replace` to register an operator (on DM-master) for the specified DDL pattern.

2. Each DM-worker parses the relay log to obtain the binlog event.

3. DM-master coordinates the DDL lock replication among DM-workers.

4. DM-master checks if the DDL lock replication succeeds, and sends the registered operator in step 1 to the DDL lock owner.

5. DM-master requests the DDL lock owner to execute the DDL statement.

6. The DDL statement that is to be executed by the DDL lock owner successfully matches with the received operator in step 4.

7. Execute the skip or replace operation corresponding to the operator and then the replication task continues. 

### Command

When you use dmctl to manually handle the SQL statements unsupported by TiDB, the commonly used commands include `query-status`, `query-error`, `sql-skip` and `sql-replace`.

#### query-status

`query-status` allows you to query the current status of items such as the subtask and the relay unit in each DM-worker. For details, see [query status](/reference/tools/data-migration/query-status.md).  

#### query-error

`query-error` allows you to query the existing errors of the running subtask and relay unit in DM-workers.

##### Command usage

```bash
query-error [--worker=127.0.0.1:8262] [task-name]
```

##### Arguments description

+ `worker`:
    - Flag parameter, string, `--worker`, optional
    - If it is not specified, this command queries the errors in all DM-workers; if it is specified, this command queries the error of the specified DM-worker.

+ `task-name`:
    - Non-flag parameter, string, optional
    - If it is not specified, this command queries the errors of all tasks; if it is specified, this command queries the error of the specified task.

##### Example of results

```bash
» query-error test
{
    "result": true,                              # The result of the error query.
    "msg": "",                                   # The additional message for the failure to the error query.
    "workers": [                                 # The information list of DM-workers.
        {
            "result": true,                      # The result of the error query in this DM-worker.
            "worker": "127.0.0.1:8262",          # The IP:port (worker-id) of this DM-worker.
            "msg": "",                           # The additional message for the failure to the error query in this DM-worker.
            "subTaskError": [                    # The error information of the running subtask in this DM-worker.
                {
                    "name": "test",              # The task name.
                    "stage": "Paused",           # The status of the current task.
                    "unit": "Sync",              # The current processing unit of the running task.
                    "sync": {                    # The error information of the binlog replication unit (sync).
                        "errors": [              # The error information list of the current processing unit.
                            {
                                // The error information description.
                                "msg": "exec sqls[[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]] failed, err:Error 1105: unsupported modify column length 10 is less than origin 11",
                                // The position of the failed binlog event.
                                "failedBinlogPosition": "mysql-bin|000001.000003:34642",
                                // The SQL statement that raises an error.
                                "errorSQL": "[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]"
                            }
                        ]
                    }
                }
            ],
            "RelayError": {                      # The error information of the relay processing unit in this DM-worker.
                "msg": ""                        # The error information description.
            }
        }
    ]
}
```

#### sql-skip

`sql-skip` allows you to preset a skip operation that is to be executed when the position or the SQL statement of the binlog event matches with the specified `binlog-pos` or `sql-pattern`. 

##### Command usage

```bash
sql-skip <--worker=127.0.0.1:8262> [--binlog-pos=mysql-bin|000001.000003:3270] [--sql-pattern=~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT] [--sharding] <task-name>
```

##### Arguments description

+ `worker`:
    - Flag parameter, string, `--worker`
    - If `--sharding` is not specified, `worker` is required; if `--sharding` is specified, `worker` is forbidden to use.
    - `worker` specifies the DM-worker in which the presetted operation is going to be executed.

+ `binlog-pos`: 
    - Flag parameter, string, `--binlog-pos`
    - You must specify `binlog-pos` or `--sql-pattern`, and you must not specify both.
    - If it is specified, the skip operation is executed when `binlog-pos` matches with the position of the binlog event. The format is `binlog-filename:binlog-pos`, for example, `mysql-bin|000001.000003:3270`.
    - When the replication error occurs, the position can be obtained from `failedBinlogPosition`  returned by `query-error`.

+ `sql-pattern`: 
    - Flag parameter, string, `--sql-pattern`
    - You must specify `--sql-pattern` or `binlog-pos`, and you must not specify both.
    - If it is specified, the skip operation is executed when `sql-pattern` matches with the DDL statement (converted by the optional router-rule) of the binlog event. The format is a regular expression prefixed with `~`, for example, ``` ~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT ```. 
        - Common spaces are not supported in the regular expression temporarily. You can replace the space with `\s` or `\s+` if it is needed.
        - The regular expression must be prefixed with `~`. For details, see [regular expression syntax](https://golang.org/pkg/regexp/syntax/#hdr-Syntax).
        - The schema/table name in the regular expression must be converted by the optional router-rule, so the converted name is consistent with the target schema/table name in the downstream. For example, if there are ``` `shard_db_1`.`shard_tbl_1` ``` in the upstream and ``` `shard_db`.`shard_tbl` ``` in the downstream, then you should match ``` `shard_db`.`shard_tbl` ```.
        - The schema/table/column name in the regular expression should be marked by ``` ` ```, for example, ``` `db1`.`tbl1` ```.

+ `sharding`: 
    - Flag parameter, boolean, `--sharding`
    - If `--worker` is not specified, `sharding` is required; if `--worker` is specified, `sharding` is forbidden to use.
    - If `sharding` is specified, it indicates that the presetted operation is going to be executed in the DDL lock owner during the sharding DDL replication.

+ `task-name`: 
    - Non-flag parameter, string, required
    - `task-name` specifies the name of the task in which the presetted operation is going to be executed. 

#### sql-replace

`sql-replace` allows you to preset a replace operation that is to be executed when the position or the SQL statement of the binlog event matches with the specified `binlog-pos` or `sql-pattern`.

##### Command usage

```bash
sql-replace <--worker=127.0.0.1:8262> [--binlog-pos=mysql-bin|000001.000003:3270] [--sql-pattern=~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT] [--sharding] <task-name> <SQL-1;SQL-2>
```

##### Arguments description

+ `worker`: 
    - same with `--worker` of `sql-skip`

+ `binlog-pos`: 
    - same with `--binlog-pos` of `sql-skip`

+ `sql-pattern`: 
    - same with `--sql-pattern` of `sql-skip`

+ `sharding`: 
    - same with `--sharding` of `sql-skip`

+ `task-name`: 
    - same with `task-name` of `sql-skip`

+ `SQLs`: 
    - Non-flag parameter, string, required 
    - `SQLs` specifies the new SQL statements that are going to replace the original binlog event. You should separate multiple SQL statements with `;`, for example, ``` ALTER TABLE shard_db.shard_table drop index idx_c2;ALTER TABLE shard_db.shard_table DROP COLUMN c2; ```. 

### Usage examples

#### Passively skip after the replication gets interrupted

##### Application scenario

Assume that you need to replicate the upstream table `db1.tbl1` to the downstream TiDB (not in the scenario of merging and replicating data from sharded tables). The initial table schema is:

```sql
mysql> SHOW CREATE TABLE db1.tbl1;
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

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

Because this DDL statement is not supported by TiDB, the replication task of DM gets interrupted and reports the following error: 

```bash
exec sqls[[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]] failed, 
err:Error 1105: unsupported modify column length 10 is less than origin 11
```

Now, if you query the status of the task using `query-status`, you can see that `stage` has changed into `Paused` and there is some related error description information in `errors`.

To obtain the details about the error, you should use `query-error`. For example, you can execute `query-error test` to get the position of the failed binlog event (`failedBinlogPosition`), which is `mysql-bin|000001.000003:34642`. 

##### Passively skip the SQL statement

Assume that it is acceptable in the actual production environment that this DDL statement is not executed in the downstream TiDB (namely, the original table schema is retained). Then you can use `sql-skip` to skip this DDL statement to resume the replication. The procedures are as follows:

1. Use `query-error` to obtain the position of the failed binlog event.
    - You can get the position from `failedBinlogPosition` returned by `query-error`.
    - In this example, the position is `mysql-bin|000001.000003:34642`.

2. Use `sql-skip` to preset a skip operation that is to be executed when DM replicates this binlog event to the downstream after using `resume-task`.

    ```bash
    » sql-skip --worker=127.0.0.1:8262 --binlog-pos=mysql-bin|000001.000003:34642 test
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "",
                "msg": ""
            }
        ]
    }
    ```

    You can also view the following log in the corresponding DM-worker node: 

    ```bash
    2018/12/28 11:17:51 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: 6bfcf30f-2841-4d70-9a34-28d7082bdbd7, pos: (mysql-bin|000001.000003, 34642), op: SKIP, args:
    on replication unit
    ```

3. Use `resume-task` to resume the replication task

    ```bash
    » resume-task --worker=127.0.0.1:8262 test
    {
        "op": "Resume",
        "result": true,
        "msg": "",
        "workers": [
            {
                "op": "Resume",
                "result": true,
                "worker": "127.0.0.1:8262",
                "msg": ""
            }
        ]
    }
    ```

    You can also view the following log in the corresponding DM-worker node:

    ```bash
    2018/12/28 11:27:46 operator.go:158: [info] [sql-operator] binlog-pos (mysql-bin|000001.000003, 34642) matched, 
    applying operator uuid: 6bfcf30f-2841-4d70-9a34-28d7082bdbd7, pos: (mysql-bin|000001.000003, 34642), op: SKIP, args:
    ```

4. Use `query-status` to guarantee that the `stage` of the task has changed into `Running`.

5. Use `query-error` to guarantee that no DDL execution error exists.

#### Actively replace before the replication gets interrupted 

##### Application scenario

Assume that you need to replicate the upstream table `db2.tbl2` to the downstream TiDB (not in the scenario of merging and replicating data from sharded tables). The initial table schema is:

```sql
mysql> SHOW CREATE TABLE db2.tbl2;
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl2  | CREATE TABLE `tbl2` (
  `c1` int(11) NOT NULL,
  `c2` int(11) DEFAULT NULL,
  PRIMARY KEY (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

Now, the following DDL statement is executed in the upstream to alter the table schema (namely, `DROP COLUMN c2`):

```sql
ALTER TABLE db2.tbl2 DROP COLUMN c2;
```

Because this DDL statement is not supported by TiDB, the replication task of DM gets interrupted and reports the following error: 

```bash
exec sqls[[USE `db2`; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`;]] failed, 
err:Error 1105: can't drop column c2 with index covered now
```

**Assume that you know in advance that this DDL statement is not supported by TiDB before it is executed in the upstream.** Then you can use `sql-skip` or `sql-replace` to preset a skip or replace operation for this DDL statement. 

For this particular DDL statement, because dropping columns with the index is not temporarily supported by TiDB, you can use two new SQL statements to replace the original DDL, namely, DROP the index first and then DROP the column c2.

##### Actively replace the SQL statement

1. Design a matchable regular expression for the DDL statement (converted by the optional router-rule) to be executed in the upstream.
    - The DDL statement to be executed in the upstream is `ALTER TABLE db2.tbl2 DROP COLUMN c2;`. 
    - Because its router-rule conversion does not exist, you can design the following regular expression:

        ```sql
        ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`
        ```

2. Build new DDL statements that are used to replace this original DDL statement.

    ```sql
    ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2;ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    ```

3. Use `sql-replace` to preset a replace operation that is to be executed when DM replicates the corresponding binlog event to the downstream.

    ```bash
    » sql-replace --worker=127.0.0.1:8262 --sql-pattern=~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` test ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2;ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "",
                "msg": ""
            }
        ]
    }
    ```

    You can also view the following log in the corresponding DM-worker node:

    ```bash
    2018/12/28 15:33:13 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: c699a18a-8e75-47eb-8e7e-0e5abde2053c, pattern: ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    on replication unit
    ```

4. Execute the DDL statements in the upstream MySQL.

5. Check if the downstream table schema is altered successfully, and you can view the following log in the corresponding DM-worker node:

    ```bash
    2018/12/28 15:33:45 operator.go:158: [info] [sql-operator] 
    sql-pattern ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `db2`; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`;, 
    applying operator uuid: c699a18a-8e75-47eb-8e7e-0e5abde2053c, 
    pattern: ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    ```

6. Use `query-status` to guarantee that the `stage` of the task has been sustained as `Running`.

7. Use `query-error` to guarantee that no DDL execution error exists.

#### Passively skip after the replication gets interrupted in the scenario of merging and replicating data from sharded tables

##### Application scenario

Assume that you need to merge and replicate multiple tables in multiple upstream MySQL instances to one same table in the downstream TiDB through multiple DM-workers. And the DDL statement unsupported by TiDB is executed to the upstream sharded tables. 

After DM-master coordinates the DDL replication through the DDL lock and requests the DDL lock owner to execute the DDL statement to the downstream, the replication gets interrupted because this DDL statement is not supported by TiDB. 

##### Passively skip the SQL statement

In the scenario of merging and replicating data from sharded tables, passively skipping the unsupported DDL statement has the similar steps with [Passively skip after the replication gets interrupted](#passively-skip-after-the-replication-gets-interrupted).

There are two major differences between the two scenarios as follows. In the scenario of merging and replicating data from sharded tables:  

1. You just need the DDL lock owner to execute `sql-skip` (`--worker={DDL-lock-owner}`). 

2. You just need the DDL lock owner to execute `resume-task` (`--worker={DDL-lock-owner}`).

#### Actively replace before the replication gets interrupted in the scenario of merging and replicating data from sharded tables

##### Application scenario

Assume that you need to merge and replicate the following four tables in the upstream to one same table ``` `shard_db`.`shard_table` ``` in the downstream: 

- In the MySQL instance 1, there is a schema `shard_db_1`, which has two tables `shard_table_1` and `shard_table_2`.
- In the MySQL instance 2, there is a schema `shard_db_2`, which has two tables `shard_table_1` and `shard_table_2`.

The initial table schema is:

```sql
mysql> SHOW CREATE TABLE shard_db_1.shard_table_1;
+---------------+------------------------------------------+
| Table         | Create Table                             |
+---------------+------------------------------------------+
| shard_table_1 | CREATE TABLE `shard_table_1` (
  `c1` int(11) NOT NULL,
  `c2` int(11) DEFAULT NULL,
  PRIMARY KEY (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+---------------+------------------------------------------+
```

Now, the following DDL statement is executed to all upstream sharded tables to alter the table schemas (namely, `DROP COLUMN c2`):

```sql
ALTER TABLE shard_db_*.shard_table_* DROP COLUMN c2;
```

When DM coordinates the two DM-workers to replicate this DDL statement through the sharding DDL lock and requests the DDL lock owner to execute the DDL statement to the downstream, because this DDL statement is not supported by TiDB, the replication task gets interrupted and report the following error: 

```bash
exec sqls[[USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;]] failed,
err:Error 1105: can't drop column c2 with index covered now
```

**Assume that you know in advance that this DDL statement is not supported by TiDB before it is executed in the upstream.** Then you can use `sql-skip` or `sql-replace` to preset a skip or replace operation for this DDL statement. 

For this particular DDL statement, because dropping columns with the index is not temporarily supported by TiDB, you can use two new SQL statements to replace the original DDL, namely, DROP the index first and then DROP the column c2.

##### Actively replace the SQL statement

1. Design a matchable regular expression for the DDL statement (converted by the optional router-rule) to be executed in the upstream.
    - The DDL statement to be executed in the upstream is `ALTER TABLE shard_db_*.shard_table_* DROP COLUMN c2`. 
    - Because the table name should be converted into ``` `shard_db`.`shard_table` ``` by the router-rule, you can design the following regular expression:

        ```sql
        ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`
        ```

2. Build new DDL statements that are used to replace this original DDL statement.

    ```sql
    ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    ```

3. Because this is in the scenario of merging and replicating data from sharded tables, you can use `--sharding` to automatically guarantee that the replace operation is only executed in the DDL lock owner.

4. Use `sql-replace` to preset a replace operation that is to be executed when DM replicates the corresponding binlog event to the downstream.

    ```bash
    » sql-replace --sharding --sql-pattern=~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` test ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
     {
         "result": true,
         "msg": "request with --sharding saved and will be sent to DDL lock's owner when resolving DDL lock",
         "workers": [
         ]
     }
    ```

    You can also view the following log in the **DM-master** node:
    
    ```bash
    2018/12/28 16:53:33 operator.go:105: [info] [sql-operator] set a new operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" 
    op:REPLACE args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true
    ```

5. Execute the DDL statements to the sharded tables in the upstream MySQL instances.

6. Check if the downstream table schema is altered successfully, and you can also view the following log in the DDL lock **owner** node:

    ```bash
    2018/12/28 16:54:35 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: c959f2fb-f1c2-40c7-a1fa-e73cd51736dd, 
    pattern: ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    on replication unit
    ```

    ```bash
    2018/12/28 16:54:35 operator.go:158: [info] [sql-operator] 
    sql-pattern ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;, 
    applying operator uuid: c959f2fb-f1c2-40c7-a1fa-e73cd51736dd, 
    pattern: ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    ```

    In addition, you can view the following log in the **DM-master** node:

    ```bash
    2018/12/28 16:54:35 operator.go:122: [info] [sql-operator] get an operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" op:REPLACE 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true  
    with key ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;
    ```

    ```bash
    2018/12/28 16:54:36 operator.go:145: [info] [sql-operator] remove an operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" op:REPLACE 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true
    ```

7. Use `query-status` to guarantee that the `stage` of the task has been sustained as `Running`, and there is no more DDL statement that is blocking the replication (`blockingDDLs`) and no more sharding group to be resolved (`unresolvedGroups`).

8. Use `query-error` to guarantee that no DDL execution error exists.

9. Use `show-ddl-locks` to guarantee that all DDL locks have been resolved.
