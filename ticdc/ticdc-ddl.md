---
title: Changefeed DDL 同步
summary: 了解 TiCDC 支持同步的 DDL 和一些特殊情况
---

# Changefeed DDL 同步

本文档介绍了 TiCDC 同步 DDL 的规则和特殊情况。

## DDL 白名单

目前 TiCDC 在同步 DDL 时使用白名单策略，只有在白名单中的 DDL 操作才会被同步到下游系统，不在白名单中的 DDL 操作将不会被 TiCDC 同步。

此外，TiCDC 会根据表中是否具有[有效索引](/ticdc/ticdc-overview.md#有效索引)以及配置项 [`force-replicate`](/ticdc/ticdc-changefeed-config.md#force-replicate) 是否为 `true` 来决定是否将 DDL 同步到下游。当 `force-replicate=true` 时，同步任务会尝试强制[同步没有有效索引的表](/ticdc/ticdc-manage-changefeed.md#同步没有有效索引的表)。

以下为 TiCDC 支持同步的 DDL 的列表。该表中出现的缩写字母含义如下：

- Y：在该条件下可以同步到下游。
- N：在该条件下不会同步到下游。

> **注意：** 
>
> - 当上游表不存在有效索引，且未配置 `force-replicate=true` 时，该表不会被同步，但是之后在该表上创建有效索引的 DDL (`CREATE INDEX`、`ADD INDEX` 和 `ADD PRIMARY KEY`）会被同步，下游表和上游表结构可能产生不一致从而导致后续数据同步失败。
> - 删除最后一个有效索引的 DDL（`DROP INDEX` 和 `DROP PRIMARY KEY`）不会被同步，并且导致后续数据同步失败。

| DDL | 存在有效索引 | 无有效索引且 `force-replicate` 为默认值 `false`  | 无有效索引且 `force-replicate` 为 `true` |
|---|:---:|:---:| :---: |
| `CREATE DATABASE` | Y | Y | Y |
| `DROP DATABASE` | Y | Y | Y |
| `ALTER DATABASE CHARACTER SET` | Y | Y | Y |
| `CREATE INDEX` | Y | Y | Y |
| `ADD INDEX` | Y | Y | Y |
| `DROP INDEX` | Y | N | Y |
| `ADD PRIMARY KEY` | Y | Y | Y |
| `DROP PRIMARY KEY` | Y | N | Y |
| `CREATE TABLE` | Y | N | Y |
| `DROP TABLE` | Y | N | Y |
| `ADD COLUMN` | Y | N | Y |
| `DROP COLUMN` | Y | N | Y |
| `TRUNCATE TABLE` | Y | N | Y |
| `MODIFY COLUMN` | Y | N | Y |
| `RENAME TABLE` | Y | N | Y |
| `ALTER COLUMN DEFAULT VALUE` | Y | N | Y |
| `ALTER TABLE COMMENT` | Y | N | Y |
| `RENAME INDEX` | Y | N | Y |
| `ADD PARTITION` | Y | N | Y |
| `DROP PARTITION` | Y | N | Y |
| `TRUNCATE PARTITION` | Y | N | Y |
| `CREATE VIEW` | Y | N | Y |
| `DROP VIEW` | Y | N | Y |
| `ALTER TABLE CHARACTER SET` | Y | N | Y |
| `RECOVER TABLE` | Y | N | Y |
| `REBASE AUTO ID` | Y | N | Y |
| `ALTER TABLE INDEX VISIBILITY` | Y | N | Y |
| `EXCHANGE PARTITION` | Y | N | Y |
| `REORGANIZE PARTITION` | Y | N | Y |
| `ALTER TABLE TTL` | Y | N | Y |
| `ALTER TABLE REMOVE TTL` | Y | N | Y |

## DDL 同步注意事项

### 创建和添加索引 DDL 的异步执行

虽然 TiCDC 在大多数情况下会按顺序同步 DDL，但如果下游是 TiDB，TiCDC 会异步执行创建和添加索引的 DDL 操作，即 TiCDC 将 `ADD INDEX` 和 `CREATE INDEX` DDL 同步到下游执行后，会立刻返回，而不会等待 DDL 操作完成。这样可以减小对 Changefeed 同步延迟的影响，避免阻塞后续的 DML 执行。

当 `ADD INDEX` 或 `CREATE INDEX` DDL 操作在下游执行期间，TiCDC 执行同一张表的下一条 DDL 时，这条 DDL 可能长期被阻塞在 `queueing` 状态，导致其被 TiCDC 重复执行多次，重试时间过长时还会导致同步任务失败。从 v8.4.0 开始，如果拥有下游数据库的 `SUPER` 权限，TiCDC 会定期执行 `ADMIN SHOW DDL JOBS` 查询异步执行的 DDL 任务的状态，等到索引创建完成后再继续同步。这期间虽然同步任务的延迟会加剧，但避免了同步任务失败的问题。

> **注意：**
>
> - 如果下游 DML 的执行依赖于未完成同步的索引，DML 可能会执行得很慢，进而影响 TiCDC 的同步延迟。
> - 在同步 DDL 到下游之前，如果 TiCDC 节点宕机或者下游有其他写操作，该 DDL 存在极低的失败概率，你可以自行检查。

### Rename table 类型的 DDL 注意事项

TiCDC 根据重命名前后的库表名和过滤规则决定是否同步 Rename DDL。以下示例假设表满足同步要求，且未配置额外的 DDL 事件过滤规则。

#### 一条 DDL 语句内 rename 单个表

如果一条 DDL 语句重命名单个表，则只有旧表名符合过滤规则时，TiCDC 才会同步该 DDL 语句。下面使用具体示例进行说明。

假设你的 changefeed 的配置文件如下：

```toml
[filter]
rules = ['test.t*']
```

那么，TiCDC 对该类型 DDL 的处理行为如下表所示：

| DDL | 是否同步 | 原因和处理方式 |
| --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2` | 同步 | test.t1 符合 filter 规则 |
| `RENAME TABLE test.t1 TO ignore.t1` | 同步 | test.t1 符合 filter 规则 |
| `RENAME TABLE ignore.t1 TO ignore.t2` | 忽略 | ignore.t1 不符合 filter 规则 |
| `RENAME TABLE test.n1 TO test.t1` | 报错，并停止同步。 | 旧表名 test.n1 不符合 filter 规则，但是新表名 test.t1 符合 filter 规则，这是非法操作。请参考错误提示信息进行处理 |
| `RENAME TABLE ignore.t1 TO test.t1` | 报错，并停止同步。 | 理由同上 |

以上规则适用于新老架构。如果旧表名匹配过滤规则而新表名不匹配，TiCDC 会同步 Rename DDL，随后停止同步该表的后续数据变更，不会额外向下游发送 `DROP TABLE`。如果旧表名不匹配而新表名匹配，TiCDC 会报 `CDC:ErrSyncRenameTableFailed` 错误，因为仅同步 Rename 无法补齐该表此前未同步的数据。

#### 一条 DDL 语句内 rename 多个表

如果一条 DDL 语句重命名多个表，新架构会按单表 Rename 的规则逐个判断：旧表名匹配时同步对应的重命名步骤；新旧表名均不匹配时忽略该步骤；旧表名不匹配而新表名匹配时，Changefeed 会报错并停止同步。老架构还要求需要同步的重命名步骤的目标库位于同步范围内，并且不支持同步互换表名的 Rename DDL。

假设你的 changefeed 的配置文件如下：

```toml
[filter]
rules = ['test.t*']
```

那么，TiCDC 对该类型的处理行为如下表所示：

| DDL | 老架构 | 新架构 | 原因 |
| --- | --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4` | 同步 | 同步 | 新旧库表名均匹配过滤规则 |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2` | 同步 | 同步 | 旧表名和目标库匹配过滤规则。同步 Rename 后，停止同步改名后的表 |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22` | 报错 | 同步 | 目标库 `ignore` 不在同步范围内。新架构同步 Rename 后，停止同步 `ignore.t1`，继续同步 `test.t22` |
| `RENAME TABLE test.t1 TO test.t2, ignore.t1 TO ignore.t2` | 仅同步 `test.t1` 的重命名步骤 | 仅同步 `test.t1` 的重命名步骤 | `ignore.t1` 和 `ignore.t2` 均不匹配过滤规则 |
| `RENAME TABLE test.t1 TO test.t2, ignore.t1 TO test.t3` | 报错 | 报错 | `ignore.t1` 不匹配而 `test.t3` 匹配过滤规则 |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3` | 报错 | 同步 | 通过临时表名 `test.t4` 交换两个表的名字，新架构保留各个重命名步骤的顺序 |

新架构将一次多表 Rename 作为一个整体协调相关表的同步进度，但下游 SQL 会被重建为多条单表 Rename。MySQL Sink 执行由分号分隔的多条子语句，Kafka 和 Pulsar Sink 则拆分为单表 DDL 消息。因此，下游执行不保证保留上游单条多表 Rename 语句的原子性。使用临时表名互换表名时，需要保留所有相互依赖的步骤，避免通过过滤规则移除其中的步骤。

### DDL 语句注意事项

当在上游执行跨数据库的 DDL 语句（如 `CREATE TABLE db1.t1 LIKE t2`）时，建议在 DDL 语句中显式地指定所有相关的库名（如 `CREATE TABLE db1.t1 LIKE db2.t2`）。否则，由于缺少库名信息，跨数据库的 DDL 语句可能无法正确地在下游执行。

### DDL SQL 文本的处理

TiCDC 会解析、格式化或重建 DDL SQL，因此同步到下游的 SQL 文本不保证与上游原语句逐字一致。新老架构都会规范关键字大小写、标识符引号、空格和部分同义语法，也都会针对 TiDB 特有语法进行兼容处理。`DROP TABLE`、`DROP VIEW` 和 `EXCHANGE PARTITION` 等 DDL 在两种架构中都有 SQL 重建逻辑。

新架构还可能进行以下处理。除特别注明的 MySQL Sink 改写外，这些处理也会影响支持 DDL 的消息协议中的 SQL 字段。具体输出形式可能随 TiCDC 版本变化。

| DDL 或场景 | 新架构的 SQL 文本处理 | 适用条件 |
| --- | --- | --- |
| 单表 Rename | 统一重建为带完整库表名的 `RENAME TABLE db.old_table TO db.new_table` | 包括 `ALTER TABLE ... RENAME AS/TO ...` 和普通 `RENAME TABLE ... TO ...`，未启用表路由时也会改写 |
| 多表 Rename | 按原顺序重建为多条单表 `RENAME TABLE`，每条子语句带尾部 `;` | MySQL Sink 接收组合 SQL；Kafka、Pulsar 等逐表输出的路径会将其拆分为多条消息 |
| 批量建表 | 拆分后的每条 `CREATE TABLE` 语句带尾部 `;` | 上游批量建表产生一个包含多张表的 DDL 事件，且下游按单表事件输出 |
| `CREATE TABLE ... LIKE ...` | 为 `LIKE` 引用表补全库名 | 原 SQL 未限定引用表的库名，且 DDL 元数据表明引用表与目标表位于不同库 |
| `CREATE VIEW` 和 `CREATE OR REPLACE VIEW` | 使用 TiDB 存储的视图查询及 DDL 时刻的库表元数据重建 SQL，可能补全表和列引用的库名、规范标识符大小写或补充列别名 | 视图定义中的名称需要解析时；不要求启用表路由 |
| 匿名二级索引 | 为 `ALTER TABLE ... ADD INDEX/KEY/...` 中未指定名称的索引补上上游生成的索引名，包括一条 `ALTER TABLE` 中的多个变更操作 | 仅在 MySQL Sink 向 MySQL 或 TiDB 执行 DDL 前处理，不适用于 MQ 消息中的 SQL |
| 名称中包含反引号的库、表或分区 | 重建 SQL 时，将名称内的反引号转义为两个反引号 | 包括 Rename、`DROP TABLE`、`DROP VIEW` 和 `EXCHANGE PARTITION` 等需要重建 SQL 的场景 |
| 表路由 | 根据路由规则改写库名、表名及相关引用，并重新生成 SQL | 配置了 `target-schema` 或 `target-table`，详情参见[表路由的 DDL 行为](/ticdc/ticdc-table-routing.md#ddl-行为) |

例如，假设当前数据库为 `db`，未启用表路由，且未过滤以下 Rename 事件，单表 Rename 的输出如下。表中省略语句结束分号。

| 上游 SQL | 老架构输出 | 新架构输出 |
| --- | --- | --- |
| `ALTER TABLE a RENAME AS b` | ``ALTER TABLE `a` RENAME AS `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |
| `ALTER TABLE a RENAME TO b` | ``ALTER TABLE `a` RENAME AS `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |
| `RENAME TABLE a TO b` | ``RENAME TABLE `a` TO `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |

对于 `RENAME TABLE a TO b, c TO d`，按单表事件输出时，老架构第一条 SQL 为 ``RENAME TABLE `db`.`a` TO `db`.`b` ``，新架构为 ``RENAME TABLE `db`.`a` TO `db`.`b`;``。尾部分号来自新架构的多表 DDL 拆分处理。

编写下游消费者或比较新老架构输出时，应解析 SQL 并结合 DDL 类型和库表元数据判断结果，避免依赖 SQL 文本完全相同。库名、表名、索引名及其大小写仍需按具体场景校验，避免忽略名称解析或表路由错误。

### 使用 Event Filter 过滤 DDL 事件的注意事项

如果被过滤的 DDL 语句涉及表的创建或删除，TiCDC 只会过滤掉这些 DDL 语句，而不影响 DML 的同步行为。下面使用具体示例进行说明。

假设你的 changefeed 的配置文件如下：

```toml
[filter]
rules = ['test.t*']

[[filter.event-filters]]
matcher = ["test.t1"] # 该过滤规则只应用于 test 库中的 t1 表
ignore-event = ["create table", "drop table", "truncate table", "rename table"]
```

| DDL | DDL 行为 | DML 行为 | 原因 |
| --- | --- | --- | --- |
| `CREATE TABLE test.t1 (id INT, name VARCHAR(50));` | 忽略 | 同步 | `test.t1` 符合 Event Filter 过滤规则，`CREATE TABLE` 事件被忽略，但不影响 DML 事件的同步 |
| `CREATE TABLE test.t2 (id INT, name VARCHAR(50));` | 同步 | 同步 | `test.t2` 不符合 Event Filter 过滤规则 |
| `CREATE TABLE test.ignore (id INT, name VARCHAR(50));` | 忽略 | 忽略 | `test.ignore` 符合 Table Filter 过滤规则，因此 DDL 和 DML 事件均被忽略 |
| `DROP TABLE test.t1;` | 忽略 | - | `test.t1` 符合 Event Filter，`DROP TABLE` 事件被忽略。该表已被删除，TiCDC 不再同步 t1 的 DML 事件 |
| `TRUNCATE TABLE test.t1;` | 忽略 | 同步 | `test.t1` 符合 Event Filter，`TRUNCATE TABLE` 事件被忽略，但不影响 DML 事件的同步  |
| `RENAME TABLE test.t1 TO test.t2;` | 忽略 | 同步 | `test.t1` 符合 Event Filter，`RENAME TABLE` 事件被忽略，但不影响 DML 事件的同步  |
| `RENAME TABLE test.t1 TO test.ignore;` | 忽略 | 忽略 | `test.t1` 符合 Event Filter，`RENAME TABLE` 事件被忽略，`test.ignore` 符合 Table Filter 过滤规则，因此 DDL 和 DML 事件均被忽略  |

使用 `ignore-sql` 过滤多表 Rename 时，需要注意新老架构的匹配输入不同：老架构在拆分为单表 DDL 事件后匹配每条 SQL；新架构逐表应用事件过滤规则时，匹配的是重建后的整组 Rename SQL。如果同一条事件过滤规则的 `matcher` 匹配多张表，`ignore-sql` 匹配到其中一个重命名步骤，也可能过滤该规则覆盖的其他重命名步骤。切换架构前，应检查此类过滤规则的实际匹配结果。

> **注意：**
>
> - 当同步数据到数据库时，应谨慎使用 Event Filter 过滤 DDL 事件，同步过程中需确保上下游的库表结构始终一致。否则，TiCDC 可能会报错或产生未定义的同步行为。
> - 在 v6.5.8、v7.1.4、v7.5.1 之前的版本中，使用 Event Filter 过滤涉及创建或删除表的 DDL 事件，会影响 DML 的同步，不推荐使用该功能。
