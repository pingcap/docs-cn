---
title: DM 执行任务时的前置检查
summary: 了解 DM 执行数据迁移任务时将进行的前置检查。
aliases: ['/docs-cn/tidb-data-migration/dev/precheck/']
---

# 任务前置检查

本文介绍了 DM 提供的前置检查功能，此功能用于在数据迁移任务启动时提前检测出上游 MySQL 实例配置中可能存在的一些错误。

## 使用命令

`check-task` 命令用于对上游 MySQL 实例配置是否满足 DM 要求进行前置检查。

> **注意：**
> 
> 在执行 `start-task/resume-task` 时，会默认先执行 `check-task`，在检查通过后，才正式执行 `start-task/resume-task`。

## 检查内容

上下游数据库用户必须具备相应读写权限。当数据迁移任务启动时，DM 会根据配置文件自动检查下列权限和上游配置：

+ 数据库版本

    - MySQL 版本 > 5.5
    - MariaDB 版本 >= 10.1.2

    > **警告：**
    >
    > 1. 支持从 MySQL v8.0 迁移数据是 DM v2.0 及以上版本的实验特性，不建议在生产环境下使用。
    > 
    > 2. 支持从 MariaDB 迁移数据也是 DM 的实验特性，不建议在生产环境下使用。

+ 上游 MySQL 表结构的兼容性

    - TiDB 不支持外键，如果上游表设置了外键，则返回警告；
    - （必须）字符集存在兼容性差异，详见 [TiDB 支持的字符集](/character-set-and-collation.md)；
    - （必须）DM 还会检查上游表中是否存在主键或唯一键约束，在 v1.0.7 版本引入。

对于 full/all 模式，将检查

+ （必须）上游 dump 权限

    - 检查 INFORMATION_SCHEMA 和 dump 表的 SELECT 权限；
    - 如果 consistency=flush，需检查 RELOAD 权限；
    - 如果 consistency=flush/lock，需检查 dump 表的 LOCK TABLES 权限。

+ （必须）上游 MySQL 多实例分库分表的一致性

    + 悲观协调模式下，检查所有分表的表结构是否一致，检查内容包括

        - Column 数量
        - Column 名称
        - Column 顺序
        - Column 类型
        - 主键
        - 唯一索引
    
    + 乐观协调模式下，检查所有分表结构是否满足[乐观协调兼容](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)；

    + 如果之前成功 `start-task` 过，那么将不会对一致性进行检查。

+ 分表中自增主键检查

    - 分表存在自增主键时返回警告，自增主键冲突请用户自行参照[自增主键冲突处理](/dm/shard-merge-best-practices.md#自增主键冲突处理)解决。

对于 increment/all 模式，将检查

+ 数据库用户是否具备 replication 权限（必须）

    - 检查 REPLiCATION CLIENT 权限；
    - 检查 REPLICATION SLAVE 权限。

+ 数据库主从配置（必须）

    - 需设置 `server_id`。

+ MySQL binlog 配置（必须）

    - binlog 是否开启（DM 要求 binlog 必须开启）；
    - 是否有 `binlog_format=ROW`（DM 只支持 ROW 格式的 binlog 迁移）；
    - 是否有 `binlog_row_image=FULL`（DM 只支持 `binlog_row_image=FULL`）；
    - 如果配置 `binlog_do_db` 或者 `binlog_ignore_db`，那么检查需要迁移的库表，是否满足 `binlog_do_db` 和 `binlog_ignore_db` 的条件。

+ 检查上游是否处于 [Online-DDL](/dm/feature-online-ddl.md) 过程中，即创建了 `ghost` 表，但还未执行 `rename` 的阶段。

## 相关配置

现 `check-task` 支持多线程检查，线程数随 `mydumpers` 中的 `threads` 变化而变化。分表数目达到万级别时，检查可在分钟级完成。

```yaml
mydumpers:                           # dump 处理单元的运行配置参数
  global:                            # 配置名称
    threads: 4                       # dump 处理单元从上游数据库实例导出数据和 check-task 访问上游的线程数量，默认值为 4
    chunk-filesize: 64               # dump 处理单元生成的数据文件大小，默认值为 64，单位为 MB
    extra-args: "--consistency none" # dump 处理单元的其他参数，不需要在 extra-args 中配置 table-list，DM 会自动生成

```