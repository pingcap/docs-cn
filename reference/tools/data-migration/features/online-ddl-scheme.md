# DM online-ddl-scheme

## 概述

DDL 是数据库应用中必然会使用的一类 SQL 。MySQL 虽然在 5.6 的版本以后支持了 online-ddl 。但是也有或多或少的限制，比如 MDL 锁的获取，某些 ddl 还是需要以 Copy 的方式来进行，在生产业务使用中，DDL执行过程中的锁表会一定程度上阻塞数据库的读取或者写入，因此 gh-ost 以及 pt-osc 可以更优雅地把 DDL 在 MySQL 上面执行，把对读写的影响降到最低。 \
**TiDB** 根据 Google F1 的在线异步 schema 变更算法实现，在 DDL 过程中并不会阻塞读写。因此 gh-ost 以 pt-osc 在 online-schema-change 过程中的产生的大量中间表的数据以及 binlogevent 在 MySQL 与 TiDB 的数据同步过程中并不需要。\
**DM** 作为 MySQL 同步到 TiDB 的工具，online-ddl-scheme 功能就是对上述两个 online-schema-change 的工具进行特殊的处理，以更快地完成所需的 DDL 的同步。\
如想从源码方面了解 DM online-ddl-scheme 可以参考 : [ DM 源码阅读系列文章（八）Online Schema Change 同步支持](https://pingcap.com/blog-cn/dm-source-code-reading-8/#dm-源码阅读系列文章八online-schema-change-同步支持)

## 配置

**online-ddl-scheme** 在 task 配置文件里面与 name 同级，例子详见下面配置 Example (完整的配置及意义可以参考 [DM 完整配置文件示例](https://pingcap.com/docs-cn/stable/reference/tools/data-migration/configure/task-configuration-file-full/#完整配置文件示例))：
```yml
# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test                      # 任务名称，需要全局唯一
task-mode: all                  # 任务模式，可设为 "full"、"incremental"、"all"
is-sharding: true               # 是否为分库分表合并任务
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
remove-meta: false              # 是否在任务同步开始前移除该任务名对应的 `meta`（`checkpoint` 和 `onlineddl` 等）。
enable-heartbeat: false         # 是否开启 `heartbeat` 功能
online-ddl-scheme: "gh-ost"     # 目前仅支持 gh-ost 、pt

target-database:                # 下游数据库实例配置
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""                  # 如果不为空则需经过 dmctl 加密

```

## online-schema-change : gh-ost 

### gh-ost 在实现 online schema change 的过程会产生 3 种 table ： **\_\*\_gho 、\_\*\_ghc 、\_\*\_del** 。

   - **gho** 用于应用 ddl ，待数据同步追上 origin table 之后会通过 rename 的方式替换 origin table 。
   - **ghc** 用于存放 online schema change 相关的信息。
   - **del** 表是由 origin table rename 过来的。
   
### dm 在同步过程中会把上述 table 中会分成 3 类：

   - ghostTable : \_\*\_gho (gh-ost) 
   - trashTable : \_\*\_ghc (gh-ost) 、\_\*\_del (gh-ost)
   - realTable : 执行的 online-ddl 的 origin table

### **gh-ost** 涉及的主要 SQL

```sql 
-- 1. 
   Create /* gh-ost */ table `test`.`_test4_ghc` (
                        id bigint auto_increment,
                        last_update timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        hint varchar(64) charset ascii not null,
                        value varchar(4096) charset ascii not null,
                        primary key(id),
                        unique key hint_uidx(hint)
                ) auto_increment=256 ;
                
-- 2. 
   Create /* gh-ost */ table `test`.`_test4_gho` like `test`.`test4` ;

-- 3.
   Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;

-- 4.
   Insert /* gh-ost */ into `test`.`_test4_ghc`;
-- 5. 
   Insert /* gh-ost `test`.`test4` */ ignore into `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (select `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` from `test`.`test4` force index (`PRIMARY`)
        where (((`id` > _binary'1') or ((`id` = _binary'1'))) and ((`id` < _binary'2') or ((`id` = _binary'2')))) lock in share mode
      )   ;
-- 6. 
   Rename /* gh-ost */ table `test`.`test4` to `test`.`_test4_del`, `test`.`_test4_gho` to `test`.`test4`;
```

>注意
>
>具体 gh-ost 的 SQL 会根据工具执行时所带的参数而变化。本文只列出主要的 SQL ，具体可以参考 gh-ost 官方文档。

### DM 对于 **online-ddl-scheme: gh-ost** 的处理

1. 不执行 _test4_ghc 的创建操作。
2. 不执行 _test4_gho 的创建操作,根据 ghost_schema 、 ghost_table 以及 dm_worker 的 server_id 删除下游 dm_meta.{task_name}\_onlineddl 的记录，清理内存中的相关信息。
   ```sql
   DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table}  
3. 不执行 _test4_gho 的 ddl 操作。把执行的 ddl 记录到 dm_meta.{task_name}\_onlineddl 以及内存中。
    ```sql 
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......)
4. 只要不是 **realtable** 的 dml 全部不执行。
5. rename 拆分成两个 SQL 。
    ```sql 
    rename test.test4 to test._test4_del; rename test._test4_gho to test.test4; 
    ```
6. 不执行 rename to _test4_del 。当要执行 rename ghost_table to origin table 的时候，并不执行 rename ，而是把步骤3 内存中的 ddl 读取出来，然后把 ghost_table，ghost_schema 替换为 origin_table 以及对应的 schema 再执行。
    ```sql 
    alter table test._test4_gho add column cl1 varchar(20) not null 
    --替换为 
    alter table test.test4 add column cl1 varchar(20) not null
    ```  

## online-schema-change : pt

### pt-osc 在实现 online schema change 的过程会产生 2 种 table ： \_\*\_new 、\_\*\_old 以及 3 种 trigger : pt_osc\_\*\_ins 、pt_osc\_\*\_upd 、pt_osc\_\*\_del。

   - **new** 用于应用 ddl ，待数据同步追上 origin table 之后会通过 rename 的方式替换 origin table 。
   - **old** 是由 origin table rename 过来的。
   - 3种 **trigger** 用于在 pt_osc 过程中，同步 orgin table 新产生的数据到 new
   
### dm 在同步过程中会把上述 table 中会分成 3 类：

   - ghostTable : \_\*\_new
   - trashTable : \_\*\_old
   - realTable : 执行的 online-ddl 的 origin table
  
### pt-osc 主要涉及的 SQL

``` sql
-- 1. 
   CREATE TABLE `test`.`_test4_new` ( id int(11) NOT NULL AUTO_INCREMENT,
   date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL,  ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
-- 2.
   ALTER TABLE `test`.`_test4_new` add column c3 int
-- 3. 
   CREATE TRIGGER `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
   CREATE TRIGGER `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
   CREATE TRIGGER `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
-- 4. 
   INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
-- 5.
   RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
-- 6.
   DROP TABLE IF EXISTS `test`.`_test4_old`;
   DROP TRIGGER IF EXISTS `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
   DROP TRIGGER IF EXISTS `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
   DROP TRIGGER IF EXISTS `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
```

>注意
>
>具体 pt-osc 的 SQL 会根据工具执行时所带的参数而变化。本文只列出主要的 SQL ，具体可以参考 pt-osc 官方文档。

### DM 对于 **online-ddl-scheme: pt** 的处理

1. 不执行 _test4_new 的创建操作。根据 ghost_schema 、 ghost_table 以及 dm_worker 的 server_id 删除下游 dm_meta.{task_name}\_onlineddl 的记录，清理内存中的相关信息。
   ```sql 
   DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table} 
2. 不执行 _test4_new 的 ddl 操作。把执行的 ddl 记录到 dm_meta.{task_name}\_onlineddl 以及内存中。
   ```sql 
   REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......)
3. 不执行 TiDB 不支持的相关的 Trigger 操作。
4. 只要不是 **realtable** 的 dml 全部不执行。
5. rename 拆分成两个 SQL 。
   ```sql 
   rename test.test4 to test._test4_old; rename test._test4_new to test.test4; 
6. 不执行 rename to  _test4_old 。当要执行 rename ghost_table to origin table 的时候，并不执行 rename ，而是把步骤 2 内存中的 ddl 读取出来，然后把 ghost_table，ghost_schema 替换为 origin_table 以及对应的 schema 再执行。
   ```sql 
   ALTER TABLE `test`.`_test4_new` add column c3 int
   --替换为 
   ALTER TABLE `test`.`test4` add column c3 int 
7. 不执行 _test4_old 以及 Trigger 的删除操作。

## FAQ：
**Q**： 设置了 **online-ddl-sheme: gh-ost** , 但是 DM 还是出现关于 gh-ost 相关的表的错误。
> [unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......

**A**： 由于 DM 是在最后 rename ghost_table to origin table 的步骤会把内存的 ddl 信息读出，并且还原为 origin table 的 ddl 。而内存中的 ddl 信息是在第 3 步的时候或者重启 dm-woker 启动 task 的时候，从 dm_meta.{task_name}_onlineddl 中读取出来。因此，如果在增量同步过程中，指定的 Pos 跳过了步骤 3 ，但是该 pos 仍在 gh-ost 的 online-ddl 的过程。就会因为 ghost_table 没有正确写入到内存以及 dm_meta.{task_name}_onlineddl ，而导致该问题。
绕过解决方法：
  1. 取消task 的 online-ddl-schema 的配置
  2. 把 **\_\*\_gho 、\_\*\_ghc 、\_\*\_del** 配置到 black-white-list.ignore-tables 中。
  3. 手工在下游的 **TiDB** 执行上游的 ddl 。
  4. 待 Pos 同步到 gh-ost 流程的位置之后，再重新启用 online-ddl-schema 以及注释掉 black-white-list.ignore-tables 。
