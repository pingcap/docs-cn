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
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

在简单任务场景下，推荐使用通配符匹配库表名，但需注意以下版本差异：

+ 对于 v1.0.5 版及后续版本，表路由支持[通配符匹配](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)。但注意所有版本中通配符匹配中的 `*` 符号 **只能有一个，且必须在末尾**。
+ 对于 v1.0.5 以前的版本，表路由支持通配符，但不支持 `[...]` 与 `[!...]` 表达式。

## 参数解释

将根据 [`schema-pattern`/`table-pattern`](/dm/table-selector.md) 匹配上该规则的上游 MySQL/MariaDB 实例的表迁移到下游的 `target-schema`/`target-table`。

## 使用示例

下面展示了三个不同场景下的配置示例。如果你需要从小数据量分库分表 MySQL 合并迁移数据到 TiDB，请参考[这篇文档](/migrate-small-mysql-shards-to-tidb.md)

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
