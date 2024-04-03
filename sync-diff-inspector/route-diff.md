---
title: 不同库名或表名的数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/route-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/route-diff/']
summary: TiDB DM 等同步工具可以使用 route-rules 设置数据同步到下游指定表中。sync-diff-inspector 通过设置 rules 提供了校验不同库名、表名的表的功能。可以通过 rules 设置映射关系来简化配置，校验大量的不同库名或者表名的表。表路由的初始化和示例包括规则中存在 target-schema/target-table 表名为 schema.table 的行为，规则中只存在 target-schema 的行为，以及规则中不存在 target-schema.target-table 的行为。
---

# 不同库名或表名的数据校验

当你在使用 [TiDB DM](/dm/dm-overview.md) 等同步工具时，可以设置 `route-rules` 将数据同步到下游指定表中。sync-diff-inspector 通过设置 `rules` 提供了校验不同库名、表名的表的功能。

下面是一个简单的配置文件说明，要了解完整配置，请参考 [sync-diff-inspector 用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]
    
[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "t_1"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test_2"         # 目标库名
target-table = "t_2" # 目标表名
```

使用该配置会对下游的 `test_2.t_2` 与实例 `mysql1` 中的 `test_1.t_1` 进行校验。

如果需要校验大量的不同库名或者表名的表，也可以通过 `rules` 设置映射关系来简化配置。可以只配置 schema 或者 table 的映射关系，也可以都配置。例如上游库 `test_1` 中的所有表都同步到了下游的 `test_2` 库中，可以使用如下配置进行校验：

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]
    
[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "*"            # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test_2"       # 目标库名
target-table = "t_2"           # 目标表名
```

## Table Router 的初始化和示例

### Table Router 的初始化

- 如果规则中存在 `target-schema/target-table` 表名为 `schema.table`，sync-diff-inspector 的行为如下：

    - 如果存在一条规则将 `schema.table` 匹配到 `schema.table`，sync-diff-inspector 不做任何处理。
    - 如果不存在将 `schema.table` 匹配到 `schema.table` 的规则，sync-diff-inspector 会在表路由中添加一条新的规则 `schema.table -> _no__exists__db_._no__exists__table_`。之后，sync-diff-inspector 会将表 `schema.table` 视为表 `_no__exists__db_._no__exists__table_`。

- 如果规则中只存在 `target-schema`，如下所示：

    ```toml
    [routes.rule1]
    schema-pattern = "schema_2"  # 匹配数据源的库名，支持通配符 "*" 和 "?"
    target-schema = "schema"     # 目标库名 
    ```

    - 如果上游中不存在库 `schema`，sync-diff-inspector 不做任何处理。
    - 如果上游中存在库 `schema`，且存在一条规则将该库匹配到其他库，sync-diff-inspector 不做任何处理。
    - 如果上游中存在库 `schema`，但不存在将该库匹配到其他库的规则，sync-diff-inspector 会在表路由中添加一条新的规则 `schema -> _no__exists__db_`。之后，sync-diff-inspector 会将库 `schema` 视为库 `_no__exists__db_`。

- 如果规则中不存在 `target-schema.target-table`，sync-diff-inspector 会添加一条规则将 `target-schema.target-table` 匹配到 `target-schema.target-table`，使其大小写不敏感，因为表路由是大小写不敏感的。

### 示例

假设在上游集群中有下列七张表：

- `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1`
- `Inspector_mysql_1.Tb_emp1`

在配置示例中，上游集群有一条规则 `Source.rule1`，目标表为 `inspector_mysql_1.tb_emp1`。

#### 示例 1

如果配置如下：

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

那么路由结果如下：

- `inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `inspector_mysql_1.Tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.Tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`

#### 示例 2

如果配置如下：

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
target-schema = "inspector_mysql_1"
```

那么路由结果如下：

- `inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` 将被路由到 `inspector_mysql_1.Tb_emp1`
- `inspector_mysql_1.tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `inspector_mysql_1.Tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.Tb_emp1` 将被路由到 `_no__exists__db_._no__exists__table_`

#### 示例 3

如果配置如下：

```toml
[Source.rule1]
schema-pattern = "other_schema"
target-schema = "other_schema"
```

那么路由结果如下：

- `inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1` 将被路由到 `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1` 将被路由到 `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`

#### 示例 4

如果配置如下：

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_?"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

那么路由结果如下：

- `inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`

#### 示例 5

如果你不设置任何规则，那么路由结果如下：

- `inspector_mysql_0.tb_emp1` 将被路由到 `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1` 将被路由到 `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1` 将被路由到 `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` 将被路由到 `inspector_mysql_1.tb_emp1`
