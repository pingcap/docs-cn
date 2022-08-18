---
title: 主要特性
summary: 了解 DM 的各主要功能特性或相关的配置选项。
---

# 主要特性

本文档介绍 DM 提供的数据迁移功能以及相关的配置选项与使用示例。

Table Routing、Block & Allow Lists、Binlog Event Filter 在匹配库表名时，有以下版本差异：

+ 对于 v1.0.5 版及后续版本，以上功能均支持[通配符匹配](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)。但注意所有版本中通配符匹配中的 `*` 符号 **只能有一个且必须在末尾**。
+ 对于 v1.0.5 以前的版本，Table Routing 和 Binlog Event Filter 支持通配符，但不支持 `[...]` 与 `[!...]` 表达式。Block & Allow Lists 仅支持正则表达式。

在简单任务场景下推荐使用通配符匹配。

## Table routing

Table routing 提供将上游 MySQL/MariaDB 实例的某些表迁移到下游指定表的功能。

> **注意：**
>
> - 不支持对同一个表设置多个不同的路由规则。
> - Schema 的匹配规则需要单独设置，用来迁移 `CREATE/DROP SCHEMA xx`，例如下面[参数配置](#参数配置)中的 rule-2。

### 参数配置

{{< copyable "" >}}

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### 参数解释

将根据 [`schema-pattern`/`table-pattern`](/dm/table-selector.md) 匹配上该规则的上游 MySQL/MariaDB 实例的表迁移到下游的 `target-schema`/`target-table`。

### 使用示例

下面展示了三个不同场景下的配置示例。

#### 分库分表合并

假设存在分库分表场景，需要将上游两个 MySQL 实例的表 `test_{1,2,3...}`.`t_{1,2,3...}` 迁移到下游 TiDB 的一张表 `test`.`t`。

为了迁移到下游实例的表 `test`.`t`，需要创建以下 table routing 规则：

- `rule-1` 用来迁移匹配上 `schema-pattern: "test_*"` 和 `table-pattern: "t_*"` 的表的 DML/DDL 语句到下游的 `test`.`t`。
- `rule-2` 用来迁移匹配上 `schema-pattern: "test_*"` 的库的 DDL 语句，例如 `CREATE/DROP SCHEMA xx`。

> **注意：**
>
> - 如果下游 TiDB `schema: test` 已经存在，并且不会被删除，则可以省略 `rule-2`。
> - 如果下游 TiDB `schema: test` 不存在，只设置了 `rule_1`，则迁移会报错 `schema test doesn't exist`。

{{< copyable "" >}}

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### 分库合并

假设存在分库场景，将上游两个 MySQL 实例 `test_{1,2,3...}`.`t_{1,2,3...}` 迁移到下游 TiDB 的 `test`.`t_{1,2,3...}`，创建一条路由规则即可：

{{< copyable "" >}}

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### 错误的 table routing

假设存在下面两个路由规则，`test_1_bak`.`t_1_bak` 可以匹配上 `rule-1` 和 `rule-2`，违反 table 路由的限制而报错。

{{< copyable "" >}}

```yaml
  rule-0:
    schema-pattern: "test_*"
    target-schema: "test"
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_1_bak"
    table-pattern: "t_1_bak"
    target-schema: "test"
    target-table: "t_bak"
```

## Block & Allow Table Lists

上游数据库实例表的黑白名单过滤规则，可以用来过滤或者只迁移某些 `database/table` 的所有操作。

### 参数配置

{{< copyable "" >}}

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

### 参数解释

- `do-dbs`：要迁移的库的白名单，类似于 MySQL 中的 [`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)。
- `ignore-dbs`：要迁移的库的黑名单，类似于 MySQL 中的 [`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)。
- `do-tables`：要迁移的表的白名单，类似于 MySQL 中的 [`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)。必须同时指定 `db-name` 与 `tbl-name`。
- `ignore-tables`：要迁移的表的黑名单，类似于 MySQL 中的 [`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)。必须同时指定 `db-name` 与 `tbl-name`。

以上参数值以 `~` 开头时均支持使用[正则表达式](https://golang.org/pkg/regexp/syntax/#hdr-syntax)来匹配库名、表名。

### 过滤规则

`do-dbs` 与 `ignore-dbs` 对应的过滤规则与 MySQL 中的 [Evaluation of Database-Level Replication and Binary Logging Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html) 类似，`do-tables` 与 `ignore-tables` 对应的过滤规则与 MySQL 中的 [Evaluation of Table-Level Replication Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html) 类似。

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

### 使用示例

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

| table | 是否过滤| 过滤的原因 |
|:----|:----|:--------------|
| `logs`.`messages_2016` | 是 | schema `logs` 没有匹配到 `do-dbs` 任意一项 |
| `logs`.`messages_2017` | 是 | schema `logs` 没有匹配到 `do-dbs` 任意一项 |
| `logs`.`messages_2018` | 是 | schema `logs` 没有匹配到 `do-dbs` 任意一项 |
| `forum_backup_2016`.`messages` | 是 | schema `forum_backup_2016` 没有匹配到 `do-dbs` 任意一项 |
| `forum_backup_2017`.`messages` | 是 | schema `forum_backup_2017` 没有匹配到 `do-dbs` 任意一项 |
| `forum`.`users` | 是 | 1. schema `forum` 匹配到 `do-dbs`，进入 table 过滤判断<br/> 2. schema 和 table 没有匹配到 `do-tables` 和 `ignore-tables` 中任意一项，并且 `do-tables` 不为空，因此过滤 |
| `forum`.`messages` | 否 | 1. schema `forum` 匹配到 `do-dbs`，进入 table 过滤判断<br/> 2. schema 和 table 匹配到 `do-tables` 的 `db-name: "~^forum.*",tbl-name: "messages"` |
| `forum_backup_2018`.`messages` | 否 | 1. schema `forum_backup_2018` 匹配到 `do-dbs`，进入 table 过滤判断<br/> 2. schema 和 table 匹配到 `do-tables` 的  `db-name: "~^forum.*",tbl-name: "messages"` |

## Binlog event filter

Binlog event filter 是比迁移表黑白名单更加细粒度的过滤规则，可以指定只迁移或者过滤掉某些 `schema / table` 的指定类型 binlog，比如 `INSERT`、`TRUNCATE TABLE`。

> **注意：**
>
> - 同一个表匹配上多个规则，将会顺序应用这些规则，并且黑名单的优先级高于白名单，即如果同时存在规则 `Ignore` 和 `Do` 应用在某个 table 上，那么 `Ignore` 生效。
> - 从 DM v2.0.2 开始，Binlog event filter 也可以在上游数据库配置文件中进行配置。见[上游数据库配置文件介绍](/dm/dm-source-configuration-file.md)。

### 参数配置

{{< copyable "" >}}

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

### 参数解释

- [`schema-pattern`/`table-pattern`](/dm/table-selector.md)：对匹配上的上游 MySQL/MariaDB 实例的表的 binlog events 或者 DDL SQL 语句通过以下规则进行过滤。

- `events`：binlog events 数组，仅支持从以下 `Event` 中选择一项或多项。

    | Event           | 分类 | 解释                           |
    | --------------- | ---- | ----------------------------- |
    | all             |      | 代表包含下面所有的 events        |
    | all dml         |      | 代表包含下面所有 DML events     |
    | all ddl         |      | 代表包含下面所有 DDL events     |
    | none            |      | 代表不包含下面所有 events        |
    | none ddl        |      | 代表不包含下面所有 DDL events    |
    | none dml        |      | 代表不包含下面所有 DML events    |
    | insert          | DML  | insert DML event              |
    | update          | DML  | update DML event              |
    | delete          | DML  | delete DML event              |
    | create database | DDL  | create database event         |
    | drop database   | DDL  | drop database event           |
    | create table    | DDL  | create table event            |
    | create index    | DDL  | create index event            |
    | drop table      | DDL  | drop table event              |
    | truncate table  | DDL  | truncate table event          |
    | rename table    | DDL  | rename table event            |
    | drop index      | DDL  | drop index event              |
    | alter table     | DDL  | alter table event             |

- `sql-pattern`：用于过滤指定的 DDL SQL 语句，支持正则表达式匹配，例如上面示例中的 `"^DROP\\s+PROCEDURE"`。

- `action`：string (`Do` / `Ignore`)；进行下面规则判断，满足其中之一则过滤，否则不过滤。

    - `Do`：白名单。binlog event 如果满足下面两个条件之一就会被过滤掉：
        - 不在该 rule 的 `events` 中。
        - 如果规则的 `sql-pattern` 不为空的话，对应的 SQL 没有匹配上 `sql-pattern` 中任意一项。
    - `Ignore`：黑名单。如果满足下面两个条件之一就会被过滤掉：
        - 在该 rule 的 `events` 中。
        - 如果规则的 `sql-pattern` 不为空的话，对应的 SQL 可以匹配上 `sql-pattern` 中任意一项。

### 使用示例

#### 过滤分库分表的所有删除操作

需要设置下面两个 `Binlog event filter rule` 来过滤掉所有的删除操作：

- `filter-table-rule` 过滤掉所有匹配到 pattern `test_*`.`t_*` 的 table 的 `turncate table`、`drop table`、`delete statement` 操作。
- `filter-schema-rule` 过滤掉所有匹配到 pattern `test_*` 的 schema 的 `drop database` 操作。

{{< copyable "" >}}

```yaml
filters:
  filter-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  filter-schema-rule:
    schema-pattern: "test_*"
    events: ["drop database"]
    action: Ignore
```

#### 只迁移分库分表的 DML 操作

需要设置下面两个 `Binlog event filter rule` 只迁移 DML 操作：

- `do-table-rule` 只迁移所有匹配到 pattern `test_*`.`t_*` 的 table 的 `create table`、`insert`、`update`、`delete` 操作。
- `do-schema-rule` 只迁移所有匹配到 pattern `test_*` 的 schema 的 `create database` 操作。

> **注意：**
>
> 迁移 `create database/table` 的原因是创建库和表后才能迁移 `DML`。

{{< copyable "" >}}

```yaml
filters:
  do-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["create table", "all dml"]
    action: Do
  do-schema-rule:
    schema-pattern: "test_*"
    events: ["create database"]
    action: Do
```

#### 过滤 TiDB 不支持的 SQL 语句

可设置如下规则过滤 TiDB 不支持的 `PROCEDURE` 语句：

{{< copyable "" >}}

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

#### 过滤 TiDB parser 不支持的 SQL 语句

对于 TiDB parser 不支持的 SQL 语句，DM 无法解析获得 `schema`/`table` 信息，因此需要使用全局过滤规则：`schema-pattern: "*"`。

> **注意：**
>
> 全局过滤规则的设置必须尽可能严格，以避免过滤掉需要迁移的数据。

可设置如下规则过滤某些版本的 TiDB parser 不支持的 `PARTITION` 语句：

{{< copyable "" >}}

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## online DDL 工具支持

在 MySQL 生态中，gh-ost 与 pt-osc 等工具较广泛地被使用，DM 对其提供了特殊的支持以避免对不必要的中间数据进行迁移。

有关 DM 对 online DDL 工具支持的原理、处理流程等，可参考 [online-ddl](/dm/feature-online-ddl.md)。

### 使用限制

- DM 仅针对 gh-ost 与 pt-osc 做了特殊支持。
- 在开启 `online-ddl` 时，增量复制对应的 checkpoint 应不处于 online DDL 执行过程中。如上游某次 online DDL 操作开始于 binlog `position-A`、结束于 `position-B`，则增量复制的起始点应早于 `position-A` 或晚于 `position-B`，否则可能出现迁移出错，具体可参考 [FAQ](/dm/dm-faq.md#设置了-online-ddl-scheme-gh-ost-gh-ost-表相关的-ddl-报错该如何处理)。

### 参数配置

<SimpleTab>
<div label="v2.0.5 及之后的版本">
 
在 v2.0.5 及之后的版本，请在 `task` 配置文件中使用 `online-ddl` 配置项。

如上游 MySQL/MariaDB （同时）使用 gh-ost 或 pt-osc 工具，则在 task 的配置文件中设置：

```yml
online-ddl: true
```

> **注意：**
>
> 自 v2.0.5 起，`online-ddl-scheme` 已被弃用，请使用 `online-ddl` 代替 `online-ddl-scheme`。如设置 `online-ddl: true` 会覆盖掉 `online-ddl-scheme`。如设置 `online-ddl-scheme: "pt"` 或 `online-ddl-scheme: "gh-ost"` 会被转换为 `online-ddl: true`。

</div>

<div label="v2.0.5 之前的版本">

在 v2.0.5 之前的版本（不含 v2.0.5），请在 `task` 配置文件中使用 `online-ddl-scheme` 配置项。

如上游 MySQL/MariaDB 使用的是 gh-ost 工具，则在 task 的配置文件中设置：

```yml
online-ddl-scheme: "gh-ost"
```

如上游 MySQL/MariaDB 使用的是 pt-osc 工具，则在 task 的配置文件中设置：

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>

## 分库分表合并

DM 支持将上游 MySQL/MariaDB 各分库分表中的 DML、DDL 数据合并后迁移到下游 TiDB 的库表中。

### 使用限制

目前分库分表合并功能仅支持有限的场景，使用该功能前，请仔细阅读[悲观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-pessimistic.md#使用限制)和[乐观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-optimistic.md#使用限制)。

### 参数配置

在 task 的配置文件中设置：

```
shard-mode: "pessimistic" # 默认值为 "" 即无需协调。如果为分库分表合并任务，请设置为悲观协调模式 "pessimistic"。在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
```

### 手动处理 Sharding DDL Lock

如果分库分表合并迁移过程中发生了异常，对于部分场景，可尝试参考[手动处理 Sharding DDL Lock](/dm/manually-handling-sharding-ddl-locks.md)进行处理。
