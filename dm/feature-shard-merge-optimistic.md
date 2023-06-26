---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: Learn how DM merges and migrates data from sharded tables in the optimistic mode.
---

# Merge and Migrate Data from Sharded Tables in Optimistic Mode

This document introduces the sharding support feature provided by Data Migration (DM) in the optimistic mode. This feature allows you to merge and migrate the data of tables with the same or different table schema(s) in the upstream MySQL or MariaDB instances into one same table in the downstream TiDB.

> **Note:**
>
> If you do not have an in-depth understanding of the optimistic mode and its restrictions, it is **NOT** recommended to use this mode. Otherwise, migration interruption or even data inconsistency might occur.

## Background

DM supports executing DDL statements on sharded tables online, which is called sharding DDL, and uses the "pessimistic mode" by default. In this mode, when a DDL statement is executed in an upstream sharded table, data migration of this table is paused until the same DDL statement is executed in all other sharded tables. Only by then this DDL statement is executed in the downstream and data migration resumes.

The pessimistic mode guarantees that the data migrated to the downstream is always correct, but it pauses the data migration, which is bad for making A/B changes in the upstream. In some cases, users might spend a long time executing DDL statements in a single sharded table and change the schemas of other sharded tables only after a period of validation. In the pessimistic mode, these DDL statements block data migration and cause many binlog events to pile up.

Therefore, an "optimistic mode" is needed. In this mode, a DDL statement executed on a sharded table is automatically converted to a statement that is compatible with other sharded tables, and then immediately migrated to the downstream. In this way, the DDL statement does not block any sharded table from executing DML migration.

## Configuration of the optimistic mode

To use the optimistic mode, specify the `shard-mode` item in the task configuration file as `optimistic`. You can restrict the behavior of the optimistic mode by enabling the `strict-optimistic-shard-mode` configuration. For the detailed sample configuration file, see [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

## Restrictions

It takes some risks to use the optimistic mode. Follow these rules when you use it:

- Ensure that the schema of every sharded table is consistent with each other before and after you execute a batch of DDL statements.
- If you perform an A/B test, perform the test **ONLY** on one sharded table.
- After the A/B test is finished, migrate only the most direct DDL statement(s) to the final schema. Do not re-execute every right or wrong step of the test.

    For example, if you have executed `ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;` in a sharded table, you only need to execute `ADD COLUMN A FLOAT` in other sharded tables. You do not need to execute all of the three DDL statements again.

- Observe the status of the DM migration when executing the DDL statement. When an error is reported, you need to determine whether this batch of DDL statements will cause data inconsistency.

In the optimistic mode, most of the DDL statements executed in the upstream are automatically migrated to the downstream with no extra effort required. These DDL statements are called "Type 1 DDL".

DDL statements that change the column name, the column type, or the column default value are called "Type 2 DDL". When you execute Type 2 DDL statements in the upstream, make sure that you execute the DDL statements in all sharded tables in the same order.

Some examples of Type 2 DDL statements are as follows:

- Alter the type of a column: `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)`.
- Rename a column: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;`.
- Add a `NOT NULL` column without a default value: `ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;`.
- Rename an index: `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;`.

When the sharded tables execute the DDL statements above, if `strict-optimistic-shard-mode: true` is set, the task is directly interrupted and an error is reported. If `strict-optimistic-shard-mode: false` is set or not specified, different execution order of the DDL statements in sharded tables will cause migration interruption. For example:

- Shard 1 renames a column and then alters the column type:
    1. Rename a column: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;`.
    2. Alter the column type: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);`.
- Shard 2 alters a column type and then renames the column:
    1. Alter a column type: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)`.
    2. Rename a column: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;`.

In addition, the following restrictions apply to both the optimistic mode and the pessimistic mode:

- `DROP TABLE` or `DROP DATABASE` is not supported.
- `TRUNCATE TABLE` is not supported.
- Each DDL statement must involve operations on only one table.
- The DDL statement that is not supported in TiDB is also not supported in DM.
- The default value of a newly added column must not contain `current_timestamp`, `rand()`, `uuid()`; otherwise, data inconsistency between the upstream and the downstream might occur.

## Risks

When you use the optimistic mode for a migration task, a DDL statement is migrated to the downstream immediately. If this mode is misused, data inconsistency between the upstream and the downstream might occur.

### Operations that cause data inconsistency

- The schema of each sharded table is incompatible with each other. For example:
    - Two columns of the same name are added to two sharded tables respectively, but the columns are of different types.
    - Two columns of the same name are added to two sharded tables respectively, but the columns have different default values.
    - Two generated columns of the same name are added to two sharded tables respectively, but the columns are generated using different expressions.
    - Two indexes of the same name are added to two sharded tables respectively, but the keys are different.
    - Other different table schemas with the same name.
- Execute the DDL statement that can corrupt data in the sharded table and then try to roll back.

    For example, drop a column `X` and then add this column back.

### Example

Merge and migrate the following three sharded tables to TiDB:

![optimistic-ddl-fail-example-1](/media/dm/optimistic-ddl-fail-example-1.png)

Add a new column `Age` in `tbl01` and set the default value of the column to `0`:

```sql
ALTER TABLE `tbl01` ADD COLUMN `Age` INT DEFAULT 0;
```

![optimistic-ddl-fail-example-2](/media/dm/optimistic-ddl-fail-example-2.png)

Add a new column `Age` in `tbl00` and set the default value of the column to `-1`:

```sql
ALTER TABLE `tbl00` ADD COLUMN `Age` INT DEFAULT -1;
```

![optimistic-ddl-fail-example-3](/media/dm/optimistic-ddl-fail-example-3.png)

By then, the `Age` column of `tbl00` is inconsistent because `DEFAULT 0` and `DEFAULT -1` are incompatible with each other. In this situation, DM will report the error, but you have to manually fix the data inconsistency.

## Implementation principle

In the optimistic mode, after DM-worker receives the DDL statement from the upstream, it forwards the updated table schema to DM-master. DM-worker tracks the current schema of each sharded table, and DM-master merges these schemas into a composite schema that is compatible with DML statements of every sharded table. Then DM-master migrates the corresponding DDL statement to the downstream. DML statements are directly migrated to the downstream.

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### Examples

Assume the upstream MySQL has three sharded tables (`tbl00`, `tbl01`, and `tbl02`). Merge and migrate these sharded tables to the `tbl` table in the downstream TiDB. See the following image:

![optimistic-ddl-example-1](/media/dm/optimistic-ddl-example-1.png)

Add a `Level` column in the upstream:

```sql
ALTER TABLE `tbl00` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-2](/media/dm/optimistic-ddl-example-2.png)

Then TiDB will receive the DML statement from `tbl00` (with the `Level` column) and the DML statement from the `tbl01` and `tbl02` tables (without the `Level` column).

![optimistic-ddl-example-3](/media/dm/optimistic-ddl-example-3.png)

The following DML statements can be migrated to the downstream without any modification:

```sql
UPDATE `tbl00` SET `Level` = 9 WHERE `ID` = 1;
INSERT INTO `tbl02` (`ID`, `Name`) VALUES (27, 'Tony');
```

![optimistic-ddl-example-4](/media/dm/optimistic-ddl-example-4.png)

Also add a `Level` column in `tbl01`:

```sql
ALTER TABLE `tbl01` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-5](/media/dm/optimistic-ddl-example-5.png)

At this time, the downstream already have had the same `Level` column, so DM-master performs no operation after comparing the table schemas.

Drop a `Name` column in `tbl01`:

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

Then the downstream will receive the DML statements from `tbl00` and `tbl02` with the `Name` column, so this column is not immediately dropped.

In the same way, all DML statements can still be migrated to the downstream:

```sql
INSERT INTO `tbl01` (`ID`, `Level`) VALUES (15, 7);
UPDATE `tbl00` SET `Level` = 5 WHERE `ID` = 5;
```

![optimistic-ddl-example-7](/media/dm/optimistic-ddl-example-7.png)

Add a `Level` column in `tbl02`:

```sql
ALTER TABLE `tbl02` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-8](/media/dm/optimistic-ddl-example-8.png)

By then, all sharded tables have the `Level` column.

Drop the `Name` columns in `tbl00` and `tbl02` respectively:

```sql
ALTER TABLE `tbl00` DROP COLUMN `Name`;
ALTER TABLE `tbl02` DROP COLUMN `Name`;
```

![optimistic-ddl-example-9](/media/dm/optimistic-ddl-example-9.png)

By then, the `Name` columns are dropped from all sharded tables and can be safely dropped in the downstream:

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
