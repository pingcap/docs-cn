---
title: AUTO_RANDOM
category: reference
---

# AUTO_RANDOM <span class="version-mark">从 v4.0.0 版本开始引入</span>

注意：该功能处于实验阶段，不排除后续版本修改语法或语义的可能，__不建议在生产环境直接使用__。另外，auto_random 属性必须在配置文件中添加 `[experimental] allow-auto-shard = true` 的小节后，才能正常使用。

## 简介

auto_random 用于解决大批量写入含有『整型自增主键列』表时的热点问题。参考：[TiDB 高并发写入场景最佳实践](/dev/reference/best-practices/high-concurrency.md)

例如下表

```sql
create table t (a int primary key auto_increment, b varchar(255))
```

在执行大量的没有指定主键值（a 列）的 insert 语句时，由于连续自增的行值作为 row_id，可能导致单个 TiKV 节点上产生写入热点，进而影响对外提供服务的性能。如果不希望有这种性能下降，可以在执行建表语句时为 a 列指定 auto_random 而不是 auto_increment，即

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random, b varchar(255))
```

或者

{{< copyable "sql" >}}

```sql
create table t (a int auto_random, b varchar(255), primary key (a))
```

此时，如果 insert 语句没有指定整形主键列（a 列）的值，TiDB 会自动分配一个，该值不保证自增，不保证连续，只保证唯一，避免了连续 row_id 带来的热点问题；而如果 insert 语句显式指定了整形主键列的值，和 auto_increment 类似，TiDB 会原封不动地保存该值。

自动分配值的计算方式是，二进制形式下的最高 5 位（称为 shard bits）由当前事务的开始时间决定，剩下的位数按照自增的顺序分配。如果希望使用一个不同的 shard bits 的数量，可以使用以下建表语句：

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random(3), b varchar(255))
```

此时，shard_bits 的数量为 3。该数量的取值范围是 [1, field_max_bits)，其中 field_max_bits 为整形主键列类型占用的位长度。

含有 auto_random 的表在 `information_schema.tables` 中 `TIDB_ROW_ID_SHARDING_INFO` 一列的值为 `PK_AUTO_RANDOM_BITS=x`，`x` 为 shard_bits 的数量。

## 兼容性

TiDB 支持解析版本注释语法，例如

{{< copyable "sql" >}}

```sql
create table t (a int primary key /*T!40000 auto_random */)
```

和

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random)
```

具有相同含义。

在 `show create table` 的结果中，auto_random 属性会被注释掉，注释会附带一个版本号，例如 `/*T!40000 auto_random */`，其中 40000 表示 4.0.0 引入该功能，低版本的 TiDB 能够忽略带有上述注释 auto_random 属性。

向前兼容，即降级兼容，新版本 TiDB 建立的含有 auto_random 的表能够被旧版本 TiDB 所使用。

## 局限性

目前 TiDB 中的 auto_random 有以下局限性：

- 必须指定在整数类型的主键列上（例外情况见『关于 alter-primary-key 配置项的说明』一节），否则报错。
- 不支持使用 alter table (change/modify) 来修改 auto_random 属性，包括添加/移除该属性。
- 不支持修改含有 auto_random 属性的主键列的列类型。
- 不支持与 auto_increment 同时指定在同一列上。
- 不支持与 default 指定在同一列上。
- 插入数据时，不建议自行显式指定含有 auto_random 列的值。原因是 rebase 仅针对除 shard_bits 以外的位进行。如果没有考虑到这一点，可能会导致提前耗尽用于自动分配的数值。

## 关于 alter-primary-key 配置项的说明：

- 当 alter-primary-key = true 时，不支持使用 auto_random。
- 配置文件中的 alter-primary-key 和 allow-auto-random 两个配置项的值不允许同时为 true。
