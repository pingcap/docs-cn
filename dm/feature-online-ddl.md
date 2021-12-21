---
title: 迁移使用 GH-ost/PT-osc 的源数据库
aliases: ['/docs-cn/tidb-data-migration/dev/feature-online-ddl-scheme/','/zh/tidb-data-migration/stable/feature-online-ddl-scheme']
---

# 迁移使用 GH-ost/PT-osc 的源数据库

本文档介绍在使用 DM 进行从 MySQL 到 TiDB 的数据迁移时，如何配置 `online-ddl`，以及 DM 与 online DDL 工具的协作细节。

## 概述

DDL 是数据库应用中必然会使用的一类 SQL。MySQL 虽然在 5.6 的版本以后支持了 online-ddl 功能，但是也有或多或少的限制。比如 MDL 锁的获取，某些 DDL 还是需要以 Copy 的方式来进行，在生产业务使用中，DDL 执行过程中的锁表会一定程度上阻塞数据库的读取或者写入。

因此，用户往往会选择 online DDL 工具执行 DDL，把对读写的影响降到最低。常见的 Online DDL 工具有 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)。

这些工具的工作原理可以概括为

1. 根据 DDL 目标表 (real table) 的表结构新建一张镜像表 (ghost table)；
2. 在镜像表上应用 DDL；
3. 将 DDL 目标表的数据同步到镜像表；
4. 在目标表与镜像表数据一致后，通过 `RENAME` 语句使镜像表替换掉目标表。

![DM online-ddl](/meida/dm/dm-online-ddl-2.png)

在使用 DM 完成 MySQL 到 TiDB 的数据迁移时，online-ddl 功能可以识别上述步骤 2 产生的 DDL，并在步骤 4 时向下游应用 DDL，从而降低镜像表的同步开销。

> **注意：**
> 
> 如果希望从源码方面了解 DM online-ddl，可以参考 [DM 源码阅读系列文章（八）Online Schema Change 迁移支持](https://pingcap.com/blog-cn/dm-source-code-reading-8/#dm-源码阅读系列文章八online-schema-change-迁移支持)，以及 [TiDB Online Schema Change 原理](https://pingcap.com/zh/blog/tidb-source-code-reading-17)。

## `online-ddl` 配置

一般情况下建议开启 DM 的 `online-ddl` 配置，将产生以下效果：

![DM online-ddl](/meida/dm/dm-online-ddl.png)

- 下游 TiDB 无需创建和同步镜像表，节约相应存储空间和网络传输等开销；
- 在分库分表合并场景下，忽略各分表镜像表的 RENAME 操作，保证同步正确性；
- 受目前 DM 实现限制，在向下游应用 DDL 时，该同步任务的其他 DML 会被阻塞直到 DDL 完成。我们会在后续优化该限制。

> **注意：**
>
> 如果需要关闭 `online-ddl` 配置，需注意以下影响：
> 
> - 下游 TiDB 将原样同步 gh-ost/pt-osc 等 online DDL 工具的行为；
> - 你需要手动将 online DDL 工具产生的各种临时表、镜像表等添加到任务配置白名单中；
> - 此场景下，无法与分库分表合并场景兼容使用。

## 配置

online-ddl 在 task 配置文件里面与 name 同级，例子详见下面配置 Example。完整的配置及意义，可以参考 [DM 完整配置文件示例](/dm/task-configuration-file-full.md#完整配置文件示例)：

```yml
# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test                      # 任务名称，需要全局唯一
task-mode: all                  # 任务模式，可设为 "full"、"incremental"、"all"
shard-mode: "pessimistic"       # 默认值为 "" 即无需协调。如果为分库分表合并任务，请设置为悲观协调模式 "pessimistic"。在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
online-ddl: true                # 支持上游使用 gh-ost 、pt 两种工具的自动处理
online-ddl-scheme: "gh-ost"     # `online-ddl-scheme` 在未来将被弃用，建议使用 `online-ddl`

target-database:                # 下游数据库实例配置
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""                  # 如果密码不为空，则推荐使用经过 dmctl 加密的密文
```

在分库分表合并场景，迁移过程中需要协调各个分表的 DDL 语句，以及该 DDL 语句前后的 DML 语句。DM 支持悲观协调模式（pessimistic）和乐观协调模式（optimistic），关于二者的区别和适用场景可参考[分库分表合并迁移](/dm/feature-shard-merge.md)。

## DM 与 online DDL 工具协作细节

本小节介绍 DM 与 online DDL工具 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html) 在实现 online-schema-change 过程中的协作细节。

### online-schema-change: gh-ost

gh-ost 在实现 online-schema-change 的过程会产生 3 种 table：

- `gho`：用于应用 DDL，待 `gho` 表中数据迁移到与 origin table 一致后，通过 rename 的方式替换 origin table。
- `ghc`：用于存放 online-schema-change 相关的信息。
- `del`：对 origin table 执行 rename 操作而生成。

DM 在迁移过程中会把上述 table 分成 3 类：

- ghostTable : `\_\*\_gho`
- trashTable : `\_\*\_ghc`、`\_\*\_del`
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

    DM：不执行 `_test4_gho` 的创建操作，根据 ghost_schema、ghost_table 以及 dm_worker 的 `server_id`，删除下游 `dm_meta.{task_name}\_onlineddl` 的记录，清理内存中的相关信息。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

3. 在 `_gho` 表应用需要执行的 DDL：

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DM：不执行 `_test4_gho` 的 DDL 操作，而是把该 DDL 记录到 `dm_meta.{task_name}\_onlineddl` 以及内存中。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4. 往 `_ghc` 表写入数据，以及往 `_gho` 表同步 origin table 的数据：

    ```sql
    Insert /* gh-ost */ into `test`.`_test4_ghc` values (......);

    Insert /* gh-ost `test`.`test4` */ ignore into `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (select `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` from `test`.`test4` force index (`PRIMARY`)
        where (((`id` > _binary'1') or ((`id` = _binary'1'))) and ((`id` < _binary'2') or ((`id` = _binary'2')))) lock in share mode
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
- 3 种 **trigger**：`pt_osc\_\*\_ins`、`pt_osc\_\*\_upd`、`pt_osc\_\*\_del`，用于在 pt_osc 过程中，同步 origin table 新产生的数据到 `new`。

DM 在迁移过程中会把上述 table 分成 3 类：

- ghostTable : `\_\*\_new`
- trashTable : `\_\*\_old`
- realTable : 执行的 online-ddl 的 origin table

pt-osc 主要涉及的 SQL 以及 DM 的处理：

1. 创建 `_new` 表：

    ```sql
    CREATE TABLE `test`.`_test4_new` (id int(11) NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL,  ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DM: 不执行 `_test4_new` 的创建操作。根据 ghost_schema、ghost_table 以及 dm_worker 的 `server_id`，删除下游 `dm_meta.{task_name}\_onlineddl` 的记录，清理内存中的相关信息。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2. 在 `_new` 表上执行 DDL：

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DM: 不执行 `_test4_new` 的 DDL 操作，而是把该 DDL 记录到 `dm_meta.{task_name}\_onlineddl` 以及内存中。

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
> 具体 pt-osc 的 SQL 会根据工具执行时所带的参数而变化。本文只列出主要的 SQL ，具体可以参考 [pt-osc 官方文档](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)。
