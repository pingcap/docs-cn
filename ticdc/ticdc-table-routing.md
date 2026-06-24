---
title: TiCDC 表路由
summary: 了解 TiCDC 新架构中的表路由配置，包括通过 target-schema 和 target-table 改写下游 schema 和表名、冲突检测、DDL 改写、限制和排查方法。
---

# TiCDC 表路由

TiCDC 表路由 (Table Routing) 允许你通过 changefeed 配置，将上游表映射到指定的下游库名或表名。该功能仅适用于 [TiCDC 新架构](/ticdc/ticdc-architecture.md)，不支持 [TiCDC 老架构](/ticdc/ticdc-classic-architecture.md)。

表路由只会改变 TiCDC 输出到下游的库名和表名，不会改变行数据、列名、表结构、表过滤规则、Topic 分发规则、Partition 分发规则或列选择规则。

## 使用场景

表路由适用于以下场景：

- 将 `sales.orders` 同步到 `archive.sales_orders`，或同步到符合其他下游命名规范的表。
- 将多个源库同步到同一个下游命名空间，同时保持目标表名唯一，例如将 `tenant_001.orders` 同步到 `tenant_mirror.tenant_001_orders`。
- 构建迁移、容灾、归档或影子 Changefeed，避免写入与上游同名的下游对象。
- 向 MQ 消费端或存储服务消费端暴露稳定的库表名。

> **注意：**
>
> 表路由仅支持一对一的表名映射，不支持将多张上游表合并到一张下游表。
> 表路由不支持将一张上游表拆分到多张下游表，或转换行数据内容。

## 配置表路由

配置前，请先启用 TiCDC 新架构。详情参见 [`newarch`](/ticdc/ticdc-server-config.md#newarch-从-v854-release1-版本开始引入)。

以下示例将 `sales.orders` 路由到 `archive.sales_orders`：

```toml
[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

Changefeed 启动后，`sales.orders` 的 DML 和 DDL 事件会写入下游的 `archive.sales_orders`。

> **注意：**
>
> 同一个上游库中的不同表可以路由到不同的目标库。此类配置只适用于 DML 和表级 DDL。
>
> 对于 `CREATE DATABASE`、`DROP DATABASE` 和 `ALTER DATABASE` 这类库级 DDL，TiCDC 必须能从路由规则中确定唯一目标库，否则该 DDL 会同步失败。
> 如果一个上游数据库映射到多个下游目标数据库，应提前创建下游目标库，或确保上游不会产生需要自动同步的库级 DDL。

## 配置字段

表路由功能使用 `sink.dispatchers` 作为配置入口。

| 字段 | 描述 |
| :--- | :--- |
| `matcher` | 匹配上游库表。语法与[表库过滤语法](/table-filter.md#表库过滤语法)相同，包括 `sales.*` 这类通配符匹配，以及 `!sales.tmp_*` 这类排除匹配。 |
| `target-schema` | 指定下游库名。如果不设置该字段，TiCDC 保持上游库名不变。 |
| `target-table` | 指定下游表名。如果不设置该字段，TiCDC 保持上游表名不变。 |

匹配行为如下：

- 只有设置了 `target-schema` 或 `target-table` 的 dispatcher 规则才会参与表路由。
- 如果一张表匹配多条表路由规则，`sink.dispatchers` 中第一条匹配的规则生效。
- `matcher` 始终匹配上游库表名，而不是路由后的目标库表名。
- Changefeed 配置项 `case-sensitive` 只影响表路由的 `matcher` 是否大小写敏感，不会改写 `{schema}` 和 `{table}` 的展开结果。详情参见 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive)。

### 占位符

你可以在 `target-schema` 和 `target-table` 中使用以下占位符：

| 占位符 | 描述 |
| :--- | :--- |
| `{schema}` | 上游库名，保留实际匹配到的库名大小写。 |
| `{table}` | 上游表名，保留实际匹配到的表名大小写。 |

`target-schema` 和 `target-table` 的值只能包含字面文本、`{schema}` 和 `{table}`。如果使用 `{db}` 这类未知占位符，TiCDC 会拒绝该 Changefeed 配置，并返回 `CDC:ErrInvalidTableRoutingRule` 错误。

以源表 `sales.orders` 为例：

| 配置 | 目标表 |
| :--- | :--- |
| `target-schema = "archive"` | `archive.orders` |
| `target-table = "{table}_bak"` | `sales.orders_bak` |
| `target-schema = "{schema}_mirror"` | `sales_mirror.orders` |
| `target-schema = "archive"` 和 `target-table = "{schema}_{table}"` | `archive.sales_orders` |

## 示例

### 路由一个库中的所有表

以下配置将 `sales` 库中的所有表路由到 `archive` 库，并在目标表名后追加 `_bak`：

```toml
[filter]
rules = ["sales.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_bak"
```

路由结果示例如下：

- `sales.orders` 会路由到 `archive.orders_bak`。
- `sales.order_items` 会路由到 `archive.order_items_bak`。

### 将多个库路由到同一个目标库

将多个库路由到同一个目标库时，建议在 `target-table` 中包含 `{schema}`，以确保目标表名唯一。

```toml
[filter]
rules = ["sales.*", "crm.*", "finance.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*", "crm.*", "finance.*"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

路由结果示例如下：

- `sales.orders` 会路由到 `archive.sales_orders`。
- `crm.orders` 会路由到 `archive.crm_orders`。
- `finance.orders` 会路由到 `archive.finance_orders`。

> **注意：**
>
> 该配置场景是合库，不是合表。本功能不支持把多个不同库的同名表合并到一个下游数据表中。

### 同时使用表路由和 Kafka Sink Topic、Partition 分发器

同一条 dispatcher 规则可以同时包含表路由字段和已有分发字段：

```toml
[filter]
rules = ["sales.orders"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
topic = "order-events"
partition = "index-value"
target-schema = "public"
target-table = "orders"
```

在以上示例中，表路由将下游数据中暴露的库表名改为 `public.orders`。

表路由不会改变 Topic 或 Partition 的分发结果，`topic` 和 `partition` 分发器仍然使用上游表 `sales.orders` 进行匹配和分发计算。

## 输出行为

| Sink | 行为 |
| :--- | :--- |
| MySQL Sink | DDL 和 DML 语句会写入路由后的目标库表。开启 Redo 功能时，执行 `redo apply` 会将事件回放到路由后的目标表。 |
| Kafka Sink 和 Pulsar Sink | 协议 `payload` 和 DDL `query` 使用路由后的目标库表名；编码协议里的 `schema`、`table` 字段值也是路由后的目标库表。 |
| Cloud Storage Sink | 根据路由后的目标库表名输出对应的存储路径、schema 文件、表定义文件和数据文件。 |

## DDL 行为

启用表路由后，TiCDC 会改写 DDL 语句，使结构化 DDL 字段和 SQL 文本使用一致的目标名。

例如，如果配置以下规则：

```toml
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_routed"
```

TiCDC 会将以下上游 DDL：

```sql
RENAME TABLE `sales`.`temp_table` TO `sales`.`renamed_table`;
```

路由为以下下游 DDL：

```sql
RENAME TABLE `archive`.`temp_table_routed` TO `archive`.`renamed_table_routed`;
```

如果 DDL 语句中包含表引用，且这些表引用匹配表路由规则，TiCDC 也会改写被引用的表名。例如，`CREATE VIEW` 语句中的表引用，以及 `ALTER TABLE` 语句中的外键引用都可以被路由。

对于 `CREATE DATABASE`、`DROP DATABASE` 和 `ALTER DATABASE ... CHARACTER SET/COLLATE` 这类库级 DDL，如果库名匹配表路由规则，TiCDC 会改写库名。**如果同一个上游库匹配多条表路由规则，但这些规则解析出不同的目标库名，TiCDC 无法为该库级 DDL 确定唯一目标库，Changefeed 会报表路由错误。**

创建或更新 Changefeed 时，TiCDC 会基于当前复制范围内的表检查目标表冲突。运行期间，TiCDC 会在同步 `CREATE TABLE`、`RENAME TABLE`、`DROP TABLE`、`DROP DATABASE` 等 DDL 时更新冲突检测状态。库级 DDL 是否能唯一路由，会在同步对应 DDL 时判断。

## 路由冲突检测

当两个不同的上游表被路由到同一个下游 `(schema, table)` 时，会发生路由冲突。TiCDC 不支持将多张上游表合并到同一张下游表。

例如，以下配置可能导致冲突：

```toml
[filter]
rules = ["sales.*", "crm.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}"

[[sink.dispatchers]]
matcher = ["crm.*"]
target-schema = "archive"
target-table = "{table}"
```

如果 `sales.orders` 和 `crm.orders` 都在复制范围内，这两张表都会被路由到 `archive.orders`。TiCDC 会拒绝创建或更新 Changefeed，并返回 `CDC:ErrTableRouteConflict` 错误。

Changefeed 运行期间，如果 `CREATE TABLE` 或 `RENAME TABLE` 等 DDL 使两个存活的上游表路由到同一个目标表，Changefeed 会失败并返回 `CDC:ErrTableRouteConflict` 错误。

如果上游表被删除或重命名，TiCDC 会释放旧源表名占用的目标表。之后新源表名可以使用同一个目标表，前提是同一时刻没有两个存活的上游表路由到该目标表。

> **警告：**
>
> 路由冲突检测仅限于单个 Changefeed。如果多个 Changefeed 写入同一个下游系统，请确保这些 Changefeed 的表路由规则不会写入相同的目标对象。

## 故障排查

| 现象 | 可能原因 | 解决方法 |
| :--- | :--- | :--- |
| 创建 Changefeed 时报 `CDC:ErrInvalidTableRoutingRule` 错误。 | `target-schema` 或 `target-table` 包含无效占位符或无效的大括号。 | 只使用字面文本、`{schema}` 和 `{table}`。 |
| MQ Topic 名仍然使用上游库表名。 | 表路由不会改变 Topic 或 Partition 分发。 | 如果需要修改 Topic 名，请在 `sink.dispatchers` 中单独配置 `topic`。 |
| DDL 语句报 `CDC:ErrTableRoutingFailed` 错误。 | 该 DDL 语句无法安全地用于表路由改写，或库级别路由存在歧义。 | 调整路由规则。 |
| Changefeed 运行中失败并报 `CDC:ErrTableRouteConflict` 错误。 | 新建表或重命名表后，两个不同的上游表被路由到同一个下游表。 | 调整表路由规则或上游 DDL，确保单个 Changefeed 内每个目标表只对应一个存活的上游表。 |

## 相关文档

- [TiCDC Changefeed 命令行参数和配置参数](/ticdc/ticdc-changefeed-config.md)
- [Changefeed 日志过滤器](/ticdc/ticdc-filter.md)
- [同步数据到 MySQL 兼容数据库](/ticdc/ticdc-sink-to-mysql.md)
- [同步数据到 Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [同步数据到 Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [同步数据到存储服务](/ticdc/ticdc-sink-to-cloud-storage.md)
