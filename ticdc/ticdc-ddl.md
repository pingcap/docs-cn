---
title: Changefeed DDL 同步
summary: 了解 TiCDC 支持同步的 DDL 和一些特殊情况
---

# Changefeed DDL 同步

## DDL 白名单

目前 TiCDC 在同步 DDL 时使用白名单策略，只有在白名单内部的 DDL 会同步到下游，不在白名单内的 DDL 不会被 TiCDC 同步到下游。

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

## DDl 同步注意事项

由于同步过程中缺乏一些上下文信息，因此 TiCDC 对 rename table 类型的 DDL 同步有一些约束。

### rename table ddl 

在同步 rename table DDL 时，只有旧的表名符合 filter 的规则，才会被同步，下面会使用具体的例子进行说明。

假设你的 changefeed 的配置文件如下

```toml
[filter]
rules = ['db1.t*']
```

那么，TiCDC 对 rename table ddl 的处理行为如下表所示

| DDL | 是否同步 | 原因和处理方式 |
| --- | --- | --- |
| rename table test.t1 to test.t2 | 同步 | test.t1 符合 filter 规则 |
| rename table test.t1 to ignore.t1 | 同步 | test.t1 符合 filter 规则 |
| rename table ignore.t1 to ignore.t2 | 忽略 | ignore.t1 不符合 filter 规则 |
| rename table test.n1 to test.t1 | 报错，并停止同步。 | test.n1 不符合 filter 规则，但是 test.t1 符合 filter 规则，这是非法操作。 请参考错误提示信息进行处理 |
| rename table ignore.t1 to test.t1 | 报错，并停止同步。 | 理由同上 |

### rename tables ddl 

TiCDC 仅会同步新旧库名都包含在 filter 规则中的 rename tables DDL。此外，TiCDC 不支持同步对表名进行交换的 rename tables DDL。下面会用具体的例子进行说明。

假设你的 changefeed 的配置文件如下

```toml
[filter]
rules = ['db1.t*']
```

那么，TiCDC 对 rename tables ddl 的处理行为如下表所示

| DDL | 是否同步 | 原因 |
| --- | --- | --- |
| rename table test.t1 to test.t2, test.t3 to test.t4 | 同步 | 新旧表库名都符合 filter 规则 |
| rename table test.t1 to ignore.t1, test.t2 to test.t22; | 忽略 | ignore 这个库名不符合 filter 规则 |
| rename table test.t1 to test1.t4, test.t3 to test.t1, test.t4 to test.t3; | 报错 | 在一条 DDL 中交换 test.t1 和 test.t3 两个表的名字，TiCDC 无法正确处理。请参考错误提示提示信息处理。 |
