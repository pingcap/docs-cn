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

> **注意：**
>
> - 如果下游 DML 的执行依赖于未完成同步的索引，DML 可能会执行得很慢，进而影响 TiCDC 的同步延迟。
> - 在同步 DDL 到下游之前，如果 TiCDC 节点宕机或者下游有其他写操作，该 DDL 存在极低的失败概率，你可以自行检查。

### Rename table 类型的 DDL 注意事项

由于同步过程中缺乏一些上下文信息，因此 TiCDC 对 rename table 类型的 DDL 同步有一些约束。

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
| `RENAME TABLE test.n1 TO test.t1` | 报错，并停止同步。 | test.n1 不符合 filter 规则，但是 test.t1 符合 filter 规则，这是非法操作。请参考错误提示信息进行处理 |
| `RENAME TABLE ignore.t1 TO test.t1` | 报错，并停止同步。 | 理由同上 |

#### 一条 DDL 语句内 rename 多个表

如果一条 DDL 语句重命名多个表，则只有当旧的表库名和新的库名都符合过滤规则时，TiCDC 才会同步该 DDL 语句。此外，TiCDC 不支持同步对表名进行交换的 rename table DDL。下面使用具体示例进行说明。

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
