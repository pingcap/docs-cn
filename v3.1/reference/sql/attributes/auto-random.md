---
title: AUTO_RANDOM
category: reference
---

# AUTO_RANDOM <span class="version-mark">从 v3.1.0 版本开始引入</span>

> **警告：**
>
> 当前 `AUTO_RANDOM` 属性为实验功能，**不建议在生产环境中使用**。在后续版本中，`AUTO_RANDOM` 的语法或语义可能会变化。

使用 `AUTO_RANDOM` 功能前，须在 TiDB 配置文件 `experimental` 部分设置 `allow-auto-random = true`。该参数详情可参见 [`allow-auto-random`](/dev/reference/configuration/tidb-server/configuration-file.md#allow-auto-random)。

## 使用场景

`AUTO_RANDOM` 用于解决大批量写数据入 TiDB 时因含有**整型自增主键列**的表而产生的热点问题。详情参阅 [TiDB 高并发写入场景最佳实践](/v3.1/reference/best-practices/high-concurrency.md)。

以下面语句建立的表为例：

```sql
create table t (a int primary key auto_increment, b varchar(255))
```

对这样的表执行大量的未指定主键值的 `INSERT` 语句时，如

```sql
insert into t(b) values ('a'), ('b'), ('c')
```

由于未指定主键列的值（`a` 列），TiDB 会使用连续自增的行值作为行 ID，可能导致单个 TiKV 节点上产生写入热点，进而影响对外提供服务的性能。要避免这种性能下降，可以在执行建表语句时为 `a` 列指定 `AUTO_RANDOM` 属性而不是 `AUTO_INCREMENT` 属性。示例如下：

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random, b varchar(255))
```

或者

{{< copyable "sql" >}}

```sql
create table t (a int auto_random, b varchar(255), primary key (a))
```

此时再执行形如 `INSERT INTO t(b) values...` 的 `INSERT` 语句，

+ 如果该 `INSERT` 语句没有指定整形主键列（`a` 列）的值，TiDB 会为该列自动分配值。该值不保证自增，不保证连续，只保证唯一，避免了连续的行 ID 带来的热点问题。
+ 如果该 `INSERT` 语句显式指定了整形主键列的值，和 `AUTO_INCREMENT` 属性类似，TiDB 会原封不动地保存该值。

自动分配值的计算方式如下：

二进制形式下的最高 5 位（称为 shard bits）由当前事务的开始时间决定，剩下的位数按照自增的顺序分配。

如果希望使用一个不同的 shard bits 的数量，可以在 `AUTO_RANDOM` 后面加一对括号，并在括号中指定，例如：

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random(3), b varchar(255))
```

以上建表语句中，shard bits 的数量为 `3`。shard bits 的数量的取值范围是 `[1, field_max_bits)`，其中 `field_max_bits` 为整形主键列类型占用的位长度。

含有 `AUTO_RANDOM` 属性的表在 `information_schema.tables` 中 `TIDB_ROW_ID_SHARDING_INFO` 一列的值为 `PK_AUTO_RANDOM_BITS=x`，其中 `x` 为 shard bits 的数量。

## 兼容性

TiDB 支持解析版本注释语法。示例如下：

{{< copyable "sql" >}}

```sql
create table t (a int primary key /*T!40000 auto_random */)
```

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random)
```

以上两个语句含义相同。

在 `show create table` 的结果中，`AUTO_RANDOM` 属性会被注释掉。注释会附带一个版本号，例如 `/*T!40000 auto_random */`。其中 `40000` 表示 v4.0.0 引入该功能，低版本的 TiDB 能够忽略带有上述注释的 `AUTO_RANDOM` 属性。

该功能支持向前兼容，即降级兼容。新版本 TiDB 建立的含有 `AUTO_RANDOM` 的表可以被旧版本 TiDB 所使用。

## 使用限制

目前在 TiDB 中使用 `AUTO_RANDOM` 有以下限制：

- 该属性必须指定在整数类型的主键列上，否则会报错。例外情况见[关于 `alter-primary-key` 配置项的说明](#关于-alter-primary-key-配置项的说明)。
- 不支持使用 `ALTER TABLE` 来修改 `AUTO_RANDOM` 属性，包括添加/移除该属性。
- 不支持修改含有 `AUTO_RANDOM` 属性的主键列的列类型。
- 不支持与 `AUTO_INCREMENT` 同时指定在同一列上。
- 不支持与 `DEFAULT` 同时指定在同一列上。
- 插入数据时，不建议自行显式指定含有 `AUTO_RANDOM` 列的值。不恰当地显式赋值，可能会导致该表提前耗尽用于自动分配的数值。因为用于保证唯一性的 rebase 仅针对除 shard bits 以外的位进行。

## 关于 `alter-primary-key` 配置项的说明

- 当 `alter-primary-key = true` 时，不支持使用 `AUTO_RANDOM`。
- 配置文件中的 `alter-primary-key` 和 `allow-auto-random` 两个配置项的值不允许同时为 `true`。
