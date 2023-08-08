---
title: 迁移使用 GH-ost/PT-osc 的源数据库
---

# 迁移使用 GH-ost/PT-osc 的源数据库

在生产业务中执行 DDL 时，产生的锁表操作会一定程度阻塞数据库的读取或者写入。为了把对读写的影响降到最低，用户往往会选择 online DDL 工具执行 DDL。常见的 Online DDL 工具有 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)。

在使用 DM 完成 MySQL 到 TiDB 的数据迁移时，可以开启`online-ddl`配置，实现 DM 工具与 gh-ost 或 pt-osc 的协同。关于如何开启 `online-ddl`配置及开启该配置后的工作流程，请参考[上游使用 pt-osc/gh-ost 工具的持续同步场景](/migrate-with-pt-ghost.md)。本文仅介绍 DM 与 online DDL 工具协作的细节。

## DM 与 online DDL 工具协作细节

DM 与 online DDL 工具 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html) 在实现 online-schema-change 过程中的协作细节如下。

### online-schema-change: gh-ost

gh-ost 在实现 online-schema-change 的过程会产生 3 种 table：

- `gho`：用于应用 DDL，待 `gho` 表中数据迁移到与 origin table 一致后，通过 rename 的方式替换 origin table。
- `ghc`：用于存放 online-schema-change 相关的信息。
- `del`：对 origin table 执行 rename 操作而生成。

DM 在迁移过程中会把上述 table 分成 3 类：

- ghostTable : `_*_gho`
- trashTable : `_*_ghc`、`_*_del`
- realTable : 执行 online-ddl 的 origin table

**gh-ost** 涉及的主要 SQL 以及 DM 的处理：

1. 创建 `_ghc` 表：

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

    DM：不执行 `_test4_ghc` 的创建操作。

2. 创建 `_gho` 表：

    ```sql
    Create /* gh-ost */ table `test`.`_test4_gho` like `test`.`test4` ;
    ```

    DM：不执行 `_test4_gho` 的创建操作，根据 ghost_schema、ghost_table 以及 dm_worker 的 `server_id`，删除下游 `dm_meta.{task_name}_onlineddl` 的记录，清理内存中的相关信息。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

3. 在 `_gho` 表应用需要执行的 DDL：

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DM：不执行 `_test4_gho` 的 DDL 操作，而是把该 DDL 记录到 `dm_meta.{task_name}_onlineddl` 以及内存中。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4. 往 `_ghc` 表写入数据，以及往 `_gho` 表同步 origin table 的数据：

    ```sql
    INSERT /* gh-ost */ INTO `test`.`_test4_ghc` VALUES (......);

    INSERT /* gh-ost `test`.`test4` */ ignore INTO `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` FROM `test`.`test4` FORCE INDEX (`PRIMARY`)
        WHERE (((`id` > _binary'1') OR ((`id` = _binary'1'))) AND ((`id` < _binary'2') OR ((`id` = _binary'2')))) lock IN share mode
      )   ;
    ```

    DM：只要不是 **realtable** 的 DML 全部不执行。

5. 数据同步完成后 origin table 与 `_gho` 一起改名，完成 online DDL 操作：

    ```sql
    Rename /* gh-ost */ table `test`.`test4` to `test`.`_test4_del`, `test`.`_test4_gho` to `test`.`test4`;
    ```

    DM 执行以下两个操作:

    - 把 rename 语句拆分成两个 SQL：

        ```sql
        rename test.test4 to test._test4_del;
        rename test._test4_gho to test.test4;
        ```

    - 不执行 `rename to _test4_del`。当要执行 `rename ghost_table to origin table` 的时候，并不执行 rename 语句，而是把步骤 3 记录在内存中的 DDL 读取出来，然后把 ghost_table、ghost_schema 替换为 origin_table 以及对应的 schema，再执行替换后的 DDL。

        ```sql
        alter table test._test4_gho add column cl1 varchar(20) not null;
        --替换为
        alter table test.test4 add column cl1 varchar(20) not null;
        ```

> **注意：**
>
> 具体 gh-ost 的 SQL 会根据工具执行时所带的参数而变化。本文只列出主要的 SQL，具体可以参考 [gh-ost 官方文档](https://github.com/github/gh-ost#gh-ost)。

### online-schema-change: pt

pt-osc 在实现 online-schema-change 的过程会产生 2 种 table：

- `new`：用于应用 DDL，待表中数据同步到与 origin table 一致后，再通过 rename 的方式替换 origin table。
- `old`：对 origin table 执行 rename 操作后生成。
- 3 种 **trigger**：`pt_osc_*_ins`、`pt_osc_*_upd`、`pt_osc_*_del`，用于在 pt_osc 过程中，同步 origin table 新产生的数据到 `new`。

DM 在迁移过程中会把上述 table 分成 3 类：

- ghostTable : `_*_new`
- trashTable : `_*_old`
- realTable : 执行的 online-ddl 的 origin table

pt-osc 主要涉及的 SQL 以及 DM 的处理：

1. 创建 `_new` 表：

    ```sql
    CREATE TABLE `test`.`_test4_new` (id int(11) NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL,  ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DM: 不执行 `_test4_new` 的创建操作。根据 ghost_schema、ghost_table 以及 dm_worker 的 `server_id`，删除下游 `dm_meta.{task_name}_onlineddl` 的记录，清理内存中的相关信息。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2. 在 `_new` 表上执行 DDL：

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DM: 不执行 `_test4_new` 的 DDL 操作，而是把该 DDL 记录到 `dm_meta.{task_name}_onlineddl` 以及内存中。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

3. 创建用于同步数据的 3 个 Trigger：

    ```sql
    CREATE TRIGGER `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DM: 不执行 TiDB 不支持的相关 Trigger 操作。

4. 往 `_new` 表同步 origin table 的数据：

    ```sql
    INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
    ```

    DM: 只要不是 **realTable** 的 DML 全部不执行。

5. 数据同步完成后 origin table 与 `_new` 一起改名，完成 online DDL 操作：

    ```sql
    RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
    ```

    DM 执行以下两个操作:

    - 把 rename 语句拆分成两个 SQL。

        ```sql
        rename test.test4 to test._test4_old;
        rename test._test4_new to test.test4;
        ```

    - 不执行 `rename to _test4_old`。当要执行 `rename ghost_table to origin table` 的时候，并不执行 rename，而是把步骤 2 记录在内存中的 DDL 读取出来，然后把 ghost_table、ghost_schema 替换为 origin_table 以及对应的 schema，再执行替换后的 DDL。

        ```sql
        ALTER TABLE `test`.`_test4_new` add column c3 int;
        --替换为
        ALTER TABLE `test`.`test4` add column c3 int;
        ```

6. 删除 `_old` 表以及 online DDL 的 3 个 Trigger：

    ```sql
    DROP TABLE IF EXISTS `test`.`_test4_old`;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DM: 不执行 `_test4_old` 以及 Trigger 的删除操作。

> **注意：**
>
> 具体 pt-osc 的 SQL 会根据工具执行时所带的参数而变化。本文只列出主要的 SQL，具体可以参考 [pt-osc 官方文档](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)。

## 其他 Online Schema Change 工具

在某些场景下，你可能需要变更 online schema change 工具的默认行为，自定义 `ghost table` 和 `trash table` 的名称；或者期望使用 `gh-ost` 和 `pt-osc` 之外的工具（原理和变更流程仍然保持一致）。此时则需要自行编写正则表达式以匹配`ghost table` 和 `trash table`。

自 v2.0.7 起，DM 实验性支持修改过的 online schema change 工具。在 DM 任务配置中设置 `online-ddl=true` 后，配合 `shadow-table-rules` 和 `trash-table-rules` 即可支持通过正则表达式来匹配修改过的临时表。

假设自定义 pt-osc 的 `ghost table` 规则为 `_{origin_table}_pcnew`，`trash table` 规则为 `_{origin_table}_pcold`，那么自定义规则需配置如下：

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
