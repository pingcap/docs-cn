---
title: Changefeed DDL 同步
summary: 了解 TiCDC 支持同步的 DDL 和一些特殊情况
---

# Changefeed DDL 同步

本文档介绍了 TiCDC 同步 DDL 的规则和特殊情况。

## DDL 白名单

目前 TiCDC 在同步 DDL 时使用白名单策略，只有在白名单中的 DDL 操作才会被同步到下游系统，不在白名单中的 DDL 操作将不会被 TiCDC 同步。

以下为 TiCDC 支持同步的 DDL 的列表。

- create database
- drop database
- create table 
- drop table 
- add column 
- drop column
- create index / add index 
- drop index 
- truncate table 
- modify column 
- rename table 
- alter column default value
- alter table comment 
- rename index 
- add partition
- drop partition 
- truncate partition 
- create view 
- drop view 
- alter table character set 
- alter database character set
- recover table 
- add primary key 
- drop primary key 
- rebase auto id
- alter table index visibility 
- exchange partition 
- reorganize partition 
- alter table ttl 
- alter table remove ttl

## DDL 同步注意事项

### 创建和添加索引 DDL 的异步执行

为了减小对 Changefeed 同步延迟的影响，如果下游是 TiDB，TiCDC 会异步执行创建和添加索引的 DDL 操作，即 TiCDC 将 `ADD INDEX` 和 `CREATE INDEX` DDL 同步到下游执行后，会立刻返回，而不会等待 DDL 操作完成。这样可以避免阻塞后续的 DML 执行。

当 `ADD INDEX` 或 `CREATE INDEX` DDL 操作在下游执行期间，TiCDC 执行同一张表的下一条 DDL 时，这条 DDL 可能长期被阻塞在 `queueing` 状态，导致其被 TiCDC 重复执行多次，重试时间过长时还会导致同步任务失败。从 v6.5.11 开始，如果拥有下游数据库的 `SUPER` 权限，TiCDC 会定期执行 `ADMIN SHOW DDL JOBS` 查询异步执行的 DDL 任务的状态，等到索引创建完成后再继续同步。这期间虽然同步任务的延迟会加剧，但避免了同步任务失败的问题。

> **注意：**
>
> - 如果下游 DML 的执行依赖于未完成同步的索引，DML 可能会执行得很慢，进而影响 TiCDC 的同步延迟。
> - 在同步 DDL 到下游之前，如果 TiCDC 节点宕机或者下游有其他写操作，该 DDL 存在极低的失败概率，你可以自行检查。

### Rename table 类型的 DDL 注意事项

由于同步过程中缺乏一些上下文信息，因此 TiCDC 对 rename table 类型的 DDL 同步有一些约束。

### 一条 DDL 语句内 rename 单个表

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

### 一条 DDL 语句内 rename 多个表

如果一条 DDL 语句重命名多个表，则只有当**旧的表库名**和**新的库名**都符合过滤规则时，TiCDC 才会同步该 DDL 语句。此外，TiCDC 不支持同步对表名进行交换的 rename table DDL。下面使用具体示例进行说明。

假设你的 changefeed 的配置文件如下：

```toml
[filter]
rules = ['test.t*']
```

那么，TiCDC 对该类型的处理行为如下表所示：

| DDL | 是否同步 | 原因 |
| --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4` | 同步 | 新旧表库名都符合 filter 规则 |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2` | 同步 | 旧的表库名，新的库名都符合 filter 规则 |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;` | 报错 | 新的库名 ignore 不符合 filter 规则 |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | 报错 | 在一条 DDL 中交换 test.t1 和 test.t3 两个表的名字，TiCDC 无法正确处理。请参考错误提示提示信息处理。 |

### SQL 模式

TiCDC 默认采用 TiDB 的默认 SQL 模式来解析 DDL 语句。如果你的上游 TiDB 集群使用了非默认的 SQL 模式，你需要在 TiCDC 的配置文件中指定 SQL 模式，否则 TiCDC 可能无法正确解析 DDL。关于 TiDB SQL 模式的更多信息，请参考 [SQL 模式](/sql-mode.md)。

例如，如果你的上游 TiDB 集群设置了 `ANSI_QUOTES` 模式，你需要在 changefeed 的配置文件中指定 SQL 模式：

```toml
# 其中，前面的 "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" 是 TiDB 默认的 SQL 模式
# 后面的 "ANSI_QUOTES" 是你的上游 TiDB 集群添加的 SQL 模式

sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,ANSI_QUOTES"
```

如果未设置 SQL 模式，那么 TiCDC 可能无法正确解析一些 DDL 语句，例如：

```sql
CREATE TABLE "t1" ("a" int PRIMARY KEY);
```

因为在 TiDB 的默认 SQL 模式下，双引号会被视为字符串而不是标志符，这将会导致 TiCDC 无法正确解析该 DDL 语句。

因此，在创建同步任务的时候，建议在配置文件中指定使用上游 TiDB 集群设置的 SQL 模式。

### 使用 Event Filter 过滤 DDL 事件的注意事项

如果被过滤的 DDL 语句涉及表的创建或删除，TiCDC 只会过滤掉这些 DDL 语句，而不影响 DML 的同步行为。下面使用具体示例进行说明。

假设你的 changefeed 的配置文件如下：

```toml
[filter]
rules = ['test.t*']

matcher = ["test.t1"] # 该过滤规则只应用于 test 库中的 t1 表
ignore-event = ["create table", "drop table", "truncate table"]
```

| DDL | DDL 行为 | DML 行为 | 原因 |
| --- | --- | --- | --- |
| `CREATE TABLE test.t1 (id INT, name VARCHAR(50));` | 忽略 | 同步 | `test.t1` 符合 Event Filter 过滤规则，`CREATE TABLE` 事件被忽略，但不影响 DML 事件的同步 |
| `CREATE TABLE test.t2 (id INT, name VARCHAR(50));` | 同步 | 同步 | `test.t2` 不符合 Event Filter 过滤规则 |
| `CREATE TABLE test.ignore (id INT, name VARCHAR(50));` | 忽略 | 忽略 | `test.ignore` 符合 Table Filter 过滤规则，因此 DDL 和 DML 事件均被忽略 |
| `DROP TABLE test.t1;` | 忽略 | - | `test.t1` 符合 Event Filter，`DROP TABLE` 事件被忽略。该表已被删除，TiCDC 不再同步 t1 的 DML 事件 |
| `TRUNCATE TABLE test.t1;` | 忽略 | 同步 | `test.t1` 符合 Event Filter，`TRUNCATE TABLE` 事件被忽略，但不影响 DML 事件的同步  |

> **注意：**
>
> - 当同步数据到数据库时，应谨慎使用 Event Filter 过滤 DDL 事件，同步过程中需确保上下游的库表结构始终一致。否则，TiCDC 可能会报错或产生未定义的同步行为。
> - 在 v6.5.8 之前的版本中，使用 Event Filter 过滤涉及创建或删除表的 DDL 事件，会影响 DML 的同步，不推荐使用该功能。
