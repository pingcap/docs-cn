---
title: TiDB Data Migration 黑白名单过滤
summary:  了解 DM 的关键特性黑白名单过滤 (Block & Allow List) 的使用方法和注意事项。
---

# TiDB Data Migration 黑白名单过滤

使用 TiDB Data Migration (DM) 迁移数据时，你可以配置上游数据库实例表的黑白名单过滤 (Block & Allow List) 规则，用来过滤或者只迁移某些 `database/table` 的所有操作。

## 配置黑白名单

在迁移任务配置文件中，添加如下配置：

```yaml
block-allow-list:             # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  rule-1:
    do-dbs: ["test*"]         # 非 ~ 字符开头，表示规则是通配符；v1.0.5 及后续版本支持通配符规则。
    do-tables:
    - db-name: "test[123]"    # 匹配 test1、test2、test3。
      tbl-name: "t[1-5]"      # 匹配 t1、t2、t3、t4、t5。
    - db-name: "test"
      tbl-name: "t"
  rule-2:
    do-dbs: ["~^test.*"]      # 以 ~ 字符开头，表示规则是正则表达式。
    ignore-dbs: ["mysql"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "test"
      tbl-name: "t"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

在简单任务场景下，推荐使用通配符匹配库表名，但需注意以下版本差异：

+ 对于 v1.0.5 版及后续版本，黑白名单支持[通配符匹配](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)。但注意所有版本中通配符匹配中的 `*` 符号 **只能有一个，且必须在末尾**。
+ 对于 v1.0.5 以前的版本，黑白名单仅支持正则表达式。

## 参数解释

- `do-dbs`：要迁移的库的白名单，类似于 MySQL 中的 [`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)。
- `ignore-dbs`：要迁移的库的黑名单，类似于 MySQL 中的 [`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)。
- `do-tables`：要迁移的表的白名单，类似于 MySQL 中的 [`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)。必须同时指定 `db-name` 与 `tbl-name`。
- `ignore-tables`：要迁移的表的黑名单，类似于 MySQL 中的 [`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)。必须同时指定 `db-name` 与 `tbl-name`。

以上参数值以 `~` 开头时均支持使用[正则表达式](https://golang.org/pkg/regexp/syntax/#hdr-syntax)来匹配库名、表名。

## 过滤规则

- `do-dbs` 与 `ignore-dbs` 对应的过滤规则与 MySQL 中的 [Evaluation of Database-Level Replication and Binary Logging Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html) 类似。
- `do-tables` 与 `ignore-tables` 对应的过滤规则与 MySQL 中的 [Evaluation of Table-Level Replication Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html) 类似。

> **注意：**
>
> DM 中黑白名单过滤规则与 MySQL 中相应规则存在以下区别：
>
> - MySQL 中存在 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table) 与 [`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table) 用于支持通配符，DM 中各配置参数直接支持以 `~` 字符开头的正则表达式。
> - DM 当前只支持 `ROW` 格式的 binlog，不支持 `STATEMENT`/`MIXED` 格式的 binlog，因此应与 MySQL 中 `ROW` 格式下的规则对应。
> - 对于 DDL，MySQL 仅依据默认的 database 名称（`USE` 语句显式指定的 database）进行判断，而 DM 优先依据 DDL 中的 database 名称部分进行判断，并当 DDL 中不包含 database 名称时再依据 `USE` 部分进行判断。假设需要判断的 SQL 为 `USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`，且 MySQL 配置了 `replicate-do-db=test_db_1`、DM 配置了 `do-dbs: ["test_db_1"]`，则对于 MySQL 该规则不会生效，而对于 DM 该规则会生效。

判断 table `test`.`t` 是否应该被过滤的流程如下：

1. 首先进行 **schema 过滤判断**

    - 如果 `do-dbs` 不为空，判断 `do-dbs` 中是否存在一个匹配的 schema。

        - 如果存在，则进入 **table 过滤判断**。
        - 如果不存在，则过滤 `test`.`t`。

    - 如果 `do-dbs` 为空并且 `ignore-dbs` 不为空，判断 `ignore-dbs` 中是否存在一个匹配的 schema。

        - 如果存在，则过滤 `test`.`t`。
        - 如果不存在，则进入 **table 过滤判断**。

    - 如果 `do-dbs` 和 `ignore-dbs` 都为空，则进入 **table 过滤判断**。

2. 进行 **table 过滤判断**

    1. 如果 `do-tables` 不为空，判断 `do-tables` 中是否存在一个匹配的 table。

        - 如果存在，则迁移 `test`.`t`。
        - 如果不存在，则过滤 `test`.`t`。

    2. 如果 `ignore-tables` 不为空，判断 `ignore-tables` 中是否存在一个匹配的 table。

        - 如果存在，则过滤 `test`.`t`.
        - 如果不存在，则迁移 `test`.`t`。

    3. 如果 `do-tables` 和 `ignore-tables` 都为空，则迁移 `test`.`t`。

> **注意：**
>
> 如果是判断 schema `test` 是否应该被过滤，则只进行 **schema 过滤判断**。

## 使用示例

假设上游 MySQL 实例包含以下表：

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

配置如下：

{{< copyable "" >}}

```yaml
block-allow-list:  # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list。
  bw-rule:
    do-dbs: ["forum_backup_2018", "forum"]
    ignore-dbs: ["~^forum_backup_"]
    do-tables:
    - db-name: "logs"
      tbl-name: "~_2018$"
    - db-name: "~^forum.*"
​      tbl-name: "messages"
    ignore-tables:
    - db-name: "~.*"
​      tbl-name: "^messages.*"
```

应用 `bw-rule` 规则后：

+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| table                          | 是否过滤              | 过滤的原因                                                                                                 |
+:===============================+:======================+:===========================================================================================================+
| `logs`.`messages_2016`         | 是                    | schema `logs` 没有匹配到 `do-dbs` 任意一项                                                                 |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `logs`.`messages_2017`         | 是                    | schema `logs` 没有匹配到 `do-dbs` 任意一项                                                                 |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `logs`.`messages_2018`         | 是                    | schema `logs` 没有匹配到 `do-dbs` 任意一项                                                                 |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `forum_backup_2016`.`messages` | 是                    | schema `forum_backup_2016` 没有匹配到 `do-dbs` 任意一项                                                    |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `forum_backup_2017`.`messages` | 是                    | schema `forum_backup_2017` 没有匹配到 `do-dbs` 任意一项                                                    |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `forum`.`users`                | 是                    | 1\. schema `forum` 匹配到 `do-dbs`，进入 table 过滤判断                                                    |
|                                |                       | 2. schema 和 table 没有匹配到 `do-tables` 和 `ignore-tables` 中任意一项，并且 `do-tables` 不为空，因此过滤 |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `forum`.`messages`             | 否                    | 1\. schema `forum` 匹配到 `do-dbs`，进入 table 过滤判断                                                    |
|                                |                       | 2. schema 和 table 匹配到 `do-tables` 的 `db-name: "~^forum.*",tbl-name: "messages"`                       |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
| `forum_backup_2018`.`messages` | 否                    | 1\. schema `forum_backup_2018` 匹配到 `do-dbs`，进入 table 过滤判断                                        |
|                                |                       | 2. schema 和 table 匹配到 `do-tables` 的 `db-name: "~^forum.*",tbl-name: "messages"`                       |
+--------------------------------+-----------------------+------------------------------------------------------------------------------------------------------------+
