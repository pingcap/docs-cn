---
title: TiDB 计算层
summary: 了解 TiDB 数据库的计算层。
---

# TiDB 计算层

基于 TiKV 提供的分布式存储，TiDB 构建了一个兼具事务处理和数据分析能力的计算引擎。本文首先介绍一个将 TiDB 数据库表中的数据映射到 TiKV 中的键值对（Key, Value）的数据映射算法，然后介绍 TiDB 如何管理元数据，最后说明 TiDB SQL 层的架构。

对于计算层所依赖的存储方案，本文仅介绍 TiKV 的行式存储结构。对于 OLAP 服务，TiDB 引入了列式存储方案 [TiFlash](/tiflash/tiflash-overview.md) 作为 TiKV 的扩展。

## 将表数据映射到键值对

本节描述 TiDB 中将数据映射到键值对（Key, Value）的方案。需要映射的数据包括以下两类：

- 表中每一行的数据，以下简称表数据。
- 表中所有索引的数据，以下简称索引数据。

### 表数据到键值对的映射

在关系型数据库中，一张表可能有很多列。要将一行中每列的数据映射到键值对（Key, Value），需要考虑如何构造 Key。首先，在 OLTP 场景中，有很多对单行或多行数据进行增删改查的操作，这需要数据库能够快速读取一行数据。因此，每个键都应该有一个唯一的 ID（显式或隐式）以便快速定位。其次，许多 OLAP 查询需要全表扫描。如果能将表中所有行的键编码到一个范围内，就可以通过范围查询高效地扫描整个表。

基于上述考虑，TiDB 中表数据到键值对的映射设计如下：

- 为确保同一个表的数据保持在一起便于查找，TiDB 为每个表分配一个表 ID，用 `TableID` 表示。表 ID 是一个整数，在整个集群中唯一。
- TiDB 为表中的每一行数据分配一个行 ID，用 `RowID` 表示。行 ID 也是一个整数，在表内唯一。对于行 ID，TiDB 做了一个小优化：如果表有整数类型的主键，TiDB 会使用这个主键的值作为行 ID。

每一行数据按照以下规则编码为一个键值对（Key, Value）：

```
Key:   tablePrefix{TableID}_recordPrefixSep{RowID}
Value: [col1, col2, col3, col4]
```

`tablePrefix` 和 `recordPrefixSep` 都是特殊的字符串常量，用于区分键空间中的其他数据。字符串常量的具体值在[映射关系总结](#映射关系总结)中介绍。

### 索引数据到键值对的映射

TiDB 支持主键和二级索引（包括唯一索引和非唯一索引）。类似于表数据映射方案，TiDB 为表的每个索引分配一个索引 ID，用 `IndexID` 表示。

对于主键和唯一索引，需要根据键值对快速定位对应的 `RowID`，所以这样的键值对按以下方式编码：

```
Key:   tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
Value: RowID
```

对于不需要满足唯一性约束的普通二级索引，一个键可能对应多行。需要根据键的范围查询对应的 `RowID`。因此，键值对必须按照以下规则编码：

```
Key:   tablePrefix{TableID}_indexPrefixSep{IndexID}_indexedColumnsValue_{RowID}
Value: null
```

### 映射关系总结

上述所有编码规则中的 `tablePrefix`、`recordPrefixSep` 和 `indexPrefixSep` 都是用于区分键空间中其他数据的字符串常量，定义如下：

```
tablePrefix     = []byte{'t'}
recordPrefixSep = []byte{'r'}
indexPrefixSep  = []byte{'i'}
```

还需要注意的是，在上述编码方案中，无论是表数据还是索引数据的键编码方案，同一个表中的所有行都有相同的键前缀，一个索引的所有数据也有相同的前缀。具有相同前缀的数据在 TiKV 的键空间中被安排在一起。因此，通过仔细设计后缀部分的编码方案，确保编码前后的比较保持一致，表数据或索引数据就可以有序地存储在 TiKV 中。使用这种编码方案，表中的所有行数据在 TiKV 的键空间中按 `RowID` 有序排列，特定索引的数据也根据索引数据的具体值（`indexedColumnsValue`）在键空间中顺序排列。

### 键值对映射关系示例

本节通过一个简单的例子帮助你理解 TiDB 的键值对映射关系。假设 TiDB 中存在以下表：

```sql
CREATE TABLE User (
     ID int,
     Name varchar(20),
     Role varchar(20),
     Age int,
     PRIMARY KEY (ID),
     KEY idxAge (Age)
);
```

假设表中有 3 行数据：

```
1, "TiDB", "SQL Layer", 10
2, "TiKV", "KV Engine", 20
3, "PD", "Manager", 30
```

每行数据被映射为一个键值对（Key, Value），而且表有一个 `int` 类型的主键，所以 `RowID` 的值就是这个主键的值。假设表的 `TableID` 是 `10`，那么它在 TiKV 中存储的表数据是：

```
t10_r1 --> ["TiDB", "SQL  Layer", 10]
t10_r2 --> ["TiKV", "KV  Engine", 20]
t10_r3 --> ["PD", " Manager", 30]
```

除了主键外，表还有一个非唯一的普通二级索引 `idxAge`。假设 `IndexID` 是 `1`，那么它在 TiKV 中存储的索引数据是：

```
t10_i1_10_1 --> null
t10_i1_20_2 --> null
t10_i1_30_3 --> null
```

上述示例展示了 TiDB 中从关系模型到键值模型的映射规则，以及这种映射方案背后的考虑。

## 元数据管理

TiDB 中的每个数据库和表都有元数据，指示其定义和各种属性。这些信息也需要持久化，TiDB 同样将这些信息存储在 TiKV 中。

每个数据库或表都被分配一个唯一的 ID。作为唯一标识符，当表数据编码为键值对时，这个 ID 会与 `m_` 前缀一起编码到 Key 中。这样构造一个键值对，其中存储序列化的元数据。

此外，TiDB 还使用一个专门的键值对（Key, Value）来存储所有表的结构信息的最新版本号。这个键值对是全局的，每次 DDL 操作状态发生变化时，其版本号就会增加 `1`。TiDB 将这个键值对持久化存储在 PD 服务器中，键为 `/tidb/ddl/global_schema_version`，Value 是 `int64` 类型的版本号值。同时，因为 TiDB 在线应用架构变更，它会保持一个后台线程不断检查存储在 PD 服务器中的表结构信息版本号是否发生变化。这个线程还确保能在一定时间内获取到版本的变化。

## SQL 层概述

TiDB 的 SQL 层，即 TiDB Server，将 SQL 语句转换为键值对操作，将这些操作转发到分布式键值存储层 TiKV，组装 TiKV 返回的结果，最后将查询结果返回给客户端。

这一层的节点是无状态的。这些节点本身不存储数据，而且完全等价。

### SQL 计算

SQL 计算最简单的解决方案是前面章节描述的[表数据到键值对的映射](#表数据到键值对的映射)，它将 SQL 查询映射到 KV 查询，通过 KV 接口获取相应的数据，并执行各种计算。

例如，要执行 `select count(*) from user where name = "TiDB"` SQL 语句，TiDB 需要读取表中的所有数据，然后检查 `name` 字段是否为 `TiDB`，如果是，则返回这一行。过程如下：

1. 构造键范围：表中所有的 `RowID` 都在 `[0, MaxInt64)` 范围内。根据行数据 `Key` 编码规则，使用 `0` 和 `MaxInt64` 可以构造一个左闭右开的 `[StartKey, EndKey)` 范围。
2. 扫描键范围：根据上面构造的键范围读取 TiKV 中的数据。
3. 过滤数据：对于读取的每一行数据，计算 `name = "TiDB"` 表达式。如果结果为 `true`，返回这一行。如果不是，跳过这一行。
4. 计算 `Count(*)`：对于每一行满足要求的数据，累加到 `Count(*)` 的结果中。

**整个过程如下图所示：**

![naive sql flow](/media/tidb-computing-native-sql-flow.jpeg)

这个解决方案直观且可行，但在分布式数据库场景中有一些明显的问题：

- 在扫描数据时，每一行都通过 KV 操作从 TiKV 读取，至少有一次 RPC 开销，如果需要扫描的数据量很大，开销可能会很高。
- 不适用于所有行。不满足条件的数据不需要读取。
- 从这个查询的返回结果来看，只需要满足要求的行数，而不需要这些行的值。

### 分布式 SQL 操作

为了解决上述问题，计算应该尽可能靠近存储节点，以避免大量的 RPC 调用。首先，SQL 谓词条件 `name = "TiDB"` 应该下推到存储节点进行计算，这样只返回有效的行，避免无意义的网络传输。然后，聚合函数 `Count(*)` 也可以下推到存储节点进行预聚合，每个节点只需要返回一个 `Count(*)` 结果。SQL 层将汇总每个节点返回的 `Count(*)` 结果。

下图显示了数据如何逐层返回：

![dist sql flow](/media/tidb-computing-dist-sql-flow.png)

### SQL 层架构

前面几节介绍了 SQL 层的一些功能，希望你对 SQL 语句的处理方式有了基本的了解。实际上，TiDB 的 SQL 层要复杂得多，有许多模块和层次。下图列出了重要的模块和调用关系：

![tidb sql layer](/media/tidb-computing-tidb-sql-layer.png)

用户的 SQL 请求直接或通过 `Load Balancer` 发送到 TiDB Server。TiDB Server 将解析 `MySQL Protocol Packet`，获取请求内容，对 SQL 请求进行语法和语义解析，制定和优化查询计划，执行查询计划，获取和处理数据。所有数据都存储在 TiKV 集群中，所以在这个过程中，TiDB Server 需要与 TiKV 交互并获取数据。最后，TiDB Server 需要将查询结果返回给用户。
