---
title: AUTO_INCREMENT
summary: 介绍 TiDB 的 `AUTO_INCREMENT` 列属性。
aliases: ['/docs-cn/dev/auto-increment/']
---

# AUTO_INCREMENT

本文介绍列属性 `AUTO_INCREMENT` 的基本概念、实现原理、自增相关的特性，以及使用限制。

## 基本概念

`AUTO_INCREMENT` 是用于自动填充缺省列值的列属性。当 `INSERT` 语句没有指定 `AUTO_INCREMENT` 列的具体值时，系统会自动地为该列分配一个值。

出于性能原因，自增编号是系统批量分配给每台 TiDB 服务器的值（默认 3 万个值），因此自增编号能保证唯一性，但分配给 `INSERT` 语句的值仅在单台 TiDB 服务器上具有单调性。

{{< copyable "sql" >}}

```sql
create table t(id int primary key AUTO_INCREMENT, c int);
```

{{< copyable "sql" >}}

```sql
insert into t(c) values (1);
insert into t(c) values (2);
insert into t(c) values (3), (4), (5);
```

```sql
mysql> select * from t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
+----+---+
5 rows in set (0.01 sec)
```

此外，`AUTO_INCREMENT` 还支持显式指定列值的插入语句，此时 TiDB 会保存显式指定的值：

{{< copyable "sql" >}}

```sql
insert into t(id, c) values (6, 6);
```

```sql
mysql> select * from t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
| 6  | 6 |
+----+---+
6 rows in set (0.01 sec)
```

以上用法和 MySQL 的 `AUTO_INCREMENT` 用法一致。但在隐式分配的具体值方面，TiDB 和 MySQL 之间具有较为显著的差异。

## 实现原理

TiDB 实现 `AUTO_INCREMENT` 隐式分配的原理是，对于每一个自增列，都使用一个全局可见的键值对用于记录当前已分配的最大 ID。由于分布式环境下的节点通信存在一定开销，为了避免写请求放大的问题，每个 TiDB 节点在分配 ID 时，都申请一段 ID 作为缓存，用完之后再去取下一段，而不是每次分配都向存储节点申请。例如，对于以下新建的表：

```sql
create table t(id int unique key AUTO_INCREMENT, c int);
```

假设集群中有两个 TiDB 实例 A 和 B，如果向 A 和 B 分别对 `t` 执行一条插入语句：

```sql
insert into t (c) values (1)
```

实例 A 可能会缓存 `[1,30000]` 的自增 ID，而实例 B 则可能缓存 `[30001,60000]` 的自增 ID。各自实例缓存的 ID 将随着执行将来的插入语句被作为缺省值，顺序地填充到 `AUTO_INCREMENT` 列中。

## 基本特性

### 唯一性保证

> **警告：**
>
> 在集群中有多个 TiDB 实例时，如果表结构中有自增 ID，建议不要混用显式插入和隐式分配（即自增列的缺省值和自定义值），否则可能会破坏隐式分配值的唯一性。

例如在上述示例中，依次执行如下操作：

1. 客户端向实例 B 插入一条将 `id` 设置为 `2` 的语句 `insert into t values (2, 1)`，并执行成功。
2. 客户端向实例 A 发送 `Insert` 语句 `insert into t (c) (1)`，这条语句中没有指定 `id` 的值，所以会由 A 分配。当前 A 缓存了 `[1, 30000]` 这段 ID，可能会分配 `2` 为自增 ID 的值，并把本地计数器加 `1`。而此时数据库中已经存在 `id` 为 `2` 的数据，最终返回 `Duplicated Error` 错误。

### 递增性保证

`AUTO_INCREMENT` 列隐式分配值的递增性只能在含有单个 TiDB 实例的集群中得到保证：即对于同一个自增列，先分配的值小于后分配的值；而在含有多个 TiDB 实例的集群中，无法保证自增列的递增性。

例如，对于上述例子，如果先向实例 B 执行一条插入语句，再向实例 A 执行一条插入语句。根据缓存自增 ID 的性质，自增列隐式分配的值可能分别是 `30002` 和 `2`。因此从时间上看，不满足递增性。

### 单调性保证

在含有多个 TiDB 实例的集群中，`AUTO_INCREMENT` 分配值的单调性**只能**单台服务器上得到保证。

例如，对以下表执行以下语句：

```sql
create table t (a int primary key AUTO_INCREMENT)
```

```sql
insert into t values (), (), (), ()
```

即使存在正在执行并发写入的其他 TiDB 实例，或者当前实例剩余的缓存 ID 数量不够，都不会影响分配值的单调性。

### `_tidb_rowid` 的关联性

> **注意：**
>
> 在没有指定整数类型主键的情况下 TiDB 会使用 `_tidb_rowid` 来标识行，该数值的分配会和自增列（如果存在的话）共用一个分配器，其中缓存的大小可能会被自增列和 `_tidb_rowid` 共同消耗。因此会有以下的示例情况：

```sql
mysql> create table t(id int unique key AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t values (),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select _tidb_rowid, id from t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

### 缓存大小控制

TiDB 自增 ID 的缓存大小在早期版本中是对用户透明的。从 v3.1.2、v3.0.14 和 v4.0.rc-2 版本开始，TiDB 引入了 `AUTO_ID_CACHE` 表选项来允许用户自主设置自增 ID 分配缓存的大小。例如：

```sql
mysql> create table t(a int auto_increment key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

mysql> insert into t values();
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> select * from t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)
```

此时如果将该列的自增缓存无效化，重新进行隐式分配：

```sql
mysql> delete from t;
Query OK, 1 row affected (0.01 sec)

mysql> rename table t to t1;
Query OK, 0 rows affected (0.01 sec)

mysql> insert into t1 values()
Query OK, 1 row affected (0.00 sec)

mysql> select * from t;
+-----+
| a   |
+-----+
| 101 |
+-----+
1 row in set (0.00 sec)
```

可以看到再一次分配的值为 `101`，说明该表的自增 ID 分配缓存的大小为 `100`。

此外如果在批量插入的 `INSERT` 语句中所需连续 ID 长度超过 `AUTO_ID_CACHE` 的长度时，TiDB 会适当调大缓存以便能够保证该语句的正常插入。

### 自增步长和偏移量设置

从 v3.0.9 和 v4.0.rc-1 开始，和 MySQL 的行为类似，自增列隐式分配的值遵循 session 变量 `@@auto_increment_increment` 和 `@@auto_increment_offset` 的控制，其中自增列隐式分配的值 (ID) 将满足式子 `(ID - auto_increment_offset) % auto_increment_increment == 0`。

## 使用限制

目前在 TiDB 中使用 `AUTO_INCREMENT` 有以下限制：

- 必须定义在主键或者唯一索引的列上。
- 只能定义在类型为整数、`FLOAT` 或 `DOUBLE` 的列上。
- 不支持与列的默认值 `DEFAULT` 同时指定在同一列上。
- 不支持使用 `ALTER TABLE` 来添加 `AUTO_INCREMENT` 属性。
- 支持使用 `ALTER TABLE` 来移除 `AUTO_INCREMENT` 属性。但从 TiDB 2.1.18 和 3.0.4 版本开始，TiDB 通过 session 变量 `@@tidb_allow_remove_auto_inc` 控制是否允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 来移除列的 `AUTO_INCREMENT` 属性，默认是不允许移除。
