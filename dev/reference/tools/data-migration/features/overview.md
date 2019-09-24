---
title: 数据同步功能
summary: DM 提供的功能及其配置介绍
category: reference
---

# 数据同步功能

本文将详细介绍 DM 提供的数据同步功能，以及相关的配置选项。

## Table routing

Table routing 提供将上游 MySQL/MariaDB 实例的某些表同步到下游指定表的功能。

> **注意：**
>
> - 不支持对同一个表设置多个不同的路由规则。
> - Schema 的匹配规则需要单独设置，用来同步 `create/drop schema xx`，例如下面[参数配置](#参数配置)中的 rule-2。

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

将根据 [`schema-pattern`/`table-pattern`](/dev/reference/tools/data-migration/table-selector.md) 匹配上该规则的上游 MySQL/MariaDB 实例的表同步到下游的 `target-schema`/`target-table`。

### 使用示例

下面展示了三个不同场景下的配置示例。

#### 分库分表合并

假设存在分库分表场景，需要将上游两个 MySQL 实例的表 `test_{1,2,3...}`.`t_{1,2,3...}` 同步到下游 TiDB 的一张表 `test`.`t`。

为了同步到下游实例的表 `test`.`t` 需要创建两个 table routing 规则：

- `rule-1` 用来同步匹配上 `schema-pattern: "test_*"` 和 `table-pattern: "t_*"` 的表的 DML/DDL 语句到下游的 `test`.`t`。
- `rule-2` 用来同步匹配上 `schema-pattern: "test_*"` 的库的 DDL 语句，例如 `create/drop schema xx`。

> **注意：**
>
> - 如果下游 TiDB `schema: test` 已经存在， 并且不会被删除，则可以省略 `rule-2`。
> - 如果下游 TiDB `schema: test` 不存在，只设置了 `rule_1`，则同步会报错 `schema test doesn't exist`。

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

假设存在分库场景，将上游两个 MySQL 实例 `test_{1,2,3...}`.`t_{1,2,3...}` 同步到下游 TiDB 的 `test`.`t_{1,2,3...}`，创建一条路由规则即可：

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

## Black & white table lists

上游数据库实例表的黑白名单过滤规则，可以用来过滤或者只同步某些 `database/table` 的所有操作。

### 参数配置

{{< copyable "" >}}

```yaml
black-white-list:
  rule-1:
    do-dbs: ["~^test.*"]         # 以 ~ 字符开头，表示规则是正则表达式
​    ignore-dbs: ["mysql"]
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

- `do-dbs` 要同步的库的白名单，类似于 MySQL 中的 [`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-do-db)
- `ignore-dbs` 要同步的库的黑名单，类似于 MySQL 中的 [`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-ignore-db)
- `do-tables` 要同步的表的白名单，类似于 MySQL 中的 [`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-do-table)
- `ignore-tables` 要同步的表的黑名单，类似于 MySQL 中的 [`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-ignore-table)
- 上面黑白名单中 以 `~` 字符开头名称为[正则表达式](https://golang.org/pkg/regexp/syntax/#hdr-syntax)。

### 过滤规则

`do-dbs` 与 `ignore-dbs` 对应的过滤规则与 MySQL 中的 [Evaluation of Database-Level Replication and Binary Logging Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html) 类似，`do-tables` 与 `ignore-tables` 对应的过滤规则与 MySQL 中的 [Evaluation of Table-Level Replication Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html) 类似。

> **注意：**
>
> DM 中黑白名单过滤规则与 MySQL 中相应规则存在以下区别：
>
> - MySQL 中存在 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-wild-do-table) 与 [`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-wild-ignore-table) 用于支持通配符，DM 中各配置参数直接支持以 `~` 字符开头的正则表达式。
> - DM 当前只支持 `ROW` 格式的 binlog，不支持 `STATEMENT`/`MIXED` 格式的 binlog，因此应与 MySQL 中 `ROW` 格式下的规则对应。
> - 对于 DDL，MySQL 仅依据默认的 database 名称（`USE` 语句显式指定的 database）进行判断，而 DM 优先依据 DDL 中的 database 名称部分进行判断、并当 DDL 中不包含 database 名称时再依据 `USE` 部分进行判断。假设需要判断的 SQL 为 `USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`，且 MySQL 配置了 `replicate-do-db=test_db_1`、DM 配置了 `do-dbs: ["test_db_1"]`，则对于 MySQL 该规则不会生效，而对于 DM 该规则会生效。

判断 table `test`.`t` 是否应该被过滤的过滤流程如下：

1. 首先 **schema 过滤判断**

    - 如果 `do-dbs` 不为空，判断 `do-dbs` 中是否存在一个匹配的 schema。

        - 如果存在，则进入 **table 过滤判断**。
        - 如果不存在，则过滤 `test`.`t`。

    - 如果 `do-dbs` 为空并且 `ignore-dbs` 不为空，判断 `ignore-dbs` 中是否存在一个匹配的 schema。

        - 如果存在，则过滤 `test`.`t`。
        - 如果不存在，则进入 **table 过滤判断**。

    - 如果 `do-dbs` 和 `ignore-dbs` 都为空，则进入 **table 过滤判断**。

2. 进行 **table 过滤判断**

    1. 如果 `do-tables` 不为空，判断 `do-tables` 中是否存在一个匹配的 table。

        - 如果存在，则同步 `test`.`t`。
        - 如果不存在，则过滤 `test`.`t`。

    2. 如果 `ignore-tables` 不为空，判断 `ignore-tables` 中是否存在一个匹配的 table。

        - 如果存在，则过滤 `test`.`t`.
        - 如果不存在，则同步 `test`.`t`。

    3. 如果 `do-tables` 和 `ignore-tables` 都为空，则同步 `test`.`t`。

> **注意：**
>
> 判断 schema `test` 是否被过滤，只进行 **schema 过滤判断**

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
black-white-list:
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
| `forum`.`users` | 是 | 1. schema `forum` 匹配到 `do-dbs` 进入 table 过滤<br> 2. schema 和 table 没有匹配到 `do-tables` 和 `ignore-tables` 中任意一项，并且 `do-tables` 不为空，因此过滤 |
| `forum`.`messages` | 否 | 1. schema `forum` 匹配到 `do-dbs` 进入 table 过滤<br> 2. schema 和 table 匹配到 `do-tables` 的 `db-name: "~^forum.*",tbl-name: "messages"` |
| `forum_backup_2018`.`messages` | 否 | 1. schema `forum_backup_2018` 匹配到 `do-dbs` 进入 table 过滤<br> 2. schema 和 table 匹配到 `do-tables` 的  `db-name: "~^forum.*",tbl-name: "messages"` |

## Binlog event filter

Binlog event filter 是比同步表黑白名单更加细粒度的过滤规则，可以指定只同步或者过滤掉某些 `schema / table` 的指定类型 binlog，比如 `INSERT`，`TRUNCATE TABLE`。

> **注意：**
>
> 同一个表匹配上多个规则，将会顺序应用这些规则，并且黑名单的优先级高于白名单，即如果同时存在规则 `Ignore` 和 `Do` 应用在某个 table 上，那么 `Ignore` 生效。

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

- [`schema-pattern`/`table-pattern`](/dev/reference/tools/data-migration/table-selector.md)：对匹配上的上游 MySQL/MariaDB 实例的表的 binlog events 或者 DDL SQL 语句进行以下规则过滤。

- `events`：binlog events 数组。

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

- `sql-pattern`：用于过滤指定的 DDL SQL 语句，支持正则表达式匹配，例如上面示例 `"^DROP\\s+PROCEDURE"`。

- `action`：string(`Do` / `Ignore`)；进行下面规则判断，满足其中之一则过滤，否则不过滤。

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

#### 只同步分库分表的 DML 操作

需要设置下面两个 `Binlog event filter rule` 只同步 DML 操作：

- `do-table-rule` 只同步所有匹配到 pattern `test_*`.`t_*` 的 table 的 `create table`、`insert`、`update`、`delete` 操作。
- `do-schema-rule` 只同步所有匹配到 pattern `test_*` 的 schema 的 `create database` 操作。

> **注意：**
>
> 同步 `create database/table` 的原因是创建库和表后才能同步 `DML`。

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
> 全局过滤规则的设置必须尽可能严格，以避免预期之外地过滤掉需要同步的数据。

可设置如下规则过滤 TiDB parser 不支持的 `PARTITION` 语句：

{{< copyable "" >}}

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## Column mapping

Column mapping 提供对表的列值进行修改的功能。可以根据不同的表达式对表的指定列做不同的修改操作，目前只支持 DM 提供的内置表达式。

> **注意：**
>
> - 不支持修改 column 的类型和表结构。
> - 不支持对同一个表设置多个不同的列值转换规则。

### 参数配置

{{< copyable "" >}}

```yaml
column-mappings:
  rule-1:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["1", "test", "t", "_"]
  rule-2:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["2", "test", "t", "_"]
```

### 参数解释

- [`schema-pattern`/`table-pattern`](/dev/reference/tools/data-migration/table-selector.md)：对匹配上该规则的上游 MySQL/MariaDB 实例的表按照指定 `expression` 进行列值修改操作。
- `source-column`，`target-column`：对 `source-column` 列的值按照指定 `expression` 进行修改，将修改后的值赋值给 `target-column`。
- `expression`：对数据进行转换的表达式，目前只支持下面的内置计算表达式。

#### `partition id` 表达式

`partition id` 目的是为了解决分库分表合并同步的自增主键的冲突。

**`partition id` 限制**

注意下面的限制：

- 只支持类型为 bigint 的列，通常为自增主键，联合主键或者联合唯一索引的其中一列
- 如果 `schema 前缀` 不为空，则库名的组成必须为 `schema 前缀` 或者 `schema 前缀 + 分隔符 + 数字（即 schema ID）`，例如：支持 `s` 和 `s_1`，不支持 `s_a`
- 如果 `table 前缀` 不为空，则表名的组成必须为 `table 前缀` 或者 `table 前缀 + 分隔符 + 数字（即 table ID）`
- 如果库名/表名不包含 `… + 分隔符 + 数字` 部分，则对应的 ID 默认为 0
- 对分库分表的规模支持限制如下
    - 支持最多 16 个 MySQL/MariaDB 实例（0 <= instance ID <= 15）
    - 每个实例支持最多 128 个 schema（0 <= schema ID  <= 127）
    - 每个实例的每个 schema 支持最多 256 个 table（0 <= table ID <= 255）
    - 进行列值映射的列的范围 (0 <= ID <= 17592186044415)
    - `{instance ID, schema ID, table ID}` 组合需要保持唯一
- 目前该功能是定制功能，如果需要调整请联系相关开发人员进行调整

**`partition id` 参数配置**

用户需要在 arguments 里面按顺序设置以下三个或四个参数：

- `instance_id`：客户指定的上游分库分表的 MySQL/MariaDB instance ID（0 <= instance ID <= 15）
- `schema 前缀`：用来解析库名并获取 `schema ID`
- `table 前缀`：用来解释表名并获取 `table ID`
- 分隔符：用来分隔前缀与 ID，可省略，省略时分隔符默认为空字符串

`instance_id`、`schema 前缀` 和 `table 前缀` 这三个参数均可被设置为空字符串（`""`），表示对应的部分不会被编码进 `partition id`。

**`partition id` 表达式规则**

`partition id` 会用 arguments 里面的数字来填充自增主键 ID 的首个比特位，计算出来一个 int64（即 MySQL bigint）类型的值，具体规则如下：

| instance_id | schema 前缀 | table 前缀 | 编码 |
|:------------|:--------------|:-------------|---------:|
| ☑ 已定义   | ☑ 已定义     | ☑ 已定义    | [`S`: 1 比特位] [`I`: 4 比特位] [`D`: 7 比特位] [`T`: 8 比特位] [`P`: 44 比特位] |
| ☐ 空     | ☑ 已定义     | ☑ 已定义    | [`S`: 1 比特位] [`D`: 7 比特位] [`T`: 8 比特位] [`P`: 48 比特位] |
| ☑ 已定义   | ☐ 空       | ☑ 已定义    | [`S`: 1 比特位] [`I`: 4 比特位] [`T`: 8 比特位] [`P`: 51 比特位] |
| ☑ 已定义   | ☑ 已定义     | ☐ 空      | [`S`: 1 比特位] [`I`: 4 比特位] [`D`: 7 比特位] [`P`: 52 比特位] |
| ☐ 空     | ☐ 空       | ☑ 已定义    | [`S`: 1 比特位] [`T`: 8 比特位] [`P`: 55 比特位] |
| ☐ 空     | ☑ 已定义     | ☐ 空      | [`S`: 1 比特位] [`D`: 7 比特位] [`P`: 56 比特位] |
| ☑ 已定义   | ☐ 空       | ☐ 空      | [`S`: 1 比特位] [`I`: 4 比特位] [`P`: 59 比特位] |

- `S`：符号位，保留
- `I`：instance ID，默认 4 比特位
- `D`：schema ID，默认 7 比特位
- `T`：table ID，默认 8 比特位
- `P`：自增主键 ID，占据剩下的比特位（≥44 比特位）

### 使用示例

假设存在分库分表场景：将上游两个 MySQL 实例的 `test_{1,2,3...}`.`t_{1,2,3...}` 同步到下游 TiDB 的 `test`.`t`，并且这些表都有自增主键。

需要设置下面两个规则：

{{< copyable "" >}}

```yaml
column-mappings:
  rule-1:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["1", "test", "t", "_"]
  rule-2:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["2", "test", "t", "_"]
```

- MySQL instance 1 的表 `test_1`.`t_1` 的 `ID = 1` 的行经过转换后 ID = 1 变为 `1 << (64-1-4) | 1 << (64-1-4-7) | 1 << 44 | 1 = 580981944116838401`
- MySQL instance 2 的表 `test_1`.`t_2` 的 `ID = 1` 的行经过转换后 ID = 2 变为 `2 << (64-1-4) | 1 << (64-1-4-7) | 2 << 44 | 2 = 1157460288606306306`

## 同步延迟监控

DM 支持通过 heartbeat 真实同步数据来计算每个同步任务与 MySQL/MariaDB 的实时同步延迟。

> **注意：**
>
> - 同步延迟的估算的精度在秒级别。
> - heartbeat 相关的 binlog 不会同步到下游，在计算延迟后会被丢弃。

### 系统权限

如果开启 heartbeat 功能，需要上游 MySQL/MariaDB 实例提供下面的权限：

- SELECT
- INSERT
- CREATE (databases, tables)

### 参数配置

在 task 的配置文件中设置：

```
enable-heartbeat: true
```

### 原理介绍

- DM-worker 在对应的上游 MySQL/MariaDB 创建库 `dm_heartbeat`（当前不可配置）
- DM-worker 在对应的上游 MySQL/MariaDB 创建表 `heartbeat`（当前不可配置）
- DM-worker 每秒钟（当前不可配置）在对应的上游 MySQL/MariaDB 的 `dm_heartbeat`.`heartbeat` 表中，利用 `replace statement` 更新当前时间戳 `TS_master`
- DM-worker 每个任务拿到 `dm_heartbeat`.`heartbeat` 的 binlog 后，更新自己的同步时间 `TS_slave_task`
- DM-worker 每 10 秒在对应的上游 MySQL/MariaDB 的 `dm_heartbeat`.`heartbeat` 查询当前的 `TS_master`，并且对每个任务计算 `task_lag` = `TS_master` - `TS_slave_task`

可以在 metrics 的 [binlog replication](/dev/reference/tools/data-migration/monitor.md#binlog-replication) 处理单元找到 replicate lag 监控项。
