---
title: TiCDC 表路由
summary: 了解如何配置 TiCDC 表路由，通过 target-schema 和 target-table 改写下游 schema 和表名，同时保持现有 topic、partition 等分发规则不变，并掌握冲突检测、DDL 改写、限制和排查方法。
---

# TiCDC 表路由

TiCDC 表路由 (Table Routing) 允许你在 `sink.dispatchers` 中添加 `target-schema` 和 `target-table`，将上游表映射到指定的下游库名或表名。当下游命名规范与上游命名规范不一致时，例如需要将数据同步到归档库、影子库，或需要在共享下游系统中保证目标表名唯一时，可以使用表路由。

表路由只会改变 TiCDC 输出到下游的库名和表名，不会改变行数据、列名、表结构、表过滤规则、Topic 分发规则、Partition 分发规则或列选择规则。

## 使用场景

表路由适用于以下场景：

- 将 `sales.orders` 同步到 `archive.sales_orders`，或同步到符合其他下游命名规范的表。
- 将多个源库同步到同一个下游命名空间，同时保持目标表名唯一，例如将 `tenant_001.orders` 同步到 `tenant_mirror.tenant_001_orders`。
- 构建迁移、容灾、归档或影子 Changefeed，避免写入与上游同名的下游对象。
- 向 MQ 消费端或存储服务消费端暴露稳定的库表名，同时不改变现有 Topic、Partition 或存储服务 Sink 配置。

表路由不适用于将多张上游表合并到一张下游表、将一张上游表拆分到多张下游表，或转换行数据内容。

## 配置表路由

1. 准备下游环境。

    确保 TiCDC 具备所需的下游权限。如果 Changefeed 从上游库表创建之后开始同步，需要手动创建兼容的目标库表。如果 Changefeed 能捕获对应的上游 DDL 事件，TiCDC 会将 DDL 语句路由到目标名。

2. 创建 Changefeed 配置文件。

    以下示例将 `sales.orders` 路由到 `archive.sales_orders`：

    ```toml
    [filter]
    rules = ["sales.orders"]

    [sink]
    [[sink.dispatchers]]
    matcher = ["sales.orders"]
    target-schema = "archive"
    target-table = "{schema}_{table}"
    ```

3. 使用该配置文件创建 Changefeed。

    ```shell
    cdc cli changefeed create \
        --server=http://127.0.0.1:8300 \
        --changefeed-id="table-route-demo" \
        --sink-uri="mysql://root:password@127.0.0.1:3306/" \
        --config=changefeed.toml
    ```

Changefeed 启动后，`sales.orders` 的 DML 和 DDL 事件会写入下游的 `archive.sales_orders`。

## 配置字段

表路由复用 `sink.dispatchers` 作为配置入口。你可以使用 `dispatchers = [...]` 写法，也可以使用 `[[sink.dispatchers]]` 写法。

| 字段 | 描述 |
| :--- | :--- |
| `matcher` | 匹配上游库表。语法与[表库过滤语法](/table-filter.md#表库过滤语法)相同，包括 `sales.*` 这类通配符匹配，以及 `!sales.tmp_*` 这类排除匹配。 |
| `target-schema` | 指定下游库名。如果不设置该字段，TiCDC 保持上游库名不变。 |
| `target-table` | 指定下游表名。如果不设置该字段，TiCDC 保持上游表名不变。 |

匹配行为如下：

- 只有设置了 `target-schema` 或 `target-table` 的 dispatcher 规则才会参与表路由。
- 如果一张表匹配多条表路由规则，`sink.dispatchers` 中第一条匹配的规则生效。
- `matcher` 始终匹配上游库表名，而不是路由后的目标库表名。
- Changefeed 配置项 `case-sensitive` 也会影响表路由的 matcher。详情参见 [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive)。

### 占位符

你可以在 `target-schema` 和 `target-table` 中使用以下占位符：

| 占位符 | 描述 |
| :--- | :--- |
| `{schema}` | 上游库名。 |
| `{table}` | 上游表名。 |

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

### 同时使用表路由和 Topic、Partition 分发器

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

在以上示例中，表路由将下游数据中暴露的库表名改为 `public.orders`。`topic` 和 `partition` 分发器仍然使用上游表 `sales.orders` 进行匹配和分发计算。

## 输出行为

表路由对各类 Sink 输出的影响如下：

| Sink 类型 | 输出行为 |
| :--- | :--- |
| MySQL 兼容数据库和 TiDB | DML 事件会写入目标库表。DDL 语句会被改写为作用于目标对象。 |
| Kafka | 表示库名或表名的消息 payload 字段使用目标名。DDL 消息字段和 DDL 查询文本使用目标名。Topic 和 Partition 分发仍然使用上游名。 |
| Pulsar | Canal-JSON payload 中表示库名或表名的字段使用目标名。Topic 和 Partition 分发仍然使用上游名。 |
| 存储服务 | 存储路径、schema 文件、表定义文件和数据文件使用目标库表名。 |
| Redo log | Redo 记录保留目标库表名。执行 redo apply 时，事件会回放到路由后的目标对象。 |

对于 MQ Sink，表路由不会改变 Topic 或 Partition 的分发结果。例如，如果配置了 `topic = "{schema}_{table}"`，且源表为 `sales.orders`，即使 payload 中的表名被路由到 `archive.sales_orders`，TiCDC 仍然会将该事件分发到 `sales_orders` Topic。

## DDL 行为

启用表路由后，TiCDC 会改写 TiDB parser 支持的 DDL 语句，使结构化 DDL 字段和 SQL 文本使用一致的目标名。

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

对于 `CREATE DATABASE` 和 `DROP DATABASE` 这类库级别 DDL，如果库名匹配表路由规则，TiCDC 会改写库名。如果同一个上游库匹配多条表路由规则，但这些规则解析出不同的目标库名，TiCDC 无法为该库级别 DDL 确定唯一目标库，Changefeed 会报表路由错误。

> **注意：**
>
> 表路由的 DDL 改写依赖 TiDB parser 支持。如果 TiCDC 无法为表路由安全地解析和恢复某条 DDL 语句，Changefeed 会返回 `CDC:ErrTableRoutingFailed` 错误，而不会静默地将原始 DDL 发送到下游。TiCDC 识别为全文索引或混合索引的 DDL 语句不会被路由。

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

TiCDC 也会检测 Changefeed 启动后出现的冲突。例如，通配符规则开始复制一张新建表，或者 `RENAME TABLE` 语句改变了源表名，且新的路由结果与已有目标表冲突时，Changefeed 会进入 Failed 状态，并返回 `CDC:ErrTableRouteConflict`。

> **警告：**
>
> 路由冲突检测仅限于单个 Changefeed。如果多个 Changefeed 写入同一个下游系统，请确保这些 Changefeed 的表路由规则不会写入相同的目标对象。

## 限制

- 表路由仅支持一对一的表名映射，不支持将多张上游表合并到一张下游表。
- 表路由不会转换行数据、列名、列类型或表结构。
- `filter.rules`、`matcher`、`topic`、`partition` 和 `columns` 仍然使用上游库表名。
- 移除表路由配置或回退 TiCDC 版本，不会重命名已写入的下游表、移动已写入的存储文件、改写已发送的 MQ 消息，或清理已经按目标名生成的 redo log。
- 如果上游和下游位于同一个数据库实例，请确保路由后的目标库不在同一个 Changefeed 的复制范围内。否则，该 Changefeed 可能会复制自己写入下游的数据。

## 故障排查

| 现象 | 可能原因 | 解决方法 |
| :--- | :--- | :--- |
| 创建 Changefeed 时报 `CDC:ErrInvalidTableRoutingRule` 错误。 | `target-schema` 或 `target-table` 包含无效占位符或无效的大括号。 | 只使用字面文本、`{schema}` 和 `{table}`。 |
| 创建、更新 Changefeed 或运行时复制报 `CDC:ErrTableRouteConflict` 错误。 | 两张上游表被路由到同一个下游库表。 | 修改路由规则，确保每张上游表映射到唯一的目标表。例如，在 `target-table` 中添加 `{schema}`。 |
| MQ Topic 名仍然使用上游库表名。 | 表路由不会改变 Topic 或 Partition 分发。 | 如果需要修改 Topic 名，请在 `sink.dispatchers` 中单独配置 `topic`。 |
| DDL 语句报 `CDC:ErrTableRoutingFailed` 错误。 | 该 DDL 语句无法安全地用于表路由改写，或库级别路由存在歧义。 | 调整路由规则，过滤掉不支持的 DDL，或在下游手动处理该 DDL。 |

## 相关文档

- [TiCDC Changefeed 命令行参数和配置参数](/ticdc/ticdc-changefeed-config.md)
- [Changefeed 日志过滤器](/ticdc/ticdc-filter.md)
- [同步数据到 MySQL 兼容数据库](/ticdc/ticdc-sink-to-mysql.md)
- [同步数据到 Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [同步数据到 Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [同步数据到存储服务](/ticdc/ticdc-sink-to-cloud-storage.md)
