---
title: TiDB Data Migration 表路由
summary: 了解 DM 的关键特性表路由 (Table Routing) 的使用方法和注意事项。
---

# TiDB Data Migration 表路由

使用 TiDB Data Migration (DM) 迁移数据时，你可以配置表路由 (Table Routing) 规则，指定将上游 MySQL/MariaDB 实例的特定表迁移到下游的特定表。

> **注意：**
>
> - 不支持对同一个表设置多个不同的路由规则。
> - Schema 的匹配规则需要单独设置，用来迁移 `CREATE/DROP SCHEMA ...`，例如下面[配置表路由](#配置表路由)中的 rule-2。

## 配置表路由

在迁移任务配置文件中，添加如下配置：

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    # extract-table、extract-schema 和 extract-source 为可选配置，仅在需要提取分表、分库和数据源信息时填写
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

支持正则表达式和通配符来匹配库表名，在简单任务场景下，推荐使用通配符匹配库表名，但需注意以下几点：

+ 支持的通配符包括 `*`、`?` 以及 `[]`。注意通配符匹配中的 `*` 符号只能有一个，且必须在末尾。例如用 `table-pattern: "t_*"` 中的 `"t_*"` 表示 `t_` 开头的表。详情请参考[通配符匹配](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)。
+ `table-regexp`、`schema-regexp` 和 `source-regexp` 仅支持配置正则表达式，但不能以 `~` 符号开头。
+ `schema-pattern` 和 `table-pattern` 同时支持通配符和正则表达式。正则表达式必须以 `~` 符号开头。

## 参数解释

- 对于匹配上 [`schema-pattern`/`table-pattern`](/dm/table-selector.md) 规则的上游 MySQL/MariaDB 实例的表，DM 将它们迁移到下游的 `target-schema`/`target-table`。
- 对于匹配上 `schema-pattern`/`table-pattern` 规则的分表，DM 通过 `extract-table`.`table-regexp` 提取分表信息，通过 `extract-schema`.`schema-regexp` 提取分库信息，通过 `extract-source`.`source-regexp` 提取数据来源信息，然后写入到下游合表对应的 `target-column` 中。

## 使用示例

下面展示了四个不同场景下的配置示例。如果你需要从小数据量分库分表 MySQL 合并迁移数据到 TiDB，请参考[这篇文档](/migrate-small-mysql-shards-to-tidb.md)

### 分库分表合并

假设存在分库分表场景，需要将上游两个 MySQL 实例的表 `test_{1,2,3...}`.`t_{1,2,3...}` 迁移到下游 TiDB 的一张表 `test`.`t`。

为了迁移到下游实例的表 `test`.`t`，需要创建以下表路由规则：

- `rule-1` 用来迁移匹配上 `schema-pattern: "test_*"` 和 `table-pattern: "t_*"` 的表的 DML/DDL 语句到下游的 `test`.`t`。
- `rule-2` 用来迁移匹配上 `schema-pattern: "test_*"` 的库的 DDL 语句，例如 `CREATE/DROP SCHEMA xx`。

> **注意：**
>
> - 如果下游 TiDB `schema: test` 已经存在，并且不会被删除，则可以省略 `rule-2`。
> - 如果下游 TiDB `schema: test` 不存在，只设置了 `rule_1`，则迁移会报错 `schema test doesn't exist`。

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

### 提取分库分表数据源信息写入合表

假设存在分库分表场景，需要将上游两个 MySQL 实例的表 `test_{11,12,13...}`.`t_{1,2,3...}` 迁移到下游 TiDB 的一张表 `test`.`t`，同时需要提取分库分表的源信息写入下游合表中，用于标识合表中各行数据的来源。

为了迁移到下游实例的表 `test`.`t`，需要创建和[分库分表合并场景](#分库分表合并)类似的表路由规则，并在其中增加 `extract-table`、`extract-schema`、`extract-source` 配置用于提取分库分表源数据信息：

- `extract-table`：对于匹配上 `schema-pattern` 和 `table-pattern` 的分表，DM 根据 `table-regexp` 提取分表，并将去除 `t_` 后的后缀信息写入合表的 `target-column`，即 `c_table` 列中。
- `extract-schema`：对于匹配上 `schema-pattern`和 `table-pattern` 的分库，DM 根据 `schema-regexp` 提取分库，并将去除 `test_` 后的后缀信息写入合表的 `target-column`，即 `c_schema` 列中。
- `extract-source`：对于匹配上 `schema-pattern` 和 `table-pattern` 的分表，DM 将其数据源信息写入合表的 `target-column`，即 `c_source` 列中。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

为了提取上游分表来源信息数据以写入到下游合表，**必须在启动迁移任务前手动**在下游创建好对应合表，合表需要包含用于存放分表源数据信息的三个扩展列 `target-column` （表名列、库名列、数据源列），扩展列**必须为表末尾列且必须为[字符串类型](/data-type-string.md)**。

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

例如，上游源数据为：

数据源 `mysql-01`:

```sql
mysql> select * from test_11.t_1;
+---+
| a |
+---+
| 1 |
+---+
mysql> select * from test_11.t_2;
+---+
| a |
+---+
| 2 |
+---+
mysql> select * from test_12.t_1;
+---+
| a |
+---+
| 3 |
+---+
```

数据源 `mysql-02`:

```sql
mysql> select * from test_13.t_3;
+---+
| a |
+---+
| 4 |
+---+
```

则 DM 同步后合表中的数据将为：

```sql
mysql> select * from test.t;
+---+---------+----------+----------+
| a | c_table | c_schema | c_source |
+---+---------+----------+----------+
| 1 | 1       | 11       | mysql-01 |
| 2 | 2       | 11       | mysql-01 |
| 3 | 1       | 12       | mysql-01 |
| 4 | 3       | 13       | mysql-02 |
+---+---------+----------+----------+
```

**错误的合表建表示例：**

> **注意：**
>
> 以下错误都可能导致分库分表数据源信息写入合表失败。

- `c-table` 列不在末尾

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int(11) PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

- `c-source` 列缺失

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

- `c_schema` 列为非 string 类型

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### 分库合并

假设存在分库场景，将上游两个 MySQL 实例 `test_{1,2,3...}`.`t_{1,2,3...}` 迁移到下游 TiDB 的 `test`.`t_{1,2,3...}`，创建一条路由规则即可：

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### 错误的表路由

假设存在下面两个路由规则，`test_1_bak`.`t_1_bak` 可以匹配上 `rule-1` 和 `rule-2`，违反 table 路由的限制而报错。

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
