---
title: 第三方工具的已知兼容性问题
summary: 描述在测试中发现的 TiDB 与第三方工具的兼容性问题。
---

# 第三方工具的已知兼容性问题

> **注意：**
>
> [不支持的特性](/mysql-compatibility.md#unsupported-features) 部分列出了 TiDB 中不支持的特性，包括：
>
> - 存储过程和函数
> - 触发器
> - 事件
> - 用户自定义函数
> - `SPATIAL` 函数、数据类型和索引
> - `XA` 语法
>
> 上述不支持的特性是预期行为，本文档中不再列出。更多详情，请参阅 [MySQL 兼容性](/mysql-compatibility.md)。

本文档列出了在一些 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-tools-compatibility.md) 中发现的兼容性问题。

## 一般兼容性问题

### `SELECT CONNECTION_ID()` 在 TiDB 中返回 64 位整数

**描述**

`SELECT CONNECTION_ID()` 函数在 TiDB 中返回 64 位整数，如 `2199023260887`，而在 MySQL 中返回 32 位整数，如 `391650`。

**规避方法**

在 TiDB 应用程序中，为避免数据溢出，应使用 64 位整数或字符串类型来存储 `SELECT CONNECTION_ID()` 的结果。例如，在 Java 中可以使用 `Long` 或 `String`，在 JavaScript 或 TypeScript 中使用 `string`。

### TiDB 不维护 `Com_*` 计数器

**描述**

MySQL 维护一系列以 `Com_` 开头的[服务器状态变量](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)，用于跟踪自上次启动以来对数据库执行的操作总数。例如，`Com_select` 记录了 MySQL 自启动以来发起的 `SELECT` 语句总数（即使语句未成功查询）。TiDB 不维护这些变量。你可以使用语句 [<code>SHOW GLOBAL STATUS LIKE 'Com_%'</code>](/sql-statements/sql-statement-show-status.md) 查看 TiDB 和 MySQL 之间的差异。

**规避方法**

<CustomContent platform="tidb">

不要使用这些变量。一个常见场景是监控。TiDB 具有良好的可观察性，不需要从服务器状态变量中查询。对于自定义监控工具，请参考 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

不要使用这些变量。一个常见场景是监控。TiDB Cloud 具有良好的可观察性，不需要从服务器状态变量中查询。有关 TiDB Cloud 监控服务的更多信息，请参考[监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)。

</CustomContent>

### TiDB 在错误消息中区分 `TIMESTAMP` 和 `DATETIME`

**描述**

TiDB 错误消息区分 `TIMESTAMP` 和 `DATETIME`，而 MySQL 不区分，都返回为 `DATETIME`。也就是说，MySQL 错误地将 `TIMESTAMP` 类型的错误消息转换为 `DATETIME` 类型。

**规避方法**

<CustomContent platform="tidb">

不要使用错误消息进行字符串匹配。相反，使用[错误码](/error-codes.md)进行故障排除。

</CustomContent>

<CustomContent platform="tidb-cloud">

不要使用错误消息进行字符串匹配。相反，使用[错误码](https://docs.pingcap.com/tidb/stable/error-codes)进行故障排除。

</CustomContent>

### TiDB 不支持 `CHECK TABLE` 语句

**描述**

TiDB 不支持 `CHECK TABLE` 语句。

**规避方法**

要检查数据和相应索引的一致性，可以在 TiDB 中使用 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句。

## MySQL JDBC 兼容性

测试版本为 MySQL Connector/J 8.0.29。

### 默认排序规则不一致

**描述**

MySQL Connector/J 的排序规则存储在客户端，并根据服务器版本进行区分。

下表列出了已知的客户端和服务器端字符集排序规则不一致：

| 字符集 | 客户端默认排序规则 | 服务器端默认排序规则 |
| --------- | -------------------- | ------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`   |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`  |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**规避方法**

手动设置排序规则，不要依赖客户端默认排序规则。客户端默认排序规则由 MySQL Connector/J 配置文件存储。

### `NO_BACKSLASH_ESCAPES` 参数不生效

**描述**

在 TiDB 中，如果不转义 `\` 字符，则无法使用 `NO_BACKSLASH_ESCAPES` 参数。更多详情，请跟踪此 [issue](https://github.com/pingcap/tidb/issues/35302)。

**规避方法**

在 TiDB 中不要将 `NO_BACKSLASH_ESCAPES` 与 `\` 一起使用，而是在 SQL 语句中使用 `\\`。

### 不支持 `INDEX_USED` 相关参数

**描述**

TiDB 不在协议中设置 `SERVER_QUERY_NO_GOOD_INDEX_USED` 和 `SERVER_QUERY_NO_INDEX_USED` 参数。这将导致以下参数返回的结果与实际情况不一致：

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**规避方法**

在 TiDB 中不要使用 `noIndexUsed()` 和 `noGoodIndexUsed()` 函数。

### 不支持 `enablePacketDebug` 参数

**描述**

TiDB 不支持 [enablePacketDebug](https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-debugging-profiling.html) 参数。这是一个用于调试的 MySQL Connector/J 参数，它会保留数据包的缓冲区。这可能导致连接意外关闭。**不要**启用它。

**规避方法**

在 TiDB 中不要设置 `enablePacketDebug` 参数。

### 不支持 UpdatableResultSet

**描述**

TiDB 不支持 `UpdatableResultSet`。**不要**指定 `ResultSet.CONCUR_UPDATABLE` 参数，**不要**在 `ResultSet` 内更新数据。

**规避方法**

要通过事务确保数据一致性，可以使用 `UPDATE` 语句更新数据。

## MySQL JDBC 错误

### `useLocalTransactionState` 和 `rewriteBatchedStatements` 同时为 true 会导致事务提交或回滚失败

**描述**

使用 MySQL Connector/J 8.0.32 或更早版本时，如果 `useLocalTransactionState` 和 `rewriteBatchedStatements` 参数同时设置为 `true`，事务可能无法提交。你可以使用[此代码](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)复现。

**规避方法**

> **注意：**
>
> `useConfigs=maxPerformance` 包含一组配置。有关 MySQL Connector/J 8.0 和 MySQL Connector/J 5.1 中的详细配置，请参阅 [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 和 [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)。使用 `maxPerformance` 时需要禁用 `useLocalTransactionState`。即使用 `useConfigs=maxPerformance&useLocalTransactionState=false`。

此错误已在 MySQL Connector/J 8.0.33 中修复。考虑到 8.0.x 系列的更新已停止，强烈建议将 MySQL Connector/J 升级到[最新的正式发布（GA）版本](https://dev.mysql.com/downloads/connector/j/)以提高稳定性和性能。

### 连接器与 5.7.5 之前的服务器版本不兼容

**描述**

使用 MySQL Connector/J 8.0.31 或更早版本时，如果 MySQL 服务器 < 5.7.5 或使用 MySQL 服务器 < 5.7.5 协议的数据库（如 TiDB v6.3.0 之前的版本），数据库连接可能在某些条件下挂起。更多详情，请参阅[错误报告](https://bugs.mysql.com/bug.php?id=106252)。

**规避方法**

此错误已在 MySQL Connector/J 8.0.32 中修复。考虑到 8.0.x 系列的更新已停止，强烈建议将 MySQL Connector/J 升级到[最新的正式发布（GA）版本](https://dev.mysql.com/downloads/connector/j/)以提高稳定性和性能。

TiDB 也通过以下方式修复了这个问题：

- 客户端：此错误已在 **pingcap/mysql-connector-j** 中修复，你可以使用 [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j) 替代官方的 MySQL Connector/J。
- 服务器端：此兼容性问题已在 TiDB v6.3.0 中修复，你可以将服务器升级到 v6.3.0 或更高版本。

## Sequelize 兼容性

本节描述的兼容性信息基于 [Sequelize v6.32.1](https://www.npmjs.com/package/sequelize/v/6.32.1)。

根据测试结果，TiDB 支持大多数 Sequelize 功能（[使用 `MySQL` 作为方言](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql)）。

不支持的功能包括：

- 不支持 [`GEOMETRY`](https://github.com/pingcap/tidb/issues/6347)。
- 不支持修改整数主键。
- 不支持 `PROCEDURE`。
- 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` [隔离级别](/system-variables.md#transaction_isolation)。
- 默认不允许修改列的 `AUTO_INCREMENT` 属性。
- 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。
- 不支持 `sequelize.queryInterface.showIndex(Model.tableName);`。
- 不支持 `sequelize.options.databaseVersion`。
- 不支持使用 [`queryInterface.addColumn`](https://sequelize.org/api/v6/class/src/dialects/abstract/query-interface.js~queryinterface#instance-method-addColumn) 添加外键引用。

### 不支持修改整数主键

**描述**

不支持修改整数主键。如果主键是整数类型，TiDB 使用主键作为数据组织的索引。参考 [Issue #18090](https://github.com/pingcap/tidb/issues/18090) 和[聚簇索引](/clustered-indexes.md)了解更多详情。

### 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别

**描述**

TiDB 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别。如果将隔离级别设置为 `READ-UNCOMMITTED` 或 `SERIALIZABLE`，TiDB 会抛出错误。

**规避方法**

仅使用 TiDB 支持的隔离级别：`REPEATABLE-READ` 或 `READ-COMMITTED`。

如果你希望 TiDB 与设置了 `SERIALIZABLE` 隔离级别但不依赖 `SERIALIZABLE` 的其他应用程序兼容，可以将 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check) 设置为 `1`。在这种情况下，TiDB 会忽略不支持的隔离级别错误。

### 默认不允许修改列的 `AUTO_INCREMENT` 属性

**描述**

默认情况下，不允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 命令添加或删除列的 `AUTO_INCREMENT` 属性。

**规避方法**

参考 [`AUTO_INCREMENT` 的限制](/auto-increment.md#restrictions)。

要允许删除 `AUTO_INCREMENT` 属性，请将 `@@tidb_allow_remove_auto_inc` 设置为 `true`。

### 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引

**描述**

不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
