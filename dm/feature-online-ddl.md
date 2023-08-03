---
title: Migrate from Databases that Use GH-ost/PT-osc
summary: This document introduces the `online-ddl/online-ddl-scheme` feature of DM.
aliases: ['/docs/tidb-data-migration/dev/online-ddl-scheme/','tidb-data-migration/dev/feature-online-ddl-scheme']
---

# Migrate from Databases that Use GH-ost/PT-osc

In production scenarios, table locking during DDL execution can block the reads from or writes to the database to a certain extent. Therefore, online DDL tools are often used to execute DDLs to minimize the impact on reads and writes. Common DDL tools are [gh-ost](https://github.com/github/gh-ost) and [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html).

When using DM to migrate data from MySQL to TiDB, you can enbale online-ddl to allow collaboration of DM and gh-ost or pt-osc. For details about how to enable online-ddl and the workflow after enabling this option, see [Continuous Replication with gh-ost or pt-osc](/migrate-with-pt-ghost.md). This document focuses on the collaboration details of DM and online DDL tools.

## Working details for DM with online DDL tools

This section describes the working details for DM with the online DDL tools [gh-ost](https://github.com/github/gh-ost) and [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html) when implementing online-schema-change.

### online-schema-change: gh-ost

When gh-ost implements online-schema-change, 3 types of tables are created:

- gho: used to apply DDLs. When the data is fully replicated and the gho table is consistent with the origin table, the origin table is replaced by renaming.
- ghc: used to store information that is related to online-schema-change.
- del: created by renaming the origin table.

In the process of migration, DM divides the above tables into 3 categories:

- ghostTable: `_*_gho`
- trashTable: `_*_ghc`, `_*_del`
- realTable: the origin table that executes online-ddl.

The SQL statements mostly used by gh-ost and the corresponding operation of DM are as follows:

1. Create the `_ghc` table:

    ```sql
    Create /* gh-ost */ table `test`.`_test4_ghc` (
                            id bigint auto_increment,
                            last_update timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            hint varchar(64) charset ascii not null,
                            value varchar(4096) charset ascii not null,
                            primary key(id),
                            unique key hint_uidx(hint)
                    ) auto_increment=256 ;
    ```

    DM does not create the `_test4_ghc` table.

2. Create the `_gho` table:

    ```sql
    Create /* gh-ost */ table `test`.`_test4_gho` like `test`.`test4` ;
    ```

    DM does not create the `_test4_gho` table. DM deletes the `dm_meta.{task_name}_onlineddl` record in the downstream according to `ghost_schema`, `ghost_table`, and the `server_id` of `dm_worker`, and clears the related information in memory.

    ```
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

3. Apply the DDL that needs to be executed in the `_gho` table:

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DM does not perform the DDL operation of `_test4_gho`. It records this DDL in `dm_meta.{task_name}_onlineddl` and memory.

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4. Write data to the `_ghc` table, and replicate the origin table data to the `_gho` table:

    ```sql
    INSERT /* gh-ost */ INTO `test`.`_test4_ghc` VALUES (......);
    INSERT /* gh-ost `test`.`test4` */ ignore INTO `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` FROM `test`.`test4` FORCE INDEX (`PRIMARY`)
        WHERE (((`id` > _binary'1') OR ((`id` = _binary'1'))) AND ((`id` < _binary'2') OR ((`id` = _binary'2')))) lock IN share mode
      )   ;
    ```

    DM does not execute DML statements that are not for **realtable**.

5. After the migration is completed, both the origin table and `_gho` table are renamed, and the online DDL operation is completed:

    ```sql
    Rename /* gh-ost */ table `test`.`test4` to `test`.`_test4_del`, `test`.`_test4_gho` to `test`.`test4`;
    ```

    DM performs the following two operations:

    * DM splits the above `rename` operation into two SQL statements.

        ```sql
        rename test.test4 to test._test4_del;
        rename test._test4_gho to test.test4;
        ```

    * DM does not execute `rename to _test4_del`. When executing `rename ghost_table to origin table`, DM takes the following steps:

        - Read the DDL recorded in memory in Step 3
        - Replace `ghost_table` and `ghost_schema` with `origin_table` and its corresponding schema
        - Execute the DDL that has been replaced

        ```sql
        alter table test._test4_gho add column cl1 varchar(20) not null;
        -- Replaced with:
        alter table test.test4 add column cl1 varchar(20) not null;
        ```

> **Note:**
>
> The specific SQL statements of gh-ost vary with the parameters used in the execution. This document only lists the major SQL statements. For more details, refer to the [gh-ost documentation](https://github.com/github/gh-ost#gh-ost).

## online-schema-change: pt

When pt-osc implements online-schema-change, 2 types of tables are created:

- `new`: used to apply DDL. When the data is fully replicated and the `new` table is consistent with the origin table, the origin table is replaced by renaming.
- `old`: created by renaming the origin table.
- 3 kinds of Trigger: `pt_osc_*_ins`, `pt_osc_*_upd`, `pt_osc_*_del`. In the process of pt_osc, the new data generated by the origin table is replicated to `new` by the Trigger.

In the process of migration, DM divides the above tables into 3 categories:

- ghostTable: `_*_new`
- trashTable: `_*_old`
- realTable: the origin table that executes online-ddl.

The SQL statements mostly used by pt-osc and the corresponding operation of DM are as follows:

1. Create the `_new` table:

    ```sql
    CREATE TABLE `test`.`_test4_new` ( id int(11) NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL, ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DM does not create the `_test4_new` table. DM deletes the `dm_meta.{task_name}_onlineddl` record in the downstream according to `ghost_schema`, `ghost_table`, and the `server_id` of `dm_worker`, and clears the related information in memory.

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2. Execute DDL in the `_new` table:

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DM does not perform the DDL operation of `_test4_new`. Instead, it records this DDL in `dm_meta.{task_name}_onlineddl` and memory.

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

3. Create 3 Triggers used for data migration:

    ```sql
    CREATE TRIGGER `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DM does not execute Trigger operations that are not supported in TiDB.

4. Replicate the origin table data to the `_new` table:

    ```sql
    INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
    ```

    DM does not execute the DML statements that are not for **realtable**.

5. After the data migration is completed, the origin table and `_new` table are renamed, and the online DDL operation is completed:

    ```sql
    RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
    ```

    DM performs the following two operations:

    * DM splits the above `rename` operation into two SQL statements:

        ```sql
        rename test.test4 to test._test4_old;
        rename test._test4_new to test.test4;
        ```

    * DM does not execute `rename to _test4_old`. When executing `rename ghost_table to origin table`, DM takes the following steps:

        - Read the DDL recorded in memory in Step 2
        - Replace `ghost_table` and `ghost_schema` with `origin_table` and its corresponding schema
        - Execute the DDL that has been replaced

        ```sql
        ALTER TABLE `test`.`_test4_new` add column c3 int;
        -- Replaced with:
        ALTER TABLE `test`.`test4` add column c3 int;
        ```

6. Delete the `_old` table and 3 Triggers of the online DDL operation:

    ```sql
    DROP TABLE IF EXISTS `test`.`_test4_old`;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DM does not delete `_test4_old` and Triggers.

> **Note:**
>
> The specific SQL statements of pt-osc vary with the parameters used in the execution. This document only lists the major SQL statements. For more details, refer to the [pt-osc documentation](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html).

## Other online schema change tools

In some cases, you might need to change the default behavior of your online schema change tool. For example, you might use customized names for `ghost table` and `trash table`. In other cases, you might want to use other tools instead of gh-ost or pt-osc, with the same working principles and change processes.

To achieve such customized needs, you need to write regular expressions to match the names of the `ghost table` and `trash table`.

Starting from v2.0.7, DM experimentally supports the modified online schema change tools. By setting `online-ddl=true` in the DM task configuration and configuring `shadow-table-rules` and `trash-table-rules`, you can match the modified temporary tables with regular expressions.

For example, if you use a customized pt-osc with the name of `ghost table` being `_{origin_table}_pcnew` and the name of `trash table` being `_{origin_table}_pcold`, you can set the custom rules as follows:

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
